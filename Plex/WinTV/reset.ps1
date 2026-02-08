
# Iter through all WinTV devices
Get-PnpDevice | Where-Object FriendlyName -like '*wintv*' | ForEach-Object -Process {

    # Uninstall the device
    pnputil.exe /remove-device $_.InstanceId /force
        
}

# Rescan Devices
pnputil.exe /scan-devices