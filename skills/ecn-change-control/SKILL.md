---
name: ecn-change-control
description: Use for consequential interface, dependency, model, toolchain or behavior changes that require impact and compatibility review.
metadata:
  version: "2.0"
---
# Ecn Change Control

1. Record requested scope, existing authorization, affected producers/consumers and rollback or repair constraints. Separate consequential scope changes from routine reversible choices.
2. Apply 4M change review as model/reviewer, tooling/runtime, dependencies/data and method/prompt. State which category changed and which prior evidence is invalidated.
3. Trace downstream impact and authorized regression checks. Report out-of-scope findings without creating external issues or messages unless requested. Complete when affected contracts and residual risks are documented.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
