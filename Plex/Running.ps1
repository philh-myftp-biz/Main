
# Store the current progress preference
$OriginalProgressPreference = $ProgressPreference 

# Set the progress preference to 'SilentlyContinue' to hide progress
$ProgressPreference = 'SilentlyContinue'

# Test the port
Test-NetConnection `
    -ComputerName localhost `
    -Port 32400 `
    -InformationLevel Quiet `
    | ConvertTo-Json | Write-Host

# Restore the original progress preference setting
$ProgressPreference = $OriginalProgressPreference 