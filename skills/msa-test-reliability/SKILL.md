---
name: msa-test-reliability
description: Use when tests are flaky or AI reviewers disagree.
---
# Measurement system analysis for tests and AI review

## Trigger
Use when tests are flaky or AI reviewers disagree.

## Operating rule
Repeat deterministic tests in controlled environment, record flake rate and false-pass/false-fail on labeled fixtures. Distinguish environment failures from product failures. Never majority-vote away an actual failing test.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
