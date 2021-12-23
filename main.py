# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging

from PyQt5 import QtWidgets

import jqlocalserver
from mainwindow import *
import sys
# from pynput.mouse import Button, Controller
# mouse = Controller()
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, Response
from flask_plugin import *
import jlog

app = Flask(__name__)
from routes import *


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    log = jlog.logging_init("main")
    log.debug("This is main")
    qtapp = QtWidgets.QApplication([])
    window = MainWindow()

    webapp = ApplicationThread(app)
    webapp.start()

    server = jqlocalserver.Server()
    server.dataReceived.connect(window.data_from_route)

    window.move(0, 0)
    window.show()

    sys.exit(qtapp.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
