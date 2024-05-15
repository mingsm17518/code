import os
import heapq
import warnings
import itertools
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import f
from astropy.table import QTable
warnings.filterwarnings("ignore")
from astropy.coordinates import SkyCoord

def Detect_variable(variable_path, variable_star_path, filter_, snr_thre = 8, p_value = 0.05, limted_num = 5):
    """
    检测变源
    :param variable_path: str，必备，输入路径.
    :param variable_star_path: str，必备，变源存储路径.
    :param filter_: str，必备，波段.
    :param snr_thre: int，默认为8，变源最低信噪比.
    :param p_value: float，默认为0.05，置信水平.
    :param limted_num: float，默认为5，变源最小图像数量.
    :return: status:状态码；error_lst:运行异常信息；outpar:变源.
    """
    #错误信息
    error_lst=[]
    
    #stdev1 = 0
    temp_sta = pd.read_csv(variable_path, sep = " ")
    
    if len(temp_sta) == 0:
        error_lst.append(str(variable_path)+"没有数据，请重新输入")
        outpar = None
        return 1, error_lst, outpar
    
    #对整个pd文件做筛选，剔除snr一下的行，将时间从小到大排序
    #选取你需要的波段的行
    filtered_df = temp_sta[temp_sta["filter"] == filter_]
    #剔除snr 低的目标
    filtered_df = filtered_df[filtered_df["snr_aper"] > snr_thre]
    
    #assert('该波段数据5幅以内，不具有统计意义，不能判断是否为变源。')
    if filtered_df.shape[0] <= limted_num:
        outpar = None
        return 0, error_lst, outpar
    
    #将剩下的行按照jd进行排序
    filtered_df = filtered_df.sort_values(by = "JD")
    filtered_df = filtered_df.drop_duplicates(subset = "JD", keep = "first")
    col_name = filtered_df.columns
    
    diff_df = pd.DataFrame()
    std_a = {}
    #存储索引,符合3sigma的行的索引
    #对star做较差
    for col in filtered_df.columns:
        #与所有的ref_做差值，并且将做差后的结果存储到diff_df中
        if "ref_mag" in col:
            new_col_name = "diff_" + col
            diff_df[new_col_name] = filtered_df["mag"] - filtered_df[col]
            # 求差的标准差，选取3sigma以内的
            temp_std = diff_df[new_col_name].std()
            temp_mean = diff_df[new_col_name].mean()
            # 保留3sigma的行，并且存储到一个新的df中
            # 符合标准的索引
            fuhe_index = np.abs(diff_df[new_col_name] - temp_mean) < 3*temp_std
            temp_diff = diff_df[fuhe_index][new_col_name]
            rest_df_std = temp_diff.std()
            #将每个标准差都存到字典中
            std_a[new_col_name] = rest_df_std
    #留下最小的2个标准差对应的标准星(不能自己减自己，标准差大于0）
    std_a = {std_score: score for std_score, score in std_a.items() if score > 0}
    if len(std_a) < 2:
        error_lst.append(str(variable_path)+"中标准星数量太少，请重新输入")
        outpar = None
        return 2, error_lst, outpar
    
    small_2_star = dict(heapq.nsmallest(2, std_a.items(), key = lambda x: x[1]))
    key_in = list(small_2_star.keys())
    stdev1 = list(small_2_star.values())
    ref_num = []
    for i in key_in:
        if i[-1] == "g":
            ref_num.append("0")
        else:
            ref_num.append(i[-1])
    #获取符合标准的参考星的名字
    col_name_ref = []
    #保留以下信息作为返回值
    for xx in ref_num:
        if xx == "0":
            col_name_ref.extend(["ref_ra", "ref_dec", "ref_xcentroid", "ref_ycentroid", "ref_mag", "ref_snr_aper", "ref_filter"])
        else:
            col_name_ref.extend([col for col in col_name if xx in col])
    #获取目标与标准星差值对应的列
    cha_ = diff_df[key_in[0]]
    # 时间
    jd_ = filtered_df["JD"]
    #这里都是参考星的信息
    fil_f = filtered_df[col_name_ref]
    mag_cols = [col for col in fil_f.columns if "mag" in col]
    col_pairs = list(itertools.combinations(mag_cols, 2))
    diff_dict = {}
    for pair in col_pairs:
        diff_col = pair[0] + "_" + pair[1]
        diff_dict[diff_col] = fil_f[pair[0]] - fil_f[pair[1]]
    #参考星的差值
    diff_df_ = pd.DataFrame(diff_dict)
    ref_er_cols = [col for col in fil_f.columns if "snr" in col]
    #参考星的误差计算的结果
    ref_er = np.sqrt(np.square(1.0857/fil_f[ref_er_cols[0]]) + np.square(1.0857/fil_f[ref_er_cols[1]]))
    #目标的测光误差
    tar_er = 1.0857/filtered_df["snr_aper"]
    oup = pd.concat([jd_, cha_, tar_er, diff_df_, ref_er], axis=1)
    outpar = pd.DataFrame(oup)
    outpar.columns = ["jd", "diff_tar_ref", "tar_err", "diff_ref", "ref_err"]
    if isinstance(outpar, pd.DataFrame) == False:
        outpar = None
        return 0, error_lst, outpar
    else:
        n_df = outpar.shape[0]
        std1 = outpar["diff_ref"].std()
        mean_tar = outpar["tar_err"].mean()
        dev = std1*std1+mean_tar*mean_tar
        ratio = stdev1[0]*stdev1[0]/dev/2.0
        P = 1 - f.cdf(ratio, n_df, n_df)
        name_ = Path(os.path.basename(variable_path))
        name_base = name_.stem
        name_base = name_base.split("_")
        ra = float(name_base[0])
        dec = float(name_base[1])
        skycoord = SkyCoord(ra, dec, frame='icrs', unit='deg')
        if P <= p_value:
            outparr = QTable.from_pandas(outpar)
            outparr = outparr.pformat_all(show_name = False, show_unit = False, align = '0=')
            file = open(variable_star_path+str(1-P)+"_"+str(ra)+"_"+str(dec)+".txt", "w")
            file.write("#P:"+str(1-P))
            file.write(",ra:"+str(round(ra,5)))
            file.write(",dec:"+str(round(dec,5)))
            for source in outparr:
                file.write("\n")
                file.write(source)
            file.close()
            return 0, error_lst, outpar
        elif P > p_value:
            return 0, error_lst, outpar


