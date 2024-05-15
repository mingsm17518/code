import threading
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QDir, Signal
from messagewidget import MessageWidget
from inieditwidget import InIEditWidget


class SystemRunThread(threading.Thread):
    def __init__(self, widget=None, config_path=None, process=None,
                 object_path=None, object_wildcard=None,
                 smod_input_path=None, smod_save_path=None, smod_cloud_flag=False, smod_cloud_path=None,
                 tvod_cat2_path=None, tvod_candidate_star_path=None,
                 tvod_combine_star_path=None, tvod_reference_path=None,tvod_variable_star_path=None
                 ):
        threading.Thread.__init__(self)
        self.widget = widget
        self.config_path = config_path
        self.process = process
        # aofc sofc deim
        self.object_path = object_path
        self.object_wildcard = object_wildcard
        # tvod
        self.tvod_variable_star_path = tvod_variable_star_path
        self.tvod_reference_path = tvod_reference_path
        self.tvod_combine_star_path = tvod_combine_star_path
        self.tvod_candidate_star_path = tvod_candidate_star_path
        self.tvod_cat2_path = tvod_cat2_path
        # smod
        self.smod_cloud_path = smod_cloud_path
        self.smod_cloud_flag = smod_cloud_flag
        self.smod_save_path = smod_save_path
        self.smod_input_path = smod_input_path

    def run(self):
        self.widget.system_process.run(config_path=self.config_path, process=self.process,
                                       object_path=self.object_path, object_wildcard=self.object_wildcard,
                                       cat2_path=self.tvod_cat2_path, candidate_star_path=self.tvod_candidate_star_path,
                                       combine_star_path=self.tvod_combine_star_path,
                                       reference_path=self.tvod_reference_path,
                                       variable_star_path=self.tvod_variable_star_path,
                                       input_path=self.smod_input_path, save_path=self.smod_save_path,
                                       cloud_flag=self.smod_cloud_flag, cloud_path=self.smod_cloud_path
                                       )
        self.widget.btn_run.setEnabled(True)


class SystemWidget(QWidget):
    sigLoadConfig = Signal(str)

    def __init__(self,parent=None):
        super().__init__(parent)

        # common ui
        self.cblist = None
        self.cbb_config = None
        self.cb_all = None
        self.textBrowser = None

        self.status = None
        self.system_name = None
        self.system_process = None
        self.system_config_dir = None

        self.errorWidget = MessageWidget()

        self.editWidget = InIEditWidget()
        self.editWidget.sigSaveOK.connect(self.loadNewConfig)
        self.editWidget.setVisible(False)

    def checkDirPath(self):
        le = self.sender()
        path = le.text()
        if path[-1] != '/':
            le.setText(path + '/')

    def loadNewConfig(self, filename):
        if self.system_name:
            self.updateConfigList('./memory/' + self.system_name + '/')
            self.cbb_config.setCurrentText(filename)
            self.sigLoadConfig.emit(filename)
        # self.loadConfig(filename)

    def stateCheck(self):
        if not self.sender().isChecked() and self.cb_all.isChecked():
            self.cb_all.setChecked(False)

    def getProcessList(self):
        m = []
        for i in range(len(self.cblist)):
            cb = self.cblist[i]
            if cb.isChecked():
                m.append(i + 1)
        return m

    def updateConfigList(self, config_dir):
        self.cbb_config.clear()
        workDir = QDir(config_dir)
        workDir.setFilter(QDir.Files)
        files = workDir.entryList()
        for f in files:
            self.cbb_config.addItem(f.split('.')[0])
        self.cbb_config.addItem('新配置')
        self.cbb_config.setCurrentText('新配置')

    def chooseAll(self):
        for cb in self.cblist:
            cb.setChecked(self.cb_all.isChecked())

    def debugInfo(self, m):
        self.textBrowser.append(m)

    def showErrorMsg(self, msg, traceback):
        self.errorWidget.setErrorMsg(msg, traceback)
        self.errorWidget.setVisible(True)

    def setStatusBar(self, statusBar):
        self.status = statusBar
        if self.system_process.sigProg:
            self.system_process.sigProg.connect(self.status.updateInfo)



