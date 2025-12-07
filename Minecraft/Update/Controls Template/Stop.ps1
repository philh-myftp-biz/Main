
$pyPID = Get-Content `
    -Path "$PSScriptRoot\.PID.txt" `
    -Raw

Stop-Process `
    -Id $pyPID `
    -Force