# Standard result form: template 1.0

The fixed output is an engine artifact, not a new document improvised by an AI on each run. [Blank form](../examples/software-audit/blank-report.md), [blank JSON](../examples/software-audit/blank-report.json), and [JSON Schema](../schemas/audit-report.schema.json) describe the same contract.

| Section | Stable result fields |
|---|---|
| Identity | Template, criterion standard and schema versions; scope; source revision |
| Summary | Effective outcome and scope limitations |
| Scores | Overall and per-stage observed score, weighted coverage, documented achievement lower bound, scored/unknown/excluded counts |
| Criterion summary | Fixed criterion ID, stage, title, status and weakest-checkpoint score |
| 72 checkpoint rows | ID, question, effective status/score, evidence IDs, reviewer/rationale, finding, improvement, owner, due, evidence issues |
| Stage transition | Gate ID, source/receiving stage, producer/receiver, input/output evidence, review and blockers |
| Investigation | Case/mode/targets, each problem-solving step and effective result |
| Interface review | Boundary/aspect, failure scenario, evidence, status/score, finding, improvement and ownership |
| Risk/action | Severity, impact, targets, owner/due, corrective action and effective verification/closure |
| Evidence register | Evidence ID, relative file, locator, kind, source identity and SHA-256 validity |

Rules:

- Report headings, questions, rubric and engine messages are English. AI-authored scope, rationale, findings, improvements and summaries must also be English. The renderer does not translate supplied narrative; prepare English assessments before evaluation. Preserve exact evidence paths, identifiers, hashes and original quotations, with English explanations for non-English quotations.
- Preserve the defined questionnaire order. Omitted inputs produce visible unverified rows; no row is removed to improve results.
- Keep claimed and effective values in JSON. Invalidated evidence can downgrade a claimed score; the report shows why.
- Never replace unknown with zero, or an empty denominator with 100%. Keep justified exclusions visible.
- Scores cannot override gate blockers or high-impact risks.
- Narrative may explain findings but cannot change the engine's values. Changes to evidence or judgment require a new evaluated manifest/report.
- Keep past reports immutable and identify source/standard/template versions before comparing runs. CLI refuses report overwrite.

Generate the blank forms and questionnaire with `python scripts/export_audit_templates.py`. Run the populated standalone example with:

```sh
python examples/software-audit/run_standalone_demo.py --out .process-audit/example-001
```

The toy target deliberately contains a duplicate-event defect. The example verifies that the target fails as expected and the audit retains a gap/unknowns. It is not a production quality assessment. Re-running requires a new output directory.

Read the [populated English example report](../examples/software-audit/sample-report.md), generated from this demo. Its 50% observed score covers only six scored checkpoints; 66 remain unverified. Read the 9.09% weighted coverage and 4.55% documented achievement lower bound alongside it. Coverage means sufficient evidence to assign a score, including design/static evidence; it is not test execution coverage or a reliability probability.
