
param(
    [string] $Name
)

Start-VM `
    -Name $Name `
    > $null