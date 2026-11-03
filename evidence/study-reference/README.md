# Manufacturing AI Coding Skill study — 90 attempted runs

Start with SUMMARY_KO.md (Korean) and RUN_DETAILS_KO.md. This is a limited-control native-session experiment, not a fully isolated causal benchmark. There are 90 final artifacts, but only 87 completion records within the instructed 300-second budget. Exact model usage is unavailable.

## Data layout

- results.csv: exact original RESULT_SCHEMA.csv columns, one row per attempted run. Blank token/call fields mean unavailable, never zero. tests_passed/tests_total describe recovered final artifact correctness; status separately identifies late recovery.
- results.json / group_summary.json: raw events, semantic observations, independent scores, timing and budget compliance, diagnostic results, comparison summaries and limitations.
- runs/rN_TXX_G: participant code, optional tests/input files, request.txt, treatment files, native timing records, runlog events and submission manifest. The reported canonical native task handle is /root/rN_txx_g; this is not an authenticated backend session ID. The platform did not expose backend model/session IDs or complete model traces.
- evaluator: pre-frozen oracle, 70 test cases and scoring rules. Primary output is semantic; no callable or output API was required of participants.
- evaluation: 630 independent executions (90 primary + 360 secondary + 180 descriptive diagnostics), actual outputs and exit codes, adapter requests and scoring.
- observations/adapters.json: transparent mappings to existing participant functions. harness/adapter_worker.py performs input passing and output representation normalization only.
- plan: pre-generated 90-run randomized sequence (seed 20261102), original user prompt files, identical complete administrative template, and disclosed administrative-delivery deviation for repeats 2/3.
- b_skill: one real public engineering Skill snapshot and MIT license, pinned by SHA256. Source URL and incomplete upstream-version provenance are in source.json.
- supplied_text: exact supplied study text (20 files) received from the parent after original ZIP extraction. Original ZIPs are not present; parent-reported archive hashes and local text hashes are distinguished.
- freeze_manifest.json: protocol, oracle, case, prompt and treatment hashes frozen before any participant code. Later adapters/reporters are not falsely represented as pre-frozen.
- observations/interruption_r2_T04.json: native-session inactivity and administrative followup record. r2_T04_A/B/C exceeded the original budget and remain flagged.
- history: this experiment's earlier preflight and 30-run snapshots, not current final results and not prior-chat benchmark code.
- preflight: recorded CLI/network/namespace failures. Existing unrelated purchasing repository was not modified.

## Recheck saved artifacts (Python 3.12.14, standard library only)

Run from the extracted archive directory:

```sh
python3 harness/audit.py
python3 -m unittest discover -s evaluator -p test_evaluator.py -v
```

To rerun participant programs and the fixed evaluator without replacing original evidence, make a separate copy of the extracted directory, rename that copy's `evaluation` directory to `evaluation_recorded`, then run:

```sh
python3 harness/evaluate.py
python3 harness/finalize_primary.py
```

This executes saved code, not new AI generations. The evaluator checks frozen hashes, runs each original entry command, and calls existing input functions through documented adapters. All observed submissions exposed usable functions; absence of such a surface would be UNASSESSABLE for secondary tests, not a correctness failure. Tests for unstated policies are diagnostic and excluded from scores.

To rebuild final statistical output from the saved observations, use:

```sh
python3 harness/aggregate_final.py
python3 harness/render_report.py
```

`harness/report.py` is the historical 30-run report generator and must not be used on the 90-run dataset. `harness/prepare.py` reproduces the predeclared cases and randomized plan; do not use it to silently overwrite a frozen study with changed inputs. `harness/collect.py` and `snapshot.py` refer to the original live participant roots and are orchestration records, not needed for portable artifact re-evaluation.

## New AI-generation replication

Use an authorized native fresh session for every plan row, with no inherited turns, identical model/effort/tool/budget settings, only that row's user prompt and assigned treatment, and no evaluator or other-run access. A receives no additional Skill. B receives the pinned verification-before-completion snapshot. C gets the index and selectively reads relevant supplied Skills. Do not reuse any runs/ code as participant input.

The current platform could not enforce read isolation or expose exact model usage. A future strict replication needs those capabilities. This package does not create credentials, invoke a paid external API, or claim those controls were achieved. Do not interpret extra repeats as fixing missing controls.

## Measurement definitions

Wall time is the real first recorded action to end-marker interval, including skill/tool/instrumentation work and interruptions; queue/pre-first-action inference is absent. Timings are not pure model generation time. Revisions are changed Python snapshots between logged executions; the single observed change was addition of a test file, not a production bug fix. Test commands are audited from logs, with explicit inline assertions separated from unittest case counts and administrative checks. Exact tokens/cached tokens/model calls/cost remain null. All 90 per-run original metrics and raw logs remain available.

## Provenance audit addendum

See native_evidence/README_KO.md and provenance_manifest.json. The 90 creation-response field records are retrospective transcriptions from coordinator conversation continuity, not original platform transcript exports. A fresh list_agents call in this audit exposed six completed handles only. Actual model ID/version/effort, backend session UUIDs, token usage and full participant tool traces remain unavailable. skills_read is self-reported. Shared filesystem access was not enforceably isolated. These artifacts establish recorded code and subprocess outcomes, not independently authenticated clean session isolation or model identity. No participant or evaluator was rerun for this addendum.
