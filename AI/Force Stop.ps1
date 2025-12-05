
# Iter through all processes
Get-Process | ForEach-Object -Process {

    # if the process is 'ollama' or 'python'
    if (@('ollama', 'python') -contains $_.ProcessName) {
      
        # Print the process to the console
        $_

        # Kill the process
        Stop-Process $_ -Force

    }

}
