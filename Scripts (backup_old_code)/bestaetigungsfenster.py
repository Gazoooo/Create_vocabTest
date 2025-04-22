import tkinter as tk
import os as os
import tools as t

class Bestaetigungsfenster():
    def __init__(self, wortschatz, lektion, datum):
        self.bestaetigungsfenster = tk.Tk()
        self.bestaetigungsfenster.title("Hinweis")
        t.mittiges_fenster(self.bestaetigungsfenster, 500, 150)
        self.wortschatz, self.lektion, self.datum = wortschatz, lektion, datum

        self.text = tk.Label(self.bestaetigungsfenster, text = 'Der Vokabeltest befindet sich im Ordner "Output"\nJetzt öffnen?', font=("Arial", 16))
        self.text.place(x=25,y=20)

        self.ja = tk.Button(self.bestaetigungsfenster, text = "Ja", command=self.oeffnen, font=("Arial", 16))
        self.ja.place(x=100, y=100)

        self.nein = tk.Button(self.bestaetigungsfenster, text="Nein", command=self.schließen, font=("Arial", 16))
        self.nein.place(x=300, y=100)

    def start(self):
        self.bestaetigungsfenster.mainloop()

    def oeffnen(self):
        os.startfile(t.find_path(f"Output\Vokabeltest_{self.wortschatz}_L{self.lektion}_{self.datum}.docx"))
        self.bestaetigungsfenster.destroy()


    def schließen(self):
        self.bestaetigungsfenster.destroy()
