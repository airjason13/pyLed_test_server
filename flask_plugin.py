from PyQt5 import QtCore
from global_def import *
import log_utils

log = log_utils.logging_init(__file__)


class ApplicationThread(QtCore.QThread):
    def __init__(self, application, port=flask_server_port):
        super(ApplicationThread, self).__init__()
        self.application = application
        self.port = port

    def __del__(self):
        self.wait()

    def run(self):
        log.debug("flask start to run")
        try:
            self.application.run(debug=False, host='0.0.0.0', port=self.port, threaded=True)
        finally:
            log.debug("flask End!")
