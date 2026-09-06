# 5-Minute Hackathon Demo

## 1. Open the UI
`http://localhost:8080`

## 2. Organizer
Login:
`organizer@surgeshield.local`
`Password@123`

Show:
- Operations Dashboard
- service health
- event capacity
- queue
- recent activity
- Create Event

## 3. Attendee
Sign out and login:
`attendee@surgeshield.local`
`Password@123`

Register for an event. Show:
- confirmation
- My Registrations
- notification queued

## 4. Resilience
In terminal:

```powershell
docker compose stop app2
```

Refresh `/health` and the UI. Explain Nginx failover.

Restart:

```powershell
docker compose start app2
```

## 5. Concurrency
Run:

```powershell
.\scripts\load-test.ps1
```

Explain that PostgreSQL `FOR UPDATE` serializes access to the event inventory row and prevents overbooking.

## 6. Architecture story

Say:

> "The API is stateless and horizontally scalable. Nginx provides the public entry point, rate limiting and load balancing. Redis handles short-lived read caching and queue infrastructure. PostgreSQL is the authoritative seat inventory, and row-level locking plus unique constraints protect concurrency. Registration commits before asynchronous notification processing, so downstream providers cannot block the critical path. In production, the same container runs under Kubernetes HPA for automatic scale-out and scale-in."
