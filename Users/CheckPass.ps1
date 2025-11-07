
param(
    [string] $Username,
    [string] $Password
)

$obj = (New-Object DirectoryServices.DirectoryEntry "", $Username, $Password)

($obj.psbase.name -ne $null) `
    | ConvertTo-Json `
    | Write-Output
