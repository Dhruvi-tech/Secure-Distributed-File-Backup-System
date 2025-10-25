@echo off
echo 🚀 Starting SDFBS Cloud Architecture...
echo.

echo 📋 Checking Docker Desktop...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Desktop is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo 🔧 Building and starting distributed services...
docker-compose up -d --build

echo ⏳ Waiting for Cassandra cluster to initialize...
echo This may take 2-3 minutes for the first startup...
timeout /t 120 /nobreak

echo 🔍 Checking service health...
docker-compose ps

echo.
echo ✅ SDFBS Cloud Architecture is running!
echo.
echo 📊 Service URLs:
echo   - Load Balancer: http://localhost:8080
echo   - Node 1: http://localhost:8001
echo   - Node 2: http://localhost:8002  
echo   - Node 3: http://localhost:8003
echo   - Cassandra: localhost:9042
echo.
echo 🧪 Test endpoints:
echo   - Health: curl http://localhost:8080/health
echo   - Files: curl http://localhost:8080/files
echo   - Nodes: curl http://localhost:8080/nodes
echo.
echo Press any key to view logs...
pause

echo 📜 Viewing service logs...
docker-compose logs --tail=50

pause