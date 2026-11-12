---
name: andon-jidoka
description: Use when a critical check, data integrity or security boundary fails and affected mutation or promotion must stop pending diagnosis.
metadata:
  version: "2.0"
---
# Andon Jidoka

1. Identify the stop trigger and affected operation; stop its mutation or promotion while preserving evidence.
2. Continue read-only diagnosis and isolated reproduction where authorized. An unknown environment blocks environment-dependent claims, not all useful investigation.
3. Define observable resumption conditions and the responsible reviewer. Resume only after those conditions are met; unavailable checks remain UNVERIFIED.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
