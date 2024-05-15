# -*- coding: utf-8 -*-            
# @Author : Code_ts
# @Time : 2023/10/6 8:15

import configparser
import sys
import traceback

from pathlib2 import Path
from astropy.table import Table
import numpy as np

sys.path.append(".")
import common.UpdateHeader as uph
import common.ExtractSource as sex
import tqdm
import common.PreProcess as pp
from common.Astrometry import astrometry
# from common.Calibration import calibration
import deim.IdentifyOverlap as io
import deim.DeblendOverlap as do
import smod.code.OutLines as ol
from PySide6.QtCore import Signal, QObject


class DeimProcess(QObject):
    sigProg = Signal(int, int, str)
    sigDebugInfo = Signal(str)
    sigError = Signal(str, str)

    def __init__(self, config_path=None):
        super().__init__()
        self.config_path = config_path

    def run(self, config_path, object_path, object_wildcard, process,
            cat2_path=None, candidate_star_path=None, combine_star_path=None, reference_path=None,
            variable_star_path=None,
            input_path=None, save_path=None, cloud_flag=None, cloud_path=None):

        # 读取配置文件
        cf = configparser.ConfigParser(converters={"raw": eval}, interpolation=configparser.ExtendedInterpolation())
        cf.read(config_path, encoding='utf-8')
        cat_path = cf.get("Calibration", "cat_path")
        track = cf.get('IdentifyTarget', 'track')
        process = process

        i = 0
        max_num = len(process) + 1
        flag_error = 0
        msg_error = ''

        if 1 in process:
            try:
                # 校正图像合并
                i = i + 1
                self.sigProg.emit(i, max_num, '校正图像合并')
                self.sigDebugInfo.emit('校正图像合并...')
                master_bias, error_list1 = pp.combine_bias(
                    path=cf.get("Preprocess", "bias_path"),
                    wildcard=cf.get("Preprocess", "bias_wildcard"), write=True)

                master_flat, error_list2 = pp.combine_flat(
                    path=cf.get("Preprocess", "flat_path"),
                    wildcard=cf.get("Preprocess", "flat_wildcard"),
                    bias=master_bias, write=True)

                if error_list1 and len(error_list1) != 0:
                    flag_error = 1
                    msg_error = ';'.join(error_list1)

                if error_list2 and len(error_list2) != 0:
                    flag_error = 1
                    if msg_error:
                        msg_error = msg_error + ';'
                    msg_error = msg_error + ';'.join(error_list2)
            except Exception as e:
                msg_error = str(e)
                self.sigError.emit(msg_error, traceback.format_exc())
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '校正图像合并失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]校正图像合并失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return flag_error, '[错误]校正图像合并失败'

        # 待处理的测光图像列表
        object_path = Path(object_path)
        fits_list = list(object_path.glob(object_wildcard))
        fits_list.sort()

        try:
            master_bias = cf.get("Preprocess", "master_bias")
        except:
            master_bias = None

        try:
            master_bias = cf.get("Preprocess", "master_flat")
        except:
            master_flat = None
        flag_error = 0
        if 2 in process:
            try:
                i = i + 1
                self.sigProg.emit(i, max_num, '更新文件头')
                self.sigDebugInfo.emit('更新文件头...')
                # 更新文件头
                for a_fits in tqdm.tqdm(fits_list):
                    flag_error, error = uph.update_header(
                        a_fits, essential_keywords=cf.getraw("UpdateHeader", "essential_keywords"),
                        update_keywords=cf.getraw("UpdateHeader", "update_keywords"))
                    if flag_error:
                        msg_error = ';'.join(error)
                        break
            except Exception as e:
                msg_error = str(e)
                self.sigError.emit(msg_error, traceback.format_exc())
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '更新文件头失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]更新文件头失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return flag_error, msg_error

        flag_error = 0
        # 图像改正
        if 3 in process:
            try:
                i = i + 1
                self.sigProg.emit(i, max_num, '图像改正')
                self.sigDebugInfo.emit('图像改正...')
                for a_fits in tqdm.tqdm(fits_list):
                    data_calib, error_list = pp.correct(a_fits, bias=None, dark=None, flat=None, write=True)
                    if error_list and len(error_list) != 0:
                        flag_error = 1
                        msg_error = ';'.join(error_list)
                        break
            except Exception as e:
                msg_error = str(e)
                self.sigError.emit(msg_error, traceback.format_exc())
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '图像改正失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]图像改正失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return flag_error, msg_error

        flag_error = 0
        # 星像提取
        if 4 in process:
            try:
                i = i + 1
                self.sigProg.emit(i, max_num, '星像提取')
                self.sigDebugInfo.emit('星像提取...')
                for a_fits in tqdm.tqdm(fits_list):
                    se = sex.StreakExtractor(
                        a_fits.with_suffix(".calib"),
                        bkg_box_size=cf.getraw("ExtractSource", "bkg_box_size"),
                        seg_threshold=cf.getfloat("ExtractSource", "seg_threshold"),
                        seg_npixels=cf.getfloat("ExtractSource", "seg_npixels"), )
                    se.extract_source()
            except Exception as e:
                msg_error = str(e)
                self.sigError.emit(msg_error, traceback.format_exc())
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '星像提取失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]星像提取失败</font>')
                    return -1, '[错误]星像提取失败'

        flag_error = 0
        # 天文定位
        if 5 in process:
            try:
                i = i + 1
                self.sigProg.emit(i, max_num, '天文定位')
                self.sigDebugInfo.emit('天文定位...')
                for a_fits in tqdm.tqdm(fits_list):
                    flag_error, error_list, wcs = astrometry(a_fits.with_suffix(".cat0").as_posix())
                    if flag_error != 0:
                        msg_error = ';'.join(error_list)
                        break
            except Exception as e:
                msg_error = str(e)
                self.sigError.emit(msg_error, traceback.format_exc())
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '天文定位失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]天文定位失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return flag_error, msg_error

        flag_error = 0
        # 流量定标
        if 6 in process:
            try:
                i = i + 1
                self.sigProg.emit(i, max_num, '流量定标')
                self.sigDebugInfo.emit('流量定标...')
                for a_fits in tqdm.tqdm(fits_list):
                    flag_error, error_list, hdu_xy = calibration(a_fits.with_suffix(".cat1").as_posix(),
                                                                 cat_path=cat_path)
                    if flag_error != 0:
                        msg_error = ';'.join(error_list)
                        break
            except Exception as e:
                msg_error = str(e)
                self.sigError.emit(msg_error, traceback.format_exc())
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '流量定标失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]流量定标失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return flag_error, msg_error
        flag_error = 0
        if 7 in process:
            try:
                # 粘连星像识别，使用霍夫变换
                i = i + 1
                self.sigProg.emit(i, max_num, '粘连星像识别')
                self.sigDebugInfo.emit('粘连星像识别...')
                lines_npoints = int(cf.get("IdentifyTarget", "lines_npoints"))
                path = Path(cf.get("Preprocess", "object_path"))
                cat2_list = list(path.glob("*.cat2"))
                write_path = cf.get("Preprocess", "object_path")

                flag_error, error_list, line_list = io.identifyOverlap(
                    cat2_list,
                    image_number=cf.getint("IdentifyTarget", "image_number"),
                    p_type=cf.get("IdentifyTarget", "ptype"),
                    time_moment=cf.getfloat("IdentifyTarget", "time_moment"),
                    noise_length=cf.getfloat("IdentifyTarget", "noise_length"),
                    save_point_clound=True,
                    hough_npoints=cf.getint("IdentifyTarget", "hough_npoints"),
                    lines_npoints=cf.getint("IdentifyTarget", "lines_npoints"),
                    write_path=write_path,
                    track=track)
                if flag_error != 0:
                    msg_error = ';'.join(error_list)
            except Exception as e:
                msg_error = str(e)
                self.sigError.emit(msg_error, traceback.format_exc())
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '粘连星像识别失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]粘连星像识别失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return flag_error, msg_error

        flag_error = 0
        # 粘连星像分离
        if 8 in process:
            try:
                i = i + 1
                self.sigProg.emit(i, max_num, '粘连星像分离')
                self.sigDebugInfo.emit('粘连星像分离...')
                a_txt = list(object_path.glob("*.txt"))
                a_txt = a_txt[0]
                line_list = ol.read_txt(a_txt)
                ids = line_list.keys()
                for a_id in ids:
                    lines = line_list[a_id]
                    lines["x"] = lines["x"].astype("float")
                    lines["y"] = lines["y"].astype("float")

                    inds = np.where(lines["x"]<0)
                    for i in inds[0]:
                        moving_file = lines.iloc[i]["file"]
                        moving_file = object_path.joinpath(moving_file)
                        fixed_file = lines.iloc[i - 1]["file"]
                        fixed_file = object_path.joinpath(fixed_file)
                        position = (lines.iloc[i - 1]["y"].astype("int"), lines.iloc[i - 1]["x"].astype("int"))
                        do.deblendOverlap(moving_file, fixed_file, position=position)
            except Exception as e:
                msg_error = str(e)
                self.sigError.emit(msg_error, traceback.format_exc())
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '粘连星像分离失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]粘连星像分离失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return flag_error, msg_error
        i = i + 1
        self.sigProg.emit(i, max_num, 'Done!')
        self.sigDebugInfo.emit('<font color="green">[运行成功]</font>')