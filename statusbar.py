from PySide6.QtWidgets import QStatusBar, QLabel, QProgressBar, QWidget, QHBoxLayout, QStyleOptionProgressBar, QStyle
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient


class StatusBar(QStatusBar):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMaximumHeight(20)

        self.progress = ProgressWidget(self)
        self.addPermanentWidget(self.progress)

        self.showMessage('.')

    def updateInfo(self, value=None, maxValue=None, text=None):
        self.progress.setValue(value, maxValue, text)

    def setInfo(self, text=None):
        #if self.progress.isVisible():
        #    self.progress.setVisible(False)
        self.showMessage(text)


class ProgressWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setLayout(QHBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(3)

        self.progInfo = QLabel(self)
        self.progInfo.setText('进度条提示')
        self.progInfo.setAlignment(Qt.AlignCenter)

        # self.progress = QProgressBar()
        self.progress = MyProgress()
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 100.0)
        self.progress.setValue(0)

        self.nextValue = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        self.timer.setInterval(30)  # 每隔 30 毫秒触发一次 timeout 信号

        self.layout().addWidget(self.progInfo)
        self.layout().addWidget(self.progress)

        self.setVisible(False)

    def setValue(self, value=None, maxValue=None, text=None):

        if not text:
            self.progInfo.setText('进度({}/{})'.format(value, maxValue))
        else:
            self.progInfo.setText('{}({}/{})'.format(text, value, maxValue))

        if maxValue:
            self.progress.setRange(0.0, maxValue * 100)

        self.nextValue = (value + 1) * 95

        if self.progress.value() < value:
            self.initTimer()

        # self.progress.setValue(value * 100)
        # if self.nextValue == 0:
        #     self.nextValue = value * 100
        # self.nextValue = self.nextValue + 100

        if not self.timer.isActive():
            self.timer.start()
            self.progress.setTimerActivated(True)  # 开始渐变

        if not self.isVisible():
            self.setVisible(True)

        if value == maxValue:
            self.setVisible(False)
            self.progInfo.setText('Done!')
            # init
            self.progress.setValue(0)
            self.initTimer()
            self.nextValue = 0

    def updateProgress(self):
        currentValue = self.progress.value()
        # print('currentValue', currentValue, 'nextValue', self.nextValue)
        if currentValue < self.nextValue and currentValue < self.progress.maximum():
            self.progress.setValue(currentValue + 1)
        else:
            self.timer.stop()  # 进度条满后停止计时器
            # self.progress.setTimerActivated(True)  # 开始渐变

    def initTimer(self):
        self.timer.stop()
        self.timer.setInterval(30)
        self.progress.setTimerActivated(False)  # 停止渐变

class MyProgress(QProgressBar):
    def paint(self, painter, gradient):
        progress = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        progress_width = self.width() * progress
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, progress_width, self.height())

    def draw(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # 使用渐变绘制内部的填充进度
        green_gradient = QLinearGradient(0, 0, self.width(), 0)
        green_gradient .setColorAt(0, QColor(0, 205, 0))
        green_gradient .setColorAt(1, QColor(0, 139, 0))
        self.paint(painter, green_gradient)

        # 绘制白色带
        white_gradient = QLinearGradient(self.white_gradient_shift, 0,
                                         self.white_gradient_shift + self.white_gradient_max_width, 0)
        white_gradient.setColorAt(0, QColor(255, 255, 255, 0))
        white_gradient.setColorAt(0.5, QColor(255, 255, 255, 80))
        white_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        self.paint(painter, white_gradient)

        painter.end()

    def __init__(self):
        super().__init__()
        self.opt = None
        self.outerRect = None
        self.innerRect = None

        self.white_gradient_shift = 0
        self.white_gradient_max_width = 50

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGradient)
        self.timer.setInterval(30)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.draw()

    def updateGradient(self):
        progress = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        progress_width = int(self.width() * progress)
        if progress_width == 0:
            return
        self.white_gradient_shift = (int(self.white_gradient_shift) + 1) % progress_width
        self.update()

    def setTimerActivated(self, flag):
        if flag:
            self.timer.start()
        else:
            self.timer.stop()
            self.timer.setInterval(30)
