Import-Module WebAdministration

$Website = Get-Website -Name 'FTP Server'

($Website.State -eq 'Started') | ConvertTo-JSON
