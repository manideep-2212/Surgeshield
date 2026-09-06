# Production autoscaling blueprint

The local Docker Compose stack intentionally uses three named API nodes so the resilience behavior is visible on one laptop.

For production, deploy the same stateless API image behind a Kubernetes Service and HorizontalPodAutoscaler (HPA). Recommended policy:

- minReplicas: 3
- maxReplicas: 20
- target CPU utilization: 60%
- additionally expose custom metrics for requests/sec and p95 latency
- use PodDisruptionBudget
- use readiness/liveness probes
- use a managed PostgreSQL/Redis service
- use a CDN/WAF at the global edge

Example HPA skeleton:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: event-api
spec:
  minReplicas: 3
  maxReplicas: 20
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: event-api
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

This is the production mechanism for automatic scale-out during spikes and scale-in after traffic stabilizes.
