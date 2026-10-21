$result = Test-NetConnection -ComputerName localhost -Port 2222
if ($result.TcpTestSucceeded) {
    Write-Host "COWRIE OK - port 2222 is reachable." -ForegroundColor Green
} else {
    Write-Host "COWRIE NOT REACHABLE - check 'docker ps' and container logs." -ForegroundColor Red
}
