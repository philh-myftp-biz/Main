
$processes = Get-Content -Path "$PSScriptRoot\__pycache__\PID.json" -Raw | ConvertFrom-Json | ForEach-Object {
    
    if (!$_.Contains('firefox-')) {

        try {
            Get-Process `
                -Id $_.Split('-')[1] `
                -ErrorAction SilentlyContinue
        } catch {
            Write-Host 'false'
            exit
        }

    }

}

if ($processes.Length -gt 0) {
    Write-Host 'true'
} else {
    Write-Host 'false'
}