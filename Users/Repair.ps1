
Get-ADUser -Filter * -SearchBase "CN=Users, DC=philh, DC=local" `
    | ForEach-Object -Process {

        $Username = $_.SamAccountName

        $Dir = "E:/Users/philh/$Username"

        if ($Username.ToLower() -ne 'administrator') {

            Write-Output "Repairing: $Username"

            #=====================================================================================================

            # Create Home Folder
            New-Item `
                -Path $Dir `
                -ItemType Directory `
                -ErrorAction SilentlyContinue

            # Create AppData Folder
            New-Item `
                -Path "$Dir/__AppData__" `
                -ItemType Directory `
                -ErrorAction SilentlyContinue

            # Hide AppData Folder
            Set-ItemProperty `
                -LiteralPath "$Dir/__AppData__" `
                -Name Attributes `
                -Value Hidden

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

            New-SmbShare `
                -Name "User-$Username" `
                -Path $Dir `
                -ErrorAction SilentlyContinue `
                | Out-Null

            Revoke-SmbShareAccess `
                -Name "User-$Username" `
                -AccountName "Everyone" `
                -Force | Out-Null

            Grant-SmbShareAccess `
                -Name "User-$Username" `
                -AccountName $Username `
                -AccessRight Full `
                -Force | Out-Null
            
            Grant-SmbShareAccess `
                -Name "User-$Username" `
                -AccountName "Administrators" `
                -AccessRight Full `
                -Force


            #=====================================================================================================

            New-Item `
                -ItemType Directory `
                -Path "$Dir\Website" `
                | Out-Null

            New-Item `
                -ItemType Junction `
                -Target "$Dir\Website" `
                -Path "E:\Website\Root\Servers\FTP\User Web Shares\$Username" `
                | Out-Null

            $Acl = Get-Acl -Path "$Dir\Website"

            # Create new access rule for 'FullControl' permissions, inheriting to subfolders and files
            $Acl.AddAccessRule((New-Object System.Security.AccessControl.FileSystemAccessRule(
                "IIS_IUSRS",
                "Read",
                "ContainerInherit,ObjectInherit",
                "None",
                "Allow"
            )))

            # Apply the updated ACL
            Set-Acl `
                -Path "$Dir\Website" `
                -AclObject $Acl

        }
}