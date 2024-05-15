# -*- coding: utf-8 -*-            
# @Author : Code_ts
# @Time : 2023/9/27 14:58

import smod.code.PointClound as pc
import smod.code.Hough as hg
import smod.code.OutLines as ol
from pathlib2 import Path
from astropy.table import QTable

# 构建点云
def identifyTarget(cat2_list, image_number = 4, p_type = "STREAK", time_moment = 20, noise_length = 2,
                   write_path= None, read_path=None,
                   save_point_clound=True,
                   hough_npoints=3, lines_npoints=4,
                   track='OBJECT'):

    #构建点云
    status1, error1, point_clound, point_clound_denoise, trail_time, vec = pc.read_cata(
        cat2_list, image_number, p_type, time_moment, noise_length)
    if status1 != 0:
        return status1, error1
    # 存储点云，路径自选
    # if False:
    #     point_clound_table = QTable.from_pandas(point_clound)
    #     point_clound_table.write("/mnt/hgfs/B009/test/test1/point_clound.dat", format="ascii.fixed_width",
    #                              overwrite=True)

    # 霍夫变换
    status2, error2, file_lines = hg.hough(point_clound_denoise, hough_npoints)
    if status2 != 0:
        return status2, error2, None
    # 直线决策与输出
    status3, error3, lines_list = ol.judge_output_lines(point_clound, file_lines, trail_time, vec, lines_npoints, track=track)
    if status3 != 0:
        return status3, error3, None
    # 存储点云，路径自选
    # write_path = "/mnt/hgfs/B009/test/test1/"
    if len(lines_list) == 0:
        return 1, ['no lines'], None
    ol.write_txt(write_path, lines_list)

    # 读出文件，路径自选
    # read_path = "/mnt/hgfs/B009/test/test1/20230316211638108.txt"
    # list_lines = ol.read_txt(read_path)
    return 0, [], lines_list

    # status1, error1, point_clound, point_clound_denoise = pc.read_cata(
    #     cat_list,
    #     number=number,
    #     p_type=p_type,
    #     moment=moment,
    #     noise_length=noise_length)
    # # 存储点云，路径自选
    # if save_point_clound:
    #     point_clound_table = QTable.from_pandas(point_clound)
    #     point_clound_table.write("./point_clound.dat", format="ascii.fixed_width", overwrite=True)
    #
    # # 霍夫变换
    # status2, error2, file_lines = hg.hough(point_clound_denoise, npoints=hough_npoints)
    #
    # # 直线决策与输出
    # status3, error3, lines_list = ol.judge_output_lines(point_clound, file_lines, lines_npoints)
    #
    # # 存储点云，路径自选
    # # path = Path(cat_list[0]).parent
    # # for i1 in range(len(lines_list)):
    # #     result = lines_list[i1]
    # #     i1 = str(i1).zfill(2)
    # #     result.write(path.joinpath(i1).with_suffix(".txt"), format="ascii.fixed_width", overwrite=True)
    #
    # write_path = "./datas/"
    # ol.write_txt(write_path, lines_list)
