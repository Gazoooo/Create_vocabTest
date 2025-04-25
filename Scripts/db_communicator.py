import sqlite3

#Class with methods to retrieve and manipulate data from the given Database
class db_communicator:
    def __init__(self, path_to_DB):
        """
        Initializes the connection to the database and sets up the cursor for SQL queries.
        
        Args:
            path_to_DB (str): The path to the SQLite database file.
        """
        self.wortschatz = f'{path_to_DB[path_to_DB.rfind("/")+1:path_to_DB.rfind(".")]}' #used by "TestCreator.py"
        self.connection = sqlite3.connect(path_to_DB)
        self.pointer = self.connection.cursor()

    def daten_aus_DB(self, sql_statement):
        """
        Executes a given SQL statement and retrieves the first result.
        
        Args:
            sql_statement (str): The SQL query to execute.
        
        Returns:
            str: The result of the query, or None if no result is found.
        """
        self.pointer.execute(sql_statement)
        inhalt_raw = self.pointer.fetchone()
        if inhalt_raw is not None:
            inhalt = inhalt_raw[0]
            return inhalt
        else:
            return None

    def wortartenliste(self, lektion, wortart):
        """
        Retrieves all vocabularies of a given word type ("Wortart") from a specified lesson.
        
        Args:
            lektion (str): The lesson from which to fetch the vocabularies.
            wortart (str): The word type (e.g., "subs", "verb") to filter the vocabularies.
        
        Returns:
            list: A list of Latin words (vocabs) for the given word type.
        """
        wortartliste = []
        self.pointer.execute(f'SELECT Latein FROM Vokabeln_Lektion_{lektion} WHERE Wortart = "{wortart}"') #not using "daten_aus_db()" because of it only works with COUNT(*)(?)
        inhalt = self.pointer.fetchall()
        for i in inhalt:
            wortartliste.append(i[0])
        return wortartliste

    def create_vokabelliste(self, lektion):
        """
        Creates a list of all vocabularies from a specified lesson.
        
        Args:
            lektion (str): The lesson for which to create the vocabulary list.
        
        Returns:
            list: A list of vocabulary indices for the specified lesson.
        """
        vokabelliste = []
        vokabeln = self.daten_aus_DB(f"SELECT COUNT(*) FROM Vokabeln_Lektion_{lektion}")
        for i in range(1,vokabeln+1):
            vokabelliste.append(i)
        return vokabelliste

    def create_lektionsliste(self):
        """
        Retrieves a list of all lessons available in the database.
        
        Returns:
            list: A list of lesson identifiers (numbers) available in the database.
        """
        lektionsliste = []
        anzahl_lektionen = self.daten_aus_DB("SELECT count(*) FROM sqlite_master WHERE type = 'table'")
        for i in range(1, anzahl_lektionen+1):
            lektionsliste.append(str(i))
        return lektionsliste
    
    def close(self):
        """
        Closes the connection to the database.
        """
        self.connection.close()