import GUI
import ReJ


'''s = ReJ.AvtoJ()
s.set_cookie('ssuz_sessionid=zjehaw1kic0m54f190m19wrqsf655gcg')
#s.create_score_pole('4078', '{"subject_id": 2484, "sub_group_id": 13511}', '3381956', prac='1')
print(s.show_score_pole('4078', '{"subject_id": 2484, "sub_group_id": 13511}', '3381956', prac='1')['rows'][0]['id'])
#s.expose_score('4078', '{"subject_id": 2484, "sub_group_id": 13511}', '3381956', '1366884', '5', '61657')'''



from customtkinter import *
from tkinter import *
from datetime import *

class Calendar(CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=2, pady=10, padx=10)
        self.mount = '01'
        self.date = datetime.strptime('01/01/2023', '%d/%m/%y')



    def create_days(self):
        n = 0
        self.canvas.create_rectangle(n,)

