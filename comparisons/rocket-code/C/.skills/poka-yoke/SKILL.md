---
name: poka-yoke
description: Use when preventing common coding and release errors.
---
# Mistake-proofing software changes

## Trigger
Use when preventing common coding and release errors.

## Operating rule
Prefer enforced schema, type checks, allowlists, permissions and CI guards over prose warnings. Guard destructive operations and prevent test weakening. Require explicit authorization for risky irreversible changes.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
