# SurgeShield — Final Hackathon Package

A complete local reference implementation for the **SurgeShield: Build a Resilient, Self-Scaling Web Platform** brief.

## Included

- Professional responsive frontend
- Attendee + Organizer roles
- JWT login and bcrypt passwords
- Event browsing
- Registration flow
- My Registrations
- Organizer Operations Dashboard
- Event creation
- System Health
- Prometheus metrics
- Nginx reverse proxy
- 3 Node.js API instances
- PostgreSQL transactions and row locks
- Duplicate and idempotency protection
- Redis caching
- BullMQ asynchronous notifications
- Retry/backoff
- Health/readiness endpoints
- Load/failure test scripts
- Architecture diagram
- Sequence diagrams
- Trade-off analysis
- Security document
- Global/regional deployment plan
- Operations runbook
- Requirements matrix
- Kubernetes HPA production blueprint
- Presentation guide

## Run on Windows

### 1. Start Docker Desktop

Make sure Docker Desktop is running.

### 2. Open this folder

Open `SurgeShield_Event_Registration_Final` in VS Code.

### 3. Start everything

```powershell
docker compose up --build
```

Wait until PostgreSQL, Redis, app1, app2, app3, worker and nginx are running.

### 4. Open

`http://localhost:8080`

## Demo credentials

The server creates/refreshes these demo users on startup.

Attendee:
- Email: `attendee@surgeshield.local`
- Password: `Password@123`

Organizer:
- Email: `organizer@surgeshield.local`
- Password: `Password@123`

## If you previously ran an older version

For a clean local database:

```powershell
docker compose down -v
docker compose up --build
```

## Useful URLs

- Application: `http://localhost:8080`
- Health: `http://localhost:8080/health`
- Readiness: `http://localhost:8080/ready`
- Events API: `http://localhost:8080/api/events`
- Metrics: `http://localhost:8080/metrics`

## Resilience tests

Failure:

```powershell
.\scripts\failure-test.ps1
```

Load:

```powershell
.\scripts\load-test.ps1
```

## Requirement mapping

See `docs/REQUIREMENTS_MATRIX.md`.

## Important production note

The local stack uses three named API nodes to make load balancing and failure testing easy on one laptop. True automatic scale-out/scale-in should be performed by a production orchestrator such as Kubernetes HPA or a managed cloud autoscaling service. The `k8s/README.md` contains the deployment policy and HPA blueprint.
