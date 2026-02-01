
$directories = @(
    "E:\Plex\__pycache__",
    "E:\Plex\Plex Media Server\Cache",
    "E:\Plex\Plex Media Server\Plug-in Support\Caches"
)

$directories | ForEach-Object -Process {

    $_ | Remove-Item -Recurse -Force

}