# Requirements & Evidence Matrix

| Brief requirement | Implementation / evidence |
|---|---|
| Scale out during unpredictable spikes | 3 stateless API nodes behind Nginx locally; production HPA blueprint in `k8s/README.md` |
| Scale back after stabilization | Production HPA min/max policy documented |
| Avoid unnecessary infrastructure cost | Stateless APIs + autoscaling blueprint |
| Concurrent registrations | PostgreSQL transaction + `SELECT ... FOR UPDATE` |
| Duplicate requests | Idempotency-Key + unique DB constraints |
| Last-seat correctness | Row lock makes seat decrement atomic |
| Failed unhealthy service | Nginx upstream fail handling + `/health` and `/ready` |
| Downstream failures | BullMQ async queue + exponential retries |
| Notifications async | Registration commits before queue job |
| Cache | Redis event-list cache with short TTL and invalidation |
| Alert/operations view | Organizer dashboard with service state, queue and capacity |
| Authentication | JWT + bcrypt |
| Multiple user roles | ATTENDEE and ORGANIZER RBAC |
| API integration | REST endpoints under `/api` |
| Security | Helmet, CORS, rate limit, input validation, parameterized SQL |
| Monitoring | Prometheus metrics + structured request IDs |
| Working demo | Docker Compose + Nginx on `localhost:8080` |
| Sequence diagrams | `SEQUENCE_DIAGRAMS.md` |
| Architecture diagram | `ARCHITECTURE.md` |
| Trade-offs | `TRADEOFFS.md` |
| Global vs regional | `GLOBAL_REGIONAL.md` |
| Edge caching/latency | Architecture document |
| Data residency | Global/regional document |
| Failure recovery | `RUNBOOK.md` |
| Test plan | `TEST_PLAN.md` |
