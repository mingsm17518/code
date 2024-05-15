import os
import warnings
import pandas as pd
from pathlib2 import Path
warnings.simplefilter("ignore")

def StandardStar(candidate_star_path, save_path, num_cand = 200, num = 10):
    """
    筛选标准星
    :param candidate_star_path: str，必备，候选星存储路径.
    :param save_path: str，筛选后的参考星需要存储的位置.
    :param num_cand: int，默认为200，选取变化最小的候选星数量最大值.
    :param num: int，默认为10，标准星数量最大值.
    :return: status:状态码；error_lst:运行异常信息.
    """
    #错误信息
    error_lst = []
    
    #读文件信息
    cat_list = os.listdir(candidate_star_path)
    if len(cat_list) == 0:
        error_lst.append(str(candidate_star_path)+"没有文件，请重新输入")
        return 1, error_lst
    
    
    data = {"name": [], "variable": []}
    data_variable = pd.DataFrame(data)
    
    for num1, name1 in enumerate(cat_list):
        path_1 = os.path.join(candidate_star_path, name1)
        candidate_star_1 = pd.read_csv(path_1, sep = " ")
        for num2, name2 in enumerate(cat_list[num1+1:]):
            path_2 = os.path.join(candidate_star_path, name2)
            candidate_star_2 = pd.read_csv(path_2, sep = " ")
            candidate_star_merg = pd.merge(candidate_star_1, candidate_star_2, on="JD")
            mag_match = candidate_star_merg["mag_x"] - candidate_star_merg["mag_y"]
            var_mag = mag_match.var()
            mag_name = "{0}--{1}".format(name1, name2).replace(".cat", "")
            data_variable = data_variable._append({"name": mag_name, "variable": var_mag}, ignore_index = True)
    star_variable = data_variable.sort_values("variable")[:num_cand]
    
    #找前30组中出现次数最多的候选星
    star_candidate = pd.DataFrame({"star": []})
    star = star_variable["name"].str.split("--")
    for i in range(star_variable.shape[0]):
        star1 = star.iloc[i][0]
        star2 = star.iloc[i][1]
        star_candidate = star_candidate._append({"star": star1}, ignore_index=True)
        star_candidate = star_candidate._append({"star": star2}, ignore_index=True)
    
    #所有候选星出现的次数,选取前num个
    mag_star = star_candidate["star"].value_counts().index[:num]
    with open(save_path, 'w') as file:
        for item in mag_star:
            file.write(str(item) + '\n')
    file.close()
    return 0, error_lst




