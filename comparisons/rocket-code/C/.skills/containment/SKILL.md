---
name: containment
description: Use when a defect might affect multiple modules or data.
---
# Containment and quarantine of failing changes

## Trigger
Use when a defect might affect multiple modules or data.

## Operating rule
Isolate the change in a branch or sandbox, preserve last-known-good state, prevent promotion, and identify affected versions. Never claim production containment without deployment evidence.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
