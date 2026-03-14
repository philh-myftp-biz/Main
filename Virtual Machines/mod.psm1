
function Repair-VirtualMachine {

    param(
        [string] $Name
    )

    $Dir = "E:/Virtual Machines/Hyper-V/$Name"

    # Get the username from the vm name
    if ($Name.StartsWith('User-')) {
        $Username = $Name.Split('User-')[1]
    } else {
        $Username = $null
    }

    Write-Host "Repairing: " -NoNewline
    Write-Host $Name -ForegroundColor Cyan

    #=====================================================================================================
    
    # Remove Filesystem compression for VM directory
    Invoke-WmiMethod `
        -Path "Win32_Directory.Name='$Dir'" `
        -Name uncompress

    #=====================================================================================================

    $VM = Get-VM `
        -Name $Name `
        -ErrorAction SilentlyContinue

    # If the vm does not exist
    if ($null -eq $VM) {

        # Create the VM in Hyper-V
        New-VM `
            -Name $Name `
            -MemoryStartupBytes 4GB `
            -Path "E:\Virtual Machines\Hyper-V\" `
            -Generation 1 `
            -SwitchName "Main Switch"

        # Attach Virtual Hard Drive
        Add-VMHardDiskDrive `
            -VMName $Name `
            -Path "$Dir\Hard Drive.vhdx" `
            -Verbose

    }

    # If a username was found
    if ($Username) {

        # Grant Remote Desktop access to the user
        Grant-VMConnectAccess `
            -VMName $Name `
            -UserName $Username `
            -ErrorAction SilentlyContinue `
            | Out-Null

    }

    # Set the # of Virtual Processors
    Set-VMProcessor `
        -VMName $Name `
        -Count 2

    # Enable Dynamic Memory
    Set-VMMemory `
        -VMName $Name `
        -DynamicMemoryEnabled $True `
        -MinimumBytes 512MB `
        -MaximumBytes 8GB `
        -Buffer 20

    # Set Paths for Snapshots and PageFiles
    Set-VM `
        -VMName $Name `
        -SnapshotFileLocation $Dir `
        -SmartPagingFilePath $Dir

    # Enable Guest Services
    Enable-VMIntegrationService `
        -VMName $Name `
        -Name "Guest Service Interface"

}

Export-ModuleMember -Function Repair-VirtualMachine