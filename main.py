import sys

import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import parsing


UI = './gui.ui'
URL = "https://kyounghwankim.github.io"


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.SetUI()
        self.SetThread()
        self.SetSlot()

        self.Cnt = [0, 0, 0, 0]

    def SetUI(self):
        uic.loadUi(UI, self)


    def SetSlot(self):
        self.Start.clicked.connect(self.Parsing_Module.GetData)


    def SetThread(self):
        self.Parsing_Module_Thread = QThread()
        self.Parsing_Module_Thread.start()

        self.Parsing_Module = parsing.Parsing(URL)
        self.Parsing_Module.moveToThread(self.Parsing_Module_Thread)

        self.Parsing_Module.Signal_Data.connect(self.AddData)


    @pyqtSlot(int, str)
    def AddData(self, cmd, data):
        self.Cnt[cmd - 1] += 1
        if cmd == 1:
            self.InternalLink.addItem(data)
            self.InternalCnt.setText(str(self.Cnt[cmd - 1]))
        elif cmd == 2:
            self.ExternalLink.addItem(data)
            self.ExternalCnt.setText(str(self.Cnt[cmd - 1]))
        elif cmd == 3:
            self.JavaScript.addItem(data)
            self.JavaScriptCnt.setText(str(self.Cnt[cmd - 1]))
        elif cmd == 4:
            self.Resources.addItem(data)
            self.ResourcesCnt.setText(str(self.Cnt[cmd - 1]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    app.exec_()