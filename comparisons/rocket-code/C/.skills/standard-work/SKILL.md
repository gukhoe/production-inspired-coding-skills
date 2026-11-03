---
name: standard-work
description: Use to standardize recurring development tasks.
---
# Standard work for coding agents

## Trigger
Use to standardize recurring development tasks.

## Operating rule
Read task and constraints, inspect only relevant files, change minimally, run targeted checks, report concise evidence. Avoid verbose self-review and duplicate agents. Stop once acceptance criteria pass.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
