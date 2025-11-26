
param(
    [string] $Name
)

try {

    $NetAdapter = (Get-VM `
        -VMName $Name `
        | Select-Object -ExpandProperty NetworkAdapters `
    )

    $IP = $NetAdapter.IPAddresses `
        | Where-Object {$_ -notlike '*::*'} `
        | Select-Object -First 1

    $IP | ConvertTo-Json | Write-Output

} catch {

    $null | ConvertTo-Json | Write-Output

}
