
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
    -Path "E:\Virtual Machines\Hyper-V\$Name" `
    -Recurse `
    -Force `
    > $null
    