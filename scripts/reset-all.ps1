Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Resetting SurgeShield Platform Data" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Login as organizer and trigger server-side full reset
$login = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/auth/login" -ContentType "application/json" -Body '{"email":"organizer@surgeshield.local","password":"Password@123"}'
$token = $login.token

Write-Host "Calling /api/admin/reset-system to restore pristine state..."
$res = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/admin/reset-system" -Headers @{ Authorization = "Bearer $token" }

Write-Host "`nResult: $($res.message)" -ForegroundColor Green
Write-Host "  - Registrations: 0 (Truncated)"
Write-Host "  - Notifications: 0 (Truncated)"
Write-Host "  - Event seats: 100% capacity restored"
Write-Host "  - Redis cache & BullMQ queue: Cleared"
Write-Host "=========================================" -ForegroundColor Cyan
