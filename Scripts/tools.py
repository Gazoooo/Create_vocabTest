import os
import datetime as d
import sys
from babel.dates import format_date

#helper script with convenience methods

def find_quelldatei():
    files = os.listdir(find_path("Sources/"))
    quelldateien = []
    for i in files:
        if i.endswith(".db"):
            quelldateien.append(i)
    return quelldateien

def find_path(file):
    # determine if application is a script file or frozen exe + using absolute path (relative doenst work for .exe files)
    if getattr(sys, 'frozen', False):
        path_to_root = os.path.dirname(sys.executable)
    elif __file__:
        path_to_root = os.path.split(os.path.dirname(__file__))[0]
            
    specific_path = os.path.join(path_to_root, file)
    return specific_path

def datumsanzeige():
    datum_us = d.date.today()
    datum_de = format_date(datum_us, "d.M.yyyy", locale = "de_DE")
    return datum_de


#all methods below are for the GUI of Tkinter

def mittiges_fenster(fenster, breite, hoehe):
    Breite_Monitor = fenster.winfo_screenwidth()
    Hoehe_Monitor = fenster.winfo_screenheight()
    x = (Breite_Monitor / 2) - (breite / 2)
    y = (Hoehe_Monitor / 2) - (hoehe / 2)
    fenster.geometry(f"{breite}x{hoehe}+{int(x)}+{int(y)}")
    fenster.configure(bg="#181818")

def text_bearbeiten(feld, *text):
    feld.config(state="normal") #Die config - Methode kann den Status des Textfeldes ändern. Bei "Normal" kann man den Text im Feld bearbeiten.
    if len(text) >= 2:
        feld.insert("end", text[0],text[1])
    else:
        feld.insert("end", text[0])
    feld.config(state="disabled") #Bei "disabled" kann man den Text im Feld nicht bearbeiten.

def text_loeschen(*felder):
    for i in felder:
        i.config(state="normal")
        i.delete('1.0', "end")
        i.config(state="disabled")