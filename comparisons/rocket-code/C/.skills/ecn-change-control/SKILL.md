---
name: ecn-change-control
description: Use when modifying existing APIs, schemas, workflows or contracts.
---
# Engineering change control

## Trigger
Use when modifying existing APIs, schemas, workflows or contracts.

## Operating rule
Record request, approved scope, affected interfaces and rollback. Changes outside scope become separate issues. For destructive or compatibility-breaking change require owner approval. Verify downstream dependencies.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
