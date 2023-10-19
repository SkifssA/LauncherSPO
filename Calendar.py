import datetime

from customtkinter import *
from tkinter import *
from datetime import *
from StudentFrame import StudentFrame


class Calendar(CTkFrame):
    """Форма календаря"""

    def __init__(self, master, session, dics, prac='', **kwargs):
        super().__init__(master, **kwargs)
        self.master1 = master
        self.prac = prac
        self.size = 40
        self.disc = dics[0]
        try:
            self.disc2 = dics[1]
        except:
            self.disc2 = None
        self.session = session
        self.date_lesson = set(
            [x['date'] for x in session.student_rows(self.disc['id_group'], self.disc['subject_id'], prac=prac)[
                'rows'][0]['lessons']])
        self.mount_mass = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                           'Октябрь', 'Ноябрь', 'Декабрь']
        self.mount = StringVar()
        self.date = StringVar()
        date_now = datetime.now()

        CTkLabel(self, textvariable=self.date).grid(row=2, column=0, pady=10, padx=10)
        CTkLabel(self, textvariable=self.mount).grid(row=0, column=1, pady=10, padx=10)
        CTkButton(self, text='<', width=50, command=lambda: self.down(True)).grid(row=0, column=0, pady=10, padx=10)
        CTkButton(self, text='>', width=50, command=lambda: self.down(False)).grid(row=0, column=2, pady=10, padx=10)
        self.open_button = CTkButton(self, text='Открыть журнал', command=self.open_frame)
        self.open_button.grid(row=2, column=2, pady=10, padx=10, columnspan=3)
        CTkButton(self, text='Назад', command=self.back).grid(row=3, column=0, pady=10, padx=10,
                                                              columnspan=4)
        CTkButton(self, text='Сегодня', command=lambda: self.date.set(datetime.strftime(date_now, "%d.%m.%Y")),
                  width=90).grid(row=0, column=3, pady=10, padx=10)
        self.canvas = Canvas(self, width=7 * self.size, height=6 * self.size, bg='#242424', highlightthickness=0)
        self.canvas.grid(row=1, column=0, pady=10, padx=10, columnspan=4)

        self.date_mass = [int(datetime.strftime(date_now, '%m')), datetime.strftime(date_now, '%y')]
        self.mount.set(self.mount_mass[self.date_mass[0] - 1])
        self.date.set(f'{datetime.strftime(date_now, "%d")}.{self.date_mass[0]:02}.20{self.date_mass[1]}')
        self.canvas_mass = [[None for _ in range(6)] for _ in range(7)]
        if datetime.now().strftime('%d.%m.%Y') not in self.date_lesson:
            self.open_button.configure(state='disabled')
        self.create_days()

    def back(self):
        """Возврат на начальную форму"""
        self.master1.frame.grid()
        self.destroy()

    def open_frame(self):
        """Открытие формы для выставления присутствия и оценок"""
        if self.prac == '':
            frane_s = StudentFrame(self.master1, self.session, dics=self.disc, dics2=self.disc2,
                                   date_from=self.date.get(),
                                   date_whis=self.date.get())
        else:
            if self.disc2 is not None:
                frane_s = StudentFrame(self.master1, self.session, dics=self.disc, dics2=self.disc2, prac=self.prac,
                                       date_from=self.date.get(),
                                       date_whis=self.date.get())
            else:
                frane_s = StudentFrame(self.master1, self.session, dics=self.disc, prac=self.prac,
                                       date_from=self.date.get(),
                                       date_whis=self.date.get())
        frane_s.root.grid()
        self.grid_forget()

    def down(self, d):
        """Перемещение по месяцам"""
        self.date_mass[0] += -1 if d else 1
        self.mount.set(self.mount_mass[self.date_mass[0] - 1])
        self.create_days()

    def date_get(self, e):
        """Показ даты и запрет на открытия формы для не учебного дня"""
        x, y = e.x // self.size, e.y // self.size
        if self.canvas_mass[x][y] is not None:
            self.date.set(f'{int(self.canvas_mass[x][y][1:]):02}.{self.date_mass[0]:02}.20{self.date_mass[1]}')
        if self.canvas.itemcget(self.canvas_mass[x][y], 'fill') == 'green':
            self.open_button.configure(state='normal')
        else:
            self.open_button.configure(state='disabled')
        self.create_days()

    def create_days(self):
        """Создание всех дней"""
        self.canvas.delete('all')
        n = 0
        for i in range(1, 32):
            try:
                date = datetime.strptime(f'{i}.{self.date_mass[0]}.{self.date_mass[1]}', '%d.%m.%y')
                w = 6 if (d := int(datetime.strftime(date, '%w'))) == 0 else d - 1
                if self.date.get() == datetime.strftime(date, '%d.%m.%Y'):
                    fill_date = 'red'
                elif datetime.strftime(date, '%d.%m.%Y') in self.date_lesson:
                    fill_date = 'green'
                else:
                    fill_date = '#cccccc' if w < 5 else '#999999'
                self.canvas.create_rectangle(w * self.size, n * self.size,
                                             (1 + w) * self.size, (n + 1) * self.size,
                                             fill=fill_date, tags=f'd{i}')
                self.canvas_mass[w][n] = f'd{i}'
                self.canvas.create_text(((w * self.size) + ((1 + w) * self.size)) / 2,
                                        ((n * self.size) + (n + 1) * self.size) / 2, text=f'{i}',
                                        fill='black', tags=f'd{i}')
                self.canvas.bind('<Button-1>', self.date_get)
                if w == 6:
                    n += 1
            except ValueError:
                break
