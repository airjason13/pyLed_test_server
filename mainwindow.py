from PyQt5 import QtWidgets, QtGui, QtCore, QtNetwork
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QRadioButton
from UI.mainwindows import Ui_MainWindow
import usb_utils as usb_utils
from pyqt_worker import *
import jlog
import sys
import logging
log = jlog.logging_init("MainWindow")
from routes import route_set_led_color, route_set_led_br, LED_PAR

class MainWindow(QtWidgets.QMainWindow ):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #self._timer = QTimer(self)
        #self._timer.timeout.connect(self.play)
        #log = jlog.logging_init("MainWindow")
        log.debug("This is MainWindow")
        self.picos = usb_utils.find_pico()
        ("we got %s picos" % len(self.picos))
        if len(self.picos) is not 0:
            self.ui.label_pico_num.setText(str(len(self.picos)) + " controller online")

        for dev in self.picos:
            dev.outep, dev.inep = usb_utils.get_ep(dev)

        for dev in self.picos:
            dev.outep.write("hello".encode())
        self.ui.radioButton_color_red.toggled.connect(self.onRedClicked)
        self.ui.radioButton_color_green.toggled.connect(self.onGreenClicked)
        self.ui.radioButton_color_blue.toggled.connect(self.onBlueClicked)
        self.ui.radioButton_color_white.toggled.connect(self.onWhiteClicked)
        self.ui.radioButton_color_red.click()
        self.ui.verticalSlider.setMinimum(0)
        self.ui.verticalSlider.setMaximum(255)
        self.ui.verticalSlider.sliderReleased.connect(self.onVerticalSlideRelease)
        self.ui.verticalSlider.sliderMoved.connect(self.onVerticalSlideMoved)
        self.ui.label_slider_value.setText("64")
        self.ui.verticalSlider.setValue(64)
        self.ui.textEdit_ledbrilevel.setText("64")
        self.ui.textEdit_ledbrilevel.textChanged.connect(self.ontextChanged)

        self.ui.radioButton_all.toggled.connect(self.onradiobuttonAllClicked)

        self.ui.radioButton_single.toggled.connect(self.onradiobuttonSingleClicked)
        self.ui.textEdit_led_single.setText("1")
        self.ui.radioButton_all.click()

        self.ui.textEdit_led_single.textChanged.connect(self.onledsingleTextChanged)



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
        if(self.ui.radioButton_single.isChecked()):
            #self.ui.textEdit_led_single.setReadOnly(True)
            if len(self.picos) > 0:
                for dev in self.picos:
                    cmd = "led_select: " + self.ui.textEdit_led_single.toPlainText()
                    dev.outep.write(cmd.encode())

    def onradiobuttonAllClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("all led")
            self.ui.textEdit_led_single.setReadOnly(True)
            if len(self.picos) > 0:
                for dev in self.picos:
                    cmd = "led_select: -1"
                    dev.outep.write(cmd.encode())

    def onradiobuttonSingleClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("single led")
            self.ui.textEdit_led_single.setReadOnly(False)
            if len(self.picos) > 0:
                for dev in self.picos:
                    cmd = "led_select: " + self.ui.textEdit_led_single.toPlainText()
                    dev.outep.write(cmd.encode())

    def ontextChanged(self):

        if self.ui.textEdit_ledbrilevel.toPlainText() is not '':
            self.ui.verticalSlider.setValue(int(self.ui.textEdit_ledbrilevel.toPlainText()))
            self.ui.label_slider_value.setText(self.ui.textEdit_ledbrilevel.toPlainText())
            if len(self.picos) > 0:
                for dev in self.picos:
                    cmd = "set_br: " + self.ui.textEdit_ledbrilevel.toPlainText()
                    dev.outep.write(cmd.encode())
        else:
            self.ui.verticalSlider.setValue(0)

    def onVerticalSlideMoved(self):

        value_str = str(self.ui.verticalSlider.value())
        self.ui.label_slider_value.setText(value_str)

    def onVerticalSlideRelease(self):

        self.ui.textEdit_ledbrilevel.setText(str(self.ui.verticalSlider.value()))

    def onRedClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            log.debug("Red")
            route_set_led_color(LED_PAR.COLOR_RED)
            if len(self.picos) > 0:
                for dev in self.picos:
                    dev.outep.write("test_color:red".encode())

    def onBlueClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            log.debug("Blue")
            route_set_led_color(LED_PAR.COLOR_BLUE)
            if len(self.picos) > 0:
                for dev in self.picos:
                    dev.outep.write("test_color:blue".encode())

    def onGreenClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            log.debug("Green")
            route_set_led_color(LED_PAR.COLOR_GREEN)
            if len(self.picos) > 0:
                for dev in self.picos:
                    dev.outep.write("test_color:green".encode())

    def onWhiteClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            log.debug("White")
            route_set_led_color(LED_PAR.COLOR_WHITE)
            if len(self.picos) > 0:
                for dev in self.picos:
                    dev.outep.write("test_color:white".encode())

    def closeEvent(self, event):
        log.debug("closeEvent")
        #server.removeServer(server.fullServerName())

    def __del__(self):
        log.debug("Main window del")
        #server.removeServer(server.fullServerName())

    def data_from_route(self, data):
        log.debug(sys._getframe().f_code.co_name)
        log.debug("data : %s", data)
        """parser color_switch"""
        if data.get('color_switch') is not None:
            log.debug(data.get('color_switch'))
            if "RED" in data.get('color_switch'):
                self.ui.radioButton_color_red.click()
            elif "GREEN" in data.get('color_switch'):
                self.ui.radioButton_color_green.click()
            elif "BLUE" in data.get('color_switch'):
                self.ui.radioButton_color_blue.click()
            elif "WHITE" in data.get('color_switch'):
                self.ui.radioButton_color_white.click()
        if data.get("led_num") is not None:
            log.debug(data.get('led_num'))
            ori_str = data.get('led_num')
            list_ori_str = ori_str.split(",")
            """handle the led_num all first"""
            if 'all' in list_ori_str[0]:
                self.ui.radioButton_all.click()
            else:
                self.ui.radioButton_single.click()
                led_select_str = list_ori_str[1].split(":")
                print("led_select_str:", led_select_str)
                self.ui.textEdit_led_single.setText(led_select_str[1])

        if data.get("set_br") is not None:
            ori_str = data.get('set_br')
            list_ori_str = ori_str.split(":")
            br_str = list_ori_str[1]
            self.ui.verticalSlider.setValue(int(br_str))
            self.ui.textEdit_ledbrilevel.setText(br_str)