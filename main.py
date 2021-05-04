# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PyQt5 import QtWidgets
from mainwindow import *
import sys
from pynput.mouse import Button, Controller
mouse = Controller()
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, Response
from flask_plugin import *

app = Flask(__name__)
from routes import *

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    qtapp = QtWidgets.QApplication([])
    window = MainWindow()

    webapp = ApplicationThread(app)
    webapp.start()

    window.move(0, 0)
    window.show()

    sys.exit(qtapp.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
