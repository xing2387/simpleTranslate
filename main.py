#! /usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import time
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
from widgets import MainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.Window 
            # QtCore.Qt.WindowStaysOnTopHint
        )
        self.init()
        self.addClipbordListener()
        print("inited")

    def addClipbordListener(self):
        clipboard = QApplication.clipboard()
        clipboard.dataChanged.connect(self.widget.onClipboradChanged)

    def init(self):
        self.widget = MainWidget(self)
        self.setCentralWidget(self.widget)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle('翻译')
        self.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


# 入口
if __name__ == '__main__':
    main()
