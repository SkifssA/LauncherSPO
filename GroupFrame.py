import tkinter
from customtkinter import *

class GroupFrame(CTkScrollableFrame):
    '''Фрейм списка групп'''

    def __init__(self, ListOfDisciplines,master, prac, **kwargs):
        super().__init__(master, **kwargs)
        self.label = None
        self.check_var = [[], []]
        self.prac = prac
        self.ListOfDisciplines = ListOfDisciplines

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
                while self.ListOfDisciplines.Theory[ch]['subject_id'] != self.ListOfDisciplines.Theory[ch + i]['subject_id']:
                    i += 1
                yield ch
                yield ch + i
            elif self.ListOfDisciplines.Practice[ch]['name'].find('/2') != -1:
                name = self.ListOfDisciplines.Practice[ch]['name'][:self.ListOfDisciplines.Practice[ch]['name'].find('(')]
                name = name[:name.find('_')] + 'в' + name[name.find('_'):]
                while name != self.ListOfDisciplines.Practice[ch + i]['name']:
                    i += 1
                yield ch
                yield ch + i
            else:
                yield ch

    def __get_check_group(self) -> tuple:
        for i in list(self.__get_check_group()):
            print(self.check_var[1][i]._text)
# .............................................. #
