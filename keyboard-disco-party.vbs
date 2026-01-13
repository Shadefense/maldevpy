set wcsh = WScript.CreateObject("WScript.Shell")
Do
    wcsh.SendKeys "{CAPSLOCK}"
    wcsh.SendKeys "{NUMLOCK}"
    wcsh.SendKeys "{SCROLLLOCK}"
    WScript.Sleep 50
Loop
