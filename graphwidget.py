from PySide6.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg
# import pyqtgraph.opengl as gl
import numpy as np


class GraphWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setLayout(QHBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.childWidget = None

        self.childWidget = ThreeDWidget()
        self.layout().addWidget(self.childWidget)
        self.parent.setCurrentWidget(self)

    def set2dGraph(self, x=0, y=0):
        if self.childWidget:
            self.layout().removeWidget(self.childWidget)

        x = np.linspace(-10, 10, 1000)
        y = np.sin(x)

        self.childWidget = TwoDWidget(x, y)
        self.layout().addWidget(self.childWidget)
        self.parent.setCurrentWidget(self)

    def set3dGraph(self, lineList=None):
        if self.childWidget:
            self.layout().removeWidget(self.childWidget)

        n = 51
        y = np.linspace(-10, 10, n)
        x = np.linspace(-10, 10, 100)
        l = []
        for i in range(n):
            yi = np.array([y[i]] * 100)
            d = (x ** 2 + yi ** 2) ** 0.5
            z = 10 * np.cos(d) / (d + 1)
            l.append(np.vstack([x, yi, z]).transpose())

        self.childWidget = ThreeDWidget(l)
        self.layout().addWidget(self.childWidget)
        self.parent.setCurrentWidget(self)


class TwoDWidget(QWidget):
    def __init__(self, x, y):
        super().__init__()

        self.view = pg.PlotWidget(title='2dGraphTest-sinX')

        self.view.plot(x, y)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.view)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)


class ThreeDWidget(QWidget):
    def __init__(self, lineList = None):
        super().__init__()

        self.view = gl.GLViewWidget()

        self.xGird = gl.GLGridItem()
        self.xAxis = gl.GLAxisItem()

        self.xAxis.setSize(10, 20, 30)
        self.xAxis = gl.GLAxisItem()

        self.view.addItem(self.xGird)
        self.view.addItem(self.xAxis)

        if not lineList:
            return

        for i in range(len(lineList)):
            plt = gl.GLLinePlotItem(pos=lineList[i], color=pg.glColor((i, 51 * 1.3)), width=(i + 1) / 10.,
                                    antialias=True)
            self.view.addItem(plt)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.view)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
