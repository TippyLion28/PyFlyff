import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://universe.flyff.com/play"))
        self.setCentralWidget(self.browser)
        self.setWindowIcon(QIcon("icons/flyffu.ico"))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized()


app = QApplication(sys.argv)

QApplication.setApplicationName("PyFlyff")

window = MainWindow()

app.exec_()
