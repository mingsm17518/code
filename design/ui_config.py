# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(440, 286)
        self.verticalLayout_14 = QVBoxLayout(Dialog)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_system = QWidget()
        self.tab_system.setObjectName(u"tab_system")
        self.verticalLayout_15 = QVBoxLayout(self.tab_system)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.tab_system)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.comboBox = QComboBox(self.tab_system)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_15.addLayout(self.horizontalLayout_2)

        self.line_3 = QFrame(self.tab_system)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_15.addWidget(self.line_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.tab_system)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.listWidget_essential_source = QListWidget(self.tab_system)
        self.listWidget_essential_source.setObjectName(u"listWidget_essential_source")

        self.horizontalLayout_26.addWidget(self.listWidget_essential_source)

        self.label_26 = QLabel(self.tab_system)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_26.addWidget(self.label_26)

        self.listWidget_essential_goal = QListWidget(self.tab_system)
        self.listWidget_essential_goal.setObjectName(u"listWidget_essential_goal")

        self.horizontalLayout_26.addWidget(self.listWidget_essential_goal)


        self.verticalLayout.addLayout(self.horizontalLayout_26)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.tab_system)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.tableWidget = QTableWidget(self.tab_system)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tableWidget.rowCount() < 1):
            self.tableWidget.setRowCount(1)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_2.addWidget(self.tableWidget)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_15.addLayout(self.horizontalLayout_4)

        self.tabWidget.addTab(self.tab_system, "")
        self.tab_sofc = QWidget()
        self.tab_sofc.setObjectName(u"tab_sofc")
        self.verticalLayout_13 = QVBoxLayout(self.tab_sofc)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 10)
        self.groupBox_5 = QGroupBox(self.tab_sofc)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_20 = QLabel(self.groupBox_5)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_24.addWidget(self.label_20)

        self.sb_bkg_box_min = QSpinBox(self.groupBox_5)
        self.sb_bkg_box_min.setObjectName(u"sb_bkg_box_min")

        self.horizontalLayout_24.addWidget(self.sb_bkg_box_min)

        self.sb_bkg_box_max = QSpinBox(self.groupBox_5)
        self.sb_bkg_box_max.setObjectName(u"sb_bkg_box_max")

        self.horizontalLayout_24.addWidget(self.sb_bkg_box_max)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_6)

        self.label_21 = QLabel(self.groupBox_5)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_24.addWidget(self.label_21)

        self.sb_seg_threshold = QDoubleSpinBox(self.groupBox_5)
        self.sb_seg_threshold.setObjectName(u"sb_seg_threshold")
        self.sb_seg_threshold.setSingleStep(0.100000000000000)

        self.horizontalLayout_24.addWidget(self.sb_seg_threshold)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_7)

        self.label_22 = QLabel(self.groupBox_5)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_24.addWidget(self.label_22)

        self.sb_seg_npixels = QSpinBox(self.groupBox_5)
        self.sb_seg_npixels.setObjectName(u"sb_seg_npixels")

        self.horizontalLayout_24.addWidget(self.sb_seg_npixels)


        self.verticalLayout_11.addLayout(self.horizontalLayout_24)


        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.tab_sofc)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.label_23 = QLabel(self.groupBox_6)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_25.addWidget(self.label_23)

        self.sb_radius = QSpinBox(self.groupBox_6)
        self.sb_radius.setObjectName(u"sb_radius")

        self.horizontalLayout_25.addWidget(self.sb_radius)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_8)

        self.label_24 = QLabel(self.groupBox_6)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_25.addWidget(self.label_24)

        self.sb_radius_in = QSpinBox(self.groupBox_6)
        self.sb_radius_in.setObjectName(u"sb_radius_in")

        self.horizontalLayout_25.addWidget(self.sb_radius_in)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_9)

        self.label_25 = QLabel(self.groupBox_6)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_25.addWidget(self.label_25)

        self.sb_radius_out = QSpinBox(self.groupBox_6)
        self.sb_radius_out.setObjectName(u"sb_radius_out")

        self.horizontalLayout_25.addWidget(self.sb_radius_out)


        self.verticalLayout_12.addLayout(self.horizontalLayout_25)


        self.verticalLayout_3.addWidget(self.groupBox_6)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)

        self.verticalLayout_13.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tab_sofc, "")
        self.tab_smod = QWidget()
        self.tab_smod.setObjectName(u"tab_smod")
        self.verticalLayout_4 = QVBoxLayout(self.tab_smod)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.tab_smod)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(60, 0))
        self.label_5.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.label_5)

        self.sb_image_num = QSpinBox(self.tab_smod)
        self.sb_image_num.setObjectName(u"sb_image_num")
        self.sb_image_num.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_5.addWidget(self.sb_image_num)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.tab_smod)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(60, 0))
        self.label_6.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_6.addWidget(self.label_6)

        self.cb_ptype = QComboBox(self.tab_smod)
        self.cb_ptype.setObjectName(u"cb_ptype")
        self.cb_ptype.setMinimumSize(QSize(60, 0))
        self.cb_ptype.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_6.addWidget(self.cb_ptype)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.tab_smod)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(60, 0))
        self.label_7.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_7.addWidget(self.label_7)

        self.sb_time_moment = QSpinBox(self.tab_smod)
        self.sb_time_moment.setObjectName(u"sb_time_moment")
        self.sb_time_moment.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_7.addWidget(self.sb_time_moment)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_18)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(self.tab_smod)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(60, 0))
        self.label_8.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_8.addWidget(self.label_8)

        self.sb_noise_length = QSpinBox(self.tab_smod)
        self.sb_noise_length.setObjectName(u"sb_noise_length")
        self.sb_noise_length.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_8.addWidget(self.sb_noise_length)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_9 = QLabel(self.tab_smod)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(60, 0))
        self.label_9.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_9.addWidget(self.label_9)

        self.sb_hough_npoints = QSpinBox(self.tab_smod)
        self.sb_hough_npoints.setObjectName(u"sb_hough_npoints")
        self.sb_hough_npoints.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_9.addWidget(self.sb_hough_npoints)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_10)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_10 = QLabel(self.tab_smod)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(60, 0))
        self.label_10.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_10.addWidget(self.label_10)

        self.sb_lines_npoints = QSpinBox(self.tab_smod)
        self.sb_lines_npoints.setObjectName(u"sb_lines_npoints")
        self.sb_lines_npoints.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_10.addWidget(self.sb_lines_npoints)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_17)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.tabWidget.addTab(self.tab_smod, "")
        self.tab_deim = QWidget()
        self.tab_deim.setObjectName(u"tab_deim")
        self.tabWidget.addTab(self.tab_deim, "")
        self.tab_aofc = QWidget()
        self.tab_aofc.setObjectName(u"tab_aofc")
        self.verticalLayout_10 = QVBoxLayout(self.tab_aofc)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_2 = QGroupBox(self.tab_aofc)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_14 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_15.addWidget(self.label_13)

        self.le_dark_path = QLineEdit(self.groupBox_2)
        self.le_dark_path.setObjectName(u"le_dark_path")

        self.horizontalLayout_15.addWidget(self.le_dark_path)

        self.btn_dark_path = QPushButton(self.groupBox_2)
        self.btn_dark_path.setObjectName(u"btn_dark_path")

        self.horizontalLayout_15.addWidget(self.btn_dark_path)


        self.verticalLayout_7.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_16.addWidget(self.label_14)

        self.le_dark_wildcard = QLineEdit(self.groupBox_2)
        self.le_dark_wildcard.setObjectName(u"le_dark_wildcard")

        self.horizontalLayout_16.addWidget(self.le_dark_wildcard)


        self.verticalLayout_7.addLayout(self.horizontalLayout_16)


        self.horizontalLayout_14.addLayout(self.verticalLayout_7)


        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.groupBox = QGroupBox(self.tab_aofc)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_13 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_11.addWidget(self.label_11)

        self.le_bias_path = QLineEdit(self.groupBox)
        self.le_bias_path.setObjectName(u"le_bias_path")

        self.horizontalLayout_11.addWidget(self.le_bias_path)

        self.btn_bias_path = QPushButton(self.groupBox)
        self.btn_bias_path.setObjectName(u"btn_bias_path")

        self.horizontalLayout_11.addWidget(self.btn_bias_path)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_12.addWidget(self.label_12)

        self.le_bias_wildcard = QLineEdit(self.groupBox)
        self.le_bias_wildcard.setObjectName(u"le_bias_wildcard")

        self.horizontalLayout_12.addWidget(self.le_bias_wildcard)


        self.verticalLayout_6.addLayout(self.horizontalLayout_12)


        self.horizontalLayout_13.addLayout(self.verticalLayout_6)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_aofc)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_17 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_18.addWidget(self.label_15)

        self.le_flat_path = QLineEdit(self.groupBox_3)
        self.le_flat_path.setObjectName(u"le_flat_path")

        self.horizontalLayout_18.addWidget(self.le_flat_path)

        self.btn_flat_path = QPushButton(self.groupBox_3)
        self.btn_flat_path.setObjectName(u"btn_flat_path")

        self.horizontalLayout_18.addWidget(self.btn_flat_path)


        self.verticalLayout_8.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_16 = QLabel(self.groupBox_3)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_19.addWidget(self.label_16)

        self.le_flat_wildcard = QLineEdit(self.groupBox_3)
        self.le_flat_wildcard.setObjectName(u"le_flat_wildcard")

        self.horizontalLayout_19.addWidget(self.le_flat_wildcard)


        self.verticalLayout_8.addLayout(self.horizontalLayout_19)


        self.horizontalLayout_17.addLayout(self.verticalLayout_8)


        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.tab_aofc)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_20 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_21.addWidget(self.label_17)

        self.le_object_path = QLineEdit(self.groupBox_4)
        self.le_object_path.setObjectName(u"le_object_path")

        self.horizontalLayout_21.addWidget(self.le_object_path)

        self.btn_object_path = QPushButton(self.groupBox_4)
        self.btn_object_path.setObjectName(u"btn_object_path")

        self.horizontalLayout_21.addWidget(self.btn_object_path)


        self.verticalLayout_9.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.label_18 = QLabel(self.groupBox_4)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_22.addWidget(self.label_18)

        self.le_object_wildcard = QLineEdit(self.groupBox_4)
        self.le_object_wildcard.setObjectName(u"le_object_wildcard")

        self.horizontalLayout_22.addWidget(self.le_object_wildcard)


        self.verticalLayout_9.addLayout(self.horizontalLayout_22)


        self.horizontalLayout_20.addLayout(self.verticalLayout_9)


        self.gridLayout.addWidget(self.groupBox_4, 1, 1, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout)

        self.tabWidget.addTab(self.tab_aofc, "")
        self.tab_tvod = QWidget()
        self.tab_tvod.setObjectName(u"tab_tvod")
        self.verticalLayout_16 = QVBoxLayout(self.tab_tvod)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.label_36 = QLabel(self.tab_tvod)
        self.label_36.setObjectName(u"label_36")

        self.horizontalLayout_32.addWidget(self.label_36)

        self.le_data_filter = QLineEdit(self.tab_tvod)
        self.le_data_filter.setObjectName(u"le_data_filter")
        self.le_data_filter.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_32.addWidget(self.le_data_filter)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_12)

        self.horizontalLayout_32.setStretch(2, 1)

        self.verticalLayout_16.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_28 = QLabel(self.tab_tvod)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_28.addWidget(self.label_28)

        self.sb_reference_num = QSpinBox(self.tab_tvod)
        self.sb_reference_num.setObjectName(u"sb_reference_num")
        self.sb_reference_num.setMinimum(3)
        self.sb_reference_num.setMaximum(999)

        self.horizontalLayout_28.addWidget(self.sb_reference_num)

        self.label_32 = QLabel(self.tab_tvod)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_28.addWidget(self.label_32)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_13)


        self.verticalLayout_16.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.label_27 = QLabel(self.tab_tvod)
        self.label_27.setObjectName(u"label_27")

        self.horizontalLayout_27.addWidget(self.label_27)

        self.sb_candiate_num = QSpinBox(self.tab_tvod)
        self.sb_candiate_num.setObjectName(u"sb_candiate_num")
        self.sb_candiate_num.setMaximumSize(QSize(45, 16777215))
        self.sb_candiate_num.setMinimum(4)
        self.sb_candiate_num.setMaximum(9999)
        self.sb_candiate_num.setValue(4)

        self.horizontalLayout_27.addWidget(self.sb_candiate_num)

        self.label_31 = QLabel(self.tab_tvod)
        self.label_31.setObjectName(u"label_31")

        self.horizontalLayout_27.addWidget(self.label_31)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_11)


        self.verticalLayout_16.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_37 = QLabel(self.tab_tvod)
        self.label_37.setObjectName(u"label_37")

        self.horizontalLayout_33.addWidget(self.label_37)

        self.dsb_ratio = QDoubleSpinBox(self.tab_tvod)
        self.dsb_ratio.setObjectName(u"dsb_ratio")
        self.dsb_ratio.setMinimum(0.200000000000000)
        self.dsb_ratio.setMaximum(0.500000000000000)
        self.dsb_ratio.setSingleStep(0.010000000000000)
        self.dsb_ratio.setValue(0.450000000000000)

        self.horizontalLayout_33.addWidget(self.dsb_ratio)

        self.label_38 = QLabel(self.tab_tvod)
        self.label_38.setObjectName(u"label_38")

        self.horizontalLayout_33.addWidget(self.label_38)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_33.addItem(self.horizontalSpacer_14)


        self.verticalLayout_16.addLayout(self.horizontalLayout_33)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label_30 = QLabel(self.tab_tvod)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_30.addWidget(self.label_30)

        self.dsb_p_num = QDoubleSpinBox(self.tab_tvod)
        self.dsb_p_num.setObjectName(u"dsb_p_num")
        self.dsb_p_num.setMaximum(100.000000000000000)
        self.dsb_p_num.setSingleStep(0.010000000000000)
        self.dsb_p_num.setValue(0.990000000000000)

        self.horizontalLayout_30.addWidget(self.dsb_p_num)

        self.label_34 = QLabel(self.tab_tvod)
        self.label_34.setObjectName(u"label_34")

        self.horizontalLayout_30.addWidget(self.label_34)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_15)


        self.verticalLayout_16.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_29 = QLabel(self.tab_tvod)
        self.label_29.setObjectName(u"label_29")

        self.horizontalLayout_29.addWidget(self.label_29)

        self.sb_min_num = QSpinBox(self.tab_tvod)
        self.sb_min_num.setObjectName(u"sb_min_num")
        self.sb_min_num.setMinimum(5)
        self.sb_min_num.setMaximum(9999)

        self.horizontalLayout_29.addWidget(self.sb_min_num)

        self.label_33 = QLabel(self.tab_tvod)
        self.label_33.setObjectName(u"label_33")

        self.horizontalLayout_29.addWidget(self.label_33)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_16)


        self.verticalLayout_16.addLayout(self.horizontalLayout_29)

        self.tabWidget.addTab(self.tab_tvod, "")

        self.verticalLayout_14.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_cancel = QPushButton(Dialog)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.horizontalLayout.addWidget(self.btn_cancel)

        self.btn_ok = QPushButton(Dialog)
        self.btn_ok.setObjectName(u"btn_ok")

        self.horizontalLayout.addWidget(self.btn_ok)

        self.btn_apply = QPushButton(Dialog)
        self.btn_apply.setObjectName(u"btn_apply")

        self.horizontalLayout.addWidget(self.btn_apply)


        self.verticalLayout_14.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u5916\u89c2\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u68c0\u6d4b\u6587\u4ef6\u5934\uff1a", None))
        self.label_26.setText(QCoreApplication.translate("Dialog", u">", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u66f4\u65b0\u6587\u4ef6\u5934\uff1a", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"\u5173\u952e\u8bcd", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"\u503c", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_system), QCoreApplication.translate("Dialog", u"system", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"\u76ee\u6807\u63d0\u53d6", None))
        self.label_20.setText(QCoreApplication.translate("Dialog", u"\u80cc\u666f\u6846\uff1a", None))
        self.label_21.setText(QCoreApplication.translate("Dialog", u"\u9608\u503c\uff1a", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"\u50cf\u7d20\u6570\uff1a", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"\u6d4b\u5149", None))
        self.label_23.setText(QCoreApplication.translate("Dialog", u"\u5b54\u5f84\uff1a", None))
        self.label_24.setText(QCoreApplication.translate("Dialog", u"\u5185\u5f84\uff1a", None))
        self.label_25.setText(QCoreApplication.translate("Dialog", u"\u5916\u5f84\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_sofc), QCoreApplication.translate("Dialog", u"sofc", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u56fe\u50cf\u6570\u91cf\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u5904\u7406\u7c7b\u578b\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"\u65f6\u523b\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u566a\u58f0\u957f\u5ea6\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"\u970d\u592b\u70b9\u6570\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"\u76f4\u7ebf\u70b9\u6570\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_smod), QCoreApplication.translate("Dialog", u"smod", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_deim), QCoreApplication.translate("Dialog", u"deim", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"\u6697\u573a", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"\u8def\u5f84\uff1a", None))
        self.btn_dark_path.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8...", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"\u6a21\u5f0f\uff1a", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u672c\u5e95", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"\u8def\u5f84\uff1a", None))
        self.btn_bias_path.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8...", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"\u6a21\u5f0f\uff1a", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"\u5e73\u573a", None))
        self.label_15.setText(QCoreApplication.translate("Dialog", u"\u8def\u5f84\uff1a", None))
        self.btn_flat_path.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8...", None))
        self.label_16.setText(QCoreApplication.translate("Dialog", u"\u6a21\u5f0f\uff1a", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"\u76ee\u6807", None))
        self.label_17.setText(QCoreApplication.translate("Dialog", u"\u8def\u5f84\uff1a", None))
        self.btn_object_path.setText(QCoreApplication.translate("Dialog", u"\u6d4f\u89c8...", None))
        self.label_18.setText(QCoreApplication.translate("Dialog", u"\u6a21\u5f0f\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_aofc), QCoreApplication.translate("Dialog", u"aofc", None))
        self.label_36.setText(QCoreApplication.translate("Dialog", u"\u6ce2\u6bb5:", None))
        self.label_28.setText(QCoreApplication.translate("Dialog", u"\u53c2\u8003\u661f\u6570\u91cf:", None))
        self.label_32.setText(QCoreApplication.translate("Dialog", u"(>=3)", None))
        self.label_27.setText(QCoreApplication.translate("Dialog", u"\u53c2\u8003\u661f\u5019\u9009\u4f53\u6570\u91cf:", None))
        self.label_31.setText(QCoreApplication.translate("Dialog", u"(>=4)", None))
        self.label_37.setText(QCoreApplication.translate("Dialog", u"\u53c2\u8003\u661f\u5019\u9009\u4f53\u533a\u57df\u8303\u56f4:", None))
        self.label_38.setText(QCoreApplication.translate("Dialog", u"(0.2~0.5)", None))
        self.label_30.setText(QCoreApplication.translate("Dialog", u"\u68c0\u6d4b\u6982\u7387\u8bbe\u7f6e:", None))
        self.label_34.setText(QCoreApplication.translate("Dialog", u"(\u5efa\u8bae99%)", None))
        self.label_29.setText(QCoreApplication.translate("Dialog", u"\u5224\u65ad\u662f\u5426\u662f\u53d8\u6e90\u7684\u6700\u5c0f\u6709\u6548\u6570\u636e\u91cf:", None))
        self.label_33.setText(QCoreApplication.translate("Dialog", u"(>=5)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_tvod), QCoreApplication.translate("Dialog", u"tvod", None))
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
        self.btn_ok.setText(QCoreApplication.translate("Dialog", u"\u786e\u5b9a", None))
        self.btn_apply.setText(QCoreApplication.translate("Dialog", u"\u5e94\u7528", None))
    # retranslateUi

