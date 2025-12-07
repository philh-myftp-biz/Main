
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

'
Shell.CurrentDirectory = UCase(Left(Wscript.ScriptFullName, Len(Wscript.ScriptFullName) - Len(Wscript.ScriptName) - 1))

'
Shell.run "python __Start.py", 0, 1