::A Script to automatically convert .py files to .exe and make it ready-to-distribute

::-----execution----------
::has to be in same folder as "Scripts" and "Sources" Folder
:: ./py2exe.bat (only on windows)


@echo off

Set foldername="ready-to-distribute"

RD /s /q %~dp0\%foldername% >nul 2>&1

echo Converting to .exe...
pyinstaller --onefile -w "Scripts/main.py" >nul 2>&1
echo Finished successfully.


echo Making ready-to-distribute-folder...
::Additional files can be added
::xcopy /q /e /c "C:\Program Files\ffmpeg\bin\ffmpeg.exe" %~dp0\%foldername%\
xcopy /q /e /i /c %~dp0\Output\ %~dp0\%foldername%\Output\
xcopy /q /c %~dp0\Sources\ %~dp0\%foldername%\Sources\
xcopy /q /c %~dp0\dist\main.exe %~dp0\%foldername%\ 

::clear up
RD /s /q %~dp0\dist >nul 2>&1
RD /s /q %~dp0\build >nul 2>&1
del /s %~dp0\main.spec >nul 2>&1

echo Finished successfully. Folder located in %~dp0.

pause >nul 2>&1

::automatically zip with tar.exe -caf