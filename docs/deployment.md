# Deployment

## Local

~~~bash
cp .env.example .env
docker compose up --build
curl http://localhost:8000/health
~~~

Compose supplies PostgreSQL and Redis for integration development. The current
reference API executes synchronously; Redis is reserved for a production job
queue/cache.

## Kubernetes

deployment/kubernetes/api.yaml contains a non-root, read-only, resource-limited
API deployment, service, autoscaler, disruption budget and default-deny network
policy. Replace the image tag with an immutable digest produced by a reviewed
release.

~~~bash
kubectl apply -f deployment/kubernetes/api.yaml
~~~

Use a managed PostgreSQL service for production. Apply migrations through a
separate, auditable job before rolling the API.

## Production checklist

- image pinned by digest and signed;
- TLS and identity-aware ingress;
- API key or workload identity stored in a secret manager;
- database encryption, backups and point-in-time recovery;
- egress allow-list for approved data providers;
- separate raw, curated and run-manifest storage;
- no privileged containers or host mounts;
- structured audit logs with protected-data redaction;
- metrics for latency, infeasibility, missingness and source freshness;
- deterministic run IDs and immutable code/input hashes;
- human review before consequential use;
- disaster-recovery and rollback exercises.

## Scaling

Route heavy Monte Carlo jobs to an asynchronous worker pool and place a hard
deployment-level cap on sample count, memory and wall time. Cache only by the
full code, input, scenario and seed manifest. Never reuse a result solely because
a human-readable scenario name matches.
