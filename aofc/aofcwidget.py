import pathlib
import configparser
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QIcon

from .ui_aofcwidget import Ui_Form
from aofc.aofc import AofcProcess
from systemwidget import SystemWidget, SystemRunThread


class AofcWidget(SystemWidget, Ui_Form):

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

        self.cblist = [self.cb_1, self.cb_2, self.cb_3, self.cb_4, self.cb_5, self.cb_6]
        self.lelist = [self.le_dir]
        for le in self.lelist:
            le.editingFinished.connect(self.checkDirPath)

        self.configparser = None
        self.system_name = 'aofc'
        self.system_config_dir = './memory/' + self.system_name + '/'
        self.updateConfigList(config_dir=self.system_config_dir)

        self.btn_dir.clicked.connect(self.getDir)
        self.btn_file.clicked.connect(self.getFile)
        self.btn_run.clicked.connect(self.run)
        self.btn_save_file.clicked.connect(self.saveFile)
        self.cb_all.clicked.connect(self.chooseAll)
        self.cbb_config.textActivated.connect(self.loadConfig)
        self.btn_detail.clicked.connect(self.showEditWidget)

        for cb in self.cblist:
            cb.clicked.connect(self.stateCheck)

        self.sigLoadConfig.connect(self.loadConfig)

        self.cb_dir_model.setVisible(False)

        self.system_process = AofcProcess()
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
        config_path = './memory/aofc/' + filename + '.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        config.set('Default', 'process', str(m))
        config.set('Preprocess', 'object_path', self.le_dir.text())
        config.set('Preprocess', 'object_wildcard', self.le_file.text())
        with open(config_path, 'w', encoding='utf-8') as f:
            config.write(f)
        self.textBrowser.append('<font color="green">[成功]配置已保存!</font>')

    def loadConfig(self, filename):
        if filename == '新配置':
            self.le_dir.clear()
            self.le_file.clear()
            self.cb_all.setChecked(False)
            for cbb in self.cblist:
                cbb.setChecked(False)
            return
        path = pathlib.Path('./memory/aofc/' + filename + '.ini')
        # 创建实例对象
        config = configparser.ConfigParser()
        # 读取配置文件
        config.clear()
        config.read(path, encoding="utf-8")
        process = config.get('Default', 'process')
        object_path = config.get('Preprocess', 'object_path')
        object_wildcard = config.get('Preprocess', 'object_wildcard')

        self.le_dir.setText(object_path)
        self.le_file.setText(object_wildcard)

        for i in range(len(self.cblist)):
            if str(i + 1) in process:
                self.cblist[i].setChecked(True)
            else:
                self.cblist[i].setChecked(False)

        self.configparser = config

    def getDir(self):
        dirPath = QFileDialog.getExistingDirectory(self, "choose directory", "./")
        self.le_dir.clear()
        self.le_dir.setText(dirPath + '/')

    def getFile(self):
        filePath = QFileDialog.getOpenFileName(self, "open file dialog")
        self.le_file.clear()
        self.le_file.setText(filePath[0])

    def chooseAll(self):
        for cb in self.cblist:
            cb.setChecked(self.cb_all.isChecked())

    def saveFile(self):
        filePath = QFileDialog.getSaveFileName(self, "save file", "./", "all files(*.*)")
        self.le_save.clear()
        self.le_save.setText(filePath[0])

    def run(self):
        self.textBrowser.clear()
        if not self.le_dir.text() or not self.le_file.text():
            self.textBrowser.append('路径或文件为空!')
            return
        # 将临时配置保存至公共配置
        self.btn_run.setEnabled(False)
        m = self.getProcessList()
        self.thread = SystemRunThread(self, config_path=self.system_config_dir + self.cbb_config.currentText() + '.ini',
                                      process=m, object_path=self.le_dir.text(), object_wildcard=self.le_file.text())
        self.thread.start()

    def showEditWidget(self):
        if self.editWidget.isVisible():
            return
        config_name = self.cbb_config.currentText()
        object_path = self.le_dir.text()
        object_wildcard = self.le_file.text()
        if config_name != '新配置':
            self.editWidget.setTitle(title='设置流量定标'+config_name+'.ini')
            self.editWidget.load(system='aofc', process=self.getProcessList(),
                                 new_config=False, config_path='./memory/aofc/'+config_name+'.ini',
                                 aofc_object_path=object_path, aofc_object_wildcard=object_wildcard)
        else:
            self.editWidget.setTitle(title='新建流量定标配置')
            self.editWidget.load(system='aofc', process=self.getProcessList(),
                                 new_config=True, config_path='./memory/common.ini',
                                 aofc_object_path=object_path, aofc_object_wildcard=object_wildcard)
        self.editWidget.setVisible(True)



