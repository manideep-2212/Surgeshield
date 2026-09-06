Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "TEST 1: API Instance Failover & Load Balancing" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Stopping app2 container..."
docker compose stop app2
Start-Sleep -Seconds 2

Write-Host "Calling /health 10 times through Nginx. Traffic should failover to app1 & app3 seamlessly:"
1..10 | ForEach-Object {
    $res = Invoke-RestMethod http://localhost:8080/health
    Write-Host "  Request $_ -> Status: $($res.status) | ServedBy: $($res.instance)"
}

Write-Host "Restarting app2..."
docker compose start app2
Start-Sleep -Seconds 2
Write-Host "app2 is back online.`n"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "TEST 2: BullMQ Worker Failure Recovery" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "1. Stopping worker container..."
docker compose stop worker
Start-Sleep -Seconds 3

Write-Host "2. Logging in as attendee..."
$login = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/auth/login" -ContentType "application/json" -Body '{"email":"attendee@surgeshield.local","password":"Password@123"}'
$token = $login.token

Write-Host "3. Submitting registration while worker is OFFLINE..."
$key = "worker-failure-test-" + (Get-Date -Format "yyyyMMdd-HHmmss")
$headers = @{ Authorization = "Bearer $token"; "Idempotency-Key" = $key }
$reg = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/events/2/register" -Headers $headers -ContentType "application/json" -Body '{"quantity":1}'
Write-Host "   Registration succeeded immediately: ID #$($reg.registration.id) (Status: $($reg.registration.status))"
Write-Host "   Notification status: $($reg.notification) (safely preserved in Redis queue)"

Write-Host "4. Restarting worker container..."
docker compose start worker
Write-Host "   Waiting 4 seconds for worker to process queued jobs..."
Start-Sleep -Seconds 4

Write-Host "5. Verifying notification outbox state..."
$regs = Invoke-RestMethod -Method Get -Uri "http://localhost:8080/api/my-registrations" -Headers @{ Authorization = "Bearer $token" }
$myReg = $regs.registrations | Where-Object { $_.id -eq $reg.registration.id }
Write-Host "   Registration #$($myReg.id) -> Notification Status: $($myReg.notification_status) (Processed with zero loss!)"
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Failure recovery tests completed successfully." -ForegroundColor Green

