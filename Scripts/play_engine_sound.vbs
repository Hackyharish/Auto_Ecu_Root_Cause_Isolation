' =========================================================================
' Script: play_engine_sound.vbs
' Plays synthesized engine acceleration audio completely silently in background
' Zero console window popups, no terminal flashing
' =========================================================================
Dim fso, scriptDir, audioPath, shell, psCmd
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
audioPath = fso.BuildPath(scriptDir, "..\Audio\engine_accel_gearchange.wav")

If fso.FileExists(audioPath) Then
    Set shell = CreateObject("WScript.Shell")
    ' 0 = vbHide (completely hidden, zero terminal popup), False = return immediately
    psCmd = "powershell.exe -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -Command ""$p = New-Object System.Media.SoundPlayer '" & audioPath & "'; $p.PlaySync()"""
    shell.Run psCmd, 0, False
End If
