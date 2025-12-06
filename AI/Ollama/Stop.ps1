
# Iter through all processes
Get-Process | ForEach-Object -Process {

    # if the process is 'ollama'
    if ($_.ProcessName -eq 'ollama') {
      
        # Print the process to the console
        $_

        # Kill the process
        Stop-Process $_ -Force

    }

}
