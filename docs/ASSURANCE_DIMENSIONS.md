# Separate review, execution and risk closure

Template 1.1 adds `scorecard.dimensions`, policy `assurance-dimensions/1.0`.
The three indicators must be shown together and must never be averaged into a
single safety score. Good documentation cannot establish runtime behavior or close a risk.

| Indicator | Included evidence | Meaning of 100 | Unknown or empty scope |
|---|---|---|---|
| Documentation / design review | The 45 inspection checkpoints and interface contract reviews | All applicable inspection conditions are supported by reviewed evidence | Unknowns earn no points; no applicable items is N/A |
| Execution verification | The 27 behavioral checkpoints and interface failure/recovery/verification/observability aspects | All applicable behavioral conditions are assessed at 4 with linked successful current execution | Without a valid execution record, retain unknown; no applicable items is N/A |
| Verified risk closure | Registered risks with effective closure and supported successful verification | All registered risks have verified closure | No registered risks is N/A, never 100 |

These are scoped reviewer assessments, not measured reliability, security assurance,
failure probability, native/live acceptance or proof that the reviewer chose adequate tests.
A successful execution record still needs checkpoint-specific review and rationale.
Local witness receipts are not signed identity attestations. A high suite pass rate is
not the execution score: scenarios, unknowns and criterion importance matter.

## Calculations

For documentation and execution, use the existing criterion priorities distributed
over their questions. Normalize applicable items within each area to its existing
area budget, then normalize over represented areas within that indicator. An area
with no questions for the selected indicator is N/A. Therefore the two indicators
have different populations and must not be added together. JSON retains each input
item, reviewed score, effective indicator score, evidence IDs and execution flags.

Positive execution credit requires a validated linked successful execution record.
Static evidence at score 1 or 2 earns no execution credit. If a valid failed run is
the only execution evidence, the indicator earns zero and counts that reviewed
failure as covered; malformed, stale or unreviewed evidence remains unknown.
Coverage describes evidence sufficient for a reviewed execution result, not code coverage.
Unknowns contribute zero earned points without being reclassified as failures.

Risk closure is `100 × verified-closed severity weight / registered severity weight`.
Policy weights are critical 4, high 3, medium 2, low 1; they are priorities, not
probabilities. Open, proposed and implemented-but-unverified actions earn no closure
credit. Retain prior risks in the register; deleting a finding is not remediation.
Changing the register or severity changes the denominator and must be disclosed.
Per-area membership follows explicit criterion/boundary targets and can overlap;
the overall calculation counts each risk once. N/A in an area means no registered
risk targeted there, not absence of risk. Overall 0% closure means none of the
registered risks is verified closed, not that the software is 0% safe.

## Compatibility and comparison

The legacy mixed score fields and their values remain available for older consumers;
they are labeled as comparison-only in Markdown. The dashboard leads with execution,
closure and documentation independently and offers an area indicator selector.
Report template 1.0 remains readable. CLI, MCP and HTML use the same evaluated data.
The criteria catalog retains `primary_metric` for older consumers with
`primary_metric_deprecated: true`; new consumers use `primary_indicators`.

Historical projections use the fixed standard-0.3.0 checkpoint classification and
the old effective scores/evidence results. Such a projection does not revalidate
old files, authenticate execution or re-review old questionnaire judgments. State
whether source, scope, criteria, evidence or the risk register changed. Preserve
original reports and write projected comparisons separately.

## Change and verification record

Requested scope: separate document review from demonstrated behavior and risk closure.
Affected contracts: additive scorecard dimensions, report template 1.1, JSON Schema,
Markdown, dashboard and generated blank forms. No manifest migration is required.
Rollback: restore the prior renderer/evaluator; legacy composite fields are unchanged.
Regression checks cover document-only inflation, partial static evidence, failed and
malformed runs, invalidated closure, empty registers, severity weighting and membership.
Validate local example reports and dashboard rendering after regenerating forms.
