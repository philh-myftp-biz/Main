
# Iter through all processes
Get-Process | ForEach-Object -Process {

    # if the process name contains 'wintv'
    if ($_.ProcessName -like '*wintv*') {
      
        # Print the process to the console
        $_

        # Kill the process
        Stop-Process $_ -Force

    }

}
