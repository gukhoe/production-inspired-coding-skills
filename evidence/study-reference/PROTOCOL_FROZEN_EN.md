# Limited native-session pilot: protocol v1 — English edition

The original freeze is recorded in `freeze_manifest.json`. The original Korean protocol is retained in [historical-originals.zip](../../sources/historical-originals.zip). This translation is for readers and is not the frozen input. File references below describe the original full study package; this repository contains only selected evidence.

## Design and execution

Begin with 10 tasks × A/B/C × one repeat: 30 balanced runs. Pre-generate a 90-run plan; execute repeats 2/3 using the same design if time/tool capacity permits after the first block. Do not add runs selectively by group. Randomize task and within-block group order using Python Random with seed 20261102. Each session uses `fork_turns=none`, inherited default model/reasoning settings and no per-session overrides. Record the exact model revision as unknown if unavailable.

Start up to six sessions (two tasks × three groups) in the same batch using `plan/run_plan_30.json` dispatch order. Record start offsets and shared-resource contention; causal development-time comparisons are limited. Each session has a distinct name/folder. Shared filesystem access cannot be technically isolated: instructions prohibit reading other runs/evaluators, but this is not enforced isolation.

Keep user requests unchanged in `plan/prompts`. Common administration specifies the folder, maximum 300 seconds, maximum 10 revisions and logging. It does not impose an output API, JSON, function name or extra business rules. Limits are instructions, not guaranteed platform termination. Provider token limits and actual usage remain null if unavailable; strict equal-token budgeting is unverified.

Wrap executions with `runlog.py` to preserve stdout/stderr, command, exit status, elapsed time and source hashes. The wrapper is experimental administration, not participant code. Participants choose their own tests; do not arbitrarily strengthen or weaken strategies by treatment. Execution logs cannot establish all edit-tool calls.

## Treatments

- A: no additional skill or AGENTS.md. Common platform/development and measurement instructions still apply; this is not instruction-free chat.
- B: the public `obra/superpowers` verification-before-completion snapshot, with full text, MIT license, provenance and local SHA-256. Upstream commit is unknown. Findings apply to this skill, not all engineering skills.
- C: supplied skill index and 16 original skills, loaded selectively for relevance. Do not supply the B skill.

Install no external programs, hooks or credentials beyond the assigned text.

## Evaluation

Primary: semantic correctness of stdout on the supplied input, one case per task. Input interface, formatting and callable structure are not requirements. Secondary: four normal/boundary/invariant cases per task (40 total), when existing interfaces or nonsemantic input adapters permit them. Adapters may pass data and normalize names/units only; they may not alter calculation or validation logic. An unconnectable artifact is UNASSESSABLE, not wrong. Do not merge primary and secondary layers into a single headline accuracy.

Diagnostics: two unspecified-policy cases per task (20 total), such as negative inputs, zero denominators, ties, early completion and overpayment. Record behavior/errors without inventing the correct policy; exclude these from correctness denominators.

| Task | Required normalized result |
|---|---|
| T01 | Annual supplier costs and unique lowest-cost supplier |
| T02 | Final inventory |
| T03 | Supply minus demand; shortage is negative, surplus positive |
| T04 | Unit manufacturing cost; total cost optional |
| T05 | Defect ratio and good quantity; divide explicit percentages by 100 |
| T06 | Unpaid balance |
| T07 | Elapsed days for on/after-plan cases; early completion diagnostic |
| T08 | Weighted scores and descending ranking; inputs are price scores, not prices |
| T09 | OEE ratio/percentage; component ratios optional |
| T10 | BOM total cost for one product |

Link observations to execution logs from frozen code. Human semantic normalization means evaluation is not fully automatic. Preserve output strings and judgment. Missing mandatory output fails; uninterpretable output is UNASSESSABLE. `oracle.py` uses Decimal/date arithmetic and is separately tested with hand-calculated golden values and deliberately incorrect observation fixtures. These are evaluator checks, not participant results. Fixed `score.py` tolerances accept two-decimal currency/score and rounded percentages.

## Measurement and interpretation

- Tokens: provider usage only; otherwise null. Do not substitute character counts or guesses.
- Development time: recorded initialization-to-completion wall time. Queue, inference and individual tool time cannot be fully separated; call it observed latency.
- Revisions: changed Python snapshots between successive logged executions after the first run. Initial authoring excluded; test-file edits included. This is not necessarily production-code repair.
- Tests: `kind=test` calls, separated from examples/syntax checks. Unlogged verification is self-reported or unknown.
- Repeated verification: repeat success with the same command/source hash. External state, inputs or environment changes may be unrecorded, so repetition alone does not establish waste. Consider skill-required final checks in context.
- Retain failures, interruptions, timeouts and infrastructure errors; distinguish infrastructure from development errors.
- Report means, medians, ranges, paired task differences and task-level bootstrap 95% intervals. Acknowledge the initial 10-task, one-repeat scope. Equal accuracy and missing tokens cannot support accuracy-gain or token-saving conclusions.

Do not give participants the evaluator, answers or other groups' results, or request corrections after evaluation.
