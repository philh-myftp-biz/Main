
$filePath = "E:\Plex\Optimization\__pycache__\PID.txt"

$pyPID = Get-Content -Path $filePath -Raw

$process = Get-Process `
    -Id $pyPID `
    -ErrorAction SilentlyContinue

if ($process) {
    Write-Host 'true'
} else {
    Write-Host 'false'
}