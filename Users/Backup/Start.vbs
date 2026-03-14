
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

' CD to the script directory
Shell.CurrentDirectory = "E:\Users\Backup\"

' Run the command
Shell.run "python __Start.py", 0, 0