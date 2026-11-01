
param(
    [string] $Name
)

$NetAdapter = (Get-VM `
    -VMName $Name `
    | Select-Object -ExpandProperty NetworkAdapters `
)

$IP = $NetAdapter.IPAddresses `
    | Where-Object {$_ -notlike '*::*'} `
    | Select-Object -First 1

if ($IP) {
    $IP | ConvertTo-Json | Write-Output
} else {
    Write-Output 'null'
}
