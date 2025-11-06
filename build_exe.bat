@echo off
echo Building FileWatchPro.exe ...
python -m PyInstaller --noconsole --onefile --name "FileWatchPro" main.py
echo Done! Your EXE is in the "dist" folder.
pause
