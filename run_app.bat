@echo off
cd /d %~dp0


:: Start the main Python script
start cmd /k "venv\Scripts\activate && python main.py"

:: Start the Celery worker
start cmd /k "venv\Scripts\activate && celery -A celery_config worker --loglevel=info -P solo"

:: Start the Celery beat scheduler
start cmd /k "venv\Scripts\activate && celery -A celery_config beat --loglevel=info"
