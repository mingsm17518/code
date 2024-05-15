import os
import re
import warnings
import pandas as pd
import astropy.units as u
from astropy.io import fits
from astropy.table import Table
warnings.filterwarnings("ignore")
from pandas import DataFrame as DF
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from astropy.coordinates import match_coordinates_sky

def Variable_Combine(save_path, orgin_star_path, combine_star_path, thr_match = 2):
    """
    合并变源
    :param save_path: str，筛选后的参考星存储位置.
    :param orgin_star_path: str，必备，cat2文件路径.
    :param combine_star_path: str，存储路径.
    :param thr_match: int，默认为2， 匹配过程中允许的最大角距离.
    :return: status:状态码；error_lst:运行异常信息, num_write:匹配星数量.
    """
    #错误信息
    error_lst = []
    
    #读取txt文件
    pattern = '(\d+\.?\d*)'
    a = pd.read_csv(save_path, header=None)
    
    if len(a) == 0:
        error_lst.append(str(save_path)+"没有数据，请重新输入")
        num_write = None
        return 1, error_lst, num_write
    
    ra_t = []
    dec_t = []
    for ixx in range(a.shape[0]):
        temp = str(a.iloc[ixx].values)
        matches = re.findall(pattern, temp)
        r_t = float(matches[0])
        d_t = float(matches[1])
        ra_t.append(r_t)
        dec_t.append(d_t)
    
    ref_skycoord_1 = SkyCoord(ra_t*u.degree, dec_t*u.degree, frame='cirs')
    ref_ra_dec = ref_skycoord_1
    num_write = 0
    
    def read_cat2(cat2):
        cat_2 = fits.open(cat2)
        a_header = cat_2[0].header
        img_x = a_header["XSIZE"]
        img_y = a_header["YSIZE"]
        data_cat2 = Table(cat_2[1].data).to_pandas()
        data_cat2 = data_cat2[["JD", "filter", "ra", "dec", "xcentroid", "ycentroid", "mag", "snr_aper"]]
        data_cat2 = data_cat2.fillna(-99)
        return data_cat2, img_x, img_y
    
    re_temp = read_cat2(orgin_star_path)[0]
    col_name = list(re_temp.columns)
    shape_temp1_re = re_temp.shape[0]
    thr_mat = Angle(thr_match/3600, unit="deg")
    os.makedirs(combine_star_path, exist_ok=True)
    
    #获取新存储文件中目前已存的所有的文件的名字，方便后面实时做匹配用
    list_star = os.listdir(combine_star_path)
    list_star = pd.Series(list_star)
    star_ra = re_temp["ra"]
    star_dec = re_temp["dec"]
    sta_skycoord = SkyCoord(star_ra*u.degree, star_dec*u.degree, frame="cirs", unit='deg')
    res_match = match_coordinates_sky(ref_ra_dec, sta_skycoord)
    res_index = res_match[0]
    res_distance = res_match[1]
    #返回符合条件的参考星对应的索引
    ref_fact_index = [res_index[index] for index,dis in enumerate(res_distance) if dis <= thr_mat ]
    no_match_index = [res_index[index] for index,dis in enumerate(res_distance) if dis > thr_mat ]
    
    #能匹配上的参考星对应的索引
    ref_final_star=re_temp.iloc[ref_fact_index]
    
    #将没有匹配上的星自己的赤经赤纬，ref_ra_dec 是存用所有参考星的赤经赤纬的df
    no_match_ref_ra_dec = ref_ra_dec[no_match_index]
    ca_ref = pd.DataFrame()
    all_ref_df = DF()
    
    #如果所有的参考星都没匹配上，则填充num颗自定义的参考星，放到一行中
    jd_time = re_temp["JD"][0]
    filt_star = str(re_temp["filter"][0])
    
    #创建同一模版
    for aa, te in enumerate(no_match_ref_ra_dec):
        if aa == 0:
        #获取所有没有匹配上的参考星对应的赤经赤纬，波段信息，其他的信息都用固定值填充，时间使用当前图像的时间
            temp_ref = DF([{"JD": jd_time, "filter": filt_star, "ra": te.ra.deg, "dec": te.dec.deg, "xcentroid": -1, "ycentroid": -1, "mag": 99.999,  "snr_aper": 0.0001}])
            all_ref_df=temp_ref
        else:
            #将所有的自定义填充的参考星拼接在一行
            temp_ref = DF([{"JD": jd_time, "filter": filt_star, "ra": te.ra, "dec": te.dec, "xcentroid": -1, "ycentroid": -1, "mag": 99.999,  "snr_aper": 0.0001}])
            all_ref_df = pd.merge(all_ref_df, temp_ref, on=["JD"], suffixes=("_{0}".format(aa+1), "_{0}".format(aa)))

    #将自定义参考星与匹配上参考星做拼接
    for aaa in range(ref_final_star.shape[0]):
        if all_ref_df.shape[0] == 0:
            all_ref_df = DF(ref_final_star.iloc[aaa]).T
        else:
            temp__ = DF(ref_final_star.iloc[aaa]).T
            all_ref_df = pd.merge(all_ref_df,temp__, on=["JD"],suffixes=("_{0}".format(aaa+1), "_{0}".format(aaa)))

    # 如果都匹配上，就直接将各个参考星拼接起来即可
    all_co=list(all_ref_df.columns)
    for i, ax in enumerate(all_co):
        if ax == "JD":
            pass
        else:
            all_co[i]="ref_"+all_co[i]
    
    df_mege_ref = pd.DataFrame(all_ref_df)
    df_mege_ref.columns = all_co
    
    def Write_in_cat(c_data, name, save_pa="./Matched_File"):
        path_add = os.path.join(save_pa, name)
        try :
            temp_df = c_data.to_frame().T
        except (AttributeError):
            temp_df = c_data
        try:
            if os.path.exists(path_add):
                temp_df.to_csv(path_add, mode = "a", index=False,header=False, sep=' ')
            else:
                temp_df.to_csv(path_add,mode = "a",index=False,sep=' ')
        except (FileNotFoundError,OSError):
                os.makedirs(save_pa, exist_ok=True)
                if os.path.exists(path_add):
                    temp_df.to_csv(path_add, mode = "a", index=False, header=False, sep=' ')
                else:
                    temp_df.to_csv(path_add, mode = "a", index=False, sep=' ')
    
    if len(list_star) == 0:
        re_temp1 = DF()
        for ax in range(re_temp.shape[0]):
            temp = pd.merge(DF(re_temp.iloc[ax]).T, df_mege_ref, on=["JD"])
            re_temp1 = re_temp1._append(temp, ignore_index=True)
            ra_n = temp["ra"].values[0]
            dec_n = temp["dec"].values[0]
            name_cun = "{0}_{1}.cat".format(ra_n, dec_n)
            Write_in_cat(temp, name=name_cun, save_pa = combine_star_path)
    else:
        temp_lis = list_star.str.replace(".cat", "")
        ra_dec = temp_lis.str.split("_")
        skycoor_all_ra = pd.Series([x for x, y in ra_dec], dtype = "float")
        skycoor_all_dec = pd.Series([y for x, y in ra_dec], dtype = "float")
        ra_dec_Skyc = SkyCoord(skycoor_all_ra*u.degree, skycoor_all_dec*u.degree, frame = "cirs", unit='deg')
        for ax in range(re_temp.shape[0]):
            re_temp1 = pd.merge(DF(re_temp.iloc[ax]).T, df_mege_ref, on=["JD"])
            #一行一行的匹配
            temp_ra = re_temp1["ra"].values
            temp_dec = re_temp1["dec"].values
            temp_skycoord = SkyCoord(temp_ra*u.degree, temp_dec*u.degree, frame = "cirs")
            res_ = match_coordinates_sky(temp_skycoord, ra_dec_Skyc)
            # 文件夹目录名的索引
            res_index_ = res_[0]
            res_dis_ = res_[1]
            star_name_ra = skycoor_all_ra[res_index_].values
            star_name_dec = skycoor_all_dec[res_index_].values
            add_name = "{0}_{1}.cat".format(star_name_ra[0], star_name_dec[0])
            sel_name="{0}_{1}.cat".format(temp_ra[0],temp_dec[0])
            #存入的名字
            if res_dis_ <= thr_mat:
                #匹配上的
                Write_in_cat(re_temp1, name = add_name, save_pa = combine_star_path)
                num_write += 1
            else:
                Write_in_cat(re_temp1, name=sel_name, save_pa = combine_star_path)
    return 0, error_lst, num_write





