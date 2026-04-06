Import-Module 'E:/Virtual Machines/mod.psm1' -Function Repair-VirtualMachine
function Repair-User {

    param(
        [string] $Username
    )

    $Dir = "E:/Users/philh/$Username"

    if ($Username.ToLower() -ne 'administrator') {

        Write-Host "Repairing: " -NoNewline
        Write-Host $Username -ForegroundColor Cyan

        #=====================================================================================================

        # Create Home Folder
        New-Item `
            -Path $Dir `
            -ItemType Directory `
            -ErrorAction SilentlyContinue `
            > $null

        #=====================================================================================================

        # Create AppData Folder
        New-Item `
            -Path "$Dir/__AppData__" `
            -ItemType Directory `
            -ErrorAction SilentlyContinue `
            > $null

        # Hide AppData Folder
        Set-ItemProperty `
            -LiteralPath "$Dir/__AppData__" `
            -Name Attributes `
            -Value Hidden `
            > $null

        
        New-Item `
            -ItemType Directory `
            -Path "$Dir\Website" `
            -ErrorAction SilentlyContinue `
            | Out-Null

        #=====================================================================================================

        # Create a blank ACL object
        $Acl = New-Object -TypeName System.Security.AccessControl.DirectorySecurity

        # Disable Inheritance
        $acl.SetAccessRuleProtection($true, $false)

        # Create new access rule for 'FullControl' permissions, inheriting to subfolders and files
        $Acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
            "Administrators",
            "FullControl",
            "ContainerInherit,ObjectInherit",
            "None",
            "Allow"
        )))

        # Create new access rule for 'FullControl' permissions, inheriting to subfolders and files
        $Acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
            $Username,
            "FullControl",
            "ContainerInherit,ObjectInherit",
            "None",
            "Allow"
        )))

        # Apply the updated ACL
        Set-Acl `
            -Path $Dir `
            -AclObject $Acl

        #=====================================================================================================
        
        # TODO fix, takes too long

        #$VM = Get-VM `
        #    -Name "User-$Username" `
        #    -ErrorAction SilentlyContinue

        # If the vm does not exist
        #if ($null -eq $VM) {
        #    ."E:/Virtual Machines/Create.ps1" `
        #        -Name "User-$Username" `
        #        | Out-Null
        #} else {
        #    Repair-VirtualMachine -Name "User-$Username"
        #}

    }

}

Export-ModuleMember -Function Repair-User