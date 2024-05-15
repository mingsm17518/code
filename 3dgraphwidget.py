from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
import pyqtgraph as pg
import pyqtgraph.opengl as gl


class MyWidget(QWidget):
    def __init__(self, lineList):
        super().__init__()

        self.view = gl.GLViewWidget()

        self.xGird = gl.GLGridItem()
        self.xAxis = gl.GLAxisItem()

        self.xAxis.setSize(10, 20, 30)
        self.xAxis = gl.GLAxisItem()

        self.view.addItem(self.xGird)
        self.view.addItem(self.xAxis)

        self.graph = gl.GLGraphItem()
        self.graph.setData()

        for i in range(len(lineList)):
            plt = gl.GLLinePlotItem(pos=lineList[i], color=pg.glColor((i, 51*1.3)), width=(i+1)/10., antialias=True)
            self.view.addItem(plt)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.view)

