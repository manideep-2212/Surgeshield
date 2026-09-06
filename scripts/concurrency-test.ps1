Write-Host ========================================================== -ForegroundColor Cyan
Write-Host SurgeShield Concurrency & Row-Locking Live Demonstration -ForegroundColor Cyan
Write-Host ========================================================== -ForegroundColor Cyan

# 1. Login
Write-Host 1. Authenticating as attendee...
 = Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/auth/login -ContentType application/json -Body '{email:attendee@surgeshield.local,password:Password@123}'
 = .token

# 2. Reset Demo Event to 5 seats
Write-Host 2. Resetting Concurrency Demo Event to exactly 5 seats...
 = Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/demo/reset-concurrency-event
 = .event.id
 = .event.available_seats
Write-Host  Event: (ID: )
Write-Host  Initial Available Seats: 

# 3. Fire 15 concurrent registration requests
Write-Host 3. Firing 15 concurrent registration requests through Nginx...
Write-Host  (Simulating a traffic spike booking the last 5 seats simultaneously)

 = {
    param(, , )
     = concurrent-cli-- + (Get-Date -Format yyyyMMddHHmmssffff)
     = @{
        Authorization = Bearer 
        Idempotency-Key = 
    }
     = '{quantity:1}'
     = [System.Diagnostics.Stopwatch]::StartNew()
    try {
         = Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/events//register -Headers  -ContentType application/json -Body 
        .Stop()
        [PSCustomObject]@{
            Request = 
            Status = 201
            Result = Confirmed (#)
            Node = .servedBy
            LatencyMs = .ElapsedMilliseconds
        }
    } catch {
        .Stop()
         = 409
         = Insufficient seats
        if (.Exception.Response) {
             = [int].Exception.Response.StatusCode
        }
        [PSCustomObject]@{
            Request = 
            Status = 
            Result = Rejected (Sold Out / Locked)
            Node = N/A
            LatencyMs = .ElapsedMilliseconds
        }
    }
}

 = 1..15 | ForEach-Object -Parallel  -ArgumentList , ,  -ThrottleLimit 15

Write-Host 
Live Execution Results: -ForegroundColor Yellow
 | Sort-Object Request | Format-Table -AutoSize

# 4. Verify Capacity & Concurrency Protection
 = Invoke-RestMethod -Method Get -Uri http://localhost:8080/api/events/
 = .event.available_seats
 = ( | Where-Object { .Status -eq 201 }).Count
 = ( | Where-Object { .Status -ne 201 }).Count

Write-Host ========================================================== -ForegroundColor Cyan
Write-Host Concurrency Summary: -ForegroundColor Cyan
Write-Host  Initial Available Seats: 
Write-Host  Total Parallel Requests: 15
Write-Host  Successfully Booked:  -ForegroundColor Green
Write-Host  Safely Rejected:  -ForegroundColor Yellow
Write-Host  Final Available Seats:  -ForegroundColor Red

if ( -eq 0 -and  -eq ) {
    Write-Host 
SUCCESS: Zero overbooking! Exactly seats consumed. Row locking fully verified. -ForegroundColor Green
} else {
    Write-Host 
Warning: Unexpected seat count or booking count. -ForegroundColor Red
}
Write-Host ========================================================== -ForegroundColor Cyan
