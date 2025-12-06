
' Create a new Shell Object
Set Shell = WScript.CreateObject("WScript.Shell")

Shell.CurrentDirectory = "C:/Program Files/Plex/Plex Media Server/"

Shell.run """Plex Media Server.exe""", 0, 1