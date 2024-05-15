# 读取数据画图
import pandas as pd
import numpy as np
import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class PNGWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        # 每一个展示面板都需要附带一个信息区 没有为None
        self.infoWidget = None
        self.setLayout(QVBoxLayout(self))

        self.lb_png = QLabel('')
        pixmap = QPixmap(filePath)
        self.lb_png.setPixmap(pixmap)

        self.layout().addWidget(self.lb_png)

class MatplotWidget(QWidget):

    def __init__(self, filePath):
        super().__init__()

        # 每一个展示面板都需要附带一个信息区 没有为None
        self.infoWidget = None

        self.setLayout(QVBoxLayout(self))

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.

        jd, diff_tar_ref, diff_ref = self.readDataFile(filePath)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.scatter(jd, diff_tar_ref, color="r", label="diff_tar_ref")
        sc.axes.scatter(jd, diff_ref, color="b", label="diff_ref")
        sc.axes.set_xlabel("JD (day)")
        sc.axes.set_ylabel("Var-Ref (mag)")
        sc.axes.legend()

        self.sc = sc
        #  sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.layout().addWidget(sc)

    def readDataFile(self, filePath):
        with open(filePath, 'r') as file:
            lines = file.readlines()
            file.close()

        data_list = [line.strip() for line in lines]
        object_list = []
        for a_line in data_list[1:]:
            object_list.append(list(a_line.split(" ")))
        data = pd.DataFrame(object_list, columns=["jd", "diff_tar_ref", "tar_err", "diff_ref", "ref_err"])
        jd = [float(x) for x in list(data.jd)]
        diff_tar_ref = [float(x) for x in list(data.diff_tar_ref)]
        diff_ref = [float(x) for x in list(data.diff_ref)]
        diff_mean = np.mean(diff_tar_ref) - np.mean(diff_ref)
        diff_ref = [x + diff_mean for x in diff_ref]

        return jd, diff_tar_ref, diff_ref
