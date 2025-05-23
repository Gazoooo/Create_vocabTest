#represents the GUI for configurate one lection

import tkinter as tk
from tkinter import ttk
import tools as t

class Configurate_View:
    """
    A class that represents the configuration view for a lesson, allowing users to select a lesson,
    specify the number of words, and choose word types (nouns, verbs, adjectives, etc.).
    """
    
    def __init__(self, quelldatei, label, db_communicator):
        """
        Initialize the Configurate_View class with the provided parameters and set up the GUI.
        
        Args:
            quelldatei (str): The source file associated with the configuration.
            label (tk.Label): The label used to display configuration details.
            db_communicator (object): The object responsible for interacting with the database.
        """
        self.quelldatei = quelldatei
        self.label = label
        self.db_communicator = db_communicator

        self.root = tk.Toplevel()
        t.mittiges_fenster(self.root, 800, 900)
        self.root.title(f"Lektion konfigurieren")
        self.icon_image = tk.PhotoImage(file=t.find_path("Sources/Vokabeltest.png"))
        self.root.iconphoto(True, self.icon_image)
        self.root.configure(bg="#2a3634")

        #for style (just use from MainMenu_View)
        self.style = ttk.Style()
        self.style.theme_use('combostyle')


        self.meldungen = tk.Text(self.root, font=("Arial", 20), bg="#262626", fg="white", width=50, height=1)
        self.meldungen.place(x=20, y=850)
        self.meldungen.tag_config('warning', foreground="red")
        self.meldungen.tag_config('green', foreground="green")

        self.lektionauswahl_frame = tk.Frame(self.root, height=200, width=390, bg="#1f2423")
        self.lektionauswahl_frame.place(x=200, y=10)

        self.lektionenlabel = ttk.Label(self.lektionauswahl_frame, text="Bitte gewünschte Lektion auswählen.", style="Custom.TLabel")
        self.lektionenlabel.place(x=10, y=10)

        self.lektionenbestaetigen = tk.Button(self.lektionauswahl_frame, text="Bestätigen", font=("Arial", 20),
                                                    bg="#2f4731", fg="white", command=self.vokabelanzahl_auswahl)
        self.lektionenbestaetigen.place(x=70, y=130)

        self.lektionenliste = ttk.Combobox(self.lektionauswahl_frame, font=("Arial", 16), width=11)
        self.lektionenliste["values"] = self.db_communicator.create_lektionsliste()
        self.lektionenliste.current(0)
        self.lektionenliste['state'] = 'readonly'
        self.lektionenliste.bind("<<ComboboxSelected>>", self.other_focus)
        self.lektionenliste.place(x=10, y=55)

    def vokabelanzahl_auswahl(self):
        """
        Display a frame to allow the user to choose the number of words for the lesson. It also
        creates a combobox for selecting the word count.

        This method is called when the user confirms their lesson choice.
        """
        self.lektion = self.lektionenliste.get()

        self.frame_vokabelanzahl = tk.Frame(self.root, height=100, width=780, bg="#1f2423")
        self.frame_vokabelanzahl.place(x=10, y=230)

        self.Label_vokabelanzahl = ttk.Label(self.frame_vokabelanzahl, text="Bitte Vokabelanzahl eingeben.",
                                             style="Custom.TLabel")
        self.Label_vokabelanzahl.place(x=10, y=10)

        self.vokabelanzahl_eingabe = ttk.Combobox(self.frame_vokabelanzahl, font=("Arial", 16), width=10)
        self.vokabelanzahl_eingabe["values"] = self.db_communicator.create_vokabelliste(self.lektion)
        if len(self.vokabelanzahl_eingabe["values"]) >= 10:
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
        """
        Display a frame to allow the user to select the word types (nouns, verbs, adjectives, etc.).
        It includes buttons to increment or decrement the count for each word type.
        """
        self.vokabelanzahl = self.vokabelanzahl_eingabe.get()

        self.frame_wortarten = tk.Frame(self.root, height=450, width=780, bg="#1f2423")
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

        self.wortart_bestaetigen = tk.Button(self.frame_wortarten, text="Konfiguration bestätigen.", font=("Arial", 20), bg="#077d1b", fg="white", relief="raised", command=self.bestaetigen)
        self.wortart_bestaetigen.place(x=440, y=50)

        self.substantive = self.db_communicator.wortartenliste(self.lektion, "subs")
        self.verben = self.db_communicator.wortartenliste(self.lektion, "verb")
        self.adjektive = self.db_communicator.wortartenliste(self.lektion, "adje")
        self.kleines_wort = self.db_communicator.wortartenliste(self.lektion, "klwo")
        self.label_info = ttk.Label(self.frame_wortarten, text=(f'In den Vokabeln der Lektion {self.lektion} sind:\n{len(self.substantive)} Substantive,\n{len(self.verben)} Verben,\n{len(self.adjektive)} Adjektive\nund {len(self.kleines_wort)} kleine Wörter.'),style="Custom.TLabel")
        self.label_info.place(x=10, y=10)

    def eingabe_anzahl_wortarten(self, wortart, rechnung):
        """
        Update the count of selected word types (e.g., nouns, verbs) based on the user's action (increment or decrement).

        Args:
            wortart (str): The type of word (e.g., 'Substantiv', 'Verb').
            anzahl (str): The amount to adjust the count (e.g., "+1", "-1").
        """
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

    def bestaetigen(self):
        """
        Start the vocabulary test based on the selected lesson and word types.
        """
        if self.anzahl_subs + self.anzahl_verb + self.anzahl_adj + self.anzahl_klwo == int(self.vokabelanzahl):
            data = f"Lektion: {self.lektion}\nAnzahl Vokabeln: {self.vokabelanzahl}\nAnzahl subs: {self.anzahl_subs}\nAnzahl verb: {self.anzahl_verb}\nAnzahl adje: {self.anzahl_adj}\nAnzahl klwo: {self.anzahl_klwo}"
            self.label.config(text = data)
            self.root.destroy()

        else:
            t.text_loeschen(self.meldungen)
            t.text_bearbeiten(self.meldungen,f"Es werden {self.vokabelanzahl} Vokabeln benötigt.", "warning")

    def other_focus(self, event):
        """
        Handle focus change events (such as user interaction with the comboboxes).
        """
        self.meldungen.focus_set()

    def start(self):
        """starts tkinter mainloop to display the GUI
        """
        self.root.mainloop()
