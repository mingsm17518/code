from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QPixmap

from ui_messagewidget import Ui_Dialog


class MessageWidget(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('错误提醒')
        pixmap = QPixmap("./resources/错误.png")
        self.label.setPixmap(pixmap)

        self.textBrowser.setVisible(False)

        self.btn_ok.clicked.connect(self.quit)
        self.btn_detail.clicked.connect(self.detail)

    def quit(self):
        if self.textBrowser.isVisible():
            self.textBrowser.setVisible(False)
        self.setVisible(False)

    def detail(self):
        self.textBrowser.setVisible(False if self.textBrowser.isVisible() else True)

    def setErrorMsg(self, error_msg, error_traceback_msg):
        self.lb_msg.setText(error_msg)
        self.textBrowser.clear()
        self.textBrowser.append(error_traceback_msg)
