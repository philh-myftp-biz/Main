#===================================================
# HOST

setx OLLAMA_HOST "0.0.0.0:11434" /M

#===================================================
# FIREWALL

$rule = Get-NetFirewallRule `
    -DisplayName 'Ollama' `
    -ErrorAction SilentlyContinue

if ($null -eq $rule) {

    New-NetFirewallRule `
        -DisplayName 'Ollama' `
        -Direction Inbound `
        -LocalPort 11434 `
        -Protocol TCP `
        -Action Allow `
        -Verbose

}

#===================================================
# DATA DIR

$SRC = "E:\AI\Ollama\data\"

$DST = "C:\Users\$env:username\.ollama\"

New-Item `
    -Path $SRC `
    -ItemType Directory `
    -ErrorAction SilentlyContinue `
    -Verbose

Remove-item `
    -Path $DST `
    -Force -Recurse -Verbose

New-Item `
    -Path $DST `
    -ItemType Junction `
    -Target $SRC `
    -Verbose

#===================================================