
param(
    [string] $Name
)

$VM = (
    Get-VM `
    -VMName $Name `
    -ErrorAction SilentlyContinue
)

if ($VM) {
    $VM.Id.ToString() | ConvertTo-Json | Write-Output
} else {
    Write-Output 'null'
}
