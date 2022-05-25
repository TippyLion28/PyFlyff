import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QIcon

url = "https://universe.flyff.com/play"
icon = "icons/flyffu.ico"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)
        self.setWindowIcon(QIcon(icon))
        self.showMaximized()

        self.reload_client = QShortcut(QKeySequence("Ctrl+Shift+F5"), self)
        self.reload_client.activated.connect(lambda: self.browser.setUrl(QUrl(url)))

        self.change_fullscreen = QShortcut(QKeySequence("Ctrl+Shift+F11"), self)
        self.change_fullscreen.activated.connect(lambda: self.fullscreen(MainWindow))

        self.new_client = QShortcut(QKeySequence("Ctrl+Shift+PgUp"), self)
        self.new_client.activated.connect(self.new_window)

        self.windows = []

    def new_window(self):
        self.nw = QWebEngineView()
        self.nw.load(QUrl(url))
        self.nw.setWindowIcon(QIcon(icon))
        self.nw.showMaximized()

        self.windows.append(self.nw)

    def fullscreen(self, w):
        if w.isFullScreen(self):
            w.showMaximized(self)
        else:
            w.showFullScreen(self)


app = QApplication(sys.argv)

QApplication.setApplicationName("PyFlyff")

window = MainWindow()

app.exec_()
