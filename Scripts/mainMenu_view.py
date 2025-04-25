from functools import partial
import tkinter as tk
from tkinter import ttk
import configurate_view as cv
import tools as t
from testModel import TestModel
import db_communicator as db

class MainMenu_View:
    """
    Represents the main menu GUI for configuring and generating vocabulary tests.
    This class allows the user to select a database, configure lessons, and create tests.
    """
    def __init__(self):
        """
        Initializes the main menu GUI with components for selecting a database,
        configuring lessons, and displaying messages.

        Creates the main window and applies styling to the various GUI elements.
        Prompts the user to select a database file and sets up the initial layout.
        """
        self.root = tk.Tk()
        t.mittiges_fenster(self.root, 800, 900)
        self.root.title("Vokabeltest erstellen")
        self.icon_image = tk.PhotoImage(file=t.find_path("Sources/Vokabeltest.png"))
        self.root.iconphoto(True, self.icon_image)
        self.root.configure(bg="#2a3634")

        #for style
        self.style = ttk.Style(self.root)
        self.style.theme_create('combostyle', settings={'TCombobox': {'configure': {'fieldbackground': '#45524f', 'background': '#d9d9d9', "foreground": "white","selectbackground": "#45524f"}}})
        self.style.theme_use('combostyle')
        self.style.configure("Custom.TLabel", font=("Arial", 16), background="#262626", foreground="white")
        self.style.configure('TCombobox.Vertical.TScrollbar', arrowsize=28, background="yellow")
        self.root.option_add("*TCombobox*Listbox*Font", "Arial -16")
        self.root.option_add("*TCombobox*Listbox*Background", '#45524f')
        self.root.option_add("*TCombobox*Listbox*Foreground", 'white')
        self.root.option_add("*TCombobox*Listbox*selectBackground", '#5b6966')
        self.root.option_add("*TCombobox*Listbox*selectForeground", 'white')

        self.meldungen = tk.Text(self.root, font=("Arial", 20), bg="#262626", fg="white", width=50, height=1)
        self.meldungen.place(x=20, y=850)
        self.meldungen.tag_config('warning', foreground="red")
        self.meldungen.tag_config('green', foreground="green")

        #choosing a DB
        self.frame_db = tk.Frame(self.root, height=100, width=570, bg="#1f2423")
        self.frame_db.place(x=130, y=10)
        self.label_db = ttk.Label(self.frame_db, text="Bitte Datenbank auswählen", style="Custom.TLabel")
        self.label_db.place(x=10, y=10)
        self.db_eingabe = ttk.Combobox(self.frame_db, font=("Arial", 16), width=11)
        self.db_eingabe["values"] = t.find_quelldatei()
        self.db_eingabe.current(0)
        self.db_eingabe['state'] = 'readonly'
        self.db_eingabe.bind("<<ComboboxSelected>>", self.other_focus)
        self.db_eingabe.place(x=10, y=55)
        self.db_bestaetigen = tk.Button(self.frame_db, text="Datei bestätigen.", font=("Arial", 20), bg="#2f4731", fg="white", command=self.show_more)
        self.db_bestaetigen.place(x=310, y=30)

    def show_more(self):
        """
        Displays the GUI elements needed to configure lessons after the database
        has been selected by the user.

        Creates frames for lesson configuration, adds buttons for creating new
        lesson labels, and handles database communication.
        """
        self.quelldatei = t.find_path(f"Sources/{self.db_eingabe.get()}") #saves the User-chosen DB
        #self.info_db = ttk.Label(self.frame_db, text=f'Gewählter Wortschatz:\n\n{self.quelldatei.split("Sources/")[1].split(".db")[0]}', style="Custom.TLabel")
        #self.info_db.place(x=10, y=10)
        self.db_communicator = db.db_communicator(self.quelldatei) #creating the right db_communicator

        self.anzahl_frames = 0
        self.xcord = 10
        self.ycord = 10
        self.frame_lektionen_bearbeiten = tk.Frame(self.root, bg="#1f2423", height=590, width=780)
        self.frame_lektionen_bearbeiten.place(x=10, y=150)

        self.label_creater = tk.Button(self.frame_lektionen_bearbeiten, text="+",font=("Arial", 20), command=self.label_erzeugen, bg = "#0D5A20", fg = "white")
        self.label_creater.place(x=125/2, y=75)
        self.infolabels = []

        self.auswahl_bes = tk.Button(self.frame_lektionen_bearbeiten, text="Konfigurationen bestätigen.",font=("Arial", 20), bg="#077d1b", fg="white",command=self.config_bestaetigt)
        self.auswahl_bes.place(x=215, y=500)

    def label_erzeugen(self):
        """
        Creates a new label for configuring a new lesson.

        Adds a frame to the GUI for configuring a lesson and displays a button for editing.
        The labels are arranged in rows, and new rows are added when necessary.
        """
        self.label_creater.destroy()
        self.lektionenframe = tk.Frame(self.frame_lektionen_bearbeiten, bg="grey", height=200, width=125)
        self.lektionenframe.place(x=self.xcord,y=self.ycord)
        self.anzahl_frames += 1
        self.xcord += 125+33.7
        self.info = tk.Label(self.lektionenframe, text = "/", bg="lightgrey", font="Arial -12",width=15,height=7)
        self.info.place(x=5.5,y=10)
        self.infolabels.append(self.info) #store the data for one label
        self.lektion_bearbeiten = tk.Button(self.lektionenframe, text="Bearbeiten", command=partial(self.config_lec, self.info)) #partal for using 2 parameters
        self.lektion_bearbeiten.place(x=27.5,y=165)

        #the labels on the GUI are always in rows of 5
        if self.anzahl_frames % 5 == 0:
            self.ycord += 230
            self.xcord = 10
        self.buttonx = self.xcord + 45
        self.buttony = self.ycord + 65
        if self.anzahl_frames < 10:
            self.label_creater = tk.Button(self.frame_lektionen_bearbeiten, text="+",font=("Arial", 20), command=self.label_erzeugen, bg = "#0D5A20", fg = "white")
            self.label_creater.place(x=self.buttonx, y=self.buttony)

    def config_lec(self, label):
        """
        Opens the configuration view for a specific lesson.

        Passes the selected lesson and its data to the configurate view for editing.
        
        Args:
            label (tk.Label): The label representing the lesson to be configured.
        """
        cv.Configurate_View(self.quelldatei, label, self.db_communicator).start()

    def config_bestaetigt(self):
        """
        Confirms the configuration of all lessons and creates the test model.

        Gathers the data from the configured lessons, checks for any errors (e.g., duplicate lessons),
        and creates a test model based on the configuration.
        """
        t.text_loeschen(self.meldungen)

        all_data = {}
        lecs = []
        continue_ = True
        for label in self.infolabels:
            text_from_label = label.cget("text")
            if text_from_label == "/": #if one label exists, which is not configured
                 t.text_bearbeiten(self.meldungen, "Konfigurationen nicht vollständig.", "warning")
                 continue_ = False
                 break
            
            data = text_from_label.split("\n")
            lec = data[0].split(": ")[1]
            lecs.append(lec)
            all_data[lec] = data[1:]
            if len(lecs) != len(set(lecs)): #if lection is doubled
                t.text_bearbeiten(self.meldungen, "Keine Lektion darf mehrfach vorkommen.", "warning")
                continue_ = False
                break
            
        if continue_:
            self.root.destroy()
            model = TestModel(all_data, self.db_communicator)
            model.create_test()


    def other_focus(self, event):
        """
        Focuses the text widget when a combobox selection is made.
        Ensures that the message area is active after a combobox selection.
        
        Args:
            event (tk.Event): The event triggered by the combobox selection.
        """
        self.meldungen.focus_set()

    def start(self):
        """
        Starts the Tkinter main loop to display the GUI.

        This method keeps the application running, allowing user interaction with the GUI.
        """
        self.root.mainloop()