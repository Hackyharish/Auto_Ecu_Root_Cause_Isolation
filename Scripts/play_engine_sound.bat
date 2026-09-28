@echo off
rem =========================================================================
rem Script: play_engine_sound.bat
rem Plays synchronized engine acceleration audio asynchronously
rem Supports --sync (pedal-synchronized) and --play (fixed loop)
rem =========================================================================
set MODE=--sync
if not "%~1"=="" set MODE=%~1

where pythonw >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start "" pythonw "%~dp0engine_sound_realtime.py" %MODE%
    exit /b 0
)

where pyw >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start "" pyw "%~dp0engine_sound_realtime.py" %MODE%
    exit /b 0
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start /min python "%~dp0engine_sound_realtime.py" %MODE%
    exit /b 0
)

powershell.exe -NoProfile -Command "$p = (Resolve-Path '%~dp0..\Audio\engine_gear1.wav').Path; [System.Media.SoundPlayer]::new($p).PlaySync()"
