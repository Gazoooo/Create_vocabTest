import tools as t
import Eingabefenster_Anfang as e
import os

for file in os.listdir(t.find_path("Output")):
    os.remove(os.path.join(t.find_path("Output"), file))


e.Eingabefenster_Anfang().start()

