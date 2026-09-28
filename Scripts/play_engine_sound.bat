@echo off
rem =========================================================================
rem Script: play_engine_sound.bat
rem Plays synthesized multi-gear engine acceleration audio asynchronously
rem =========================================================================
powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -Command "$p = New-Object Media.SoundPlayer '%~dp0..\Audio\engine_accel_gearchange.wav'; $p.Play()"
