
param(
    [string] $Name
)

Import-Module 'E:/Virtual Machines/mod.psm1' -Function Repair-VirtualMachine
#=====================================================================================================

$Dir = "E:\Virtual Machines\Hyper-V\$Name"

New-Item `
    -Path $Dir `
    -ItemType Directory `
    -ErrorAction SilentlyContinue `
    -Verbose

New-VHD `
    -Path "$Dir\Hard Drive.vhdx" `
    -SizeBytes 150GB `
    -Dynamic

Repair-VirtualMachine -Name $Name

#=====================================================================================================