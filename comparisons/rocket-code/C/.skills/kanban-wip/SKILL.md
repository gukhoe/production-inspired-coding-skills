---
name: kanban-wip
description: Use when multiple agents edit or review a repository.
---
# Kanban WIP limits for parallel agents

## Trigger
Use when multiple agents edit or review a repository.

## Operating rule
Limit active edits per shared module to one owner. Parallelize independent files only. Reserve integration ownership and queue competing edits. Measure queue time rather than adding agents reflexively.

## Evidence and termination
Use existing executable tooling first. Store full logs on disk; send only exit status, failing assertion, and at most 3 unique error signatures to the model. Report PASS only for executed checks, BLOCKED for failed mandatory checks, UNVERIFIED for unavailable checks. Stop at the defined gate; do not iterate without new evidence.
