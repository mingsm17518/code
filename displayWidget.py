from PySide6.QtWidgets import QStackedWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget


class DisplayTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hasHistogram = True
        self.flowInfoWidget = FlowInfoWidget(parent=self, horizontal='right')
        self.flowInfoWidget.setVisible(False)
        # self.layout().setSpacing(0)
        # self.layout().setContentsMargins(0, 0, 0, 0)

    def setCurrentTab(self, widget):
        self.setCurrentWidget(widget)
        self.flowInfoWidget.raise_()

    def setHistogram(self, flag):
        self.hasHistogram = flag

    def reposition(self, width=None, height=None, histogram=None):
        if not width:
            if histogram:
                width = self.width() - 120
            else:
                width = self.width()
        if not height:
            height = self.height()
        if self.flowInfoWidget.currentDisplayWidget and self.flowInfoWidget.currentDisplayWidget.isVisible():
            self.flowInfoWidget.setFixedWidth(width)
            self.flowInfoWidget.move(0, height - self.flowInfoWidget.height())
        else:
            self.flowInfoWidget.move(0, height - self.flowInfoWidget.height())

    def setFlowInfoWidgetCurrentWidget(self, widget):
        self.flowInfoWidget.setCurrentDisplayWidget(widget)


class DisplayWidget(QStackedWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.flowInfoWidget = FlowInfoWidget(parent=self, horizontal='right')
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def setCurrentWidget(self, widget):
        super().setCurrentWidget(widget)
        self.flowInfoWidget.raise_()

    def reposition(self, width=None, height=None):
        if not width:
            width = self.width()
        if not height:
            height = self.height()
        if self.flowInfoWidget.currentDisplayWidget and self.flowInfoWidget.currentDisplayWidget.isVisible():
            self.flowInfoWidget.setFixedWidth(width)
            self.flowInfoWidget.move(0, height - self.flowInfoWidget.height())
        else:
            self.flowInfoWidget.move(width - self.flowInfoWidget.width(),
                                     height - self.flowInfoWidget.height())

    def setFlowInfoWidgetCurrentWidget(self, widget):
        self.flowInfoWidget.setCurrentDisplayWidget(widget)


class FlowInfoWidget(QWidget):

    def __init__(self, horizontal=None, vertical=None, parent=None):

        #if horizontal not in ['left', 'right'] and vertical not in ['top', 'bottom']:
        #    print('error')
        #    return None

        super().__init__(parent)
        self.parent = parent
        self._height = 160
        self.currentDisplayWidget = QWidget()
        self.currentDisplayWidget.setVisible(False)

        # self.label = QLabel('要展示内容')
        # self.label.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

        self.btnUnfold = QPushButton()
        self.btnUnfold.clicked.connect(self.update)
        self.btnUnfold.setFixedWidth(20)
        self.btnUnfold.setMinimumHeight(self._height)
        self.displayLayout = QHBoxLayout()
        self.displayLayout.setSpacing(0)
        self.displayLayout.setContentsMargins(0, 0, 0, 0)
        self.displayLayout.addWidget(self.currentDisplayWidget)

        flag = True
        self.layout = None
        if horizontal is not None:
            self.layout = QHBoxLayout(self)
            flag = True if horizontal == 'left' else False

        if vertical is not None:
            self.layout = QVBoxLayout(self)
            flag = True if vertical == 'top' else False

        if flag:
            self.layout.addWidget(self.btnUnfold)
            self.layout.addLayout(self.displayLayout)
            self.btnUnfold.setText('<')
            # self.layout.addWidget(self.label)
        else:
            # self.layout.addWidget(self.label)
            self.layout.addLayout(self.displayLayout)
            self.layout.addWidget(self.btnUnfold)
            self.btnUnfold.setText('>')

        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.resize(self.btnUnfold.width(), self._height)

    def setCurrentDisplayWidget(self, widget):
        # 移除原有的面板
        if self.currentDisplayWidget:
            self.currentDisplayWidget.setVisible(False)
            self.displayLayout.removeWidget(self.currentDisplayWidget)

        self.currentDisplayWidget = widget
        # 如果是None，需要关闭
        if not self.currentDisplayWidget:
            self.checkBtnState()
            return

        # 显示新的面板
        self.displayLayout.addWidget(widget)
        if self.btnUnfold.text() == '>':
            self.currentDisplayWidget.setVisible(False)
        else:
            self.currentDisplayWidget.setVisible(True)

    def deleteWidget(self):
        if self.currentDisplayWidget:
            self.currentDisplayWidget.deleteLater()
        self.currentDisplayWidget = None
        self.checkBtnState()

    def setWidgetVisible(self, flag):
        if self.currentDisplayWidget:
            self.currentDisplayWidget.setVisible(flag)
        self.checkBtnState()

    def checkBtnState(self):
        if not self.currentDisplayWidget:
            self.btnUnfold.setText('>')
            self.setFixedWidth(self.btnUnfold.width())
            self.move(0, self.parent.height() - self.height())
            return

        if self.currentDisplayWidget.isVisible():
            self.btnUnfold.setText('<')
            if self.parent.hasHistogram:
                self.setFixedWidth(self.parent.width() - 120)
            else:
                self.setFixedWidth(self.parent.width())
            self.move(0, self.parent.height() - self.height())
        else:
            self.btnUnfold.setText('>')
            self.setFixedWidth(self.btnUnfold.width())
            # self.move(self.parent.width() - self.btnUnfold.width(), self.parent.height() - self.height())
            self.move(0, self.parent.height() - self.height())

    def update(self):
        if isinstance(self.sender(), QPushButton):
            # self.label.setVisible(False if self.label.isVisible() else True)
            if self.currentDisplayWidget:
                self.currentDisplayWidget.setVisible(False if self.currentDisplayWidget.isVisible() else True)
        self.checkBtnState()



