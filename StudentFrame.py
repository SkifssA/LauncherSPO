from customtkinter import *
import re
from ProgressBar import ProgressBar
from datetime import datetime


class StudentFrame(CTkScrollableFrame):
    """Форма для проверки явки"""

    def __init__(self, master, session, dics=None, dics2=None, prac='', date_from=None, date_whis=None):
        self.date_from = date_from
        self.date_whis = date_whis
        self.root = CTkFrame(master)
        self.master1 = master
        super().__init__(self.root, width=750, height=500)
        self.grid(row=1, column=0, pady=10, padx=10, columnspan=5)
        self.session = session
        self.disc = dics
        self.prac = prac
        self.rows = session.student_rows(dics['id_group'], dics['subject_id'], prac=self.prac,
                                         date_from=date_from, date_whis=date_whis)['rows']
        self.disc2 = dics2
        self.rows2 = None
        self.value_combobox = ['', 'Н', 'Б', 'У', 'О']
        self.score = []
        self.combo = []
        self.label = []
        self.entry = []
        self.year_score = []
        for j, i in enumerate(self.rows):
            self.student_lesson(i, j)
        if self.disc2 is not None:
            self.add_v_group(self.disc2, date_from, date_whis)
        self.upload_year_score()
        CTkLabel(self.root, text=self.disc['name'], text_color='white') \
            .grid(row=0, column=0, pady=10, padx=10, columnspan=3)
        CTkLabel(self.root, text_color='white' if (cl := self.clock_back()) > 10 or cl < 0 else 'red',
                 text=f'Осталось часов {cl}' if cl >= 0 else f'Выдано часов {-cl}') \
            .grid(row=0, column=3, pady=10, padx=10, columnspan=2)
        self.button_save = CTkButton(self.root, text='Сохранить', command=lambda: ProgressBar(master, self.all_save))
        self.button_save.grid(row=3, column=0, pady=10, padx=10)
        self.button_create = CTkButton(self.root, text='Создать поле для оценок', command=lambda: self.add_score())
        self.button_create.grid(row=3, column=1, pady=10, padx=10)
        self.button_begin = CTkButton(self.root, text='Вернуться в начало', command=self.begin)
        self.button_begin.grid(row=3, column=2, pady=10, padx=10)
        self.button_back = CTkButton(self.root, text='Назад', command=self.back)
        self.button_back.grid(row=3, column=3, pady=10, padx=10)
        for i in range(self.session.show_score_pole(self.disc['id_group'], self.disc['subject_id'],
                                                    self.rows[0]['lessons'][-1]['id'])['total']):
            self.add_score_ui()

    def clock_back(self):
        cl = 0

        mon = int(datetime.today().strftime('%m'))
        if 13 > mon > 8:
            date_from = datetime.today().strftime('%Y')
        else:
            date_from = int(datetime.today().strftime('%Y')) - 1

        prac = 't' if self.prac == '' else 'p'
        for file in os.listdir(os.getcwd() + '/Themes'):
            if self.disc['id_group'] in file and self.disc['name'][
                                                 self.disc['name'].find('_') + 1:self.disc['name'].find(' ')] in file \
                    and prac in file[:-4]:
                with open('Themes/' + file, 'r') as f:
                    cl = int(f.readline())
        return cl - len(self.session.student_rows(self.disc['id_group'], self.disc['subject_id'], prac=self.prac,
                                                  date_from=f'01.09.{date_from}',
                                                  date_whis=self.date_whis)['rows'][0]['lessons'])

    def begin(self):
        """Возврат к начальной форме"""
        self.master1.frame.grid()
        self.master1.studen_frame.destroy()
        self.root.destroy()

    def back(self):
        """Возврат на прошлую форму"""
        self.master1.studen_frame.grid()
        self.root.destroy()

    def all_save(self, que):
        """Сохранение всей формы"""
        que.put('Оценки')
        self.save_score()
        que.put('Неявка')
        self.turnout()
        que.put('Итоговые оценки')
        self.upload_year_score()

    def move(self, e):
        """Возможность быстро перемещаться по полям оценок вниз и вверх"""
        nums = re.findall(r'\d+', str(self.root.focus_get()))
        n = 1 if len(nums) == 1 else int(nums[1])
        if e.keysym == 'Down':
            if n < len(self.entry):
                self.entry[n].focus_set()
        elif e.keysym == 'Up':
            if n > 0:
                self.entry[n - 2].focus_set()

    def add_score_ui(self):
        """Создание полей для оценок в лаунчере"""
        self.score = []

        self.score.append(self.session.show_score_pole(self.disc['id_group'], self.disc['subject_id'],
                                                       self.rows[0]['lessons'][-1]['id']))

        if self.disc2 is not None:
            self.score.append(self.session.show_score_pole(self.disc2['id_group'], self.disc2['subject_id'],
                                                           self.rows2[0]['lessons'][-1]['id']))
        n = len(self.entry)
        if self.score[0]['total'] != 0:
            self.entry.append([])
            for com in range(len(self.combo)):
                self.entry[n].append(CTkEntry(self, width=10))
                if com < len(self.rows):
                    self.entry[n][-1].insert(0, self.rows[com]['lessons'][-1][
                        f'work_{self.score[0]["rows"][self.score[0]["total"] - n - 1]["id"]}'][
                        'type_id_36_score'])
                else:
                    self.entry[n][-1].insert(0, self.rows2[com - len(self.rows)]['lessons'][-1][
                        f'work_{self.score[1]["rows"][self.score[0]["total"] - n - 1]["id"]}'][
                        'type_id_36_score'])
                self.entry[n][-1].grid(row=com, column=len(self.combo[0]) + 1 + n, pady=5, padx=5)
                self.entry[n][-1].bind('<KeyPress>', lambda e: self.move(e))
            # self.button_create.configure(state='disabled')

    def add_score(self):
        """Создание полей для оценок в журнале"""
        self.session.create_score_pole(self.disc['id_group'], self.disc['subject_id'],
                                       self.rows[0]['lessons'][-1]['id'])
        self.rows = self.session.student_rows(self.disc['id_group'], self.disc['subject_id'], prac=self.prac,
                                              date_from=self.date_from, date_whis=self.date_whis)['rows']
        if self.rows2 is not None:
            self.session.create_score_pole(self.disc2['id_group'], self.disc2['subject_id'],
                                           self.rows2[0]['lessons'][-1]['id'])
            self.rows2 = self.session.student_rows(self.disc2['id_group'], self.disc2['subject_id'], prac=self.prac,
                                                   date_from=self.date_from, date_whis=self.date_whis)['rows']
        self.add_score_ui()

    def add_v_group(self, dics, date_from, date_whis):
        """Добавление группы 'в'"""
        self.rows2 = self.session.student_rows(dics['id_group'], dics['subject_id'], prac=self.prac,
                                               date_from=date_from, date_whis=date_whis)['rows']
        for j, i in enumerate(self.rows2):
            self.student_lesson(i, j + len(self.rows))

    def upload_year_score(self):
        """Обновление средней оценки"""
        self.rows = self.session.student_rows(self.disc['id_group'], self.disc['subject_id'], prac=self.prac,
                                              date_from=self.date_from, date_whis=self.date_whis)['rows']
        for i, student in enumerate(self.rows):
            self.year_score[i].set(f'    {student["aver_period"]}')
        if self.rows2 is not None:
            self.rows2 = self.session.student_rows(self.disc2['id_group'], self.disc2['subject_id'], prac=self.prac,
                                                   date_from=self.date_from, date_whis=self.date_whis)['rows']
            n = len(self.rows)
            for i, student in enumerate(self.rows2):
                self.year_score[n + i].set(f'    {student["aver_period"]}')

    def student_lesson(self, student, j):
        """Метод создания явки на 1 студента"""
        self.label.append(CTkLabel(self, text=student['student_name']))
        self.label[-1].grid(row=j, column=0, padx=20, pady=5)
        self.combo.append([])
        for i, n in enumerate(student['lessons']):
            self.combo[-1].append(
                CTkOptionMenu(self, values=self.value_combobox, width=50, command=lambda x: self.p(j, x)))
            self.combo[-1][-1].grid(row=j, column=i + 1, padx=5, pady=5)
            self.combo[-1][-1].set(n['attendance']['value'])

        self.year_score.append(StringVar())
        CTkLabel(self, textvariable=self.year_score[-1]).grid(row=j, column=len(student['lessons']) + 10, padx=5,
                                                              pady=5)

    def p(self, j, x):
        """Метод проставления значений студенту до конца занятий"""
        set_box = False
        for box in self.combo[j]:
            if box.get() == x:
                set_box = True
            elif set_box:
                box.set('' if x == 'О' else x)

    def turnout(self):
        """Выставление явки в журнал"""
        n = len(self.rows)
        for id_student, student in enumerate(self.combo[:n]):
            for id_lesson, lesson in enumerate(student):
                if lesson.get() != ' ':
                    self.session.setting_turnout(self.disc['id_group'], self.disc['subject_id'],
                                                 self.rows[id_student]['student_id'],
                                                 self.rows[id_student]['lessons'][id_lesson]['id'], lesson.get(),
                                                 prac=self.prac)
        if self.rows2 is not None:
            for id_student, student in enumerate(self.combo[n:]):
                for id_lesson, lesson in enumerate(student):
                    if lesson.get() != ' ':
                        self.session.setting_turnout(self.disc2['id_group'], self.disc2['subject_id'],
                                                     self.rows2[id_student]['student_id'],
                                                     self.rows2[id_student]['lessons'][id_lesson]['id'], lesson.get(),
                                                     prac=self.prac)

    def save_score(self):
        """Сохранение оценок в журнал"""
        n = len(self.rows)
        for j, s in enumerate(self.entry):
            for i, entry in enumerate(s[:n]):
                if entry.get() != ' ':
                    self.session.expose_score(self.disc['id_group'], self.disc['subject_id'],
                                              self.rows[0]['lessons'][-1]['id'],
                                              self.score[0]['rows'][self.score[0]['total'] - j - 1]['id'],
                                              entry.get(),
                                              self.rows[i]['student_id'])
            if self.rows2 is not None:
                for i, entry in enumerate(s[n:]):
                    if entry.get() != ' ':
                        self.session.expose_score(self.disc2['id_group'], self.disc2['subject_id'],
                                                  self.rows2[0]['lessons'][-1]['id'],
                                                  self.score[1]['rows'][self.score[0]['total'] - j - 1]['id'],
                                                  entry.get(),
                                                  self.rows2[i]['student_id'])
