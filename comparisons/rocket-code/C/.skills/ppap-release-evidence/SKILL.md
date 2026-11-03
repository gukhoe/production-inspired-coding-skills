---
name: ppap-release-evidence
description: Use before high-risk deployment or release approval.
---
# PPAP-inspired release evidence

## Trigger
Use before high-risk deployment or release approval.

## Operating rule
Collect concise requirement-to-test mapping, build id, exact commands, exit codes, artifact hashes, unresolved risks and rollback readiness. No fabricated evidence. Missing required proof means UNVERIFIED, not PASS.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
