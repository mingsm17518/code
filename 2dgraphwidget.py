from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
import pyqtgraph as pg


class MyWidget(QWidget):
    def __init__(self, x, y):
        super().__init__()

        self.view = pg.PlotWidget(title='2dGraphTest-sinX')

        self.view.plot(x, y)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.view)

