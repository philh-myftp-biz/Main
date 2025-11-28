
# Iter through all processes
Get-Process | ForEach-Object -Process {

    # if the process is 'firefox' or 'python'
    if (@('firefox', 'python') -contains $_.ProcessName) {
      
        # Print the process to the console
        $_

        # Kill the process
        Stop-Process $_ -Force

    }

}