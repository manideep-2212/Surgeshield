# Global vs Regional Deployment

## Global architecture

Use:
- DNS/global load balancing
- CDN/WAF for static assets and edge protection
- nearest healthy region routing
- regional API clusters
- regional caches
- managed PostgreSQL/Redis

## Latency

Keep static assets at the edge. Keep API calls in the nearest region. Avoid cross-region synchronous calls on the registration critical path.

## Consistency

For an event, choose a single authoritative inventory region (or shard the seat pool explicitly). Cross-region writes to the same inventory without a consensus/partition strategy can oversell.

## Data residency

Tag users/events with residency region. Keep restricted PII in the required geography. Replicate only data allowed by policy.

## Disaster recovery

Use backups and replicas. Define RPO/RTO per business requirement. During regional failure, fail traffic to a secondary region only if that region has a safe inventory strategy.
