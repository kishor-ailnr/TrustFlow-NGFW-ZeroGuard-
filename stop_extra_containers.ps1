$keep = "cowrie"
$all = docker ps --format "{{.Names}}"
foreach ($name in $all) {
    if ($name -ne $keep) {
        Write-Host "Stopping $name..."
        docker stop $name | Out-Null
    } else {
        Write-Host "Keeping $name running."
    }
}
Write-Host "`nRemaining running containers:"
docker ps --format "table {{.Names}}\t{{.Status}}"
