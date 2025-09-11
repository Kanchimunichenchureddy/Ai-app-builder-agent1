@echo off
echo Starting AI App Builder Frontend...
echo ================================

REM Install dependencies if node_modules doesn't exist
if not exist node_modules (
    echo Installing frontend dependencies...
    npm install
)

REM Start the frontend server
echo Starting the frontend...
npm start

pause