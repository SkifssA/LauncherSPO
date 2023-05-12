'''
Создание таблицы(?) для ввода темы и кол-во часов
Выбор групп у которых рп одинаковые
Сохранение всего(?)

'''

'''test bild'''
from customtkinter import *
from tkinter import *
from tkinter import ttk

class Create_RP(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.set = ttk.Treeview(self)
        self.set.grid()
        self.set['columns'] = ('t', 'c')
        self.set.column("#0", width=0, stretch=NO)
        self.set.column("t", anchor=CENTER, width=500)
        self.set.column("c", anchor=CENTER, width=100)

        self.set.heading("#0", text="", anchor=CENTER)
        self.set.heading("t", text="Тема", anchor=CENTER)
        self.set.heading("c", text="Кол-во часов", anchor=CENTER)

        self.set.insert(parent='', index='end', iid=0, text='',
                   values=('Основы ООП', '4'))







if __name__ == '__main__':
    root = CTk()
    s = Create_RP(root)
    s.grid()
    root.mainloop()