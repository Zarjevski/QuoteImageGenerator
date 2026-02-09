#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Change to project root (one level up from scripts folder)
cd "$SCRIPT_DIR/.."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Quote Image Generator Development Environment${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed. Please install Python 3.7+${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js${NC}"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed. Please install npm${NC}"
    exit 1
fi

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "server/venv" ]; then
        echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
        cd server
        python3 -m venv venv || python -m venv venv
        echo -e "${GREEN}✅ Virtual environment created${NC}"
        cd ..
    fi
}

# Function to check if node_modules exists
check_node_modules() {
    if [ ! -d "client/node_modules" ]; then
        echo -e "${YELLOW}⚠️  Frontend dependencies not found. Installing...${NC}"
        cd client
        npm install
        echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
        cd ..
    fi
}

# Check and setup backend
echo -e "${BLUE}📦 Checking backend setup...${NC}"
check_venv

# Check and setup frontend
echo -e "${BLUE}📦 Checking frontend setup...${NC}"
check_node_modules

# Activate virtual environment and start backend
start_backend() {
    cd server
    source venv/bin/activate
    
    # Load environment variables if .env exists
    if [ -f .env ]; then
        echo -e "${GREEN}🌱 Loading environment variables from .env${NC}"
        export $(grep -v '^#' .env | xargs)
    fi
    
    echo -e "${GREEN}🔧 Starting Flask backend server...${NC}"
    python app.py &
    BACKEND_PID=$!
    cd ..
    echo $BACKEND_PID > .backend.pid
}

# Start frontend
start_frontend() {
    cd client
    echo -e "${GREEN}⚛️  Starting React frontend server...${NC}"
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo $FRONTEND_PID > .frontend.pid
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    if [ -f .backend.pid ]; then
        kill $(cat .backend.pid) 2>/dev/null
        rm .backend.pid
    fi
    if [ -f .frontend.pid ]; then
        kill $(cat .frontend.pid) 2>/dev/null
        rm .frontend.pid
    fi
    echo -e "${GREEN}✅ Servers stopped${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

# Start both servers
start_backend
sleep 2
start_frontend

echo -e "\n${GREEN}✅ Both servers are starting!${NC}"
echo -e "${BLUE}📱 Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}🔧 Backend:  http://localhost:5000${NC}"
echo -e "\n${YELLOW}Press Ctrl+C to stop both servers${NC}\n"

# Wait for both processes
wait
