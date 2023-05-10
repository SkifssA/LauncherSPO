from tkinter.messagebox import showerror
import tkinter
from customtkinter import *
from ReJ import AvtoJ
import ListOfDisciplines
from importlib import reload
from Calendar import Calendar

'''Фрейм списка групп'''


class GroupFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = None
        self.check_var = [[], []]

    '''Удаление всех групп с таблицы'''

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


'''Виджет выбора отображения теории или практики'''


class TabView(CTkTabview):
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

    '''Создание перечисления с группами'''

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

    '''Функция кнопки(Авторизация)'''

    def work_login_form(self, login, password):
        if self.sessoin.login(login, password):  # Если авторизация прошла успешно
            if self.check_var.get() == 'on':
                print('='*20)
                with open('cash', 'r+') as f:
                    print(f'{login};{password}', file=f)
            self.sessoin.save_file_disc()
            reload(ListOfDisciplines)
            self.destroy()
        else:
            # Сообщение об ошибке
            showerror(title="Ошибка авторизации", message="Неправильный логин или пароль")


'''Основное приложение'''


class APP(CTk):
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

    '''Основная функция отрисовки виджетов'''

    def main_frame(self):
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
        self.frame.grid()


if __name__ == '__main__':
    APP()
