import configparser
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (QWidget, QFileDialog, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit,
                               QHeaderView, QTableWidgetItem, QMenu)
from ast import literal_eval

from ui_inieditwidget import Ui_Form


class MyDialog(QDialog):

    def __init__(self, parent=None, title=None, label_name=None):
        super().__init__(parent)
        self.value = ""
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        label = QLabel(label_name)
        self.line_edit = QLineEdit()
        button = QPushButton("确定")
        button.clicked.connect(self.closeDialog)

        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.addWidget(button)
        self.setLayout(layout)
        self.setMinimumWidth(300)

    def closeDialog(self):
        self.value = self.line_edit.text()
        self.accept()


class InIEditWidget(QWidget, Ui_Form):
    sigSaveOK = Signal(str)

    def checkDirPath(self):
        le = self.sender()
        path = le.text()
        if path[-1] != '/':
            le.setText(path + '/')

    def __init__(self, title=None, config_path=None):
        super().__init__()
        self.setupUi(self)
        self.resize(600, 400)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.btn_cancel.clicked.connect(self.quit)
        self.btn_ok.clicked.connect(self.save)
        self.btn_cat_path.clicked.connect(self.getCatDir)
        self.btn_bias_path.clicked.connect(self.getBiasDir)
        self.btn_dark_path.clicked.connect(self.getDarkDir)
        self.btn_flat_path.clicked.connect(self.getFlatDir)
        self.btn_object_path.clicked.connect(self.getObjectDir)

        self.items_goal = []
        self.items_source = []
        self.update_keyword_dict = {}

        self.le_list = [self.le_cat_path, self.le_bias_path, self.le_dark_path, self.le_object_path, self.le_flat_path]
        for le in self.le_list:
            le.editingFinished.connect(self.checkDirPath)

        self.cb_ptype.addItems(['ALL', 'STREAK', 'POINT'])
        self.cb_track.addItems(['STAR', 'TARGET'])

        self.box_header.setVisible(True)
        self.initHeader()
        self.box_aofc.setVisible(True)

        self.box_sofc.setVisible(False)
        self.box_smod.setVisible(False)
        self.box_tvod.setVisible(False)
        self.box_track.setVisible(False)
        self.btn_ok.setText('保存')

        self.title = title
        self.system = None
        self.process_list = []
        self.new_config = False
        self.config_path = config_path
        self.configparser = configparser.ConfigParser()

        self.tvod_input_path = None
        self.tvod_can_path = None
        self.tvod_ref_path = None
        self.tvod_com_path = None
        self.tvod_var_path = None
        self.smod_input_path = None
        self.smod_save_path = None
        self.smod_cloud_save_flag = None
        self.smod_cloud_save_path = None

    def setTitle(self, title):
        self.title = title
        self.setWindowTitle(title)

    def load(self, system, config_path, process, new_config=False,
             aofc_object_path=None, aofc_object_wildcard=None,
             smod_input_path=None, smod_save_path=None, smod_cloud_save_flag=None, smod_cloud_save_path=None,
             tvod_input_path=None, tvod_can_path=None, tvod_ref_path=None, tvod_com_path=None, tvod_var_path=None):
        self.configparser.clear()
        self.configparser.read(config_path)

        # aofc
        (bias_path, bias_wildcard, dark_path, dark_wildcard, flat_path, flat_wildcard, object_path,
         object_wildcard) = self.getPreprocess()
        if aofc_object_path:
            object_path = aofc_object_path
        if aofc_object_wildcard:
            object_wildcard = aofc_object_wildcard
        self.setPreprocess(bias_path, bias_wildcard, dark_path, dark_wildcard, flat_path, flat_wildcard,
                           object_path,
                           object_wildcard)
        essential_keywords, update_keywords = self.getUpdateHeader()
        self.setUpdateHeader(essential_keywords, update_keywords)
        self.setCalibration(self.getCalibration())
        self.box_sofc.setVisible(True)
        bkg_box_size, seg_threshold, seg_npixels = self.getExtractSource()
        self.setExtractSource(bkg_box_size, seg_threshold, seg_npixels)
        radius, radius_in, radius_out = self.getAperTarget()
        self.setAperTarget(radius, radius_in, radius_out)

        if system == 'sofc' or system == 'deim' or system == 'smod':
            self.box_track.setVisible(True)
            self.box_smod.setVisible(True)
            image_number, time_moment, noise_length, hough_npoints, lines_npoints, p_type, track = self.getIdentifyTarget()
            self.setIdentifyTarget(image_number, time_moment, noise_length, hough_npoints, lines_npoints, p_type, track)

            self.smod_input_path = smod_input_path
            self.smod_save_path = smod_save_path
            self.smod_cloud_save_flag = smod_cloud_save_flag
            self.smod_cloud_save_path = smod_cloud_save_path
            if system == 'smod':
                self.cb_track.setCurrentText('STAR')
            elif system == 'sofc':
                self.cb_track.setCurrentText('TARGET')

        if system == 'tvod':
            self.box_tvod.setVisible(True)
            candidate_star_num, reference_star_num, p, min_num, ratio, data_filter = self.getTvod()
            self.setTvod(candidate_star_num, reference_star_num, p, min_num, ratio, data_filter)
            self.tvod_input_path = tvod_input_path
            self.tvod_can_path = tvod_can_path
            self.tvod_ref_path = tvod_ref_path
            self.tvod_com_path = tvod_com_path
            self.tvod_var_path = tvod_var_path
        elif system == 'deim':
            pass

        self.new_config = new_config
        self.process_list = process
        self.system = system
        self.config_path = config_path

    def save(self):
        filename = ''
        if self.new_config:
            # create new config
            dialog = MyDialog(self, title='保存设置', label_name='配置名:')
            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.value
                self.config_path = './memory/' + self.system + '/' + filename + '.ini'
            else:
                return
        config = configparser.ConfigParser()
        # aofc and sofc
        self.saveDefault(config)
        self.savePreprocess(config)
        self.saveUpdateHeader(config)
        self.saveCalibration(config)
        self.saveExtractSource(config)
        self.saveAperTarget(config)

        if self.system == 'sofc' or self.system == 'deim' or self.system == 'smod':
            self.saveIdentifyTarget(config)

        if self.system == 'tvod':
            self.saveTvod(config)
        elif self.system == 'smod':
            self.saveSmod(config)
        elif self.system == 'deim':
            pass

        with open(self.config_path, 'w', encoding='utf-8') as f:
            config.write(f)

        self.setVisible(False)
        self.sigSaveOK.emit(self.config_path[14:-4])

    def quit(self):
        self.setVisible(False)

    def initHeader(self):
        self.tableWidget.clear()
        self.listWidget_essential_source.clear()
        self.listWidget_essential_source.itemDoubleClicked.connect(self.addItemToGoal)
        self.listWidget_essential_goal.itemDoubleClicked.connect(self.removeItemFromGoal)
        self.listWidget_essential_goal.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_essential_goal.customContextMenuRequested.connect(self.showListMenu)

        # update keyword table
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.showTableMenu)

    def showListMenu(self, pos):
        menu = QMenu()
        item1 = menu.addAction('新增')
        action = menu.exec(self.listWidget_essential_goal.mapToGlobal(pos))
        if action == item1:
            dialog = MyDialog(self, title='新增文件头', label_name='文件头:')
            if dialog.exec_() == QDialog.Accepted:
                header = dialog.value
                self.items_goal.append(header)
                self.listWidget_essential_goal.clear()
                self.listWidget_essential_goal.addItems(self.items_goal)

    def showTableMenu(self, pos):
        def on_menu_about_to_hide():
            # 判断鼠标是否还在菜单区域内
            if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
                return

        selectedItems = self.tableWidget.selectionModel().selectedIndexes()

        menu = QMenu()
        menu.aboutToHide.connect(on_menu_about_to_hide)

        item1 = menu.addAction('新增')
        item2 = menu.addAction('删除')
        item3 = menu.addAction('取消')
        action = menu.exec(self.tableWidget.mapToGlobal(pos))

        if action == item1:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        elif action == item2:
            if len(selectedItems) > 0:
                rowNum = selectedItems[-1].row()
                self.tableWidget.removeRow(rowNum)
        else:
            return

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

    def getPreprocess(self):
        bias_path = self.configparser.get('Preprocess', 'bias_path')
        bias_wildcard = self.configparser.get('Preprocess', 'bias_wildcard')
        dark_path = self.configparser.get('Preprocess', 'dark_path')
        dark_wildcard = self.configparser.get('Preprocess', 'dark_wildcard')
        flat_path = self.configparser.get('Preprocess', 'flat_path')
        flat_wildcard = self.configparser.get('Preprocess', 'flat_wildcard')
        object_path = self.configparser.get('Preprocess', 'object_path')
        object_wildcard = self.configparser.get('Preprocess', 'object_wildcard')
        return (bias_path, bias_wildcard, dark_path, dark_wildcard, flat_path, flat_wildcard, object_path,
                object_wildcard)

    def setPreprocess(self, bias_path, bias_wildcard, dark_path, dark_wildcard, flat_path, flat_wildcard, object_path,
                      object_wildcard):
        self.le_bias_path.setText(bias_path)
        self.le_bias_wildcard.setText(bias_wildcard)
        self.le_dark_path.setText(dark_path)
        self.le_dark_wildcard.setText(dark_wildcard)
        self.le_flat_path.setText(flat_path)
        self.le_flat_wildcard.setText(flat_wildcard)
        self.le_object_path.setText(object_path)
        self.le_object_wildcard.setText(object_wildcard)

    def getUpdateHeader(self):
        essential_keywords = self.configparser.get('UpdateHeader', 'essential_keywords')
        update_keywords = self.configparser.get('UpdateHeader', 'update_keywords')
        return essential_keywords, update_keywords

    def setUpdateHeader(self, essential_keywords, update_keywords):
        self.listWidget_essential_source.clear()
        self.listWidget_essential_goal.clear()
        self.items_goal = literal_eval(essential_keywords)
        self.listWidget_essential_goal.addItems(self.items_goal)
        self.items_source = ["RA", "DEC", "EPOCH", "OBSTIME", "EXPTIME", "FILTER", "SCALE", "CCDTYPE", "TRACK", "GAIN",
                             "RDNOISE"]
        for s in self.items_goal:
            if s in self.items_source:
                self.items_source.remove(s)

        self.listWidget_essential_source.addItems(self.items_source)

        # 字符串转换成列表和字典
        self.update_keyword_dict = literal_eval(update_keywords)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(self.update_keyword_dict))
        self.tableWidget.setHorizontalHeaderLabels(['关键字', '值'])
        # 设置表格数据
        row_index = 0
        for key, value in self.update_keyword_dict.items():
            self.tableWidget.setItem(row_index, 0, QTableWidgetItem(key))
            self.tableWidget.setItem(row_index, 1, QTableWidgetItem(str(value)))
            row_index += 1

    def getCalibration(self):
        return self.configparser.get('Calibration', 'cat_path')

    def setCalibration(self, cat_path):
        self.le_cat_path.setText(cat_path)

    def getExtractSource(self):
        bkg_box_size = self.configparser.get('ExtractSource', 'bkg_box_size')
        seg_threshold = self.configparser.get('ExtractSource', 'seg_threshold')
        seg_npixels = self.configparser.get('ExtractSource', 'seg_npixels')
        return bkg_box_size, seg_threshold, seg_npixels

    def setExtractSource(self, bkg_box_size, seg_threshold, seg_npixels):
        size = bkg_box_size.replace('(', '').replace(')', ' ').split(',')
        self.sb_bkg_box_min.setValue(int(size[0]))
        self.sb_bkg_box_max.setValue(int(size[1]))
        self.sb_seg_threshold.setValue(float(seg_threshold))
        self.sb_seg_npixels.setValue(int(seg_npixels))

    def getAperTarget(self):
        radius = self.configparser.get('AperTarget', 'radius')
        radius_in = self.configparser.get('AperTarget', 'radius_in')
        radius_out = self.configparser.get('AperTarget', 'radius_out')
        return radius, radius_in, radius_out

    def setAperTarget(self, radius, radius_in, radius_out):
        self.sb_radius.setValue(int(radius))
        self.sb_radius_in.setValue(int(radius_in))
        self.sb_radius_out.setValue(int(radius_out))

    def getIdentifyTarget(self):
        image_number = self.configparser.get('IdentifyTarget', 'image_number')
        time_moment = self.configparser.get('IdentifyTarget', 'time_moment')
        noise_length = self.configparser.get('IdentifyTarget', 'noise_length')
        hough_npoints = self.configparser.get('IdentifyTarget', 'hough_npoints')
        lines_npoints = self.configparser.get('IdentifyTarget', 'lines_npoints')
        p_type = self.configparser.get('IdentifyTarget', 'ptype')
        track = self.configparser.get('IdentifyTarget', 'track')
        return image_number, time_moment, noise_length, hough_npoints, lines_npoints, p_type, track

    def setIdentifyTarget(self, image_number, time_moment, noise_length, hough_npoints, lines_npoints, p_type, track):
        self.sb_image_num.setValue(int(image_number))
        self.sb_time_moment.setValue(int(time_moment))
        self.sb_noise_length.setValue(int(noise_length))
        self.sb_hough_npoints.setValue(int(hough_npoints))
        self.sb_lines_npoints.setValue(int(lines_npoints))
        # self.le_ptype.setText(p_type)
        self.cb_ptype.setCurrentText(p_type)
        # self.le_track.setText(track)
        self.cb_track.setCurrentText(track)

    def getTvod(self):
        candidate_star_num = self.configparser.get('Tvod', 'candidate_star_num')
        reference_star_num = self.configparser.get('Tvod', 'reference_star_num')
        p = self.configparser.get('Tvod', 'p')
        min_num = self.configparser.get('Tvod', 'min_num')
        ratio = self.configparser.get('Tvod', 'ratio')
        data_filter = self.configparser.get('Tvod', 'data_filter')
        return candidate_star_num, reference_star_num, p, min_num, ratio, data_filter

    def setTvod(self, candidate_star_num, reference_star_num, p, min_num, ratio, data_filter):
        self.sb_min_num.setValue(int(min_num))
        self.sb_candiate_num.setValue(int(candidate_star_num))
        self.sb_reference_num.setValue(int(reference_star_num))
        self.dsb_p_num.setValue(float(p))
        self.dsb_ratio.setValue(float(ratio))
        self.le_data_filter.setText(data_filter)

    def getHeaderParameter(self):
        essential_keywords = str(self.items_goal)
        update_keywords = str(self.update_keyword_dict)
        return essential_keywords, update_keywords

    def getAofcParameter(self):
        bias_path = self.le_bias_path.text()
        bias_wildcard = self.le_bias_wildcard.text()
        dark_path = self.le_dark_path.text()
        dark_wildcard = self.le_dark_wildcard.text()
        flat_path = self.le_flat_path.text()
        flat_wildcard = self.le_flat_wildcard.text()
        object_path = self.le_object_path.text()
        object_wildcard = self.le_object_wildcard.text()

        return (bias_path, bias_wildcard, dark_path, dark_wildcard, flat_path, flat_wildcard,
                object_path, object_wildcard)

    def getCatPathParameter(self):
        return self.le_cat_path.text()

    def saveDefault(self, config):
        if not config.has_section('Default'):
            # 增加section
            config.add_section('Default')
        config.set('Default', 'process', str(self.process_list))

    def savePreprocess(self, config):
        if not config.has_section('Preprocess'):
            config.add_section('Preprocess')
        (bias_path, bias_wildcard, dark_path, dark_wildcard,
         flat_path, flat_wildcard, object_path, object_wildcard) = self.getAofcParameter()
        config.set('Preprocess', 'bias_path', bias_path)
        config.set('Preprocess', 'bias_wildcard', bias_wildcard)
        config.set('Preprocess', 'dark_path', dark_path)
        config.set('Preprocess', 'dark_wildcard', dark_wildcard)
        config.set('Preprocess', 'flat_path', flat_path)
        config.set('Preprocess', 'flat_wildcard', flat_wildcard)
        config.set('Preprocess', 'object_path', object_path)
        config.set('Preprocess', 'object_wildcard', object_wildcard)

    def saveUpdateHeader(self, config):
        if not config.has_section('UpdateHeader'):
            config.add_section('UpdateHeader')
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

        config.set('UpdateHeader', 'essential_keywords', str(self.items_goal))
        config.set('UpdateHeader', 'update_keywords', str(self.update_keyword_dict))

    def saveCalibration(self, config):
        if not config.has_section('Calibration'):
            config.add_section('Calibration')
        config.set('Calibration', 'cat_path', self.le_cat_path.text())

    def saveExtractSource(self, config):
        if not config.has_section('ExtractSource'):
            config.add_section('ExtractSource')

        bkg_box_size = '(' + str(self.sb_bkg_box_min.value()) + ',' + str(self.sb_bkg_box_max.value()) + ')'
        seg_threshold = str(self.sb_seg_threshold.value())
        seg_npixels = str(self.sb_seg_npixels.value())

        config.set('ExtractSource', 'bkg_box_size', bkg_box_size)
        config.set('ExtractSource', 'seg_threshold', seg_threshold)
        config.set('ExtractSource', 'seg_npixels', seg_npixels)

    def saveAperTarget(self, config):
        if not config.has_section('AperTarget'):
            config.add_section('AperTarget')

        radius = str(self.sb_radius.value())
        radius_in = str(self.sb_radius_in.value())
        radius_out = str(self.sb_radius_out.value())

        config.set('AperTarget', 'radius', radius)
        config.set('AperTarget', 'radius_in', radius_in)
        config.set('AperTarget', 'radius_out', radius_out)

    def saveTvod(self, config):
        if not config.has_section('Tvod'):
            config.add_section('Tvod')

        candidate_star_num = str(self.sb_candiate_num.value())
        reference_star_num = str(self.sb_reference_num.value())
        p = str(self.dsb_p_num.value())
        min_num = str(self.sb_min_num.value())
        ratio = str(self.dsb_ratio.value())
        data_filter = self.le_data_filter.text()

        config.set('Tvod', 'cat2_path', self.tvod_input_path)
        config.set('Tvod', 'reference_star_path', self.tvod_ref_path)
        config.set('Tvod', 'candidate_star_path', self.tvod_can_path)
        config.set('Tvod', 'combine_star_path', self.tvod_com_path)
        config.set('Tvod', 'variable_star_path', self.tvod_var_path)

        config.set('Tvod', 'candidate_star_num', candidate_star_num)
        config.set('Tvod', 'reference_star_num', reference_star_num)
        config.set('Tvod', 'p', p)
        config.set('Tvod', 'min_num', min_num)
        config.set('Tvod', 'ratio', ratio)
        config.set('Tvod', 'data_filter', data_filter)

    def saveIdentifyTarget(self, config):
        if not config.has_section('IdentifyTarget'):
            config.add_section('IdentifyTarget')

        image_number = str(self.sb_image_num.value())
        # p_type = self.le_ptype.text()
        p_type = self.cb_ptype.currentText()
        time_moment = str(self.sb_time_moment.value())
        noise_length = str(self.sb_noise_length.value())
        hough_npoints = str(self.sb_hough_npoints.value())
        lines_npoints = str(self.sb_lines_npoints.value())
        # track = self.le_track.text()
        track = self.cb_track.currentText()
        config.set('IdentifyTarget', 'track', track)

        config.set('IdentifyTarget', 'image_number', image_number)
        config.set('IdentifyTarget', 'ptype', p_type)
        config.set('IdentifyTarget', 'time_moment', time_moment)
        config.set('IdentifyTarget', 'noise_length', noise_length)
        config.set('IdentifyTarget', 'hough_npoints', hough_npoints)
        config.set('IdentifyTarget', 'lines_npoints', lines_npoints)

    def saveSmod(self, config):
        if not config.has_section('Smod'):
            config.add_section('Smod')

        config.set('Smod', 'input_path', self.smod_input_path)
        config.set('Smod', 'save_path', self.smod_save_path)
        config.set('Smod', 'cloud_save_flag', str(self.smod_cloud_save_flag))
        config.set('Smod', 'cloud_save_path', self.smod_cloud_save_path)

    def getCatDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        if dirPath:
            self.le_cat_path.clear()
            self.le_cat_path.setText(dirPath + '/')

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



