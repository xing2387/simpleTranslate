# coding=utf-8

import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget, QWidget, QLineEdit, QDateTimeEdit, QVBoxLayout, QHBoxLayout \
        , QGridLayout, QLabel, QCheckBox, QShortcut, QMessageBox
from PyQt5.QtCore import Qt, QDateTime, QRect
from PyQt5.QtGui import QKeySequence
import os
import baidudict
import youdaodict
from pyqtkeybind import keybinder       #全局快捷键

# 应用程序的主Widget
class MainWidget(QWidget):
    def __init__(self, window:QMainWindow):
        super().__init__()
        self.window_ = window
        self.initUI()

    def initUI(self):
        vlayout = QVBoxLayout()
        grid = QGridLayout()
        label1 = QLabel('原文')
        self.input = QTextEdit()
        label2 = QLabel('翻译')
        self.output = QTextEdit()
        self.switch = QCheckBox("剪贴板")
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
        self.alwaysOnTop.stateChanged.connect(lambda: self.setAlwaysOnTop(self.alwaysOnTop))

        grid.addWidget(self.baidu, 2, 3)
        grid.addWidget(self.youdao, 2, 4)
        self.baidu.stateChanged.connect(lambda: self.switchToBaidu())
        self.youdao.stateChanged.connect(lambda: self.switchToYoudao())

        self.hotkeyCombo = "Alt+T"
        self.hotkey = QCheckBox(self.hotkeyCombo)
        self.hotkey.stateChanged.connect(lambda: self.onHotkeyChecked())
        grid.addWidget(self.hotkey, 2, 5)
        self.hotkey.setChecked(True)
        self.onHotkeyChecked()

        vlayout.addLayout(grid)
        vlayout.addStretch(1)
        self.setLayout(vlayout)

    def setAlwaysOnTop(self, checkBox:QCheckBox):
        if checkBox.isChecked():
            self.window_.setWindowFlags(
                self.window_.windowFlags() |
                QtCore.Qt.WindowStaysOnTopHint
            )
        else:
            self.window_.setWindowFlags(
                self.window_.windowFlags() &
                ~QtCore.Qt.WindowStaysOnTopHint
            )
        if not self.window_.isVisible():
            self.window_.setVisible(True)

    def onHotkeyChecked(self):
        self.enableHotKey(self.hotkey.isChecked())

    def onTriggerHotKey(self):
        self.bringToFront()
        text = os.popen('xsel').read()
        self.doTranslation(text)

    def enableHotKey(self, enable:bool):
        if enable:
            keybinder.register_hotkey(self.window_.winId(), self.hotkeyCombo,self.onTriggerHotKey)
        else:
            keybinder.unregister_hotkey(self.window_.winId(), self.hotkeyCombo)
            
    def doTranslation(self, text):
        if type(text) is str:
            content = str(text)
            self.input.setText(content)
            translation = ""
            if self.baidu.isChecked():
                translation = baidudict.getTranslate(content)
            elif self.youdao.isChecked():
                translation = youdaodict.getTranslate(content)
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
        window = self.window_
        savedGeometry = QRect(window.geometry())
        print("hello world " + str(window.isActiveWindow()) + ", " + str(savedGeometry))
        window.hide()
        window.setWindowState((window.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive)
        window.move(savedGeometry.left(), savedGeometry.top() + window.statusBar().height())
        window.show()
        window.raise_()
        window.activateWindow()