import tkinter as tk
from tkinter import ttk
import tools as t
import creater as c
import Eingabefenster_mehrere as e
from functools import partial

class Mainmenu:
    def __init__(self, quelldatei, data):

        self.data = data
        self.quelldatei = quelldatei
        self.schon_gewählte_lektion = data.split("\n")[0].split(": ")[1]
        self.values = []
        self.mainmenu = tk.Tk()
        t.mittiges_fenster(self.mainmenu, 800, 900)
        self.mainmenu.title("Vokabeltest erstellen")
        self.mainmenu.iconbitmap(t.find_path("sources/Vokabeltest.ico"))
        self.mainmenu.configure(bg="#2a3634")

        self.style = ttk.Style(self.mainmenu)
        self.style.theme_create('combostyle', settings={'TCombobox': {'configure': {'fieldbackground': '#45524f', 'background': '#d9d9d9', "foreground": "white","selectbackground": "#45524f"}}})
        self.style.theme_use('combostyle')
        self.style.configure("Custom.TLabel", font=("Arial", 16), background="#262626", foreground="white")

        self.style.configure('TCombobox.Vertical.TScrollbar', arrowsize=28, background="yellow")

        self.mainmenu.option_add("*TCombobox*Listbox*Font", "Arial -16")
        self.mainmenu.option_add("*TCombobox*Listbox*Background", '#45524f')
        self.mainmenu.option_add("*TCombobox*Listbox*Foreground", 'white')
        self.mainmenu.option_add("*TCombobox*Listbox*selectBackground", '#5b6966')
        self.mainmenu.option_add("*TCombobox*Listbox*selectForeground", 'white')

        self.meldungen = tk.Text(self.mainmenu, font=("Arial", 20), bg="#262626", fg="white", width=50, height=1)
        self.meldungen.place(x=20, y=850)
        self.meldungen.tag_config('warning', foreground="red")
        self.meldungen.tag_config('green', foreground="green")

        self.frame_db = tk.Frame(self.mainmenu, height=100, width=350, bg="#1f2423")
        self.frame_db.place(x=225, y=10)

        self.info_db = ttk.Label(self.frame_db, text=f'Gewählter Wortschatz:\n\n{self.quelldatei.split("sources/")[1].split(".db")[0]}', style="Custom.TLabel")
        self.info_db.place(x=10, y=10)

        self.anzahl_frames = 0
        self.xcord = 10
        self.ycord = 10
        self.frame_lektionen_bearbeiten = tk.Frame(self.mainmenu, bg="#1f2423", height=590, width=780)
        self.frame_lektionen_bearbeiten.place(x=10, y=150)

        self.lektionenframe = tk.Frame(self.frame_lektionen_bearbeiten, bg="grey", height=200, width=125)
        self.lektionenframe.place(x=self.xcord, y=self.ycord)
        self.anzahl_frames += 1
        self.xcord += 125 + 33.7
        self.info = tk.Label(self.lektionenframe, text=self.data, bg="lightgrey", font="Arial -12", width=15, height=7)
        self.info.place(x=5.5, y=10)
        self.lektion_bearbeiten = tk.Button(self.lektionenframe, text="Bearbeiten", command=partial(self.bearbeiten, self.info))
        self.lektion_bearbeiten.place(x=27.5, y=165)

        self.label_creater = tk.Button(self.frame_lektionen_bearbeiten, text="+",font=("Arial", 20), command=self.label_erzeugen, bg = "#0D5A20", fg = "white")
        self.label_creater.place(x=(125/2)+125, y=75)
        self.infolabels = [self.info]

        self.auswahl_bes = tk.Button(self.frame_lektionen_bearbeiten, text="Konfigurationen bestätigen.",font=("Arial", 20), bg="#077d1b", fg="white",command=self.config_bestaetigt)
        self.auswahl_bes.place(x=215, y=500)


    def label_erzeugen(self):
            self.label_creater.destroy()
            self.lektionenframe = tk.Frame(self.frame_lektionen_bearbeiten, bg="grey", height=200, width=125)
            self.lektionenframe.place(x=self.xcord,y=self.ycord)
            self.anzahl_frames += 1
            self.xcord += 125+33.7
            self.info = tk.Label(self.lektionenframe, text = "/", bg="lightgrey", font="Arial -12",width=15,height=7)
            self.info.place(x=5.5,y=10)
            self.infolabels.append(self.info)
            self.lektion_bearbeiten = tk.Button(self.lektionenframe, text="Bearbeiten", command=partial(self.bearbeiten, self.info))
            self.lektion_bearbeiten.place(x=27.5,y=165)

            if self.anzahl_frames % 5 == 0:
                self.ycord += 230
                self.xcord = 10

            self.buttonx = self.xcord + 45
            self.buttony = self.ycord + 65
            if self.anzahl_frames < 10:
                self.label_creater = tk.Button(self.frame_lektionen_bearbeiten, text="+",font=("Arial", 20), command=self.label_erzeugen, bg = "#0D5A20", fg = "white")
                self.label_creater.place(x=self.buttonx, y=self.buttony)

    def config_bestaetigt(self):
        #for labels in self.infolabels:
            #print(labels.cget("text"))
        t.text_loeschen(self.meldungen)
        ges = {}
        lecs = []
        alles_ausgefuellt = True
        print(self.infolabels)
        for label in self.infolabels:

            text_from_label = label.cget("text")
            if text_from_label != "/":
                data = text_from_label.split("\n")
                lec = data[0].split(": ")[1]
                lecs.append(lec)
                ges[lec] = data[1:]
            else:
                alles_ausgefuellt = False
        if alles_ausgefuellt:
            if len(lecs) == len(set(lecs)):
                self.mainmenu.destroy()
                c.Creater(self.quelldatei,ges).create_test()
            else:
                t.text_bearbeiten(self.meldungen, "Keine Lektion darf mehrfach vorkommen.", "warning")
        else:
            t.text_bearbeiten(self.meldungen, "Konfigurationen nicht vollständig.", "warning")

    def start(self):
        self.mainmenu.mainloop()

    def bearbeiten(self, label):
       e.Eingabefenster(self.quelldatei,label).start()

    def other_focus(self, event):
        self.meldungen.focus_set()

