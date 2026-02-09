# Development Scripts Guide

This project includes several scripts to quickly start both the frontend and backend development servers.

## Quick Start

### Option 1: Platform-Specific Scripts (Recommended)

**Linux/macOS:**
```bash
./scripts/start-dev.sh
```

**Windows PowerShell:**
```powershell
.\scripts\start-dev.ps1
```

**Windows Command Prompt:**
```cmd
scripts\start-dev.bat
```

### Option 2: Using npm (Cross-Platform)

First, install the root dependencies:
```bash
npm install
```

Then start both servers:
```bash
npm run dev
```

## What the Scripts Do

All scripts will:
1. ✅ Check if Python and Node.js are installed
2. ✅ Create virtual environment if it doesn't exist
3. ✅ Install frontend dependencies if missing
4. ✅ Start the Flask backend server
5. ✅ Start the React frontend server

## Server URLs

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

## Stopping the Servers

- **Linux/macOS script**: Press `Ctrl+C` in the terminal
- **Windows scripts**: Close the server windows or press `Ctrl+C` in the terminal
- **npm script**: Press `Ctrl+C` in the terminal

## Troubleshooting

### Python not found
- Make sure Python 3.7+ is installed and in your PATH
- On Windows, you may need to restart your terminal after installing Python

### Node.js not found
- Make sure Node.js is installed and in your PATH
- Verify with: `node --version` and `npm --version`

### Virtual environment issues
- Delete `server/venv` and let the script recreate it
- On Windows, you might need to run PowerShell as Administrator

### Port already in use
- Make sure ports 3000 and 5000 are not being used by other applications
- Change the ports in the `.env` files if needed

## Manual Start (Alternative)

If the scripts don't work, you can start servers manually:

**Backend:**
```bash
cd server
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

**Frontend (in a new terminal):**
```bash
cd client
npm start
```
