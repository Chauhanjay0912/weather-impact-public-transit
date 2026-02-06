@echo off
echo Starting Airflow with Docker...
echo.

cd /d "%~dp0"

echo Step 1: Creating directories...
if not exist "logs" mkdir logs
if not exist "plugins" mkdir plugins

echo Step 2: Initializing Airflow database...
docker-compose up airflow-init

echo.
echo Step 3: Starting Airflow services...
docker-compose up -d

echo.
echo ============================================================
echo Airflow is starting!
echo.
echo Wait 2-3 minutes, then open:
echo http://localhost:8080
echo.
echo Login: airflow / airflow
echo ============================================================
echo.
echo Commands:
echo - Stop: docker-compose down
echo - Logs: docker-compose logs -f
echo - Status: docker-compose ps
echo.
pause
