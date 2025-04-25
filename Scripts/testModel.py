import random
import testCreator

#represents the test itself with methods for operating with the vocabs
class TestModel:
    def __init__(self, vocabinfo, db_communicator):
        """
        Initializes the TestModel with vocabinfo and a db_communicator.
        
        Args:
            vocabinfo (dict): Information about the vocabulary to be used in the test.
            db_communicator (DBCommunicator): Object responsible for communicating with the database.
        """
        self.vocabinfo = vocabinfo
        self.db_communicator = db_communicator
        self.anordnung_gruppe = {"A": [], "B": []} #2 Groups, can be changed

        #determine total number of vocabs per test
        self.vokabelanzahl = 0
        for lektion in self.vocabinfo:
            self.vokabelanzahl += int(self.vocabinfo[lektion][0].split(":")[1])

    def create_test(self):
        """
        Creates a test by choosing vocabs, mixing their order, and then starting the test creator.
        """
        self.choose_vocabsForTest()
        self.mix_orderOfVocab()
        creator = testCreator.TestCreator(self.db_communicator.wortschatz, self.vocabinfo, self.anordnung_gruppe)
        self.db_communicator.close() #closes connection to the db, see "db_communicator.py"
        creator.create_txt()
        creator.create_docx()
    
    def choose_vocabByWortart(self, wortart, lektion, ges, anordnung_gruppen):
        """
        Chooses vocabs by a given word type (wortart) and assigns them to the test groups (A and B).
        used by `choose_vocabsForTest()`.
        
        Args:
            wortart (str): The word type to choose (e.g., "subs", "verb").
            lektion (str): The lesson or vocabulary set to choose from.
            ges (dict): The complete vocabulary list.
            anordnung_gruppen (dict): The dictionary holding groups A and B where the chosen vocabs are assigned.
        
        Returns:
            dict: The updated anordnung_gruppen with new vocabs added to the groups.
        """
        index = [i for i, elem in enumerate(ges[lektion]) if wortart in elem][0]
        anzahl_der_wortart = int(ges[lektion][index].split(":")[1])
        vokabeln_der_wortart = self.db_communicator.wortartenliste(lektion, wortart)
        vokabeln_fuer_test_tmp = []

        for i in range(anzahl_der_wortart * len(anordnung_gruppen)):
            if len(vokabeln_der_wortart) == 0:
                break #if there doesnt exist any vocab from the given "Wortart"
            else:
                vok = random.choice(vokabeln_der_wortart)
                vokabeln_fuer_test_tmp.append(vok)
                #vokabeln_fuer_test_tmp.append(f"{vok} ({wortart}) ({lektion})")
                vokabeln_der_wortart.pop(vokabeln_der_wortart.index(vok)) #delete after use to avoid double use

        voc_fuer_A = vokabeln_fuer_test_tmp[:anzahl_der_wortart]
        voc_fuer_B = vokabeln_fuer_test_tmp[anzahl_der_wortart:]

        anordnung_gruppen["A"] += voc_fuer_A
        if len(voc_fuer_B) != anzahl_der_wortart: #if there are less vocabs for B too use
            for k in range(anzahl_der_wortart - len(voc_fuer_B)):
                voc = random.choice(voc_fuer_A)
                voc_fuer_A.pop(voc_fuer_A.index(voc)) #get missing vocab from A
                voc_fuer_B.append(voc)
        anordnung_gruppen["B"] += voc_fuer_B
        return anordnung_gruppen
    
    def choose_vocabsForTest(self):
        """
        Chooses vocabs from various word types (subs, verb, adje, klwo) for each lesson and groups them.
        used by `create_test()`.
        """
        for lektion in self.vocabinfo:
            self.choose_vocabByWortart("subs", lektion, self.vocabinfo, self.anordnung_gruppe)
            self.choose_vocabByWortart("verb", lektion, self.vocabinfo, self.anordnung_gruppe)
            self.choose_vocabByWortart("adje", lektion, self.vocabinfo, self.anordnung_gruppe)
            self.choose_vocabByWortart("klwo", lektion, self.vocabinfo, self.anordnung_gruppe)

    def mix_orderOfVocab(self):
        """
        Mixes the order of the vocabs in groups A and B to randomize their order.
        Ensures that the same vocab does not appear in the same position in both groups.
        used by `create_test()`.
        """
        for i in range(len(self.anordnung_gruppe["A"])):
            if self.anordnung_gruppe["A"][i] == self.anordnung_gruppe["B"][i]: #wenn gleiche Vokabel an gleicher Stelle steht...
                #...change index of vocab in A
                index = random.randint(0, len(self.anordnung_gruppe["A"]) - 1)
                while index == i:
                    index = random.randint(0, len(self.anordnung_gruppe["A"]) - 1)
                self.anordnung_gruppe["A"][i], self.anordnung_gruppe["A"][index] = self.anordnung_gruppe["A"][index], self.anordnung_gruppe["A"][i]
