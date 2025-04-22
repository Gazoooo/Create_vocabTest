import os
import tools as t
from mainMenu_view import MainMenu_View

#delete all old files in the fodler "Output"
for file in os.listdir(t.find_path("Output")):
    os.remove(os.path.join(t.find_path("Output"), file))
    
view = MainMenu_View()
view.start()