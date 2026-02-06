@echo off
echo Setting up Indian Weather Transit Pipeline...

set TASK_NAME=IndianWeatherTransitPipeline
set SCRIPT_PATH=%~dp0schedule_india_pipeline.bat

schtasks /create /tn "%TASK_NAME%" /tr "%SCRIPT_PATH%" /sc daily /st 06:30 /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS! Indian pipeline scheduled to run daily at 6:30 AM
    echo.
    echo Manage:
    echo - View: schtasks /query /tn %TASK_NAME%
    echo - Run now: schtasks /run /tn %TASK_NAME%
    echo - Delete: schtasks /delete /tn %TASK_NAME% /f
) else (
    echo ERROR: Run as Administrator
)
pause
