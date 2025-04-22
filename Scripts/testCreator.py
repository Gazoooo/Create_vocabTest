import tools as t
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import docx as docx

#creates the .docx and .txt files for the test
class TestCreator:
    #creates the filename of the .docx and .txt files
    def __init__(self, wortschatz, all_data, anordnung_gruppe):
        self.datum = t.datumsanzeige()
        self.wortschatz = wortschatz
        self.lektionsangabe = ""
        self.vokabelanzahl = 0
        for lektion in all_data:
            self.lektionsangabe += f"{lektion}+"
            self.vokabelanzahl += int(all_data[lektion][0].split(":")[1]) #used not for filename, but later
        self.lektionsangabe = self.lektionsangabe.strip("+")
        self.filename = f"Vokabeltest_{self.wortschatz}_L{self.lektionsangabe}_{self.datum}"

        self.anordnung_gruppe = anordnung_gruppe

    #creates a .docx file containing the vocabtest and saves it under "Output\Vokabeltest\"
    def create_docx(self):
        self.doc = docx.Document()
        for gruppe in self.anordnung_gruppe:
            self.text(self.datum, 9, "Calibri", "RIGHT")
            self.text(f"({gruppe}) Vokabeltest - Lektion {self.lektionsangabe}", 9, "Calibri", "underline", "bold", "CENTER")
            self.text("Übersetzen Sie die folgenden Vokabeln und ergänzen Sie bei Nomen Genitiv Sg. und Geschlecht, bei den Verben\n""Stammformen, bei Präpositionen den Kasus, mit dem sie stehen, und bei Adjektiven und Pronomen die Genera.",9, "Calibri")
            for voc in range(self.vokabelanzahl):
                vokabel = self.anordnung_gruppe[gruppe][voc]
                if vokabel.rstrip().endswith(")"):
                    vokabel = vokabel.split('(')[0]
                self.text(f"{vokabel} {self.create_line()}", 9,"Calibri", "underline", "DISTRIBUTE")
        self.doc.save(t.find_path(f"Output/{self.filename}.docx"))

    #creates a .txt file containing the vocabtest and saves it under "Output\Vokabeltest\"
    def create_txt(self):
        file = open(t.find_path(f"Output/{self.filename}.txt"), "w")
        for gruppe in self.anordnung_gruppe:
            file.write(f"Test {gruppe}:\n\n")
            for voc in range(self.vokabelanzahl):
                vokabel = self.anordnung_gruppe[gruppe][voc]
                if vokabel.rstrip().endswith(")"):
                    vokabel = vokabel.split('(')[0]
                file.write(f"{vokabel}\n")
            file.write("\n\n")
        file.close() 

    #convenience method to write to .docx file (!)
    def text(self, text, schriftgroesse, schriftstil, *extras):
        para = self.doc.add_paragraph()
        if "RIGHT" in extras:
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if "CENTER" in extras:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if "DISTRIBUTE" in extras:
           para.alignment = WD_ALIGN_PARAGRAPH.DISTRIBUTE
        para = para.add_run(text)
        para.font.size = Pt(schriftgroesse)
        para.font.name = schriftstil
        if "underline" in extras:
            para.underline = True
        if "bold" in extras:
                para.bold = True

    #convenience method for underlining the vocabs in the docx. files (see Sources\Vorlage.png)
    def create_line(self):
        space = ""
        for i in range(100):
            space += " "
        line = space + "_"
        return line

    #b.Bestaetigungsfenster(self.wortschatz, self.lektionsangabe, self.datum).start() 


