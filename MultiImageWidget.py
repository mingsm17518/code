import os.path
from pathlib2 import Path
import numpy as np
from astropy.io import fits, ascii
from astropy.table import Table
from PySide6.QtWidgets import (QStackedWidget, QWidget, QScrollArea, QLabel, QSpacerItem, QSizePolicy, QDialog,
                               QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout)
from PySide6.QtCore import QTimer, QThread, Signal, Qt
from imagedisplay import ImageDisplay

import pyqtgraph as pg

# 设置显示背景色为白色，默认为黑色
# pg.setConfigOption('background', 'w')
# 设置显示前景色为黑色，默认为灰色
# pg.setConfigOption('foreground', 'k')
# 设置图像显示以行为主，默认以列为主
pg.setConfigOption('imageAxisOrder', 'row-major')
# 设置
pg.setConfigOption('mouseRateLimit', 1000)


class CalibWidget(QDialog):
    def __init__(self, datas):
        super().__init__()
        file_name = datas[0]
        time = datas[1]
        x = datas[2]
        y = datas[3]
        ra = datas[4]
        dec = datas[5]
        flux = datas[6]
        mag = datas[7]
        snr = datas[8]
        fwhm = datas[9]
        self.setWindowTitle('详细信息')

        info = (f"file:{file_name}\ntime:{time}\n(x, y):({x}, {y})\nra:{ra}\ndec:{dec}\nflux:{flux}\nmag:{mag}\nsnr:{snr}\n"
                f"fwhm:{fwhm}")
        label = QLabel(self)
        label.setText(info)
        layout = QVBoxLayout(self)
        layout.addWidget(label)


class FlowButton(QPushButton):

    def __init__(self, text=None, parent=None):
        super().__init__(text=text, parent=parent)

        self.setFixedSize(32, 32)


class FlowBtnWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗体背景透明

        self.setLayout(QHBoxLayout())

        self.layout().setSpacing(6)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(32 * 5 + 6 * 4)
        self.setFixedHeight(32)


class FlowCalibInfoArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setGeometry(0, 0, 150, 200)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 128);")
        self.viewport().setStyleSheet("background-color: rgba(0, 0, 0, 128);")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.container = QWidget()
        self.container.setContentsMargins(0, 0, 0, 0)
        self.container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(self.container)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        self.setWidget(self.container)
        self.setContentsMargins(0, 0, 0, 0)
        self.btns = []

    def addCalibBtn(self, str_calib):
        datas = str_calib.split(',')
        file_name = datas[0]
        time = datas[1]
        x = datas[2]
        y = datas[3]
        ra = datas[4]
        dec = datas[5]
        flux = datas[6]
        mag = datas[7]
        snr = datas[8]
        fwhm = datas[9]

        wrapper_widget = QWidget(self.container)
        button = QPushButton(wrapper_widget)
        button.setText(f"ID:test_id\nx,y:{x},{y}\nsnr:{snr}")
        button.setStyleSheet("""
                        QPushButton {
                            background-color: rgba(255, 255, 255, 128);
                            border: none;
                            text-align: left;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 255, 255, 180);
                        }
                    """)
        button.clicked.connect(lambda: self.showCalibWidget(datas))
        # 创建关闭图标
        closeIcon = QLabel(wrapper_widget)
        closeIcon.setText('<')
        closeIcon.mousePressEvent = lambda event, widget=wrapper_widget: self.closeButton(event, widget)
        closeIcon.setStyleSheet("""
                        QLabel {
                            background-color: rgba(255, 255, 255, 128);
                            border: none;
                            text-align: left;
                        }
                    """)

        h_layout = QHBoxLayout()
        h_layout.addWidget(button)
        h_layout.addWidget(closeIcon)
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setStretch(0, 1)

        wrapper_widget.setLayout(h_layout)
        self.container.layout().insertWidget(self.container.layout().count() - 1, wrapper_widget)
        self.btns.append(button)

    def closeButton(self, event, widget):
        widget.parent().layout().removeWidget(widget)
        widget.deleteLater()

    def showCalibWidget(self, calib):
        w = CalibWidget(calib)
        w.show()
        w.exec()


class TableWidget(QWidget):
    def __init__(self, parent=None, data=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.table = QTableWidget()
        rowCount = 0
        for i in range(len(data)):
            rowCount = rowCount + len(data[i])
        self.table.setRowCount(rowCount)  # 设置行数
        self.table.setColumnCount(len(data[0].colnames))  # 设置列数
        self.table.setHorizontalHeaderLabels(
            ['ID', 'time', 'x', 'y', 'ra', 'dec', 'flux', 'mag', 'snr', 'fwhm'])  # 设置表头

        # 填充表格数据
        itemName = ''
        for i in range(len(data)):
            for row in range(len(data[i])):
                for column in range(len(data[i].colnames)):
                    if column == 0:  # ID
                        itemName = str(i+1) + '_' + data[i][row][column][-10:-6]
                    elif column == 1:  # time
                        itemName = data[i][row][column]
                    elif column == 4:  # ra
                        itemName = f"{data[i][row][column]: .6f}"
                    elif column == 5:  # dec
                        itemName = f"{data[i][row][column]: .6f}"
                    elif column == 7:  # mag
                        itemName = f"{data[i][row][column]: .4f}"
                    else:
                        itemName = f"{data[i][row][column]: .2f}"
                    item = QTableWidgetItem(itemName)
                    self.table.setItem(i * len(data[i]) + row, column, item)

        layout.addWidget(self.table)


class MultiImageWidget(QWidget):
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateFlowInfoWidgetPos()

    def __init__(self, parent=None, master=None, action=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.master = master
        self.action = action

        self.status = None
        self.datas = None
        self.fits = []
        self.fitsWidgets = []
        self.currentWidget = 0
        self.infoWidget = None
        self.isPlaying = False

        self.dataWidget = None
        self.flowCalibWidget = FlowCalibInfoArea(self)
        self.flowCalibWidget.setVisible(False)

        self.flowInfoWidget = FlowBtnWidget(parent=self)
        self.btn_last = FlowButton('<-', parent=self.flowInfoWidget)
        self.btn_play = FlowButton('▶', parent=self.flowInfoWidget)
        self.btn_pause = FlowButton('||', parent=self.flowInfoWidget)
        self.btn_next = FlowButton('->', parent=self.flowInfoWidget)
        self.btn_data = FlowButton('...', parent=self.flowInfoWidget)
        self.flowInfoWidget.layout().addWidget(self.btn_last)
        self.flowInfoWidget.layout().addWidget(self.btn_play)
        self.flowInfoWidget.layout().addWidget(self.btn_pause)
        self.flowInfoWidget.layout().addWidget(self.btn_next)
        self.flowInfoWidget.layout().addWidget(self.btn_data)
        self.flowInfoWidget.setVisible(False)

        self.btn_play.clicked.connect(self.play)
        self.btn_pause.clicked.connect(self.pause)
        self.btn_last.clicked.connect(self.last)
        self.btn_next.clicked.connect(self.next)
        self.btn_data.clicked.connect(self.showData)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.timeOut)
        # self.timer.start()

        self.setLayout(QVBoxLayout(self))

        self.stackedWidget = QStackedWidget(self)
        # self.btnPlay = QPushButton('播放')
        # self.btnPause = QPushButton('暂停')
        # self.btnPlay.clicked.connect(self.play)
        # self.btnPause.clicked.connect(self.pause)

        self.layout().addWidget(self.stackedWidget)
        # self.layout().addWidget(self.btnPlay)
        # self.layout().addWidget(self.btnPause)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def addFitsWidget(self, fitsWidget):
        self.fitsWidgets.append(fitsWidget)
        self.stackedWidget.addWidget(fitsWidget)
        # self.layout().addWidget(fitsWidget)
        fitsWidget.id = len(self.fitsWidgets)
        self.connectSlot(fitsWidget)

    def connectSlot(self, fitsWidget):
        for rectItem in fitsWidget.rectItems:
            rectItem.emitter.sigDoubleClicked.connect(self.getTargetCalib)

        v = fitsWidget.getView()
        v.sigUpdate.connect(self.freshFits)
        v.sigMousePress.connect(self.pause)
        v.sigMouseRelease.connect(self.play)

    def timeOut(self):
        if len(self.fitsWidgets) > 0:
            self.currentWidget = (self.currentWidget + 1) % len(self.fitsWidgets)
            self.stackedWidget.setCurrentWidget(self.fitsWidgets[self.currentWidget])

    def play(self):
        if isinstance(self.sender(), QPushButton):
            self.isPlaying = True
        if self.isPlaying:
            self.timer.start()

    def pause(self):
        if isinstance(self.sender(), QPushButton):
            self.isPlaying = False
        self.timer.stop()
        self.timer.setInterval(1000)

    def getTargetCalib(self, calib):
        self.flowCalibWidget.addCalibBtn(calib)

    def freshFits(self, i):
        rect = self.sender().viewRect()
        for w in self.fitsWidgets:
            if w.id == i:
                continue
            else:
                w.getView().setRange(rect, padding=0)

    def loadFits(self, input_path):
        with open(input_path, 'r') as file:
            lines = file.readlines()[:3]
            image_path = lines[0].split(':')[1].strip()
            image_number = int(lines[1].split(':')[1].strip())
            object_number = int(lines[2].split(':')[1].strip())
        file.close()

        data = ascii.read(input_path, delimiter=' ', data_start=0)
        size = len(data) // object_number
        datas = [data[i:i + size] for i in range(0, len(data), size)]

        self.datas = datas

        prefixStr = image_path + str(datas[0]['col1'][0])[:-10]
        suffixStr = str(datas[0]['col1'][0])[-6:]

        t = WorkThread(parent=self)
        t.sigReadOK.connect(self.load)
        if self.status:
            t.sigProg.connect(self.status.updateInfo)
        t.setParameter(prefixStr, suffixStr, image_number)
        t.start()
        self.master.gb3BtnLoad.setEnabled(False)

    def load(self, images):
        self.fits.clear()
        self.fitsWidgets.clear()
        self.currentWidget = 0
        self.isPlaying = False

        self.fits = images
        self.dataWidget = None
        self.dataWidget = TableWidget(data=self.datas)
        self.dataWidget.setWindowTitle('详情数据')
        self.dataWidget.resize(800, 500)
        self.dataWidget.setVisible(False)

        for i in range(len(images)):
            fitsWidget = ImageDisplay(self, action=self.action)
            fitsWidget.setFits(images[i])
            calibs = []
            for j in range(len(self.datas)):
                calibs.append(self.datas[j][i])
            fitsWidget.setCalib(calibs)
            self.addFitsWidget(fitsWidget)

        self.master.gb3BtnLoad.setEnabled(True)
        # 将画面显示
        self.parent.setCurrentWidget(self)
        self.updateFlowInfoWidgetPos()
        self.flowInfoWidget.setVisible(True)
        self.flowCalibWidget.setVisible(True)

    def updateFlowInfoWidgetPos(self):
        x = self.x() + (self.width() - self.flowInfoWidget.width()) // 2
        y = self.y() + self.height() - self.flowInfoWidget.height()
        self.flowInfoWidget.move(x, y)
        self.flowInfoWidget.raise_()
        self.flowCalibWidget.move(0, 0)
        self.flowCalibWidget.raise_()

    def last(self):
        index = (self.stackedWidget.currentIndex() - 1) % len(self.fits)
        self.stackedWidget.setCurrentIndex(index)

    def next(self):
        index = (self.stackedWidget.currentIndex() + 1) % len(self.fits)
        self.stackedWidget.setCurrentIndex(index)

    def setStatusBar(self, statusBar):
        self.status = statusBar

    def showData(self):
        if self.dataWidget:
            self.dataWidget.setVisible(True)


def openFits(path, hdu=None):
    with open(path, 'rb') as input_file:
        hduList = fits.open(input_file)
        if hdu is None:
            hdu = 0
            while hduList[hdu].data is None:
                hdu += 1
    return hduList[hdu].data.astype(np.float32)


class WorkThread(QThread):
    sigReadOK = Signal(list)
    sigProg = Signal(int, int, str)

    def __init__(self, parent=None):
        super(WorkThread, self).__init__(parent=parent)
        self.prefixStr = None
        self.suffixStr = None
        self.num = 0
        self.fits = []

    def run(self):
        self.fits.clear()

        self.sigProg.emit(0, self.num, '加载fits')

        for i in range(1, self.num + 1):
            filename = self.prefixStr + str(i).zfill(4) + self.suffixStr

            image = openFits(filename)
            black, white = np.percentile(image, [50, 99.7])
            clipped = (image - black).clip(0, white - black)
            image = (clipped / clipped.max() * 255).astype(np.uint8)

            self.fits.append(image)
            self.sigProg.emit(i, self.num, '加载fits')

        self.sigReadOK.emit(self.fits)

    def setParameter(self, prefixStr=None, suffixStr=None, num=0):
        self.prefixStr = prefixStr
        self.suffixStr = suffixStr
        self.num = num
