
$processes = Get-Content -Path "$PSScriptRoot\__pycache__\PID.json" -Raw | ConvertFrom-Json | ForEach-Object {
    
    try {
        Get-Process -Id $_ -ErrorAction SilentlyContinue
    } catch {
        Write-Host 'false'
        exit
    }

}

if ($processes.Length -gt 0) {
    Write-Host 'true'
} else {
    Write-Host 'false'
}