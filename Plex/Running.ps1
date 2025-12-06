
$process = (Get-Process | Where-Object ProcessName -eq 'Plex Media Server')

# If process exists
if ($process) {
    Write-Host 'true'
} else {
    Write-Host 'false'
}