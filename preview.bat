@echo off
echo 🚀 Starting Cars360 Preview...

REM Check if setup has been run
if not exist "backend\venv" (
    echo ❌ Backend not set up. Please run setup.bat first.
    pause
    exit /b 1
)

if not exist "frontend\node_modules" (
    echo ❌ Frontend not set up. Please run setup.bat first.
    pause
    exit /b 1
)

echo 🌐 Starting frontend server...
cd frontend
start "Cars360 Frontend" cmd /k "npm run dev"

echo ⚡ Frontend starting at http://localhost:3000
echo.
echo 📝 Note: Backend API endpoints will return mock data for preview
echo 🔗 Open http://localhost:3000 in your browser
echo.
echo Press any key to stop the preview...
pause >nul

REM Kill the frontend process
taskkill /f /im node.exe >nul 2>&1

echo 👋 Preview stopped!
pause
