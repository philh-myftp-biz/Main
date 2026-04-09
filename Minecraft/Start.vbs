
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

Shell.CurrentDirectory = "E:\"

Dim CMD, arg

CMD = "python -m Minecraft._Start.py "

' Build the arguments string
For Each arg In WScript.Arguments
    
    CMD = CMD & " " & Chr(34) & arg & Chr(34)

Next

' Run the command
Shell.run CMD, 0, 0