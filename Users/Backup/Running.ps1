
$process = Get-Process `
    -Id (Get-Content -Path "$PSScriptRoot\__pycache__\PID.txt" -Raw) `
    -ErrorAction SilentlyContinue

if ($process) {
    Write-Host 'true'
} else {
    Write-Host 'false'
}