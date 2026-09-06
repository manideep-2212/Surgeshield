$login = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/auth/login" -ContentType "application/json" -Body '{"email":"attendee@surgeshield.local","password":"Password@123"}'
$token=$login.token
Write-Host "Sending 120 registration requests concurrently through Nginx (ThrottleLimit: 40)..."
$results = 1..120 | ForEach-Object -Parallel {
  $headers=@{Authorization="Bearer $using:token";"Idempotency-Key"="load-$(Get-Date -Format 'yyyyMMddHHmmss')-$($_)"}
  try {
    $r=Invoke-WebRequest -Method Post -Uri "http://localhost:8080/api/events/1/register" -Headers $headers -ContentType "application/json" -Body '{"quantity":1}'
    $r.StatusCode
  } catch { if($_.Exception.Response){[int]$_.Exception.Response.StatusCode}else{"ERR"} }
} -ThrottleLimit 40

$success = ($results | Where-Object { $_ -eq 200 -or $_ -eq 201 }).Count
$rejected = ($results | Where-Object { $_ -eq 409 }).Count
$limited = ($results | Where-Object { $_ -eq 429 }).Count
Write-Host "Load test completed:"
Write-Host "  Success: $success | Sold Out (409): $rejected | Rate Limited (429): $limited"
Write-Host "Open http://localhost:8080/api/events/1 to verify remaining capacity."
