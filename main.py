import GUI
import ReJ
import ListOfDisciplines

#s = GUI.APP()



s =ReJ.AvtoJ()
s.set_cookie('ssuz_sessionid=nfflxrh8xp2nekaom6jwf6fnzn7xoy6p')





import customtkinter


class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = s.student_rows('4078', '{"subject_id": 2484, "sub_group_id": 13511}', prac='1', date_from='10.04.2023')['rows']
        self.lesson = [x['id'] for x in self.rows[0]['lessons']]
        self.value_combobox = ['', 'Н', 'Б', 'У', 'О']
        self.combo = []
        for j, i in enumerate(self.rows):
            self.student_lesson(i, j)
    def student_lesson(self, student, j):
        label = customtkinter.CTkLabel(self, text=student['student_name'])
        label.grid(row=j, column=0, padx=20, pady=5)
        for i, n in enumerate(student['lessons']):
            self.combo[-1].append(customtkinter.CTkOptionMenu(self, values=self.value_combobox, width=50, command=lambda x: self.p(j, x)))
            self.combo[-1][-1].grid(row=j, column=i+1, padx=5, pady=5)
            self.combo[-1][-1].set(n['attendance']['value'])

    def p(self, j, x):
        print(j, x)






class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.my_frame = MyFrame(self, width=500, height=500)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20)


app = App()
app.mainloop()

