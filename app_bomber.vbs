Dim objShell, i
Set objShell = WScript.CreateObject("WScript.Shell")

For i = 1 to 20 ' Opens Notepad 20 times. Change the number as you like.
    objShell.Run "notepad.exe"
    WScript.Sleep 1 ' Wait a tenth of a second before opening the next one
Next
