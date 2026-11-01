
param(
    [string] $Name
)

$VM = Get-VM -Name $Name

if ($VM.State -eq 'Running') {
    Write-Host 'true'
} else {
    Write-Host 'false'
}