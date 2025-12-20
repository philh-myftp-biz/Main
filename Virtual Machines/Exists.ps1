
param(
    [string] $Name
)

try {
    Get-VM -Name $Name
    Write-Host 'true'
} catch {
    Write-Host 'false'
}
