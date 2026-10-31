@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title Сборка Portabilizer Launcher
echo === Сборка Portabilizer Launcher.exe ===
python --version >nul 2>&1
if errorlevel 1 (
  echo Python не найден. Установите Python 3.9 или новее с python.org, отметив Add Python to PATH.
  pause
  exit /b 1
)
echo [1/2] Ставлю pyinstaller...
python -m pip install --upgrade pyinstaller
if errorlevel 1 goto fail
echo [2/2] Собираю exe...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "Portabilizer Launcher" --icon launcher.ico launcher.py
if errorlevel 1 goto fail
echo.
echo Готово: dist\Portabilizer Launcher.exe
pause
exit /b 0
:fail
echo Сборка не удалась.
pause
exit /b 1
