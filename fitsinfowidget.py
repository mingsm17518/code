from PySide6.QtWidgets import QWidget, QHBoxLayout, QTextBrowser, QTableView
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QStandardItem, QStandardItemModel
from PySide6.QtGui import QPalette, QColor

from ui_fitsinfowidget import Ui_Form


class MyThread(QThread):
    sigLoadingOK = Signal()
    def __init__(self, table, data):
        super().__init__()
        self.table = table
        self.data = data

    def run(self):
        self.table.setData(self.data)
        self.sigLoadingOK.emit()


class TableView(QTableView):
    sigProg = Signal(int, int, str)

    def __init__(self):
        super().__init__()

    def createModel(self, row, col):
        # 创建模型
        self.model = QStandardItemModel(row, col)
        self.setModel(self.model)

    def setData(self, data):
        x = data.shape[1]  # 列
        y = data.shape[0]

        self.sigProg.emit(0, x * y, '加载数据')
        # 添加数据
        for i in range(y):
            for j in range(x):
                item = QStandardItem(f'{data[i][j]}')
                self.model.setItem(i, j, item)
            self.sigProg.emit(i * x + 1, x * y, '加载数据')

        self.sigProg.emit(x * y, x * y, '加载数据')


class FitsInfoWidget(QWidget, Ui_Form):
    def __init__(self, parent=None, statusBar=None):
        super().__init__()
        self.setupUi(self)
        self.cards = None
        self.header = None
        self.hdu = None
        self.hduList = None
        self.image = None
        self.statusBar = statusBar
        self.dataWidget = QWidget()
        self.dataWidget.setLayout(QHBoxLayout(self.dataWidget))
        self.dataWidget.setWindowTitle('fits数据显示')
        self.dataWidget.resize(500, 500)
        self.dataDisplay = TableView()
        self.dataWidget.layout().addWidget(self.dataDisplay)
        self.dataWidget.setVisible(False)
        #self.dataLoadOK = False

        self.initLabel()
        self.btn_data.setEnabled(False)

    def initLabel(self):
        # self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        # self.label.setFixedSize(100, 90)
        self.label.setFixedWidth(120)
        self.label.setToolTip('Cursor location and image value at location')
        self.label.setText('(x, y): ({}, {})\nValue: {}'.format(0, 0, 0.0))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color:red")
        # self.setStyleSheet("background-color:gold")
        palette = self.label.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('black'))
        self.label.setPalette(palette)
        self.label.setAutoFillBackground(True)

    def setImage(self, image):
        self.image = image

    def setHDU(self, hduList, hdu):
        self.hduList = hduList
        self.hdu = hdu
        self.setHeader(repr(self.hduList[hdu].header))

    def setHeader(self, header):
        self.header = header
        self.cards = self.header.split('\n')

        self.plainTextEdit.setPlainText('\n'.join(self.cards))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setFocusPolicy(Qt.NoFocus)
        self.plainTextEdit.setFont(QFont("Courier New", 10))
        self.plainTextEdit.setPlaceholderText('No results found')

        self.btn_data.clicked.connect(self.showFitsData)
        data = self.hduList[self.hdu].data
        y = data.shape[0]
        x = data.shape[1]  # 列
        self.dataDisplay.createModel(y, x)
        self.dataLoading = MyThread(self.dataDisplay, data)
        self.dataLoading.sigLoadingOK.connect(self.setDataBtnOK)
        self.dataDisplay.sigProg.connect(self.statusBar.updateInfo)
        self.dataLoading.start()

    def getFitsData(self, pos):
        if self.hduList is None or self.image is None:
            return
        array = self.hduList[self.hdu].data
        x = int(pos.x())
        y = int(pos.y())
        if x < 0 or x > self.image.shape[1] - 1 or y < 0 or y > self.image.shape[0] - 1:
            self.label.setText('(x, y): \n({}, {})\nValue: {}'.format(0, 0, 0.0))
            return
        self.label.setText('(x, y): \n({}, {})\nValue: {}'.format(x, y, array[y, x]))

    def setDataBtnOK(self):
        self.btn_data.setEnabled(True)

    def showFitsData(self):
        self.dataWidget.setVisible(True)

        #if self.dataLoadOK:
        #    self.dataWidget.setVisible(True)
        #else:
        #    self.dataDisplay.setData(self.hduList[self.hdu].data)
        #    self.dataLoadOK = True
        #    self.dataWidget.setVisible(True)



