# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'smodwidget.ui'
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
        Form.resize(207, 519)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, -1, 0)
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

        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.le_dir = QLineEdit(Form)
        self.le_dir.setObjectName(u"le_dir")

        self.horizontalLayout.addWidget(self.le_dir)

        self.btn_dir = QPushButton(Form)
        self.btn_dir.setObjectName(u"btn_dir")
        self.btn_dir.setMaximumSize(QSize(30, 16777215))
        self.btn_dir.setSizeIncrement(QSize(10, 10))

        self.horizontalLayout.addWidget(self.btn_dir)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.cb_1 = QCheckBox(Form)
        self.cb_1.setObjectName(u"cb_1")

        self.verticalLayout_5.addWidget(self.cb_1)

        self.cb_2 = QCheckBox(Form)
        self.cb_2.setObjectName(u"cb_2")

        self.verticalLayout_5.addWidget(self.cb_2)

        self.cb_3 = QCheckBox(Form)
        self.cb_3.setObjectName(u"cb_3")

        self.verticalLayout_5.addWidget(self.cb_3)

        self.cb_4 = QCheckBox(Form)
        self.cb_4.setObjectName(u"cb_4")

        self.verticalLayout_5.addWidget(self.cb_4)

        self.cb_5 = QCheckBox(Form)
        self.cb_5.setObjectName(u"cb_5")

        self.verticalLayout_5.addWidget(self.cb_5)

        self.cb_6 = QCheckBox(Form)
        self.cb_6.setObjectName(u"cb_6")

        self.verticalLayout_5.addWidget(self.cb_6)

        self.cb_7 = QCheckBox(Form)
        self.cb_7.setObjectName(u"cb_7")

        self.verticalLayout_5.addWidget(self.cb_7)

        self.cb_8 = QCheckBox(Form)
        self.cb_8.setObjectName(u"cb_8")

        self.verticalLayout_5.addWidget(self.cb_8)

        self.cb_9 = QCheckBox(Form)
        self.cb_9.setObjectName(u"cb_9")

        self.verticalLayout_5.addWidget(self.cb_9)

        self.cb_all = QCheckBox(Form)
        self.cb_all.setObjectName(u"cb_all")

        self.verticalLayout_5.addWidget(self.cb_all)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.le_save = QLineEdit(Form)
        self.le_save.setObjectName(u"le_save")

        self.horizontalLayout_3.addWidget(self.le_save)

        self.btn_save_file = QPushButton(Form)
        self.btn_save_file.setObjectName(u"btn_save_file")
        self.btn_save_file.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_3.addWidget(self.btn_save_file)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cb_save_cloud = QCheckBox(Form)
        self.cb_save_cloud.setObjectName(u"cb_save_cloud")

        self.horizontalLayout_2.addWidget(self.cb_save_cloud)

        self.le_cloud = QLineEdit(Form)
        self.le_cloud.setObjectName(u"le_cloud")

        self.horizontalLayout_2.addWidget(self.le_cloud)

        self.btn_cloud = QPushButton(Form)
        self.btn_cloud.setObjectName(u"btn_cloud")
        self.btn_cloud.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_2.addWidget(self.btn_cloud)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.btn_run = QPushButton(Form)
        self.btn_run.setObjectName(u"btn_run")

        self.horizontalLayout_11.addWidget(self.btn_run)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_4.addWidget(self.textBrowser)


        self.verticalLayout.addLayout(self.verticalLayout_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lb_config.setText(QCoreApplication.translate("Form", u"\u914d\u7f6e\u540d\u79f0:", None))
        self.btn_save_config.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58", None))
        self.btn_detail.setText(QCoreApplication.translate("Form", u">", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u8f93\u5165\u8def\u5f84:", None))
        self.btn_dir.setText(QCoreApplication.translate("Form", u"...", None))
        self.cb_1.setText(QCoreApplication.translate("Form", u"\u56fe\u50cf\u5408\u5e76", None))
        self.cb_2.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0\u6587\u4ef6\u5934", None))
        self.cb_3.setText(QCoreApplication.translate("Form", u"\u56fe\u50cf\u6539\u6b63", None))
        self.cb_4.setText(QCoreApplication.translate("Form", u"\u661f\u50cf\u63d0\u53d6", None))
        self.cb_5.setText(QCoreApplication.translate("Form", u"\u5929\u6587\u5b9a\u4f4d", None))
        self.cb_6.setText(QCoreApplication.translate("Form", u"\u6d41\u91cf\u5b9a\u6807", None))
        self.cb_7.setText(QCoreApplication.translate("Form", u"\u6784\u5efa\u70b9\u4e91", None))
        self.cb_8.setText(QCoreApplication.translate("Form", u"\u970d\u592b\u53d8\u6362", None))
        self.cb_9.setText(QCoreApplication.translate("Form", u"\u51b3\u7b56\u8f93\u51fa", None))
        self.cb_all.setText(QCoreApplication.translate("Form", u"\u5168\u9009", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u8def\u5f84:", None))
        self.btn_save_file.setText(QCoreApplication.translate("Form", u"...", None))
        self.cb_save_cloud.setText(QCoreApplication.translate("Form", u"\u70b9\u4e91\u8def\u5f84:", None))
        self.btn_cloud.setText(QCoreApplication.translate("Form", u"...", None))
        self.btn_run.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8f93\u51fa\u4fe1\u606f:", None))
    # retranslateUi

