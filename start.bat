@echo off
REM ToxiGuard Project Startup Script for Windows
REM This script sets up and starts the entire project

echo 🚀 ToxiGuard - Advanced Toxicity Detection System
echo ==================================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Install root dependencies
echo 📦 Installing root dependencies...
call npm install

REM Setup frontend
echo 🎨 Setting up frontend...
cd frontend
call npm install
cd ..

REM Setup backend
echo 🐍 Setting up backend...
cd backend
call pip install -r requirements.txt
cd ..

echo ✅ Setup completed successfully!
echo.
echo 🚀 Starting ToxiGuard...
echo    Frontend will be available at: http://localhost:5173
echo    Backend API will be available at: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop all services
echo.

REM Start both services
call npm run dev

pause
