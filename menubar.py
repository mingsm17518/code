from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu
# import qdarktheme


class MenuBar(QMenuBar):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self._startPos = None
        self._endPos = None
        self._tracking = False

        self.fileMenu = self.addMenu('文件(&F)')
        self.fileMenu.addAction('打开(&O)', self.master.openDialog)
        self.fileMenu.addAction('设置(&T)', self.master.openConfig)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction('退出(&X)', self.master.exitSys)

        self.viewMenu = self.addMenu('视图(&V)')
        self.viewMenu.addAction('文件头(&H)', self.master.showHeader)
        themeAct = QAction('暗色主题(&M)', self, checkable=True)
        themeAct.triggered.connect(self.master.setTheme)
        self.viewMenu.addAction(themeAct)
        self.viewMenu.addAction('面板(&P)')
        # self.setMenu = self.addMenu('Setting')
        # self.setMenu.addAction('Theme...', self.master.setTheme)

        # self.fileMenu.addAction('Config...', self.master.openConfig)

        self.viewMenu.addSeparator()
        self.fitsMenu = QMenu('Fits展示...', self.viewMenu)
        # Histogram 按钮显示
        histogramAct = QAction('Histogram', self.fitsMenu, checkable=True)
        histogramAct.setChecked(True)
        self.fitsMenu.addAction(histogramAct)

        self.viewMenu.addMenu(self.fitsMenu)

        self.setObjectName('MenuBar')
        self.theme = 'light'
