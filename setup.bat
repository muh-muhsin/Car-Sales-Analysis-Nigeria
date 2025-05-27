@echo off
echo 🚀 Setting up Cars360 Development Environment...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

echo 📦 Setting up backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Copy environment file
if not exist ".env" (
    echo Creating backend environment file...
    copy .env.example .env
    echo ⚠️  Please update the .env file with your configuration
)

REM Create uploads directory
if not exist "uploads" mkdir uploads

echo ✅ Backend setup completed!

REM Frontend setup
cd ..\frontend

echo 📦 Setting up frontend...

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

REM Copy environment file
if not exist ".env.local" (
    echo Creating frontend environment file...
    copy .env.example .env.local
    echo ⚠️  Please update the .env.local file with your configuration
)

echo ✅ Frontend setup completed!

cd ..

echo 🎉 Cars360 setup completed!
echo.
echo Next steps:
echo 1. Update backend\.env with your database and service configurations
echo 2. Update frontend\.env.local with your API and blockchain configurations
echo 3. Run the preview with: npm run preview
echo.
echo For development servers:
echo   Backend:  cd backend ^&^& venv\Scripts\activate ^&^& uvicorn main:app --reload
echo   Frontend: cd frontend ^&^& npm run dev
echo.
pause
