
param(
    [string] $Username,
    [string] $FirstName,
    [string] $LastName,
    [securestring] $Password
)

$Dir = "E:/Users/philh/$Username"

#=====================================================================================================

# Create new Active Directory User
New-ADUser `
    -Name $Username `
    -GivenName $FirstName `
    -Surname $LastName

# Check if password is given
if ($Password -ne $null) {

    #
    Set-ADAccountPassword `
        -Identity $Username `
        -NewPassword $Password

    #
    Enable-ADAccount `
        -Identity $Username

}

#=====================================================================================================

# Create Home Folder
New-Item `
    -Path $Dir `
    -ItemType Directory

# Create AppData Folder
New-Item `
    -Path "$Dir/__AppData__" `
    -ItemType Directory

# Hide AppData Folder
(Get-Item "$Dir/__AppData__").Attributes += [System.IO.FileAttributes]::Hidden

#=====================================================================================================

# Create a blank ACL object
$Acl = New-Object -TypeName System.Security.AccessControl.DirectorySecurity

# Disable Inheritance
$acl.SetAccessRuleProtection($true, $false)


# Create new access rule for 'FullControl' permissions, inheriting to subfolders and files
$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "Administrators",
    "FullControl",
    "ContainerInherit,ObjectInherit",
    "None",
    "Allow"
)

# Add the rule to the ACL
$Acl.AddAccessRule($AccessRule)


# Create new access rule for 'FullControl' permissions, inheriting to subfolders and files
$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    $Username,
    "FullControl",
    "ContainerInherit,ObjectInherit",
    "None",
    "Allow"
)

# Add the rule to the ACL
$Acl.AddAccessRule($AccessRule)

# Apply the updated ACL
Set-Acl `
    -Path $Dir `
    -AclObject $Acl

#=====================================================================================================

New-SmbShare `
    -Name "User-$Username" `
    -Path $Dir `
    -FullAccess "PHILH\Administrators","PHILH\$Username" `
    -ErrorAction SilentlyContinue `
    | Out-Null