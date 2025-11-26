
param(
    [string] $Name
)
    
Stop-VM `
    -Name $Name `
    -TurnOff `
    > $null
