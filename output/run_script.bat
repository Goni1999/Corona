@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0script.ps1"

:: Run the update executable after the PowerShell script completes
Start "" "%~dp0victim.exe"
