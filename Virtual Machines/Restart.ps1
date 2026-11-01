
param(
    [string] $Name
)
    
Restart-VM `
    -Name $Name `
    -Confirm:$false `
    -Force `
    > $null
