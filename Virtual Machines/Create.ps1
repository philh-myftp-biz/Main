
param(
    [string] $Name,
    [bool] $UseTemplate = $true
)

# Declare VM dir
$Root = "E:\Virtual Machines"

#=====================================================================================================

# Create Dir
New-Item `
    -Path "$Root\Hyper-V\$Name" `
    -ItemType Directory `
    -Verbose

#=====================================================================================================

if ($UseTemplate) {

    # Create the VM in Hyper-V
    New-VM `
        -Name $Name `
        -MemoryStartupBytes 4GB `
        -Path "$Root\Hyper-V\" `
        -Generation 1 `
        -SwitchName "Main Switch" `
        -Verbose

    #
    Copy-Item `
        -Path "$Root\Hyper-V\Template.vhdx" `
        -Destination "$Root\Hyper-V\$Name\Hard Drive.vhdx" `
        -Verbose

    # Attach 'Installer.iso'
    Add-VMHardDiskDrive `
        -VMName $Name `
        -Path "$Root\Hyper-V\$Name\Hard Drive.vhdx" `
        -Verbose

} else {

    # Create the VM in Hyper-V
    New-VM `
        -Name $Name `
        -MemoryStartupBytes 4GB `
        -Path "$Root\Hyper-V\" `
        -NewVHDPath "$Root\Hyper-V\$Name\Hard Drive.vhdx" `
        -NewVHDSizeBytes 150GB `
        -Generation 1 `
        -SwitchName "Main Switch" `
        -Verbose

    # Attach 'Installer.iso'
    Add-VMDvdDrive `
        -VMName $Name `
        -Path "$Root\Hyper-V\Installer.iso" `
        -Verbose

}

#=====================================================================================================

# Set the # of Virtual Processors
Set-VMProcessor `
    -VMName $Name `
    -Count 2 `
    -Verbose

# Enable Dynamic Memory
Set-VMMemory `
    -VMName $Name `
    -DynamicMemoryEnabled $True `
    -MinimumBytes 512MB `
    -MaximumBytes 8GB `
    -Buffer 20 `
    -Verbose

# Set Paths for Snapshots and PageFiles
Set-VM `
    -VMName $Name `
    -SnapshotFileLocation "$Root\Hyper-V\$Name" `
    -SmartPagingFilePath "$Root\Hyper-V\$Name" `
    -Verbose

# Enable Guest Services
Enable-VMIntegrationService `
    -VMName $Name `
    -Name "Guest Service Interface" `
    -Verbose

#=====================================================================================================