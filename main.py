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
        self.canvas = Canvas(self, width=140, height=100)
        self.canvas.grid(row=0, column=2, pady=10, padx=10)
        self.date_mass = [4, 23]
        self.size = 20
        self.create_days()


    def create_days(self):
        n = 0
        for i in range(1, 32):
            try:
                date = datetime.strptime(f'{i}/{self.date_mass[0]}/{self.date_mass[1]}', '%d/%m/%y')
                w = 6 if (d := int(datetime.strftime(date, '%w'))) == 0 else d-1
                self.canvas.create_rectangle(w * self.size, n * self.size,
                                             (1+w) * self.size, (n+1) * self.size,
                                             fill='#cccccc' if w < 5 else '#999999', tags=f'{i}')
                self.canvas.create_text(((w * self.size) + ((1 + w) * self.size))/2,
                                        ((n * self.size)+(n + 1) * self.size)/2, text=f'{i}',
                                        fill='black')
                if w == 6:
                    n += 1
            except ValueError:
                break


s = Calendar()
s.mainloop()