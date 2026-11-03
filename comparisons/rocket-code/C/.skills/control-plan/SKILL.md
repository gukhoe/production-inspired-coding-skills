---
name: control-plan
description: Use when choosing which checks to run after code changes.
---
# Risk-based verification control plan

## Trigger
Use when choosing which checks to run after code changes.

## Operating rule
LOW: diff and targeted checks; MEDIUM: unit plus impacted regression; HIGH: integration, negative-path and recovery tests. Capture command, expected result, frequency and failure response. Never rerun unchanged passing checks without an invalidation reason.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
