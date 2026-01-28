
Get-Content -Path "$PSScriptRoot\__pycache__\PID.json" -Raw | ConvertFrom-Json | ForEach-Object {
    
    Stop-Process `
        -Id $_.Split('-')[1] `
        -Force
}