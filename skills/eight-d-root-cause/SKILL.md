---
name: eight-d-root-cause
description: Use for reproduced failures or repeated defects.
---
# 8D-lite evidence-based debugging

## Trigger
Use for reproduced failures or repeated defects.

## Operating rule
Fingerprint error from exception type, normalized stack and test id. Reproduce once, isolate root cause, make one focused fix and rerun impacted tests. Stop after three attempts or two identical no-progress signatures. Record regression test.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
