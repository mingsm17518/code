import astropy.io.fits as fits
import cv2
import numpy as np
from astropy.convolution import Gaussian2DKernel, convolve
from astropy.stats import SigmaClip
from astropy.table import Table, vstack
from pathlib2 import Path
# from photutils import Background2D, detect_sources, find_peaks
from photutils.aperture import CircularAperture, aperture_photometry, CircularAnnulus, ApertureStats
from photutils.background import MedianBackground, MeanBackground, SExtractorBackground
from photutils.segmentation import SourceCatalog
from scipy.signal import correlate
from photutils.utils import calc_total_error
from photutils.segmentation import deblend_sources


class StreakExtractor:

    def __init__(self, file, bkg_box_size=(64, 64), bkg_filter_size=(3, 3), bkg_estimator="MeanBackground",
                 seg_threshold=1.5, seg_npixels=25, seg_filter_sigma=2.0, seg_filter_size=(5, 5),
                 radius=15, radius_in=18, radius_out=25, gain=None, rdnoise=None,
                 corr_threshold=0.5, ecc_threshold=0.866):
        """
        :param file: 测光图像
        :param bkg_box_size:  背景估计时网格划分的大小
        :param bkg_filter_size: 背景插值时滤波器的尺寸
        :param bkg_estimator: 背景估计方式
        :param seg_threshold: 阈值分割的阈值大小
        :param seg_npixels: 星像的最小面积
        :param seg_filter_sigma: 阈值分割时高斯滤波器的sigma值
        :param seg_filter_size: 阈值分割时高斯滤波器的尺寸
        :param radius: 孔径测光时测光孔径的大小
        :param radius_in: 孔径测光时，背景估计环内径的大小
        :param radius_out: 孔径测光时，背景估计环外径的大小
        :param gain: CCD的gain值
        :param rdnoise: CCD的读出噪声
        :param corr_threshold: 基于模板匹配的星像提取方法，匹配点筛选的阈值，大于该值的匹配点有效
        :param ecc_threshold: 拖长星像（STREAK）与点星像（POINT）的椭率分界点
        """

        # 读取fits图像
        self.file = Path(file)
        with fits.open(self.file.as_posix()) as hduL:
            self.image_calib = hduL[0].data.astype(np.float32)
            self.header = hduL[0].header

        # 初始化提取参数
        self.bkg_box_size = bkg_box_size
        self.bkg_filter_size = bkg_filter_size
        self.bkg_estimator = bkg_estimator

        self.seg_threshold = seg_threshold
        self.seg_npixels = seg_npixels
        self.seg_filter_sigma = seg_filter_sigma
        self.seg_filter_size = seg_filter_size

        self.radius = radius
        self.radius_in = radius_in
        self.radius_out = radius_out

        if gain is None:
            self.gain = self.header["GAIN"]
        else:
            self.gain = gain

        if rdnoise is None:
            self.rdnoise = self.header["RDNOISE"]
        else:
            self.rdnoise = rdnoise

        self.corr_threshold = corr_threshold
        self.ecc_threshold = ecc_threshold

        self.names = ["label", "xcentroid", "ycentroid",
                      "background_sum", "area", "eccentricity",
                      "segment_flux", "segment_fluxerr", "fwhm"]

        # 程序运行状态信息
        self.error_lst = []

    def sub_background(self, box_size=None, filter_size=None, bkg_estimator=None, write=True):
        """

        :param box_size:  背景估计时网格划分的大小
        :param filter_size: 背景插值时滤波器的尺寸
        :param bkg_estimator: 背景估计方式
        :return:
        """

        # 背景估计的窗格大小
        if box_size is None:
            box_size = self.bkg_box_size

        if filter_size is None:
            filter_size = self.bkg_filter_size

        if bkg_estimator is None:
            bkg_estimator = self.bkg_estimator

        if bkg_estimator == "MeanBackground":
            bkg_estimator = MeanBackground()
        elif bkg_estimator == "MedianBackground":
            bkg_estimator = MedianBackground()
        elif bkg_estimator == "SExtractorBackground":
            bkg_estimator = SExtractorBackground()
        else:
            self.error_lst.append("无法识别{}类型".format(bkg_estimator))

        if self.error_lst:
            return 1, self.error_lst, None

        # 背景估计
        bkg = Background2D(self.image_calib, box_size=box_size,
                           filter_size=filter_size,
                           sigma_clip=SigmaClip(sigma=3.0),
                           bkg_estimator=MeanBackground())

        # 减背景
        self.background = bkg.background
        self.background_rms = bkg.background_rms
        self.image = self.image_calib - self.background

        # 将减背景之后的图像写入fits文件
        if write:
            fits.PrimaryHDU(self.image, header=self.header).writeto(self.file.with_suffix(".subback"), overwrite=True)

        return 0, self.error_lst, bkg

    def do_thresholding(self, threshold=None, npixels=None, filter_sigma=None, filter_size=None, check_image=None,
                        mask=None, saturation=65535, write=True):
        """

        :param saturation:饱和水平
        :param threshold:阈值分割的阈值大小
        :param npixels:星像的最小面积
        :param filter_sigma:阈值分割时高斯滤波器的sigma值
        :param filter_size:阈值分割时高斯滤波器的尺寸
        :param check_image:检测图像名称
        :param mask:mask，为True的像素，在阈值分割时将被排除
        :param write:是否将结果写入文件
        :return:
        """

        # 阈值水平
        if threshold is None:
            threshold = self.seg_threshold
        threshold = threshold * self.background_rms

        # 面积阈值
        if npixels is None:
            npixels = self.seg_npixels

        # 滤波器参数
        if filter_sigma is None:
            filter_sigma = self.seg_filter_sigma

        if filter_size is None:
            filter_size = self.seg_filter_size

        # 滤波器
        kernel = Gaussian2DKernel(filter_sigma, x_size=filter_size[0], y_size=filter_size[1])
        kernel.normalize()
        self.image_conv = convolve(self.image, kernel)
        self.kernel = kernel

        # 阈值分割
        mask = self.image_calib > saturation
        self.segmentation = detect_sources(self.image_conv, threshold, npixels=npixels, mask=mask)

        # 清除拖出边缘的星像
        self.segmentation.remove_border_labels(border_width=1, partial_overlap=True, relabel=True)

        # 如果是点星像，进行重叠星像的分离
        if self.header["TRACK"] == "STAR":
            self.segmentation = deblend_sources(
                self.image_conv, self.segmentation, npixels=npixels, nlevels=32, contrast=0.001, progress_bar=False)

        # 计算误差
        self.error = calc_total_error(self.image, self.background_rms, effective_gain=self.gain)

        # 计算拖长星像的各个属性，生成结果，结果保存为Qtable形式
        try:
            self.sourcecatalog = SourceCatalog(
                self.image, self.segmentation, error=self.error,
                convolved_data=self.image_conv, background=self.background)
        except ValueError:
            raise Exception("阈值分割未得到星像.")

        self.catalog_thresh = self.sourcecatalog.to_table(columns=self.names)
        self.catalog_thresh = Table(self.catalog_thresh)
        self.catalog_thresh["exptime"] = self.header["EXPTIME"]
        self.catalog_thresh["file"] = self.file.name
        self.catalog_thresh["JD"] = self.header["JD"]
        self.catalog_thresh["filter"] = self.header["FILTER"]

        # 保存阈值分割得到的图像？
        if check_image:
            hdu = fits.PrimaryHDU(self.segmentation.data)
            hdu.writeto(check_image, overwrite=True)

        # 保存阈值分割的结果
        if write:
            # self.catalog_thresh.write(self.file.with_suffix(".thresh"), format="ascii.fixed_width", overwrite=True)
            self.catalog_thresh.write(self.file.with_suffix(".cat0"), self.header, format="fits")

    def do_aperture(self, radius=None, radius_in=None, radius_out=None, gain=None, rdnoise=None, write=True, ecc_threshold=None):
        """

        :param radius:
        :param radius_in:
        :param radius_out:
        :param gain:
        :param rdnoise:
        :param write:
        :return:
        """

        if radius is None:
            radius = self.radius
        if radius_in is None:
            radius_in = self.radius_in
        if radius_out is None:
            radius_out = self.radius_out

        if gain is None:
            gain = self.header["GAIN"]
        if rdnoise is None:
            rdnoise = self.header["RDNOISE"]

        if ecc_threshold is None:
            ecc_threshold = self.ecc_threshold

        # 孔径测光
        positions = list(zip(self.catalog_thresh["xcentroid"], self.catalog_thresh["ycentroid"]))
        apertures = CircularAperture(positions, r=radius)
        annulus_aperture = CircularAnnulus(positions, r_in=radius_in, r_out=radius_out)
        aperstats = ApertureStats(self.image_calib, annulus_aperture)
        bkg_mean = aperstats.median
        aperture_area = apertures.area_overlap(self.image_calib)
        total_bkg = bkg_mean * aperture_area
        phot_data = aperture_photometry(self.image_calib, apertures)
        phot_data["flux"] = phot_data["aperture_sum"] - total_bkg

        self.catalog_thresh["flux_aper"] = phot_data["flux"]
        self.catalog_thresh["snr_aper"] = (phot_data["flux"] * gain) / (phot_data["aperture_sum"] * gain +
                                                                 np.pi * radius * radius * rdnoise ** 2) ** 0.5
        self.catalog_thresh["type"] = "POINT "
        mask = self.catalog_thresh["eccentricity"] > ecc_threshold
        if len(mask) > 0:
            self.catalog_thresh["type"][mask] = "STREAK"

        if write:
            hdu0 = fits.PrimaryHDU(header=self.header)
            hdu0.header["XSIZE"] = self.header["NAXIS1"]
            hdu0.header["YSIZE"] = self.header["NAXIS2"]

            # 规范数据格式
            self.catalog_thresh['xcentroid'].info.format = '.2f'
            self.catalog_thresh['ycentroid'].info.format = '.2f'
            self.catalog_thresh['background_sum'].info.format = '.2f'
            self.catalog_thresh['area'].info.format = '.2f'
            self.catalog_thresh['eccentricity'].info.format = '.2f'
            self.catalog_thresh['segment_flux'].info.format = '.2f'
            self.catalog_thresh['segment_fluxerr'].info.format = '.2f'
            self.catalog_thresh['fwhm'].info.format = '.2f'
            self.catalog_thresh['flux_aper'].info.format = '.2f'
            self.catalog_thresh['snr_aper'].info.format = '.2f'
            self.catalog_thresh['exptime'].info.format = '.2f'

            hdu1 = fits.BinTableHDU(self.catalog_thresh)
            fits.HDUList([hdu0, hdu1]).writeto(self.file.with_suffix(".cat0"), output_verify="ignore", overwrite=True)

        return self.catalog_thresh

    def make_template(self, num=3, save_mask=False, save_tem=False, ecc_threshold=None):
        """

        :param num:
        :param save_mask:
        :param save_tem:
        :param ecc:
        :return:
        """

        if ecc_threshold is None:
            ecc_threshold = self.ecc_threshold

        object_list = self.catalog_thresh.to_pandas()

        # 按椭率选取模版候选体
        object_list = object_list.loc[object_list["eccentricity"] > ecc_threshold]
        if len(object_list) == 0:
            return None

        # 按流量选取模版候选体
        object_list = object_list.sort_values(by="segment_flux", ascending=False)
        labels = object_list["label"].iloc[0:num]

        # 按相关系数选取模版
        corr_means = []
        for i, label in enumerate(labels):
            temp = self.sourcecatalog.get_label(label)
            template = temp.data_ma.filled(0)
            mask = ~temp.data_ma.mask
            corr_image = cv2.matchTemplate(self.image.astype(np.float32),
                                           template.astype(np.float32),
                                           cv2.TM_CCORR_NORMED,
                                           mask=mask.astype(np.float32))
            corr_mean = np.mean(corr_image[corr_image > 0.3])
            corr_means.append(corr_mean)

        idx = np.where(corr_means == np.max(corr_means))
        if (len(idx[0]) == 0):
            return None
        idx = idx[0][0]
        label = labels.iloc[idx]
        template = self.sourcecatalog.get_label(label)

        self.template = template.data_ma.filled(0)
        self.mask = self.template > 0

        # 保存模板图像？
        if save_tem:
            hdu = fits.PrimaryHDU(self.template)
            hdu.writeto(self.file.with_suffix(".tem"), overwrite=True)

        # 保存蒙版图像？
        if save_mask:
            hdu = fits.PrimaryHDU(self.mask)
            hdu.writeto(self.file.with_suffix(".mask"), overwrite=True)

        return 1

    def do_matching(self, save_image=False):
        """

        :param save_image:
        :return:
        """
        # 计算相关系数
        self.corr_image = cv2.matchTemplate(
            self.image.astype(np.float32),
            self.template.astype(np.float32),
            cv2.TM_CCORR_NORMED,
            mask=self.mask.astype(np.float32))

        # 保存相关系数图像？
        if save_image:
            hdu = fits.PrimaryHDU(self.corr_image)
            hdu.writeto(save_image)

        return self.corr_image

    def match_identify(self, threshold=None, write=None, max_num=np.inf):
        """

        :param threshold:
        :param save_file:
        :param max_num:
        :return:
        """

        if threshold is None:
            threshold = self.corr_threshold

        # 搜索最佳匹配点
        mask = (self.mask).astype("int")
        footprint = correlate(mask, mask, mode="same") > 0
        match_point = find_peaks(
            self.corr_image, threshold=threshold,
            footprint=footprint, border_width=1, npeaks=max_num)
        self.match_point = match_point

        # 保存最佳匹配点？
        if write:
            match_point.write(self.file.with_suffix(".point"), format='ascii.fixed_width', overwrite=True)

        return self.match_point

    def do_PhAst(self, npixels=None, gain=None, rdnoise=None, ecc_threshold=None, write=True):
        """
        定心与测光。
        """

        if gain is None:
            gain = self.gain

        if rdnoise is None:
            rdnoise = self.rdnoise

        if ecc_threshold is None:
            ecc_threshold = self.ecc_threshold

        if npixels is None:
            npixels=self.seg_npixels

        aperture = self.mask
        shape = self.image.shape
        aper_shape = aperture.shape

        # streak_data = np.zeros(self.image.shape)
        streak_data = np.ones_like(self.image, dtype=bool)
        for x, y in zip(self.match_point["x_peak"].astype(np.int32), self.match_point["y_peak"].astype(np.int32)):
            i_low = y
            i_up = min(y + aper_shape[0], shape[0])
            j_low = x
            j_up = min(x + aper_shape[1], shape[1])

            # trail = self.image[i_low:i_up, j_low:j_up] * aperture[0:i_up - i_low, 0:j_up - j_low]
            streak_data[i_low:i_up, j_low:j_up] = streak_data[i_low:i_up, j_low:j_up]*(~aperture)

        streak_seg = detect_sources(self.image, -np.inf, npixels=npixels, mask=streak_data)
        streak_seg.remove_border_labels(border_width=1, partial_overlap=True, relabel=True)
        try:
            streaks = SourceCatalog(
                self.image, streak_seg, error=self.error,
                convolved_data=self.image_conv, background=self.background)
        except:
            raise Exception("阈值分割未得到星像！")

        streaks = streaks.to_table(columns=self.names)
        streaks = Table(streaks)

        streaks["flux_aper"] = streaks["segment_flux"]
        streaks["snr_aper"] = (streaks["segment_flux"] * gain) / (streaks["segment_flux"] * gain +
                                                                  streaks["background_sum"] * gain +
                                                                  streaks["area"] * rdnoise ** 2) ** 0.5
        streaks["type"] = "STREAK"

        # 点目标提取
        # point_data = convolve(self.image-streak_data, self.kernel)
        point_seg = detect_sources(self.image_conv, 1.5 * self.background_rms, npixels=npixels, mask=~streak_data)
        point_seg.remove_border_labels(border_width=1, partial_overlap=True, relabel=True)
        try:
            points = SourceCatalog(
                self.image, point_seg, error=self.error,
                convolved_data=self.image_conv, background=self.background)
        except:
            raise Exception("阈值分割未得到星像！")

        points = points.to_table(columns=self.names)
        points = Table(points)
        mask = points["eccentricity"] < ecc_threshold
        points = points[mask]

        points["flux_aper"] = points["segment_flux"]
        points["snr_aper"] = (points["segment_flux"] * gain) / (points["segment_flux"] * gain +
                                                                points["background_sum"] * gain +
                                                                points["area"] * rdnoise ** 2) ** 0.5
        points["type"] = "POINT"

        catalog = vstack([streaks, points])
        catalog["exptime"] = self.header["EXPTIME"]
        catalog["file"] = self.file.name
        catalog["JD"] = self.header["JD"]
        catalog["filter"] = self.header["FILTER"]
        if write:
            # catalog.write(self.file.with_suffix(".catalog"), format='ascii.fixed_width', overwrite=True)
            # catalog.write(self.file.with_suffix(".cata"), header=self.header, format='fits')
            hdu0 = fits.PrimaryHDU(header=self.header)
            # hdu0.header["NAXIS"] = self.header["NAXIS"]
            hdu0.header["XSIZE"] = self.header["NAXIS1"]
            hdu0.header["YSIZE"] = self.header["NAXIS2"]

            # 规范数据格式
            catalog['xcentroid'].info.format = '.2f'
            catalog['ycentroid'].info.format = '.2f'
            catalog['background_sum'].info.format = '.2f'
            catalog['area'].info.format = '.2f'
            catalog['eccentricity'].info.format = '.2f'
            catalog['segment_flux'].info.format = '.2f'
            catalog['segment_fluxerr'].info.format = '.2f'
            catalog['fwhm'].info.format = '.2f'
            catalog['flux_aper'].info.format = '.2f'
            catalog['snr_aper'].info.format = '.2f'
            catalog['exptime'].info.format = '.2f'

            hdu1 = fits.BinTableHDU(catalog)
            fits.HDUList([hdu0, hdu1]).writeto(self.file.with_suffix(".cat0"), output_verify="ignore", overwrite=True)
            # fits.BinTableHDU(catalog, header=self.header).writeto(self.file.with_suffix(".cata"), overwrite=True)

    def extract_source(self):
        """

        :return:
        """
        self.sub_background(write=False)
        self.do_thresholding(write=False)
        if self.header["TRACK"] == "STAR":
            self.do_aperture()
        elif self.header["TRACK"] == "TARGET":
            self.make_template()
            self.do_matching()
            self.match_identify()
            self.do_PhAst()
