---
name: poka-yoke
description: Use when an invalid input, unsafe mutation or recurring operator error can be prevented at the actual code boundary.
metadata:
  version: "2.0"
---
# Poka Yoke

1. Identify the harmful action and last safe admission point; prefer schema, type, authorization, state or idempotency guards over warnings.
2. Challenge the real boundary with a known-bad sentinel (red rabbit) and an adjacent known-good input. Show the guard rejects the former while preserving the latter.
3. Preserve existing authorization and scope. Complete when the original failure is prevented and the control cannot be bypassed through an equivalent route.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
