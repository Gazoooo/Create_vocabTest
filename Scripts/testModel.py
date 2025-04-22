import random
import testCreator

#represents the test itself with methods for operating with the vocabs
class TestModel:
    def __init__(self, vocabinfo, db_communicator):
        self.vocabinfo = vocabinfo
        self.db_communicator = db_communicator
        self.anordnung_gruppe = {"A": [], "B": []} #2 Groups, can be changed

        #determine total number of vocabs per test
        self.vokabelanzahl = 0
        for lektion in self.vocabinfo:
            self.vokabelanzahl += int(self.vocabinfo[lektion][0].split(":")[1])

    #creates a pure model for the vocabtest by choosing the vocabs and then mixing it
    #at the end it starts the testCreator
    def create_test(self):
        self.choose_vocabsForTest()
        self.mix_orderOfVocab()
        creator = testCreator.TestCreator(self.db_communicator.wortschatz, self.vocabinfo, self.anordnung_gruppe)
        self.db_communicator.close() #closes connection to the db, see "db_communicator.py"
        creator.create_txt()
        creator.create_docx()
    
    #chooses vocabs by the given number of the different "Wortarten"
    #operating on the passed parameter "anordnung_gruppen" and retrieving it at the end
    #used by choose_vocabsForTest(self)
    def choose_vocabByWortart(self, wortart, lektion, ges, anordnung_gruppen):
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
    
    #chooses the vocabs
    #used by create_test(self)
    def choose_vocabsForTest(self):
            for lektion in self.vocabinfo:
                self.choose_vocabByWortart("subs", lektion, self.vocabinfo, self.anordnung_gruppe)
                self.choose_vocabByWortart("verb", lektion, self.vocabinfo, self.anordnung_gruppe)
                self.choose_vocabByWortart("adje", lektion, self.vocabinfo, self.anordnung_gruppe)
                self.choose_vocabByWortart("klwo", lektion, self.vocabinfo, self.anordnung_gruppe)

    #mixes the order of the vocabs
    #used by create_test(self)
    def mix_orderOfVocab(self):
        for i in range(len(self.anordnung_gruppe["A"])):
            if self.anordnung_gruppe["A"][i] == self.anordnung_gruppe["B"][i]: #wenn gleiche Vokabel an gleicher Stelle steht...
                #...change index of vocab in A
                index = random.randint(0, len(self.anordnung_gruppe["A"]) - 1)
                while index == i:
                    index = random.randint(0, len(self.anordnung_gruppe["A"]) - 1)
                self.anordnung_gruppe["A"][i], self.anordnung_gruppe["A"][index] = self.anordnung_gruppe["A"][index], self.anordnung_gruppe["A"][i]
