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
from APP import APP

try:
    import ListOfDisciplines
except ModuleNotFoundError:
    with open('ListOfDisciplines.py', 'w') as f:
        f.write('Practice = [\n]\nTheory = [\n]')
    import ListOfDisciplines


if __name__ == '__main__':
    s = CTk()
    set_widget_scaling(s.winfo_screenheight() / 1080)
    s.destroy()
    APP(ListOfDisciplines)
