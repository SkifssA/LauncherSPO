from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror
import tkinter.filedialog as fd


class CreateRP(CTkFrame):
    """Класс формы для добавления тем"""

    def __init__(self, master, disc, prac):
        super().__init__(master)

        self.master = master
        self.id_group = sorted(set(x['id_group'] for x in disc))
        self.name_p = disc[-1]['name'][disc[-1]['name'].find('_') + 1:disc[-1]['name'].find('(')]
        self.prac = prac

        CTkLabel(self, text=self.name_p + (' Практика' if self.prac == 'p' else ' Теория'), text_color='white') \
            .grid(row=0, column=0, pady=10, padx=10, columnspan=3)

        self.tabl = ttk.Treeview(self)
        self.tabl.grid(row=1, column=0, columnspan=3)
        self.tabl['columns'] = ('t', 'c')
        self.tabl.column("#0", width=0, stretch=NO)
        self.tabl.column("t", anchor=CENTER, width=650)
        self.tabl.column("c", anchor=CENTER, width=100)

        self.tabl.bind("<<TreeviewSelect>>", self.item_selected)
        self.tabl.bind("<Button-3>", self.delete_select)

        self.tabl.heading("#0", text="", anchor=CENTER)
        self.tabl.heading("t", text="Тема", anchor=CENTER)
        self.tabl.heading("c", text="Кол-во часов", anchor=CENTER)

        self.entry = [CTkEntry(self, width=650,placeholder_text="Введите тему"),
                      CTkEntry(self,width=100,placeholder_text="Введите часы")]
        self.entry[0].grid(row=2, column=0,columnspan=2,sticky='ew')
        self.entry[1].grid(row=2, column=2,sticky='ew')

        self.count = 0
        f = CTkFrame(self)
        CTkButton(f, text='Добавить тему', command=self.save_in_table)\
            .grid(row=0, column=0, pady=10, padx=10)
        CTkButton(f, text='Изменить тему', command=self.modification_in_tabl)\
            .grid(row=0, column=1, pady=10, padx=10)
        CTkButton(f, text='Удалить тему', command=self.delete_in_tabl)\
            .grid(row=0, column=2, pady=10, padx=10)
        CTkButton(f, text='Сохранить файл', command=self.save_file)\
            .grid(row=1, column=0, pady=10, padx=10)
        CTkButton(f, text='Открыть файл', command=self.choose_file)\
            .grid(row=1, column=1, pady=10, padx=10)
        CTkButton(f, text='Назад', command=self.back)\
            .grid(row=1, column=2, pady=10, padx=10)
        f.grid(row=3, column=0, pady=10, padx=10, columnspan=3)

    def back(self):
        """Возврат на начальную форму"""
        self.master.frame.grid()
        self.destroy()

    def save_in_table(self):
        """Добавление темы в таблицу"""
        if self.entry[0].get() != '' and self.entry[1].get() != '' and self.entry[1].get().isdigit():
            self.tabl.insert(parent='', index='end', iid=self.count, text='',
                             values=(self.entry[0].get().replace('\n', ' '), self.entry[1].get().replace('\n', '')))
            self.entry[0].delete(0, END)
            self.entry[1].delete(0, END)
            self.count += 1
        else:
            showerror(title="Ошибка", message="Неверные значения")

    def delete_in_tabl(self):
        """Удаление выделенного элемента"""
        for selected_item in self.tabl.selection():
            self.tabl.delete(selected_item)
        self.entry[0].delete(0, END)
        self.entry[1].delete(0, END)

    def modification_in_tabl(self):
        """Изменение выделенного элемента"""
        if self.entry[0].get() != '' and self.entry[1].get() != '' and self.entry[1].get().isdigit():
            if len(self.tabl.selection()) == 1:
                self.tabl.item(self.tabl.selection(),
                               values=(self.entry[0].get().replace('\n', ' '), self.entry[1].get()))
                self.entry[0].delete(0, END)
                self.entry[1].delete(0, END)
            else:
                showerror(title="Ошибка", message="Нужно выбрать одно значение")
        else:
            showerror(title="Ошибка", message="Неверные значения")

    def save_file(self):
        """Сохранение в файл"""
        with open('Themes/' + self.name_p + self.prac + ' ' + '_'.join(self.id_group) + '.txt', 'w') as f:
            print(sum([int(self.tabl.item(iid)['values'][1]) for iid in self.tabl.get_children()]), file=f)
            for iid in self.tabl.get_children():
                print(self.tabl.item(iid)['values'][0], self.tabl.item(iid)['values'][1], file=f)

    def item_selected(self, event):
        """Вывод выбраной строки в entry"""
        for selected_item in self.tabl.selection():
            self.entry[0].delete(0, END)
            self.entry[1].delete(0, END)
            self.entry[0].insert(0, self.tabl.item(selected_item)['values'][0])
            self.entry[1].insert(0, self.tabl.item(selected_item)['values'][1])

    def delete_select(self, event):
        """Удаление выделения"""
        self.tabl.selection_remove(self.tabl.get_children())
        self.entry[0].delete(0, END)
        self.entry[1].delete(0, END)

    def choose_file(self):
        """Открытия окна с выбором файла"""
        filetypes = (("Текстовый файл", "*.txt"),)
        filename = fd.askopenfilename(title="Открыть файл", initialdir=os.getcwd() + '/Themes',
                                      filetypes=filetypes)
        if filename:
            for iid in self.tabl.get_children():
                self.tabl.delete(iid)
            self.count = 0
            with open(filename) as f:
                f.readline()
                for line in f:
                    self.tabl.insert(parent='', index='end', iid=self.count, text='',
                                     values=(line[:line.rfind(' ')], line[line.rfind(' ') + 1:-1]))
                    self.count += 1


