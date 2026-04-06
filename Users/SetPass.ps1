
param(
    [string] $Username,
    [string] $Password
)

Set-ADAccountPassword `
    -Identity $Username `
    -NewPassword (ConvertTo-SecureString -String $Password -AsPlainText -Force) `
    -Reset

Enable-ADAccount `
    -Identity $Username