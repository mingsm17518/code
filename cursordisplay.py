from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt


class CursorDisplay(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.setToolTip('Cursor location and image value at location')
        self.set(0, 0, 0.0)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("color:red")
        # self.setStyleSheet("background-color:gold")

    def set(self, x, y, value):
        self.setText('(x, y): ({}, {}) Value: {}'.format(x, y, value))

    def setXY(self, pos):
        x = int(pos.x())
        y = int(pos.y())
        value = 0.0
        self.setText('(x, y): ({}, {}) Value: {}'.format(x, y, value))
