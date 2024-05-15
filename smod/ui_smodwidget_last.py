# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_smodwidget.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(213, 236)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cbb_config = QComboBox(Form)
        self.cbb_config.setObjectName(u"cbb_config")

        self.horizontalLayout.addWidget(self.cbb_config)

        self.btn_save = QPushButton(Form)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setMaximumSize(QSize(60, 25))

        self.horizontalLayout.addWidget(self.btn_save)

        self.horizontalLayout.setStretch(0, 1)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.sb_houghPoints = QSpinBox(Form)
        self.sb_houghPoints.setObjectName(u"sb_houghPoints")
        self.sb_houghPoints.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout.addWidget(self.sb_houghPoints, 5, 1, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.cbb_ptype = QComboBox(Form)
        self.cbb_ptype.setObjectName(u"cbb_ptype")

        self.gridLayout.addWidget(self.cbb_ptype, 2, 1, 1, 1)

        self.sb_imageNum = QSpinBox(Form)
        self.sb_imageNum.setObjectName(u"sb_imageNum")
        self.sb_imageNum.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout.addWidget(self.sb_imageNum, 1, 1, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.sb_noiseLength = QSpinBox(Form)
        self.sb_noiseLength.setObjectName(u"sb_noiseLength")
        self.sb_noiseLength.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout.addWidget(self.sb_noiseLength, 4, 1, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.sb_timeMoment = QSpinBox(Form)
        self.sb_timeMoment.setObjectName(u"sb_timeMoment")
        self.sb_timeMoment.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout.addWidget(self.sb_timeMoment, 3, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)

        self.sb_linePoints = QSpinBox(Form)
        self.sb_linePoints.setObjectName(u"sb_linePoints")
        self.sb_linePoints.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.gridLayout.addWidget(self.sb_linePoints, 6, 1, 1, 1)

        self.btn_run = QPushButton(Form)
        self.btn_run.setObjectName(u"btn_run")

        self.gridLayout.addWidget(self.btn_run, 7, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u56fe\u50cf\u6570\u91cf:", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u914d\u7f6e\u540d\u79f0:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u65f6      \u523b:", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u970d\u592b\u70b9\u6570:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5904\u7406\u7c7b\u578b:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u566a\u58f0\u957f\u5ea6:", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u76f4\u7ebf\u70b9\u6570:", None))
        self.btn_run.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
    # retranslateUi

