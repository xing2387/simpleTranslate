# coding=utf-8

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget, QWidget, QLineEdit, QDateTimeEdit, QVBoxLayout, QHBoxLayout \
        , QGridLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt, QDateTime
import os
import utils

# 应用程序的主Widget
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vlayout = QVBoxLayout()
        grid = QGridLayout()
        label1 = QLabel('原文')
        self.input = QTextEdit()
        label2 = QLabel('翻译')
        self.output = QTextEdit()
        self.switch = QCheckBox("开始")
        grid.addWidget(label1, 0, 0)
        grid.addWidget(self.input, 0, 1, )
        grid.addWidget(label2, 1, 0)
        grid.addWidget(self.output, 1, 1)
        grid.addWidget(self.switch, 2, 1)
        vlayout.addLayout(grid)
        vlayout.addStretch(1)
        self.setLayout(vlayout)


    def onClipboradChanged(self):
        if not self.switch.isChecked():
            return
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            content = str(text)
            print('onClipboradChanged---' + content + ' len = ' + str(len(content)))
            self.input.setText(content)
            self.output.setText(utils.getTranslate(content))
