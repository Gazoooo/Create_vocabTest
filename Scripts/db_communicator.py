import sqlite3

#Class with methods to retrieve and manipulate data from the given Database
class db_communicator:
    #connects to the DB (given path) for communication 
    def __init__(self, path_to_DB):
        self.wortschatz = f'{path_to_DB[path_to_DB.rfind("/")+1:path_to_DB.rfind(".")]}' #used by "TestCreator.py"
        self.connection = sqlite3.connect(path_to_DB)
        self.pointer = self.connection.cursor()

    #method for retrieving data from DB
    def daten_aus_DB(self, sql_statement):
        self.pointer.execute(sql_statement)
        inhalt_raw = self.pointer.fetchone()
        if inhalt_raw is not None:
            inhalt = inhalt_raw[0]
            return inhalt
        else:
            return None

    #method for getting all vocabs of a given lection and part of speech ("Wortart")
    def wortartenliste(self, lektion, wortart):
        wortartliste = []
        self.pointer.execute(f'SELECT Latein FROM Vokabeln_Lektion_{lektion} WHERE Wortart = "{wortart}"') #not using "daten_aus_db()" because of it only works with COUNT(*)(?)
        inhalt = self.pointer.fetchall()
        for i in inhalt:
            wortartliste.append(i[0])
        return wortartliste

    #method for getting the total number of all vocabs of a given lection and stores them into a list
    def create_vokabelliste(self, lektion):
        vokabelliste = []
        vokabeln = self.daten_aus_DB(f"SELECT COUNT(*) FROM Vokabeln_Lektion_{lektion}")
        for i in range(1,vokabeln+1):
            vokabelliste.append(i)
        return vokabelliste

    #method for getting all existing lections in the DB
    def create_lektionsliste(self):
        lektionsliste = []
        anzahl_lektionen = self.daten_aus_DB("SELECT count(*) FROM sqlite_master WHERE type = 'table'")
        for i in range(1, anzahl_lektionen+1):
            lektionsliste.append(str(i))
        return lektionsliste
    
    
    #closes connection to DB
    def close(self):
        self.connection.close()