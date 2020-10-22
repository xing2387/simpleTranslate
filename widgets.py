# coding=utf-8

import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget, QWidget, QLineEdit, QDateTimeEdit, QVBoxLayout, QHBoxLayout \
        , QGridLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt, QDateTime
import os
import baidudict
import youdaodict

# 应用程序的主Widget
class MainWidget(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.initUI()

    def initUI(self):
        vlayout = QVBoxLayout()
        grid = QGridLayout()
        label1 = QLabel('原文')
        self.input = QTextEdit()
        label2 = QLabel('翻译')
        self.output = QTextEdit()
        self.switch = QCheckBox("开始")
        self.alwaysOnTop = QCheckBox("置顶窗口")
        self.baidu = QCheckBox("百度")
        self.youdao = QCheckBox("有道")
        self.youdao.setCheckState(Qt.CheckState.Checked)
        grid.addWidget(label1, 0, 0)
        grid.addWidget(self.input, 0, 1, 1, 6)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(self.output, 1, 1, 1, 6)
        grid.addWidget(self.switch, 2, 1)
        grid.addWidget(self.alwaysOnTop, 2, 2)
        grid.addWidget(self.baidu, 2, 3)
        grid.addWidget(self.youdao, 2, 4)
        vlayout.addLayout(grid)
        vlayout.addStretch(1)
        self.setLayout(vlayout)
        self.alwaysOnTop.stateChanged.connect(lambda: self.setAlwaysOnTop(self.alwaysOnTop))
        self.baidu.stateChanged.connect(lambda: self.switchToBaidu())
        self.youdao.stateChanged.connect(lambda: self.switchToYoudao())

    def setAlwaysOnTop(self, checkBox):
        if checkBox.isChecked():
            self.window.setWindowFlags(
                self.window.windowFlags() |
                QtCore.Qt.WindowStaysOnTopHint
            )
        else:
            self.window.setWindowFlags(
                self.window.windowFlags() &
                ~QtCore.Qt.WindowStaysOnTopHint
            )
        if not self.window.isVisible():
            self.window.setVisible(True)

    def onClipboradChanged(self):
        if not self.switch.isChecked():
            return
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            content = str(text)
            print('onClipboradChanged---' + content + ' len = ' + str(len(content)))
            self.input.setText(content)
            translation = ""
            if self.baidu.isChecked():
                translation = baidudict.getTranslate(content)
            elif self.youdao.isChecked():
                translation = youdaodict.getTranslate(content)
            self.output.setText(translation)

    def switchToBaidu(self):
        if self.baidu.isChecked():
            self.youdao.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.youdao.setCheckState(Qt.CheckState.Checked)

    def switchToYoudao(self):
        if self.youdao.isChecked():
            self.baidu.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.baidu.setCheckState(Qt.CheckState.Checked)