@echo off
echo 🚀 Starting SDFBS Phase 1 - Standalone Mode
echo.

echo 📦 Installing requirements...
pip install flask flask-cors

echo.
echo 🔧 Starting API Server (Port 8080)...
start "SDFBS API" python standalone_server.py

echo ⏳ Waiting for API to start...
timeout /t 3 /nobreak

echo 🌐 Starting Web Interface (Port 3001)...
start "SDFBS Web" python web_server.py

echo.
echo ✅ SDFBS Phase 1 is running!
echo 📊 API: http://localhost:8080
echo 🌐 Web Interface: http://localhost:3001
echo.
echo Press any key to stop servers...
pause

echo 🛑 Stopping servers...
taskkill /f /im python.exe /fi "WINDOWTITLE eq SDFBS*" 2>nul