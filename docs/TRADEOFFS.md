# Trade-offs

## PostgreSQL row lock vs distributed lock

Chosen: PostgreSQL row lock.

Why:
- seat inventory already lives in PostgreSQL
- transaction covers registration + inventory decrement
- fewer moving parts
- easy to explain and audit

Alternative: Redis distributed lock. Useful at larger scale but introduces lock expiry, fencing and failure-mode complexity.

## SQL vs NoSQL

Chosen: SQL for inventory.

Why:
- strong consistency
- transactions
- unique constraints
- row-level locking

NoSQL can be useful for high-volume read models, activity streams or analytics.

## REST vs GraphQL

Chosen: REST.

Why:
- small hackathon surface
- simple caching and load testing
- straightforward Nginx routing

GraphQL becomes attractive when clients need highly variable aggregates.

## Monolith vs microservices

Chosen: modular stateless Node.js service plus worker.

Why:
- fast to ship
- independently scalable API and worker
- fewer operational dependencies than many microservices

Split services only when ownership, scaling or failure boundaries justify it.

## Cache vs source of truth

Redis caches event listings; PostgreSQL remains authoritative. A cache miss or invalidation failure cannot create an extra seat because registration never trusts the cache for inventory.
