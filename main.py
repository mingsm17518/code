from PySide6.QtCore import Qt, QPoint
# coding:utf-8
import sys
import numpy as np
# from astropy.io import fits
from PySide6.QtGui import QPalette, QColor, Qt, QGuiApplication,QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox,QVBoxLayout,
                               QPushButton,QLabel,QWidget,QHBoxLayout,QFrame,QStatusBar)
# import qdarktheme
from astropy.io import fits

from configwidget import ConfigDlg
# from fitsdisplay import FitsWidget
from menubar import MenuBar
from statusbar import StatusBar
# from toolbar import ToolBar
from headerdisplay import HeaderDisplay
from controlWidget import ControlWidget
from set.setwidget import setWidget

class BorderlessWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)  # 设置无边框窗口
        self.draggable = True  # 添加一个可拖动标志
        self.theme = 'light'
        self.setGeometry(500, 50, 1024,760)

        self.top_layout_height = 60  # 顶部布局高度
        self.createTopLayout()
        self.createCenterLayout()
        self.createBottomLayout()

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(self.top_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(self.center_layout)
        main_layout.addWidget(central_widget)

        main_layout.addWidget(self.bottom_widget)

        self.header = None
        self.show()
        self.init()

    # def show_menu(self):
    #     # 计算菜单的位置
    #     menu_pos = self.menu_button.mapToGlobal(QPoint(0, self.menu_button.height()))
    #     # 在计算出的位置显示菜单
    #     # self.menu_widget.setGeometry(menu_pos.x(), menu_pos.y(), self.menu_widget.width(), self.menu_widget.height())
    #     self.menu_widget.show()

    def createTopLayout(self):
        self.top_layout = QHBoxLayout()

        # 添加图标
        icon_label = QLabel()
        # 设置图标
        self.top_layout.addWidget(icon_label)

        # 添加标题
        title_label = QLabel("时域天文观测处理新技术应用系统")
        title_label.setStyleSheet("text-align: center;")
        self.top_layout.addWidget(title_label)

        # 添加最小化按钮
        minimize_button = QPushButton("-")
        minimize_button.setFixedSize(30, 30)  # 设置最小化按钮的固定大小
        self.top_layout.addWidget(minimize_button)
        minimize_button.clicked.connect(self.minimize_window)

        # 添加最大化按钮
        maximize_button = QPushButton(self,icon = QIcon('./resources/maximize_button.png'))
        maximize_button.setFixedSize(30, 30)  # 设置最大化按钮的固定大小
        self.top_layout.addWidget(maximize_button)
        maximize_button.clicked.connect(self.maximize_window)

        # 添加关闭按钮
        close_button = QPushButton("×")
        close_button.setFixedSize(30, 30)  # 设置关闭按钮的固定大小
        self.top_layout.addWidget(close_button)
        close_button.clicked.connect(self.close_window)

    def createCenterLayout(self):
        self.center_layout = QVBoxLayout()
        # 面板
        # self.mainWidget = ControlWidget(self)
        # self.center_layout.addWidget(self.mainWidget)

    def createBottomLayout(self):
        self.bottom_layout = QHBoxLayout()

        # 创建状态栏并添加到布局的底部
        self.statusBar = QStatusBar()
        self.statusBar.showMessage('Ready')
        self.bottom_layout.addWidget(self.statusBar)
        self.statusBar.setStyleSheet("background-color: lightgray;")

        # 创建状态栏
        # self._statusBar = StatusBar(parent=self)
        # self.bottom_layout.addWidget(self._statusBar)  # 将状态栏添加到底部布局中

        # 添加文本显示
        status_label = QLabel("状态栏")
        self.bottom_layout.addWidget(status_label)

        # 添加进度条
        progress_bar = QFrame()  # 自定义进度条样式
        self.bottom_layout.addWidget(progress_bar)
        self.bottom_layout.setSpacing(5)

        # 创建底部布局的容器，并设置固定高度
        self.bottom_widget = QWidget(self)
        self.bottom_widget.setLayout(self.bottom_layout)
        self.bottom_widget.setFixedHeight(self.top_layout_height // 2)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.draggable:
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.draggable:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_position = None

    def minimize_window(self):
        self.setWindowState(Qt.WindowState.WindowMinimized)

    def maximize_window(self):
        if self.windowState() == Qt.WindowState.WindowMaximized:
            self.setWindowState(Qt.WindowState.WindowNoState)
        else:
            self.setWindowState(Qt.WindowState.WindowMaximized)

    def close_window(self):
        self.close()

    def init(self):
        pass
        # self.mainWidget.init()

    def open(self, path, hdu=None):
        with open(path, 'rb') as input_file:
            hduList = fits.open(input_file)
            if hdu is None:
                hdu = 0
                while hduList[hdu].data is None:
                    hdu += 1
        image = hduList[hdu].data.astype(np.float32)

        return hduList, hdu, image


if __name__ == "__main__":
    app = QApplication([])
    window = BorderlessWindow()
    window.show()
    app.exec()
