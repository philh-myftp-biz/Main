
param(
    [string] $Username,
    [securestring] $Password
)

Set-ADAccountPassword `
    -Identity $Username `
    -NewPassword $Password `
    -Reset

Enable-ADAccount `
    -Identity $Username