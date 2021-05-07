from asyncore import loop

from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QThread
from PyQt5 import QtWidgets, QtGui, QtCore, QtNetwork
import time

class Worker(QThread):

    def __init__(self, parent=None, method=None):
        super(Worker, self).__init__(parent)
        self.method = method
        # self.count = 0
        self.loop = loop(method= self.method)

    def run(self):
        #self.loop.methodA()
        while True:
            time.sleep(0.1)
            self.method()


class loop(object):

    def __init__(self, method=None):
        self.count = 0
        self.method = method

    def methodA(self):
        while True:
            time.sleep(3)
            self.method()
