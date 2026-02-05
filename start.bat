@echo off
echo ========================================
echo GDP Growth Prediction System
echo ========================================
echo.
echo Starting Backend Server (Flask)...
start cmd /k "python app.py"
timeout /t 3 /nobreak >nul
echo.
echo Starting Frontend Server (React)...
start cmd /k "cd fronend && npm start"
echo.
echo ========================================
echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul
