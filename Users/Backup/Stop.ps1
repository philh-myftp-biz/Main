
Stop-Process `
    -Id (Get-Content -Path "$PSScriptRoot\__pycache__\PID.txt" -Raw) `
    -Force
