@echo off
REM Windows Batch script to start both frontend and backend

REM Change to project root (one level up from scripts folder)
cd /d "%~dp0.."

echo 🚀 Starting Quote Image Generator Development Environment
echo.

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where python3 >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Python is not installed. Please install Python 3.7+
        exit /b 1
    )
    set PYTHON_CMD=python3
) else (
    set PYTHON_CMD=python
)

REM Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is not installed. Please install Node.js
    exit /b 1
)

REM Check if npm is installed
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ npm is not installed. Please install npm
    exit /b 1
)

REM Check if virtual environment exists
if not exist "server\venv" (
    echo ⚠️  Virtual environment not found. Creating one...
    cd server
    %PYTHON_CMD% -m venv venv
    echo ✅ Virtual environment created
    cd ..
)

REM Check if node_modules exists
if not exist "client\node_modules" (
    echo ⚠️  Frontend dependencies not found. Installing...
    cd client
    call npm install
    echo ✅ Frontend dependencies installed
    cd ..
)

REM Start backend in a new window
echo 🔧 Starting Flask backend server...
start "Backend Server" cmd /k "cd server && venv\Scripts\activate && python app.py"

REM Wait a bit for backend to start
timeout /t 2 /nobreak >nul

REM Start frontend in a new window
echo ⚛️  Starting React frontend server...
start "Frontend Server" cmd /k "cd client && npm start"

echo.
echo ✅ Both servers are starting!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:5000
echo.
echo Close the server windows to stop them, or press Ctrl+C here.
echo.

pause
