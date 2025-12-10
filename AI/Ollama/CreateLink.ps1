
$SRC = "E:\AI\Ollama\data"

$DST = "C:\Users\$env:username\.ollama\"

New-Item `
    -Path $SRC `
    -ItemType Directory `
    -Verbose

Remove-item `
    -Path $DST `
    -Force -Recurse -Verbose

New-Item `
    -Path $DST `
    -ItemType Junction `
    -Target $SRC `
    -Verbose