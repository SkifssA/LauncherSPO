from tkinter.messagebox import showerror
from customtkinter import *
from ProgressBar import ProgressBar
from GroupFrame import GroupFrame



class TabView(CTkTabview):
    '''Виджет выбора отображения теории или практики'''

    def __init__(self,ListOfDisciplines, master, **kwargs):
        super().__init__(master, **kwargs)
        self.height = 450
        self.width = 700
        self.ListOfDisciplines = ListOfDisciplines

        # Создание табл

        self.add("Теория")
        self.add("Практика")

        self.frame_pr = GroupFrame(self.ListOfDisciplines,self.tab('Практика'), True, width=self.width, height=self.height)
        self.frame_tr = GroupFrame(self.ListOfDisciplines,self.tab('Теория'), False, width=self.width, height=self.height)
        self.recreate_frame('')

    def recreate_frame(self, filter, today=None):
        '''Создание перечисления с группами'''
        if filter == 'Сегодня':
            self.frame_pr.create_group_checkbox(today[1], '')
            self.frame_pr.pack()

            self.frame_tr.create_group_checkbox(today[0], '')
            self.frame_tr.pack()
        else:
            self.frame_pr.create_group_checkbox(self.ListOfDisciplines.Practice, filter)
            self.frame_pr.pack()

            self.frame_tr.create_group_checkbox(self.ListOfDisciplines.Theory, filter)
            self.frame_tr.pack()

    def all_check_in_tabl(self, name_tabl, on_off):
        '''Выделение всех групп'''
        if name_tabl == 'Практика':
            self.frame_pr.all_check(on_off)
        else:
            self.frame_tr.all_check(on_off)
# .............................................. #