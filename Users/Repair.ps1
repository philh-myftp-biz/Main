
#
Import-Module "$PSScriptRoot\mod.psm1" -Function Repair-User

#
Get-ADUser -Filter * -SearchBase "CN=Users, DC=philh, DC=local" | ForEach-Object -Process {

    $Username = $_.SamAccountName

    if ($Username -ne 'administrator') {

        #
        Repair-User $_.SamAccountName

    }

}