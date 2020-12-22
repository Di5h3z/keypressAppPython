import tkinter as tk
import keyboard
import multiprocessing
import time


def press_release(topress, interval, press_release_close):
    while not press_release_close.is_set():
        keyboard.press_and_release(topress)
        time.sleep(interval)
    exit(0)


def key_check_process(start, quit, topress, interval, key_check_close):
    while not key_check_close.is_set():
        if keyboard.is_pressed(start):
            press_release_close = multiprocessing.Event()
            press_process = multiprocessing.Process(target=press_release, args=(topress, interval, press_release_close),
                                                    daemon=True)

            press_process.start()

            while not keyboard.is_pressed(quit) and not key_check_close.is_set():
                time.sleep(.01)

            press_release_close.set()
            while press_process.is_alive():
                pass
            press_process.close()
            press_release_close.clear()

        else:
            time.sleep(.01)

    exit(0)


class keypressApp():
    key_check_close = multiprocessing.Event()
    startkey = "|"
    quitkey = "q"
    topress = "1"
    interval = .1

    def __init__(self):
        self.window = tk.Tk()
        self.initialize_widgets()

        self.start_keycheck()
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.mainloop()

    def close_window(self):
        self.close_keycheck()
        self.window.destroy()

    def set_quitkey(self, event):
        newkey = keyboard.read_key(suppress=True)
        self.quitkey = newkey
        event.widget["text"] = newkey

        self.close_keycheck()
        self.start_keycheck()
        # restart process after updating references

    def set_startkey(self, event):
        newkey = keyboard.read_key(suppress=True)
        self.startkey = newkey
        event.widget["text"] = newkey

        self.close_keycheck()
        self.start_keycheck()
        # restart process after updating references

    def set_presskey(self, event):
        newkey = keyboard.read_key(suppress=True)
        self.topress = newkey
        event.widget["text"] = newkey

        self.close_keycheck()
        self.start_keycheck()
        # restart process after updating references

    def initialize_widgets(self):
        quitkeylabel = tk.Label(master=self.window, text="Press to set Quit")
        quitset = tk.Button(master=self.window, text="q")
        quitset.grid(row=0, column=1)
        quitkeylabel.grid(row=0, column=0)

        startkeylabel = tk.Label(master=self.window, text="Press to set Start")
        startset = tk.Button(master=self.window, text="|")
        startset.grid(row=1, column=1)
        startkeylabel.grid(row=1, column=0)

        topresslabel = tk.Label(master=self.window, text="Press to set key")
        topress = tk.Button(master=self.window, text="1")
        topress.grid(row=2, column=1)
        topresslabel.grid(row=2, column=0)

        quitset.bind("<Button-1>", self.set_quitkey)
        startset.bind("<Button-1>", self.set_startkey)
        topress.bind("<Button-1>", self.set_presskey)

    def close_keycheck(self):
        self.key_check_close.set()
        while self.keycheck.is_alive():
            pass
        self.keycheck.close()
        self.key_check_close.clear()
        # closing the keycheck process

    def start_keycheck(self):
        self.keycheck = multiprocessing.Process(target=key_check_process,
                                                args=(self.startkey, self.quitkey, self.topress, self.interval,
                                                      self.key_check_close))
        self.keycheck.start()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    keypressApp()

