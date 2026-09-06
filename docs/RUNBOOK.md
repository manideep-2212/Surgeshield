# Operations Runbook

## Service unhealthy

1. Check `http://localhost:8080/health`.
2. Run `docker compose ps`.
3. Inspect logs: `docker compose logs --tail=100 app1 app2 app3`.
4. Restart only the unhealthy API.
5. Nginx should continue routing to healthy nodes.

## Database issue

Check:
`docker compose logs --tail=100 postgres`

Do not delete the volume in production.

## Redis issue

Check:
`docker compose logs --tail=100 redis`

Redis is not the source of truth for seats.

## Queue issue

Check:
`docker compose logs --tail=100 worker`

Registrations remain committed even if notification delivery is delayed.

## Local clean reset

Only for development:

```powershell
docker compose down -v
docker compose up --build
```

This deletes local PostgreSQL/Redis volumes.
