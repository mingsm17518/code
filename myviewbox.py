import numpy as np
from pyqtgraph import Point, ViewBox, GraphicsView
from pyqtgraph import functions as fn
from PySide6.QtCore import Qt, Signal, QRectF, QEvent
from pyqtgraph.GraphicsScene.mouseEvents import MouseDragEvent
from PySide6.QtWidgets import QGraphicsSceneWheelEvent


class MiniMapViewBox(ViewBox):
    # 信号
    sigZoomRect = Signal(float)
    sigUpdateRect = Signal(QRectF)
    sigMoveRect = Signal(Point)

    def __init__(self):
        super(MiniMapViewBox, self).__init__()

    def mousePressEvent(self, ev):
        """
        @param ev:
        @return:
        按下鼠标左键，将鼠标相对在缩略图的坐标传给槽
        """
        self.sigMoveRect.emit(Point(fn.invertQTransform(self.childGroup.transform()).map(ev.pos())))
        ev.accept()

    def mouseMoveEvent(self, ev):
        self.mousePressEvent(ev)
        ev.accept()

    def wheelEvent(self, ev, axis=None):
        if axis in (0, 1):
            mask = [False, False]
            mask[axis] = self.state['mouseEnabled'][axis]
        else:
            mask = self.state['mouseEnabled'][:]
        s = 1.02 ** (ev.delta() * self.state['wheelScaleFactor'])  # actual scaling factor

        self.sigZoomRect.emit(s)
        ev.accept()
        self.sigRangeChangedManually.emit(mask)


class MainViewBox(ViewBox):
    # 信号
    sigZoomRect = Signal(float)
    sigUpdateRect = Signal(QRectF)
    sigTransformCursor = Signal(Point)

    sigMousePress = Signal()
    sigMouseRelease = Signal()

    sigUpdate = Signal(int)

    def __init__(self, parent=None):
        super(MainViewBox, self).__init__()
        self.parent = parent

    # 转换坐标后更新标签
    def transformCursor(self, pos):
        self.sigTransformCursor.emit(fn.invertQTransform(self.childGroup.transform()).map(pos))

    def mouseClickEvent(self, ev):
        # 禁用源库定义的点击事件
        ev.accept()
        pass

    def mouseDragEvent(self, ev, axis=None):
        ev.accept()
        if ev.isStart():
            self.sigMousePress.emit()
        if ev.isFinish():
            self.sigMouseRelease.emit()
        self.mouseDrag(ev)
        self.sigUpdateRect.emit(self.viewRect())
        self.sigUpdate.emit(self.parent.id)

    def wheelEvent(self, ev, axis=None):
        self.wheel(ev)
        ev.accept()
        self.sigUpdateRect.emit(self.viewRect())
        self.sigUpdate.emit(self.parent.id)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        self.sigUpdateRect.emit(self.viewRect())

    def mouseDrag(self, ev, axis=None):
        # 展示区处理，基本照搬库源代码
        pos = ev.pos()
        lastPos = ev.lastPos()
        dif = pos - lastPos
        dif = dif * -1

        mouseEnabled = np.array(self.state['mouseEnabled'], dtype=np.float64)
        mask = mouseEnabled.copy()
        if axis is not None:
            mask[1 - axis] = 0.0

        # Scale or translate based on mouse button
        if ev.button() in [Qt.MouseButton.LeftButton, Qt.MouseButton.MiddleButton]:
            if self.state['mouseMode'] == ViewBox.RectMode and axis is None:
                if ev.isFinish():  # This is the final move in the drag; change the view scale now
                    # print "finish"
                    self.rbScaleBox.hide()
                    ax = QRectF(Point(ev.buttonDownPos(ev.button())), Point(pos))
                    ax = self.childGroup.mapRectFromParent(ax)
                    self.showAxRect(ax)
                    self.axHistoryPointer += 1
                    self.axHistory = self.axHistory[:self.axHistoryPointer] + [ax]
                else:
                    # update shape of scale box
                    self.updateScaleBox(ev.buttonDownPos(), ev.pos())
            else:
                tr = self.childGroup.transform()
                tr = fn.invertQTransform(tr)
                tr = tr.map(dif * mask) - tr.map(Point(0, 0))

                x = tr.x() if mask[0] == 1 else None
                y = tr.y() if mask[1] == 1 else None

                self._resetTarget()
                if x is not None or y is not None:
                    self.translateBy(x=x, y=y)
                self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
        elif ev.button() & Qt.MouseButton.RightButton:
            # print "vb.rightDrag"
            if self.state['aspectLocked'] is not False:
                mask[0] = 0

            dif = ev.screenPos() - ev.lastScreenPos()
            dif = np.array([dif.x(), dif.y()])
            dif[0] *= -1
            s = ((mask * 0.02) + 1) ** dif

            tr = self.childGroup.transform()
            tr = fn.invertQTransform(tr)

            x = s[0] if mouseEnabled[0] == 1 else None
            y = s[1] if mouseEnabled[1] == 1 else None

            center = Point(tr.map(ev.buttonDownPos(Qt.MouseButton.RightButton)))
            self._resetTarget()
            self.scaleBy(x=x, y=y, center=center)
            self.sigRangeChangedManually.emit(self.state['mouseEnabled'])

    def wheel(self, ev, axis=None):
        if axis in (0, 1):
            mask = [False, False]
            mask[axis] = self.state['mouseEnabled'][axis]
        else:
            mask = self.state['mouseEnabled'][:]
        s = 1.02 ** (ev.delta() * self.state['wheelScaleFactor'])  # actual scaling factor
        center = Point(fn.invertQTransform(self.childGroup.transform()).map(ev.pos()))

        s = [(None if m is False else s) for m in mask]
        self._resetTarget()
        self.scaleBy(s, center)
        self.sigRangeChangedManually.emit(mask)
