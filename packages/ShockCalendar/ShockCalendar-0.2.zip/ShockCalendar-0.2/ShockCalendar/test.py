#test.py

from Tkinter import *;
from tkMessageBox import showinfo;
import ShockCalendar;




class TestApp:
    def __init__(self):
        self.win = Tk();
        self.win.title("Test ShockCalendar.py");
        self.win.geometry("330x230");

        width, height = 170, 170;
        self.calendar = ShockCalendar.Calendar(self.win, width, height);
        self.calendar.place(x=0, y=0, width=width, height=height);

        Label(self.win, text="Add event date:").place(x=176, y=5);

        Label(self.win, text="year:").place(x=176, y=30);
        self.entryYear = Entry(self.win);
        self.entryYear.insert(0, "2016");
        self.entryYear.place(x=232, y=30, width=55);

        Label(self.win, text="month:").place(x=176, y=70);
        self.entryMonth = Entry(self.win);
        self.entryMonth.insert(0, "12");
        self.entryMonth.place(x=232, y=70, width=55);

        Label(self.win, text="day:").place(x=176, y=110);
        self.entryDay = Entry(self.win);
        self.entryDay.insert(0, "2");
        self.entryDay.place(x=232, y=110, width=55);

        self.btnAdd = Button(self.win, text="Add event", command=self.AddEvent);
        self.btnAdd.place(x=175, y=140, width=72);
        self.btnShow = Button(self.win, text="Show date", command=self.ShowDate);
        self.btnShow.place(x=255, y=140, width=72);

        self.btnShowSel = Button(self.win, text="Show selection", command=self.ShowSels);
        self.btnShowSel.place(x=110, y=180, width=100);
        self.btnShowEvents = Button(self.win, text="Show Events", command=self.GetEvents);
        self.btnShowEvents.place(x=5, y=180, width=100);

    def ShowSels(self):
        res = self.calendar.GetSelectDay();
        text = "Result: " + str(res) + "\n" + str(type(res));
        showinfo("GetSelectDay()", text);

    def ShowDate(self):
        d, m, y = int(self.entryDay.get()), int(self.entryMonth.get()), int(self.entryYear.get());
        self.calendar.ShowDate(y, m, d);

        showinfo("ShowDate", "calendar.ShowDate(y, m, d)");
        
    def AddEvent(self):
        d, m, y = int(self.entryDay.get()), int(self.entryMonth.get()), int(self.entryYear.get());

        varinfo = {"text": "example of information (varinfo)"}
        
        self.calendar.AddEventDay(y, m, d, varinfo);

        showinfo("AddEventDay", "calendar.AddEventDay(y, m, d, varinfo)");

    def GetEvents(self):

        w2 = Toplevel(self.win);
        w2.transient(self.win);
        w2.title("Events info");
        w2.geometry("300x200+%s+%s" % ( self.win.winfo_x()-100, self.win.winfo_y()+100 ) );

        text = Text(w2);
        text.place(x=0, y=0, width=280, height=200);

        scrolly = Scrollbar(w2, command=text.yview);
        scrolly.place(x=281, y=0, height=200);

        text.configure(yscrollcommand=scrolly.set);

        events = self.calendar.GetEventDays();

        for e in events:
            
            text.insert(END, "date: %d/%02d/%d\ninfoVar: %s\ncolor: %s\n" % (e.year, e.month, e.day,
                            str(e.infoVar), str(e.color))
                        );
        
        
        
        
m = TestApp()
m.win.mainloop();
