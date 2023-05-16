from customtkinter import *
from queue import Queue
import threading


class ProgressBar(CTkToplevel):
    """Окно загрузки"""

    def __init__(self, master, func):
        super().__init__(master)
        self.string = StringVar()
        self.attributes('-disabled', True)

        CTkLabel(self, text='Подождите идёт загрузка', justify=CENTER, width=210).grid()
        CTkLabel(self, textvariable=self.string, justify=CENTER, width=210).grid()

        self.title('')
        x = (self.winfo_screenwidth() - 210) / 2
        y = (self.winfo_screenheight() - 200) / 2
        self.geometry("210x200+%d+%d" % (x, y))

        self.que = Queue()
        self.thread = threading.Thread(target=func, args=(self.que,))
        self.thread.start()

        self.start()
        self.grab_set()
        self.wait_window()

    def start(self):
        """Обработка загрузки и автоматическое закрытие окна при её окончании"""
        if not self.thread.is_alive():
            self.destroy()
        try:
            self.string.set(self.que.get(block=False))
        except:
            pass
        self.after(500, self.start)
