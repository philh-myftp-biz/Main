param(
    [string] $Name
)

Stop-VM `
    -Name $Name `
    -Save `
    > $null