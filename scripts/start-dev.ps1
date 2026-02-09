# PowerShell script to start both frontend and backend

# Get the directory where this script is located and change to project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $ScriptDir "..")

Write-Host "🚀 Starting Quote Image Generator Development Environment" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$python = $null
try {
    $python = Get-Command python -ErrorAction Stop
} catch {
    try {
        $python = Get-Command python3 -ErrorAction Stop
    } catch {
        Write-Host "❌ Python is not installed. Please install Python 3.7+" -ForegroundColor Red
        exit 1
    }
}

# Check if Node.js is installed
try {
    $null = Get-Command node -ErrorAction Stop
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js" -ForegroundColor Red
    exit 1
}

# Check if npm is installed
try {
    $null = Get-Command npm -ErrorAction Stop
} catch {
    Write-Host "❌ npm is not installed. Please install npm" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "server\venv")) {
    Write-Host "⚠️  Virtual environment not found. Creating one..." -ForegroundColor Yellow
    Set-Location server
    & $python.Name -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
    Set-Location ..
}

# Check if node_modules exists
if (-not (Test-Path "client\node_modules")) {
    Write-Host "⚠️  Frontend dependencies not found. Installing..." -ForegroundColor Yellow
    Set-Location client
    npm install
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
    Set-Location ..
}

Write-Host "📦 Starting servers..." -ForegroundColor Cyan
Write-Host ""

# Start backend in a new window
Write-Host "🔧 Starting Flask backend server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\server'; .\venv\Scripts\Activate.ps1; python app.py"

# Wait a bit for backend to start
Start-Sleep -Seconds 2

# Start frontend in a new window
Write-Host "⚛️  Starting React frontend server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\client'; npm start"

Write-Host ""
Write-Host "✅ Both servers are starting!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend:  http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Close the server windows to stop them." -ForegroundColor Yellow
Write-Host ""
