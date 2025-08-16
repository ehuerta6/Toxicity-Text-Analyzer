#!/bin/bash

# ToxiGuard Project Startup Script
# This script sets up and starts the entire project

echo "🚀 ToxiGuard - Advanced Toxicity Detection System"
echo "=================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend
npm install
cd ..

# Setup backend
echo "🐍 Setting up backend..."
cd backend
pip3 install -r requirements.txt
cd ..

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 Starting ToxiGuard..."
echo "   Frontend will be available at: http://localhost:5173"
echo "   Backend API will be available at: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Start both services
npm run dev
