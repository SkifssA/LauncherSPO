from customtkinter import *
import re


'''Форма для проверки явки'''


class StudentFrame(CTkScrollableFrame):
    def __init__(self, master, session, dics=None, dics2=None, prac='', date_from=None, date_whis=None):

        self.date_from = date_from
        self.date_whis = date_whis
        self.root = CTkFrame(master)
        self.master1 = master
        super().__init__(self.root, width=700, height=500)
        self.grid(row=0, column=0, pady=10, padx=10, columnspan=5)
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
        for j, i in enumerate(self.rows):
            self.student_lesson(i, j)
        if self.disc2 is not None:
            self.add_v_group(self.disc2, date_from, date_whis)
        self.button_save = CTkButton(self.root, text='Сохранить', command=lambda: self.all_save())
        self.button_save.grid(row=2, column=0, pady=10, padx=10)
        self.button_create = CTkButton(self.root, text='Создать поле для оценок', command=lambda: self.add_score())
        self.button_create.grid(row=2, column=1, pady=10, padx=10)
        self.button_begin = CTkButton(self.root, text='Вернуться в начало', command=self.begin)
        self.button_begin.grid(row=2, column=2, pady=10, padx=10)
        self.button_back = CTkButton(self.root, text='Назад', command=self.back)
        self.button_back.grid(row=2, column=3, pady=10, padx=10)
        self.add_score_ui()


    def begin(self):
        self.master1.frame.grid()
        self.master1.studen_frame.destroy()
        self.root.destroy()

    def back(self):
        self.master1.studen_frame.grid()
        self.root.destroy()

    '''Сохранение всей формы'''
    def all_save(self):
        self.save_score()
        self.turnout()

    '''Возможность быстро перемещаться по полям оценок вниз'''

    def move(self, e):
        nums = re.findall(r'\d+', str(self.root.focus_get()))
        n = 1 if len(nums) == 1 else int(nums[1])
        if e.keysym == 'Down':
            if n < len(self.entry):
                self.entry[n].focus_set()
        elif e.keysym == 'Up':
            if n > 0:
                self.entry[n-2].focus_set()

    '''Сохранение оценок в журнал'''

    def save_score(self):
        n = len(self.rows)
        for i, entry in enumerate(self.entry[:n]):
            self.session.expose_score(self.disc['id_group'], self.disc['subject_id'], self.rows[0]['lessons'][-1]['id'],
                                      self.score[0]['rows'][0]['id'], entry.get(), self.rows[i]['student_id'])
        if self.rows2 is not None:
            for i, entry in enumerate(self.entry[n:]):
                self.session.expose_score(self.disc2['id_group'], self.disc2['subject_id'],
                                          self.rows2[0]['lessons'][-1]['id'],
                                          self.score[1]['rows'][0]['id'], entry.get(), self.rows2[i]['student_id'])

    '''Создание полей для оценок в лаучере'''

    def add_score_ui(self):
        self.score = []
        self.score.append(self.session.show_score_pole(self.disc['id_group'], self.disc['subject_id'],
                                                       self.rows[0]['lessons'][-1]['id']))
        if self.disc2 is not None:
            self.score.append(self.session.show_score_pole(self.disc2['id_group'], self.disc2['subject_id'],
                                                           self.rows2[0]['lessons'][-1]['id']))
        if self.score[0]['total'] != 0:
            for com in range(len(self.combo)):

                self.entry.append(CTkEntry(self, width=10))
                if com < len(self.rows):
                    self.entry[-1].insert(0, self.rows[com]['lessons'][-1][f'work_{self.score[0]["rows"][0]["id"]}'][
                        'type_id_36_score'])
                else:
                    self.entry[-1].insert(0, self.rows2[com - len(self.rows)]['lessons'][-1][
                        f'work_{self.score[1]["rows"][0]["id"]}'][
                        'type_id_36_score'])
                self.entry[-1].grid(row=com, column=len(self.combo[0]) + 1, pady=5, padx=5)
                self.entry[-1].bind('<KeyPress>', lambda e: self.move(e))
            self.button_create.configure(state='disabled')

    '''Создание полей для оценок в журнале'''

    def add_score(self):
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

    '''Добавление группы "в"'''

    def add_v_group(self, dics, date_from, date_whis):
        self.rows2 = self.session.student_rows(dics['id_group'], dics['subject_id'], prac=self.prac,
                                               date_from=date_from, date_whis=date_whis)['rows']
        for j, i in enumerate(self.rows2):
            self.student_lesson(i, j + len(self.rows))

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
            set_box = False
            for box in self.combo[j]:
                if box.get() == x:
                    set_box = True
                elif set_box:
                    box.set('' if x == 'О' else x)

    '''Выставление явки в журнал'''

    def turnout(self):
        n = len(self.rows)
        for id_student, student in enumerate(self.combo[:n]):
            for id_lesson, lesson in enumerate(student):
                # if lesson.get() != '':
                self.session.setting_turnout(self.disc['id_group'], self.disc['subject_id'],
                                             self.rows[id_student]['student_id'],
                                             self.rows[id_student]['lessons'][id_lesson]['id'], lesson.get(),
                                             prac=self.prac)
        if self.rows2 is not None:
            for id_student, student in enumerate(self.combo[n:]):
                for id_lesson, lesson in enumerate(student):
                    # if lesson.get() != '':
                    self.session.setting_turnout(self.disc2['id_group'], self.disc2['subject_id'],
                                                 self.rows2[id_student]['student_id'],
                                                 self.rows2[id_student]['lessons'][id_lesson]['id'], lesson.get(),
                                                 prac=self.prac)
