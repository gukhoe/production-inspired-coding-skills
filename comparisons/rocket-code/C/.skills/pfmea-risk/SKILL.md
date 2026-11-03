---
name: pfmea-risk
description: Use when business logic, state, security or persistence changes.
---
# PFMEA software risk analysis

## Trigger
Use when business logic, state, security or persistence changes.

## Operating rule
Identify up to five credible failure modes, effects, causes and controls. Rate severity, occurrence and detection 1-10 only if evidence allows; unknown stays unknown. High severity overrides low RPN. Convert highest risks to executable tests.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
