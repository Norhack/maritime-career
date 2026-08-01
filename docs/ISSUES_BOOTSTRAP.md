# Issues Bootstrap — AutoApply AI Delivery Plan

Use this file to create milestones and issues in GitHub.

## Milestones
1. M1-MVP
2. M2-Reliability
3. M3-Intelligence
4. M4-Production

## Labels (recommended)
- area/backend
- area/frontend
- area/automation
- area/llm
- area/infra
- area/observability
- area/security
- type/feature
- type/chore
- type/bug
- priority/p0
- priority/p1
- priority/p2

---

## Issue 1 — Unify apply mode enums across API, settings, and models
**Labels:** area/backend, type/chore, priority/p0
**Milestone:** M1-MVP

### Description
The architecture currently mixes `auto` and `autonomous`. Standardize all contracts to `autonomous | review | batch`.

### Tasks
- Update request/response schemas.
- Update DB model constraints.
- Update frontend enums and settings forms.
- Add migration for existing values if needed.
- Add tests for validation and serialization.

### Acceptance Criteria
- All API endpoints accept/return only `autonomous|review|batch`.
- Existing records are migrated safely.
- Tests pass.

---

## Issue 2 — Implement application state machine and transition guards
**Labels:** area/backend, type/feature, priority/p0
**Milestone:** M1-MVP

### Description
Implement explicit allowed transitions for application lifecycle.

### Allowed transitions
- `queued -> pending_review -> applying -> applied`
- `applying -> failed`
- `applied -> interview|rejected|offer|withdrawn`

### Tasks
- Add transition map in domain layer.
- Validate transitions in service methods.
- Add audit note on status change.

### Acceptance Criteria
- Invalid transitions return clear 4xx errors.
- Transition history is persisted.

---

## Issue 3 — Add idempotency keys for application submissions
**Labels:** area/backend, type/feature, priority/p0
**Milestone:** M2-Reliability

### Description
Prevent duplicate applications due to retries, re-clicks, or worker restarts.

### Tasks
- Define idempotency key strategy.
- Add DB unique constraint/index.
- Enforce in API create/batch endpoints.
- Enforce in worker before submit step.

### Acceptance Criteria
- Duplicate requests return prior result/reference.
- No duplicate platform submissions for same key.

---

## Issue 4 — Build first platform plugin with resilient selectors
**Labels:** area/automation, type/feature, priority/p0
**Milestone:** M1-MVP

### Description
Implement first production-grade platform plugin with robust selectors and fallback strategies.

### Tasks
- Implement `search`, `scrape_details`, `apply`, `login`.
- Selector abstraction layer with versioned selector sets.
- Retry for stale element / navigation timeout.
- Screenshot on each major step.

### Acceptance Criteria
- Happy path flow works end-to-end in E2E.
- Failure reason taxonomy captured.

---

## Issue 5 — Worker retry/backoff policy by failure class
**Labels:** area/backend, area/automation, type/feature, priority/p0
**Milestone:** M2-Reliability

### Description
Differentiate transient/permanent/challenge failures and apply appropriate retry strategies.

### Tasks
- Classify exceptions.
- Configure exponential backoff with jitter for transient errors.
- Route repeated failures to dead-letter queue.
- Emit retry metrics/events.

### Acceptance Criteria
- Transient failures are retried automatically.
- Permanent failures fail fast with actionable reason.

---

## Issue 6 — Session persistence, rotation, and secure storage
**Labels:** area/automation, area/security, type/feature, priority/p1
**Milestone:** M2-Reliability

### Description
Persist browser sessions safely and rotate when stale/invalid.

### Tasks
- Encrypt session artifacts at rest.
- Add TTL and refresh logic.
- Add manual re-auth intervention flow.

### Acceptance Criteria
- Sessions survive restarts when valid.
- Expired sessions trigger controlled recovery.

---

## Issue 7 — Define and version WebSocket event schema
**Labels:** area/backend, area/frontend, type/chore, priority/p1
**Milestone:** M1-MVP

### Description
Stabilize event payloads for real-time updates and backward compatibility.

### Tasks
- Add event envelope `{version,type,timestamp,correlation_id,data}`.
- Version initial schema as `v1`.
- Add frontend parser guards.

### Acceptance Criteria
- Frontend handles all declared event types without runtime errors.

---

## Issue 8 — ATS scoring service with threshold policy
**Labels:** area/backend, type/feature, priority/p1
**Milestone:** M3-Intelligence

### Description
Implement weighted ATS composite score and threshold-based optimization trigger.

### Tasks
- Keyword + semantic + skills + format scoring.
- Configurable weights and minimum threshold.
- Persist score components for analytics.

### Acceptance Criteria
- API returns total + component breakdown.

---

## Issue 9 — LLM fallback and budget controls
**Labels:** area/llm, area/backend, type/feature, priority/p1
**Milestone:** M3-Intelligence

### Description
Ensure reliable and cost-controlled LLM operations.

### Tasks
- Provider priority and fallback chain.
- Timeout and retry caps.
- Per-purpose budget thresholds.
- Usage logging with model/provider metadata.

### Acceptance Criteria
- Failed provider automatically falls back.
- Budget cap breaches are surfaced and enforced.

---

## Issue 10 — Structured failure taxonomy in application results
**Labels:** area/backend, area/frontend, type/feature, priority/p1
**Milestone:** M2-Reliability

### Description
Expose machine-readable failure reasons for recovery and analytics.

### Suggested reason codes
- `NETWORK_TIMEOUT`
- `SELECTOR_NOT_FOUND`
- `UNSUPPORTED_FORM`
- `CAPTCHA_REQUIRED`
- `VALIDATION_ERROR`
- `PLATFORM_BLOCKED`

### Acceptance Criteria
- UI displays user-friendly guidance mapped from reason codes.

---

## Issue 11 — End-to-end tests for critical workflows
**Labels:** area/backend, area/frontend, type/chore, priority/p0
**Milestone:** M2-Reliability

### Description
Create E2E suite for job search to apply completion and key failure paths.

### Tasks
- Happy path: search -> review -> approve -> apply -> complete.
- Failure path: captcha/challenge -> intervention required.
- Failure path: network timeout -> retry then success/fail.

### Acceptance Criteria
- Tests run in CI and block merge on failure.

---

## Issue 12 — Prometheus metrics and Grafana dashboard baseline
**Labels:** area/observability, area/infra, type/feature, priority/p1
**Milestone:** M4-Production

### Description
Operational dashboards for throughput, failure, cost, and latency.

### Tasks
- Export core app/worker/LLM metrics.
- Add dashboard JSON and alert thresholds.
- Add runbook links for alerts.

### Acceptance Criteria
- Dashboards render expected panels in staging.

---

## Issue 13 — SQLite to PostgreSQL migration plan and cutover
**Labels:** area/infra, area/backend, type/chore, priority/p1
**Milestone:** M4-Production

### Description
Plan and execute safe cutover to PostgreSQL for production workloads.

### Tasks
- Compatibility audit.
- Migration scripts and verification checks.
- Backup and rollback procedure.

### Acceptance Criteria
- Staging cutover completed and verified.

---

## Issue 14 — Encrypt sensitive artifacts and secrets hardening
**Labels:** area/security, area/infra, type/feature, priority/p0
**Milestone:** M4-Production

### Description
Protect API keys, resumes, cookies, screenshots, and generated documents.

### Tasks
- Secrets loading policy.
- Artifact encryption and key rotation design.
- PII redaction in logs.

### Acceptance Criteria
- Security checklist passes for staging release.

---

## Issue 15 — Platform health monitor and canary automation checks
**Labels:** area/automation, area/observability, type/feature, priority/p2
**Milestone:** M4-Production

### Description
Detect integration drift and platform outages early.

### Tasks
- Daily canary flow per platform.
- Success/failure trend metrics.
- Auto-disable unstable platform integrations.

### Acceptance Criteria
- Alerts trigger on sustained degradation.

