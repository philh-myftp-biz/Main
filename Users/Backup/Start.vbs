
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = "E:\Users\"

' Run the command
Shell.run "python -m Backup.__Start", 0, 0