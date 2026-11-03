# SKILL.md Update Plan

Status: ready for implementation; no behavioral changes have been applied to the original 16 `SKILL.md` files.

The goal is to turn manufacturing production and quality practices into executable software development procedures. Success is a useful change in coding behavior, not the amount of manufacturing terminology used.

## Implementation sequence

1. Preserve the original skills and attachments as the repository baseline.
2. Correct the evaluator's false passes and inaccurate result description in a separate v2 revision. Preserve the original records.
3. Make focused improvements to the connection between SOR, PFMEA, Poka-Yoke, Control Plan, and MSA.
4. Compare actual implementations and execution results on the same tasks before and after skill changes. Treat code and documentation length as descriptive measurements only.
5. Apply changes with demonstrated behavioral benefits first. Improve the remaining skills when relevant validation cases are available.

## Changes prepared for all 16 skills

| Skill | Observed concern | Focused change | Behavior to verify |
|---|---|---|---|
| `sor-requirements` | “Never infer unstated behavior” can block minor decisions | Clarify consequential policies; document reasonable low-risk assumptions and proceed; connect key contracts to tests | Units, precision, and ranges match the implementation without unnecessary questions |
| `pfmea-risk` | A documented risk may lack an implemented control | Link each important risk to its control location, check, and observed result; treat five risks as prioritization guidance | Important failure modes appear in code controls and tests |
| `poka-yoke` | Lists preventive mechanisms without sufficiently checking their effectiveness | Use meaningful checks that expose the failure before the control and confirm prevention afterward | Preserve valid inputs while preventing the relevant error |
| `control-plan` | “Never rerun” can conflict with MSA reproduction checks | Define invalidation and rerun conditions for source, dependencies, configuration, inputs, environment, external state, and flakiness investigation | Distinguish redundant checks from necessary revalidation |
| `msa-test-reliability` | Triggers emphasize flaky tests and reviewer disagreement, overlooking false passes | Include incorrect oracles and tests that cannot distinguish always-successful or always-failing implementations | An always-raising implementation is not treated as a sound implementation |
| `standard-work` | Index and body have different activation scopes; acceptance criteria may be too weak | Finish against task-appropriate acceptance criteria and required checks; avoid ritual on every task | Keep small work short without omitting necessary verification |
| `eight-d-root-cause` | Fixed limits of three attempts or two identical signatures can stop productive diagnosis | Stop repeated attempts with the same hypothesis and conditions when no progress occurs; change approach when new evidence appears | Reproduce the cause, check the regression, and distinguish infrastructure failures |
| `andon-jidoka` | “Unknown environment” can cause an overly broad stop | Stop affected mutations or promotion while continuing read-only investigation and isolated reproduction; specify resumption conditions | Halt risky actions while continuing safe diagnosis |
| `containment` | Creating a branch may be mistaken for containing operational impact | Distinguish development isolation from production containment; record scope and evidence | Claim only the containment actually demonstrated |
| `ecn-change-control` | Can trigger repeat approval or unsolicited external issue creation | Respect existing user authorization; report out-of-scope findings and create external issues only when requested | Track impact without redundant approvals or unauthorized external changes |
| `first-article` | One sample may be assumed to cover every variant | Check representative types and important variations before scaling; link the reference hash | Prevent defects in a template from propagating widely |
| `apqp-stage-gates` | Gate overhead may exceed task complexity | Apply only risk-appropriate gates with clear evidence and promotion conditions | Avoid excessive ceremony for small changes |
| `ppap-release-evidence` | Collecting documents may be mistaken for operational readiness | Connect requirements, checks, artifact versions, and unknowns; distinguish evidence from approval authority | Do not mark untested deployment or recovery behavior as passing |
| `kanban-wip` | Parallelism may become a goal in itself | Apply only when multiple agents are needed and authorized; record file ownership and integration responsibility | Reduce conflicts and verify the integrated result |
| `line-balancing` | Unavailable metrics may be filled with estimates | Distinguish measurements from unavailable values; track errors and regressions alongside time | Do not weaken quality checks to shorten elapsed time |
| `spc-quality-trends` | Mixed tasks, models, and environments may create misleading trends | Record comparable conditions and change points; separate incompatible observations | Do not infer statistical control from one success or an unqualified average |

## Shared wording and packaging

- Consider shortening the repeated “Evidence and termination” paragraph according to each skill's role. Preserve independent usability; do not automatically move shared text into a mandatory external file.
- Treat “at most 3 unique error signatures” as a default summary length. Allow reading additional raw logs when diagnosis requires them.
- Define PASS, FAIL, BLOCKED, and UNVERIFIED at the check level. A failing check and an unavailable tool are different states.
- Validate the relationship between `name`, `description`, and folder name. Descriptions should distinguish actual activation conditions. Keep `SKILL.md` as the entrypoint.
- Link optional references at the branch that needs them. Avoid loading the entire skill collection for every task.
- Decide installation paths, licensing, and release metadata according to the user's distribution plan. This baseline does not introduce an inferred license or global installation.

## Acceptance criteria for future updates

Evaluate against the actual request and agreed contract. Do not retroactively require an unrequested GUI, database, API, visual style, or documentation format.

- **Request fulfillment:** Does the code execute and produce the requested result?
- **Defect detection:** Do the checks detect the important failures?
- **Prevention:** Does the control avoid unnecessarily restricting valid inputs?
- **Evidence consistency:** Do completion claims match actual logs and artifact versions?
- **Proportionality:** Is the added process appropriate to the observed risk and change size?
- **Cost:** Are time, tool calls, revisions, and tokens measured rather than invented, with unavailable values left unavailable?

Implementing these changes and building the revised evaluator are subsequent tasks based on this plan.
