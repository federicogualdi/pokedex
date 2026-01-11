## Production-readiness - quick technical checklist (given: retries, cache, Sentry, k6, coverage, CI)

### What’s already in a good place
- DDD + Ports/Adapters boundaries are clear
- Retries + caching exist
- Sentry + load testing (k6) + coverage + pipeline already present

---

## What to improve next (high signal)

### 1) Observability beyond Sentry
- **Structured JSON logs** + **correlation/request-id** propagated to outbound calls
- **Metrics** (Prometheus / OpenTelemetry): p95/p99 latency, 5xx rate, provider error rate, cache hit/miss, retry count
- **Tracing** (OpenTelemetry) to see the full path: route → service → provider

**TODO:** add `/health` (liveness) + `/ready` (readiness) with dependency checks configurable.

---

### 2) Resilience controls (not just retry)
Retries alone can amplify incidents.
- **Circuit breaker** per external provider
- **Concurrency limits** for outbound calls
- **Rate-limit handling** (429 + Retry-After)
- Ensure **timeouts** are enforced at HTTP client and request level (cancellation propagation)

---

### 3) Cache correctness for scale
You have cache, but production needs correctness + multi-replica behavior.
- If running >1 replica: prefer **shared cache (Redis)** or accept inconsistency explicitly
- **Stampede protection** (single-flight / per-key lock)
- Define **TTL policy** + **negative caching** (short TTL for not-found)

---

### 4) API stability & error contract
- Define and document a stable **error schema** (`code`, `message`, `correlationId`)
- Ensure domain errors map consistently to HTTP status codes
- Add **API versioning** strategy (`/api/v1`) if you expect public consumers

---

### 5) Security & abuse protection
- **Rate limiting** (per IP / per key) + request size limits
- Tight **CORS** and security headers (usually at reverse proxy)
- Input constraints for `name` (length/charset) to reduce attack surface

---

## Minimal “to ship to prod” runbook
- Deploy: run behind reverse proxy (TLS termination), autoscaling + multiple replicas
- SLOs: define p95 latency + error budget, alert on provider failure and retry spikes
- Backups/DR (if you add state like Redis): document restore procedure
