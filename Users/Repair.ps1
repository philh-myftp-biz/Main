
param(
    [String]$User = $null
)

#
Import-Module "$PSScriptRoot\mod.psm1" -Function Repair-User

if ($User) {

    Repair-User $User
    
} else {

    #
    Get-ADUser -Filter * -SearchBase "CN=Users, DC=philh, DC=local" | ForEach-Object -Process {

        if ($_.SamAccountName -ne 'administrator') {

            #
            Repair-User $_.SamAccountName

        }

    }

}