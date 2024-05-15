import numpy as np
import ccdproc
from tqdm import tqdm
from pathlib2 import Path
import astropy.io.fits as fits
import astropy.units as u
from astropy.nddata import CCDData
import warnings
warnings.filterwarnings('ignore')
from ccdproc import  combine

# class Correct:

#     def __init__(self, path):

#         self.path = path


def combine_bias(path,output_file=None):
    """
    本底图像合并，默认使用中值合并
    使用时需指定文件路径
    :param para: path-目标文件所在路径(字符串格式);output_file-输出文件路径(字符串格式),不输出文件时为空
    :return: master_bias-合并后的本底图像;error_lst-错误列表
    """
    error_lst=[]
    # 本底图像列表
    path = Path(path)
    bias_list = list(path.glob("*BIAS*"))

    if len(bias_list) < 1:
        error_lst.append("本底图像未提供")
        master_bias = 0
        return master_bias,error_lst

    ccd_list = []
    for bias in tqdm(bias_list, desc="combining bias..."):
        ccd = CCDData.read(str(bias), unit="adu", format="fits")
        ccd_list.append(ccd)
    del ccd
    master_bias = combine(ccd_list, method="median", format="fits")

    if output_file is not None:
        # 将函数的输出写入文件
        fits.PrimaryHDU(data=master_bias.data.astype(np.float32)).writeto(output_file+"MASTER_BIAS.fits", overwrite=True)
    
    return master_bias, error_lst


def combine_dark(path,output_file=None):
    """
    暗流图像合并，默认使用中值合并
    使用时需指定文件路径
    :param para: path-目标文件所在路径(字符串格式);output_file-输出文件路径(字符串格式),不输出文件时为空
    :return: master_dark-合并后的暗流图像;error_lst-错误列表
    """
    error_lst=[]
    # 图像列表
    path = Path(path)
    dark_list = list(path.glob("*dark*"))

    if len(dark_list) < 1:
        error_lst.append("暗流图像未提供")
        master_dark = 0
        return master_dark,error_lst

    ccd_list = []
    for dark in tqdm(dark_list, desc="combining dark..."):
        ccd = CCDData.read(str(dark), unit="adu", format="fits")
        ccd_list.append(ccd)
    del ccd
    master_dark = combine(ccd_list, method="median", format="fits")

    if output_file is not None:
        # 将函数的输出写入文件       
        fits.PrimaryHDU(data=master_dark.data.astype(np.float32)).writeto(output_file+"MASTER_DARK.fits", overwrite=True)
    
    return master_dark,error_lst


def combine_flat(path, output_file=None, bias=None, dark=None):
    """
    平场图像合并，默认使用中值合并
    使用时需指定文件路径
    :param para: path-目标文件所在路径(字符串格式);output_file-输出文件路径(字符串格式),不输出文件时为空;
                bias-合并后本底图像所在的路径或变量;dark-合并后暗流图像所在的路径或变量;               
    :return: master_flat-合并后的平场图像;error_lst-错误列表
    """

    error_lst=[]
    # 平场图像列表
    path = Path(path)
    flat_list = list(path.glob("*FLAT*B*"))
    
    if len(flat_list) < 1:
        error_lst.append("平场图像未提供")
        master_flat = 1
        return master_flat,error_lst

    ccd_list = []
    if bias is not None:
        if type(bias) is str:
            # 读取本底图像
            try:
                master_bias = CCDData.read(bias+"MASTER_BIAS.fits", unit="adu", format="fits")
            except FileNotFoundError:
                master_bias = 0
                error_lst.append("合并本底图像未提供")
        else:
            master_bias = bias
    else:
        master_bias = 0
        error_lst.append("合并本底图像未提供")

        
    if dark is not None:
        if type(dark) is str:
            # 读取暗流图像
            try:
                master_dark = CCDData.read(dark+"MASTER_DARK.fits", unit="adu", format="fits")
            except FileNotFoundError:
                master_dark = 0
                error_lst.append("合并暗流图像未提供")
        else:
            master_dark = dark
    else:
        master_dark = 0
        error_lst.append("合并暗流图像未提供")

    for flat in tqdm(flat_list, desc="combining flat..."):
        ccd = CCDData.read(str(flat), unit="adu", format="fits")
        ccd = ccdproc.subtract_bias(ccd, master_bias)
        if master_dark != 0:
            ccd = ccdproc.subtract_dark(ccd, master_dark)
        ccd = ccd.divide(np.median(ccd))
        ccd_list.append(ccd)
    del ccd
    master_flat = combine(ccd_list, method="median", format="fits")
    if output_file is not None:
        # 将函数的输出写入文件    
        fits.PrimaryHDU(data=master_flat.data.astype(np.float32)).writeto(output_file+"MASTER_FLAT.fits", overwrite=True)
    
    return master_flat,error_lst



def correct(path,output_file=None, bias=None, dark=None, flat=None):
    """
    测光图像改正，做减本底除平场
    使用时需指定文件路径
    :param para: path-目标文件所在路径(字符串格式);output_file-输出文件路径(字符串格式),不输出文件时为空;
                bias-合并后本底图像所在的路径或变量;dark-合并后暗流图像所在的路径或变量; flat-合并后平场图像所在的路径或变量
    :return: *.calib-改正后的图像;error_lst-错误列表
    """
    error_lst=[]
    # 图像列表
    path = Path(path)
    
    obj_set = set(list(path.glob("*.fit*")))-set(list(path.glob("*FLAT*")))-set(list(path.glob("*BIAS*")))-set(list(path.glob("*dark*")))
    obj_list = list(obj_set)
    
    if len(obj_list) < 1:
        error_lst.append("图像未提供")
        return error_lst

    if bias is not None:
        if type(bias) is str:
            # 读取本底图像
            try:
                master_bias = CCDData.read(bias+"MASTER_BIAS.fits", unit="adu", format="fits")
            except FileNotFoundError:
                master_bias = 0
                error_lst.append("合并本底图像未提供")
        else:
            master_bias = bias
    else:
        master_bias = 0
        error_lst.append("合并本底图像未提供")

        
    if dark is not None:
        if type(dark) is str:
            # 读取暗流图像
            try:
                master_dark = CCDData.read(dark+"MASTER_DARK.fits", unit="adu", format="fits")
            except FileNotFoundError:
                master_dark = 0
                error_lst.append("合并暗流图像未提供")
        else:
            master_dark = dark
    else:
        master_dark = 0
        error_lst.append("合并暗流图像未提供")


    if flat is not None:
        if type(flat) is str:
            # 读取平场图像
            try:
                master_flat = CCDData.read(flat+"MASTER_FLAT.fits", unit="adu", format="fits")
            except FileNotFoundError:
                master_flat = 0
                error_lst.append("合并平场图像未提供")
        else:
            master_flat = flat
    else:
        master_flat = 0
        error_lst.append("合并平场图像未提供")


    ccd_list=[]
    for obj in tqdm(obj_list, desc="correcting..."):  
        header = fits.getheader(obj)

        ccd = CCDData.read(obj, unit="adu", format="fits")
        ccd = ccdproc.subtract_bias(ccd, master_bias)
        if master_dark != 0:
            ccd = ccdproc.subtract_dark(ccd, master_dark,exposure_time='EXPTIME' , exposure_unit=u.second)
        ccd = ccdproc.flat_correct(ccd, master_flat)
        ccd_list.append(ccd)

        if output_file is not None:
        # 将函数的输出写入文件    
            fits.PrimaryHDU(data=ccd.data.astype(np.float32)).writeto(output_file+obj.stem+".calib", overwrite=True)
    
    return ccd_list,error_lst


        
