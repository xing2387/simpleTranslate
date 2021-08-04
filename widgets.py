# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QWidget, QVBoxLayout, \
        QGridLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt, QRect
import os
import baidudict
import youdao2
from pyqtkeybind import keybinder       #全局快捷键

class MainWidget(QWidget):
    def __init__(self, window:QMainWindow):
        super().__init__()
        self.window_ = window
        self.initUI()

    def initUI(self):
        vlayout = QVBoxLayout()
        grid = QGridLayout()

        def incColumn():
            nonlocal column
            result = column
            column += 1
            return result
        row = 0
        column = 0
        label1 = QLabel('原文')
        grid.addWidget(label1, row, incColumn(), 1, 1)
        self.input = QTextEdit()
        grid.addWidget(self.input, row, incColumn(), 1, 8)
        row = 1
        column = 0
        label2 = QLabel('翻译')
        grid.addWidget(label2, row, incColumn(), 1, 1)
        self.output = QTextEdit()
        grid.addWidget(self.output, row, incColumn(), 1, 8)

        row = 2
        column = 0
        labelSpan = QLabel('')
        grid.addWidget(labelSpan, row, incColumn(), 1, 1)
        self.switch = QCheckBox("剪贴板")
        self.switch.stateChanged.connect(lambda: self.onClipboardChecked())
        grid.addWidget(self.switch, row, incColumn())
        
        self.hotkeyCombo = "Alt+T"
        self.hotkey = QCheckBox(self.hotkeyCombo)
        self.hotkey.stateChanged.connect(lambda: self.onHotkeyChecked())
        # self.hotkey.setChecked(True)
        # self.onHotkeyChecked()
        grid.addWidget(self.hotkey, row, incColumn())

        self.alwaysOnTop = QCheckBox("置顶")
        self.alwaysOnTop.stateChanged.connect(lambda: self.setAlwaysOnTop(self.alwaysOnTop))
        grid.addWidget(self.alwaysOnTop, row, incColumn())

        # row = 3
        # column = 0
        # labelSpan = QLabel('')
        # grid.addWidget(labelSpan, row, incColumn(), 1, 1)
        self.baidu = QCheckBox("百度")
        self.baidu.stateChanged.connect(lambda: self.switchToBaidu())
        grid.addWidget(self.baidu, row, incColumn())
        self.youdao = QCheckBox("有道")
        self.youdao.setCheckState(Qt.CheckState.Checked)
        self.youdao.stateChanged.connect(lambda: self.switchToYoudao())
        grid.addWidget(self.youdao, row, incColumn())

        grid.setColumnStretch(0,0)
        grid.setRowStretch(1,2)
        grid.setRowStretch(0,1)

        vlayout.addLayout(grid)
        self.setLayout(vlayout)

    def setAlwaysOnTop(self, checkBox:QCheckBox):
        if checkBox.isChecked():
            self.window_.setWindowFlags(
                self.window_.windowFlags() |
                Qt.WindowStaysOnTopHint
            )
        else:
            self.window_.setWindowFlags(
                self.window_.windowFlags() &
                ~Qt.WindowStaysOnTopHint
            )
        if not self.window_.isVisible():
            self.window_.setVisible(True)

    def onClipboardChecked(self):
        if self.switch.isChecked():
            self.hotkey.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.hotkey.setCheckState(Qt.CheckState.Checked)

    def onHotkeyChecked(self):
        if self.hotkey.isChecked():
            self.switch.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.switch.setCheckState(Qt.CheckState.Checked)
        self.enableHotKey(self.hotkey.isChecked())

    def onTriggerHotKey(self):
        self.bringToFront()
        text = ""
        try:
            text = os.popen('xsel').read()
        except Exception as e:
            self.input.setText(str(e))
        self.doTranslation(text)

    def enableHotKey(self, enable:bool):
        try:
            if enable:
                keybinder.register_hotkey(self.window_.winId(), self.hotkeyCombo,self.onTriggerHotKey)
            else:
                keybinder.unregister_hotkey(self.window_.winId(), self.hotkeyCombo)
        except Exception as e:
            print(e)
            
    def doTranslation(self, text):
        if type(text) is str:
            content = str(text)
            self.input.setText(content)
            translation = ""
            if self.baidu.isChecked():
                translation = baidudict.getTranslate(content)
            elif self.youdao.isChecked():
                translation = youdao2.getTranslate(content)
            self.output.setText(translation)

    def onClipboradChanged(self):
        if not self.switch.isChecked():
            return
        clipboard = QApplication.clipboard()
        self.doTranslation(clipboard.text())

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

    def bringToFront(self):  #还有点问题
        if not self.alwaysOnTop.isChecked():
            window = self.window_
            savedGeometry = QRect(window.geometry())
            print("hello world " + str(window.isActiveWindow()) + ", " + str(savedGeometry))
            window.hide()
            window.setWindowState((window.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive)
            window.move(savedGeometry.left(), savedGeometry.top() + window.statusBar().height())
            window.show()
            window.raise_()
            window.activateWindow()