#! /usr/bin/python3
# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from widgets import MainWidget

from pyqtkeybind import keybinder       #全局快捷键
from PyQt5.QtCore import Qt, QAbstractNativeEventFilter, QAbstractEventDispatcher


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        # print("WinEventFilter " + str(keybinder))
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        # print("nativeEventFilter " + str(eventType))
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() |
            Qt.Window 
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
        self.setGeometry(200, 200, 400, 500)
        self.setWindowTitle('翻译')


def main():
    app = QApplication(sys.argv)
    keybinder.init()
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# 入口
if __name__ == '__main__':
    main()
