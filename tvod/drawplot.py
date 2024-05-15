import sys
import matplotlib

matplotlib.use('Qt5Agg')

from PySide6.QtWidgets import QMainWindow, QApplication

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


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
# plt.scatter(jd, diff_tar_ref, color = "r", label = "diff_tar_ref")
# plt.scatter(jd, diff_ref, color = "b", label = "diff_ref")
# plt.xlabel("JD")
# plt.ylabel("diff")
# plt.legend()
# plt.show()

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.scatter(jd, diff_tar_ref, color = "r", label = "diff_tar_ref")
        sc.axes.scatter(jd, diff_ref, color = "b", label = "diff_ref")
        sc.axes.set_xlabel("JD")
        sc.axes.set_ylabel("diff")
        sc.axes.legend()
        #  sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.setCentralWidget(sc)

        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec()