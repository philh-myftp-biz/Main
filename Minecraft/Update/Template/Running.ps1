
$pyPID = Get-Content `
    -Path "$PSScriptRoot\__PID__.txt" `
    -Raw

$process = Get-Process `
    -Id $pyPID `
    -ErrorAction SilentlyContinue

if ($process) {
    Write-Host 'true'
} else {
    Write-Host 'false'
}