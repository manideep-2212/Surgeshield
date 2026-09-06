# Test Plan

## 1. Functional

- create account
- login as attendee
- login as organizer
- organizer creates event
- attendee registers
- attendee views registration
- duplicate registration is rejected

## 2. Concurrency

Run PowerShell:

```powershell
.\scripts\load-test.ps1
```

The 100-seat event receives 120 unique concurrent attempts. Verify the final registration count never exceeds 100.

## 3. Idempotency

Send the same event/user request twice with the same `Idempotency-Key`. The second request must not create another registration.

## 4. Failure

Run:

```powershell
.\scripts\failure-test.ps1
```

Stop app2 and continue sending traffic through Nginx. The service should remain reachable through healthy nodes.

## 5. Observability

Open:
- `/health`
- `/ready`
- `/metrics`
- Organizer → Operations
- Organizer → System Health
