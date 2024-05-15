from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction


class ToolBar(QToolBar):

    def __init__(self, master):
        super().__init__()

        self.master = master

        self.c1 = QAction('操作1')
        # self.c1.triggered.connect(self.master.test1)
        self.addAction(self.c1)

        self.c2 = QAction('操作2')
        # self.c2.triggered.connect(self.master.test2)
        self.addAction(self.c2)

        self.c3 = QAction('操作3')
        # self.c3.triggered.connect(self.master.test3)
        self.addAction(self.c3)
