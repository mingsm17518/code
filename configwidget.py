import pathlib
import configparser
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QTableWidgetItem,
                               QMenu, QMessageBox)
from PySide6.QtCore import QDir, Qt
from PySide6.QtGui import QAction
from ast import literal_eval

from ui_config import Ui_Dialog


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = ""
        self.setWindowTitle('方案保存')
        layout = QVBoxLayout()
        label = QLabel("配置名称:")
        self.line_edit = QLineEdit()
        button = QPushButton("确定")
        button.clicked.connect(self.closeDialog)

        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.addWidget(button)
        self.setLayout(layout)

    def closeDialog(self):
        self.value = self.line_edit.text()
        self.accept()


class ConfigDlg(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle('设置面板')
        self.btn_apply.setVisible(False)

        self.btn_ok.clicked.connect(self.save)
        self.btn_apply.clicked.connect(self.apply)
        self.btn_cancel.clicked.connect(self.reject)

        self.tableWidget.clear()
        self.listWidget_essential_source.clear()
        self.items_goal = []
        self.update_keyword_dict = {}

        # common
        self.config_common = configparser.ConfigParser()
        self.getCommonConfig()

        # keyword
        self.items_source = ["RA", "DEC", "EPOCH", "OBSTIME", "EXPTIME", "FILTER", "SCALE", "CCDTYPE", "TRACK", "GAIN", "RDNOISE"]
        for s in self.items_goal:
            if s in self.items_source:
                self.items_source.remove(s)

        self.listWidget_essential_source.addItems(self.items_source)
        self.listWidget_essential_source.itemDoubleClicked.connect(self.addItemToGoal)
        self.listWidget_essential_goal.itemDoubleClicked.connect(self.removeItemFromGoal)

        # update keyword table
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.showTableMenu)
        self.tableWidget.setHorizontalHeaderLabels(['关键字', '值'])

        self.cb_ptype.addItems(['ALL', 'STREAK', 'POINT'])

        self.btn_bias_path.clicked.connect(self.getBiasDir)
        self.btn_flat_path.clicked.connect(self.getFlatDir)
        self.btn_dark_path.clicked.connect(self.getDarkDir)
        self.btn_object_path.clicked.connect(self.getObjectDir)

    def showTableMenu(self, pos):
        selectedItems = self.tableWidget.selectionModel().selectedIndexes()

        menu = QMenu()
        item1 = menu.addAction('新增')
        item2 = menu.addAction('删除')

        action = menu.exec(self.tableWidget.mapToGlobal(pos))

        if action == item1:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        else:
            if len(selectedItems) > 0:
                rowNum = selectedItems[-1].row()
                self.tableWidget.removeRow(rowNum)

    def addItemToGoal(self):
        item = self.listWidget_essential_source.selectedItems()[0].text()
        self.items_source.remove(item)
        self.listWidget_essential_source.clear()
        self.listWidget_essential_source.addItems(self.items_source)

        self.items_goal.append(item)
        self.listWidget_essential_goal.clear()
        self.listWidget_essential_goal.addItems(self.items_goal)

    def removeItemFromGoal(self):
        item = self.listWidget_essential_goal.selectedItems()[0].text()
        self.items_goal.remove(item)
        self.listWidget_essential_goal.clear()
        self.listWidget_essential_goal.addItems(self.items_goal)

        self.items_source.append(item)
        self.listWidget_essential_source.clear()
        self.listWidget_essential_source.addItems(self.items_source)

    def getBiasDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        if dirPath:
            self.le_bias_path.clear()
            self.le_bias_path.setText(dirPath + '/')

    def getDarkDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        if dirPath:
            self.le_dark_path.clear()
            self.le_dark_path.setText(dirPath + '/')

    def getFlatDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        if dirPath:
            self.le_flat_path.clear()
            self.le_flat_path.setText(dirPath + '/')

    def getObjectDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        if dirPath:
            self.le_object_path.clear()
            self.le_object_path.setText(dirPath + '/')

    def saveAllConfig(self):
        # system页面 - 文件头
        self.items_goal.clear()

        for i in range(self.listWidget_essential_goal.count()):
            self.items_goal.append(self.listWidget_essential_goal.item(i).text())

        self.update_keyword_dict.clear()
        for row in range(self.tableWidget.rowCount()):
            key = self.tableWidget.item(row, 0).text()
            value = self.tableWidget.item(row, 1).text()
            if value.count('.') == 1:
                value = float(value)
            elif value.isdigit():
                value = int(value)
            self.update_keyword_dict[key] = value

        self.config_common.set('UpdateHeader', 'essential_keywords', str(self.items_goal))
        self.config_common.set('UpdateHeader', 'update_keywords', str(self.update_keyword_dict))

        # aofc
        bias_path, bias_wildcard, dark_path, dark_wildcard, flat_path, flat_wildcard, object_path, object_wildcard = self.getAofcParameter()
        self.config_common.set('Preprocess', 'bias_path', bias_path)
        self.config_common.set('Preprocess', 'bias_wildcard', bias_wildcard)
        self.config_common.set('Preprocess', 'dark_path', dark_path)
        self.config_common.set('Preprocess', 'dark_wildcard', dark_wildcard)
        self.config_common.set('Preprocess', 'flat_path', flat_path)
        self.config_common.set('Preprocess', 'flat_wildcard', flat_wildcard)
        self.config_common.set('Preprocess', 'object_path', object_path)
        self.config_common.set('Preprocess', 'object_wildcard', object_wildcard)

        # sofc
        bkg_box_size, seg_threshold, seg_npixels, radius, radius_in, radius_out = self.getSofcParameter()
        self.config_common.set('ExtractSource', 'bkg_box_size', bkg_box_size)
        self.config_common.set('ExtractSource', 'seg_threshold', seg_threshold)
        self.config_common.set('ExtractSource', 'seg_npixels', seg_npixels)
        self.config_common.set('AperTarget', 'radius', radius)
        self.config_common.set('AperTarget', 'radius_in', radius_in)
        self.config_common.set('AperTarget', 'radius_out', radius_out)

        # smod
        image_number, ptype, time_moment, noise_length, hough_npoints, lines_npoints = self.getSmodParameter()
        self.config_common.set('IdentifyTarget', 'image_number', image_number)
        self.config_common.set('IdentifyTarget', 'ptype', ptype)
        self.config_common.set('IdentifyTarget', 'time_moment', time_moment)
        self.config_common.set('IdentifyTarget', 'noise_length', noise_length)
        self.config_common.set('IdentifyTarget', 'hough_npoints', hough_npoints)
        self.config_common.set('IdentifyTarget', 'lines_npoints', lines_npoints)

        #tvod
        candidate_star_num, reference_star_num, p, min_num, ratio, data_filter = self.getTvodParameter()
        self.config_common.set('Tvod', 'candidate_star_num', candidate_star_num)
        self.config_common.set('Tvod', 'reference_star_num', reference_star_num)
        self.config_common.set('Tvod', 'p', p)
        self.config_common.set('Tvod', 'min_num', min_num)
        self.config_common.set('Tvod', 'ratio', ratio)
        self.config_common.set('Tvod', 'data_filter', data_filter)

        with open("./memory/common.ini", 'w', encoding='utf-8') as f:
            self.config_common.write(f)
        f.close()

    def getCommonConfig(self):
        self.config_common.clear()
        self.config_common.read(pathlib.Path('./memory/common.ini'))

        # 参数读取
        # [Default]
        process = self.config_common.get('Default', 'process')

        # [Preprocess]
        bias_path = self.config_common.get('Preprocess', 'bias_path')
        bias_wildcard = self.config_common.get('Preprocess', 'bias_wildcard')
        dark_path = self.config_common.get('Preprocess', 'dark_path')
        dark_wildcard = self.config_common.get('Preprocess', 'dark_wildcard')
        flat_path = self.config_common.get('Preprocess', 'flat_path')
        flat_wildcard = self.config_common.get('Preprocess', 'flat_wildcard')
        object_path = self.config_common.get('Preprocess', 'object_path')
        object_wildcard = self.config_common.get('Preprocess', 'object_wildcard')

        # [UpdateHeader]
        essential_keywords = self.config_common.get('UpdateHeader', 'essential_keywords')
        update_keywords = self.config_common.get('UpdateHeader', 'update_keywords')

        self.items_goal = literal_eval(essential_keywords)
        self.listWidget_essential_goal.clear()
        self.listWidget_essential_goal.addItems(self.items_goal)

        # 字符串转换成列表和字典
        self.update_keyword_dict = literal_eval(update_keywords)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(self.update_keyword_dict))
        # 设置表格数据
        row_index = 0
        for key, value in self.update_keyword_dict.items():
            self.tableWidget.setItem(row_index, 0, QTableWidgetItem(key))
            self.tableWidget.setItem(row_index, 1, QTableWidgetItem(str(value)))
            row_index += 1

        # [ExtractSource]
        bkg_box_size = self.config_common.get('ExtractSource', 'bkg_box_size')
        seg_threshold = self.config_common.get('ExtractSource', 'seg_threshold')
        seg_npixels = self.config_common.get('ExtractSource', 'seg_npixels')

        # [AperTarget]
        radius = self.config_common.get('AperTarget', 'radius')
        radius_in = self.config_common.get('AperTarget', 'radius_in')
        radius_out = self.config_common.get('AperTarget', 'radius_out')

        # [IdentifyTarget]
        image_number = self.config_common.get('IdentifyTarget', 'image_number')
        ptype = self.config_common.get('IdentifyTarget', 'ptype')
        time_moment = self.config_common.get('IdentifyTarget', 'time_moment')
        noise_length = self.config_common.get('IdentifyTarget', 'noise_length')
        hough_npoints = self.config_common.get('IdentifyTarget', 'hough_npoints')
        lines_npoints = self.config_common.get('IdentifyTarget', 'lines_npoints')

        # [TvodParameter]
        candidate_star_num = self.config_common.get('Tvod', 'candidate_star_num')
        reference_star_num = self.config_common.get('Tvod', 'reference_star_num')
        p = self.config_common.get('Tvod', 'p')
        min_num = self.config_common.get('Tvod', 'min_num')
        ratio = self.config_common.get('Tvod', 'ratio')
        data_filter = self.config_common.get('Tvod', 'data_filter')

        # 填入页面
        # sofc
        size = bkg_box_size.replace('(', '').replace(')', ' ').split(',')
        self.sb_bkg_box_min.setValue(int(size[0]))
        self.sb_bkg_box_max.setValue(int(size[1]))

        self.sb_seg_threshold.setValue(float(seg_threshold))

        self.sb_seg_npixels.setValue(int(seg_npixels))

        self.sb_radius.setValue(int(radius))
        self.sb_radius_in.setValue(int(radius_in))
        self.sb_radius_out.setValue(int(radius_out))

        # smod
        self.sb_image_num.setValue(int(image_number))
        self.sb_time_moment.setValue(int(time_moment))
        self.sb_noise_length.setValue(int(noise_length))
        self.sb_hough_npoints.setValue(int(hough_npoints))
        self.sb_lines_npoints.setValue(int(lines_npoints))

        # deim

        # aofc
        self.le_bias_path.setText(bias_path)
        self.le_bias_wildcard.setText(bias_wildcard)
        self.le_dark_path.setText(dark_path)
        self.le_dark_wildcard.setText(dark_wildcard)
        self.le_flat_path.setText(flat_path)
        self.le_flat_wildcard.setText(flat_wildcard)
        self.le_object_path.setText(object_path)
        self.le_object_wildcard.setText(object_wildcard)

        # tvod
        self.sb_min_num.setValue(int(min_num))
        self.sb_candiate_num.setValue(int(candidate_star_num))
        self.sb_reference_num.setValue(int(reference_star_num))
        self.dsb_p_num.setValue(float(p))
        self.cb_ptype.setCurrentText(ptype)
        # self.le_ptype.setText(ptype)
        self.dsb_ratio.setValue(float(ratio))
        self.le_data_filter.setText(data_filter)

    def getAofcParameter(self):
        bias_path = self.le_bias_path.text()
        bias_wildcard = self.le_bias_wildcard.text()
        dark_path = self.le_dark_path.text()
        dark_wildcard = self.le_dark_wildcard.text()
        flat_path = self.le_flat_path.text()
        flat_wildcard = self.le_flat_wildcard.text()
        object_path = self.le_object_path.text()
        object_wildcard = self.le_object_wildcard.text()
        return bias_path, bias_wildcard, dark_path, dark_wildcard, flat_path, flat_wildcard, object_path, object_wildcard

    def getSofcParameter(self):
        bkg_box_size = '(' + str(self.sb_bkg_box_min.value()) + ',' + str(self.sb_bkg_box_max.value()) + ')'
        seg_threshold = str(self.sb_seg_threshold.value())
        seg_npixels = str(self.sb_seg_npixels.value())

        radius = str(self.sb_radius.value())
        radius_in = str(self.sb_radius_in.value())
        radius_out = str(self.sb_radius_out.value())
        return bkg_box_size, seg_threshold, seg_npixels, radius, radius_in, radius_out

    def getTvodParameter(self):
        candidate_num = str(self.sb_candiate_num.value())
        reference_num = str(self.sb_reference_num.value())
        p = str(self.dsb_p_num.value())
        min_num = str(self.sb_min_num.value())
        ratio = str(self.dsb_ratio.value())
        data_filter = self.le_data_filter.text()
        return candidate_num, reference_num, p, min_num, ratio, data_filter

    def getSmodParameter(self):
        image_number = str(self.sb_image_num.value())
        ptype = self.cb_ptype.currentText()
        time_moment = str(self.sb_time_moment.value())
        noise_length = str(self.sb_noise_length.value())
        hough_npoints = str(self.sb_hough_npoints.value())
        lines_npoints = str(self.sb_lines_npoints.value())
        return image_number, ptype, time_moment, noise_length, hough_npoints, lines_npoints

    def save(self):
        self.saveAllConfig()
        self.accept()

    def apply(self):
        self.saveAllConfig()

