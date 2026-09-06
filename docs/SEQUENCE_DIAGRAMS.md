# Sequence Diagrams

## 1. Registration happy path

```text
Attendee -> Nginx: POST /events/{id}/register
Nginx -> API: route request
API -> PostgreSQL: BEGIN
API -> PostgreSQL: SELECT event FOR UPDATE
PostgreSQL --> API: locked row + available seats
API -> PostgreSQL: INSERT registration
API -> PostgreSQL: UPDATE available_seats - 1
API -> PostgreSQL: INSERT notification_outbox
API -> PostgreSQL: COMMIT
API -> Redis/BullMQ: enqueue notification
API --> Nginx: 201 Confirmed
Nginx --> Attendee: confirmation
Worker -> Notification provider: send asynchronously
```

## 2. Concurrent last-seat race

```text
User A -> API: register
User B -> API: register
API A -> DB: SELECT event FOR UPDATE
API B -> DB: SELECT event FOR UPDATE (waits)
DB --> API A: 1 seat
API A -> DB: insert + decrement to 0
API A -> DB: COMMIT
DB --> API B: lock acquired
API B -> DB: available_seats = 0
API B --> User B: 409 Sold out
```

## 3. Duplicate

```text
User -> API: same event + same user
API -> DB: check unique registration
DB --> API: existing row
API --> User: 409 Already registered
```

## 4. Failure

```text
User -> Nginx
Nginx -> app2: request
app2: unhealthy
Nginx -> app1/app3: retry/failover
Nginx --> User: response
```
