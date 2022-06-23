import json
import pathlib
import sys
import time

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QKeySequence, QIcon

from tkinter import Tk, Frame, Label, Entry, Button, X, W, LEFT, RIGHT
from tkinter import messagebox

import random

import threading

import win32gui
import win32con
import win32api

url = "https://universe.flyff.com/play"
icon = "icons/PyFlyff.ico"

default_user_agent = "None"

ftool_activation_key = ""
ftool_in_game_key = ""

alt_control_activation_key = ""
alt_control_ingame_key = ""

window_name = ""
hwndMain = ""
hwndAlt = ""
user_agent = ""

repeat_times = 0
interval = 0

start_ftool_loop = False
alt_control_boolean = False
toolbar_window = False

ftool_json_file = "FToolConfig.json"
ftool_json_file_location = pathlib.Path(ftool_json_file)

alt_control_json_file = "AltControl.json"
alt_control_json_file_location = pathlib.Path(alt_control_json_file)

user_agent_json_file = "UserAgent.json"
user_agent_json_file_location = pathlib.Path(user_agent_json_file)

vk_code = {'backspace': 0x08,
           'tab': 0x09,
           'clear': 0x0C,
           'enter': 0x0D,
           'shift': 0x10,
           'ctrl': 0x11,
           'alt': 0x12,
           'pause': 0x13,
           'caps_lock': 0x14,
           'esc': 0x1B,
           'spacebar': 0x20,
           'page_up': 0x21,
           'page_down': 0x22,
           'end': 0x23,
           'home': 0x24,
           'left_arrow': 0x25,
           'up_arrow': 0x26,
           'right_arrow': 0x27,
           'down_arrow': 0x28,
           'select': 0x29,
           'print': 0x2A,
           'execute': 0x2B,
           'print_screen': 0x2C,
           'ins': 0x2D,
           'del': 0x2E,
           'help': 0x2F,
           '0': 0x30,
           '1': 0x31,
           '2': 0x32,
           '3': 0x33,
           '4': 0x34,
           '5': 0x35,
           '6': 0x36,
           '7': 0x37,
           '8': 0x38,
           '9': 0x39,
           'a': 0x41,
           'b': 0x42,
           'c': 0x43,
           'd': 0x44,
           'e': 0x45,
           'f': 0x46,
           'g': 0x47,
           'h': 0x48,
           'i': 0x49,
           'j': 0x4A,
           'k': 0x4B,
           'l': 0x4C,
           'm': 0x4D,
           'n': 0x4E,
           'o': 0x4F,
           'p': 0x50,
           'q': 0x51,
           'r': 0x52,
           's': 0x53,
           't': 0x54,
           'u': 0x55,
           'v': 0x56,
           'w': 0x57,
           'x': 0x58,
           'y': 0x59,
           'z': 0x5A,
           'numpad_0': 0x60,
           'numpad_1': 0x61,
           'numpad_2': 0x62,
           'numpad_3': 0x63,
           'numpad_4': 0x64,
           'numpad_5': 0x65,
           'numpad_6': 0x66,
           'numpad_7': 0x67,
           'numpad_8': 0x68,
           'numpad_9': 0x69,
           'multiply_key': 0x6A,
           'add_key': 0x6B,
           'separator_key': 0x6C,
           'subtract_key': 0x6D,
           'decimal_key': 0x6E,
           'divide_key': 0x6F,
           'F1': 0x70,
           'F2': 0x71,
           'F3': 0x72,
           'F4': 0x73,
           'F5': 0x74,
           'F6': 0x75,
           'F7': 0x76,
           'F8': 0x77,
           'F9': 0x78,
           'F10': 0x79,
           'F11': 0x7A,
           'F12': 0x7B,
           'F13': 0x7C,
           'F14': 0x7D,
           'F15': 0x7E,
           'F16': 0x7F,
           'F17': 0x80,
           'F18': 0x81,
           'F19': 0x82,
           'F20': 0x83,
           'F21': 0x84,
           'F22': 0x85,
           'F23': 0x86,
           'F24': 0x87,
           'num_lock': 0x90,
           'scroll_lock': 0x91,
           'left_shift': 0xA0,
           'right_shift ': 0xA1,
           'left_control': 0xA2,
           'right_control': 0xA3,
           'left_menu': 0xA4,
           'right_menu': 0xA5,
           'browser_back': 0xA6,
           'browser_forward': 0xA7,
           'browser_refresh': 0xA8,
           'browser_stop': 0xA9,
           'browser_search': 0xAA,
           'browser_favorites': 0xAB,
           'browser_start_and_home': 0xAC,
           'volume_mute': 0xAD,
           'volume_Down': 0xAE,
           'volume_up': 0xAF,
           'next_track': 0xB0,
           'previous_track': 0xB1,
           'stop_media': 0xB2,
           'play/pause_media': 0xB3,
           'start_mail': 0xB4,
           'select_media': 0xB5,
           'start_application_1': 0xB6,
           'start_application_2': 0xB7,
           'attn_key': 0xF6,
           'crsel_key': 0xF7,
           'exsel_key': 0xF8,
           'play_key': 0xFA,
           'zoom_key': 0xFB,
           'clear_key': 0xFE,
           '+': 0xBB,
           ',': 0xBC,
           '-': 0xBD,
           '.': 0xBE,
           '/': 0xBF,
           '`': 0xC0,
           ';': 0xBA,
           '[': 0xDB,
           '\\': 0xDC,
           ']': 0xDD,
           "'": 0xDE}


class MainWindow(QMainWindow):
    def __init__(self):

        global user_agent

        super(MainWindow, self).__init__()

        self.browser = QWebEngineView()

        main_profile = QWebEngineProfile("MainProfile", self.browser)
        main_profile.setCachePath("C:/PyFlyff/PyFlyffMain")
        main_profile.setPersistentStoragePath("C:/PyFlyff/PyFlyffMain")
        main_page = QWebEnginePage(main_profile, self.browser)

        self.browser.setPage(main_page)
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)
        self.setWindowTitle("PyFlyff - Main")
        self.setWindowIcon(QIcon(icon))
        self.showMaximized()

        ftool = QAction("Mini FTool", self)
        ftool.triggered.connect(lambda: self.multithreading(self.ftool_config))

        alt_control = QAction("Alt Control", self)
        alt_control.triggered.connect(lambda: self.multithreading(self.alt_control_config))

        clear_keys = QAction("Reset Hotkeys", self)
        clear_keys.triggered.connect(self.reset_hotkeys)

        ua = QAction("Set User Agent", self)
        ua.setToolTip(
            "Change your User Agent to something else if you are having trouble connecting your Google Account/Facebook Account/Apple ID, or connecting to the game as a whole.")
        ua.triggered.connect(lambda: self.multithreading(self.set_user_agent))

        fullscreen = QAction("Fullscreen | Ctrl+Shift+F11", self)
        fullscreen.triggered.connect(lambda: self.fullscreen(MainWindow, menuBar))

        open_alt_client = QAction("Open Alt Client | Ctrl+Shift+PageUp", self)
        open_alt_client.triggered.connect(lambda: self.create_new_window(url, "PyFlyff - Alt"))

        reload_main_client = QAction("Reload Main Client | Ctrl+Shift+F5", self)
        reload_main_client.triggered.connect(lambda: self.browser.setUrl(QUrl(url)))

        flyffipedia = QAction("Flyffipedia", self)
        flyffipedia.triggered.connect(lambda: self.create_new_window("https://flyffipedia.com/", "Flyffipedia"))

        madrigalinside = QAction("Madrigal Inside", self)
        madrigalinside.triggered.connect(
            lambda: self.create_new_window("https://madrigalinside.com/", "Madrigal Inside"))

        flyffulator = QAction("Flyffulator", self)
        flyffulator.triggered.connect(lambda: self.create_new_window("https://flyffulator.com/", "Flyffulator"))

        madrigalmaps = QAction("Madrigal Maps", self)
        madrigalmaps.triggered.connect(lambda: self.create_new_window("https://www.madrigalmaps.com/", "Madrigal Maps"))

        flyffmodelviewer = QAction("Flyff Model Viewer", self)
        flyffmodelviewer.triggered.connect(
            lambda: self.create_new_window("https://flyffmodelviewer.com/", "Flyff Model Viewer"))

        skillulator = QAction("Skillulator", self)
        skillulator.triggered.connect(lambda: self.create_new_window("https://skillulator.com/", "Skillulator"))

        menuBar = self.menuBar()

        tools = menuBar.addMenu("Tools")
        tools.addAction(ftool)
        tools.addAction(alt_control)
        tools.addAction(clear_keys)

        others = menuBar.addMenu("Client")
        others.addAction(ua)
        others.addAction(fullscreen)
        others.addAction(open_alt_client)
        others.addAction(reload_main_client)
        others.setToolTipsVisible(True)

        community = menuBar.addMenu("Community")
        community.addAction(flyffipedia)
        community.addAction(madrigalmaps)
        community.addAction(flyffulator)
        community.addAction(madrigalmaps)
        community.addAction(flyffmodelviewer)
        community.addAction(skillulator)

        self.reload_client = QShortcut(QKeySequence("Ctrl+Shift+F5"), self)
        self.reload_client.activated.connect(lambda: self.browser.setUrl(QUrl(url)))

        self.change_fullscreen = QShortcut(QKeySequence("Ctrl+Shift+F11"), self)
        self.change_fullscreen.activated.connect(lambda: self.fullscreen(MainWindow, menuBar))

        self.new_client = QShortcut(QKeySequence("Ctrl+Shift+PgUp"), self)
        self.new_client.activated.connect(lambda: self.create_new_window(url, "PyFlyff - Alt"))

        self.ftool_key = QShortcut(self)
        self.ftool_key.activated.connect(self.start_ftool)

        self.alt_control_key = QShortcut(self)
        self.alt_control_key.activated.connect(lambda: self.multithreading(self.send_alt_control_command))

        self.windows = []

        try:
            if user_agent_json_file_location.exists():
                with open(user_agent_json_file_location) as js:
                    data = json.load(js)
                    user_agent = data["user_agent"]
        except Exception as e:
            messagebox.showerror("Error", str(e))

        if user_agent == "":
            self.browser.page().profile().setHttpUserAgent(default_user_agent)
        else:
            self.browser.page().profile().setHttpUserAgent(user_agent)

    def create_new_window(self, link, wn):
        self.new_window = QWebEngineView()

        alt_profile = QWebEngineProfile("AltProfile", self.new_window)
        alt_profile.setCachePath("C:/PyFlyff/PyFlyffAlt")
        alt_profile.setPersistentStoragePath("C:/PyFlyff/PyFlyffAlt")
        alt_page = QWebEnginePage(alt_profile, self.new_window)

        self.new_window.setPage(alt_page)
        self.new_window.load(QUrl(link))
        self.new_window.setWindowTitle(wn)
        self.new_window.setWindowIcon(QIcon(icon))
        self.new_window.showMaximized()

        if user_agent == "":
            self.new_window.page().profile().setHttpUserAgent(default_user_agent)
        else:
            self.new_window.page().profile().setHttpUserAgent(user_agent)

        self.windows.append(self.new_window)

    def fullscreen(self, w, bar):
        if w.isFullScreen(self):
            w.showMaximized(self)
            bar.setVisible(True)
        else:
            w.showFullScreen(self)
            bar.setVisible(False)

    def set_short_cut(self, **kwargs):

        config = kwargs.get("config")
        key = kwargs.get("key")

        if config == "ftool":
            self.ftool_key.setKey(key)
        if config == "altcontrol":
            self.alt_control_key.setKey(key)

    @staticmethod
    def ftool_loop():
        global start_ftool_loop
        global hwndMain
        global ftool_in_game_key

        counter = 0

        try:
            while True:

                if counter < repeat_times and start_ftool_loop is True:

                    win32api.SendMessage(hwndMain, win32con.WM_KEYDOWN, ftool_in_game_key, 0)
                    time.sleep(random.uniform(0.369420, 0.769420))
                    win32api.SendMessage(hwndMain, win32con.WM_KEYUP, ftool_in_game_key, 0)

                    time.sleep(random.uniform(0, interval + 1))

                    counter += 1
                else:
                    start_ftool_loop = False
                    break

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_ftool(self):
        global start_ftool_loop
        global hwndMain
        global window_name

        hwndMain = win32gui.FindWindow(None, "PyFlyff - " + window_name)

        if not start_ftool_loop:
            if ftool_activation_key != "" and ftool_in_game_key != "":
                start_ftool_loop = True
                self.multithreading(self.ftool_loop)
        else:
            start_ftool_loop = False

    def ftool_config(self):

        global ftool_activation_key
        global ftool_in_game_key
        global repeat_times
        global interval
        global toolbar_window

        if not toolbar_window:

            toolbar_window = True

            ftool_config_window = Tk()

            window_width = 250
            window_height = 200

            screen_width = ftool_config_window.winfo_screenwidth()
            screen_height = ftool_config_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            ftool_config_window.geometry("250x200+" + str(int(x)) + "+" + str(int(y)))
            ftool_config_window.minsize(250, 200)
            ftool_config_window.attributes("-topmost", True)
            ftool_config_window.title("Mini Ftool")
            ftool_config_window.iconbitmap(icon)

            def save():
                global ftool_activation_key
                global ftool_in_game_key
                global alt_control_activation_key
                global repeat_times
                global interval
                global window_name
                global vk_code
                global toolbar_window
                global ftool_json_file

                try:
                    if (
                            activation_key_entry.get() and in_game_hotkey_entry.get() and repeat_times_entry.get() and interval_entry.get() and window_entry.get()) == "":
                        messagebox.showerror("Error", "Fields cannot be empty.")
                    elif activation_key_entry.get() == in_game_hotkey_entry.get():
                        messagebox.showerror("Error", "Activation Key and In-game Hotkey must be different.")
                    elif activation_key_entry.get() == alt_control_activation_key:
                        messagebox.showerror("Error",
                                             "Main Client HotKey from Alt Control cannot be the same as the Mini Ftool Activation Key.")
                    else:
                        self.save_config_json(file=ftool_json_file, values=(
                            activation_key_entry.get(), in_game_hotkey_entry.get(), repeat_times_entry.get(),
                            interval_entry.get(), window_entry.get()))

                        ftool_activation_key = activation_key_entry.get()
                        ftool_in_game_key = vk_code.get(in_game_hotkey_entry.get())
                        repeat_times = int(repeat_times_entry.get())
                        interval = float(interval_entry.get())
                        window_name = window_entry.get()

                        self.set_short_cut(config="ftool", key=ftool_activation_key)

                        toolbar_window = False
                        ftool_config_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            frame = Frame()

            frame.pack(fill=X, padx=5, pady=5)

            activation_key_label = Label(frame, text="Activation Key:", width=15, anchor=W)
            activation_key_entry = Entry(frame, width=20)

            in_game_hotkey_label = Label(frame, text="In-game Hotkey:", width=15, anchor=W)
            in_game_hotkey_entry = Entry(frame, width=20)

            repeat_times_label = Label(frame, text="Repeat:", width=15, anchor=W)
            repeat_times_entry = Entry(frame, width=20)

            interval_label = Label(frame, text="Interval:", width=15, anchor=W)
            interval_entry = Entry(frame, width=20)

            window_label = Label(frame, text="Window:", width=15, anchor=W)
            window_entry = Entry(frame, width=20)

            activation_key_label.grid(row=0, column=0, pady=5)
            activation_key_entry.grid(row=0, column=1, pady=5)

            in_game_hotkey_label.grid(row=1, column=0, pady=5)
            in_game_hotkey_entry.grid(row=1, column=1, pady=5)

            repeat_times_label.grid(row=2, column=0, pady=5)
            repeat_times_entry.grid(row=2, column=1, pady=5)

            interval_label.grid(row=3, column=0, pady=5)
            interval_entry.grid(row=3, column=1, pady=5)

            window_label.grid(row=4, column=0, pady=5)
            window_entry.grid(row=4, column=1, pady=5)

            button_save = Button(text="Save", width=10, height=1, command=save)
            button_save.pack()

            try:
                if ftool_json_file_location.exists():
                    with open(ftool_json_file_location) as js:
                        data = json.load(js)

                        activation_key_entry.insert(0, data["activation_key"])
                        in_game_hotkey_entry.insert(0, data["in_game_key"])
                        repeat_times_entry.insert(0, data["repeat_times"])
                        interval_entry.insert(0, data["interval"])
                        window_entry.insert(0, data["window"])

            except Exception as e:
                messagebox.showerror("Error", str(e))

            if window_entry.get() == "":
                window_entry.insert(0, "Main")

            ftool_config_window.wm_protocol("WM_DELETE_WINDOW",
                                            lambda: self.destroy_toolbar_windows(ftool_config_window))
            ftool_config_window.mainloop()

    def alt_control_config(self):

        global alt_control_activation_key
        global alt_control_ingame_key
        global toolbar_window

        if not toolbar_window:

            toolbar_window = True

            alt_control_config_window = Tk()

            window_width = 250
            window_height = 120

            screen_width = alt_control_config_window.winfo_screenwidth()
            screen_height = alt_control_config_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            alt_control_config_window.geometry("250x120+" + str(int(x)) + "+" + str(int(y)))
            alt_control_config_window.minsize(250, 120)
            alt_control_config_window.attributes("-topmost", True)
            alt_control_config_window.title("Alt Control")
            alt_control_config_window.iconbitmap(icon)

            def start():
                global alt_control_activation_key
                global alt_control_ingame_key
                global ftool_activation_key
                global vk_code
                global alt_control_boolean
                global toolbar_window
                global alt_control_json_file

                try:
                    if (main_client_hotkey_entry.get() and alt_client_hotkey_entry.get()) == "":
                        messagebox.showerror("Error", "Fields cannot be empty.")
                    elif main_client_hotkey_entry.get() == alt_client_hotkey_entry.get():
                        messagebox.showerror("Error", "Main Client Hotkey and Alt Client Hotkey must be different.")
                    elif main_client_hotkey_entry.get() == ftool_activation_key:
                        messagebox.showerror("Error",
                                             "Main Client HotKey from Alt Control cannot be the same as the Mini Ftool Activation Key.")
                    else:

                        self.save_config_json(file=alt_control_json_file,
                                              values=(main_client_hotkey_entry.get(), alt_client_hotkey_entry.get()))

                        alt_control_activation_key = main_client_hotkey_entry.get()
                        alt_control_ingame_key = vk_code.get(alt_client_hotkey_entry.get())

                        self.set_short_cut(config="altcontrol", key=alt_control_activation_key)

                        alt_control_boolean = True
                        toolbar_window = False

                        alt_control_config_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            def stop():
                global alt_control_boolean

                alt_control_boolean = False

            frame = Frame()

            frame.pack(fill=X, padx=5, pady=5)

            main_client_hotkey_label = Label(frame, text="Main Client Hotkey:", width=20, anchor=W)
            main_client_hotkey_entry = Entry(frame, width=10)

            alt_client_hotkey_label = Label(frame, text="Alt Client Hotkey:", width=20, anchor=W)
            alt_client_hotkey_entry = Entry(frame, width=10)

            main_client_hotkey_label.grid(row=0, column=0, pady=5)
            main_client_hotkey_entry.grid(row=0, column=1, pady=5)

            alt_client_hotkey_label.grid(row=1, column=0, pady=5)
            alt_client_hotkey_entry.grid(row=1, column=1, pady=5)

            button_start = Button(text="Start", width=10, height=1, command=start)
            button_start.pack(side=LEFT, padx=25)

            button_stop = Button(text="Stop", width=10, height=1, command=stop)
            button_stop.pack(side=RIGHT, padx=25)

            try:
                if alt_control_json_file_location.exists():
                    with open(alt_control_json_file_location) as js:
                        data = json.load(js)

                        main_client_hotkey_entry.insert(0, data["activation_key"])
                        alt_client_hotkey_entry.insert(0, data["in_game_key"])

            except Exception as e:
                messagebox.showerror("Error", str(e))

            alt_control_config_window.wm_protocol("WM_DELETE_WINDOW",
                                                  lambda: self.destroy_toolbar_windows(alt_control_config_window))
            alt_control_config_window.mainloop()

    @staticmethod
    def send_alt_control_command():
        global alt_control_boolean
        global hwndAlt

        if alt_control_boolean and alt_control_ingame_key != "" and alt_control_activation_key != "":
            hwndAlt = win32gui.FindWindow(None, "PyFlyff - Alt")

            win32api.SendMessage(hwndAlt, win32con.WM_KEYDOWN, alt_control_ingame_key, 0)
            time.sleep(0.5)
            win32api.SendMessage(hwndAlt, win32con.WM_KEYUP, alt_control_ingame_key, 0)

    def set_user_agent(self):
        global user_agent
        global toolbar_window

        if not toolbar_window:

            toolbar_window = True

            user_agent_config_window = Tk()

            window_width = 300
            window_height = 130

            screen_width = user_agent_config_window.winfo_screenwidth()
            screen_height = user_agent_config_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            user_agent_config_window.geometry("300x130+" + str(int(x)) + "+" + str(int(y)))
            user_agent_config_window.minsize(300, 130)
            user_agent_config_window.attributes("-topmost", True)
            user_agent_config_window.title("User Agent")
            user_agent_config_window.iconbitmap(icon)

            def save():
                global toolbar_window
                global user_agent_json_file

                try:
                    if user_agent_entry.get() == "":
                        messagebox.showerror("Error", "Field cannot be empty.")
                    else:

                        self.save_config_json(file=user_agent_json_file, values=(user_agent_entry.get(),))

                        toolbar_window = False
                        user_agent_config_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            user_agent_label = Label(user_agent_config_window, text="Set your User Agent below:", width=30)
            user_agent_entry = Entry(user_agent_config_window, width=40)
            restart_label = Label(user_agent_config_window, text="After setting your User Agent, restart the Client.",
                                  width=50)

            user_agent_label.pack(pady=5)
            user_agent_entry.pack(pady=5)
            restart_label.pack(pady=5)

            button_save = Button(text="Save", width=10, height=1, command=save)
            button_save.pack(pady=5)

            user_agent_entry.insert(0, user_agent)

            user_agent_config_window.wm_protocol("WM_DELETE_WINDOW",
                                                 lambda: self.destroy_toolbar_windows(user_agent_config_window))
            user_agent_config_window.mainloop()

    @staticmethod
    def multithreading(function):
        threading.Thread(target=function).start()

    @staticmethod
    def save_config_json(**kwargs):
        global ftool_json_file
        global alt_control_json_file
        global user_agent_json_file

        file = kwargs.get("file")
        values = kwargs.get("values")

        data = ""

        try:
            if file == ftool_json_file:
                data = {"activation_key": values[0], "in_game_key": values[1], "repeat_times": values[2],
                        "interval": values[3], "window": values[4]}
            if file == alt_control_json_file:
                data = {"activation_key": values[0], "in_game_key": values[1]}
            if file == user_agent_json_file:
                data = {"user_agent": values[0]}

            json_data = json.dumps(data)
            save_json = open(file, "w")
            save_json.write(str(json_data))
            save_json.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def destroy_toolbar_windows(window):
        global toolbar_window

        toolbar_window = False
        window.destroy()

    def reset_hotkeys(self):
        global window_name
        global hwndMain
        global hwndAlt
        global alt_control_activation_key
        global ftool_activation_key
        global alt_control_ingame_key
        global ftool_in_game_key
        global start_ftool_loop

        if not start_ftool_loop:
            window_name = ""
            hwndMain = ""
            hwndAlt = ""

            alt_control_activation_key = ""
            ftool_activation_key = ""
            alt_control_ingame_key = ""
            ftool_in_game_key = ""

            self.ftool_key.setKey("")
            self.alt_control_key.setKey("")


app = QApplication(sys.argv)

QApplication.setApplicationName("PyFlyff")

window = MainWindow()

app.exec_()
