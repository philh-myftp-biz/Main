
param(
    [string]$Name = $null
)

Import-Module 'E:/Virtual Machines/mod.psm1' -Function Repair-VirtualMachine

# If a name was passed
if ($Name) {

    Repair-VirtualMachine -Name $Name

} else {

    Get-ChildItem -Path 'E:/Virtual Machines/Hyper-V' -Directory | ForEach-Object {
        
        Repair-VirtualMachine -Name $_.Name

    }

}
