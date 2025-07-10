@echo off
echo Installing AI Data Analyst Dashboard...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo Please edit .env file and add your OpenAI API key before running the application.
)

echo.
echo Installation complete!
echo.
echo To run the application:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: streamlit run app.py
echo.
pause
