# Production-inspired coding skills: historical 90-run study

English editorial edition. The full original report, including its detailed tables, is preserved in [historical-originals.zip](../../sources/historical-originals.zip), under `evidence/study-reference/SUMMARY_KO.md`. References to evaluation logs and original study directories describe the full source package, not files necessarily included in this selected evidence checkout.

## Findings

The study recorded final code and output for 10 tasks × three groups × three repeats. All groups' final artifacts had the same correctness results. Exact token usage was not measured, so token savings cannot be evaluated. Only 87 of 90 runs recorded completion within the instructed 300 seconds. Repeat 2 of T04 exceeded the budget in all groups after interruption/recovery; recovered artifacts are included in final correctness, not on-time completion.

Ninety artifacts and recorded executions do not independently authenticate 90 isolated sessions. Creation-response fields were retrospectively transcribed rather than exported as original platform logs. A later live query exposed only the last six session states. Complete conversations, tool traces and exact model/version/reasoning settings were unavailable. Skill-reading reports are participant self-reports. Do not present this as an independently verified causal experiment with clean isolation and confirmed model identity.

| Metric | A: no extra skill | B: verification skill | C: production-inspired skills |
|---|---:|---:|---:|
| Final artifacts | 30 | 30 | 30 |
| Supplied-input passes | 30/30 | 30/30 | 30/30 |
| Additional normal/boundary/invariant passes | 120/120 | 120/120 | 120/120 |
| Completion within 300 seconds | 29/30 | 29/30 | 29/30 |
| Timeouts | 1 | 1 | 1 |
| Development test commands | 25 | 27 | 27 |
| Test commands within 300 seconds | 24 | 27 | 26 |
| Self-test cases executed | 102 | 110 | 90 |
| Administrative check commands | 0 | 3 | 0 |
| Example executions | 30 | 30 | 30 |
| Observed Python revision batches between executions | 1 | 0 | 0 |
| Recorded development-program execution failures | 0 | 0 | 0 |
| Repeated success with same source and command | 0 | 0 | 0 |
| Mean observed time, seconds | 62.04 | 65.01 | 71.44 |
| Median observed time, seconds | 28.83 | 29.68 | 37.17 |
| Minimum observed time, seconds | 20.70 | 16.16 | 26.56 |
| Maximum observed time, seconds | 1036.85 | 1044.51 | 1053.03 |
| Total observed time, seconds | 1861.30 | 1950.23 | 2143.29 |
| Provider tokens, calls and cost | Unmeasured | Unmeasured | Unmeasured |

Each group also had 60 unspecified-policy diagnostic executions excluded from correctness denominators. Original CSV combined primary/additional correctness fields, while `status` separately recorded budget violations. `r2_T03_A` contained three assertions in a command labeled `check`; it counts as one program-test command. B's three extra `check` commands examined files/logs/end markers and are administrative. A's one revision was a test-file addition in `r2_T10_A`, not a production defect repair.

## Interpretation

No accuracy improvement was observed. Small arithmetic/date tasks and a final-artifact ceiling effect prevent a conclusion that the skills are ineffective or equivalent across development contexts. Token savings are unknown: code length, response length and estimated tokens are not substitutes for provider usage. Skill-reading, caching and reasoning costs are unavailable.

C executed fewer self-test cases than B but the same number of test commands. All groups had zero recorded repeated successes with identical source/command. There is no evidence that C reduced unnecessary verification.

Excluding the entire repeat-2 T04 block from all groups gives mean observed times A 28.43, B 31.23 and C 37.60 seconds. C was not faster in these observations. Timing includes skill reading, tools and measurement, excludes pre-first-action queue/inference, and is not a causal speed estimate. The original report's task-cluster bootstrap used 20,000 resamples and exploratory 95% intervals; those describe selected-task variation, not uncertainty over all software development. Zero accuracy differences yield degenerate intervals and do not establish equivalence.

## Expected and observed outputs

All final outputs passed their frozen tolerances. Primary expected results were: T01 supplier costs Alpha 52000, Beta 50500, Gamma 50300 and winner Gamma; T02 inventory 100; T03 balance -200; T04 unit cost 20; T05 defect ratio 0.03 and good units 2425; T06 unpaid balance 6000; T07 delay four days; T08 scores A 86, B 88.2, C 86.7 and ranking B/C/A; T09 OEE 0.765625; T10 BOM cost 19.1. Some OEE displays normalized to approximately 0.7656 and passed the frozen rounding tolerance. Formatting, units and integer/float representation were normalized without changing participant calculations.

## Timeout deviation

| Run | Start-to-end seconds | Production execution within 300 seconds | Treatment |
|---|---:|---|---|
| r2_T04_C | 1053.03 | Yes | Late recovered artifact, excluded from on-time completion |
| r2_T04_B | 1044.51 | Yes | Late recovered artifact, excluded from on-time completion |
| r2_T04_A | 1036.85 | No | Late recovered artifact, excluded from on-time completion |

Sessions disappeared from the active list without completion records. Administrative follow-ups asked them to finish within the original limits or report blocked status, without evaluation results or repair hints. Actual time checks later showed the budget had already expired. B's examples/tests ran on time but its end marker was late; C's example was on time but its test/end marker were late. A ran after the limit. The cause was not established. The instruction-level limit was not enforced by platform termination.

## Provenance and limitations

A received no extra experiment skill/AGENTS.md, but shared platform instructions remained. B used the pinned `obra/superpowers` verification-before-completion text and MIT license; its hash is `3e8a4adf7bd1df7881c56bf85ec014c430ccd9699cc0c0d212389d8922f5d074`. Upstream commit and raw HTTP byte identity were not verified. C received the index and 16 skills; all 30 C sessions reported reading standard-work and sor-requirements. The study does not establish effects of the other 14 skills.

Original ZIP hashes in the report were parent-reported assertions, distinct from direct local verification: study package `9c7a0cf1b8a8d0eabd74ea4408fae007d12dcfb9e1db322b798c11f679818365`; skills package `144498e0129db7d4caa709284c5513d248291e72ab2e90d226b3d6866e66f010`. The study environment failed to download the ZIPs directly and received 20 extracted UTF-8 files. Local text hashes are in `supplied_text_provenance.json`. Existing benchmark code and prior-chat scores were not reused as participant output.

The original package records 70 frozen cases (10 primary, 40 additional, 20 diagnostics), 12 evaluator self-checks and 630 independent saved-code executions. Input adapters changed only input/output representation. Session creation requested fresh contexts and identical inherited settings, but exact model identity and enforced filesystem isolation were unavailable. Run 1 received administration in its start message; runs 2/3 received the same content as files, adding reads equally across groups. Up to six concurrent sessions and randomized dispatch did not control actual scheduling or changing shared load. Python hash changes measure logged revision batches, not every edit or model call. No unrelated purchasing repository was modified and no paid external API key was created or used.

See [90 run details](RUN_DETAILS_EN.md), [protocol](PROTOCOL_FROZEN_EN.md), [source notes](README.md) and the repository's [independent evidence review](../../reports/REVIEW.md). Stronger future evaluation needs more demanding development/change tasks, enforceable isolation and exact model/usage instrumentation.
