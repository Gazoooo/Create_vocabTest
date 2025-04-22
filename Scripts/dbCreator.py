from openpyxl import load_workbook
import sqlite3
import tools as t
import os
from tkinter import Tk, filedialog

#Class to creates Sqllite Databases from given Excel worksheets, started separately by "new_DB.bat"

class dbCreator:
    #loads Excel Workbook from User-chosen file
    def __init__(self):
        root = Tk()
        root.withdraw()
        self.file = filedialog.askopenfilename(title="Bitte Datei auswählen", initialdir=t.find_path("Sources"),filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*')))
        workbook = load_workbook(self.file)
        self.sheet = workbook.active

    #establishes a connection to the new DB
    def get_connection(self):

        if (self.file != "") and (self.sheet["A"][0].value != "Lektion" or self.sheet["B"][0].value != "lat" or self.sheet["C"][0].value != "art"):
            print("Datenbank wurde nicht erstellt. Bitte folgende Reihenfolge der Tabelle beachten:\nLektion - lat - art")
        else:
            name_of_new_DB = f'{self.file[:self.file.rfind(".")]}.db'
            if os.path.isfile(t.find_path(name_of_new_DB)):
                os.remove(t.find_path(name_of_new_DB))
            self.connection = sqlite3.connect(name_of_new_DB)

    #creates DB with the given connection
    def create_DB(self):
        pointer = self.connection.cursor()

        num_lecs = []
        for lecs in self.sheet["A"]:
            num_lecs.append(lecs.value)
        num_lecs.pop(0)
        for i in range(1, max(num_lecs)+1):
            pointer.execute(f'CREATE TABLE "Vokabeln_Lektion_{i}" ("Latein" TEXT, "Wortart" TEXT, PRIMARY KEY("Latein") )')

        for value in self.sheet.iter_rows(min_col=1,max_col=3,values_only=True):
            if value[0] == "Lektion":
                pass
            else:
                lektion = value[0]
                vokabel = value[1]
                wortart = value[2]
                pointer.execute(f'INSERT INTO Vokabeln_Lektion_{lektion} VALUES ("{vokabel}", "{wortart}")')
                self.connection.commit()

        self.connection.close()

#main Code for executing
creator = dbCreator()
creator.get_connection()
creator.create_DB()