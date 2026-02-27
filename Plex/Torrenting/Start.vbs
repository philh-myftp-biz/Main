
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = UCase(Left(Wscript.ScriptFullName, Len(Wscript.ScriptFullName) - Len(Wscript.ScriptName) - 1))

CMD = "python __Start.py"

' Append all arguments to the command string
For i = 0 To WScript.Arguments.Count - 1
    
    CMD = CMD & " """ & WScript.Arguments.Item(i) & """"

Next

' Run the command
Shell.run CMD, 0, 0