import tkinter as tk
from tkinter import ttk
import tools as t
import menu as m
import creater as c

class Eingabefenster_Anfang:
    def __init__(self):

       self.eingabefenster = tk.Tk()
       t.mittiges_fenster(self.eingabefenster, 800, 900)
       self.eingabefenster.title(f"Vokabeltest erstellen")
       self.eingabefenster.iconbitmap(t.find_path("sources/Vokabeltest.ico"))
       self.eingabefenster.configure(bg="#2a3634")

       self.style = ttk.Style(self.eingabefenster)
       self.style.theme_create('combostyle', settings={'TCombobox': {
           'configure': {'fieldbackground': '#45524f', 'background': '#d9d9d9', "foreground": "white",
                         "selectbackground": "#45524f"}}})
       self.style.theme_use('combostyle')
       self.style.configure("Custom.TLabel", font=("Arial", 16), background="#262626", foreground="white")

       self.style.configure('TCombobox.Vertical.TScrollbar', arrowsize=28, background="yellow")

       self.eingabefenster.option_add("*TCombobox*Listbox*Font", "Arial -16")
       self.eingabefenster.option_add("*TCombobox*Listbox*Background", '#45524f')
       self.eingabefenster.option_add("*TCombobox*Listbox*Foreground", 'white')
       self.eingabefenster.option_add("*TCombobox*Listbox*selectBackground", '#5b6966')
       self.eingabefenster.option_add("*TCombobox*Listbox*selectForeground", 'white')

       self.meldungen = tk.Text(self.eingabefenster, font=("Arial", 20), bg="#262626", fg="white", width=50, height=1)
       self.meldungen.place(x=20, y=850)
       self.meldungen.tag_config('warning', foreground="red")
       self.meldungen.tag_config('green', foreground="green")

       self.frame_db = tk.Frame(self.eingabefenster, height=200, width=370, bg="#1f2423")
       self.frame_db.place(x=10, y=10)

       self.label_db = ttk.Label(self.frame_db, text="Bitte Datenbank auswählen", style="Custom.TLabel")
       self.label_db.place(x=10, y=10)

       self.db_eingabe = ttk.Combobox(self.frame_db, font=("Arial", 16), width=11)
       self.db_eingabe["values"] = t.find_quelldatei()
       self.db_eingabe.current(0)
       self.db_eingabe['state'] = 'readonly'
       self.db_eingabe.bind("<<ComboboxSelected>>", self.other_focus)
       self.db_eingabe.place(x=10, y=55)

       self.db_bestaetigen = tk.Button(self.frame_db, text="Datei bestätigen.", font=("Arial", 20), bg="#2f4731",
                                       fg="white", command=self.lektion_auswahl)
       self.db_bestaetigen.place(x=70, y=130)

    def lektion_auswahl(self):

        self.quelldatei = t.find_path(f"sources/{self.db_eingabe.get()}")

        self.lektionauswahl_frame = tk.Frame(self.eingabefenster, height=200, width=390, bg="#1f2423")
        self.lektionauswahl_frame.place(x=400, y=10)

        self.lektionenlabel = ttk.Label(self.lektionauswahl_frame, text = "Bitte gewünschte Lektion auswählen.", style="Custom.TLabel")
        self.lektionenlabel.place(x=10, y=10)

        self.lektionenbestaetigen = tk.Button(self.lektionauswahl_frame, text="Bestätigen", font=("Arial", 20),
                                              bg="#2f4731", fg="white", command=self.vokabelanzahl_auswahl)
        self.lektionenbestaetigen.place(x=70, y=130)

        self.lektionenliste = ttk.Combobox(self.lektionauswahl_frame, font=("Arial", 16), width=11)
        self.lektionenliste["values"] = t.create_lektionsliste(t.find_path(self.quelldatei))
        self.lektionenliste.current(0)
        self.lektionenliste['state'] = 'readonly'
        self.lektionenliste.bind("<<ComboboxSelected>>", self.other_focus)
        self.lektionenliste.place(x=10, y=55)


    def vokabelanzahl_auswahl(self):

        self.lektion = self.lektionenliste.get()

        self.frame_vokabelanzahl = tk.Frame(self.eingabefenster, height=100, width=780, bg="#1f2423")
        self.frame_vokabelanzahl.place(x=10, y=230)

        self.Label_vokabelanzahl = ttk.Label(self.frame_vokabelanzahl, text="Bitte Vokabelanzahl eingeben.", style="Custom.TLabel")
        self.Label_vokabelanzahl.place(x=10, y=10)

        self.vokabelanzahl_eingabe = ttk.Combobox(self.frame_vokabelanzahl, font=("Arial", 16), width=10)
        self.vokabelanzahl_eingabe["values"] = t.create_vokabelliste(self.quelldatei, self.lektion)
        if len(t.create_vokabelliste(self.quelldatei, int(self.lektion))) >= 10:
           self.vokabelanzahl_eingabe.current(4)
        else:
           self.vokabelanzahl_eingabe.current(0)

        self.vokabelanzahl_eingabe['state'] = 'readonly'
        self.vokabelanzahl_eingabe.bind("<<ComboboxSelected>>", self.other_focus)
        self.vokabelanzahl_eingabe.place(x=10, y=60)

        self.vokabelanzahl_bestaetigen = tk.Button(self.frame_vokabelanzahl, text="Vokabelanzahl bestätigen.",
                                                  font=("Arial", 20), bg="#2f4731", fg="white",
                                                  command=self.wortart_auswahl)
        self.vokabelanzahl_bestaetigen.place(x=400, y=10)


    def wortart_auswahl(self):

        self.vokabelanzahl = self.vokabelanzahl_eingabe.get()

        self.frame_wortarten = tk.Frame(self.eingabefenster, height=450, width=780, bg="#1f2423")
        self.frame_wortarten.place(x=10, y=350)
        self.Label_wortarten = ttk.Label(self.frame_wortarten, text="Bitte gewünschte Wortarten eingeben.", style="Custom.TLabel")
        self.Label_wortarten.place(x=170, y=170)

        self.anzahl_subs = 0
        self.subszähler = tk.StringVar(self.frame_wortarten)
        self.subszähler.set(f"Anzahl Substantive: {self.anzahl_subs}")
        self.subs_info = ttk.Label(self.frame_wortarten, textvariable=self.subszähler, style="Custom.TLabel")
        self.subs_info.place(x=10, y=250)

        self.anzahl_verb = 0
        self.verbzähler = tk.StringVar(self.frame_wortarten)
        self.verbzähler.set(f"Anzahl Verben: {self.anzahl_verb}")
        self.verb_info = ttk.Label(self.frame_wortarten, style="Custom.TLabel", textvariable=self.verbzähler)
        self.verb_info.place(x=400, y=250)

        self.anzahl_adj = 0
        self.adjzähler = tk.StringVar(self.frame_wortarten)
        self.adjzähler.set(f"Anzahl Adjektive: {self.anzahl_adj}")
        self.adj_info = ttk.Label(self.frame_wortarten, style="Custom.TLabel", textvariable=self.adjzähler)
        self.adj_info.place(x=10, y=350)

        self.anzahl_klwo = 0
        self.klwozähler = tk.StringVar(self.frame_wortarten)
        self.klwozähler.set(f"Anzahl kleine Wörter: {self.anzahl_klwo}")
        self.klwo_info = ttk.Label(self.frame_wortarten, style="Custom.TLabel", textvariable=self.klwozähler)
        self.klwo_info.place(x=400, y=350)

        self.button_minus_subs = tk.Button(self.frame_wortarten, text="-", font=("Arial", 16), bg="#262626", fg="white",
                                           command=lambda: self.eingabe_anzahl_wortarten("Substantiv", "-1"))
        self.button_minus_subs.place(x=10, y=290)
        self.button_plus1 = tk.Button(self.frame_wortarten, text="+", font=("Arial", 16), bg="#262626", fg="white",
                                      command=lambda: self.eingabe_anzahl_wortarten("Substantiv", "+1"))
        self.button_plus1.place(x=50, y=290)

        self.button_minus_verb = tk.Button(self.frame_wortarten, text="-", font=("Arial", 16), bg="#262626", fg="white",
                                           command=lambda: self.eingabe_anzahl_wortarten("Verb", "-1"))
        self.button_minus_verb.place(x=400, y=290)
        self.button_plus_verb = tk.Button(self.frame_wortarten, text="+", font=("Arial", 16), bg="#262626", fg="white",
                                          command=lambda: self.eingabe_anzahl_wortarten("Verb", "+1", ))
        self.button_plus_verb.place(x=440, y=290)

        self.button_minus_adj = tk.Button(self.frame_wortarten, text="-", font=("Arial", 16), bg="#262626", fg="white",
                                          command=lambda: self.eingabe_anzahl_wortarten("Adjektiv", "-1"))
        self.button_minus_adj.place(x=10, y=390)
        self.button_plus_adj = tk.Button(self.frame_wortarten, text="+", font=("Arial", 16), bg="#262626", fg="white",
                                         command=lambda: self.eingabe_anzahl_wortarten("Adjektiv", "+1"))
        self.button_plus_adj.place(x=50, y=390)

        self.button_minus_klwo = tk.Button(self.frame_wortarten, text="-", font=("Arial", 16), bg="#262626", fg="white",
                                           command=lambda: self.eingabe_anzahl_wortarten("Kleines Wort", "-1"))
        self.button_minus_klwo.place(x=400, y=390)
        self.button_plus_klwo = tk.Button(self.frame_wortarten, text="+", font=("Arial", 16), bg="#262626", fg="white",
                                          command=lambda: self.eingabe_anzahl_wortarten("Kleines Wort", "+1"))
        self.button_plus_klwo.place(x=440, y=390)

        self.wortart_bestaetigen = tk.Button(self.frame_wortarten, text="Vokabeltest erstellen.", font=("Arial", 20), bg="#077d1b", fg="white", relief="raised", command=self.bestaetigen)
        self.wortart_bestaetigen.place(x=440, y=25)

        self.wortart_bestaetigen_mehr = tk.Button(self.frame_wortarten, text="Mehrere Lektionen.", font=("Arial", 20),
                                             bg="#077d1b", fg="white", relief="raised", command=self.bestaetigen_mehr)
        self.wortart_bestaetigen_mehr.place(x=440, y=90)

        self.substantive = t.wortartenliste(self.quelldatei, self.lektion, "subs")
        self.verben = t.wortartenliste(self.quelldatei, self.lektion, "verb")
        self.adjektive = t.wortartenliste(self.quelldatei, self.lektion, "adje")
        self.kleines_wort = t.wortartenliste(self.quelldatei, self.lektion, "klwo")
        self.label_info = ttk.Label(self.frame_wortarten, text=(
            f'In den Vokabeln der Lektion {self.lektion} sind:\n{len(self.substantive)} Substantive,\n{len(self.verben)} Verben,\n{len(self.adjektive)} Adjektive\nund {len(self.kleines_wort)} kleine Wörter.'),
                                    style="Custom.TLabel")
        self.label_info.place(x=10, y=10)

    def eingabe_anzahl_wortarten(self, wortart, rechnung):


        t.text_loeschen(self.meldungen)

        if wortart == "Substantiv":
            self.anzahl_subs += int(rechnung)
            if self.anzahl_subs + self.anzahl_verb + self.anzahl_adj + self.anzahl_klwo > int(self.vokabelanzahl) or self.anzahl_subs > len(self.substantive):
                self.anzahl_subs -= 1
            if self.anzahl_subs < 0:
                self.anzahl_subs = 0
            self.subszähler.set(f"Anzahl Substantive: {self.anzahl_subs}")

        if wortart == "Verb":
            self.anzahl_verb += int(rechnung)
            if self.anzahl_subs + self.anzahl_verb + self.anzahl_adj + self.anzahl_klwo > int(self.vokabelanzahl) or self.anzahl_verb > len(self.verben):
                self.anzahl_verb -= 1
            if self.anzahl_verb < 0:
                self.anzahl_verb = 0
            self.verbzähler.set(f"Anzahl Verben: {self.anzahl_verb}")

        if wortart == "Adjektiv":
            self.anzahl_adj += int(rechnung)
            if self.anzahl_subs + self.anzahl_verb + self.anzahl_adj + self.anzahl_klwo > int(self.vokabelanzahl) or self.anzahl_adj > len(self.adjektive):
                self.anzahl_adj -= 1
            if self.anzahl_adj < 0:
                self.anzahl_adj = 0
            self.adjzähler.set(f"Anzahl Adjektive: {self.anzahl_adj}")

        if wortart == "Kleines Wort":
            self.anzahl_klwo += int(rechnung)
            if self.anzahl_subs + self.anzahl_verb + self.anzahl_adj + self.anzahl_klwo > int(self.vokabelanzahl) or self.anzahl_klwo > len(self.kleines_wort):
                self.anzahl_klwo -= 1
            if self.anzahl_klwo < 0:
                self.anzahl_klwo = 0
            self.klwozähler.set(f"Anzahl kleine Wörter: {self.anzahl_klwo}")

    def bestaetigen_mehr(self):
        if self.anzahl_subs + self.anzahl_verb + self.anzahl_adj + self.anzahl_klwo == int(self.vokabelanzahl):
            self.data = f"Lektion: {self.lektion}\nAnzahl Vokabeln: {self.vokabelanzahl}\nAnzahl subs: {self.anzahl_subs}\nAnzahl verb: {self.anzahl_verb}\nAnzahl adje: {self.anzahl_adj}\nAnzahl klwo: {self.anzahl_klwo}"
            self.eingabefenster.destroy()
            m.Mainmenu(self.quelldatei, self.data).start()
        else:
            t.text_loeschen(self.meldungen)
            t.text_bearbeiten(self.meldungen,f"Es werden {self.vokabelanzahl} Vokabeln benötigt.", "warning")

    def bestaetigen(self):
        ges = {}
        if self.anzahl_subs + self.anzahl_verb + self.anzahl_adj + self.anzahl_klwo == int(self.vokabelanzahl):
            data = f"Anzahl Vokabeln: {self.vokabelanzahl}\nAnzahl subs: {self.anzahl_subs}\nAnzahl verb: {self.anzahl_verb}\nAnzahl adje: {self.anzahl_adj}\nAnzahl klwo: {self.anzahl_klwo}".split("\n")
            ges[self.lektion] = data
            c.Creater(self.quelldatei, ges).create_test()
            self.eingabefenster.destroy()

        else:
            t.text_loeschen(self.meldungen)
            t.text_bearbeiten(self.meldungen,f"Es werden {self.vokabelanzahl} Vokabeln benötigt.", "warning")

    def other_focus(self, event):
        self.meldungen.focus_set()

    def start(self):
        self.eingabefenster.mainloop()

