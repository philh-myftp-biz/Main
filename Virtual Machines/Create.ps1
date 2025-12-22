
param(
    [string] $Name
)

Import-Module 'E:/Virtual Machines/mod.psm1' -Function Repair-VirtualMachine

# Declare VM dir
$Root = "E:\Virtual Machines"

#=====================================================================================================

# Create Dir
New-Item `
    -Path "$Root\Hyper-V\$Name" `
    -ItemType Directory `
    -Verbose

#
Copy-Item `
    -Path "$Root\Hyper-V\Template.vhdx" `
    -Destination "$Root\Hyper-V\$Name\Hard Drive.vhdx" `
    -Verbose

#
Repair-VirtualMachine -Name $Name

#=====================================================================================================