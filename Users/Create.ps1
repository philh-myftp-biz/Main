
param (
    [string] $Username,
    [string] $FirstName,
    [string] $LastName,
    [String] $Password
)

Import-Module "$PSScriptRoot\mod.psm1" -Function Repair-User

#=====================================================================================================

$ADUser = Get-ADUser `
    -Identity $Username `
    -ErrorAction SilentlyContinue

# If user does not exist
if ($null -eq $ADUser) {

    # Create new Active Directory User
    New-ADUser `
        -Name $Username `
        -GivenName $FirstName `
        -Surname $LastName `
        -Verbose

# If user does exist
} else {

    Set-ADUser `
        -Identity $Username `
        -GivenName $FirstName `
        -Surname $LastName `
        -Verbose

}

# Check if password is given
if ($null -ne $Password) {

    Set-ADAccountPassword `
        -Identity $Username `
        -NewPassword (ConvertTo-SecureString -String $Password -AsPlainText -Force) `
        -Verbose

    Enable-ADAccount `
        -Identity $Username `
        -Verbose

}

#=====================================================================================================

Repair-User $Username