@echo off
:: This batch file starts the FastAPI web server for the converter.

:: Change the current directory to the script's directory.
cd /d "%~dp0"

echo Starting FastAPI server...
echo Access the application at http://127.0.0.1:28888

:: Launch the Uvicorn server.
:: --reload will automatically restart the server when code changes.
uvicorn web_server:app --reload --port 28888
