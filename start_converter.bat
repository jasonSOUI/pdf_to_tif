@echo off
:: This batch file starts the PDF to TIF Converter application.

:: Change the current directory to the script's directory to ensure relative paths work.
cd /d "%~dp0"

:: Launch the Python GUI application using pyw.exe to avoid a background console window.
start "PDF to TIF Converter" pyw.exe main.py
