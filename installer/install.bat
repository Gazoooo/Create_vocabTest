@echo off
::Adminrechte benötigt

set version="3.9.0"

echo Installing Python from Web...
curl https://www.python.org/ftp/python/%version%/python-%version%.exe -o python-%version%.exe
python-%version%.exe /passive InstallAllUsers=1 TargetDir=%cd%\Python%version%
echo Install successful!

echo Install required modules using pip...
cd Python%version%
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
echo All required modules installed successfully. 

echo Install DB Browser for sqllite...
curl https://download.sqlitebrowser.org/DB.Browser.for.SQLite-3.12.2-win32.msi -o DB.Browser.for.SQLite-3.12.2-win32.msi
Msiexec /i DB.Browser.for.SQLite-3.12.2-win32.msi /passive INSTALLDIR="%cd%\DB Browser for sqllite"

echo Installation successful. Press Enter to exit 

pause > nul 2>&1