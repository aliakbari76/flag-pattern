@echo off
cd /d %~dp0

:: Install dependencies from requirements.txt
start cmd /k "venv\Scripts\activate && pip install -r requirements.txt"