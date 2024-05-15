import os
import warnings
import itertools
import numpy as np
import pandas as pd
from pathlib2 import Path
from astropy.time import Time
import astropy.io.fits as fits
from astropy.table import Table
from astropy.table import vstack
warnings.filterwarnings("ignore")
from astropy.stats import sigma_clip


def judge_output_lines(point_clound, file_lines, trail_time, vec, npoints=4, track="STAR"):
    """
    判断直线，输出直线
    :param point_clound: dataframe，必备，点云.
    :param file_lines: list，必备，直线结果.
    :param trail_time: float，必备，时间尺寸.
    :param vec: vector，必备，图像速度.
    :param npoints: int, 默认为4，直线最小点数(4/!=4(手动输入)).
    :return: status:状态码；error_lst:运行异常信息；lines_list:目标列表.
    """
    #错误信息
    error_lst=[]
    
    #半高全宽平均值
    point_fwhm = np.mean(sigma_clip(point_clound.fwhm, sigma_lower=2, sigma_upper=2, maxiters=None, \
                                    cenfunc=np.mean, masked=False))
    
    #计算步长
    IX = min(point_clound.xcen)
    AX = max(point_clound.xcen)
    IY = min(point_clound.ycen)
    AY = max(point_clound.ycen)
    IT = min(point_clound.zcen)
    AT = max(point_clound.zcen)
    step = round(pow((pow(AX-IX,2)+pow(AY-IY,2)+pow(AT-IT,2)),0.5)*0.0032)
    
    #时间列表
    Tt = list(np.unique(point_clound.zcen))
    Tt.sort()
    image_number = len(Tt)
    
    if npoints > image_number:
        error_lst.append("npoints太大，超过图像数量，请重新输入")
        line_output = False
        return 2, error_lst, line_output

    # 距离和
    def length(cx1, cy1, cx2, cy2, x2, y2):
        d = pow(pow(cx1 - x2, 2) + pow(cy1 - y2, 2), 0.5) + pow(pow(cx2 - x2, 2) + pow(cy2 - y2, 2), 0.5)
        return d

    # 距离
    def high(x1, y1, x2, y2):
        d = pow(pow(x1 - x2, 2) + pow(y1 - y2, 2), 0.5)
        return d

    # 索引判定
    def include(index_list):
        index_min = min(index_list)
        index_max = max(index_list)
        dx_list = list(range(1, int((index_max - index_min) / 3) + 1, 1))
        for dx1 in dx_list:
            for dx2 in range(dx1):
                dx_list1 = list(range(index_min + dx2, index_max + 1, dx1))
                if len(dx_list1) > 2:
                    for dx3 in range(len(dx_list1) - 2):
                        dx_list2 = dx_list1[dx3:dx3 + 3]
                        if all(dx4 in index_list for dx4 in dx_list2):
                            return True

    # 直线判断
    line_list = []
    for i1 in range(len(file_lines)):
        fg1 = file_lines[i1].split("(")
        fg2_1, fg2_2 = fg1[1].split(")")[0], fg1[2].split(")")[0]
        fg3_1, fg3_2 = fg2_1.split(","), fg2_2.split(",")
        a1, a2, a3, b1, b2, b3 = float(fg3_1[0]), float(fg3_1[1]), float(fg3_1[2]), float(fg3_2[0]), float(fg3_2[1]), float(fg3_2[2])
        # 斜率
        k_min = 20 / (pow((pow(AX - IX, 2) + pow(AY - IY, 2) + pow(AT - IT, 2)), 0.5) / int(image_number / (npoints - 1)))
        k_max = (max(Tt) - min(Tt)) / pow(pow(max(Tt) - min(Tt), 2) + pow(len(Tt), 2), 0.5)
        if k_min <= abs(b3) <= k_max:
            line_vec = np.array([b1, b2, b3])
            line_vec = line_vec * (trail_time / line_vec[2])
            dvec = line_vec - vec
            model = np.linalg.norm(dvec)
            point_list, point_xcen, point_ycen, index_list, point_snr, point_length, inter_x, inter_y = [], [], [], [], [], [], [], []
            point_x, point_y = [], []
            point_sum = 0
            dxcen = (20 / b3) * b1
            dycen = (20 / b3) * b2
            track_judge = (track == "TARGET")
            if model < 10 * point_fwhm or track_judge:
                for i2 in range(len(Tt)):
                    c = (Tt[i2] - a3) / b3
                    x1 = (c * b1) + a1
                    y1 = (c * b2) + a2
                    if IX <= x1 <= AX and IY <= y1 <= AY:
                        point_sum = point_sum + 1
                        sma = (point_fwhm) / pow(1 - pow(b3, 2), 0.5)
                        smc = b3 * sma
                        dx = smc * (b1 / pow(pow(b1, 2) + pow(b2, 2), 0.5))
                        dy = smc * (b2 / pow(pow(b1, 2) + pow(b2, 2), 0.5))
                        cx1, cy1 = x1 + dx / 2, y1 + dy / 2
                        cx2, cy2 = x1 - dx / 2, y1 - dy / 2
                        point_index_list = \
                            point_clound[(point_clound.zcen == Tt[i2]) & \
                                         (length(cx1, cy1, cx2, cy2, point_clound.xcen, point_clound.ycen) <= 3 * sma)].index.tolist()
                        if len(point_index_list) > 0:
                            high_list1 = []
                            for i3 in range(len(point_index_list)):
                                high1 = high(x1, y1, point_clound.xcen[point_index_list[i3]],
                                             point_clound.ycen[point_index_list[i3]])
                                high_list1.append(high1)
                            index = point_index_list[high_list1.index(min(high_list1))]
                            point_xcen.append(point_clound.xcen.loc[index])
                            point_ycen.append(point_clound.ycen.loc[index])
                            point_x.append(point_clound.x.loc[index])
                            point_y.append(point_clound.y.loc[index])
                            inter_x.append(x1)
                            inter_y.append(y1)
                            point_snr.append(point_clound.snr.loc[index])
                            point_length.append(point_clound.fwhm.loc[index])
                            point_list.append(index)
                            index_list.append(int(Tt[i2] / 20))

                point_number = len(point_list)
                if point_number >= npoints:
                    index_diff = [index_list[p + 1] - index_list[p] for p in range(len(index_list) - 1)]
                    x_diff = [point_xcen[px + 1] - point_xcen[px] for px in range(len(point_xcen) - 1)]
                    y_diff = [point_ycen[py + 1] - point_ycen[py] for py in range(len(point_ycen) - 1)]
                    xx_diff = [x_diff[px] - dxcen * index_diff[px] for px in range(len(x_diff))]
                    yy_diff = [y_diff[py] - dycen * index_diff[py] for py in range(len(y_diff))]
                    xx_std, xx_mean, yy_std, yy_mean = \
                        np.std(xx_diff), np.mean(xx_diff), np.std(yy_diff), np.mean(yy_diff)
                    point_length = sigma_clip(point_length, sigma_lower=2, \
                                              sigma_upper=2, maxiters=None, cenfunc=np.mean, masked=False)
                    length_number = len(point_length)
                    point_dx = abs(point_x[-1] - point_x[0])
                    point_dy = abs(point_y[-1] - point_y[0])

                    if xx_std <= point_fwhm and yy_std <= point_fwhm and length_number >= npoints:
                        if length_number >= 10:
                            line_list.append(point_list)
                        elif include(index_list):
                            line_list.append(point_list)
    
    #合并相同直线
    result_list = list(range(len(line_list)))
    result_com = itertools.combinations(result_list,2)
    
    for result_a in result_com:
        com_a = line_list[result_a[0]]
        com_b = line_list[result_a[1]]
        if len(set(com_a).intersection(set(com_b))) >= 2:
            com_c = list(set(com_a).union(set(com_b)))
            line_list[result_a[0]] = com_c
            line_list[result_a[1]] = com_c
    
    line_list = list(set(tuple(sorted(sub)) for sub in line_list))
    line_list = [list(sub) for sub in line_list]
    
    #输出直线
    Ttime = list(np.unique(point_clound.time))
    Ttime.sort()
    lines_list = []
    for i5 in range(len(line_list)):
        
        line = line_list[i5]
        jd_time,file,time,x,y,ra,dec,flux,mag,snr,fwhm = [],[],[],[],[],[],[],[],[],[],[]
        
        for i6 in range(len(line)):
            
            file.append(point_clound.file.loc[line[i6]])
            jd_time.append(point_clound.time.loc[line[i6]])
            time_jd = Time(point_clound.time.loc[line[i6]], format="jd")
            time_jd.format = "isot"
            time.append(str(time_jd))
            x.append(round(point_clound.x.loc[line[i6]],2))
            y.append(round(point_clound.y.loc[line[i6]],2))
            ra.append(round(point_clound.ra.loc[line[i6]],6))
            dec.append(round(point_clound.dec.loc[line[i6]],6))
            flux.append(round(point_clound.flux.loc[line[i6]],2))
            mag.append(round(point_clound.mag.loc[line[i6]],4))
            snr.append(round(point_clound.snr.loc[line[i6]],2))
            fwhm.append(round(point_clound.fwhm.loc[line[i6]],2))
        
        result = Table([file,time,x,y,ra,dec,flux,mag,snr,fwhm], \
                       names = ("file","time","x","y","ra","dec","flux","mag","snr","fwhm"))
        if len(Ttime) > len(jd_time):
            time_sub = list(set(Ttime) - set(jd_time))
            time_lost,file_lost = [],[]
            for i7 in range(len(time_sub)):
                lost_time = Time(time_sub[i7], format="jd")
                lost_time.format = "isot"
                time_lost.append(str(lost_time))
                file_lost.append(point_clound[point_clound.time == time_sub[i7]].file.iloc[0])
                
            lost = [-99 for lostt in range(len(time_lost))]
            result2 = Table([file_lost,time_lost,lost,lost,lost,lost,lost,lost,lost,lost], \
                            names = ("file","time","x","y","ra","dec","flux","mag","snr","fwhm"))
            result = vstack([result,result2])
        result.sort(keys='time')
        lines_list.append(result)
        
    if len(lines_list) == 0:
        error_lst.append('no lines')
        return 1, error_lst, lines_list

    return 0, error_lst, lines_list
def write_txt(path, lines_list, image_path=None):
    file = open(path+"".join([char for char in lines_list[0]['time'][0] if char.isdigit()])+".txt", "w")
    if image_path:
        file.write("#image_path:"+image_path + "\n")
    file.write("#image_number:"+str(len(lines_list[0])))
    file.write("\n#object_number:"+str(len(lines_list)))
    file.write\
    ("\n#COL1:file\n#COL2:time\n#COL3:x\n#COL4:y\n#COL5:ra\n#COL6:dec\n#COL7:flux\n#COL8:mag\n#COL9:snr\n#COL10:fwhm")
    for i1 in range(len(lines_list)):
        line = lines_list[i1].pformat_all(show_name = False, show_unit = False, align = '0=')
        i2 = str(i1+1).zfill(3)
        file.write("\n#ID:"+i2)
        for source in line:
            file.write("\n")
            file.write(source)
    file.close()

def read_txt(path):
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    data = [line.strip() for line in lines]
    image_number = int(data[0].split(":")[1])
    object_number = int(data[1].split(":")[1])
    list_lines = {}
    for i1 in range(object_number):
        object_list = []
        for a_line in data[13+11*i1:23+11*i1]:
            object_list.append(list(a_line.split(" ")))
        object_list = pd.DataFrame(object_list, \
                                   columns = ["file","time","x","y","ra","dec","flux","mag","snr","fwhm"])
        keys = data[12+11*i1]
        list_lines[keys] = object_list
    return list_lines