#读取数据画图
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#输入文件路径
path = "./variable_test/variable_star/0.9997577825199774_164.7157073479011_71.65864265393442.txt"
file = open(path, "r")
lines = file.readlines()
file.close()
data_list = [line.strip() for line in lines]
object_list = []
for a_line in data_list[1:]:
    object_list.append(list(a_line.split(" ")))
data = pd.DataFrame(object_list, columns = ["jd", "diff_tar_ref", "tar_err", "diff_ref", "ref_err"])
jd = [float(x) for x in list(data.jd)]
diff_tar_ref = [float(x) for x in list(data.diff_tar_ref)]
diff_ref = [float(x) for x in list(data.diff_ref)]
diff_mean = np.mean(diff_tar_ref) - np.mean(diff_ref)
diff_ref = [x+diff_mean for x in diff_ref]
plt.scatter(jd, diff_tar_ref, color = "r", label = "diff_tar_ref")
plt.scatter(jd, diff_ref, color = "b", label = "diff_ref")
plt.xlabel("JD")
plt.ylabel("diff")
plt.legend()
plt.show()