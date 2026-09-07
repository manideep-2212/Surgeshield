# SurgeShield — Resilient Event Registration Platform

SurgeShield is a resilient, scalable event-registration platform designed to
handle high-concurrency registration traffic while preventing overbooking,
duplicate registrations, and service failures.

The project focuses on real-world scalability and reliability rather than
surface-level novelty.

## Key Features

- Attendee and Organizer roles
- JWT authentication and bcrypt password hashing
- Event browsing and registration
- Duplicate and idempotency protection
- PostgreSQL transactions and row-level locking
- Connection pooling
- Redis caching
- BullMQ asynchronous notifications
- Retry and backoff mechanisms
- Nginx reverse proxy and load balancing
- 3 Node.js API instances
- Health and readiness endpoints
- Prometheus metrics
- Load and failure testing
- Kubernetes HPA production blueprint

## Architecture

```text
                    Browser
                       │
                       ▼
                    Nginx
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       API #1        API #2        API #3
          │            │            │
          └────────────┼────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
         PostgreSQL           Redis
        (Source of Truth)    (Cache/Queue)
                                │
                                ▼
                           BullMQ Worker
