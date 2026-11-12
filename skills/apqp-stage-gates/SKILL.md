---
name: apqp-stage-gates
description: Use for higher-risk multi-stage delivery where design, implementation, verification and release handoffs need explicit evidence and unresolved-exception review.
metadata:
  version: "2.0"
---
# Apqp Stage Gates

1. Select only risk-appropriate gates; trivial changes need no formal ceremony. Identify producer, receiver, inputs, outputs and acceptance at each chosen handoff.
2. Check current evidence separately from reviewer identity and acceptance. A missing reviewer is a review gap, not a corrupt artifact.
3. Prevent promotion when mandatory evidence or a high-impact mode remains unresolved. Complete when each applicable receiving owner has reviewed exceptions; evidence readiness does not itself authorize deployment.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
