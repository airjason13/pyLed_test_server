from PyQt5 import QtWidgets, QtGui, QtCore, QtNetwork
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel, QRadioButton
from PyQt5.QtCore import QStringListModel
from UI.mainwindows import Ui_MainWindow
import usb_utils as usb_utils
from pyqt_worker import *

import sys
import log_utils

log = log_utils.logging_init(__file__)

from routes import route_set_led_color, route_set_led_br, LED_PAR
import threading
qmut = threading.Lock()

class MainWindow(QtWidgets.QMainWindow ):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mutex = qmut
        #self._timer = QTimer(self)
        #self._timer.timeout.connect(self.play)
        #log = jlog.logging_init("MainWindow")
        log.debug("This is MainWindow")
        self.picos = usb_utils.find_pico()
        log.debug("we got %s picos" % len(self.picos))
        if len(self.picos) != 0:
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

        self.ui.radioButton_normalmode.toggled.connect(self.onradiobuttonNormalModeClicked)
        self.ui.radioButton_areamode.toggled.connect(self.onradiobuttonAreaModeClicked)
        self.ui.btn_area_mode_params_confirm.clicked.connect(self.onpushbuttonAreaParamsConfirm)

        self.ui.textEdit_led_single.setText("1")
        self.ui.radioButton_all.click()
        self.ui.radioButton_normalmode.click()

        self.ui.textEdit_led_single.textChanged.connect(self.onledsingleTextChanged)



        self.search_pico = self.search_pico
        self.thread = Worker(method=self.search_pico)
        self.thread.start()

    def search_pico(self):

        self.mutex.acquire()
        #log.debug("search_pico")
        #print("num of self.picos: ", len(self.picos))
        if len(self.picos) is 0:
            self.picos = usb_utils.find_pico()
            if len(self.picos) != 0:
                self.ui.label_pico_num.setText(str(len(self.picos)) + " controller online")
                for dev in self.picos:
                    dev.outep, dev.inep = usb_utils.get_ep(dev)
        else:
            tmp_picos = usb_utils.find_pico()
            #print("num of tmp_picos: ", len(tmp_picos))
            if len(tmp_picos) == 0:
                self.picos = []

                self.ui.label_pico_num.setText("Zero controller online")
            elif len(tmp_picos) == len(self.picos):
                log.debug("no changed")
            else:
                log.debug("num of picos changed")
                #print(tmp_picos)

        #log.debug("search_pico out")
        self.mutex.release()

    def onledsingleTextChanged(self):
        print("led single num:", self.ui.textEdit_led_single.toPlainText())
        if(self.ui.radioButton_single.isChecked()):
            #self.ui.textEdit_led_single.setReadOnly(True)
            cmd = "led_select: " + self.ui.textEdit_led_single.toPlainText()

            self.send_pico_cmd(cmd)
            """self.mutex.acquire()
            if len(self.picos) > 0:
                for dev in self.picos:
                    cmd = "led_select: " + self.ui.textEdit_led_single.toPlainText()
                    dev.outep.write(cmd.encode())
            self.mutex.release()"""

    def onradiobuttonAllClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            #print("all led")
            self.ui.textEdit_led_single.setReadOnly(True)
            cmd = "led_select: -1"
            self.send_pico_cmd(cmd)
            """self.mutex.acquire()
            if len(self.picos) > 0:
                for dev in self.picos:
                    cmd = "led_select: -1"
                    dev.outep.write(cmd.encode())
            self.mutex.release()"""

    def onradiobuttonSingleClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            #print("single led")
            self.ui.textEdit_led_single.setReadOnly(False)
            cmd = "led_select: " + self.ui.textEdit_led_single.toPlainText()
            self.send_pico_cmd(cmd)
            """self.mutex.acquire()
            if len(self.picos) > 0:
                for dev in self.picos:
                    cmd = "led_select: " + self.ui.textEdit_led_single.toPlainText()
                    dev.outep.write(cmd.encode())
            self.mutex.release()"""

    def onradiobuttonNormalModeClicked(self):
        log.debug("")
        self.ui.edit_led_total_width.setDisabled(True)
        self.ui.edit_led_total_height.setDisabled(True)
        self.ui.edit_area_startx.setDisabled(True)
        self.ui.edit_area_starty.setDisabled(True)
        self.ui.edit_area_width.setDisabled(True)
        self.ui.edit_area_height.setDisabled(True)

    def onradiobuttonAreaModeClicked(self):
        log.debug("")
        self.ui.edit_led_total_width.setDisabled(False)
        self.ui.edit_led_total_height.setDisabled(False)
        self.ui.edit_area_startx.setDisabled(False)
        self.ui.edit_area_starty.setDisabled(False)
        self.ui.edit_area_width.setDisabled(False)
        self.ui.edit_area_height.setDisabled(False)

    def onpushbuttonAreaParamsConfirm(self):
        log.debug("")

    def ontextChanged(self):

        if self.ui.textEdit_ledbrilevel.toPlainText() is not '':
            self.ui.verticalSlider.setValue(int(self.ui.textEdit_ledbrilevel.toPlainText()))
            self.ui.label_slider_value.setText(self.ui.textEdit_ledbrilevel.toPlainText())
            cmd = "set_br: " + self.ui.textEdit_ledbrilevel.toPlainText()
            self.send_pico_cmd(cmd)
            """self.mutex.acquire()
            if len(self.picos) > 0:
                for dev in self.picos:
                    cmd = "set_br: " + self.ui.textEdit_ledbrilevel.toPlainText()
                    dev.outep.write(cmd.encode())
            self.mutex.release()"""
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
            self.send_pico_cmd("test_color:red")

    def onBlueClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            log.debug("Blue")
            route_set_led_color(LED_PAR.COLOR_BLUE)
            self.send_pico_cmd("test_color:blue")

    def onGreenClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            log.debug("Green")
            route_set_led_color(LED_PAR.COLOR_GREEN)
            self.send_pico_cmd("test_color:green")

    def onWhiteClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            log.debug("White")
            route_set_led_color(LED_PAR.COLOR_WHITE)
            self.send_pico_cmd("test_color:white")

    def closeEvent(self, event):
        log.debug("closeEvent")
        #server.removeServer(server.fullServerName())

    def send_pico_cmd(self, cmd_str):
        self.mutex.acquire()
        try:
            if len(self.picos) > 0:
                for dev in self.picos:
                    dev.outep.write(cmd_str.encode())
        except:
            log.error("send_pico_cmd error")
        self.mutex.release()

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