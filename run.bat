@echo off
echo Starting AI Data Analyst Dashboard...

REM Check if virtual environment exists
if not exist venv (
    echo Virtual environment not found. Please run install.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist .env (
    echo .env file not found. Creating from template...
    copy .env.example .env
    echo Please edit .env file and add your OpenAI API key.
    pause
)

REM Start the application
echo Starting Streamlit application...
streamlit run app.py

pause
