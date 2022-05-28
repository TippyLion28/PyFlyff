import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QKeySequence
from PyQt5.QtGui import QIcon

from tkinter import Tk, Frame, Label, Entry, Button, X, W
from tkinter import messagebox

import pyautogui
import threading

url = "https://universe.flyff.com/play"
icon = "icons/flyffu.ico"

key_to_press = ""
repeat_times = 0
break_loop = False


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
        self.new_client.activated.connect(self.create_new_window)

        self.autoKey = QShortcut(self)
        self.autoKey.activated.connect(lambda: self.multithreading(self.auto_key_press))

        self.break_auto_hotkey = QShortcut(QKeySequence("End"), self)
        self.break_auto_hotkey.activated.connect(self.break_the_loop)

        self.windows = []

    def set_short_cut(self, shortcut):
        self.autoKey.setKey(shortcut)

    @staticmethod
    def auto_key_press():
        global break_loop

        counter = 0

        try:
            while True:

                if counter < repeat_times and break_loop is False:
                    pyautogui.press(key_to_press)

                    pyautogui.sleep(2)

                    counter += 1
                else:
                    break_loop = False
                    break
        except Exception as e:
            messagebox.showerror("Error", e)

    @staticmethod
    def break_the_loop():
        global break_loop

        break_loop = True

    def auto_hotkey_config(self):

        hotkey_window_config = Tk()

        window_width = 250
        window_height = 140

        screen_width = hotkey_window_config.winfo_screenwidth()
        screen_height = hotkey_window_config.winfo_screenheight()

        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        hotkey_window_config.geometry("250x140+" + str(int(x)) + "+" + str(int(y)))
        hotkey_window_config.resizable(False, False)
        hotkey_window_config.title("Config")
        hotkey_window_config.iconbitmap("icons/flyffu.ico")

        def save():
            global key_to_press
            global repeat_times

            try:
                if (activation_key_entry.get() and in_game_hotkey_entry.get() and repeat_times_entry.get()) == "":
                    messagebox.showerror("Error", "Fields cannot be empty.")
                elif activation_key_entry.get() == in_game_hotkey_entry.get():
                    messagebox.showerror("Error", "Activate Key and Pressed Key must be different.")
                else:
                    activate_key = activation_key_entry.get()
                    key_to_press = in_game_hotkey_entry.get()
                    repeat_times = int(repeat_times_entry.get())

                    self.set_short_cut(activate_key)

                    hotkey_window_config.destroy()
            except Exception as e:
                messagebox.showerror("Error", e)

        frame = Frame()

        frame.pack(fill=X, padx=5, pady=5)

        activation_key_label = Label(frame, text="Activation Key:", width=15, anchor=W)
        activation_key_entry = Entry(frame, width=20)

        in_game_hotkey_label = Label(frame, text="In-game Hotkey:", width=15, anchor=W)
        in_game_hotkey_entry = Entry(frame, width=20)

        repeat_times_label = Label(frame, text="Repeat:", width=15, anchor=W)
        repeat_times_entry = Entry(frame, width=20)

        activation_key_label.grid(row=0, column=0, pady=5)
        activation_key_entry.grid(row=0, column=1, pady=5)

        in_game_hotkey_label.grid(row=1, column=0, pady=5)
        in_game_hotkey_entry.grid(row=1, column=1, pady=5)

        repeat_times_label.grid(row=2, column=0, pady=5)
        repeat_times_entry.grid(row=2, column=1, pady=5)

        button_save = Button(text="Save", width=10, height=1, command=save)
        button_save.pack()

        hotkey_window_config.mainloop()

    @staticmethod
    def multithreading(function):
        threading.Thread(target=function).start()

    def create_new_window(self):
        self.new_window = QWebEngineView()
        self.new_window.load(QUrl(url))
        self.new_window.setWindowIcon(QIcon(icon))
        self.new_window.showMaximized()

        self.windows.append(self.new_window)

    def fullscreen(self, w):
        if w.isFullScreen(self):
            w.showMaximized(self)
        else:
            w.showFullScreen(self)


app = QApplication(sys.argv)

QApplication.setApplicationName("PyFlyff")

window = MainWindow()

app.exec_()
