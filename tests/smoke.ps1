Write-Host "Health:"
Invoke-RestMethod http://localhost:8080/health | Format-List
Write-Host "Events:"
Invoke-RestMethod http://localhost:8080/api/events | ConvertTo-Json -Depth 5
