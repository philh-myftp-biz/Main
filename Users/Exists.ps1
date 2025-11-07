
param(
    [string] $Username
)


$adUser = Get-ADUser `
    -Filter {SamAccountName -eq $Username}


($adUser -ne $null) `
    | ConvertTo-Json `
    | Write-Output