from PyQt5 import QtWidgets, QtGui, QtCore, QtNetwork
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QThread
import json

SERVER = "OrHCSZBAQz" #None
def get_server_name():
    global SERVER

    return SERVER

class Server(QtNetwork.QLocalServer):
    dataReceived = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()


        if self.isListening():
            print("listening")
        else:
            print("not listening")

        if self.hasPendingConnections():
            print("has Pending Connections")
        else:
            print("No Pending Connections")

        self.newConnection.connect(self.handleConnection)


        self.removeServer(get_server_name())
        if not self.listen(get_server_name()):
            raise RuntimeError(self.errorString())



    def handleConnection(self):
        data = {}
        socket = self.nextPendingConnection()
        if socket is not None:
            if socket.waitForReadyRead(2000):
                data = json.loads(str(socket.readAll().data(), 'utf-8'))
                socket.disconnectFromServer()
            socket.deleteLater()
        if 'shutdown' in data:
            self.close()
            self.removeServer(self.fullServerName())
            QtWidgets.qApp.quit()
        else:
            self.dataReceived.emit(data)