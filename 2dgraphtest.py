## build a QApplication before building other widgets
import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
import pyqtgraph as pg

import numpy as np


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.view = pg.PlotWidget(title='2dGraphTest-sinX')

        x = np.linspace(-10, 10, 1000)
        sinX = np.sin(x)

        self.view.plot(x, sinX)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.view)


if __name__ == '__main__':
    app = QApplication([])

    window = MyWidget()
    window.show()
    sys.exit(app.exec())
