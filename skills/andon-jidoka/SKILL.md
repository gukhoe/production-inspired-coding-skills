---
name: andon-jidoka
description: Use for failing safety gates, repeated errors or uncertain evidence.
---
# Andon and Jidoka automatic stop

## Trigger
Use for failing safety gates, repeated errors or uncertain evidence.

## Operating rule
Stop immediately on data loss, security regression, broken critical tests, unknown environment or repeat-failure budget exhaustion. Quarantine change, preserve logs and report BLOCKED or UNVERIFIED. Never silently continue.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
