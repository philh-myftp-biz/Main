
param(
    [string] $Name,
    [string] $Username,
    [securestring] $Password = (New-Object System.Security.SecureString),
    [string] $CMD
)

$cred = New-Object `
    -TypeName System.Management.Automation.PSCredential `
    -ArgumentList($Username, $Password)

if ($null -eq $CMD) {

    Enter-PSSession `
        -VMName $Name `
        -Credential $cred `
        -Authentication NegotiateWithImplicitCredentials

} else {

    Invoke-Command `
        -VMName $Name `
        -ScriptBlock { $cmd } `
        -Credential $cred

}