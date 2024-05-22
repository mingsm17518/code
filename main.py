# coding:utf-8
import sys
import numpy as np
# from astropy.io import fits
from PySide6.QtGui import QPalette, QColor, Qt, QGuiApplication,QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox,QVBoxLayout,
                               QPushButton,QLabel,QWidget,QHBoxLayout)
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


class MyWindow(QMainWindow):
    BORDER_WIDTH = 5

    def __init__(self, filename=None):
        super().__init__()

        # self.setWindowTitle('时域天文观测处理新技术应用系统')
        self.resize(1024, 760)
        self.theme = 'light'
        self.create_titlebar_buttons()

        # 创建标题栏部件
        # title_bar_widget = QWidget()
        # title_layout = QHBoxLayout()
        # 在标题栏上添加标题文本

        # title_layout.addWidget(title_text)
        #
        #
        #
        # 将标题栏添加到窗口中
        # main_layout = QVBoxLayout()
        # main_layout.addWidget(title_bar_widget)
        # self.setLayout(main_layout)

        # 移除窗口边框
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.central_widget = QWidget()
        # 设置标题栏可拖动
        self.draggable = True
        self.drag_position = None

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)
        # layout.setSpacing(0)
        # self.btnLayout.setSpacing(0)
        # self.btnLayout.setContentsMargins(0, 0, 0, 0)
        # self.setLayout(layout)
        title_text = QLabel('时域天文观测处理新技术应用系统')

        title_layout = QHBoxLayout()
        title_layout.addWidget(title_text)


        # 添加最大化和关闭按钮
        self.btnLayout = QHBoxLayout()
        self.btnLayout.addStretch(1)  # 添加弹性空间
        self.btnLayout.addWidget(self.minimize_button)
        self.btnLayout.addWidget(self.maximize_button)
        self.btnLayout.addWidget(self.close_button)
        title_layout.addLayout(self.btnLayout)
        layout.addLayout(title_layout)
        # title_layout.addLayout(self.btnLayout)
        # title_bar_widget.setLayout(title_layout)
        # layout.addLayout(self.btnLayout)

        # 菜单
        # self._menuBar = MenuBar(master=self)
        # self.setMenuBar(self._menuBar)

        # self._toolBar = ToolBar(master=self)
        # self.addToolBar(self._toolBar)
        # 状态栏
        self._statusBar = StatusBar(parent=self)
        self.setStatusBar(self._statusBar)
        # self.statusBar()

        # self.control_widget = ControlWidget(parent=self)  # 将当前窗口实例作为父级对象传递给 ControlWidget
        self.setCentralWidget(self.central_widget)
        # 连接控件中的自定义信号到槽函数
        # self.control_widget.close_signal.connect(self.close_window)

        # 面板
        self.mainWidget = ControlWidget(self)
        # self.setWidget = setWidget()
        layout.addWidget(self.mainWidget)
        #self.setLayout(layout)
        # self.setCentralWidget(self.mainWidget)

        self.header = None
        self.show()
        self.init()
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_titlebar_buttons(self):
        self.minimize_button = QPushButton("-", self)
        self.minimize_button.setGeometry(880, 10, 30, 30)
        self.minimize_button.clicked.connect(self.minimize_window)

        self.maximize_button = QPushButton(self)
        icon = QIcon('./resources/maximize_button.png')
        self.maximize_button.setIcon(icon)
        self.maximize_button.setGeometry(930, 10, 30, 30)
        self.maximize_button.clicked.connect(self.maximize_window)

        self.close_button = QPushButton("×", self)
        self.close_button.setGeometry(980, 10, 30, 30)
        self.close_button.clicked.connect(self.close_window)

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

    def close_window(self):
        # 执行需要在关闭按钮点击时执行的操作
        reply = QMessageBox.question(self, "退出", "退出系统?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def init(self):
        self.mainWidget.init()

    def open(self, path, hdu=None):
        with open(path, 'rb') as input_file:
            hduList = fits.open(input_file)
            if hdu is None:
                hdu = 0
                while hduList[hdu].data is None:
                    hdu += 1
        image = hduList[hdu].data.astype(np.float32)

        return hduList, hdu, image

    def openDialog(self):
        pass
    #     filename = QFileDialog.getOpenFileName(self, '打开文件', '.', filter='fits文件(*.fits *.fit *.gz);;所有文件(*.*)')
    #     if filename[0]:
    #         hduList, hdu, image = self.open(filename[0])
    #
    #         fitsWidget = FitsWidget(parent=self.mainWidget.display, action=self.menuBar().fitsMenu.actions()[0],
    #                                 hduList=hduList, hdu=hdu, image=image, statusBar=self.statusBar())
    #         self.mainWidget.addFitsTab(fitsWidget=fitsWidget, name=filename[0].split('/')[-1])

    def openConfig(self):
        config_win = ConfigDlg()
        config_win.show()
        config_win.exec()

    def showHeader(self):
        if not self.header:
            return
        headerWindow = HeaderDisplay(self.header)
        headerWindow.show()
        headerWindow.exec()

    def setTheme(self):
        if self.theme == 'light':
            self.theme = 'dark'
        else:
            self.theme = 'light'

        # qdarktheme.setup_theme(self.theme)
        self.mainWidget.setTheme(self.theme)
        self.setStyleSheet("QWidget:{background: transparent}")

    def exitSys(self):
        reply = QMessageBox.question(self, "退出", "退出系统?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

# todo 已经更改（app=None） -> (self, app=None)
    def get_darkModePalette(self, app=None):
        darkPalette = app.palette()
        darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.WindowText, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
        darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        darkPalette.setColor(QPalette.ToolTipBase, Qt.white)
        darkPalette.setColor(QPalette.ToolTipText, Qt.white)
        darkPalette.setColor(QPalette.Text, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
        darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
        darkPalette.setColor(QPalette.ButtonText, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        darkPalette.setColor(QPalette.BrightText, Qt.red)
        darkPalette.setColor(QPalette.Link, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        darkPalette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        darkPalette.setColor(QPalette.HighlightedText, Qt.white)
        darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127), )

        return darkPalette

    # 处理子控件信号
    # 状态栏
    def setStatusInfo(self, text):
        self._statusBar.setInfo(text)


if __name__ == '__main__':
    app = QApplication([])
    # qdarktheme.setup_theme('light')
    window = MyWindow()
    sys.exit(app.exec())