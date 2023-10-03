import tkinter
from tkinter.messagebox import showerror
from customtkinter import *
from importlib import reload
from ProgressBar import ProgressBar

class LoginForm(CTkToplevel):
    '''Форма авторизации'''

    def __init__(self, session,ListOfDisciplines):
        super().__init__()
        self.sessoin = session
        self.ListOfDisciplines = ListOfDisciplines
        self.check_var = tkinter.StringVar()
        self.check_var.set('on')
        x = (self.winfo_screenwidth() - 210) / 2
        y = (self.winfo_screenheight() - 200) / 2
        self.geometry("+%d+%d" % (x, y))
        self.title('')
        self.resizable(False, False)
        # Создание формы
        self.creat_login_form()
        # Ожидание закрытия окна
        self.grab_set()
        self.wait_window()
        return

    def creat_login_form(self):
        '''Создание формы авторизации'''
        entry_login = CTkEntry(master=self, placeholder_text="login")
        entry_login.pack(padx=20, pady=10)
        entry_pass = CTkEntry(master=self, placeholder_text="password", show='*')
        entry_pass.pack(padx=20, pady=15)
        try:
            with open('cash', 'r+') as f:
                l_p = f.read()
                if l_p != '':
                    entry_login.insert(0, l_p[:l_p.index(';')])
                    entry_pass.insert(0, l_p[l_p.index(';') + 1:-1])
        except IOError:
            open('cash', 'w')
            with open('cash', 'r+') as f:
                l_p = f.read()
                if l_p != '':
                    entry_login.insert(0, l_p[:l_p.index(';')])
                    entry_pass.insert(0, l_p[l_p.index(';') + 1:-1])

        checkbox = CTkCheckBox(master=self, text="Запомнить меня",
                                variable=self.check_var,onvalue="on", offvalue="off")
        checkbox.pack(padx=20, pady=10)
        button = CTkButton(master=self, text="Вход",
                           command=lambda: self.work_login_form(entry_login.get(), entry_pass.get()))
        button.pack(padx=20, pady=10)

    def work_login_form(self, login, password):
        '''Функция кнопки(Авторизация)'''
        if self.sessoin.login(login, password):  # Если авторизация прошла успешно
            if self.check_var.get() == 'on':
                with open('cash', 'r+') as f:
                    print(f'{login};{password}', file=f)
            if not self.ListOfDisciplines.Theory and not self.ListOfDisciplines.Practice:
                try:
                    os.mkdir("Themes")
                except FileExistsError:
                    pass
                ProgressBar(self, self.sessoin.save_file_disc)
            reload(self.ListOfDisciplines)
            self.destroy()
        else:
            # Сообщение об ошибке
            showerror(title="Ошибка авторизации", message="Неправильный логин или пароль")