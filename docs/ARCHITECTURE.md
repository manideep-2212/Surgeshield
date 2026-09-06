# SurgeShield Architecture

```text
                         GLOBAL USERS
                              |
                         CDN / WAF
                              |
                    Global Load Balancer
                       /            \
                Region A            Region B
                   |                   |
              Regional LB         Regional LB
                   |                   |
             +-----+-----+       +-----+-----+
             |     |     |       |     |     |
            API1  API2  API3    API1  API2  API3
             |     |     |       |     |     |
             +-----+-----+       +-----+-----+
                   |                   |
             Redis / Queue       Redis / Queue
                   |                   |
            PostgreSQL primary/replicas per region
```

## Local implementation

```text
Browser
   |
Nginx :8080
   |
   +------ app1 :3000
   +------ app2 :3000
   +------ app3 :3000
             |
       PostgreSQL
             |
          Redis
             |
          BullMQ
             |
        Worker
```

### Why Nginx?

- reverse proxy
- load balancing
- rate limiting at the edge
- upstream retry/failure handling
- single public entry point

### Why PostgreSQL?

Seat inventory is strongly consistent. A relational transaction with row locking is straightforward and auditable.

### Why Redis?

Event listings are read-heavy and change less frequently than registration requests. A short TTL reduces database reads. Redis also backs BullMQ.

### Why asynchronous notifications?

Registration should finish without waiting for email/SMS/push providers. The queue isolates downstream latency and retries failures.

### Scale model

Local: three visible API instances.

Production: stateless API Deployment + HPA. Scale based on CPU plus custom request-rate/p95-latency metrics. Use minimum warm capacity for sudden spikes.

### Global vs regional

Route users to the nearest healthy region. Keep event inventory authoritative in one region per event or use a carefully designed reservation service. Do not use active-active writes for the same seat pool without a consistency strategy.

### Data residency

Partition event/user data by residency requirements. Keep sensitive user records within the allowed region and replicate only permitted aggregates or operational data.
