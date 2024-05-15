import pathlib
import configparser
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QIcon

from .ui_smodwidget import Ui_Form
from smod.code.main import SmodProcess
from systemwidget import SystemWidget, SystemRunThread


class SmodWidget(SystemWidget, Ui_Form):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.btn_save_config.setVisible(True)
        self.btn_save_config.setIcon(QIcon('./resources/保存.png'))
        self.btn_save_config.setFixedSize(25, 25)
        self.btn_save_config.clicked.connect(self.saveConfig)
        self.btn_detail.setIcon(QIcon('./resources/设置.png'))
        self.btn_detail.setFixedSize(25, 25)
        self.btn_save_config.setText('')
        self.btn_detail.setText('')

        self.cblist = [self.cb_1, self.cb_2, self.cb_3, self.cb_4, self.cb_5, self.cb_6, self.cb_7, self.cb_8,
                       self.cb_9]
        self.lelist = [self.le_dir, self.le_save]
        for le in self.lelist:
            le.editingFinished.connect(self.checkDirPath)

        self.configparser = None
        self.system_name = 'smod'
        self.system_config_dir = './memory/' + self.system_name + '/'
        self.updateConfigList(config_dir=self.system_config_dir)

        self.btn_dir.clicked.connect(self.getDir)
        self.btn_cloud.clicked.connect(self.saveCloud)
        self.btn_run.clicked.connect(self.run)
        self.btn_save_file.clicked.connect(self.saveDir)
        self.cb_all.clicked.connect(self.chooseAll)
        self.cbb_config.textActivated.connect(self.loadConfig)
        self.sigLoadConfig.connect(self.loadConfig)
        self.btn_detail.clicked.connect(self.showEditWidget)

        for cb in self.cblist:
            cb.clicked.connect(self.stateCheck)

        self.system_process = SmodProcess()
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
        config_path = './memory/smod/' + filename + '.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        config.set('Default', 'process', str(m))
        config.set('Smod', 'input_path', self.le_dir.text())
        config.set('Smod', 'save_path', self.le_save.text())
        config.set('Smod', 'cloud_save_flag', str(self.cb_save_cloud.isChecked()))
        config.set('Smod', 'cloud_save_path', self.le_cloud.text())
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)
        self.textBrowser.append('<font color="green">[成功]配置已保存!</font>')

    def getDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        self.le_dir.clear()
        self.le_dir.setText(dirPath + '/')

    def getSaveFile(self):
        filePath = QFileDialog.getSaveFileName(self, "save file", "./", "all files(*.*)")
        return filePath[0]

    def saveCloud(self):
        filePath = self.getSaveFile()
        self.le_cloud.clear()
        self.le_cloud.setText(filePath)

    def saveDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        self.le_save.clear()
        self.le_save.setText(dirPath + '/')

    def loadConfig(self, filename):
        if filename == '新配置':
            self.le_dir.clear()
            self.le_save.clear()
            self.le_cloud.clear()
            self.cb_all.setChecked(False)
            self.cb_save_cloud.setChecked(False)
            for cbb in self.cblist:
                cbb.setChecked(False)
            return
        path = pathlib.Path('./memory/smod/' + filename + '.ini')
        # 创建实例对象
        config = configparser.ConfigParser()
        # 读取配置文件
        config.clear()
        config.read(path, encoding="utf-8")

        process = config.get('Default', 'process')
        input_path = config.get('Smod', 'input_path')
        save_path = config.get('Smod', 'save_path')
        cloud_flag = config.get('Smod', 'cloud_save_flag')
        cloud_path = config.get('Smod', 'cloud_save_path')

        self.le_dir.setText(input_path)
        self.le_save.setText(save_path)
        self.cb_save_cloud.setChecked(True if cloud_flag.upper() == 'TRUE' else False)
        self.le_cloud.setText(cloud_path)

        for i in range(len(self.cblist)):
            if str(i + 1) in process:
                self.cblist[i].setChecked(True)
            else:
                self.cblist[i].setChecked(False)

        self.configparser = config

    def run(self):
        self.textBrowser.clear()
        if self.cbb_config.currentText() == '新配置':
            self.textBrowser.append('请选择已保存的配置运行!')
            return
        if not self.le_dir.text() or not self.le_save.text():
            self.textBrowser.append('路径或文件为空!')
            return

        if self.cb_save_cloud.isChecked() and (not self.le_cloud.text()):
            self.textBrowser.append('点云路径为空!')
            return

        self.btn_run.setEnabled(False)
        m = self.getProcessList()

        self.thread = SystemRunThread(widget=self, process=m,
                                      config_path='./memory/smod/' + self.cbb_config.currentText() + '.ini',
                                      smod_input_path=self.le_dir.text(),
                                      smod_save_path=self.le_save.text(),
                                      smod_cloud_flag=self.cb_save_cloud.isChecked(),
                                      smod_cloud_path=self.le_cloud.text())
        self.thread.start()

    def showEditWidget(self):
        if self.editWidget.isVisible():
            return
        config_name = self.cbb_config.currentText()
        input_path = self.le_dir.text()
        save_path = self.le_save.text()
        cloud_path = self.le_cloud.text()
        if config_name != '新配置':
            self.editWidget.setTitle(title='设置目标搜寻' + config_name + '.ini')
            self.editWidget.load(system='smod', process=self.getProcessList(),
                                 new_config=False, config_path='./memory/smod/' + config_name + '.ini',
                                 smod_input_path=input_path, smod_save_path=save_path,
                                 smod_cloud_save_flag=self.cb_save_cloud.isChecked(), smod_cloud_save_path=cloud_path)
        else:
            self.editWidget.setTitle(title='新建目标搜寻配置')
            self.editWidget.load(system='smod', process=self.getProcessList(),
                                 new_config=True, config_path='./memory/common.ini',
                                 smod_input_path=input_path, smod_save_path=save_path,
                                 smod_cloud_save_flag=self.cb_save_cloud.isChecked(), smod_cloud_save_path=cloud_path)
        self.editWidget.setVisible(True)
