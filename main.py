'''test bild'''
import time

from customtkinter import *
import threading

class ProgressBar(CTkToplevel):
    def __init__(self, master, func, txt):
        super().__init__(master)
        CTkLabel(self, text=txt).grid()
        self.thread = threading.Thread(target=func)
        self.thread.start()
        self.start()



    def start(self):
        if not self.thread.is_alive():
            print('='*20)
            self.destroy()
        self.after(100, self.start)






def s():
    time.sleep(300)

q = CTk()
w = ProgressBar(q,s, 'Идёт проверка')
w.grid()
q.mainloop()
