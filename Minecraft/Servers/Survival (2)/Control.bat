@echo off
cd /d "%~dp0"

if "%1"=="0" (
    taskkill /F /IM java.exe
)

if "%1"=="1" (
    cd Server
    start /B java -Xmx2G -jar fabric-server-launch.jar nogui
)