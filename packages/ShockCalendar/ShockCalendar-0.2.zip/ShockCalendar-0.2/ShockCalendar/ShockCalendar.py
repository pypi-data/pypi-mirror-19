# ShockCalendar.py
# Copyright (c) <2016>  <adrian_leonardo_05@hotmail.com.ar>
#########################################################################
# un modulo calendario en Python para Tkinter
#########################################################################


########################################################################
# Copyright (c) <2016> <adrian_leonardo_05@hotmail.com.ar>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#########################################################################

"""

Calendar.py para usar como modulo en Tkinter

Descripcion y funcionalidad:
 Un calendario que muestra dias de meses, la fecha actual,
 incluye funciones utiles para seleccionar fechas, marcar eventos,
 recuperar seleccion, eventos...
 
 El usuario puede elegir fechas, y la aplicacion puede recuperar esa
 seleccion con metodos del objeto Calendar.

 Ademas, se puede marcar una fecha (evento) la cual sera
 una fecha con informacion que sera marcada en color para el usuario.

 El usuario puede recorrer los meses con botones hacia atras '<' o hacia adelante '>'.
 Ademas de esos botones, tambien puede cambiar de mes seleccionando dias de antes o dias
 despues del mes mostrado.

 Se puede modificar el diccionario "colors" antes de crear la instancia Calendar
 para mostrar un calendario con otros colores. Asi tambien se puede cambiar
 las variables "monthnames" y "days" por si fuese necesario pasar a otros idiomas.

Ejemplo:

from Tkinter import *;
import ShockCalendar;

win = Tk();
win.title("Test ShockCalendar");
win.geometry("330x250");


width, height = 170, 170;
cal = ShockCalendar.Calendar(win, width, height);
cal.place(x=0, y=0, width=width, height=height);

win.mainloop();

"""


from Tkinter import Canvas;
from tkFont import Font;
import calendar;
import time;


__version__ = "0.2"
__author__ = "adrian_leonardo_05@hotmail.com.ar"
__license__ = "MIT"


monthnames = [
          "Enero",
          "Febrero",
          "Marzo",
          "Abril",
          "Mayo",
          "Junio",
          "Julio",
          "Agosto",
          "Septiembre",
          "Ocutubre",
          "Noviembre",
          "Diciembre"
          ];

days = ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"];

colors = {
              "background": "#000000",
              "foreground": "green",
              "daybg": "#333333",
              "dayfg": "green",
              "linescolor": "#333333",
              "outrangedaysfg": "#007700",
              "currentdayfg": "white",
              "currentdayoutline": "#85FF85",
              "selectdatebg": "#303030",
              "selectdatelinecolor": "green",
              "eventday": "violet"
        };

def InfoDateVar(datetime=None, titlename=None, extras=None):
    """
    datetime = None or time.struc_time
    titlename = None or Descripcion date
    extras = Variables, strings, notes...
    """
    
    return {
            "datetime": datetime,
            "titlename": titlename,
            "extras": extras
            };


class EventDay:
    def __init__(self, year, month, day, color=colors["eventday"], infovar=InfoDateVar()):
        if year<0 and month<1 and month>12 and day<1 and day>31:
            raise ValueError;
        
        self.year, self.month, self.day = year, month, day;
        self.color = color;
        self.infoVar = infovar;

    def __str__(self):
        return "date=%d/%d/%d color=%s" % (self.year, self.month, self.day, self.color);
        


class MonthInfo:
    def __init__(self, year, month):
        self.year = year;
        self.month = month;

    def makeRanges(self):
        self.firstDayWeek, self.maxMonthDays = calendar.monthrange(self.year, self.month);

class StructSelectMonth:
    def __init__(self, year, month):
        self.current = MonthInfo(year, month);
        self.before = MonthInfo(year, month-1) if month>1 else MonthInfo(year-1, 12);
        self.next = MonthInfo(year, month+1) if month<12 else MonthInfo(year+1, 1);


class Calendar(Canvas):
    pos = StructSelectMonth(2016, 11);
    __cursorNumDay = 0;
    __eventsDays = [];
    __callback =None;
    def __init__(self, master, maxwidth, maxheight, showdefaultdate=(None, None, None), font=None):

        """
        Calendar for Tkinter

        master               ->   place in master.
        maxwidth & maxheight ->   calendar size drawn.
        showdefaultdate = (year, month, day) -> a tuple of integers to set the date to display.
        If not used the current date is displayed
        """
        Canvas.__init__(self, master, highlightthickness=0, bg=colors["background"]);

        rectwidth = maxwidth/7;
        rectheight = maxheight/8;

        pixsel = 6 #cantidad de pixeles por lado del selector '<' o '>' de meses

        x = rectwidth/2 - pixsel;
        y = rectheight/2;

        idmonth_antesRect = self.create_rectangle(x-3, y-pixsel-3, x+pixsel+3,y+pixsel+3, tags="mesbefore", fill=colors["background"], width=0)
        
        idmonth_antes = self.create_polygon(x,y, x+pixsel,y+pixsel, x+pixsel,y-pixsel, tags="mesbefore", fill=colors["foreground"], width=0)
        x = x + rectwidth*6 + pixsel*2

        idmonth_despuesRect = self.create_rectangle(x-pixsel-3, y-pixsel-3, x+3,y+pixsel+3, tags="mesnext", fill=colors["background"], width=0)
        
        idmonth_despues = self.create_polygon(x,y, x-pixsel,y-pixsel, x-pixsel,y+pixsel, tags="mesnext", fill=colors["foreground"], width=0)
        
        self.tag_bind("mesbefore", "<ButtonPress-1>", self.__changemonth_before);
        self.tag_bind("mesnext", "<ButtonPress-1>", self.__changemonth_next);

        self.font = font;
        if not font:
            self.font = Font(family="Verdana", name=self.font, size=8);

        self.fontUnderline = self.font.copy();
        self.fontUnderline.config(underline=1);
        
        self.create_text(maxwidth/2, y, text="", tags="textmonthyear", font=self.font, anchor="center", fill=colors["foreground"])
        
        y = rectheight;
        x = 0;

        for day in days:
            x2 = x + rectwidth;
            y2 = y + rectheight;

            idr = self.create_rectangle(x, y, x2, y2, fill=colors["daybg"], outline=colors["linescolor"])
            idt = self.create_text(x+rectwidth/2, y+rectheight/2, text=day[:2], font=self.font, fill=colors["dayfg"], anchor="center")

            x += rectwidth

        y = y + rectheight;

        for i in range(1, 7):

            x = 0;
            x2 = rectwidth;
            
            y2 = y + rectheight;
            
            for e in range(1, 8):
                
                idr = self.create_rectangle(x, y, x2, y2, tags="dayrect", fill=colors["background"], outline=colors["linescolor"])
                idt = self.create_text(x+rectwidth/2, y+rectheight/2, tags="dayentry", text="", font=self.font, fill=colors["foreground"])

                x += rectwidth;
                x2 = x + rectwidth;

            y += rectheight;

        self.tag_bind("dayrect", "<ButtonPress-1>", self.__selectday);
        self.tag_bind("dayentry", "<ButtonPress-1>", self.__selectday);

        year, month, day = showdefaultdate;
        
        self.ShowDate(year, month, day);

    def SetCallback(self, func=None):
        """Se le pasa el parametro func que define la funcion a llamar para
        cada vez que se seleccione un dia."""
        self.__callback = func;

    def __startCallback(self):
        if self.__callback():
            self.__callback();
        

    def ShowDate(self, year=None, month=None, day=None):
        """Se usa para mostrar una fecha en el calendario,
        si no se utiliza ningun parametro se recupera la fecha actual."""

        if not year and not month and not day:
            systime = time.localtime();
            year = systime.tm_year;
            month = systime.tm_mon;
            day = systime.tm_mday;
        
        self.__setmonth(year, month);

        self.__selectday(day=day);
        

    def __selectday(self, event=None, day=None):

        """Se usa por otros metodos o al hacer clic sobre un dia"""
        
        idsRects = sorted(self.find_withtag("dayrect"));
        idsEntrys = sorted(self.find_withtag("dayentry"));

        current = self.pos.current

        if event:
            _id = self.find_closest(event.x, event.y)[0];

            if _id in idsRects:
                index = idsRects.index(_id);
            elif _id in idsEntrys:
                index = idsEntrys.index(_id);
            else:
                #clic errado
                return 0;
            
            if index <= current.firstDayWeek:
                #se selecciono dias del mes pasado, se mostrara el anterior mes
                self.__changemonth_before(defaultdayselect = int(self.itemcget(idsEntrys[index], "text")));
                
                return 0;
            elif index > current.firstDayWeek+current.maxMonthDays:
                #se selecciono dias del siguiente mes, se mostrara en el siguiente mes
                self.__changemonth_next(defaultdayselect = index - current.maxMonthDays - current.firstDayWeek);
                
                return 0;

        elif day:
            index = current.firstDayWeek + day;
        else:
            raise ValueError, "no se uso el parametro day"

        self.__cursorNumDay = index;

        #damos el color y dash default a todos los cuadrados:
        self.itemconfig("dayrect", fill=colors["background"], dash="", outline = colors["linescolor"]);
        
        idEntry = idsEntrys[index];
        idRect  = idsRects[index];
        
        self.itemconfig(idRect, fill=colors["selectdatebg"], dash=(1, 1), outline = colors["selectdatelinecolor"]);
        
        self.tag_raise(idRect);
        self.tag_raise(idEntry);

        self.__showEventDays();

        if self.__callback:
            self.__callback();
        
    def __showEventDays(self):

        idsRects = sorted(self.find_withtag("dayrect"));
        idsEntrys = sorted(self.find_withtag("dayentry"));

        self.itemconfig("dayentry", font=self.font);

        stime = time.localtime();
        titlename = "Fecha de hoy %d/%02d/%d." % (stime.tm_mday, stime.tm_mon, stime.tm_year);
        infovar = InfoDateVar(datetime=None, titlename=titlename, extras=None);
        
        eventToday = EventDay(stime.tm_year, stime.tm_mon, stime.tm_mday, color=colors["currentdayfg"], infovar=infovar);

        events = [eventToday] + self.__eventsDays;

        current = self.pos.current
        before = self.pos.before
        next = self.pos.next

        for event in events:
            index = 0;
            
            if current.year==event.year and current.month==event.month:
                index = current.firstDayWeek + event.day;

            elif before.year==event.year and before.month==event.month:
                if event.day >= before.maxMonthDays-current.firstDayWeek and event.day <= before.maxMonthDays:
                    index =  event.day - (before.maxMonthDays-current.firstDayWeek);
                else:
                    continue;

            elif next.year==event.year and next.month==event.month:
                indexNext = (current.firstDayWeek +1 +current.maxMonthDays);

                maxRange = len(idsRects) - indexNext;
                if event.day <= maxRange:
                    index = indexNext + event.day - 1;
                else:
                    continue;

            else:
                continue;
            
            if event.color==colors["currentdayfg"]:
                self.itemconfig(idsEntrys[index], font=self.font, fill=colors["currentdayfg"]);
                self.itemconfig(idsRects[index], outline=colors["currentdayfg"]);

                self.tag_raise(idsRects[index]);
                self.tag_raise(idsEntrys[index]);
            else:
                self.itemconfig(idsEntrys[index], font=self.fontUnderline, fill=event.color);
                

    def AddEventDay(self, year, month, day, infovar=None, color=colors["eventday"]):

        """Agrega una fecha que se mostrara en color en el calendario, ademas
        se puede usar el parametro infovar para definir una variable a como dato informativo."""

        event = EventDay(year, month, day, color, infovar);
        self.__eventsDays.append(event);

        self.__showEventDays();

    def GetEventDays(self):
        """Recupera la lista de fechas (eventos) marcadas en color y agregadas con el metodo AddEventDay."""
        return self.__eventsDays;

    def GetSelectDay(self):
        """Recupera la fecha seleccionada por el cursor."""
        day = self.__cursorNumDay - self.pos.current.firstDayWeek;
        month, year = self.pos.current.year, self.pos.current.month;

        return day, month, year;

    def GetEventsSelected(self):
        """Recupera una lista de los eventos seleccionados por el cursor."""
        day = self.getSelectDay();

        selEvents = [];

        for event in self.__eventsDays:
            if event.year==self.pos.current.year and event.month==self.pos.current.month:
                if event.day == day:
                    selEvents.append(event);
                    
        return selEvents;
        

    def __setmonth(self, nyear, nmonth):
        self.pos = StructSelectMonth(nyear, nmonth);

        self.itemconfig("textmonthyear", text="%s - %d"%(monthnames[nmonth-1], nyear));

        idsText = sorted(self.find_withtag("dayentry"));
        idsRects = sorted(self.find_withtag("dayrect"));

        current = self.pos.current
        current.makeRanges();
        before = self.pos.before
        before.makeRanges();
            
        entrysoldmonth = idsText[:current.firstDayWeek+1];
        oldmonthdays = range(before.maxMonthDays-len(entrysoldmonth)+1, before.maxMonthDays+1);
        for nday in range(len(oldmonthdays)):
            self.itemconfig(entrysoldmonth[nday], text="%d" % oldmonthdays[nday], fill=colors["outrangedaysfg"]); 

        entrysthismonth = idsText[current.firstDayWeek+1:];
        for day in range(current.maxMonthDays):
            self.itemconfig(entrysthismonth[day], text="%d" % (day+1), fill=colors["foreground"]);

        entrysnextmonth = idsText[current.firstDayWeek + current.maxMonthDays +1:]
        
        for day in range(len(entrysnextmonth)):
            self.itemconfig(entrysnextmonth[day], text="%d" % (day+1), fill=colors["outrangedaysfg"]);

    def __changemonth_before(self, e=None, defaultdayselect=1):
            
        self.__setmonth(self.pos.before.year, self.pos.before.month);

        self.__selectday(day=defaultdayselect);
        

    def __changemonth_next(self, e=None, defaultdayselect=1):

        self.__setmonth(self.pos.next.year, self.pos.next.month);

        self.__selectday(day=defaultdayselect);
        
