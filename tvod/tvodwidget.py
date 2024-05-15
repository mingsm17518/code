import pathlib
import configparser

from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QIcon

from .ui_tvodwidget import Ui_Form
from tvod.main import TvodProcess
from systemwidget import SystemWidget, SystemRunThread


class TvodWidget(SystemWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.configparser = None
        self.btn_save_config.setVisible(True)
        self.btn_save_config.setIcon(QIcon('./resources/保存.png'))
        self.btn_save_config.setFixedSize(25, 25)
        self.btn_save_config.clicked.connect(self.saveConfig)
        self.btn_detail.setIcon(QIcon('./resources/设置.png'))
        self.btn_detail.setFixedSize(25, 25)
        self.btn_save_config.setText('')
        self.btn_detail.setText('')

        self.btn_cat2.clicked.connect(self.getCat2)
        self.btn_combine.clicked.connect(self.getCombine)
        self.btn_reference.clicked.connect(self.getReference)
        self.btn_candidate.clicked.connect(self.getCandidate)
        self.btn_save_file.clicked.connect(self.getVariable)
        self.btn_detail.clicked.connect(self.showEditWidget)

        self.btn_run.clicked.connect(self.run)

        self.cblist = [self.cb_1, self.cb_2, self.cb_3]
        self.lelist = [self.le_cat2, self.le_candidate, self.le_combine, self.le_save]
        for le in self.lelist:
            le.editingFinished.connect(self.checkDirPath)

        self.cb_all.clicked.connect(self.chooseAll)
        self.cbb_config.textActivated.connect(self.loadConfig)
        self.sigLoadConfig.connect(self.loadConfig)

        for cb in self.cblist:
            cb.clicked.connect(self.stateCheck)

        self.system_name = 'tvod'
        self.system_config_dir = './memory/' + self.system_name + '/'
        self.updateConfigList(config_dir=self.system_config_dir)

        self.system_process = TvodProcess()
        self.system_process.sigDebugInfo.connect(self.debugInfo)
        self.system_process.sigError.connect(self.showErrorMsg)

        self.status = None
        self.thread = None

    def saveConfig(self):
        filename = self.cbb_config.currentText()
        if filename == '新配置':
            self.textBrowser.append('<font color="blue">[警告]详细配置未设置!</font>')
            return
        m = self.getProcessList()
        config_path = './memory/tvod/' + filename + '.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        config.set('Default', 'process', str(m))
        config.set('Tvod', 'cat2_path', self.le_cat2.text())
        config.set('Tvod', 'reference_star_path', self.le_reference.text())
        config.set('Tvod', 'candidate_star_path', self.le_candidate.text())
        config.set('Tvod', 'combine_star_path', self.le_candidate.text())
        config.set('Tvod', 'variable_star_path', self.le_save.text())
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)
        self.textBrowser.append('<font color="green">[成功]配置已保存!</font>')

    def loadConfig(self, filename):
        if filename == '新配置':
            self.le_save.clear()
            self.le_combine.clear()
            self.le_candidate.clear()
            self.le_cat2.clear()
            self.le_reference.clear()
            self.cb_all.setChecked(False)
            for cbb in self.cblist:
                cbb.setChecked(False)
            return
        path = pathlib.Path('./memory/tvod/' + filename + '.ini')
        # 创建实例对象
        config = configparser.ConfigParser()
        # 读取配置文件
        config.clear()
        config.read(path, encoding="utf-8")

        process = []
        cat2_path = ''
        candidate_star_path = ''
        reference_star_path = ''
        variable_star_path = ''
        combine_star_path = ''

        if config.has_section('Tvod'):
            process = config.get('Default', 'process')
            cat2_path = config.get('Tvod', 'cat2_path')
            candidate_star_path = config.get('Tvod', 'candidate_star_path')
            reference_star_path = config.get('Tvod', 'reference_star_path')
            combine_star_path = config.get('Tvod', 'combine_star_path')
            variable_star_path = config.get('Tvod', 'variable_star_path')

        for i in range(len(self.cblist)):
            if str(i + 1) in process:
                self.cblist[i].setChecked(True)
            else:
                self.cblist[i].setChecked(False)

        self.le_candidate.setText(candidate_star_path)
        self.le_cat2.setText(cat2_path)
        self.le_reference.setText(reference_star_path)
        self.le_save.setText(variable_star_path)
        self.le_combine.setText(combine_star_path)

        self.configparser = config

    def getDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        return dirPath

    def getFile(self):
        filePath = QFileDialog.getOpenFileName(self, "open file dialog")
        return filePath[0]

    def getSaveFile(self):
        filePath = QFileDialog.getSaveFileName(self, "save file", "./", "all files(*.*)")
        return filePath[0]

    def getCat2(self):
        dirPath = self.getDir()
        self.le_cat2.clear()
        self.le_cat2.setText(dirPath + '/')

    def getCandidate(self):
        dirPath = self.getDir()
        self.le_candidate.clear()
        self.le_candidate.setText(dirPath + '/')

    def getVariable(self):
        dirPath = self.getDir()
        self.le_save.clear()
        self.le_save.setText(dirPath + '/')

    def getCombine(self):
        dirPath = self.getDir()
        self.le_combine.clear()
        self.le_combine.setText(dirPath + '/')

    def getReference(self):
        filePath = self.getSaveFile()
        self.le_reference.clear()
        self.le_reference.setText(filePath)

    def run(self):
        # get parameter
        if not self.le_cat2.text() or not self.le_candidate.text() or not self.le_combine.text() or not self.le_reference.text() or not self.le_save.text():
            self.textBrowser.append('路径或文件为空!')
            return

        self.btn_run.setEnabled(False)
        self.textBrowser.clear()
        m = self.getProcessList()

        process = SystemRunThread(widget=self, tvod_cat2_path=self.le_cat2.text(),
                                  tvod_candidate_star_path=self.le_candidate.text(),
                                  tvod_combine_star_path=self.le_combine.text(),
                                  tvod_reference_path=self.le_reference.text(),
                                  tvod_variable_star_path=self.le_save.text(),
                                  process=m,
                                  config_path=self.system_config_dir + self.cbb_config.currentText() + '.ini')

        process.start()

    def showEditWidget(self):
        if self.editWidget.isVisible():
            return
        config_name = self.cbb_config.currentText()
        cat_path = self.le_cat2.text()
        ref_path = self.le_reference.text()
        com_path = self.le_combine.text()
        var_path = self.le_save.text()
        can_path = self.le_candidate.text()

        if config_name != '新配置':
            self.editWidget.setTitle(title='设置变源检测' + config_name + '.ini')
            self.editWidget.load(system='tvod', process=self.getProcessList(),
                                 new_config=False, config_path='./memory/tvod/' + config_name + '.ini',
                                 tvod_input_path=cat_path, tvod_ref_path=ref_path, tvod_com_path=com_path,
                                 tvod_var_path=var_path, tvod_can_path=can_path)
        else:
            self.editWidget.setTitle(title='新建变源检测配置')
            self.editWidget.load(system='tvod', process=self.getProcessList(),
                                 new_config=True, config_path='./memory/common.ini',
                                 tvod_input_path=cat_path, tvod_ref_path=ref_path, tvod_com_path=com_path,
                                 tvod_var_path=var_path, tvod_can_path=can_path)
        self.editWidget.setVisible(True)
