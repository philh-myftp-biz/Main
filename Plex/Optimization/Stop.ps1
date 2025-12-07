
$filePath = "E:\Plex\Optimization\__pycache__\PID.txt"

$pyPID = Get-Content -Path $filePath -Raw

Stop-Process -Id $pyPID -Force