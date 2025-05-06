import os
import tools as t
from mainMenu_view import MainMenu_View

#delete all old files in the folder "Output"
output_path = t.find_path("Output")
for file in os.listdir(output_path):
    path = os.path.join(output_path, file)
    if os.path.isfile(path):
        try:
            os.remove(path)
        except PermissionError:
            print(f"Permission denied: {path}. File might be open in another program.")
    os.remove(path)
    
#start the GUI
view = MainMenu_View()
view.start()