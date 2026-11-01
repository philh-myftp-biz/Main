
param(
    [string] $Name
)

Import-Module 'E:/Virtual Machines/mod.psm1' -Function Repair-VirtualMachine
#=====================================================================================================

New-Item `
    -Path "$HyperV\$Name" `
    -ItemType Directory `
    -ErrorAction SilentlyContinue `
    -Verbose

New-VHD `
    -Path "$HyperV\$Name\Hard Drive.vhdx" `
    -SizeBytes 150GB `
    -Dynamic

Repair-VirtualMachine -Name $Name

#=====================================================================================================