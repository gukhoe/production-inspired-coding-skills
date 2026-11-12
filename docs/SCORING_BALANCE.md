# Software scoring balance and evidence requirements

Template 1.1 leads with [documentation/design review, execution verification and verified risk closure](ASSURANCE_DIMENSIONS.md). The mixed score described below is retained for historical comparison, not presented as software stability.

Standard **0.3.0** uses scoring policy **balanced-area/1.0**. The 24 criteria and
72 checkpoint IDs remain available; five criteria have clarified question wording.
The 0–4 scale remains, with separate inspection and execution anchors. These are
explicit software assurance priorities, not empirically calibrated incident
probabilities or a certification standard.

## Area budgets

The base budget totals 100. An area's importance no longer grows just because it
has more recorded boundaries or questions. Within an area, the existing criterion
priorities (2 or 3) allocate its budget. Each criterion distributes its priority
over its checkpoints. Interface reviews share one area budget.

| Area | Budget % | Reason for allocation |
|---|---|---|
| Requirements | 5 | Define observable outcomes and unacceptable states |
| Design | 7 | Establish contracts, ownership and state constraints |
| Dependencies | 4 | Control external assumptions and changes |
| Implementation | 12 | Protect authorization, data and state at actual boundaries |
| Verification | 12 | Establish discriminating oracles and adverse-path evidence |
| Release | 7 | Verify artifacts, compatibility, migration and rollback |
| Operations | 7 | Detect failures and recover without uncontrolled effects |
| Change | 4 | Trace affected consumers and adjacent regressions |
| Risk | 6 | Preserve credible failure modes and unresolved impact |
| Improvement | 6 | Own corrective actions and demonstrate effectiveness |
| Scope | 4 | Establish what was and was not examined |
| Prevention | 10 | Prevent harmful transitions and contain failures |
| Handoff | 4 | Review entry/exit evidence and receiving-party acceptance |
| Diagnosis | 6 | Reproduce failures and distinguish competing causes |
| Interfaces | 6 | Inspect communication boundaries without letting graph size dominate |

The allocation deliberately emphasizes implementation, verification and prevention.
It does not imply that a low-budget area's severe defect is acceptable: open
high/critical risks, known gaps, incomplete evidence and stage blockers remain
separate from numeric averages. Weights cannot override them.

## Calculation and scope disclosure

For a criterion, each checkpoint's raw weight is its criterion priority divided
by the number of checkpoints. Within an area, scale applicable raw weights so
their total equals that area's budget. Boundary aspects share the interface
budget. Use these effective weights in the existing formulas:

- **Documented score**: earned points divided by the maximum for all applicable
  items, multiplied by 100. This is the documented achievement lower bound and is
  the primary diagram/summary score. Unknown evidence contributes no earned points
  but is not classified as a defect.
- **Scorable coverage**: maximum points of scored items divided by the maximum
  for all applicable items, multiplied by 100.
- **Observed score**: earned points divided by the maximum for scored items only,
  multiplied by 100. This is a secondary, conditional measure. It can be 100 when
  very little was reviewed; read coverage and documented score beside it.

The detailed report lists base budget, effective budget and earned contribution
for every area. An area whose questions are all validly not applicable is marked
`excluded`. An area with no records, such as interfaces in a declared single-unit
scope, is marked `not_represented`; absence is not proof that no interface exists.
Remaining applicable area budgets are normalized. Review the process inventory,
scope justification and excluded budget before comparing systems. Adding a real
new area changes the declared scope; adding equivalent boundaries inside an
existing area cannot expand that area's total importance.

All-excluded/empty scoring denominators remain null. Unknown questions still
count toward their area's denominator. Source graph nodes and edges never add
points by themselves. Duplicate evidence does not create additional assurance.

## Match the evidence to the question

The [complete questionnaire](AUDIT_QUESTIONNAIRE.md) lists evidence mode and
score-3/score-4 anchors for every checkpoint:

- **45 inspection checkpoints** examine current requirements, contracts, source,
  controls and records. A high score requires relevant cross-checks against source,
  referenced contracts or receiving-party evidence. A document's existence or title
  is insufficient. These questions do not require an unrelated command to run.
- **27 execution checkpoints** make behavioral claims. Scores 3/4 require valid
  successful execution evidence with a relevant scenario and oracle. Source-only
  inspection cannot establish rejection, isolation, recovery or recurrence behavior.

For example, PRE-01.1 identifies a harmful transition and PRE-01.2 inspects the
guard and bypass paths; PRE-01.3 challenges the actual guard with adverse input.
The first two use inspection evidence; the third requires execution. CHG-01.3
now explicitly requires execution for its neighboring-workflow claim. Each
checkpoint is scored on its own acceptance conditions, not on whether every
sibling checkpoint passed. Criterion/gate readiness still follows the weakest
applicable checkpoint, preserving failures and unknowns.

The engine validates evidence records and required modes; the reviewer must judge
semantic adequacy. Receipt consistency, a convincing rationale or a high score is
not authenticated identity, truthful testimony or a verified oracle by itself.

## Compatibility and calibration

Manifests explicitly declaring standard **0.2.0** retain its original questions,
criterion-wide execution requirements and checkpoint-weight scoring policy.
Assurance policy 1.0 still applies its accountability/evidence integrity controls.
New manifests default to **0.3.0**. To migrate, retain the original manifest,
reassess changed question wording and evidence modes against the current snapshot,
then create a new revision of the review. Do not merely relabel an old score or
compare scores across standards as a quality trend.

Regression tests check area-size invariance, criterion question-count invariance,
priority ordering, contribution arithmetic, unknowns, exclusions, execution
requirements and old-standard behavior. These establish calculation properties,
not universal optimal weights. Future calibration needs labeled normal/faulted
systems across domains, blinded reviewers, false-pass/false-fail measurements and
sensitivity analysis. Change budgets through a reviewed, versioned policy; do not
tune them after seeing a target project's desired score.
