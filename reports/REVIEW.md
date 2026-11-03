# Review of the Supplied Analysis

Review date: November 2, 2026 (America/Chicago). Purpose: prepare improvements to coding skills that apply manufacturing production, quality, and verification processes to AI software development. The original skills remain unchanged.

## Assessment

The direction is useful. SOR can clarify requirements, PFMEA can identify credible failures, Poka-Yoke can prevent errors, and a Control Plan can select appropriate checks. These concepts can translate into observable development behavior. However, manufacturing terminology, additional documentation, or fewer test invocations alone do not demonstrate better code.

The improvement target is the connection between **requirements, risks, implemented controls, executed checks, and recorded evidence**. Apply only the relevant parts to small tasks, and avoid rewarding process length for its own sake.

## Distinguish the three evidence sets

| Evidence | What was actually compared | Supported interpretation |
|---|---|---|
| `benchmark/` in the original skill ZIP | Code that invokes the same tests five times versus once | A demonstration of fewer invocations; no measurement of models, tokens, or generated-code quality |
| `Manufacturing_ABC_Benchmark_v1.zip` | Three implementations with different validation rigor, authored in the same assistant session | Behavior of those implementations under those tests; not an isolated estimate of skill effects |
| The 90-artifact completeness review and referenced study | Final artifacts from 10 tasks × A/B/C × 3 repetitions, plus post-hoc static review | Observations on small tasks under limited controls; not production readiness or a general causal effect |

In the 90-run study, A had no additional skill, B had `verification-before-completion`, and C could select relevant skills from the 16 manufacturing process skills. These conditions must not be conflated with the deliberately different implementation levels in the illustrative ABC benchmark.

## Supported findings

- All 90 review records have unique run IDs and the expected task/group/repetition combinations.
- Core fields and observable features agree between CSV and JSON. Group summaries recomputed from individual records match the supplied summaries.
- The frozen review rubric matches its recorded SHA-256.
- In the related study ZIP, all 45 frozen-file hashes, 20 supplied-text hashes, and 1,737 submission-file hash entries match. This establishes file consistency, not authenticated model-session independence.
- The 16 skills in the newly supplied source ZIP match the study snapshots. All 16 pass the local `skill-creator` format validator. Format validity does not guarantee good behavior.
- The original report appropriately separates documentation, input defense, calculation correctness, and completion within the time budget. Its decision not to sum S/R/E/T/D into a leaderboard should be retained.

Evidence: [audit results](verification/audit.json), [study integrity checks](verification/study-integrity.json), [skill format validation](verification/skill-format-validation.json), and the [original Korean review](../evidence/completeness-review/CODE_COMPLETENESS_REVIEW_KO.md).

## Evaluation defects to fix first

### 1. Exceptions can produce false passes

The `throws()` helper in `benchmarks/abc-v1/tests/hidden_tests.py` accepts ValueError, TypeError, KeyError, and ArithmeticError as passing outcomes. Implementation A does not support the string-valued monetary inputs used in the fixture, so it raises TypeError even on valid inputs. The same unrelated defect is then counted as input defense in several negative tests.

Rerunning the original suite reproduced A=13/18, B=17/18, and C=18/18. However, **a deliberately broken implementation that always raises ValueError also passes 13/18**. A's score cannot be interpreted as 72% completeness or an adequate level of defensive validation.

With otherwise valid numeric input, A accepts quantity zero, fractional quantity 1.5, and duplicate suppliers. The passes for these cases in the original suite therefore do not establish correct contract enforcement.

For evaluator v2, first establish success on valid inputs. Change one condition at a time from a valid baseline, and verify the relevant error type or code and field. Check that the evaluator detects deliberately broken implementations that always fail, always succeed, or return a fixed answer. Freeze v2 separately and preserve the original results.

Evidence: [rerun outcomes](verification/abc-rerun.json), [deliberately broken implementation and diagnostic probes](verification/diagnostics.json), and the [original tests](../benchmarks/abc-v1/tests/hidden_tests.py).

### 2. The narrative disagrees with the recorded outcomes

The original `results/COMPARISON.md` says A fails zero quantity, fractional quantity, duplicate suppliers, nonfinite input, and rounding. The original JSON and the rerun instead show these five failures:

1. `correct_winner`
2. `correct_total`
3. `tie_deterministic`
4. `no_input_mutation`
5. `rounding_half_up`

The failure narrative needs correction. The original remains preserved as historical evidence, and this review identifies the discrepancy. In particular, the input-mutation check fails because calculation raises TypeError, not because mutation was observed.

### 3. The repetition demonstration does not measure optimization by an agent

The original skill package's `benchmark/benchmark.py` directly sets invocation counts to five and one. It does not implement or validate cache keys or invalidation. It therefore does not show that an agent identified redundant checks or saved tokens. The original README correctly states this limitation.

## Rechecking selected claims from the 90-artifact review

This was not a fresh rating or execution of all 90 programs. All records and relevant hashes were checked, and the following key examples were statically compared with the actual source.

| Example | Source observation | Implication for skill improvements |
|---|---|---|
| `r3_T05_C/production_quality.py:3,9–13` | The input range is documented but not enforced by the function | Connect SOR requirements to implemented checks and tests |
| `r1_T05_A/quality.py:6–11`, `r2_T05_B/quality.py:7–12` | A/B explicitly validate integer type, positive production, and defect counts | Do not assume C always provides stronger validation |
| `r3_T06_A/invoice_balance.py:17–19` | Display formatting rounds to integers despite Decimal arithmetic | Check user-visible output as well as returned values |
| `r1_T06_C/invoice_balance.py:19–21` | Output adds a currency unit not present in the request | Distinguish consequential assumptions from stated requirements |
| `r2_T09_B/oee.py:13–25` | NaN ideal-cycle time is not explicitly rejected and can propagate | Comparisons alone do not reject every nonfinite input |
| `r1_T09_A/oee.py:6,15`, `r3_T09_C/oee.py:4–5,30` | A documented 0–1 range conflicts with a calculation that can exceed 100% | Align the contract with behavior instead of inventing an unstated cap |
| `r1_T03_C/README.md:3–20` | Inputs, formula, conservation relationship, and execution instructions appear together | Retain useful handover documentation without rewarding length itself |

The [study source evidence](../evidence/study-reference/runs/) is preserved. The original report's 90/90 core pass count comes from its earlier execution evidence; it is not the result of rerunning all 90 programs in this review.

C has standalone documentation in 18/30 artifacts, versus 0/30 for A and B. Explicit raises occur in 12/11/6 artifacts for A/B/C, and finite-number checks in 4/4/2. Appropriate validation varies by task, so these frequencies are observations rather than rankings.

## Priorities for the skill instructions

1. In SOR, define important input/output contracts and testable examples while allowing reasonable, reversible decisions without unnecessary clarification.
2. In PFMEA, connect important risks to implemented controls and executed checks. A written risk list is not sufficient evidence of mitigation.
3. In Poka-Yoke, choose checks, types, constraints, or safe defaults that prevent relevant errors rather than adding warnings alone.
4. Apply MSA to evaluator false passes as well as flaky tests.
5. In the Control Plan, state when prior passing evidence remains valid and what invalidates it. Investigating flakiness or changed environments can justify repeated checks.
6. Limit completion claims to what was actually checked. Distinguish syntax checks, unit tests, visual inspection, and operational compatibility.
7. Scale the process to the task. Fixed document counts, attempt limits, or summary lengths should not block necessary work.

## Role of the rocket coding comparison

The requested comparison gives independent A/B/C conditions the same task: write and execute code that draws a rocket, then compare code and rendered output. It does not ask for a rocket with a manufacturing aesthetic. An earlier image-generation exploration did not execute a coding workflow and was excluded from the coding comparison evidence.

The new observations are recorded in the [actual coding comparison](../comparisons/rocket-code/README.md). More elaborate artwork or longer code does not establish C's superiority. A single observation must remain distinct from a repeatedly demonstrated effect.
