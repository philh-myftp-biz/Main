
# Iter through all processes
Get-Process | ForEach-Object -Process {

    # if the process name starts with 'plex'
    if ($_.ProcessName -like 'plex*') {
      
        # Print the process to the console
        $_

        # Kill the process
        Stop-Process $_ -Force

    }

}
