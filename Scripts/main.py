import os
import tools as t
from mainMenu_view import MainMenu_View

#delete all old files in the folder "Output"
output_path = t.find_path("Output")
for file in os.listdir(output_path):
    path = os.path.join(output_path, file)
    print(os.path.isfile(path))
    if os.path.isfile(path):
        try:
            os.remove(path)
        except PermissionError:
            print(f"Permission denied: {path}. File might be open in another program.")
    else:
        pass # ignore file that is deleted by the program itself
    os.remove(path)
    
#start the GUI
view = MainMenu_View()
view.start()