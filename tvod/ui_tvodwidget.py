# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tvodwidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(220, 518)
        self.verticalLayout_8 = QVBoxLayout(Form)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.lb_config = QLabel(Form)
        self.lb_config.setObjectName(u"lb_config")

        self.horizontalLayout_10.addWidget(self.lb_config)

        self.cbb_config = QComboBox(Form)
        self.cbb_config.setObjectName(u"cbb_config")

        self.horizontalLayout_10.addWidget(self.cbb_config)

        self.btn_save_config = QPushButton(Form)
        self.btn_save_config.setObjectName(u"btn_save_config")
        self.btn_save_config.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_10.addWidget(self.btn_save_config)

        self.btn_detail = QPushButton(Form)
        self.btn_detail.setObjectName(u"btn_detail")
        self.btn_detail.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_10.addWidget(self.btn_detail)

        self.horizontalLayout_10.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.le_cat2 = QLineEdit(Form)
        self.le_cat2.setObjectName(u"le_cat2")

        self.horizontalLayout.addWidget(self.le_cat2)

        self.btn_cat2 = QPushButton(Form)
        self.btn_cat2.setObjectName(u"btn_cat2")
        self.btn_cat2.setMaximumSize(QSize(30, 16777215))
        self.btn_cat2.setSizeIncrement(QSize(10, 10))

        self.horizontalLayout.addWidget(self.btn_cat2)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.le_candidate = QLineEdit(Form)
        self.le_candidate.setObjectName(u"le_candidate")

        self.horizontalLayout_2.addWidget(self.le_candidate)

        self.btn_candidate = QPushButton(Form)
        self.btn_candidate.setObjectName(u"btn_candidate")
        self.btn_candidate.setMaximumSize(QSize(30, 16777215))
        self.btn_candidate.setSizeIncrement(QSize(10, 10))

        self.horizontalLayout_2.addWidget(self.btn_candidate)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_5.addWidget(self.label_5)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.le_reference = QLineEdit(Form)
        self.le_reference.setObjectName(u"le_reference")

        self.horizontalLayout_5.addWidget(self.le_reference)

        self.btn_reference = QPushButton(Form)
        self.btn_reference.setObjectName(u"btn_reference")
        self.btn_reference.setMaximumSize(QSize(30, 16777215))
        self.btn_reference.setSizeIncrement(QSize(10, 10))

        self.horizontalLayout_5.addWidget(self.btn_reference)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_6.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.le_combine = QLineEdit(Form)
        self.le_combine.setObjectName(u"le_combine")

        self.horizontalLayout_3.addWidget(self.le_combine)

        self.btn_combine = QPushButton(Form)
        self.btn_combine.setObjectName(u"btn_combine")
        self.btn_combine.setMaximumSize(QSize(30, 16777215))
        self.btn_combine.setSizeIncrement(QSize(10, 10))

        self.horizontalLayout_3.addWidget(self.btn_combine)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_7.addWidget(self.label_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.le_save = QLineEdit(Form)
        self.le_save.setObjectName(u"le_save")

        self.horizontalLayout_6.addWidget(self.le_save)

        self.btn_save_file = QPushButton(Form)
        self.btn_save_file.setObjectName(u"btn_save_file")
        self.btn_save_file.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_6.addWidget(self.btn_save_file)

        self.horizontalLayout_6.setStretch(0, 1)

        self.verticalLayout_7.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addLayout(self.verticalLayout_7)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.cb_1 = QCheckBox(Form)
        self.cb_1.setObjectName(u"cb_1")

        self.verticalLayout_4.addWidget(self.cb_1)

        self.cb_2 = QCheckBox(Form)
        self.cb_2.setObjectName(u"cb_2")

        self.verticalLayout_4.addWidget(self.cb_2)

        self.cb_3 = QCheckBox(Form)
        self.cb_3.setObjectName(u"cb_3")

        self.verticalLayout_4.addWidget(self.cb_3)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cb_all = QCheckBox(Form)
        self.cb_all.setObjectName(u"cb_all")

        self.horizontalLayout_4.addWidget(self.cb_all)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.btn_run = QPushButton(Form)
        self.btn_run.setObjectName(u"btn_run")

        self.horizontalLayout_11.addWidget(self.btn_run)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)


        self.verticalLayout_8.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lb_config.setText(QCoreApplication.translate("Form", u"\u914d\u7f6e\u540d\u79f0:", None))
        self.btn_save_config.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.btn_detail.setText(QCoreApplication.translate("Form", u">", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u89c2\u6d4b\u6570\u636e:", None))
        self.btn_cat2.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5019\u9009\u661f\u4fdd\u5b58\u8def\u5f84\uff1a", None))
        self.btn_candidate.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u53c2\u8003\u661f\u6587\u4ef6:", None))
        self.btn_reference.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u661f\u7b49\u6570\u636e\u4fdd\u5b58\u8def\u5f84:", None))
        self.btn_combine.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u53d8\u6e90\u4fdd\u5b58\u8def\u5f84:", None))
        self.btn_save_file.setText(QCoreApplication.translate("Form", u"...", None))
        self.cb_1.setText(QCoreApplication.translate("Form", u"\u56fe\u50cf\u9884\u5904\u7406\u548c\u6d4b\u5149", None))
        self.cb_2.setText(QCoreApplication.translate("Form", u"\u7b5b\u9009\u53c2\u8003\u661f", None))
        self.cb_3.setText(QCoreApplication.translate("Form", u"\u53d8\u6e90\u68c0\u6d4b", None))
        self.cb_all.setText(QCoreApplication.translate("Form", u"\u5168\u9009", None))
        self.btn_run.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8f93\u51fa\u4fe1\u606f:", None))
    # retranslateUi

