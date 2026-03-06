
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = UCase(Left(Wscript.ScriptFullName, Len(Wscript.ScriptFullName) - Len(Wscript.ScriptName) - 1))

' Run (and wait for) CreateLink.ps1
Shell.run "Powershell -File CreateLink.ps1", 0, 1

' Start Ollama Service
Shell.run "ollama serve", 0, 0
