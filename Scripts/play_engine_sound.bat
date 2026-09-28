@echo off
rem =========================================================================
rem Script: play_engine_sound.bat
rem Plays synthesized multi-gear engine acceleration audio asynchronously
rem =========================================================================
where pythonw >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start "" pythonw "%~dp0engine_sound_realtime.py" --play
    exit /b 0
)

where pyw >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start "" pyw "%~dp0engine_sound_realtime.py" --play
    exit /b 0
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    start /min python "%~dp0engine_sound_realtime.py" --play
    exit /b 0
)

powershell.exe -NoProfile -Command "$p = (Resolve-Path '%~dp0..\Audio\engine_accel_gearchange.wav').Path; [System.Media.SoundPlayer]::new($p).PlaySync()"
