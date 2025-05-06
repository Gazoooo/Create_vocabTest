import os
import datetime as d
import sys
from babel.dates import format_date

#helper script with convenience methods

def find_quelldatei():
    """
    Finds and returns a list of source files with a '.db' extension.
    
    Returns:
        list: A list of source files with a '.db' extension.
    """
    files = os.listdir(find_path("Sources/"))
    quelldateien = []
    for i in files:
        if i.endswith(".db"):
            quelldateien.append(i)
    return quelldateien

def find_path(file):
    """
    Determines the absolute path of a file/dir, handling both script and frozen executable scenarios.
    Creates base directory if not exists.
    
    Args:
        file (str): The relative file path.
    
    Returns:
        str: The absolute path to the file.
    """
    if getattr(sys, 'frozen', False):
        path_to_root = os.path.dirname(sys.executable)
    elif __file__:
        path_to_root = os.path.split(os.path.dirname(__file__))[0]
            
    specific_path = os.path.join(path_to_root, file)
    if os.path.splitext(specific_path)[1]:  # is file
        os.makedirs(os.path.dirname(specific_path), exist_ok=True)
    else:
        os.makedirs(specific_path, exist_ok=True) # is dir
    #print(f"Path: {specific_path}")
    return specific_path

def datumsanzeige():
    """
    Returns the current date formatted in the German style (d.M.yyyy).
    
    Returns:
        str: The current date in German format.
    """
    datum_us = d.date.today()
    datum_de = format_date(datum_us, "d.M.yyyy", locale = "de_DE")
    return datum_de


#----------------------all methods below are for the GUI of Tkinter--------------------------

def mittiges_fenster(fenster, breite, hoehe):
    """
    Centers the given Tkinter window on the screen and sets its background color.
    
    Args:
        fenster (Tkinter.Tk): The Tkinter window to be centered.
        breite (int): The width of the window.
        hoehe (int): The height of the window.
    """
    Breite_Monitor = fenster.winfo_screenwidth()
    Hoehe_Monitor = fenster.winfo_screenheight()
    x = (Breite_Monitor / 2) - (breite / 2)
    y = (Hoehe_Monitor / 2) - (hoehe / 2)
    fenster.geometry(f"{breite}x{hoehe}+{int(x)}+{int(y)}")
    fenster.configure(bg="#181818")

def text_bearbeiten(feld, *text):
    """
    Modifies the text in a Tkinter Text widget, allowing the insertion of new text.
    
    Args:
        feld (Tkinter.Text): The text field to modify.
        *text: Text to be inserted into the text field.
    """
    feld.config(state="normal") #Die config - Methode kann den Status des Textfeldes ändern. Bei "Normal" kann man den Text im Feld bearbeiten.
    if len(text) >= 2:
        feld.insert("end", text[0],text[1])
    else:
        feld.insert("end", text[0])
    feld.config(state="disabled") #Bei "disabled" kann man den Text im Feld nicht bearbeiten.

def text_loeschen(*felder):
    """
    Clears the content of one or more Tkinter Text widgets.
    
    Args:
        *felder: One or more Text widgets to be cleared.
    """
    for i in felder:
        i.config(state="normal")
        i.delete('1.0', "end")
        i.config(state="disabled")