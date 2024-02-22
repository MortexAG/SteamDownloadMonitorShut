@echo off
call .\venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    goto end
)


if errorlevel 1 (
    echo Failed to change directory.
    goto end
)

pyinstaller --name SteamDownloadMonitorShut-Folders-Only --noconsole check_folders_only.py
pyinstaller --name SteamDownloadMonitorShut-Everythying --noconsole check_everything.py

:end
call .\venv\Scripts\deactivate.bat
