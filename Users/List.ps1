
$Names = @()

Get-ADUser -Filter * -SearchBase "CN=Users, DC=philh, DC=local" `
    | Where-Object UserPrincipalName `
    | ForEach-Object -Process {
        $Names += @{
            FirstName = $_.GivenName
            LastName = $_.Surname
            Username = $_.SamAccountName.ToLower()
        }
    }

$Names `
    | ConvertTo-Json `
    | Write-Output