
param(
    [string] $Name
)

# Remove the VM from Hyper-V
Remove-VM `
    -Name $Name `
    -Force `
    > $null

# Delete Dir
Remove-Item `
    -Path "$HyperV\$Name" `
    -Recurse `
    -Force `
    > $null
    