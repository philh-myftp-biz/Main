Import-Module WebAdministration

Set-ItemProperty "IIS:\Sites\FTP Server" serverAutoStart False

Stop-IISSite -Name 'FTP Server' -Confirm:$false
