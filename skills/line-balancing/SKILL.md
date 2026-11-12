---
name: line-balancing
description: Use for measured development or verification bottlenecks across stages when throughput needs improvement without weakening checks.
metadata:
  version: "2.0"
---
# Line Balancing

1. Measure stage wall time, tool time, retries and merge conflicts; record token use only if available. Separate measured values from estimates and unknowns.
2. Improve the demonstrated bottleneck using bounded independent work where appropriate. Keep correctness and failure containment gates intact.
3. Compare comparable before/after conditions including escaped defects and regressions. Complete when benefit is measured or the hypothesis is rejected.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
