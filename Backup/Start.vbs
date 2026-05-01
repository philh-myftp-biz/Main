
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = "E:\"

' Run the command
Shell.run "python -m Backup", 0, 0