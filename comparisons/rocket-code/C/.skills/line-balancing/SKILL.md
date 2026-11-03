---
name: line-balancing
description: Use when optimizing agent throughput.
---
# Line balancing and bottleneck management

## Trigger
Use when optimizing agent throughput.

## Operating rule
Measure wall time, tool time, token use, retries and merge conflicts by stage. Optimize the measured bottleneck. Avoid speculative agent parallelism; keep quality gates unchanged.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
