$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $PSScriptRoot

if (-not (Test-Path -LiteralPath ".\.venv")) {
  py -3.11 -m venv ".\.venv"
}

& ".\.venv\Scripts\python.exe" -m pip install -r "requirements.txt"
& ".\.venv\Scripts\python.exe" "main.py"

