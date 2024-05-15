import pathlib
import configparser
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileDialog, QApplication
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from .ui_setwidget import Ui_Form
# from controlWidget import ControlWidget
from systemwidget import SystemWidget, SystemRunThread


class setWidget(SystemWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 从文件中加载UI定义
        # qfile_stats = QFile("design/setWidget.ui")
        #
        # # qfile_stats.open(QFile.ReadOnly)
        # # Todo (qfile_stats.open(QFile.ReadOnly)) =>
        # if qfile_stats.open(QFile.ReadOnly):
        #     loader = QUiLoader()
        #     self.ui = loader.load(qfile_stats)
        #     qfile_stats.close()
        # else:
        #     pass

        # qfile_stats.close()  # 这里为什么要 close掉，我很好奇
        # 从UI定义中动态创建一个相应的窗口对象
        # #注意:里面的控件对象也成为窗口对象的属性了
        # #比如 self.ui.button , self.ui.textEditself.ui = QUiLoader() . load(qfile_stats)


# 调试用的 （不用注释）
# if __name__ == "__main__":
#     app = QApplication([])
#     window = setWidget()
#     window.show()
#     sys.exit(app.exec())
