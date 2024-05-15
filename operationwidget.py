from PySide6.QtWidgets import QWidget
from ui_operationwidget import Ui_OperationWidget


class OperationWidget(QWidget, Ui_OperationWidget):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
