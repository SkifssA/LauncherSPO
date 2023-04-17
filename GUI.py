from tkinter.messagebox import showerror
import tkinter
from customtkinter import *
from ReJ import AvtoJ
import ListOfDisciplines
from importlib import reload
from threading import Thread
from datetime import *




'''Форма для проверки явки'''


class StudentFrame(CTkScrollableFrame):
    def __init__(self, master, session, dics, prac, **kwargs):
        super().__init__(master, **kwargs)
        self.session = session
        self.disc = dics
        self.prac = prac
        self.rows = session.student_rows(dics['id_group'], dics['subject_id'], prac=self.prac,
                                         date_from=datetime.today().strftime('%d.%m.%Y'))['rows']
        self.disc2 = None
        self.rows2 = None
        self.value_combobox = ['', 'Н', 'Б', 'У', 'О']
        self.combo = []
        self.label = []
        for j, i in enumerate(self.rows):
            self.student_lesson(i, j)

    def add_v_group(self, dics):
        self.disc2 = dics
        self.rows2 = self.session.student_rows(dics['id_group'], dics['subject_id'], prac=self.prac,
                                         date_from=datetime.today().strftime('%d.%m.%Y'))['rows']
        for j, i in enumerate(self.rows2):
            self.student_lesson(i, j+len(self.rows))

    '''Метод создания явки на 1 студента'''

    def student_lesson(self, student, j):
        self.label.append(CTkLabel(self, text=student['student_name']))
        self.label[-1].grid(row=j, column=0, padx=20, pady=5)
        self.combo.append([])
        for i, n in enumerate(student['lessons']):
            self.combo[-1].append(
                CTkOptionMenu(self, values=self.value_combobox, width=50, command=lambda x: self.p(j, x)))
            self.combo[-1][-1].grid(row=j, column=i + 1, padx=5, pady=5)
            self.combo[-1][-1].set(n['attendance']['value'])

    '''Метод проставления значений студенту до конца занятий'''

    def p(self, j, x):
        if x != 'О':
            set_box = False
            for box in self.combo[j]:
                if box.get() == x:
                    set_box = True
                elif set_box:
                    box.set(x)

    '''Выставление явки в журнал'''

    def turnout(self):
        n = len(self.rows)
        for id_student, student in enumerate(self.combo[:n]):
            for id_lesson, lesson in enumerate(student):
                if lesson.get() != '':
                    self.session.setting_turnout(self.disc['id_group'], self.disc['subject_id'],
                                                 self.rows[id_student]['student_id'],
                                                 self.rows[id_student]['lessons'][id_lesson]['id'], lesson.get(),
                                                 prac=self.prac)
        if self.rows2 is not None:
            for id_student, student in enumerate(self.combo[n:]):
                for id_lesson, lesson in enumerate(student):
                    if lesson.get() != '':
                        self.session.setting_turnout(self.disc2['id_group'], self.disc2['subject_id'],
                                                     self.rows2[id_student]['student_id'],
                                                     self.rows2[id_student]['lessons'][id_lesson]['id'], lesson.get(),
                                                     prac=self.prac)


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
        print('=' * 20)
        self.sessoin.save_file_disc()
        reload(ListOfDisciplines)
        self.destroy()


'''Фрейм списка групп'''


class GroupFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = None
        self.check_var = [[], []]

    def all_del(self):
        for chec in self.check_var[1]:
            chec.destroy()

    '''Создание "галачек" с группами'''

    def create_group_checkbox(self, group_list, filter):
        self.all_del()
        self.check_var = [[], []]
        # add widgets onto the frame...
        for group in group_list:
            if group['name'].find(filter) != -1:
                self.check_var[0].append(tkinter.StringVar())
                self.check_var[1].append(CTkCheckBox(self, text=group['name'],
                                                     variable=self.check_var[0][-1], onvalue="on", offvalue="off"))
                self.check_var[1][-1].pack(padx=20, pady=10, anchor='w')

    '''Метот для выделения всех групп'''

    def all_check(self, on_off):
        for check in self.check_var[0]:
            check.set(on_off)

    '''Возвращение вcех выделенных групп'''

    def get_check_group(self):
        return tuple(i for i, x in enumerate(self.check_var[0]) if x.get() == 'on')


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
        self.frame_tr = GroupFrame(self.tab('Теория'), width=self.width, height=self.height)
        self.recreate_frame('')

    def recreate_frame(self, filter):
        self.frame_pr.create_group_checkbox(ListOfDisciplines.Practice, filter)
        self.frame_pr.pack()

        self.frame_tr.create_group_checkbox(ListOfDisciplines.Theory, filter)
        self.frame_tr.pack()

    '''Выделение всех групп'''

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
        self.studen_frame = None
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
            #ProgressForm(self.session)

            self.degin_I()
            self.mainloop()
        else:
            self.destroy()

    '''Функция для открытия/закрытия занятий'''

    def button_close_open_lesson(self, open):
        for group_idl in self.tab.frame_tr.get_check_group():
            group = ListOfDisciplines.Theory[group_idl]
            self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'], open=open)
        for group_idl in self.tab.frame_pr.get_check_group():
            group = ListOfDisciplines.Practice[group_idl]
            self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'],
                                           prac='1', open=open)

    '''Функция создания формы для явки'''

    def create_student_frame(self):
        tr = self.tab.frame_tr.get_check_group()
        pr = self.tab.frame_pr.get_check_group()
        if len(tr) + len(pr) == 1:
            if len(tr) == 1:
                self.studen_frame = StudentFrame(self, self.session, ListOfDisciplines.Theory[tr[0]], '', width=610,
                                                 height=500)
                self.studen_frame.add_v_group(ListOfDisciplines.Theory[tr[0]+1])
            elif len(pr) == 1:
                self.studen_frame = StudentFrame(self, self.session, ListOfDisciplines.Practice[pr[0]], '1', width=610,
                                                 height=500)

                if ListOfDisciplines.Practice[pr[0]]['name'].find('/2') != -1:
                    self.studen_frame.add_v_group(ListOfDisciplines.Practice[pr[0] + 1])
            self.studen_frame.grid(row=0, column=3, pady=10, padx=10, columnspan=3)

            self.studen_frame.grid(row=1, column=3, pady=10, padx=10, columnspan=3)

        else:
            showerror(title="Ошибка", message="Надо выбрать 1 группу")



    '''Основная функция отрисовки виджетов'''

    def degin_I(self):
        self.tab = TabView(self)
        self.studen_frame = None
        self.entry = CTkEntry(self, placeholder_text="Поиск", width=300)
        button = CTkButton(self, text='Найти', command=lambda: self.tab.recreate_frame(self.entry.get()))
        button.grid(row=0, column=2, pady=10, padx=10)
        self.entry.grid(row=0, column=0, pady=10, padx=10, columnspan=2)
        self.tab.grid(row=1, column=0, pady=10, padx=10, columnspan=3)
        button = CTkButton(self, text='Выбрать всё', command=lambda: self.tab.all_check_in_tabl(self.tab.get(), 'on'))
        button.grid(row=2, column=0, pady=10, padx=10)
        button = CTkButton(self, text='Снять всё', command=lambda: self.tab.all_check_in_tabl(self.tab.get(), 'off'))
        button.grid(row=3, column=0, pady=10, padx=10)
        button = CTkButton(self, text='Открыть занятия', command=lambda: self.button_close_open_lesson(True))
        button.grid(row=2, column=1, pady=10, padx=10)
        button = CTkButton(self, text='Закрыть занятия', command=lambda: self.button_close_open_lesson(False))
        button.grid(row=3, column=1, pady=10, padx=10)
        button = CTkButton(self, text='Проверить явку', command=lambda: self.create_student_frame())
        button.grid(row=2, column=2, pady=10, padx=10)
        button = CTkButton(self, text='Сохранить явку', command=lambda: self.studen_frame.turnout())
        button.grid(row=3, column=2, pady=10, padx=10)



if __name__ == '__main__':
    APP()



