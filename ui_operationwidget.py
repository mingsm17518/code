# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'operationwidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_OperationWidget(object):
    def setupUi(self, OperationWidget):
        if not OperationWidget.objectName():
            OperationWidget.setObjectName(u"OperationWidget")
        OperationWidget.resize(262, 104)
        self.verticalLayout = QVBoxLayout(OperationWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(OperationWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.btnGetConfig = QPushButton(OperationWidget)
        self.btnGetConfig.setObjectName(u"btnGetConfig")

        self.gridLayout.addWidget(self.btnGetConfig, 1, 0, 1, 1)

        self.btnOrient = QPushButton(OperationWidget)
        self.btnOrient.setObjectName(u"btnOrient")

        self.gridLayout.addWidget(self.btnOrient, 1, 2, 1, 1)

        self.btnExtractStar = QPushButton(OperationWidget)
        self.btnExtractStar.setObjectName(u"btnExtractStar")

        self.gridLayout.addWidget(self.btnExtractStar, 0, 2, 1, 1)

        self.btnCorrectMerge = QPushButton(OperationWidget)
        self.btnCorrectMerge.setObjectName(u"btnCorrectMerge")

        self.gridLayout.addWidget(self.btnCorrectMerge, 1, 1, 1, 1)

        self.btnUpdateHeader = QPushButton(OperationWidget)
        self.btnUpdateHeader.setObjectName(u"btnUpdateHeader")

        self.gridLayout.addWidget(self.btnUpdateHeader, 0, 1, 1, 1)

        self.btnCorrectImage = QPushButton(OperationWidget)
        self.btnCorrectImage.setObjectName(u"btnCorrectImage")

        self.gridLayout.addWidget(self.btnCorrectImage, 2, 1, 1, 1)

        self.btnCalibrate = QPushButton(OperationWidget)
        self.btnCalibrate.setObjectName(u"btnCalibrate")

        self.gridLayout.addWidget(self.btnCalibrate, 2, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(OperationWidget)

        QMetaObject.connectSlotsByName(OperationWidget)
    # setupUi

    def retranslateUi(self, OperationWidget):
        OperationWidget.setWindowTitle(QCoreApplication.translate("OperationWidget", u"OperationWidget", None))
        self.label.setText(QCoreApplication.translate("OperationWidget", u"\u64cd\u4f5c\u83dc\u5355", None))
        self.btnGetConfig.setText(QCoreApplication.translate("OperationWidget", u"\u63d0\u53d6\u914d\u7f6e", None))
        self.btnOrient.setText(QCoreApplication.translate("OperationWidget", u"\u5929\u6587\u5b9a\u4f4d", None))
        self.btnExtractStar.setText(QCoreApplication.translate("OperationWidget", u"\u661f\u50cf\u63d0\u53d6", None))
        self.btnCorrectMerge.setText(QCoreApplication.translate("OperationWidget", u"\u6821\u6b63\u56fe\u50cf\u5408\u5e76", None))
        self.btnUpdateHeader.setText(QCoreApplication.translate("OperationWidget", u"\u66f4\u65b0\u6587\u4ef6\u5934", None))
        self.btnCorrectImage.setText(QCoreApplication.translate("OperationWidget", u"\u56fe\u50cf\u6539\u6b63", None))
        self.btnCalibrate.setText(QCoreApplication.translate("OperationWidget", u"\u6d41\u91cf\u5b9a\u6807", None))
    # retranslateUi

