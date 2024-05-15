from pyqtgraph import ImageView
from myviewbox import MainViewBox
from mygraphicsview import MyGraphicsView
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtGui import QPen, QFont
from PySide6.QtCore import Qt, Signal, QObject
from astropy.table import Table


class SignalEmitter(QObject):
    sigDoubleClicked = Signal(str)

    def __init__(self):
        super().__init__()


class MyRectItem(QGraphicsRectItem):
    sigDoubleClick = Signal(str)

    def __init__(self, calibInfo=None):
        super().__init__()
        self.pen = QPen()
        self.pen.setColor(Qt.green)
        self.pen.setWidth(4)
        self.setPen(self.pen)
        self.calibInfoTable = calibInfo
        self.emitter = SignalEmitter()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if self.rect().contains(event.pos()):
            msg = (f"{self.calibInfoTable['col1']},"
                   f"{self.calibInfoTable['col2']},"
                   f"{self.calibInfoTable['col3']},"
                   f"{self.calibInfoTable['col4']},"
                   f"{self.calibInfoTable['col5']},"
                   f"{self.calibInfoTable['col6']},"
                   f"{self.calibInfoTable['col7']},"
                   f"{self.calibInfoTable['col8']},"
                   f"{self.calibInfoTable['col9']},"
                   f"{self.calibInfoTable['col10']}")
            self.emitter.sigDoubleClicked.emit(msg)


class ImageDisplay(ImageView):

    def __init__(self, parent=None, action=None):
        self.calibs = None
        self.id = None
        self.rectItems = []

        self._view = MainViewBox(self)
        self.color = 'w'
        super(ImageDisplay, self).__init__(parent=parent, view=self._view)

        self._graphicsView = MyGraphicsView(parent=self.ui.layoutWidget)

        self.ui.gridLayout.removeWidget(self.ui.graphicsView)
        self.ui.graphicsView = self._graphicsView
        self.ui.gridLayout.addWidget(self._graphicsView, 0, 0, 2, 1)
        self.ui.graphicsView.setCentralItem(self.view)
        self.ui.graphicsView.setBackground(background='w')
        self.scene = self._graphicsView.scene()

        # 隐藏不必要的控件
        # self.ui.histogram.hide()
        self.ui.menuBtn.hide()
        self.ui.roiBtn.hide()

        self._graphicsView.setMouseTracking(True)

        self.action = action
        self.action.triggered.connect(self.setHistogramShow)
        if self.action.isChecked():
            self.ui.histogram.show()
        else:
            self.ui.histogram.hide()


    @property
    def graphicsView(self):
        return self._graphicsView

    # 重写，返回的是自定义的ViewBox
    def getView(self):
        return self._view

    def moveView(self, rect):
        self._view.setRange(rect, padding=0)

    def setHistogramHidden(self):
        self.ui.histogram.hide()

    def setHistogramShow(self):
        if self.action.isChecked():
            self.ui.histogram.show()
        else:
            self.ui.histogram.hide()

    def setFits(self, fits):
        self.clear()
        self.setImage(fits)
        self.view.autoRange(item=self.imageItem)
        self.setBackgroundColor('k')

    def setCalib(self, calibs):
        self.calibs = calibs
        # text = f"ID:{self.calib['file'][-10:-6]}\nSNR:{self.calib['snr']: .2f}"
        # self.drawRect(self.calib['x'], self.calib['y'], text)

        for i in range(len(self.calibs)):
            calib = self.calibs[i]
            text = f'ID:' + str(i+1) + f"{calib['col1'][-10:-6]}\nSNR:{calib['col9']: .2f}"
            self.drawRect(calib['col3'], calib['col4'], text, calib)

    def drawEllipse(self, x, y):
        r = max(self.image.shape) / 250
        self.ellipse.setRect(x - r, y - r, 2 * r, 2 * r)
        # 颜色
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(max(self.image.shape) / 1000)
        self.ellipse.setPen(pen)

    def drawRect(self, x, y, info, calib):
        r = max(self.image.shape) / 250
        rect = MyRectItem(calib)
        rect.setRect(x - r, y - r, 2 * r, 2 * r)
        self.rectItems.append(rect)

        text = QGraphicsTextItem()
        text.setDefaultTextColor(Qt.green)
        text.setFont(QFont("Arial", 18))
        text.setX(x + r)
        text.setY(y - r - 4)
        text.setPlainText(info)

        self._view.addItem(rect)
        self._view.addItem(text)

    def setBackgroundColor(self, color):
        if self.color != color:
            self.ui.graphicsView.setBackground(background=color)
            self.color = color
