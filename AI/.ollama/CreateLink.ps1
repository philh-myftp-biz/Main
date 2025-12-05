
$SRC = 'E:\Plex\.ollama\'

$DST = "C:\Users\$env:username\.ollama\"

Remove-item `
    -Path $SRC `
    -Force -Recurse

New-Item `
    -ItemType Junction `
    -Path $DST `
    -Target $SRC