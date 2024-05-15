import configparser
from pathlib2 import Path
import UpdateHeader as uph
import ExtractSource as sex
from astropy.visualization import ImageNormalize
import tqdm
import PreProcess as pp
from Astrometry import astrometry
from Calibration import calibration
from astropy.nddata import CCDData

# 读取配置文件
cf = configparser.ConfigParser(converters={"raw": eval}, interpolation=configparser.ExtendedInterpolation())
# cf.read('../configure.ini')
# cf.read('../target.ini')
cf.read("../test.ini")
# cf.read("../chenxu.ini")

# 校正图像合并
if 0:
    master_bias, _ = pp.combine_bias(
        path=cf.get("Preprocess", "bias_path"),
        wildcard=cf.get("Preprocess", "bias_wildcard"), write=True)

    master_flat, _ = pp.combine_flat(
        path=cf.get("Preprocess", "flat_path"),
        wildcard=cf.get("Preprocess", "flat_wildcard"),
        bias=master_bias, write=True)

# 待处理的测光图像列表

object_path = Path(cf.get("Preprocess", "object_path"))
print(object_path)
fits_list = list(object_path.glob(cf.get("Preprocess", "object_wildcard")))
fits_list.sort()

for a_fits in tqdm.tqdm(fits_list[1:]):

    print(a_fits)

    # 更新文件头
    if 0:
        sta, error = uph.update_header(
            a_fits, essential_keywords=cf.getraw("UpdateHeader", "essential_keywords"),
            update_keywords=cf.getraw("UpdateHeader", "update_keywords"))

        print(sta)

    # 图像改正
    master_bias = None
    master_flat = None
    if 0:
        data_calib = pp.correct(a_fits, bias=master_bias, dark=None, flat=master_flat, write=True)

    # 星像提取
    if 1:
        se = sex.StreakExtractor(
            a_fits.with_suffix(".calib"),
            bkg_box_size=cf.getraw("ExtractSource", "bkg_box_size"),
            seg_threshold=cf.getfloat("ExtractSource", "seg_threshold"),
            seg_npixels=cf.getfloat("ExtractSource", "seg_npixels"),)
        se.extract_source()

    # 天文定位
    if 0:
        astrometry(a_fits.with_suffix(".cata"))

    # 流量定标
    if 0:
        calibration(a_fits.with_suffix(".catalog").as_posix(), a_fits)
