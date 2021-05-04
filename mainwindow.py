from PyQt5 import QtWidgets, QtGui, QtCore, QtNetwork
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QRadioButton
from UI.mainwindows import Ui_MainWindow
import usb_utils as usb_utils
from pyqt_worker import *

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #self._timer = QTimer(self)
        #self._timer.timeout.connect(self.play)

        self.ui.radioButton_color_red.toggled.connect(self.onRedClicked)
        self.ui.radioButton_color_green.toggled.connect(self.onGreenClicked)


        self.ui.radioButton_color_blue.toggled.connect(self.onBlueClicked)
        self.ui.radioButton_color_white.toggled.connect(self.onWhiteClicked)
        self.ui.verticalSlider.setMinimum(0)
        self.ui.verticalSlider.setMaximum(255)
        self.ui.verticalSlider.sliderReleased.connect(self.onVerticalSlideRelease)
        self.ui.verticalSlider.sliderMoved.connect(self.onVerticalSlideMoved)

        self.ui.textEdit_ledbrilevel.textChanged.connect(self.ontextChanged)

        self.ui.radioButton_all.toggled.connect(self.onradiobuttonAllClicked)

        self.ui.radioButton_single.toggled.connect(self.onradiobuttonSingleClicked)
        self.ui.textEdit_led_single.setText("1")
        self.ui.radioButton_all.click()

        self.ui.textEdit_led_single.textChanged.connect(self.onledsingleTextChanged)

        self.picos = usb_utils.find_pico()
        print("we got %s picos" % len(self.picos))
        if len(self.picos) is not 0:
            self.ui.label_pico_num.setText(str(len(self.picos)) + " controller online")

        for dev in self.picos:
            dev.outep, dev.inep = usb_utils.get_ep(dev)

        for dev in self.picos:
            dev.outep.write("hello".encode())

        self.search_pico = usb_utils.find_pico
        self.thread = Worker(method=self.search_pico)
        self.thread.start()
        """self.flask_server_port = flask_server_port
        if self.ipAddress is not None:
            print("self.ipAddress : ", self.ipAddress)

        self.ui.StartHDMIin.clicked.connect(self.startHDMIin)
        self.ui.closeButton.clicked.connect(self.closewindows)
        self.ui.PauseButton.clicked.connect(self.pause)
        self.ui.PauseButton.setEnabled(False)

        self.ui.closeEvent = self.closeEvent

        self.communicate = Communicate()
        self.communicate.route_sig[str].connect(self.test_from_route)
        self.thread = Worker(communicate=self.communicate)
        self.thread.start()"""
    def onledsingleTextChanged(self):
        print("led single num:", self.ui.textEdit_led_single.toPlainText())

    def onradiobuttonAllClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("all led")
            self.ui.textEdit_led_single.setReadOnly(True)

    def onradiobuttonSingleClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("single led")
            self.ui.textEdit_led_single.setReadOnly(False)

    def ontextChanged(self):

        if self.ui.textEdit_ledbrilevel.toPlainText() is not '':
            self.ui.verticalSlider.setValue(int(self.ui.textEdit_ledbrilevel.toPlainText()))
        else:
            self.ui.verticalSlider.setValue(0)

    def onVerticalSlideMoved(self):
        print("onVerticalSlide")
        print("", self.ui.verticalSlider.value())
        self.ui.textEdit_ledbrilevel.setText(str(self.ui.verticalSlider.value()))

    def onVerticalSlideRelease(self):
        print("onVerticalSlide")
        print("", self.ui.verticalSlider.value())
        self.ui.textEdit_ledbrilevel.setText(str(self.ui.verticalSlider.value()))

    def onRedClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Red")

    def onBlueClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Blue")

    def onGreenClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Green")

    def onWhiteClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("White")

    def closeEvent(self, event):
        print("closeEvent")
        """server.removeServer(server.fullServerName())"""

    def __del__(self):
        print("Main window del")
        """server.removeServer(server.fullServerName())"""
