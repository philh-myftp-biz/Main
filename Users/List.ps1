
$Names = @()

$Users = Get-ADUser -Filter * -SearchBase "CN=Users, DC=philh, DC=local"

$Users | ForEach-Object -Process {

    $Name = @{
        FirstName = $_.GivenName
        LastName = $_.Surname
        Username = $_.SamAccountName.ToLower()
    }

    if (@('krbtgt', 'guest', 'administrator') -notcontains $Name['Username']) {
        $Names += $Name
    }
}

$Names `
    | ConvertTo-Json `
    | Write-Output