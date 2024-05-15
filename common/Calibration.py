import numpy as np
import pandas as pd
from astropy.modeling import models, fitting
from sklearn.linear_model import LinearRegression
import common.Cross_Match as cm
import catsHTM as cts
from pathlib2 import Path
import astropy.io.fits as fits
import astropy.units as u
from astropy.wcs import WCS
from astropy.time import Time
from astropy.table import Table
from astropy.stats import sigma_clip
from astropy.coordinates import SkyCoord
import astropy.coordinates as coord
import warnings
import concurrent.futures
warnings.filterwarnings("ignore")

# 定义一个函数，防止出现坐标“12 34 56”的情况

def dms_to_degrees(dms_string):
    dms_parts = dms_string.split()  # 将字符串分割为度、分、秒的部分
    degrees = float(dms_parts[0])  # 度部分直接转换为浮点数

    if len(dms_parts) > 1:
        minutes = float(dms_parts[1])
        degrees += minutes / 60.0  # 将分转换为度并加到总度数上

    if len(dms_parts) > 2:
        seconds = float(dms_parts[2])
        degrees += seconds / 3600.0  # 将秒转换为度并加到总度数上

    return degrees

# # 定义一个函数，用于检查xy列表是否具备所需字段
# def check_and_get_missing_columns(dataframe, column_names):
#     existing_columns = dataframe.columns.tolist()
#     missing_columns = [column_name for column_name in column_names if column_name not in existing_columns]

#     if not missing_columns:
#         return True, []
#     else:
#         return False, missing_columns

# 定义一个函数，用于将非字符串元素转换为float类型，保留字符串值


def convert_to_float_or_keep_string(value):
    """
    将非字符串元素转换为float类型，保留字符串值
    :param para: value-具体值;
    :return: value-字符串值；float(value)-非字符串元素的float类型
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def perform_cone_search(catalog_name, cra, cde, radius, catalogs_dir):
    """
    方便使用并行
    :return: data-数据
            names-列名
    """
    data, names, _ = cts.cone_search(catalog_name, np.deg2rad(cra), np.deg2rad(cde), radius, catalogs_dir=catalogs_dir)
    return data, names

def split_image_into_blocks(N1, N2, block_size):
    """
    大视场分割
    :param para: N1,N2-图像xy长度;
                block_size -分割尺寸
    :return: 分割图像
    """
    blocks = []
    for i in range(0, N1, block_size):
        for j in range(0, N2, block_size):
            block = {
                "start_x": i,
                "start_y": j,
                "end_x": min(i + block_size, N1),
                "end_y": min(j + block_size, N2),
            }
            blocks.append(block)
    return blocks

def calibration(xyls: str,cat_path: str):
    """
    流量定标
    :param para: xyls-xy列表绝对路径名+文件名(str)
    :param para: cat_path-星表绝对路径名(str)

    :return:错误码
            1-"参数必须是字符串类型"
            2-"未运行成功，星像列表未提供"
            3-"未运行成功，星像列表文件格式错误"
            4-"未运行成功，wcs文件未提供"
            5-"当前不支持此波段定标"
            6-"标准星数量过少，不能完成定标"

    :return: error_list-错误列表
    :return: hdu_xy-包含位置亮度等信息的table;

    """
    # 错误列表
    error_list = []
    # 检查参数输入格式
    if xyls is not None and not isinstance(xyls, str):
        error_list.append("参数必须是字符串类型")
        return 1, error_list, None

    # 检查星像列表文件
    try:
        hdu = fits.open(Path(xyls), mode='update')
        header = hdu[0].header
        print(header)
    except FileNotFoundError:
        error_list.append("未运行成功，星像列表未提供")
        return 2, error_list, None
    except:
        error_list.append("未运行成功，星像列表文件格式错误")
        return 3, error_list, None

    try:
        hdu_xy = Table(hdu[1].data)
    except:
        error_list.append("未运行成功，星像列表文件格式错误")
        return 3, error_list, None
    data_origin = hdu_xy.to_pandas()

    # 使用apply()方法将函数应用到DataFrame的每个元素
    data = data_origin.apply(convert_to_float_or_keep_string)

    # 检查wcs文件
    try:
        wcs = WCS(header)
    except:
        error_list.append("未运行成功，wcs文件未提供")
        return 4, error_list, None

    # 检查xy列表是否具备所需字段
    # er_lst = check_xyls(data)
    # if er_lst is not None:
    #     return er_lst

    data["mag"] = 25-2.5*np.log10(data["flux_aper"])

    # data = data.loc[data["snr_aper"] >= 8].reset_index(drop=True)
    # data = data.reset_index(drop=True)
    data["ra"], data["dec"] = wcs.pixel_to_world_values(
        data["xcentroid"], data["ycentroid"])

    # 计算大气质量存入df
    try:
        if (len(header["FILTER"]) > 0):
            filter_head = header["FILTER"][0]
        else:
            filter_head = "N"
    except:
        filter_head = "N"
    # longitude = float(header["LONGITUDE"])
    # latitude = float(header["HIERARCH LONGITUDE"])
    try:
        longitude = float(header["SITELONG"])
        latitude = float(header["SITELAT"])
    except:
        longitude = dms_to_degrees(header["SITELONG"])
        latitude = dms_to_degrees(header["SITELAT"])
    if len(header["DATE-OBS"]) > 12:
        t = header["DATE-OBS"]
    else:
        t = header["DATE-OBS"]+"T"+header["TIME-OBS"]
    time = Time(t, format="isot", scale="utc")
    S = time.sidereal_time("apparent", longitude, "IAU2006A").degree

    HA = S-data["ra"]
    secz = 1/(np.sin(latitude*np.pi/180)*np.sin(data["dec"]*np.pi/180)
            + np.cos(latitude*np.pi/180)*np.cos(data["dec"]*np.pi/180)*np.cos(HA*np.pi/180))
    airmass = secz - 0.0018167*(secz-1) - 0.002875 * \
        (secz-1)**2 - 0.0008083*(secz-1)**3

    data["airmass"] = airmass
    hdu_xy["airmass"] = data["airmass"]

    # 交叉匹配
    N1 = header["XSIZE"]
    N2 = header["YSIZE"]
    if filter_head in {"U", "B", "V"}:
        catalog_name = "UCAC4"
    else:
        catalog_name = "GAIADR2"
    if N1/2*header["SCALE"]>7200:
        block_size = int(N1/4)  # 调整块的大小，根据实际情况
        blocks = split_image_into_blocks(N1, N2, block_size)
        tasks = []
        for block in blocks:
            cra, cde = wcs.pixel_to_world_values((block['start_x'] + block['end_x']) / 2, (block['start_y'] + block['end_y']) / 2)

            try:
                radius = (block['end_x'] - block['start_x']) / 2 * header["SCALE"]
            except:
                radius = 7200
            datas,names = perform_cone_search(catalog_name, cra, cde, radius, catalogs_dir=cat_path)
            tasks.append(datas)
        datas=tasks
    else:
        cra, cde = wcs.pixel_to_world_values(N1/2, N2/2)
        try:
            radius = N1/2*header["SCALE"]
        except:
            radius = 1000
        datas,names = perform_cone_search(catalog_name, cra, cde, radius, catalogs_dir=cat_path)



    flag = 0 if catalog_name == "UCAC4" else 1

    reference = pd.DataFrame(datas, columns=names)
    reference["RA"] = np.rad2deg(reference["RA"])
    reference["Dec"] = np.rad2deg(reference["Dec"])
    reference = reference.reset_index(drop=True)

    if len(reference)<=3:
        error_list.append("标准星数量过少，不能完成定标")
        return 6, error_list, None

    if flag == 1:
        # 定义旧历元的坐标和自行
        ra_old = list(reference["RA"])  # 旧历元的赤经（单位：度）
        dec_old = list(reference["Dec"])  # 旧历元的赤纬（单位：度）
        pm_ra = list(reference["PMRA"])    # 赤经自行（单位：mas/yr）
        pm_dec = list(reference["PMDec"])   # 赤纬自行（单位：mas/yr）

        # 定义旧历元的时间
        old_epoch = Time(2015.5, format='jyear')

        # 定义当前时间
        current_time = time

        # 创建 SkyCoord 对象，考虑自行
        coord_old = coord.SkyCoord(ra=ra_old * u.deg, dec=dec_old * u.deg, pm_ra_cosdec=pm_ra * u.mas/u.yr,
                                pm_dec=pm_dec * u.mas/u.yr, obstime=old_epoch)

        # 进行坐标转换到当前历元下
        coord_current = coord_old.apply_space_motion(new_obstime=current_time)

        # 获取转换后的坐标
        reference["RA"] = coord_current.ra.deg
        reference["Dec"] = coord_current.dec.deg

    reference["xcenter"], reference["ycenter"] = wcs.world_to_pixel_values(
        reference["RA"], reference["Dec"])
    idx1, idx2, _idx1, _idx2, d2d, d3d = cm.Cross_match(
        reference["xcenter"].values, reference["ycenter"].values, np.zeros(
            len(reference)),
        data["xcentroid"].values, data["ycentroid"].values, np.zeros(
            len(data)),
        10, 10, frame="cartesian")
    reference1 = reference.iloc[idx1].copy()
    extracted1 = data.iloc[idx2].copy()

    idx1, idx2, _idx1, _idx2, d2d, d3d = cm.Cross_match(
        extracted1["xcentroid"].values, extracted1["ycentroid"].values, np.zeros(
            len(extracted1)),
        reference1["xcenter"].values, reference1["ycenter"].values, np.zeros(
            len(reference1)),
        3, 10, frame="cartesian")

    reference2 = reference1.iloc[idx2].copy()
    extracted2 = extracted1.iloc[idx1].copy()

    # 将匹配成功的 “结果对” 按列的方向连接在一起
    tp = pd.concat([reference2.reset_index(drop=True),
                   extracted2.reset_index(drop=True)], axis=1)
    df = tp.drop_duplicates("RA").reset_index(drop=True)
    data_new = pd.merge(data_origin, df, on=["xcentroid"], how="left")
    hdu_xy["ra"], hdu_xy["dec"] = wcs.pixel_to_world_values(
        hdu_xy["xcentroid"], hdu_xy["ycentroid"])
    # df = df.loc[df["SNR"]>10].reset_index(drop = True)
    # 拟合
    # result_tab = Table()
    df1 = df.loc[~np.isnan(df["mag"])]
    df1 = df1.loc[df1["snr_aper"] >= 8].reset_index(drop=True)
    if filter_head == "N":
        df1 = df1.loc[~np.isnan(df1["Mag_G"])]
        df1 = df1.reset_index()
        # result_tab["cat_mag"] = df1["Mag_G"]
        y0 = np.array(df1["Mag_G"])
        c = np.array(df1["Mag_BP"]-df1["Mag_RP"])
        hdu_xy["mag_cat"] = data_new["Mag_G"]
        hdu_xy["C"] = data_new["Mag_BP"]-data_new["Mag_RP"]
        hdu_xy["mag_cat_error"] = data_new["MagErr_G"]
        str_header = "calibrated with G"
    elif filter_head == "U":
        df1 = df1.loc[~np.isnan(df1["MagU"])]
        df1 = df1.reset_index()
        # result_tab["cat_mag"] = df1["MagU"]
        y0 = np.array(df1["MagU"])
        c = np.array(df1["MagB"]-df1["MagV"])
        hdu_xy["mag_cat"] = data_new["MagU"]
        hdu_xy["C"] = data_new["MagB"]-data_new["MagV"]
        hdu_xy["mag_cat_error"] = data_new["ErrMagU"]
        str_header = "calibrated with U"
    elif filter_head == "B":
        df1 = df1.loc[~np.isnan(df1["MagB"])]
        df1 = df1.reset_index()
        # result_tab["cat_mag"] = df1["MagB"]
        y0 = np.array(df1["MagB"])
        c = np.array(df1["MagB"]-df1["MagV"])
        hdu_xy["mag_cat"] = data_new["MagB"]
        hdu_xy["C"] = data_new["MagB"]-data_new["MagV"]
        hdu_xy["mag_cat_error"] = data_new["ErrMagB"]
        str_header = "calibrated with B"
    elif filter_head == "V":
        df1 = df1.loc[~np.isnan(df1["MagV"])]
        df1 = df1.reset_index()
        # result_tab["cat_mag"] = df1["MagV"]
        y0 = np.array(df1["MagV"])
        c = np.array(df1["MagB"]-df1["MagV"])
        hdu_xy["mag_cat"] = data_new["MagV"]
        hdu_xy["C"] = data_new["MagB"]-data_new["MagV"]
        hdu_xy["mag_cat_error"] = data_new["ErrMagV"]
        str_header = "calibrated with V"
    else:
        df1 = df1.loc[~np.isnan(df1["Mag_G"])]
        df1 = df1.reset_index()
        # result_tab["cat_mag"] = df1["Mag_G"]
        y0 = np.array(df1["Mag_G"])
        c = np.array(df1["Mag_BP"]-df1["Mag_RP"])
        hdu_xy["mag_cat"] = data_new["Mag_G"]
        hdu_xy["C"] = data_new["Mag_BP"]-data_new["Mag_RP"]
        hdu_xy["mag_cat_error"] = data_new["MagErr_G"]
        str_header = "calibrated with G"
    hdu_xy["mag"] = 25-2.5*np.log10(hdu_xy["flux_aper"])

    x0 = np.array(df1["mag"])

    # initialize a linear fitter
    fit = fitting.LinearLSQFitter()

    # initialize the outlier removal fitter
    or_fit = fitting.FittingWithOutlierRemoval(
        fit, sigma_clip, niter=2, sigma=3)

    # initialize a linear model
    line_init = models.Linear1D()

    # fit the data with the fitter
    fitted_line, mask = or_fit(line_init, x0, y0)
    filtered_data = np.ma.masked_array(y0, mask=mask)

    filter_list = [filter_head]*len(df1)

    # result_tab["filter"] = filter_list
    # result_tab["JD"] = df1["JD"]
    # result_tab["ra"] = df1["ra"]
    # result_tab["dec"] = df1["dec"]
    # result_tab["xcentroid"] = df1["xcentroid"]
    # result_tab["ycentroid"] = df1["ycentroid"]
    # result_tab["inst_mag"] = df1["mag"]

    # result_tab["SNR"] = df1["snr_aper"]
    # result_tab["Aper_error"] = 1.0857/df1["snr_aper"]
    # result_tab["Mag_error"] = [0.000]*len(df1)

    automagx = []
    ams = []
    MAG = []
    Mag_error = []
    SNR = []
    color=[]
    # mask = filtered_data != "masked"
    mask = ~filtered_data.mask
    automagx = x0[mask].tolist()
    ams = df1.loc[mask, "airmass"].tolist()
    MAG = y0[mask].tolist()
    color = c[mask].tolist()
    if filter_head == "N":
        Mag_error = df1.loc[mask, "MagErr_G"].tolist()
        # result_tab["Mag_error"][n] = float(df1["MagErr_G"][n])
    elif filter_head == "U":
        Mag_error = df1.loc[mask, "ErrMagU"].tolist()
        # result_tab["Mag_error"][n] = float(df1["ErrMagU"][n])
    elif filter_head == "B":
        Mag_error = df1.loc[mask, "ErrMagB"].tolist()
        # result_tab["Mag_error"][n] = float(df1["ErrMagB"][n])
    elif filter_head == "V":
       Mag_error = df1.loc[mask, "ErrMagV"].tolist()
        # result_tab["Mag_error"][n] = float(df1["ErrMagV"][n])
    else:
        Mag_error = df1.loc[mask, "MagErr_G"].tolist()
    # elif filter_head == "R":
    #     Mag_error.append(df1["ErrMagr"][n])
    #     result_tab["Mag_error"][n] = float(df1["ErrMagr"][n])
    # elif filter_head == "I":
    #     Mag_error.append(df1["ErrMagi"][n])
    #     result_tab["Mag_error"][n] = float(df1["ErrMagi"][n])
    SNR = df1.loc[mask, "snr_aper"].tolist()

    x_tab = pd.DataFrame(columns=["obsmag", "airmass"])
    x_tab["obsmag"] = automagx
    x_tab["airmass"] = ams

    x_tab1 = pd.DataFrame()
    x_tab1["Mag"] = MAG

    x = np.zeros((len(x_tab), 2))
    for i in range(len(x_tab)):
        x[i] = np.array(x_tab.iloc[i])

    y = np.zeros((len(x_tab1), 1))
    for i in range(len(x_tab1)):
        y[i] = x_tab1["Mag"][i]

    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)

    # rb = Table()  # 包含定标星等和星标星等的table
    # rb["Mag"] = MAG
    # rb["fit"] = x_tab["obsmag"]*model.coef_[0][0] + \
    #     x_tab["airmass"]*model.coef_[0][1] + model.intercept_[0]
    # rb["Mag_error"] = Mag_error
    # rb["Aper_error"] = 1.0857/SNR

    # Final Table["MAG"]
    # result_tab["MAG"] = df1["mag"]*model.coef_[0][0] + \
    #     df1["airmass"]*model.coef_[0][1] + model.intercept_[0]

    # 修改头部信息
    header["Fitting"] = "Calibrated Mag=A*mag+B*airmass+C"
    header["calib_passband"] = str_header
    header["A"] = f"{model.coef_[0][0]}"
    header["B"] = f"{model.coef_[0][1]}"
    header["C"] = f"{model.intercept_[0]}"
    # # 保存修改后的FITS文件
    # hdu.flush()

    # 输出
    # 创建一个主要的 HDU（包含文件头）
    primary_hdu = fits.PrimaryHDU(header=header)

    hdu_xy = hdu_xy.to_pandas()
    # 将表格数据保存为一个二进制表格扩展
    hdu_xy["mag_aper"] = model.coef_[0][0]*hdu_xy["mag"]+model.coef_[0][1]*hdu_xy["airmass"]+model.intercept_[0]
    # 格式化
    hdu_xy["xcentroid"] = ["{:.3f}".format(value) for value in hdu_xy["xcentroid"]]
    hdu_xy["ycentroid"] = ["{:.3f}".format(value) for value in hdu_xy["ycentroid"]]
    hdu_xy["background_sum"] = ["{:.3f}".format(value) for value in hdu_xy["background_sum"]]
    hdu_xy["area"] = ["{:.1f}".format(value) for value in hdu_xy["area"]]
    hdu_xy["eccentricity"] = ["{:.4f}".format(value) for value in hdu_xy["eccentricity"]]
    hdu_xy["segment_flux"] = ["{:.4f}".format(value) for value in hdu_xy["segment_flux"]]
    hdu_xy["segment_fluxerr"] = ["{:.4f}".format(value) for value in hdu_xy["segment_fluxerr"]]
    hdu_xy["fwhm"] = ["{:.3f}".format(value) for value in hdu_xy["fwhm"]]
    hdu_xy["exptime"] = ["{:.3f}".format(value) for value in hdu_xy["exptime"]]
    hdu_xy["JD"] = ["{:.9f}".format(value) for value in hdu_xy["JD"]]
    hdu_xy["flux_aper"] = ["{:.4f}".format(value) for value in hdu_xy["flux_aper"]]
    hdu_xy["snr_aper"] = ["{:.4f}".format(value) for value in hdu_xy["snr_aper"]]
    hdu_xy["airmass"] = ["{:.2f}".format(value) for value in hdu_xy["airmass"]]
    hdu_xy["ra"] = ["{:.4f}".format(value) for value in hdu_xy["ra"]]
    hdu_xy["dec"] = ["{:.4f}".format(value) for value in hdu_xy["dec"]]
    hdu_xy["mag"] = ["{:.3f}".format(value) for value in hdu_xy["mag"]]
    hdu_xy["mag_cat"] = ["{:.3f}".format(value) for value in hdu_xy["mag_cat"]]
    hdu_xy["mag_cat_error"] = ["{:.4f}".format(value) for value in hdu_xy["mag_cat_error"]]
    hdu_xy["mag_aper"] = ["{:.3f}".format(value) for value in hdu_xy["mag_aper"]]
    hdu_xy["C"] = round(hdu_xy["C"], 3)
    hdu_xy = Table.from_pandas(hdu_xy)
    table_hdu = fits.BinTableHDU(hdu_xy)

    # 将主要 HDU 和表格 HDU 组合为 HDUList
    hdul = fits.HDUList([primary_hdu, table_hdu])

    # 保存为 FITS 文件
    fits_filename = Path(xyls).with_suffix('.cat2')
    hdul.writeto(fits_filename, overwrite=True)

    # 关闭FITS文件
    hdu.close()

    return 0, error_list, hdu_xy