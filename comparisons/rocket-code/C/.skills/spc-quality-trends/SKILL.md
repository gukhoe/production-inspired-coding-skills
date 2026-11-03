---
name: spc-quality-trends
description: Use when enough repeated build or defect observations exist.
---
# SPC-inspired development quality monitoring

## Trigger
Use when enough repeated build or defect observations exist.

## Operating rule
Track test failures, escaped defects, rerun counts and time to repair across comparable builds. Use run charts first; do not claim statistical control with insufficient or mixed data. Escalate sustained deterioration.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
