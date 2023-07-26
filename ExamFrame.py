from tkinter.messagebox import showerror
from customtkinter import *
from datetime import datetime


def create_data():
    mon = int(datetime.today().strftime('%m'))
    y = int(datetime.today().strftime('%y'))
    if 13 > mon > 8:
        subperiod = 399
        sem = f'1 семестр({y}/{y + 1})'
    else:
        subperiod = 400
        sem = f'2 семестр({y - 1}/{y})'
    return subperiod, sem


def sd(score):
    i = int(score) if score % 1 < 0.75 else int(score) + 1
    return i


class Exam(CTkScrollableFrame):
    def __init__(self, master, session, disc=None, disc2=None):

        self.exam_id = (i['id'] for i in session.ved_get(30, 399, 'Копылов')
                        if (disc['name'][:disc['name'].find('_')] == i['group_actual_name'][
                                                                     :i['group_actual_name'].find(' ')]
                            or disc2['name'][:disc2['name'].find('_')] == i['group_actual_name'][
                                                                          :i['group_actual_name'].find(' ')])
                        and disc['name'][disc['name'].find('_') + 1:-1] == i['exam_schedule'][
                            'subject_names'])
        if len(tuple(self.exam_id)) == 0:
            showerror(title="Ошибка", message="Нет ведомости")
            self.back(master)

        self.session = session
        self.disc = [disc, disc2]
        self.root = CTkFrame(master)
        self.rows = (session.student_rows(self.disc[0]['id_group'], self.disc[0]['subject_id'],
                                          date_from=datetime.today().strftime('%d.%m.%Y'))['rows'] +
                     session.student_rows(self.disc[1]['id_group'], self.disc[1]['subject_id'],
                                          date_from=datetime.today().strftime('%d.%m.%Y'))['rows'])

        super().__init__(self.root, width=650, height=500)
        self.grid(row=1, column=0, pady=10, padx=10, columnspan=5)

        CTkLabel(self.root, text=self.disc[0]['name']).grid(row=0, column=0, pady=10, padx=10, columnspan=5)

        self.score_exam = []
        for i in self.rows:
            self.create_score(i)

        CTkButton(self.root, text='Назад', command=lambda: self.back(master)).grid(row=2, column=4, pady=10, padx=10)
        CTkButton(self.root, text='Сводка', command=lambda: self.info()).grid(row=2, column=0, pady=10, padx=10)

    def back(self, master):
        master.frame.grid()
        self.root.destroy()

    def info(self):
        s = [0, 0, 0, 0]
        w = 0
        for i in self.score_exam:
            try:
                s[int(i.get()) - 2] += 1
                w += int(i.get())
            except ValueError:
                pass
        mess = f'5: {s[3]}\n4: {s[2]}\n3: {s[1]}\n2: {s[0]}\nН\\Я: {len(self.score_exam) - sum(s)}\n'
        mess += f'Качественная успеваемость: {round((s[3] + s[2]) * 100 / len(self.score_exam), 2)}%\n'
        mess += f'Степень обученности учащихся: {round((s[3] * 100 + s[2] * 64 + s[1] * 36 + s[0] * 16 + (len(self.score_exam) - sum(s)) * 7) / len(self.score_exam), 2)}%\n'
        mess += f'Средняя оценка: {round(w / len(self.score_exam), 2)}'
        showerror(title="Сводка", message=mess)

    def create_score(self, student):
        self.score_exam.append(CTkEntry(self, width=10))
        CTkLabel(self, text=student['student_name']).grid(row=len(self.score_exam) - 1, column=0, pady=5, padx=50)
        CTkLabel(self, text=student['aver_period']).grid(row=len(self.score_exam) - 1, column=1, pady=5, padx=50)
        self.score_exam[-1].insert(0, str(student['final_grade']))
        self.score_exam[-1].grid(row=len(self.score_exam) - 1, column=2, pady=5, padx=50)

    def type_score(self, disc):
        data = create_data()
        self.session.аssign_rating(disc['id_group'], disc['subject_id'], 'Годовая', mark=0)
        self.session.аssign_rating(disc['id_group'], disc['subject_id'], 'Итоговая', mark=1)
        self.session.аssign_rating(disc['id_group'], disc['subject_id'], data[1], subperiod=data[0])

    def save_exam(self):
        self.type_score(self.disc[0])
        self.type_score(self.disc[1])
        for i in self.exam_id:
            self.session.ved_score_type(i)
