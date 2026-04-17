@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist ".venv" (
  py -3.11 -m venv ".venv"
)

call ".venv\Scripts\activate.bat"

python -m pip install -r requirements.txt
python main.py

endlocal

