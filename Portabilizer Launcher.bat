@echo off
chcp 65001 >nul
rem Запуск Portabilizer Launcher. Сначала пробует Portabilizer Launcher.exe. Если компьютер его блокирует
rem (например, "Access is denied" на учебных и рабочих компьютерах), открывает лаунчер через Python из исходников:
rem нужен Python с Tkinter и launcher.py рядом или в подпапке source. Версии и настройки остаются рядом с этим файлом.
if not exist "%~dp0Portabilizer Launcher.exe" goto py
start "" /wait "%~dp0Portabilizer Launcher.exe" %*
if not errorlevel 1 exit /b 0
echo.
echo Portabilizer Launcher.exe не запустился. Скорее всего, компьютер блокирует неподписанные exe-файлы.
:py
set "PZ_DIR="
for %%D in ("%~dp0" "%~dp0source\") do if not defined PZ_DIR if exist "%%~D\launcher.py" set "PZ_DIR=%%~D"
if not defined PZ_DIR goto nosrc
set "PORTABILIZER_LAUNCHER_HOME=%~dp0"
cd /d "%PZ_DIR%"
echo Запускаю лаунчер через Python...
where pythonw >nul 2>&1 && ( start "" pythonw "%PZ_DIR%\launcher.py" %* & exit /b 0 )
where pyw >nul 2>&1 && ( start "" pyw "%PZ_DIR%\launcher.py" %* & exit /b 0 )
where python >nul 2>&1 || goto nopy
python "%PZ_DIR%\launcher.py" %*
if errorlevel 1 pause
exit /b
:nopy
echo Python не найден в PATH.
pause
exit /b 1
:nosrc
echo Рядом нет исходников лаунчера (launcher.py), запустить через Python нельзя.
echo Скачайте папку с исходниками целиком (GitHub: Code - Download ZIP) или положите рядом папку source.
pause
exit /b 1
