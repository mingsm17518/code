from PySide6.QtWidgets import QWidget,  QVBoxLayout, QPlainTextEdit


class TxTWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 每一个展示面板都需要附带一个信息区 没有为None
        self.infoWidget = None

        self.setLayout(QVBoxLayout(self))

        self.textEdit = QPlainTextEdit()
        self.layout().addWidget(self.textEdit)

    def loadTxTFile(self, path):
        if path:
            with open(path, 'r') as f:
                content = f.read()
            self.textEdit.setPlainText(content)
            f.close()

