import sqlite3
import os
import datetime as d
from babel.dates import format_date
import random


def daten_aus_DB(directionary_to_DB, sql_statement):
    verbindung = sqlite3.connect(directionary_to_DB)
    zeiger = verbindung.cursor()
    data = zeiger.execute(sql_statement)
    inhalt_raw = zeiger.fetchone()
    if inhalt_raw is not None:
        inhalt = inhalt_raw[0]
        verbindung.close()
        return inhalt
    else:
        return None

def wortartenliste(directionary_to_DB, lektion, wortart):
    wortartliste = []
    verbindung = sqlite3.connect(directionary_to_DB)
    zeiger = verbindung.cursor()
    data = zeiger.execute(f'SELECT Latein FROM Vokabeln_Lektion_{lektion} WHERE Wortart = "{wortart}"')
    inhalt = zeiger.fetchall()
    for i in inhalt:
        wortartliste.append(i[0])
    verbindung.close()
    return wortartliste

def create_vokabelliste(directionary_to_DB, lektion):
    vokabelliste = []
    vokabeln = daten_aus_DB(directionary_to_DB, f"SELECT COUNT(*) FROM Vokabeln_Lektion_{lektion}")
    for i in range(1,vokabeln+1):
        vokabelliste.append(i)

    return vokabelliste

def create_lektionsliste(directionary_to_DB):
    lektionsliste = []
    anzahl_lektionen = daten_aus_DB(directionary_to_DB, "SELECT count(*) FROM sqlite_master WHERE type = 'table'")
    for i in range(1, anzahl_lektionen+1):
        lektionsliste.append(str(i))
    return lektionsliste

def find_quelldatei():
    files = os.listdir(find_path("sources/"))
    quelldateien = []
    for i in files:
        if i.endswith(".db"):
            quelldateien.append(i)
    return quelldateien

def find_path(file):
    directionary = os.path.join(os.path.split(os.path.dirname(__file__))[0], file)
    return directionary

def datumsanzeige():
    datum_us = d.date.today()
    datum_de = format_date(datum_us, "d.M.yyyy", locale = "de_DE")
    return datum_de

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

def vokabelauswahl(wortart, lektion, ges, quelldatei, anordnung_gruppen):

    gruppen = len(anordnung_gruppen)
    index = [i for i, elem in enumerate(ges[lektion]) if wortart in elem][0]
    anzahl_der_wortart = int(ges[lektion][index].split(":")[1])
    vokabeln_der_wortart = wortartenliste(quelldatei, lektion, wortart)
    vokabeln_fuer_test_tmp = []

    for i in range(anzahl_der_wortart * gruppen):
        if len(vokabeln_der_wortart) == 0:
            break
        else:
            vok = random.choice(vokabeln_der_wortart)
            vokabeln_fuer_test_tmp.append(vok)
            #vokabeln_fuer_test_tmp.append(f"{vok} ({wortart}) ({lektion})")
            vokabeln_der_wortart.pop(vokabeln_der_wortart.index(vok))

    voc_fuer_A = vokabeln_fuer_test_tmp[:anzahl_der_wortart]
    voc_fuer_B = vokabeln_fuer_test_tmp[anzahl_der_wortart:]

    anordnung_gruppen["A"] += voc_fuer_A
    if len(voc_fuer_B) != anzahl_der_wortart:
        for k in range(anzahl_der_wortart - len(voc_fuer_B)):
            voc = random.choice(voc_fuer_A)
            voc_fuer_A.pop(voc_fuer_A.index(voc))
            voc_fuer_B.append(voc)
    anordnung_gruppen["B"] += voc_fuer_B

    return anordnung_gruppen











