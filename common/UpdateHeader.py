import astropy.io.fits as fits
import astropy.units as u
from astropy.coordinates import SkyCoord, FK5
from astropy.time import Time, TimeDelta
from pathlib2 import Path
import re


def update_header(a_object, essential_keywords=None, update_keywords=None):
    """
    用于检测、更新测光图像的文件头，计算必要的参数。
    :param a_object: str or Path，需要进行文件头检测和更新的测光图像.
    :param essential_keywords: list, 必备的关键字.
    :param update_keywords: dict, 需要更新的关键字.
    :return: status:状态码；error_lst:运行异常信息.
    """

    # 错误信息
    error_lst = []

    # 打开文件
    try:
        a_object = Path(a_object)
        hduL = fits.open(a_object.as_posix(), mode='update', ignore_missing_end=True)
        header = hduL[0].header
    except FileNotFoundError:
        error_lst.append("测光图像不存在！")

    if error_lst:
        return 1, error_lst


    # 更新文件头参数
    for a_key, a_value in update_keywords.items():
        try:
            header[a_key] = a_value
        except:
            error_lst.append("关键字{}更新错误！".format(a_key))

    if error_lst:
        return 2, error_lst

    # 检查文件头
    for a_key in essential_keywords:
        if a_key in header.keys():
            pass
        else:
            error_lst.append("关键字{}不存在!".format(a_key))

    if error_lst:
        return 3, error_lst

    # 更新时间,检测几种常见的时间格式
    pattern1 = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9.]+$")
    pattern2 = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9.]+$")
    pattern3 = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

    if "EXPTIME" not in header.keys():
        if "EXPOSURE" in header.keys():
            header["EXPTIME"] = header["EXPOSURE"]

    if pattern1.match(header["DATE-OBS"]):
        obs_time = Time(header['DATE-OBS'], format='iso') + TimeDelta(0.5 * header['EXPTIME'], format='sec')

    elif pattern2.match(header["DATE-OBS"]):
        obs_time = Time(header['DATE-OBS'], format='isot') + TimeDelta(0.5 * header['EXPTIME'], format='sec')

    elif pattern3.match(header["DATE-OBS"]):
        obs_time = Time(header['DATE-OBS']+"T"+header["TIME-OBS"], format='isot') + \
                   TimeDelta(0.5 * header['EXPTIME'], format='sec')
    else:
        error_lst.append("观测时间DATE-OBS解析错误！")

    if error_lst:
        return 4, error_lst

    header['JD'] = obs_time.jd
    header['JD2'] = obs_time.jd2

    # 计算J2000坐标系下，图像中心的位置
    try:
        ra = header["RA"]
        dec = header["DEC"]
        ra_dec = SkyCoord(ra, dec, unit=(u.deg, u.deg), frame=FK5, equinox='J' + str(obs_time.jyear))
    except:
        error_lst.append("关键字RA、DEC不存在.")

    # try:
    #     ra = header["HA"]
    #     dec = header["DE"]
    #     ra_dec = SkyCoord(ra/15, dec, unit=(u.hour, u.deg), frame=FK5, equinox='J' + str(obs_time.jyear))
    # except:
    #     error_lst.append("关键字HA、DE不存在.")

    if error_lst:
        return 5, error_lst

    # 计算图像的指向坐标
    ra_dec = ra_dec.transform_to(FK5(equinox='J2000.0'))
    header['CRVAL1'] = ra_dec.ra.deg
    header['CRVAL2'] = ra_dec.dec.deg

    # 更新文件头
    hduL.flush()
    hduL.close()
    return 0, error_lst
