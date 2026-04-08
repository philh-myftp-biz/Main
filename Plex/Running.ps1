
$proc = Get-Process -Name 'Plex Media Server'

if ($null -eq $proc) {
    Write-Host 'false'
} else {
    Write-Host 'true'
}
