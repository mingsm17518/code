from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class Cat2Widget(QWidget):
    def __init__(self, parent=None, table=None):
        super().__init__(parent)

        self.infoWidget = None

        self.setLayout(QVBoxLayout(self))
        self.plainTextEdit = QPlainTextEdit(parent=self)

        cards = repr(table.header).split('\n')
        self.plainTextEdit.setPlainText('\n'.join(cards))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setFocusPolicy(Qt.NoFocus)
        self.plainTextEdit.setFont(QFont("Courier New", 10))

        self.plainTextEdit.appendPlainText('')

        data = table.data
        index = data.columns.names.index('exptime')
        exptime = f'exptime'.ljust(7) + f' = {data[0][index]}'
        file = f'file'.ljust(7) + f' = {data[0][index + 1]}'
        JD = f'JD'.ljust(7) + f' = {data[0][index + 2]}'
        filter = f'filter'.ljust(7) + f' = {data[0][index + 3]}'

        self.plainTextEdit.appendPlainText(exptime + '\n' + file + '\n' + JD + '\n' + filter)

        # 计算每列的最大宽度
        widths = [max(len(str(x)) for x in col) for col in zip(*data)]

        widths = [max(widths[i], len(str(data.columns.names[i]))) for i in range(len(widths))]

        self.plainTextEdit.appendPlainText(' '.join([str(x).ljust(widths[i])
                                                     for i, x in enumerate(data.columns.names)
                                                     if i < index or i > index + 3]))

        for row in table.data:
            self.plainTextEdit.appendPlainText(' '.join([str(x).ljust(widths[i])
                                                         for i, x in enumerate(row)
                                                         if i < index or i > index + 3]))

        self.layout().addWidget(self.plainTextEdit)

