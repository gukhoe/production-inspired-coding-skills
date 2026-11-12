---
name: containment
description: Use when a defect may affect users, data or downstream artifacts and its spread must be bounded before a permanent correction.
metadata:
  version: "2.0"
---
# Containment

1. Identify affected versions, users and data. Preserve a last-known-good reference and isolate the development change.
2. Distinguish development isolation from operational containment. Use only authorized operational actions and record their actual outcome.
3. Complete when spread is demonstrably bounded or explicitly unknown, with recovery/resumption conditions and adjacent users checked.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
