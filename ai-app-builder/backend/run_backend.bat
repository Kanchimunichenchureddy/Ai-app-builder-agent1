@echo off
echo Starting AI App Builder Backend...
echo =================================

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env file with your API keys
)

REM Run the backend
echo Starting backend server...
python -m uvicorn app.main:app --host localhost --port 8000 --reload