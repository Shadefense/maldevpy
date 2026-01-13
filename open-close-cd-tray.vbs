Set wmp = CreateObject("WMPlayer.OCX.7")
Set cd = wmp.CDRomCollection
Do
    For i = 0 To cd.Count - 1
        cd.Item(i).Eject
    Next
    For i = 0 To cd.Count - 1
        cd.Item(i).Eject
    Next
Loop
