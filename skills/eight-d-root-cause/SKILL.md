---
name: eight-d-root-cause
description: Use for reproduced or recurring failures to separate occurrence cause from the reason existing checks let the defect escape.
metadata:
  version: "2.0"
---
# Eight D Root Cause

1. D1-D2: identify the owner and expected versus observed behavior. D3: contain the affected scope with evidence; distinguish a development branch from operational containment.
2. D4: reproduce the failure and test competing causes. Analyze the escape point separately: which control should have caught it, and why did that control fail?
3. D5-D6: select a focused correction, replay the original failure and verify an adjacent valid path. Stop repeating the same hypothesis under unchanged conditions; continue when new evidence changes the experiment.
4. D7: apply recurrence prevention to the system and inspect analogous sites (Yokoten). D8: close only with effectiveness evidence, ownership and residual risks recorded.

## Output and evidence

Use [the blank output form](assets/output-template.md) for this workflow and [the portable record](assets/review-record.json) when transferring it to the auditor. Fill only observed facts; link raw evidence rather than copying logs into the conversation. A completed form is a document, not execution evidence or an automatic supported score.
