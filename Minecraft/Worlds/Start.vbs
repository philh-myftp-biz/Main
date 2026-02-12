
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = UCase(Left(Wscript.ScriptFullName, Len(Wscript.ScriptFullName) - Len(Wscript.ScriptName) - 1))

Dim CMD, arg, quotedArg

CMD = "python __Start.py "

' Build the arguments string
For Each arg In WScript.Arguments
    
    CMD = CMD & " " & Chr(34) & arg & Chr(34)

Next

' Run the command
Shell.run CMD, 0, 0