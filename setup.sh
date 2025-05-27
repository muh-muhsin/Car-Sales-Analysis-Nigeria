#!/bin/bash

# Cars360 Development Setup Script
echo "🚀 Setting up Cars360 Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

# Check if PostgreSQL is available
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL is not installed. You'll need to install it or use a cloud database."
fi

print_status "Setting up backend..."

# Backend setup
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f ".env" ]; then
    print_status "Creating backend environment file..."
    cp .env.example .env
    print_warning "Please update the .env file with your configuration"
fi

# Create uploads directory
mkdir -p uploads

print_success "Backend setup completed!"

# Frontend setup
cd ../frontend

print_status "Setting up frontend..."

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install

# Copy environment file
if [ ! -f ".env.local" ]; then
    print_status "Creating frontend environment file..."
    cp .env.example .env.local
    print_warning "Please update the .env.local file with your configuration"
fi

print_success "Frontend setup completed!"

cd ..

print_success "🎉 Cars360 setup completed!"
echo ""
print_status "Next steps:"
echo "1. Update backend/.env with your database and service configurations"
echo "2. Update frontend/.env.local with your API and blockchain configurations"
echo "3. Set up PostgreSQL database"
echo "4. Deploy smart contracts to testnet"
echo "5. Start the development servers:"
echo ""
echo "   Backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "   Frontend: cd frontend && npm run dev"
echo ""
print_status "For detailed instructions, see the README.md file"
