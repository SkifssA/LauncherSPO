import tkinter
from tkinter.messagebox import showerror
from customtkinter import *
import os
import ListOfDisciplines
from ReJ import AvtoJ
from importlib import reload
from Calendar import Calendar
from RPread import CreateRP


class GroupFrame(CTkScrollableFrame):
    '''Фрейм списка групп'''

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = None
        self.check_var = [[], []]

    def all_del(self):
        '''Удаление всех групп с таблицы'''
        for chec in self.check_var[1]:
            chec.destroy()

    def create_group_checkbox(self, group_list, filter):
        '''Создание "галачек" с группами'''
        self.all_del()
        self.check_var = [[], []]
        for group in group_list:
            if group['name'].find(filter) != -1:
                self.check_var[0].append(tkinter.StringVar())
                self.check_var[1].append(CTkCheckBox(self, text=group['name'],
                                                     variable=self.check_var[0][-1], onvalue="on", offvalue="off"))
                self.check_var[1][-1].pack(padx=20, pady=10, anchor='w')

    def all_check(self, on_off):
        '''Метот для выделения всех групп'''
        for check in self.check_var[0]:
            check.set(on_off)

    def get_check_group(self):
        '''Возвращение вcех выделенных групп'''
        return tuple(i for i, x in enumerate(self.check_var[0]) if x.get() == 'on')


class TabView(CTkTabview):
    '''Виджет выбора отображения теории или практики'''

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.height = 450
        self.width = 500

        # Создание табл
        self.add("Практика")
        self.add("Теория")

        self.frame_pr = GroupFrame(self.tab('Практика'), width=self.width, height=self.height)
        self.frame_tr = GroupFrame(self.tab('Теория'), width=self.width, height=self.height)
        self.recreate_frame('')

    def recreate_frame(self, filter):
        '''Создание перечисления с группами'''
        self.frame_pr.create_group_checkbox(ListOfDisciplines.Practice, filter)
        self.frame_pr.pack()

        self.frame_tr.create_group_checkbox(ListOfDisciplines.Theory, filter)
        self.frame_tr.pack()

    def all_check_in_tabl(self, name_tabl, on_off):
        '''Выделение всех групп'''
        if name_tabl == 'Практика':
            self.frame_pr.all_check(on_off)
        else:
            self.frame_tr.all_check(on_off)


class LoginForm(CTkToplevel):
    '''Форма авторизации'''

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
            print('файл заново создан')
            open('cash', 'w')
            with open('cash', 'r+') as f:
                l_p = f.read()
                if l_p != '':
                    entry_login.insert(0, l_p[:l_p.index(';')])
                    entry_pass.insert(0, l_p[l_p.index(';') + 1:-1])

        checkbox = CTkCheckBox(master=self, text="Запомнить меня", variable=self.check_var,
                               onvalue="on", offvalue="off")
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
            if not ListOfDisciplines.Theory and not ListOfDisciplines.Practice:
                try:
                    os.mkdir("Themes")
                except FileExistsError:
                    pass
                self.sessoin.save_file_disc()
            reload(ListOfDisciplines)
            self.destroy()
        else:
            # Сообщение об ошибке
            showerror(title="Ошибка авторизации", message="Неправильный логин или пароль")


class APP(CTk):
    """Основное приложение"""

    def __init__(self):
        super().__init__()
        self.studen_frame = None
        set_appearance_mode("Dark")
        set_default_color_theme('blue')
        self.session = AvtoJ()
        self.title('Журнал')
        x = (self.winfo_screenwidth() - 555) / 2
        y = (self.winfo_screenheight() - 720) / 2
        self.geometry("+%d+%d" % (x, y))
        self.resizable(False, False)
        self.frame = None

        LoginForm(self.session)
        if self.session.cookie != '':  # Основная отработка
            self.main_frame()
            self.mainloop()
        else:
            self.destroy()

    def button_close_open_lesson(self, open):
        """Функция для открытия/закрытия занятий"""
        for group_idl in self.tab.frame_tr.get_check_group():
            group = ListOfDisciplines.Theory[group_idl]
            self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'], open=open)
        for group_idl in self.tab.frame_pr.get_check_group():
            group = ListOfDisciplines.Practice[group_idl]
            self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'],
                                           prac='1', open=open)

    def create_student_frame(self):
        """Функция создания формы для явки"""
        tr = self.tab.frame_tr.get_check_group()
        pr = self.tab.frame_pr.get_check_group()
        if len(tr) + len(pr) == 1:
            if len(tr) == 1:
                self.studen_frame = Calendar(self, self.session, dics=ListOfDisciplines.Theory[tr[0]],
                                             dics2=ListOfDisciplines.Theory[tr[0] + 1])
            elif len(pr) == 1:
                if ListOfDisciplines.Practice[pr[0]]['name'].find('/2') != -1:
                    name = ListOfDisciplines.Practice[pr[0]]['name']
                    if name[:name.find('_')] + 'в' == ListOfDisciplines.Practice[pr[0] + 1]['name'][
                                                      :ListOfDisciplines.Practice[pr[0] + 1]['name'].find('_')]:
                        self.studen_frame = Calendar(self, self.session, dics=ListOfDisciplines.Practice[pr[0]],
                                                     dics2=ListOfDisciplines.Practice[pr[0] + 1], prac='1')
                    elif name[:name.find('_')] + 'в' == ListOfDisciplines.Practice[pr[0] + 2]['name'][
                                                        :ListOfDisciplines.Practice[pr[0] + 2]['name'].find('_')]:
                        self.studen_frame = Calendar(self, self.session, dics=ListOfDisciplines.Practice[pr[0]],
                                                     dics2=ListOfDisciplines.Practice[pr[0] + 2], prac='1')
                else:
                    self.studen_frame = Calendar(self, self.session, dics=ListOfDisciplines.Practice[pr[0]], prac='1')
            self.frame.grid_forget()
            self.studen_frame.grid()
        else:
            showerror(title="Ошибка", message="Надо выбрать 1 группу")

    def open_win_rp(self):
        """Открытие окна с рп"""
        tr = self.tab.frame_tr.get_check_group()
        pr = self.tab.frame_pr.get_check_group()
        disc = []
        if len(tr) == 0:
            for id in pr:
                disc.append(ListOfDisciplines.Practice[id])
            prac = 'p'
            self.rp = CreateRP(self, disc=disc, prac=prac)
            self.frame.grid_forget()
            self.rp.grid()
        elif len(pr) == 0:
            for id in tr:
                disc.append(ListOfDisciplines.Theory[id])
            prac = 't'
            self.rp = CreateRP(self, disc=disc, prac=prac)
            self.frame.grid_forget()
            self.rp.grid()
        else:
            showerror(title="Ошибка", message="Надо выбрать только теорию или только практику")

    def save_themes(self):
        """Загрузка тем в журнал"""
        for id in self.tab.frame_tr.get_check_group():
            self.session.save_themes(ListOfDisciplines.Theory[id], prac='')
        for id in self.tab.frame_pr.get_check_group():
            self.session.save_themes(ListOfDisciplines.Practice[id], prac='1')

    def upload_tabl(self):
        """Обновление журнала"""
        self.session.save_file_disc()
        reload(ListOfDisciplines)
        self.tab.destroy()
        self.tab = TabView(self.frame)
        self.tab.grid(row=1, column=0, pady=10, padx=10, columnspan=3)

    def main_frame(self):
        """Основная функция отрисовки виджетов"""
        self.frame = CTkFrame(self)
        self.tab = TabView(self.frame)
        self.studen_frame = None
        self.entry = CTkEntry(self.frame, placeholder_text="Поиск", width=300)
        button = CTkButton(self.frame, text='Найти', command=lambda: self.tab.recreate_frame(self.entry.get()))
        button.grid(row=0, column=2, pady=10, padx=10)
        self.entry.grid(row=0, column=0, pady=10, padx=10, columnspan=2)
        self.tab.grid(row=1, column=0, pady=10, padx=10, columnspan=3)
        button = CTkButton(self.frame, text='Выбрать всё',
                           command=lambda: self.tab.all_check_in_tabl(self.tab.get(), 'on'))
        button.grid(row=2, column=0, pady=10, padx=10)
        button = CTkButton(self.frame, text='Снять всё',
                           command=lambda: self.tab.all_check_in_tabl(self.tab.get(), 'off'))
        button.grid(row=3, column=0, pady=10, padx=10)
        button = CTkButton(self.frame, text='Открыть занятия', command=lambda: self.button_close_open_lesson(True))
        button.grid(row=2, column=1, pady=10, padx=10)
        button = CTkButton(self.frame, text='Закрыть занятия', command=lambda: self.button_close_open_lesson(False))
        button.grid(row=3, column=1, pady=10, padx=10)
        button = CTkButton(self.frame, text='Проверить явку', command=lambda: self.create_student_frame())
        button.grid(row=2, column=2, pady=10, padx=10)
        button = CTkButton(self.frame, text='Обновить таблицу', command=lambda: self.upload_tabl())
        button.grid(row=3, column=2, pady=10, padx=10)
        button = CTkButton(self.frame, text='Открыть окно для рп', command=lambda: self.open_win_rp())
        button.grid(row=4, column=2, pady=10, padx=10)
        button = CTkButton(self.frame, text='Заполнить темы', command=lambda: self.save_themes())
        button.grid(row=4, column=1, pady=10, padx=10)
        self.frame.grid()


if __name__ == '__main__':
    APP()
