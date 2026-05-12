# Issue 11 - Production Backend and Async Ingestion

## Goal
Harden the system into a resilient backend service with async ingestion and recoverability.

## Scope
- In: Postgres, production vector store, Redis queue, workers, job states, retries, backup/restore, migrations.
- Out: advanced agent actions.

## Deliverables
- Async ingestion job orchestration
- Job status and retry management
- Backup/restore and migration runbooks

## Implementation Tasks
1. Migrate metadata DB to Postgres.
2. Add Redis + worker runtime.
3. Implement ingestion job state machine.
4. Add retry policies and dead-letter handling.
5. Add backups and restore verification flow.

## Tests
- Integration: async job lifecycle (pending->processing->completed/failed).
- Integration: retry path for transient parser failure.
- Ops test: backup + restore into clean environment.

## Definition of Done
- Large file ingestion is non-blocking.
- Failed jobs are retryable with logs.
- System survives restart without orphaned state.
- Migrations and restore tested.

## Success Metrics
- `job_success_rate >= 0.95` (excluding unsupported formats).
- `mean_recovery_time <= 15 min` after simulated restart.

## Deployment
- Release tag: `v0.11.0-production-backend`
- SLO + alert thresholds documented.
