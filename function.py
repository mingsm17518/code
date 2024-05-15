import configparser

# from pathlib2 import Path
from common import UpdateHeader as uph
from common import ExtractSource as sex
# from astropy.visualization import ImageNormalize
# import tqdm
from common import PreProcess as pp
from common.Astrometry import astrometry
from common.Calibration import calibration
from PySide6.QtWidgets import QFileDialog


class Function:

    def __init__(self):
        self.cf = None
        self.fits = None

    def updateHeader(self):
        if self.cf is None:
            print('config is None')
            return
        if self.fits is None:
            print('fits is None')
            return
        cf = self.cf
        fits = self.fits
        print(cf.getraw("UpdateHeader", "essential_keywords"))
        sta, error = uph.update_header(
            fits, essential_keywords=cf.getraw("UpdateHeader", "essential_keywords"),
            update_keywords=cf.getraw("UpdateHeader", "update_keywords"))

        print('更新文件头')

    def correctImage(self):
        if self.fits is None:
            print('fits is None')
            return
        fits = self.fits
        data_calib = pp.correct(fits, bias=None, dark=None, flat=None, write=True)
        print('图像改正')

    def extractStarImage(self):
        if self.cf is None:
            print('config is None')
            return
        if self.fits is None:
            print('fits is None')
            return
        cf = self.cf
        fits = self.fits
        se = sex.StreakExtractor(
            fits.with_suffix(".calib"),
            bkg_box_size=cf.getraw("ExtractSource", "bkg_box_size"),
            seg_threshold=cf.getfloat("ExtractSource", "seg_threshold"),
            seg_npixels=cf.getfloat("ExtractSource", "seg_npixels"), )
        se.extract_source()

        print('星像提取')

    def orientAstronomy(self):
        if self.fits is None:
            print('fits is None')
            return
        cf = self.cf
        fits = self.fits
        state, _, _ = astrometry(fits.with_suffix(".catalog"))

        print(state)

    def calibrateFlow(self):
        if self.fits is None:
            print('fits is None')
            return
        fits = self.fits
        calibration(fits.with_suffix(".catalog").as_posix(), fits)
        print('流量定标')

    def correctImageMerging(self):
        if self.cf is None:
            print('config is None')
            return
        cf = self.cf
        master_bias, _ = pp.combine_bias(
            path=cf.get("Preprocess", "bias_path"),
            wildcard=cf.get("Preprocess", "bias_wildcard"), write=False)

        master_flat, _ = pp.combine_flat(
            path=cf.get("Preprocess", "flat_path"),
            wildcard=cf.get("Preprocess", "flat_wildcard"),
            bias=master_bias, write=False)
        print('校正图像合并')

    def getConfig(self):
        filename = QFileDialog.getOpenFileName(None, 'Open file', '.')
        if filename[0]:
            # 读取配置文件
            self.cf = configparser.ConfigParser(converters={"raw": eval})
            # cf.read('../configure.ini')
            # cf.read('../target.ini')
            self.cf.read(filename[0], encoding='utf-8')
