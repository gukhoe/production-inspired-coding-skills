# Portable skill v2 workflows

The 16 skill folders now provide revised procedures and independently usable blank
forms. Original supplied bytes remain in the source ZIP and provenance manifest;
historical experiment outcomes describe v1 only. `historical_sources.original_bytes`
reads that baseline for rechecks, while generated-file checks validate v2.

Edit `scripts/skill_catalog.py`, then run `python scripts/build_skills.py`. CI runs
`--check` to detect drift. The catalog is the maintenance source of truth; generated
skills carry all necessary instructions and local templates so installing one
complete folder does not require the rest of the repository.

Each skill provides `assets/output-template.md` and `assets/review-record.json`.
Keep copied user records outside tracked source. The portable record identifies
skill/version, source revision, author/reviewer, actual check status, observations,
evidence references, open actions and intended criterion targets. A populated form
is not an execution certificate or an automatic audit pass.

```sh
software-audit skill-evidence --repo /project --path reviews/risk.json --id SK1 --revision SNAPSHOT
```

This registers a populated `software-skill-record/1` as **document** evidence with
target hints. Blank forms, revision mismatches and unknown criterion targets are
rejected. Register raw execution separately and review the relevant checkpoints;
the bridge never converts a claimed PASS into supported.

## Substantive changes

PFMEA links effects, causes, control locations, discriminating tests and actions.
The [AIAG white paper](https://www.aiag.org/docs/default-source/quality-/new_aiag_vda_fmea_-whitepaper.pdf?sfvrsn=6923e9d_4)
describes the move from RPN to Action Priority. This project does not reproduce the
handbook's AP tables or infer ratings from missing occurrence data: use a supplied
authorized rubric, or label priorities explicitly as a software-specific policy.
Severe effects remain visible even when aggregate indicators are low.

8D separates occurrence cause from escape point, records temporary containment,
and includes system-level recurrence prevention and analogous-site review
(Yokoten). Poka-Yoke and first-article checks use good controls and deliberately bad
sentinels. Change control maps 4M to model/reviewer, tooling/runtime,
dependencies/data and method/prompt. Control plans can select short per-change and
deeper periodic layers without forcing a full audit on every edit.

MSA covers false passes, false failures, flakiness and reviewer agreement.
`scripts/check_audit_mutations.py` challenges actual validation code in a temporary
copy. `scripts/evaluate_reviewers.py` accepts JSON cases with unique `id`, truth
`PASS`/`FAIL`, and a `decisions` object keyed by reviewer. Decisions may be PASS,
FAIL or UNVERIFIED. It reports agreement, confusion counts, false-pass/false-fail
rates and Cohen kappa against labeled truth; undefined values remain null.

Example input shape, not an executed audit result:

```json
[{"id":"known-good","truth":"PASS","decisions":{"reviewer-A":"PASS"}},
 {"id":"known-bad","truth":"FAIL","decisions":{"reviewer-A":"UNVERIFIED"}}]
```

## Behavioral evaluation still required

Format checks prove portable structure and consistency, not improved AI coding.
Compare v1 and v2 on paired tasks with the same model, source snapshot, prompt,
budget and scoring oracle; include normal, adverse, recovery and sentinel cases.
Record actual model/prompt/toolchain changes and unavailable metrics. No new live
model comparison or coding-superiority claim is supplied by this update.

The software evidence-maturity rubric remains 0–4. A 0/4/6/8/10 automotive-style
profile and A/B/C categories would require a separately versioned, calibrated
mapping and migration study; they are not silently substituted for the software
rubric. Existing high-impact risks continue to block readiness independently of
averages.
