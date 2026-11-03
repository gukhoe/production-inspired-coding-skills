# Audit model, scoring and fixed report contract

Standard 0.2.0; manifest schema 2; report template 1.0. Original software assurance criteria translating manufacturing audit and quality practices into software review. External risk reports and graph tools are optional.

## Questionnaire

`criteria` / `audit_criteria` returns the authoritative complete questionnaire: 24 criteria with three independently assessed checkpoints each (72 total). IDs such as `REQ-01.1` are stable within the standard version. A criterion score is its lowest applicable checkpoint score, and remains unscored if any applicable checkpoint is unverified. A known gap remains visible even if another checkpoint is unknown.

Each criterion record has `id` and `checks`. Each checkpoint has `id`, `status`, `score`, `reviewer`, `rationale`, `finding`, `improvement`, `owner`, `due`, and `evidence`.

```json
{"id":"PRE-01","checks":[{"id":"PRE-01.3","status":"gap","score":0,"reviewer":"Reviewer role","rationale":"Duplicate event changes balance twice in the isolated run.","finding":"Duplicate protection is missing.","improvement":"Guard the mutation and replay the failure plus adjacent cases.","owner":"Maintainer","due":"2026-11-10","evidence":["E1"]}]}
```

Omitted criteria/checkpoints retain their report positions as unverified. Unknown/duplicate IDs, invalid score/status combinations and unsupported versions are input errors. Parent-level completion claims cannot override missing checkpoint evidence.

## Software evidence maturity scale

| Score | Status | Interpretation |
|---|---|---|
| 0 | gap | Current evidence demonstrates failure or a missing required control |
| 1 | partial | Intent/design exists; implementation/execution is not established |
| 2 | partial | Implemented with limited/static evidence; required scenarios incomplete |
| 3 | partial | Relevant normal scenarios verified; adverse/recovery/adjacent checks incomplete |
| 4 | supported | All applicable checkpoint requirements supported, including adverse/recurrence evidence where relevant |
| null | unverified | No defensible current score |
| null | not_applicable | Evidence-backed scope exclusion |

Every scored/excluded checkpoint needs reviewer, rationale and valid current evidence. Execution-sensitive checkpoints require successful execution for scores 3/4. The AI judges semantic adequacy; the engine verifies consistency and file identity, not truth or authenticity.

Initial weights: 3 for IMP-02, PRE-01, PRE-02, VER-02, REL-02, OPS-02 and CAP-02; 2 for other criteria and boundary aspects. Each checkpoint inherits its criterion weight. These are explicit policy weights, not calibrated incident probabilities.

- **Observed score** = 100 * weighted earned points / maximum points of scored applicable checkpoints.
- **Weighted coverage** = 100 * maximum points of scored applicable checkpoints / maximum points of all applicable checkpoints.
- **Documented achievement lower bound** = 100 * weighted earned points / maximum points of all applicable checkpoints.

Unknowns lower coverage and contribute no earned points to the lower bound; this does not classify them as defects. Justified exclusions leave denominators and are counted separately. Empty denominators produce null, not 100%. High scores with low coverage do not establish whole-system assurance. High/critical open risks independently block applicable gates.

## Evidence and source identity

`evidence` prints a file SHA-256 record skeleton. Add precise locator and summary. Kinds: source, document, execution. Execution also needs command, integer exit code and timezone-qualified non-future timestamp. Failed runs can support gaps; only successful records support execution-sensitive scores 3/4. The tool never executes these commands.

Paths are repository-relative; absolute paths, parent traversal and symlink escape are rejected. Missing/modified files or changed revision invalidate use. `revision` is reviewer-supplied: commit plus dirty-tree fingerprint, or a content-manifest digest. The tool compares it; it does not independently hash the entire repository. Reusing one log for unrelated checks requires substantive justification.

## Boundaries and stage transitions

Processes have id, kind (delivery/runtime), owner, input, output, optional graph_nodes. Boundaries have id, source, target, failure_mode and reviews for contract, failure_handling, recovery, verification, observability. Reviews use the same score/evidence fields. Manual HTTP/file/native links are valid without a graph.

Five fixed gates cover requirements -> design -> implementation -> verification -> release -> operations. Each requires producer, receiver, input/output evidence and a reviewed handoff. Relevant criteria and high-impact risks produce blockers. Omitted gates stay blocked. Justified not-applicable gates stay visibly excluded. `evidence_ready` describes the record; it never performs a transition or authorizes release.

## Investigation and improvement

Preventive cases: failure_scenario, prevention_design, challenge_test, effectiveness.
Corrective cases: problem_definition, containment, reproduction, root_cause, correction, effectiveness.

Create a template with `investigation` / `audit_investigation`. Assess every step under the same evidence contract; designated behavioral steps require execution. A case stays open until all steps are supported. Unavailable reproduction stays open; no waiver silently completes it. Cases target criterion IDs or `boundary:<id>`. Confirmed gaps without linked investigations appear in scope issues.

Risks carry severity, failure_mode, impact, targets, owner, action, due, status and verification. A closed claim without an owned action and supported execution verification stays effectively open. Dates are tracked as text; v1 does not schedule/enforce deadlines.

## Fixed result document

Template 1.0 uses this stable order:

1. Identity, scope, outcome, limitations, scope issues.
2. Overall/per-stage score, coverage, lower bound and counts.
3. Criterion summary, then all 72 checkpoint rows: ID, question, status, score, evidence IDs, reviewer/rationale, finding, improvement, owner, due, evidence issues.
4. Stage blockers, investigation step results, interface results and risks/action verification.
5. Optional graph evidence, review queue and evidence register (paths, locators, hashes).

JSON preserves the same structured details. Unknown cells remain visible. The same evaluated input renders deterministically. AI explanations may accompany the document but must not replace/rewrite its tables. Compare criterion, schema and template versions across audits.

Outcome: needs_attention for gaps/partial results/open risks; incomplete for other missing evidence, open investigations or blocked gates; reviewed_scope_supported only for the declared fully reviewed scope. Historical schema-1 records remain readable but receive a legacy flag and no current scoring/lifecycle-completion claim.
