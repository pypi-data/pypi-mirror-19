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

from ShockCalendar import Calendar;
from ShockCalendar import monthnames, days;
from ShockCalendar import colors;


__version__ = "0.3"
__author__ = "adrian_leonardo_05@hotmail.com.ar"
__license__ = "MIT"
