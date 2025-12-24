
Test-NetConnection `
    -ComputerName localhost `
    -Port 32400 `
    -InformationLevel Quiet `
    | ConvertTo-Json | Write-Host
