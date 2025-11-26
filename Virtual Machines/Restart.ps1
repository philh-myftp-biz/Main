
param(
    [string] $Name
)
    
Restart-VM `
    -Name $Name `
    -Confirm `
    > $null
