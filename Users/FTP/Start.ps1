
Enable-NetFirewallRule -DisplayGroup "FTP Server"

Start-IISSite -Name 'FTP Server'
