---
name: first-article
description: Use before mass-generating modules, migrations or similar changes.
---
# First article inspection for code templates

## Trigger
Use before mass-generating modules, migrations or similar changes.

## Operating rule
Build one representative instance, test edge cases and review outputs before scaling. If first article fails, do not propagate template. Record approved reference hash.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
