
#
Get-VM | ForEach-Object -Process {

    #
    Start-VM -VM $_

}

#
$Credentials = (Get-Credential)

Get-VM | ForEach-Object -Process {

    #
    while(-not $_.ExtensionData.Guest.guestOperationsReady) {
        
        Start-Sleep 5
        $_.ExtensionData.UpdateViewData('Guest')
    
    }

    Invoke-Command `
        -VMName $_.Name `
        -Credential $Credentials `
        -ScriptBlock { #

            #
            Rename-Computer -NewName "VM-$($_.Name)";
            
            #
            Set-DnsClientServerAddress `
                -ServerAddresses ('192.168.1.2', '8.8.8.8') `
                -InterfaceIndex (Get-NetIpConfiguration | Select-Object -First 1).InterfaceIndex
        
        }

}