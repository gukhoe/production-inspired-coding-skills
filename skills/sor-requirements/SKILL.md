---
name: sor-requirements
description: Use for new features or ambiguous requirements.
---
# SOR and SOW requirements control

## Trigger
Use for new features or ambiguous requirements.

## Operating rule
Define inputs, outputs, invariants, acceptance criteria and explicit exclusions. Require a testable acceptance example. Never infer unstated behavior. Freeze scope for the current task; new requests enter change control.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
