## build a QApplication before building other widgets
import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.view = gl.GLViewWidget()

        ## create three grids, add each to the view
        self.xgird = gl.GLGridItem()
        self.xaxis = gl.GLAxisItem()

        self.xaxis.setSize(10, 20 , 30)

        self.yaxis = gl.GLAxisItem()
        self.zaxis = gl.GLAxisItem()

        self.view.addItem(self.xgird)
        self.view.addItem(self.xaxis)

        self.graph = gl.GLGraphItem()
        self.graph.setData()

        n = 51
        y = np.linspace(-10, 10, n)
        x = np.linspace(-10, 10, 100)
        for i in range(n):
            yi = np.array([y[i]]*100)
            d = (x**2 + yi**2)**0.5
            z = 10 * np.cos(d) / (d + 1)
            pts = np.vstack([x, yi, z]).transpose()
            print(pts)
            plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((i, n*1.3)), width=(i+1)/10., antialias=True)
            self.view.addItem(plt)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.view)


if __name__ == '__main__':
    app = QApplication([])

    window = MyWidget()
    window.show()
    sys.exit(app.exec())
