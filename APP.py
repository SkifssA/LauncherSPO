from tkinter.messagebox import showerror
from customtkinter import *
from importlib import reload
from Calendar import Calendar
from RPread import CreateRP
from ProgressBar import ProgressBar
from ReJ import AvtoJ
from ExamFrame import Exam
from LoginForm import LoginForm
from TabView import TabView


class APP(CTk):
    """Основное приложение"""

    def __init__(self, ListOfDisciplines):
        super().__init__()
        self.ListOfDisciplines = ListOfDisciplines

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

        LoginForm(self.session, self.ListOfDisciplines)
        if self.session.cookie != '':  # Основная отработка
            self.today = self.session.today_list()
            self.main_frame()
            self.mainloop()
        else:
            self.destroy()

    def button_close_open_lesson(self, open, que):
        """Функция для открытия/закрытия занятий"""
        i = 0
        for group_idl in self.tab.frame_tr.get_check_group():
            group = self.ListOfDisciplines.Theory[group_idl]
            que.put(f"Теория {group['name'][:group['name'].find('_')]}")
            i += self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'], open=open)
        i = 0
        for group_idl in self.tab.frame_pr.get_check_group():
            group = self.ListOfDisciplines.Practice[group_idl]
            que.put(f"Практика {group['name'][group['name'].find('('):]}")
            i += self.session.close_open_lesson(group['id_group'], group['subject_id'], group['student_id'],
                                                prac='1', open=open)

    def create_student_frame(self):
        """Функция создания формы для явки"""
        tr = tuple(self.tab.frame_tr.get_check_group())
        pr = tuple(self.tab.frame_pr.get_check_group())
        if len(tr) == 2:
            self.studen_frame = Calendar(self, self.session, dics=[self.ListOfDisciplines.Theory[tr[0]],
                                                                   self.ListOfDisciplines.Theory[tr[1]]])
            self.frame.grid_forget()
            self.studen_frame.grid()
        elif len(pr) == 1:
            self.studen_frame = Calendar(self, self.session, dics=[self.ListOfDisciplines.Practice[pr[0]]], prac='1')
            self.frame.grid_forget()
            self.studen_frame.grid()
        elif len(pr) == 2:
            self.studen_frame = Calendar(self, self.session, dics=[self.ListOfDisciplines.Practice[pr[0]],
                                                                   self.ListOfDisciplines.Practice[pr[1]]], prac='1')
            self.frame.grid_forget()
            self.studen_frame.grid()
        else:
            showerror(title="Ошибка", message="Надо выбрать 1 группу")

    def create_exam_frame(self):
        tr = tuple(self.tab.frame_tr.get_check_group())
        if len(tr) == 2:
            self.exam_frame = Exam(self, self.session, disc=self.ListOfDisciplines.Theory[tr[0]],
                                   disc2=self.ListOfDisciplines.Theory[tr[1]])
            self.frame.grid_forget()
            self.exam_frame.root.grid()
        else:
            showerror(title="Ошибка", message="Надо выбрать 1 группу")

    def open_win_rp(self):
        """Открытие окна с рп"""
        tr = tuple(self.tab.frame_tr.get_check_group())
        pr = tuple(self.tab.frame_pr.get_check_group())
        if len(tr) == 0 and not len(pr) == 0:
            self.rp = CreateRP(self, disc=[self.ListOfDisciplines.Practice[id] for id in pr], prac='p')
            self.frame.grid_forget()
            self.rp.grid()
        elif len(pr) == 0 and not len(tr) == 0:
            self.rp = CreateRP(self, disc=[self.ListOfDisciplines.Theory[id] for id in tr], prac='t')
            self.frame.grid_forget()
            self.rp.grid()
        else:
            showerror(title="Ошибка", message="Надо выбрать только теорию или только практику")

    def save_themes(self, que):
        """Загрузка тем в журнал"""
        for id in self.tab.frame_tr.get_check_group():
            que.put(
                f"Теория {self.ListOfDisciplines.Theory[id]['name'][:self.ListOfDisciplines.Theory[id]['name'].find('_')]}")
            self.session.save_themes(self.ListOfDisciplines.Theory[id], prac='')
        for id in self.tab.frame_pr.get_check_group():
            que.put(
                f"Практика {self.ListOfDisciplines.Practice[id]['name'][:self.ListOfDisciplines.Practice[id]['name'].find('_')]}")
            self.session.save_themes(self.ListOfDisciplines.Practice[id], prac='1')

    def upload_tabl(self):
        """Обновление журнала"""
        ProgressBar(self, self.session.save_file_disc)
        reload(self.ListOfDisciplines)
        self.tab.destroy()
        self.tab = TabView(self.ListOfDisciplines, self.frame)
        self.tab.grid(row=1, column=0, pady=10, padx=10, columnspan=3)

    def on_button_click(self):
        input_text = self.entry.get()
        # .lower()
        today = None if input_text != 'Сегодня' else self.today
        self.tab.recreate_frame(input_text, today)

    def on_enter_pressed(self, event):
        # Вызвать функцию on_button_click при нажатии клавиши Enter
        self.on_button_click()

    def main_frame(self):
        """Основная функция отрисовки виджетов"""
        self.frame = CTkFrame(self)
        self.tab = TabView(self.ListOfDisciplines, self.frame)
        self.studen_frame = None
        self.entry = CTkEntry(self.frame, placeholder_text="Поиск", width=300)
        button = CTkButton(self.frame, text='Найти', command=self.on_button_click)
        button.grid(row=0, column=2, pady=10, padx=10)
        self.entry.grid(row=0, column=0, pady=10, padx=10, columnspan=2)
        # Привязать событие <Return> к полю ввода
        self.entry.bind("<Return>", self.on_enter_pressed)

        self.tab.grid(row=1, column=0, pady=10, padx=10, columnspan=3)
        button = CTkButton(self.frame, text='Выбрать всё',
                           command=lambda: self.tab.all_check_in_tabl(self.tab.get(), 'on'))
        button.grid(row=2, column=0, pady=10, padx=10)
        button = CTkButton(self.frame, text='Снять всё',
                           command=lambda: self.tab.all_check_in_tabl(self.tab.get(), 'off'))
        button.grid(row=3, column=0, pady=10, padx=10)
        button = CTkButton(self.frame, text='Открыть занятия',
                           command=lambda: ProgressBar(self, lambda q: self.button_close_open_lesson(True, q)))
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
# .............................................. #
