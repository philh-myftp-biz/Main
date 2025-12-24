
$port = (Test-NetConnection localhost -Port 32400)

$port.TcpTestSucceeded | ConvertTo-Json | Write-Host
