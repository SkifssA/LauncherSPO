from tkinter.messagebox import showerror
import tkinter
from customtkinter import *
from ReJ import AvtoJ
import ListOfDisciplines
from importlib import reload
from threading import Thread

'''Форма процесса загрузки данных'''


class ProgressForm(CTkToplevel):
    def __init__(self, session):
        super().__init__()
        self.sessoin = session
        x = (self.winfo_screenwidth() - 210) / 2
        y = (self.winfo_screenheight() - 200) / 2
        self.geometry("210x200+%d+%d" % (x, y))
        self.title('')
        self.resizable(False, False)
        self.val = StringVar()
        # Создание формы
        label = CTkLabel(self, text="Идёт загрузка подождите")
        label.pack()
        label = CTkLabel(self, textvariable=self.val)
        label.pack()
        # Ожидание закрытия окна
        th = Thread(target=self.xx)
        th.start()
        self.grab_set()
        self.wait_window()

    def xx(self):
        self.sessoin.save_file_disc()
        reload(ListOfDisciplines)
        self.destroy()


'''Фрейм списка групп'''


class GroupFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = None
        self.check_var = []

    def create_group_checkbox(self, group_list):
        self.check_var = []
        # add widgets onto the frame...
        for group in group_list:
            self.check_var.append(tkinter.StringVar())
            checkbox = CTkCheckBox(self, text=group['name'],
                                   variable=self.check_var[-1], onvalue="on", offvalue="off")
            checkbox.pack(padx=20, pady=10, anchor='w')

    def all_check(self, on_off):
        for check in self.check_var:
            check.set(on_off)

    def get_check_group(self):
        return tuple(i for i, x in enumerate(self.check_var) if x.get() == 'on')


'''Виджет выбора отоброжения теории или практики'''


class TabView(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.height = 500
        self.width = 500

        # Создание табл
        self.add("Практика")
        self.add("Теория")

        self.frame_pr = GroupFrame(self.tab('Практика'), width=self.width, height=self.height)
        self.frame_pr.create_group_checkbox(ListOfDisciplines.Practice)
        self.frame_pr.pack()

        self.frame_tr = GroupFrame(self.tab('Теория'), width=self.width, height=self.height)
        self.frame_tr.create_group_checkbox(ListOfDisciplines.Theory)
        self.frame_tr.pack()

    def all_check_in_tabl(self, name_tabl, on_off):
        if name_tabl == 'Практика':
            self.frame_pr.all_check(on_off)
        else:
            self.frame_tr.all_check(on_off)


'''Форма авторизации'''


class LoginForm(CTkToplevel):
    def __init__(self, session):
        super().__init__()
        self.sessoin = session
        self.check_var = tkinter.StringVar()
        self.check_var.set('on')
        x = (self.winfo_screenwidth() - 210) / 2
        y = (self.winfo_screenheight() - 200) / 2
        self.geometry("210x200+%d+%d" % (x, y))
        self.title('')
        self.resizable(False, False)
        # Создание формы
        self.creat_login_form()
        # Ожидание закрытия окна
        self.grab_set()
        self.wait_window()

    '''Создание формы авторизации'''

    def creat_login_form(self):
        entry_login = CTkEntry(master=self, placeholder_text="login")
        entry_login.pack(padx=20, pady=10)
        entry_pass = CTkEntry(master=self, placeholder_text="password", show='*')
        entry_pass.pack(padx=20, pady=15)
        with open('cash', 'r+') as f:
            l_p = f.read()
            if l_p != '':
                entry_login.insert(0, l_p[:l_p.index(';')])
                entry_pass.insert(0, l_p[l_p.index(';') + 1:])
        checkbox = CTkCheckBox(master=self, text="Запомнить меня", variable=self.check_var,
                               onvalue="on", offvalue="off")
        checkbox.pack(padx=20, pady=10)
        button = CTkButton(master=self, text="Вход",
                           command=lambda: self.work_login_form(entry_login.get(), entry_pass.get()))
        button.pack(padx=20, pady=10)

    '''Функция кнопки(Авторизация)'''

    def work_login_form(self, login, password):
        if self.sessoin.login(login, password):  # Если авторизация прошла успешно
            if self.check_var == 'on':
                with open('cash', 'r+') as f:
                    print(f'{login};{password}', file=f)
            self.destroy()
        else:
            # Сообщение об ошибке
            showerror(title="Ошибка авторизации", message="Неправильный логин или пароль")


'''Основное приложение'''


class APP(CTk):
    def __init__(self):
        super().__init__()
        set_appearance_mode("System")
        set_default_color_theme('blue')
        self.session = AvtoJ()
        self.geometry('1280x720')
        x = (self.winfo_screenwidth() - 1280) / 2
        y = (self.winfo_screenheight() - 720) / 2
        self.geometry("+%d+%d" % (x, y))
        self.resizable(False, False)

        LoginForm(self.session)
        if self.session.cookie != '':  # Основная отработка
            # ProgressForm(self.session)

            self.degin_I()
            self.mainloop()
        else:
            self.destroy()

    def button_close_open_lesson(self, open):
        for group_idl in self.tab.frame_tr.get_check_group():
            group = ListOfDisciplines.Theory[group_idl]
            self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'], open=open)
        for group_idl in self.tab.frame_pr.get_check_group():
            group = ListOfDisciplines.Practice[group_idl]
            self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'],
                                           prac='1', open=open)

    def degin_I(self):
        self.tab = TabView(self)
        self.tab.pack()
        button = CTkButton(self, text='Выбрать всё', command=lambda: self.tab.all_check_in_tabl(self.tab.get(), 'on'))
        button.pack()
        button = CTkButton(self, text='Снять всё', command=lambda: self.tab.all_check_in_tabl(self.tab.get(), 'off'))
        button.pack()
        button = CTkButton(self, text='Открыть занятия', command=lambda: self.button_close_open_lesson(True))
        button.pack()
        button = CTkButton(self, text='Закрыть занятия', command=lambda: self.button_close_open_lesson(False))
        button.pack()
