
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
    -ErrorAction SilentlyContinue `
    -Verbose

New-VHD `
    -Path "$Root\Hyper-V\$Name\Hard Drive.vhdx"
    -ParentPath "$Root\Template\Tiny11\Hard Drive.vhdx" `
    -Differencing

Repair-VirtualMachine -Name $Name

#=====================================================================================================