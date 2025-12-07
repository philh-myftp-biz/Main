
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

Shell.CurrentDirectory = "E:\Plex\Torrenting\"

Shell.run "python __Start.py", 0, 1