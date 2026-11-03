---
name: apqp-stage-gates
description: Use for multi-stage or high-impact feature delivery.
---
# APQP development gates

## Trigger
Use for multi-stage or high-impact feature delivery.

## Operating rule
Plan design, implementation, validation and release gates. Require evidence appropriate to risk, not lengthy documents. Skip formal gates for trivial changes. A failed mandatory gate blocks promotion.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
