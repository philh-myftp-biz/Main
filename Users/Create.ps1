
param (
    [string] $Username,
    [string] $FirstName,
    [string] $LastName,
    [securestring] $Password
)

Import-Module "$PSScriptRoot\mod.psm1" -Function Repair-User

#=====================================================================================================

# Create new Active Directory User
New-ADUser `
    -Name $Username `
    -GivenName $FirstName `
    -Surname $LastName

# Check if password is given
if ($null -ne $Password) {

    #
    Set-ADAccountPassword `
        -Identity $Username `
        -NewPassword $Password

    #
    Enable-ADAccount `
        -Identity $Username

}

#=====================================================================================================

Repair-User $Username