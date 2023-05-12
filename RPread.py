'''
Выбор групп у которых рп одинаковые
Сохранение всего(?)

'''

'''test bild'''
from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror


class Create_RP(CTkFrame):
    """Класс формы для добавление тем"""
    def __init__(self, master, *disc):
        super().__init__(master)

        self.id_group = set(x['id_group'] for x in disc)

        self.tabl = ttk.Treeview(self)
        self.tabl.grid()
        self.tabl['columns'] = ('t', 'c')
        self.tabl.column("#0", width=0, stretch=NO)
        self.tabl.column("t", anchor=CENTER, width=500)
        self.tabl.column("c", anchor=CENTER, width=100)
        self.tabl.bind("<<TreeviewSelect>>", self.item_selected)
        self.tabl.bind("<Button-3>", self.delete_select)

        self.tabl.heading("#0", text="", anchor=CENTER)
        self.tabl.heading("t", text="Тема", anchor=CENTER)
        self.tabl.heading("c", text="Кол-во часов", anchor=CENTER)

        self.entry = [CTkEntry(self, width=500), CTkEntry(self)]
        self.entry[0].grid()
        self.entry[1].grid()

        self.count = 0

        self.button_save = CTkButton(self, text='Добавить тему', command=self.save_in_table)
        self.button_save.grid()

        self.button_save = CTkButton(self, text='Сохранить файл', command=self.save_file)
        self.button_save.grid()

    def save_in_table(self):
        """Добавление темы в таблицу"""
        if self.entry[0].get() != '' and self.entry[1].get() != '' and self.entry[1].get().isdigit():
            self.tabl.insert(parent='', index='end', iid=self.count, text='',
                             values=(self.entry[0].get().replace('\n', ' '), self.entry[1].get()))
            self.entry[0].delete(0, END)
            self.entry[1].delete(0, END)
            self.count += 1
        else:
            showerror(title="Ошибка", message="Неверные значения")

    def save_file(self):
        """Сохранение в файл"""
        for iid in self.tabl.get_children():
            print(self.tabl.item(iid)['values'])

    def item_selected(self, event):
        """Вывод выбраной строки в entry"""
        for selected_item in self.tabl.selection():
            self.entry[0].insert(0, self.tabl.item(selected_item)['values'][0])
            self.entry[1].insert(0, self.tabl.item(selected_item)['values'][1])

    def delete_select(self, event):
        """Удаление выделения"""
        self.tabl.selection_remove(self.tabl.get_children())
        self.entry[0].delete(0, END)
        self.entry[1].delete(0, END)


if __name__ == '__main__':
    root = CTk()
    s = Create_RP(root)
    s.grid()
    root.mainloop()