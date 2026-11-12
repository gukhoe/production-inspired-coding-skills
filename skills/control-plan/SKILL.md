---
name: control-plan
description: Use when selecting or reusing verification after source, dependency, configuration or environment changes; also for short recurring CI checks.
metadata:
  version: "2.0"
---
# Control Plan

1. Map risk to check, oracle, command, frequency, owner and failure response. Use targeted checks for low impact and interface/adverse/recovery checks for higher impact.
2. Reuse a result only with matching source, dependencies, configuration, inputs, environment and relevant external state. Rerun when identity changes, a prior failure is corrected or a flakiness/MSA hypothesis requires it.
3. For layered process audits, separate quick per-change sentinels from deeper periodic checks. Complete when mandatory checks have an observed result or an explicit blocked/unverified reason.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
