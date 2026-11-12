---
name: pfmea-risk
description: Use when changing state, persistence, security boundaries or business rules to connect credible failure modes to preventive controls and tests.
metadata:
  version: "2.0"
---
# Pfmea Risk

1. Prioritize credible failure modes by effect and exposure; five is a starting shortlist, not a cap on severe risks. Separate causes from detection gaps.
2. Record severity, occurrence and detection only against an explicit rubric with evidence; unknown stays unknown. Prefer action priority over multiplying ordinal scores. Use an authorized AP table if supplied; otherwise label high/medium/low as a project-specific software priority, never an official AP result.
3. Trace each important mode to its actual prevention location, detection check, executed observation and owner. Severe effects remain visible regardless of aggregate score. Complete when each prioritized mode has a control or an explicitly open action.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
