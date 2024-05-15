from pyqtgraph import ImageView, Point
from myviewbox import MiniMapViewBox
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtWidgets import QGraphicsRectItem


class MiniMap(ImageView):
    # 信号
    sigUpdateMainDisPlay = Signal(QRectF)

    def __init__(self, parent=None):

        self.master = parent

        self.view = MiniMapViewBox()
        # 设置禁止鼠标缩放拖拽
        self.view.setMouseEnabled(False, False)
        # 关联信号和槽
        self.view.sigMoveRect.connect(self.moveRect)
        self.view.sigZoomRect.connect(self.zoomRect)

        super(MiniMap, self).__init__(parent, view=self.view)

        # 隐藏不必要控件
        self.ui.histogram.hide()
        self.ui.menuBtn.hide()
        self.ui.roiBtn.hide()
        self.ui.graphicsView.setBackground(background='w')

        self.color = 'w'

        self.view.setBorder(color='r', width=2)

        # 创建矩形框
        self._rect = QGraphicsRectItem()
        self.view.addItem(self._rect)

        # 矩形框颜色
        self.pen = QPen()
        self.pen.setColor(Qt.green)
        self.pen.setWidth(1)
        self._rect.setPen(self.pen)
        self._rect.setVisible(False)

    def setPenWidth(self, w):
        self.pen.setWidth(w)
        self._rect.setPen(self.pen)

    def setRect(self, rect):
        self._rect.setRect(rect)

    def setFits(self, fits):
        y, x = fits.shape
        rect = QRectF(0, 0, x, y)
        self.setPenWidth(max(x, y) / 100)
        self.clear()
        self.setImage(fits)
        self.view.autoRange(item=self.imageItem, padding=0)

        if not self._rect.isVisible():
            self._rect.setVisible(True)

        self.setBackgroundColor('k')

    def getView(self):
        return self.view

    def updateRect(self, rect):
        self.setRect(rect)

    def moveRect(self, point):
        """
        @param point: 鼠标坐标
        @return:
        """
        w = self._rect.rect().width()
        h = self._rect.rect().height()

        left = point.x() - w/2.0
        top = point.y() - h/2.0

        new = QRectF(left, top, w, h)
        self.setRect(new)
        self.sigUpdateMainDisPlay.emit(new)

    def zoomRect(self, scale):
        """
        @param scale: 缩放倍数
        @return:
        """
        vr = self._rect.rect()
        center = Point(vr.center())

        tl = center + (vr.topLeft() - center) * scale
        br = center + (vr.bottomRight() - center) * scale

        new = QRectF(tl, br)
        self.setRect(new)
        self.sigUpdateMainDisPlay.emit(new)

    def setBackgroundColor(self, color):
        if self.color != color:
            self.ui.graphicsView.setBackground(background=color)
