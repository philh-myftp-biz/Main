
function Add-GitIgnoreItem {
    param([string]$Path)

    # Convert LiteralPath To RelativePath
    if ($Path -like 'E:\Minecraft\*') {
        $Path = [regex]::Replace($Path, 'E:\\Minecraft', '', 1)
    }

    # Add the pattern to .gitignore
    Add-Content `
        -Path "$PSScriptRoot\.gitignore" `
        -Value $Path
    
    Write-Host "Added $Path to .gitignore" -ForegroundColor Green

}

#==================================================================================

# Clear .gitignore
Set-Content `
    -Path "$PSScriptRoot\.gitignore" `
    -Value '# Auto Generated'


Add-GitIgnoreItem '**/__pycache__/'

Add-GitIgnoreItem '**/session.lock'

#==================================================================================
# WORLDS

Add-GitIgnoreItem '!/worlds/'

$Worlds = Get-ChildItem "$PSScriptRoot/Worlds/" `
    -Directory `
    | Where-Object Name -NotLike '__*__'

$Worlds | ForEach-Object {

    $Base = "/Worlds/$($_.Name)"

    Add-GitIgnoreItem "!$Base" 
    Add-GitIgnoreItem "$Base/*"

    Add-GitIgnoreItem "!$Base/config.yaml"
    Add-GitIgnoreItem "!$Base/world"

}

#==================================================================================
# FINIT

# Purge Cache
git.exe rm -r --cached . -f

# ReTrack Everything
git.exe add . --verbose