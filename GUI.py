import tkinter
from tkinter.messagebox import showerror
from customtkinter import *
import os
from importlib import reload
from Calendar import Calendar
from RPread import CreateRP
from ProgressBar import ProgressBar
from ReJ import AvtoJ
from ExamFrame import Exam

try:
    import ListOfDisciplines
except ModuleNotFoundError:
    with open('ListOfDisciplines.py', 'w') as f:
        f.write('Practice = [\n]\nTheory = [\n]')
    import ListOfDisciplines


class GroupFrame(CTkScrollableFrame):
    '''Фрейм списка групп'''

    def __init__(self, master, prac, **kwargs):
        super().__init__(master, **kwargs)
        self.label = None
        self.check_var = [[], []]
        self.prac = prac

    def all_del(self):
        '''Удаление всех групп с таблицы'''
        for chec in self.check_var[1]:
            chec.destroy()

    def create_group_checkbox(self, group_list, filter):
        '''Создание "галачек" с группами'''
        self.all_del()
        self.check_var = [[], [], []]
        for i, group in enumerate(group_list):
            if group['name'].find(filter) != -1:
                v = group['name'].find('_')
                if group['name'][v - 1:v] != 'в':
                    self.check_var[0].append(tkinter.StringVar())
                    self.check_var[1].append(CTkCheckBox(self, text=group['name'],
                                                         variable=self.check_var[0][-1], onvalue="on", offvalue="off"))
                    self.check_var[1][-1].pack(padx=20, pady=10, anchor='w')
                    self.check_var[2].append(i)

    def all_check(self, on_off):
        '''Метот для выделения всех групп'''
        for check in self.check_var[0]:
            check.set(on_off)

    def get_check_group(self) -> tuple[int]:
        '''Возвращение выделенных групп'''
        for ch in list(
                self.check_var[2][j] for j in range(len(self.check_var[0])) if self.check_var[0][j].get() == 'on'):
            i = 1
            if not self.prac:
                while ListOfDisciplines.Theory[ch]['subject_id'] != ListOfDisciplines.Theory[ch + i]['subject_id']:
                    i += 1
                yield ch
                yield ch + i
            elif ListOfDisciplines.Practice[ch]['name'].find('/2') != -1:
                name = ListOfDisciplines.Practice[ch]['name'][:ListOfDisciplines.Practice[ch]['name'].find('(')]
                name = name[:name.find('_')] + 'в' + name[name.find('_'):]
                while name != ListOfDisciplines.Practice[ch + i]['name']:
                    i += 1
                yield ch
                yield ch + i
            else:
                yield ch


class TabView(CTkTabview):
    '''Виджет выбора отображения теории или практики'''

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.height = 450
        self.width = 700

        # Создание табл

        self.add("Теория")
        self.add("Практика")

        self.frame_pr = GroupFrame(self.tab('Практика'), True, width=self.width, height=self.height)
        self.frame_tr = GroupFrame(self.tab('Теория'), False, width=self.width, height=self.height)
        self.recreate_frame('')

    def recreate_frame(self, filter, today=None):
        '''Создание перечисления с группами'''
        if filter == 'Сегодня':
            self.frame_pr.create_group_checkbox(today[1], '')
            self.frame_pr.pack()

            self.frame_tr.create_group_checkbox(today[0], '')
            self.frame_tr.pack()
        else:
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
                ProgressBar(self, self.sessoin.save_file_disc)
            reload(ListOfDisciplines)
            self.destroy()
        else:
            # Сообщение об ошибке
            showerror(title="Ошибка авторизации", message="Неправильный логин или пароль")


class APP(CTk):
    """Основное приложение"""

    def __init__(self):
        super().__init__()

        print(self.winfo_screenheight() / 1080)
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
            #self.today = self.session.today_list()
            self.main_frame()
            self.mainloop()
        else:
            self.destroy()

    def button_close_open_lesson(self, open, que):
        """Функция для открытия/закрытия занятий"""
        i = 0
        for group_idl in self.tab.frame_tr.get_check_group():
            group = ListOfDisciplines.Theory[group_idl]
            que.put(f"Теория {group['name'][:group['name'].find('_')]}")
            i += self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'], open=open)
        print(i)
        i = 0
        for group_idl in self.tab.frame_pr.get_check_group():
            group = ListOfDisciplines.Practice[group_idl]
            que.put(f"Практика {group['name'][group['name'].find('('):]}")
            i += self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'],
                                                prac='1', open=open)
        print(i)

    def create_student_frame(self):
        """Функция создания формы для явки"""
        tr = tuple(self.tab.frame_tr.get_check_group())
        pr = tuple(self.tab.frame_pr.get_check_group())
        if len(tr) == 2:
            self.studen_frame = Calendar(self, self.session, dics=[ListOfDisciplines.Theory[tr[0]],
                                                                   ListOfDisciplines.Theory[tr[1]]])
            self.frame.grid_forget()
            self.studen_frame.grid()
        elif len(pr) == 1:
            self.studen_frame = Calendar(self, self.session, dics=[ListOfDisciplines.Practice[pr[0]]], prac='1')
            self.frame.grid_forget()
            self.studen_frame.grid()
        elif len(pr) == 2:
            self.studen_frame = Calendar(self, self.session, dics=[ListOfDisciplines.Practice[pr[0]],
                                                                   ListOfDisciplines.Practice[pr[1]]], prac='1')
            self.frame.grid_forget()
            self.studen_frame.grid()
        else:
            showerror(title="Ошибка", message="Надо выбрать 1 группу")

    def create_exam_frame(self):
        tr = tuple(self.tab.frame_tr.get_check_group())
        if len(tr) == 2:
            self.exam_frame = Exam(self, self.session, disc=ListOfDisciplines.Theory[tr[0]],
                                                                   disc2=ListOfDisciplines.Theory[tr[1]])
            self.frame.grid_forget()
            self.exam_frame.root.grid()
        else:
            showerror(title="Ошибка", message="Надо выбрать 1 группу")

    def open_win_rp(self):
        """Открытие окна с рп"""
        tr = tuple(self.tab.frame_tr.get_check_group())
        pr = tuple(self.tab.frame_pr.get_check_group())
        if len(tr) == 0:
            self.rp = CreateRP(self, disc=[ListOfDisciplines.Practice[id] for id in pr], prac='p')
            self.frame.grid_forget()
            self.rp.grid()
        elif len(pr) == 0:
            self.rp = CreateRP(self, disc=[ListOfDisciplines.Theory[id] for id in tr], prac='t')
            self.frame.grid_forget()
            self.rp.grid()
        else:
            showerror(title="Ошибка", message="Надо выбрать только теорию или только практику")

    def save_themes(self, que):
        """Загрузка тем в журнал"""
        for id in self.tab.frame_tr.get_check_group():
            que.put(f"Теория {ListOfDisciplines.Theory[id]['name'][:ListOfDisciplines.Theory[id]['name'].find('_')]}")
            self.session.save_themes(ListOfDisciplines.Theory[id], prac='')
        for id in self.tab.frame_pr.get_check_group():
            que.put(
                f"Практика {ListOfDisciplines.Practice[id]['name'][:ListOfDisciplines.Practice[id]['name'].find('_')]}")
            self.session.save_themes(ListOfDisciplines.Practice[id], prac='1')

    def upload_tabl(self):
        """Обновление журнала"""
        ProgressBar(self, self.session.save_file_disc)
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
        button = CTkButton(self.frame, text='Найти', command=lambda: self.tab.recreate_frame(self.entry.get(),
                                                                                             today=None if self.entry.get() != 'Сегодня' else self.today))
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
        button = CTkButton(self.frame, text='Закрыть занятия',
                           command=lambda: ProgressBar(self, lambda q: self.button_close_open_lesson(False, q)))
        button.grid(row=3, column=1, pady=10, padx=10)
        button = CTkButton(self.frame, text='Проверить явку', command=lambda: self.create_student_frame())
        button.grid(row=2, column=2, pady=10, padx=10)
        button = CTkButton(self.frame, text='Обновить таблицу', command=lambda: self.upload_tabl())
        button.grid(row=3, column=2, pady=10, padx=10)
        button = CTkButton(self.frame, text='Открыть окно для рп', command=lambda: self.open_win_rp())
        button.grid(row=4, column=2, pady=10, padx=10)
        button = CTkButton(self.frame, text='Заполнить темы', command=lambda: ProgressBar(self, self.save_themes))
        button.grid(row=4, column=1, pady=10, padx=10)
        button = CTkButton(self.frame, text='TEST', command=lambda: self.create_exam_frame())
        button.grid(row=4, column=0, pady=10, padx=10)
        self.frame.grid()


if __name__ == '__main__':
    s = CTk()
    set_widget_scaling(s.winfo_screenheight() / 1080)
    s.destroy()
    APP()
