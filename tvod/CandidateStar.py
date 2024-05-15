import re
import warnings
import pandas as pd
from pathlib2 import Path
import astropy.units as u
from astropy.io import fits
from astropy.table import Table
warnings.filterwarnings("ignore")
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from astropy.coordinates import match_coordinates_sky

def Candidate_star(cat2_path, candidate_star_path, ratio = 0.45, number = 200, data_filter = "N", snr = 20, candidate_star_number = 4, dis_thre = 2/3600, save_mode = "w"):
    """
    筛选候选星
    :param cat2_path: str，必备，cat2输入路径.
    :param candidate_star_path: str，必备，候选星存储路径.
    :param ratio: float，默认为0.45，区间:[0.2, 0.5].
    :param number: int，默认为200，候选星最大数目.
    :param data_filter: str，默认为"N"，数据波段.
    :param snr: float，默认为20，候选星最低信噪比.
    :param candidate_star_number: int，默认为4，候选星最小数目.
    :param dis_thre: float，默认为2/3600，匹配阈值.
    :param save_mode: str，必备，存储模式("w"覆盖/"a"不覆盖).
    :return: status:状态码；error_lst:运行异常信息；star_candidate_list:候选星.
    """
    #错误信息
    error_lst=[]
    
    #文件列表
    cat2_path = Path(cat2_path)
    cat2_list = list(cat2_path.glob("*.cat2"))
    cat2_list.sort()
    
    if len(cat2_list) == 0:
        error_lst.append(str(cat2_path)+"没有文件，请重新输入")
        star_candidate_list = None
        return 1, error_lst, star_candidate_list
    
    #ratio, number不在范围内，报错
    if ratio < 0.2 or ratio > 0.5:
        error_lst.append("ratio不在0.2-0.5之内，请重新输入")
        star_candidate_list = None
        return 2, error_lst, star_candidate_list
    
    
    #读文件信息
    def read_cat2(cat2):
        cat_2 = fits.open(cat2)
        a_header = cat_2[0].header
        img_x = a_header["XSIZE"]
        img_y = a_header["YSIZE"]
        data_cat2 = Table(cat_2[1].data).to_pandas()
        data_cat2 = data_cat2[["JD", "filter", "ra", "dec", "xcentroid", "ycentroid", "mag", "snr_aper"]]
        data_cat2 = data_cat2.fillna(-99)
        return data_cat2, img_x, img_y
    
    #筛选候选星
    data_cat2, img_x, img_y = read_cat2(cat2_list[0])
    data_cat2 = data_cat2[data_cat2["filter"] == data_filter]
    data_cat2 = data_cat2[data_cat2["mag"] >= 0]
    cat2_x = (data_cat2["xcentroid"] - 0.5*img_x).abs() < ratio*img_x
    cat2_y = (data_cat2["ycentroid"] - 0.5*img_y).abs() < ratio*img_y
    data_cat2 = data_cat2[cat2_x & cat2_y]
    data_cat2 = data_cat2.sort_values('snr_aper',ascending=False)
    star_candidate = data_cat2[:number]
    star_candidate = star_candidate[star_candidate["snr_aper"] > snr]
    
    if len(star_candidate) < candidate_star_number:
        error_lst.append("候选星数量少于"+str(candidate_star_number)+"颗，请更换输入数据")
        star_candidate_list = None
        return 3, error_lst, star_candidate_list
    
    #匹配
    dis_thre = Angle(dis_thre,unit='deg')
    #cat2_sky = SkyCoord(star_candidate["ra"]*u.degree, star_candidate["dec"]*u.degree, frame='cirs')
    cat2_sky = SkyCoord(star_candidate["ra"], star_candidate["dec"], frame='cirs', unit='deg')
    star_candidate_list = []
    for i in range(len(star_candidate)):
        star_candidate_list.append(star_candidate[i:i+1])
    for a_cat2 in cat2_list:
        a_data_cat2 = read_cat2(a_cat2)[0]
        a_cat2_sky = SkyCoord(a_data_cat2["ra"], a_data_cat2["dec"], frame='cirs', unit='deg')
        #a_cat2_sky = SkyCoord(a_data_cat2["ra"]*u.degree, a_data_cat2["dec"]*u.degree, frame='cirs')
        match_res = match_coordinates_sky(cat2_sky, a_cat2_sky)
        match_cat2 = a_data_cat2.iloc[match_res[0]]
        match_dis = dis_thre > match_res[1]
        index_list=[index for index, value in enumerate(match_dis) if value == True]
        for j in index_list:
            star_candidate_list[j] = pd.concat([star_candidate_list[j], match_cat2[j:j+1]])
    
    for k in range(len(star_candidate_list)):
        star_candidate_list[k] = star_candidate_list[k].reset_index(drop=True)
        star_candidate_list[k] = star_candidate_list[k].drop(0)
        cat_name = candidate_star_path+str(star_candidate_list[k]["ra"].iloc[0])+"_"+str(star_candidate_list[k]["dec"].iloc[0])+".cat"
        star_candidate_list[k].to_csv(cat_name, mode = save_mode, index=False, sep=" ")
    return 0, error_lst, star_candidate_list



