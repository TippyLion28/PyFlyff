import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QIcon
import pyautogui
import threading
from tkinter import *
from tkinter import messagebox

url = "https://universe.flyff.com/play"
icon = "icons/flyffu.ico"

key_to_press = ""
repeat_times = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)
        self.setWindowIcon(QIcon(icon))
        self.showMaximized()

        navbar = QToolBar()
        self.addToolBar(navbar)

        auto_hotkey = QAction("Set Auto Hotkey", self)
        auto_hotkey.triggered.connect(lambda: self.multithreading(self.auto_hotkey_config))
        navbar.addAction(auto_hotkey)

        self.reload_client = QShortcut(QKeySequence("Ctrl+Shift+F5"), self)
        self.reload_client.activated.connect(lambda: self.browser.setUrl(QUrl(url)))

        self.change_fullscreen = QShortcut(QKeySequence("Ctrl+Shift+F11"), self)
        self.change_fullscreen.activated.connect(lambda: self.fullscreen(MainWindow))

        self.new_client = QShortcut(QKeySequence("Ctrl+Shift+PgUp"), self)
        self.new_client.activated.connect(self.new_window)

        self.autoKey = QShortcut(self)
        self.autoKey.activated.connect(lambda: self.multithreading(self.auto_key_press))

        self.windows = []

    def set_short_cut(self, shortcut):
        self.autoKey.setKey(shortcut)

    def auto_key_press(self):

        counter = 0

        try:
            while True:

                if counter < repeat_times:
                    pyautogui.press(key_to_press)

                    pyautogui.sleep(2)

                    counter += 1
                else:
                    break
        except Exception as e:
            messagebox.showerror("Error", e)

    def auto_hotkey_config(self):

        window = Tk()
        window.geometry("220x150")
        window.resizable(False, False)
        window.title("Config")
        window.iconbitmap("icons/flyffu.ico")

        def save():
            global key_to_press
            global repeat_times

            try:
                if activate_key_entry.get() == key_pressed_entry.get():
                    messagebox.showerror("Error", "Activate Key and Pressed Key must be different.")
                else:
                    activate_key = activate_key_entry.get()
                    key_to_press = key_pressed_entry.get()
                    repeat_times = int(times_pressed_entry.get())

                    self.set_short_cut(activate_key)

                    window.destroy()
            except Exception as e:
                messagebox.showerror("Error", e)

        frame = Frame()

        frame.pack(fill=X, padx=5, pady=5)

        activate_key_label = Label(frame, text="Activate Key:", width=10, anchor=W)
        activate_key_entry = Entry(frame, width=20)

        key_pressed_label = Label(frame, text="Pressed Key:", width=10, anchor=W)
        key_pressed_entry = Entry(frame, width=20)

        times_pressed_label = Label(frame, text="Repeat:", width=10, anchor=W)
        times_pressed_entry = Entry(frame, width=20)

        activate_key_label.grid(row=0, column=0, pady=5)
        activate_key_entry.grid(row=0, column=1, pady=5)

        key_pressed_label.grid(row=1, column=0, pady=5)
        key_pressed_entry.grid(row=1, column=1, pady=5)

        times_pressed_label.grid(row=2, column=0, pady=5)
        times_pressed_entry.grid(row=2, column=1, pady=5)

        button_save = Button(text="Save", width=10, height=2, command=save)
        button_save.pack()

        window.mainloop()

    def multithreading(self, function):
        threading.Thread(target=function).start()

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
