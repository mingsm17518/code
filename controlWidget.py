# coding:utf-8
import numpy as np
from astropy.io import fits
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit,QDialog,QMenu,
                               QPushButton, QLabel, QSpacerItem, QSizePolicy, QGroupBox, QStackedWidget, QFileDialog)
from PySide6.QtCore import Qt, QSize,QPoint
from PySide6.QtGui import QIcon, QFont

from operationwidget import OperationWidget
from displayWidget import DisplayWidget, DisplayTabWidget
from fitsdisplay import FitsWidget
from MultiImageWidget import MultiImageWidget
from graphwidget import GraphWidget
from filetreewidget import FileTreeWidget
from matplotwidget import MatplotWidget, PNGWidget
from txtwidget import TxTWidget
from cat2widget import Cat2Widget

from set.setwidget import setWidget
from sofc.sofcwidget import SofcWidget
from smod.smodwidget import SmodWidget
from aofc.aofcwidget import AofcWidget
from deim.deimwidget import DeimWidget
from tvod.tvodwidget import TvodWidget
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PySide6.QtCore import Signal
class SystemButton(QPushButton):

    def __init__(self, text=None, parent=None, master=None, icon1=None, icon2=None, icon3=None, icon4=None):
        super().__init__(text=text, parent=parent)

        self.master = master
        self.isPressed = False
        self.groupbox = None
        self.released.connect(self.master.systemBtnEvent)
        self.setFixedSize(32, 32)

        self.iconUnPressedLight = QIcon(icon1)
        self.iconPressedLight = QIcon(icon2)
        self.iconUnPressedDark = QIcon(icon3)
        self.iconPressedDark = QIcon(icon4)
        self.currentIconUnPressed = self.iconUnPressedLight
        self.currentIconPressed = self.iconPressedLight
        self.setIcon(self.iconUnPressedLight)
        self.setIconSize(QSize(32, 32))
        self.setFlat(True)

    def setPressed(self, isPressed):
        self.isPressed = isPressed
        if isPressed:
            self.setIcon(self.currentIconPressed)
        else:
            self.setIcon(self.currentIconUnPressed)

    def setTheme(self, theme):
        if theme == 'light':
            if self.isPressed:
                self.setIcon(self.iconPressedLight)
                self.currentIconPressed = self.iconPressedLight
            else:
                self.setIcon(self.iconUnPressedLight)
                self.currentIconUnPressed = self.iconPressedLight
        else:
            if self.isPressed:
                self.setIcon(self.iconPressedDark)
                self.currentIconPressed = self.iconPressedDark
            else:
                self.setIcon(self.iconUnPressedDark)
                self.currentIconUnPressed = self.iconUnPressedDark



class Splitter(QLabel):

    def __init__(self, parent=None):
        super(Splitter, self).__init__(parent=parent)

        self.setText('================')
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)


class ControlWidget(QWidget):
    BORDER_WIDTH = 5
    close_signal = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.master = None
        self.parent = parent
        self.header = None
        self.hdu = None
        self.hduList = None
        self.hasHistogram = True
        # self.histogramAct = self.parent.menuBar().fitsMenu.actions()[0]
        # self.histogramAct.triggered.connect(self.setHistogram)
        self.resize(350, 600)

        # 主体采用水平布局
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 30, 0, 0)

        # 按钮列表纵向布局
        self.btnLayout = QVBoxLayout()
        self.btnLayout.setSpacing(0)
        self.btnLayout.setContentsMargins(0, 30, 0, 0)

        # 设置布局
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.btnLayout)

        # 创建按钮
        self.btn1 = SystemButton(master=self,
                                 icon1='./resources/SOFC跟踪定标0.png',
                                 icon2='./resources/SOFC跟踪定标1.png')
        self.btn2 = SystemButton(master=self,
                                 icon1='./resources/SMOD目标搜寻0.png',
                                 icon2='./resources/SMOD目标搜寻1.png')
        self.btn3 = SystemButton(master=self,
                                 icon1='./resources/DEIM星像分割0.png',
                                 icon2='./resources/DEIM星像分割1.png'
                                 )
        self.btn4 = SystemButton(master=self,
                                 icon1='./resources/AOFC流量定标0.png',
                                 icon2='./resources/AOFC流量定标1.png'
                                 )
        self.btn5 = SystemButton(master=self,
                                 icon1='./resources/TVOD变源检测0.png',
                                 icon2='./resources/TVOD变源检测1.png'
                                 )
        self.btn6 = SystemButton(master=self,
                                 icon1='./resources/1_unpressed_light',
                                 icon2='./resources/1_pressed_light'
                                 )
        self.btn7 = QPushButton('文件(&F)', self)
        self.btn8 = QPushButton('视图(&V)', self)
        # self.btn9 = QPushButton('click me',self)
        #self.btn9.clicked.connect(self.openSetWidget)
        self.btn9 = SystemButton(master=self,
                     icon1='./resources/1_unpressed_light',
                     icon2='./resources/1_pressed_light'
                     )
        self.menu_button = QPushButton(self,icon = QIcon('./resources/设置.png'))


        self.btnList = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6,self.btn7,self.btn8,self.btn9]

        for btn in self.btnList:
            self.btnLayout.addWidget(btn)


        # 在btnLayout中添加stretch和btn10
        self.btnLayout.addStretch(1)
        self.btnLayout.addWidget(self.menu_button)
        self.menu_button.clicked.connect(self.showMenu)




        # self.btnLayout.addWidget(self.btn1)
        # self.btnLayout.addWidget(self.btn2)
        # self.btnLayout.addWidget(self.btn3)
        # self.btnLayout.addWidget(self.btn4)
        # self.btnLayout.addWidget(self.btn5)
        # self.btnLayout.addWidget(self.btn6)
        # self.btnLayout.addWidget(self.btn7)
        # self.btnLayout.addWidget(self.btn8)
        # self.btnLayout.addWidget(self.btn9)
        self.btnLayout.setSpacing(6)

        # self.btn7.clicked.connect(self.showbtn)
        # self.btn8.clicked.connect(self.showbtn2)
        #
        # self.file_btn = QPushButton('文件头(&H)', self)
        # self.theme_btn = QPushButton('暗色主题(&M)', self)
        # self.p_btn = QPushButton('面板(&P)', self)
        #
        # self.open_btn = QPushButton('打开(&O)', self)
        # self.set_btn = QPushButton('设置(&T)', self)
        # self.close_btn = QPushButton('退出(&X)', self)
        #
        # self.open_btn.clicked.connect(self.open_action)
        # self.close_btn.clicked.connect(self.emit_close_signal)
        #
        # self.toggle_layout = QVBoxLayout()
        # self.toggle2_layout = QVBoxLayout()
        # # 将按钮添加到垂直布局中
        # self.toggle_layout.addWidget(self.open_btn)
        # self.toggle_layout.addWidget(self.set_btn)
        # self.toggle_layout.addWidget(self.close_btn)
        #
        # self.toggle2_layout.addWidget(self.file_btn)
        # self.toggle2_layout.addWidget(self.theme_btn)
        # self.toggle2_layout.addWidget(self.p_btn)
        # # 标记按钮的布局默认是隐藏的
        # self.toggle_layout_visible = False
        # self.toggle2_layout_visible = False

        #spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.btnLayout.addItem(spacerItem)

        # 创建设置面板
        # self.scrollArea = QScrollArea(self)
        # self.scrollArea.setVisible(False)
        # self.scrollArea.verticalScrollBar().setVisible(False)
        # self.scrollArea.verticalScrollBar().setStyleSheet("width:0px")
        # self.scrollArea.horizontalScrollBar().setVisible(False)
        # self.scrollArea.horizontalScrollBar().setStyleSheet("height:0px")
        # self.scroll = self.scrollArea.verticalScrollBar()

        # self.settingWidget = QWidget(self.scrollArea)
        # self.scrollArea.setWidget(self.settingWidget)
        # self.mainLayout.addWidget(self.scrollArea)
        self.settingWidget = QWidget(self)
        self.settingWidget.setVisible(False)
        self.mainLayout.addWidget(self.settingWidget)

        # self.settingWidget.setStyleSheet("background-color:green;")
        self.settingWidget.setFixedWidth(self.width() - 75)  # 滚动区域
        # self.settingWidget.setFixedHeight(6000)
        # self.scrollArea.setFixedWidth(self.width() - 75)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.settingWidget.setLayout(layout)

        # 创建子系统操作箱
        self.currentGroupBox = None
        self.currentBtn = None

        self.gb9 = QGroupBox(self.settingWidget)
        self.gb9.setTitle('设置')
        self.btn9.groupbox = self.gb9

        # 往gb9塞入界面
        self.gb9.setObjectName('set')

        self.gb9.setLayout(QVBoxLayout(self.gb9))
        self.setWidget = setWidget()
        # self.setWidget.setStatusBar(self.parent.statusBar())
        self.gb9.layout().addWidget(self.setWidget)
        self.gb9.layout().setContentsMargins(0, 0, 0, 0)





        self.gb1 = QGroupBox(self.settingWidget)
        self.gb1.setTitle('移动目标测量')
        # self.gb1.setMinimumSize(self.settingWidget.width(), 0)
        self.btn1.groupbox = self.gb1

        # 往gb1塞入界面
        self.gb1.setObjectName('sofc')
        self.gb1.setLayout(QVBoxLayout(self.gb1))
        self.sofcWidget = SofcWidget()
        self.sofcWidget.setStatusBar(self.parent.statusBar)
        self.gb1.layout().addWidget(self.sofcWidget)
        self.gb1.layout().setContentsMargins(0, 0, 0, 0)

        # 创建groupbox2
        self.gb2 = QGroupBox(self.settingWidget)
        self.gb2.setTitle('移动目标检测')
        # self.gb2.setMinimumSize(self.settingWidget.width(), 400)
        self.btn2.groupbox = self.gb2

        # 往gb2塞入控件
        self.gb2.setObjectName('smod')
        self.gb2.setLayout(QVBoxLayout(self.gb2))
        self.smod = SmodWidget()
        self.gb2.layout().addWidget(self.smod)
        self.gb2.layout().setContentsMargins(0, 0, 0, 0)
        self.gb2.layout().setSpacing(0)
        self.smod.setStatusBar(self.parent.statusBar)
        # self.operation2 = OperationWidget()
        # self.operation2 = QPushButton('打开fits')
        # self.operation2.clicked.connect(self.openFits)

        # self.gb2BtnShow = QPushButton('查看Fits')
        # self.gb2BtnShow.setObjectName('gb2')
        # self.gb2BtnShow.clicked.connect(self.switchover)

        # self.gb2.setLayout(QVBoxLayout(self.gb2))
        # self.gb2.layout().addWidget(self.operation2)
        # self.gb2.layout().addWidget(self.gb2BtnShow)

        # 创建groupbox3
        self.gb3 = QGroupBox(self.settingWidget)
        self.gb3.setTitle('粘连星象分割')
        # self.gb3.setMinimumSize(self.settingWidget.width(), 400)
        self.btn3.groupbox = self.gb3

        # 往gb3塞入控件
        self.gb3.setObjectName('deim')
        self.gb3.setLayout(QVBoxLayout(self.gb3))
        self.gb3.layout().setContentsMargins(0, 0, 0, 0)
        self.gb3.layout().setSpacing(0)
        self.deim = DeimWidget()
        self.gb3.layout().addWidget(self.deim)

        # 创建groupbox4
        self.gb4 = QGroupBox(self.settingWidget)
        self.gb4.setTitle('巡天数据定标')
        # self.gb4.setMinimumSize(self.settingWidget.width(), 400)
        self.btn4.groupbox = self.gb4

        # 往gb4塞控件
        self.gb4.setObjectName('aofc')
        self.gb4.setLayout(QVBoxLayout(self.gb4))
        self.aofcWidget = AofcWidget()
        self.aofcWidget.setStatusBar(self.parent.statusBar)
        self.gb4.layout().addWidget(self.aofcWidget)
        self.gb4.layout().setContentsMargins(0, 0, 0, 0)
        self.gb4.layout().setSpacing(0)
        # self.gb4Btn2d = QPushButton('2d图像示例')
        # self.gb4Btn3d = QPushButton('3d图像示例')
        # self.gb4.layout().addWidget(self.gb4Btn2d)
        # self.gb4.layout().addWidget(self.gb4Btn3d)

        # 创建groupbox5
        self.gb5 = QGroupBox(self.settingWidget)
        self.gb5.setLayout(QVBoxLayout(self.gb5))
        self.gb5.setTitle('时域变源检测')
        self.btn5.groupbox = self.gb5

        # 往gb5塞控件
        self.gb5.setObjectName('tvod')
        self.tvod = TvodWidget()
        self.tvod.setStatusBar(self.parent.statusBar)
        self.gb5.layout().addWidget(self.tvod)
        #self.gb5.layout().addWidget(self.FileWidget)
        self.gb5.layout().setContentsMargins(0, 0, 0, 0)
        self.gb5.layout().setSpacing(0)

        # 创建groupbox6
        self.gb6 = QGroupBox(self.settingWidget)
        self.gb6.setLayout(QVBoxLayout(self.gb6))
        self.gb6.setTitle('测试功能集合面板')
        self.btn6.groupbox = self.gb6
        self.gb6.setObjectName('test')

        # 往gb6塞控件
        self.gb6.layout().setContentsMargins(0, 0, 0, 0)
        self.gb6.layout().setSpacing(0)

        self.operation2 = OperationWidget()
        self.operation2 = QPushButton('打开fits')
        self.operation2.clicked.connect(self.openFits)

        self.gb2BtnShow = QPushButton('查看Fits')
        self.gb2BtnShow.setObjectName('gb2')
        self.gb2BtnShow.clicked.connect(self.switchover)

        self.gb6.layout().addWidget(self.operation2)
        self.gb6.layout().addWidget(self.gb2BtnShow)

        self.gb3BtnLoad = QPushButton('加载Fits')
        self.gb3BtnShow = QPushButton('查看Fits')
        self.gb3BtnShow.setObjectName('gb3')
        self.gb3BtnShow.clicked.connect(self.switchover)
        self.gb3BtnPlay = QPushButton('播放')
        self.gb3BtnPause = QPushButton('停止')
        self.gb3BtnLast = QPushButton('上一页')
        self.gb3BtnNext = QPushButton('下一页')

        # self.gb6.layout().addWidget(self.gb3BtnLoad)
        # self.gb6.layout().addWidget(self.gb3BtnShow)
        # self.gb6.layout().addWidget(self.gb3BtnPlay)
        # self.gb6.layout().addWidget(self.gb3BtnPause)
        # self.gb6.layout().addWidget(self.gb3BtnLast)
        # self.gb6.layout().addWidget(self.gb3BtnNext)
        buttons_list3 = [self.gb3BtnLoad, self.gb3BtnShow, self.gb3BtnPlay, self.gb3BtnPause,
                        self.gb3BtnLast,self.gb3BtnNext]

        for button in buttons_list3:
            self.gb6.layout().addWidget(button)

        # 添加组件
        widget_list = [self.gb1, self.gb2, self.gb3, self.gb4, self.gb5, self.gb6, self.gb9]
        for widget in widget_list:
            self.settingWidget.layout().addWidget(widget)
        # self.settingWidget.layout().addWidget(self.gb1)
        # self.settingWidget.layout().addWidget(self.gb2)
        # self.settingWidget.layout().addWidget(self.gb3)
        # self.settingWidget.layout().addWidget(self.gb4)
        # self.settingWidget.layout().addWidget(self.gb5)
        # self.settingWidget.layout().addWidget(self.gb6)
        # self.settingWidget.layout().addWidget(self.gb9)

        self.fileWidget = FileTreeWidget(parent=self.settingWidget)
        # self.tvodFileWidget = FileTreeWidget(parent=self.tvod, rootPath=None)
        # self.FileWidget.fileTreeView.setFilter(['.txt'])
        self.fileWidget.fileTreeView.sigShowFileInfo.connect(self.parent.setStatusInfo)
        self.fileWidget.fileTreeView.sigOpenFile.connect(self.fileResultShow)

        self.settingWidget.layout().addWidget(self.fileWidget)

        self.groupBoxList = [self.gb1, self.gb2, self.gb3, self.gb4, self.gb5, self.gb6,self.gb9]
        # spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.settingWidget.layout().addItem(spacerItem)

        # 隐藏
        self.gb1.setVisible(False)
        self.gb2.setVisible(False)
        self.gb3.setVisible(False)
        self.gb4.setVisible(False)
        self.gb5.setVisible(False)
        self.gb6.setVisible(False)
        self.gb9.setVisible(False)

        # 展示区
        # QStackWidget样式
        # self.display = DisplayWidget(self)
        # self.display.layout().setSpacing(0)
        # self.display.layout().setContentsMargins(0, 0, 0, 0)
        # QTabWidget样式
        self.display = DisplayTabWidget(self)
        self.display.setTabsClosable(True)
        self.display.tabCloseRequested.connect(self.tabClose)
        self.display.currentChanged.connect(self.tabChange)
        self.mainLayout.addWidget(self.display)
        # self.display.addWidget(QWidget(self.display))

        # fits展示界面
        # self.fitsDisplay = FitsWidget(self.display, action=self.parent.menuBar().fitsMenu.actions()[0])
        # self.display.addWidget(self.fitsDisplay)
        # self.display.addTab(self.fitsDisplay, self.fitsDisplay.tabName)

        # fits轮播界面
        # self.multiFitsDisplay = MultiImageWidget(parent=self.display, master=self, action=self.histogramAct)
        # self.multiFitsDisplay.setStatusBar(self.parent.statusBar())
        # self.display.addWidget(self.multiFitsDisplay)

        # 图界面
        # self.graphDisplay = GraphWidget(parent=self.display)
        # self.display.addWidget(self.graphDisplay)

        # 关联按钮
        # self.gb3BtnLoad.clicked.connect(lambda: self.multiFitsDisplay.loadFits(num=10))
        # self.gb3BtnPlay.clicked.connect(self.multiFitsDisplay.play)
        # self.gb3BtnPause.clicked.connect(self.multiFitsDisplay.pause)
        # self.gb3BtnLast.clicked.connect(self.multiFitsDisplay.last)
        # self.gb3BtnNext.clicked.connect(self.multiFitsDisplay.next)

        # self.gb4Btn2d.clicked.connect(self.graphDisplay.set2dGraph)
        # self.gb4Btn3d.clicked.connect(self.graphDisplay.set3dGraph)

        # self.flowBtnWidget = FlowBtnWidget(self.label)
        # self.flowBtnWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.flowBtnWidget.move(0, 0)
        # self.flowBtnWidget.raise_()

        # self.flowBtnWidget.move()

        self.mainLayout.setStretch(2, 1)

        # self.scroll.valueChanged.connect(self.scrollTest)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.display.reposition(histogram=self.hasHistogram)

    def setHistogram(self):
        if self.parent.menuBar().fitsMenu.actions()[0].isChecked():
            self.hasHistogram = True
        else:
            self.hasHistogram = False
        self.display.setHistogram(self.hasHistogram)
        self.display.reposition(histogram=self.hasHistogram)

    def init(self):
        self.display.reposition(histogram=self.hasHistogram)

    def scrollTest(self):
        y = self.scroll.value()

        # 最大范围检测
        gb = self.groupBoxList[-1]
        if y >= gb.mapTo(self.settingWidget, gb.rect().topLeft()).y():
            self.scroll.setValue(gb.mapTo(self.settingWidget, gb.rect().topLeft()).y())
        # print(self.settingWidget.geometry().topLeft().y())
        # y += self.currentGroupBox.height() / 2
        for btn in self.btnList:
            groupbox = btn.groupbox
            yMin = groupbox.mapTo(self.settingWidget, groupbox.rect().topLeft()).y()
            yMax = groupbox.mapTo(self.settingWidget, groupbox.rect().bottomLeft()).y()

            if yMin <= y <= yMax:
                self.currentGroupBox = groupbox
                self.currentBtn = btn
                btn.setPressed(True)
                # btn.setText(btn.text().split('*')[0] + '*')
            else:
                btn.setPressed(False)
                # btn.setText(btn.text().split('*')[0])

    def switchover(self):
        name = self.sender().objectName()
        if name == 'gb2':
            self.display.setCurrentWidget(self.fitsDisplay)
            self.fitsDisplay.init()
        elif name == 'gb3':
           # self.display.setCurrentWidget(self.multiFitsDisplay)
            self.addFitsTab(fitsWidget=self.multiFitsDisplay, name='gif')

    def systemBtnEvent(self):
        btn = self.sender()

        if self.currentBtn == btn:
            self.currentBtn = None
            btn.setPressed(False)
            # self.scrollArea.setVisible(False)
            self.settingWidget.setVisible(False)
            # self.display.reposition(width=self.display.width() + self.scrollArea.width())
            self.display.reposition(width=self.display.width() + self.settingWidget.width() - 120)
        else:
            if self.currentBtn:
                self.currentBtn.setIcon(self.currentBtn.currentIconUnPressed)

            self.currentBtn = btn
            btn.setPressed(True)
            # self.scrollArea.setVisible(True)
            self.settingWidget.setVisible(True)
            self.display.reposition(histogram=self.hasHistogram)

        if isinstance(self.sender(), SystemButton):
            if self.currentGroupBox:
                self.currentGroupBox.setVisible(False)
            gb = self.sender().groupbox
            gb.setVisible(True)

            self.currentGroupBox = gb
            if gb.objectName() == 'set':
                self.fileWidget.setVisible(False)
            else:
                self.fileWidget.setVisible(False)
                self.fileWidget.setSystemName(self.currentGroupBox.objectName())

    def btnTest(self):

        btn = self.sender()

        if self.currentBtn == btn:
            self.currentBtn = None
            btn.setPressed(False)
            self.scrollArea.setVisible(False)
            # btn.setText(btn.text().split('*')[0])
            self.display.reposition(width=self.display.width() + self.scrollArea.width())
        else:
            if self.currentBtn:
                self.currentBtn.setIcon(self.currentBtn.iconUnPressed)

            self.currentBtn = btn
            btn.setPressed(True)
            self.scrollArea.setVisible(True)
            # btn.setText(btn.text() + '*')
            self.display.reposition(width=self.display.width())

        if isinstance(self.sender(), SystemButton):
            gb = self.sender().groupbox
            self.scroll.setValue(gb.mapTo(self.settingWidget, gb.rect().topLeft()).y())

    def tabClose(self, index):
        if self.display.currentIndex() == index:
            self.display.flowInfoWidget.deleteWidget()
        self.display.widget(index).deleteLater()
        self.display.removeTab(index)

    def tabChange(self):
        if self.display.count() == 0:
            return
        widget = self.display.currentWidget()

        self.display.flowInfoWidget.setCurrentDisplayWidget(widget.infoWidget)

    def openFits(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if filename[0]:
            hduList, hdu, image = self.open(filename[0])

            fitsWidget = FitsWidget(parent=self.display, action=self.histogramAct,
                                    hduList=hduList, hdu=hdu, image=image, statusBar=self.parent.statusBar())
            self.addFitsTab(fitsWidget=fitsWidget, name=filename[0].split('/')[-1])

    def open(self, path, hdu=None, image_need=True):
        image = None
        with open(path, 'rb') as input_file:
            hduList = fits.open(input_file)
            if hdu is None:
                hdu = 0
                while hduList[hdu].data is None:
                    hdu += 1
        if image_need:
            image = hduList[hdu].data.astype(np.float32)
        else:
            image = hduList[hdu]
        return hduList, hdu, image


    def setTheme(self, theme):
        for btn in self.btnList:
            btn.setTheme(theme)
        # 不想让qdarktheme影响到pyqtgraph
        # 设置显示背景色为白色，默认为黑色

    def addFitsTab(self, fitsWidget, name=None):
        if name is None:
            name = '未命名  '
        else:
            name = name.rstrip() + '  '
        self.display.addTab(fitsWidget, name)
        self.display.flowInfoWidget.setCurrentDisplayWidget(fitsWidget.infoWidget)
        self.display.setCurrentIndex(self.display.count() - 1)

    def fileResultShow(self, systemName, filePath, fileName):
        widget = None
        isFile, fileType = self.isFileOK(systemName, filePath)
        if systemName == 'tvod' and isFile:
            widget = MatplotWidget(filePath)
        elif systemName == 'smod' and isFile:
            if fileType == 'txt':
                widget = TxTWidget()
                widget.loadTxTFile(filePath)
            else:
                widget = MultiImageWidget(parent=self.display, master=self, action=self.histogramAct)
                widget.setStatusBar(self.parent.statusBar())
                widget.loadFits(filePath)
        elif systemName == 'aofc' and isFile:
            _, _, table = self.open(filePath, image_need=False)
            widget = Cat2Widget(parent=self.display, table=table)
        elif systemName == 'sofc' and isFile:
            if fileType == 'txt':
                widget = TxTWidget()
                widget.loadTxTFile(filePath)
        elif systemName == 'deim' and isFile:
            if fileType == 'png':
                widget = PNGWidget(filePath)

        if widget:
            self.display.addTab(widget, fileName)
            self.display.setCurrentIndex(self.display.count() - 1)

    def isFileOK(self, systemName, path):
        flag = False
        fileType = None
        with open(path, 'r') as file:
            if systemName == 'tvod':
                first_line = file.readline()
                if first_line.startswith('#P'):
                    flag = True
                    fileType = 'plot'
            elif systemName == 'smod':
                first_line = file.readline()
                if first_line.startswith('|'):
                    flag = True
                    fileType = 'txt'
                elif first_line.startswith('#image'):
                    flag = True
                    fileType = 'multi'
            elif systemName == 'aofc':
                flag = True
                fileType = 'fits'
            elif systemName == 'sofc':
                flag = True
                fileType = 'txt'
            elif systemName == 'deim':
                flag = True
                fileType = 'png'
        file.close()
        if not flag:
            self.parent.statusBar().setInfo('目标文件错误')
        return flag, fileType
    def showbtn(self):
        if not self.toggle_layout_visible:
            # 将垂直布局添加到主布局中
            self.layout().addLayout(self.toggle_layout)
            self.toggle_layout_visible = True
        else:
            # 从主布局中移除垂直布局
            self.layout().removeItem(self.toggle_layout)
            self.toggle_layout_visible = False
    def showbtn2(self):
        if not self.toggle2_layout_visible:
            # 将垂直布局添加到主布局中
            self.layout().addLayout(self.toggle2_layout)
            self.toggle2_layout_visible = True
        else:
            # 从主布局中移除垂直布局
            self.layout().removeItem(self.toggle2_layout)
            self.toggle2_layout_visible = False



    def open_action(self):
        filename = QFileDialog.getOpenFileName(self, '打开文件', '.',
                                               filter='fits文件(*.fits *.fit *.gz);;所有文件(*.*)')
        if filename[0]:
            hduList, hdu, image = self.open(filename[0])

            fitsWidget = FitsWidget(parent=self.mainWidget.display, action=self.menuBar().fitsMenu.actions()[0],
                                    hduList=hduList, hdu=hdu, image=image, statusBar=self.statusBar())
            self.mainWidget.addFitsTab(fitsWidget=fitsWidget, name=filename[0].split('/')[-1])

    def emit_close_signal(self):
        # 发射自定义信号
        self.close_signal.emit()

    def openSetWidget(self):
        self.gb9.setVisible(True)
        self.setWidget.setVisible(True)
        # self.set_widget.show()

    # 定义showMenu方法
    def showMenu(self):
        menu = QMenu()
        theme_action = menu.addAction("主题")
        panel_action = menu.addAction("面板")
        header_action = menu.addAction("文件头")
        settings_action = menu.addAction("设置")

        # 为每个动作创建对应的槽函数
        theme_action.triggered.connect(self.changeStyle)
        panel_action.triggered.connect(self.panelFunction)
        header_action.triggered.connect(self.headerFunction)
        settings_action.triggered.connect(self.settingsFunction)

        # 向右移动菜单的位置
        btn_pos = self.mapToGlobal(self.menu_button.pos())
        menu.move(btn_pos + QPoint(self.menu_button.width(), 0))

        # 显示菜单列表
        menu.exec_(btn_pos + QPoint(self.menu_button.width(), 0))

    def changeStyle(self):
        pass

    def panelFunction(self):
        pass
    def headerFunction(self):
        pass
    def settingsFunction(self):
        pass