
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = UCase(Left(Wscript.ScriptFullName, Len(Wscript.ScriptFullName) - Len(Wscript.ScriptName) - 1))

' Run the command
Shell.run "python __Start.py", 0, 0