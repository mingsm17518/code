# 获取指定目录下所有文件
# 可根据后缀筛选
import os

from PySide6.QtWidgets import (QTreeView, QFileSystemModel, QWidget, QHBoxLayout, QVBoxLayout,
                               QLineEdit, QFileDialog, QPushButton, QLabel)
from PySide6.QtCore import Qt, Signal, QDir


class FileTreeWidget(QWidget):

    def __init__(self, parent=None, name='None', rootPath=None, filters=None):
        super().__init__(parent)

        layoutMain = QVBoxLayout()

        self.fileTreeView = FileTreeView(self, name, rootPath, filters)
        self.systemName = name
        self.fileResultPath = {'sofc': None, 'smod': None, 'deim': None, 'aofc': None, 'tvod': None}
        self.fileResultSuffix = {'sofc': ['*.aper', '*.photo'], 'smod': ['*.txt'], 'deim': ['*.png'], 'aofc': ['*.cat2'], 'tvod': ['*.txt']}

        self.lbDir = QLabel('路径:')
        self.leDir = QLineEdit(self)
        self.leDir.setFixedHeight(20)
        self.btnDir = QPushButton(self)
        self.btnDir.setText('...')
        self.btnDir.clicked.connect(self.selectDir)
        self.btnDir.setFixedWidth(30)

        layoutSelect = QHBoxLayout()
        layoutSelect.addWidget(self.lbDir)
        layoutSelect.addWidget(self.leDir)
        layoutSelect.addWidget(self.btnDir)

        layoutSelect.setSpacing(1)
        layoutSelect.setContentsMargins(0, 0, 0, 0)

        layoutMain.addLayout(layoutSelect)
        layoutMain.addWidget(self.fileTreeView)

        layoutMain.setSpacing(0)
        layoutMain.setContentsMargins(0, 0, 0, 0)
        layoutMain.setStretch(0, 0)
        layoutMain.setStretch(0, 1)

        self.setLayout(layoutMain)

    def selectDir(self):
        path = QFileDialog.getExistingDirectory(self, '请选择路径', './')
        self.leDir.setText(path)
        self.fileTreeView.setRootPath(path)
        self.fileResultPath[self.systemName] = path
        if self.systemName in self.fileResultPath:
            self.fileTreeView.model.setNameFilters(self.fileResultSuffix[self.systemName])

    def setSystemName(self, name):
        self.systemName = name
        self.fileTreeView.systemName = name
        if self.systemName in self.fileResultPath:
            self.setFileTreeViewRootPath(self.fileResultPath[self.systemName])

    def setFileTreeViewRootPath(self, path):
        self.leDir.setText(path)
        self.fileTreeView.setRootPath(path)


class FileTreeView(QTreeView):
    sigShowFileInfo = Signal(str)
    sigOpenFile = Signal(str, str, str)

    def __init__(self, parent=None, name='None', rootPath=None, filters=None):
        super().__init__(parent=parent)

        self.setObjectName(name)
        self.systemName = None

        self.model = QFileSystemModel()
        if rootPath:
            self.model.setRootPath(rootPath)

        if filters:
            self.model.setFilter(filters)

        self.model.setFilter(QDir.Files | QDir.NoDotAndDotDot)
        self.model.setNameFilterDisables(False)

        self.setModel(self.model)
        self.setRootIndex(self.model.index(rootPath))

        self.doubleClicked.connect(self.openFile)

        self.setMouseTracking(True)
        self.currentItemRow = None

        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)

    def openFile(self, index):
        flag = False
        if self.systemName == 'tvod':
            if self.model.fileInfo(index).suffix() == 'txt':
                flag = True
        elif self.systemName == 'smod':
            if self.model.fileInfo(index).suffix() == 'txt':
                flag = True
        elif self.systemName == 'aofc':
            if self.model.fileInfo(index).suffix() == 'cat2':
                flag = True
        elif self.systemName == 'sofc':
            if self.model.fileInfo(index).suffix() == 'aper' or self.model.fileInfo(index).suffix() == 'photo':
                flag = True
        elif self.systemName == 'deim':
            if self.model.fileInfo(index).suffix() == 'png':
                flag = True

        if flag:
            self.sigOpenFile.emit(self.systemName, self.model.fileInfo(index).filePath(),
                                  self.model.fileInfo(index).fileName())

    def setRootPath(self, path):
        self.model.setRootPath(path)
        self.setRootIndex(self.model.index(path))

    def setFilter(self, filters):
        self.model.setNameFilters(filters)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        row = index.row()
        if self.currentItemRow == row:
            return
        if index.isValid():
            # print(self.model.fileInfo(index))
            self.sigShowFileInfo.emit(self.model.fileInfo(index).fileName())

        self.currentItemRow = row
