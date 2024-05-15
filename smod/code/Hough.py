import os
import uuid
import warnings
import pandas as pd
import numpy as np
from pathlib2 import Path
warnings.filterwarnings("ignore")

def hough(point_clound_denoise, npoints = 2):
    """
    霍夫变换
    :param point_clound_denoise: dataframe，必备，降噪点云.
    :param npoints: int, 默认为2，直线最小点数(2(自动模式)/>2(手动输入)).
    :return: status:状态码；error_lst:运行异常信息；file_lines:直线结果.
    """
    #错误信息
    error_lst=[]
    
    #存储
    point_clound_denoise_name = str(uuid.uuid1())
    input_file = "point_clound_denoise_"+point_clound_denoise_name+".dat"
    point_clound_denoise.to_csv(input_file, index=False, header=False)
    
    #没有point_clound_denoise.dat文件，报错
    if not os.path.exists(input_file):
        error_lst.append(input_file+"不存在")
        file_lines = None
        return 1, error_lst, file_lines
    
    #计算步长
    IX = min(point_clound_denoise.xcen)
    AX = max(point_clound_denoise.xcen)
    IY = min(point_clound_denoise.ycen)
    AY = max(point_clound_denoise.ycen)
    IT = min(point_clound_denoise.zcen)
    AT = max(point_clound_denoise.zcen)
    step = round(pow((pow(AX-IX,2)+pow(AY-IY,2)+pow(AT-IT,2)),0.5)*0.0032)
    
    #计算点数
    Tt = list(np.unique(point_clound_denoise.zcen))
    Tt.sort()
    
    if npoints == 2:
        npoints = int(len(Tt)/4)
        npoints = max(npoints, 4)
    elif npoints < 2:
        error_lst.append("直线点数太少，建议加大npoints")
        file_lines = None
        return 2, error_lst, file_lines
    
    #霍夫变换
    output_file = str(uuid.uuid1())+"_result.csv"

    os.system(os.getcwd() + "/smod/code/hough3dlines "+input_file+" -o "+output_file+" -dx "+str(step)+" -minvotes "+str(npoints))
    
    #删除文件
    os.remove(input_file)
    
    #没有result.csv文件，报错
    # print(output_file)
    if not os.path.exists(output_file):
        error_lst.append(output_file+"不存在")
        file_lines = None
        return 3, error_lst, file_lines
    
    #读取结果
    file = open(output_file, 'r')
    file_lines = file.readlines()
    file.close()
    #删除文件
    os.remove(output_file)
    
    return 0, error_lst, file_lines



