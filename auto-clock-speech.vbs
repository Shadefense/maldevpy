Option Explicit
Dim Speak, CurrentTime, WshShell

' Create the SAPI (Speech API) object
Set Speak = CreateObject("Sapi.spvoice")

' Loop indefinitely
Do While True
    ' Get the current system time
    CurrentTime = Time
    
    ' Construct the message to speak
    Dim Message
    Message = "The current time is " & CurrentTime
    
    ' Speak the time
    Speak.Speak Message
    
    ' Wait for 60 seconds (60000 milliseconds) before looping again
    Wscript.Sleep(60000)
Loop

' Clean up objects (Note: this part is technically unreachable due to the Do While True loop, 
' but good practice if the loop had an exit condition)
Set Speak = Nothing
