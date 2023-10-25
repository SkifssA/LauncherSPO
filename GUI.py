from customtkinter import *
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
