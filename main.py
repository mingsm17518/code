# coding:utf-8
import sys
import numpy as np
# from astropy.io import fits
from PySide6.QtGui import QPalette, QColor, Qt, QGuiApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
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
        self.setWindowTitle('时域天文观测处理新技术应用系统')
        self.resize(1024, 768)

        self.theme = 'light'

        # 菜单
        self._menuBar = MenuBar(master=self)
        self.setMenuBar(self._menuBar)

        # self._toolBar = ToolBar(master=self)
        # self.addToolBar(self._toolBar)
        # 状态栏
        self._statusBar = StatusBar(parent=self)
        self.setStatusBar(self._statusBar)
        # self.statusBar()

        # self.control_widget = ControlWidget(parent=self)  # 将当前窗口实例作为父级对象传递给 ControlWidget
        # self.setCentralWidget(self.control_widget)
        # 连接控件中的自定义信号到槽函数
        # self.control_widget.close_signal.connect(self.close_window)

        # 面板
        self.mainWidget = ControlWidget(self)
        # self.setWidget = setWidget()
        self.setCentralWidget(self.mainWidget)

        self.header = None
        self.show()
        self.init()

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