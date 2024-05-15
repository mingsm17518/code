# coding:utf-8

import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt

from minimap import MiniMap
from imagedisplay import ImageDisplay
from cursordisplay import CursorDisplay
from fitsinfowidget import FitsInfoWidget

# 设置显示背景色为白色，默认为黑色
# pg.setConfigOption('background', 'w')
# 设置显示前景色为黑色，默认为灰色
# pg.setConfigOption('foreground', 'k')
#设置图像显示以行为主，默认以列为主
pg.setConfigOption('imageAxisOrder', 'row-major')
# 设置
pg.setConfigOption('mouseRateLimit', 1000)


class FitsWidget(QWidget):

    def __init__(self, parent=None, action=None, tabName=None, hduList=None, hdu=None, image=None, statusBar=None):
        super().__init__(parent)

        self.parent = parent
        self.hduList=None
        self.hdu=None
        self.image=None
        self.calib = None

        if tabName:
            self.tabName = tabName
        else:
            self.tabName = '未命名'

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # 图片展示区
        self.mainWidget = QWidget(self)
        self.main = ImageDisplay(self.mainWidget, action=action)
        # 缩略图
        self.minimapWidget = QWidget(self.mainWidget)
        self.minimap = MiniMap(self.minimapWidget)
        # 坐标等信息展示区
        self.infoFlowWidget = QWidget(self.mainWidget)
        # self.infoFlowLabel = CursorDisplay(self.infoFlowWidget)
        self.infoWidget = FitsInfoWidget(self, statusBar=statusBar)
        self.infoWidget.setVisible(False)

        # 关联信号与槽
        # 展示区的缩放、拖拽等变化会让缩略图的矩形框更新
        # 缩略图的矩形框移动会更新展示区
        self.main.getView().sigUpdateRect.connect(self.minimap.updateRect)
        self.minimap.sigUpdateMainDisPlay.connect(self.main.moveView)
        # 鼠标实时坐标
        # 主视图上鼠标移动时，会传递坐标进行转换
        self.main.graphicsView.sigMouseMoved.connect(self.main.getView().transformCursor)

        # 转换完后更新标签
        # self.main.getView().sigTransformCursor.connect(self.getFitsData)
        self.main.getView().sigTransformCursor.connect(self.infoWidget.getFitsData)

        # 初始化界面
        self.initWidget()
        # 初始化数据
        self.initData(hduList, hdu, image)

        # 操作按钮
        # 测试阶段-print
        # self.ofn = Function()
        # self.operation.btnGetConfig.clicked.connect(lambda: self.ofn.getConfig())
        # self.operation.btnOrient.clicked.connect(self.ofn.orientAstronomy)
        # self.operation.btnCalibrate.clicked.connect(self.ofn.calibrateFlow)
        # self.operation.btnCorrectImage.clicked.connect(self.ofn.correctImage)
        # self.operation.btnUpdateHeader.clicked.connect(self.ofn.updateHeader)
        # self.operation.btnExtractStar.clicked.connect(self.ofn.extractStarImage)
        # self.operation.btnCorrectMerge.clicked.connect(self.ofn.correctImageMerging)

    def test(self):
        print("test")

    def initWidget(self):
        # 布局
        layoutMiniMap = QHBoxLayout()
        layoutMiniMap.setSpacing(0)
        layoutMiniMap.setContentsMargins(0, 0, 0, 0)
        layoutMain = QHBoxLayout()
        layoutMain.setSpacing(0)
        layoutMain.setContentsMargins(0, 0, 0, 0)
        # 添加控件
        # 禁止缩略图拉伸
        layoutMiniMap.addWidget(self.minimap)
        self.minimapWidget.setLayout(layoutMiniMap)

        layoutMain.addWidget(self.main)
        self.mainWidget.setLayout(layoutMain)

        self.layout.addWidget(self.mainWidget)

        layoutInfo = QHBoxLayout(self.infoFlowWidget)
        # layoutInfo.addWidget(self.infoFlowLabel)
        self.infoFlowWidget.setLayout(layoutInfo)
        self.infoFlowWidget.raise_()
        self.minimapWidget.raise_()
        self.minimapWidget.resize(100, 100)

        # self.layoutLeft.addLayout(self.layoutMiniMap)
        # self.layoutLeft.addWidget(self.info)
        # self.layoutLeft.addWidget(self.operation)
        # self.spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # self.layoutLeft.addItem(self.spacerItem)
        # self.layoutLeft.setStretch(0, 0)
        # self.layoutLeft.setStretch(1, 0)
        # self.layoutLeft.setStretch(2, 0)
        # self.layoutLeft.setStretch(3, 1)
        # 将左侧布局添加到主布局
        # self.layoutMain.addLayout(self.layoutLeft)
        # self.layoutMain.addWidget(self.main)

        # 设定缩略图不改变大小，展示区可拉伸
        # self.layoutMain.setStretch(0, 0)
        # self.layoutMain.setStretch(1, 1)
        # self.setLayout(self.layoutMain)

    def initData(self, hduList=None, hdu=None, image=None):
        self.setHDU(hduList, hdu)
        self.setFits(image)

    def setHDU(self, hduList, hdu):
        self.hduList = hduList
        self.hdu = hdu
        self.header = repr(self.hduList[hdu].header)
        self.infoWidget.setHDU(self.hduList, self.hdu)

    def setFits(self, image):
        self.image = image
        # 显示fits
        black, white = np.percentile(self.image, [50, 99.7])
        clipped = (self.image - black).clip(0, white - black)
        self.image = (clipped / clipped.max() * 255).astype(np.uint8)

        y, x = self.image.shape
        if y > x:
            self.minimapWidget.resize(100, 100 * y / x)
        else:
            self.minimapWidget.resize(100 * y / x, 100)

        self.minimap.setFits(self.image)
        self.main.setFits(self.image)
        self.minimap.updateRect(self.main.getView().viewRect())
        self.infoWidget.setImage(self.image)
        # self.parent.setFlowInfoWidgetCurrentWidget(self.infoWidget)

    def getFitsData(self, pos):
        if self.image is None:
            return
        x = int(pos.x())
        y = int(pos.y())
        if x < 0 or x > self.image.shape[1] - 1 or y < 0 or y > self.image.shape[0] - 1:
            self.infoFlowLabel.set(0, 0, 0)
            return
        self.infoFlowLabel.set(x, y, self.image[y, x])

    def init(self):
        self.infoFlowWidget.setFixedWidth(self.main.getView().width())

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.infoFlowWidget.setFixedWidth(self.main.getView().width())

    def setTheme(self, theme):
        if theme == 'light':
            pass
        else:
            pass



