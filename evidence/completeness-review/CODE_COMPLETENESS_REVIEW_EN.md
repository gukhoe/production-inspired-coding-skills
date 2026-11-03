# Code completeness review: correct output and maintenance readiness

English editorial edition of the historical post-hoc review. The complete Korean source is preserved byte-for-byte in [historical-originals.zip](../../sources/historical-originals.zip), under the corresponding `_KO.md` path. This edition is not the frozen source used for the original review hashes.

## Conclusion and scope

All 90 final submissions contained real calculation logic and fulfilled the requested input/output scope as small Python programs. This does not mean 100% production readiness. Every group separated calculations from examples and exposed reusable functions with arguments and return values. The review found no consistent structural or implementation-completeness advantage unique to C.

C more often produced requirements, scope and usage documents. Those documents did not consistently translate into defensive code. This was a static AI review after the experiment, not a new generation experiment or production validation. Review criteria were frozen before rereading code and randomized IDs concealed group labels. Style could reveal treatment, and the coordinator already knew aggregate results, so full blinding was not established.

Required: executable Python with actual calculations and the requested selection, ranking or output. Embedding supplied input values was allowed; printing hard-coded answers was not. GUI, database, API, packaging, CI, specific function names, JSON and CLI interfaces were not required. Neither code volume nor document volume earned credit. S/R/E/T/D labels are qualitative evidence categories, not a summed completeness percentage or statistical ranking.

## Observations

| Observed feature | A | B | C |
|---|---:|---:|---:|
| Final source meets original request | 30/30 | 30/30 | 30/30 |
| Calculation/example separation, arguments/returns and import guard | 30/30 | 30/30 | 30/30 |
| Assertion-based self-check evidence | 25/30 | 27/30 | 27/30 |
| Meaningful assertions beyond supplied example | 25/30 | 27/30 | 26/30 |
| No assertions beyond running the example | 5/30 | 3/30 | 3/30 |
| Separately authored requirements/scope/README | 0/30 | 0/30 | 18/30 |
| Explicit raise checks | 12/30 | 11/30 | 6/30 |
| Finite-number validation | 4/30 | 4/30 | 2/30 |
| Standard date-parser validation | 3/30 | 3/30 | 3/30 |

Feature counts are observations, not a more-is-better score. Validation appropriate for simple inventory arithmetic differs from OEE. Docstrings and examples can be sufficient documentation; standard-library exceptions may supply validation without custom `raise` statements. Tests were not explicitly required, so missing assertions did not automatically fail the original task. `r2_T03_A` had three inline assertions in execution logs despite having no test file. `r1_T01_C` meaningfully checked a quantity change that switched the selected supplier from Gamma to Beta.

## Task comparison

All task/group cells met the required scope in 3/3 final submissions. Self-check counts below count submissions with assertion evidence.

| Task | A checks | B checks | C checks | Interpretation |
|---|---:|---:|---:|---|
| T01 total cost / supplier selection | 3/3 | 3/3 | 3/3 | All separate data and calculation. Empty-list and tie policies vary. C documents requirements twice, but one implementation still fails on an empty `min` input. |
| T02 inventory | 1/3 | 1/3 | 1/3 | Concise reusable functions throughout. C's two documents do not establish better verification or input defense. |
| T03 shortage / surplus | 3/3 | 3/3 | 3/3 | Normal/shortage/surplus or balance checks. C supplies scope/usage documents in all repeats. Extra integer/negative checks in some A submissions require a justified business contract. |
| T04 unit cost | 2/3 | 3/3 | 3/3 | C documents all repeats. A repeat 2 adds finite-cost/quantity checks but is a late recovered artifact, not an on-time advantage. |
| T05 defect rate / good units | 1/3 | 2/3 | 3/3 | C self-checks more consistently; repeat 3 does not enforce its stated quantity constraints. All A/B repeats have explicit input checks. |
| T06 unpaid balance | 3/3 | 3/3 | 3/3 | C repeat 2 tests only the supplied example. A repeat 3 returns exact Decimal values but rounds displayed amounts. C repeat 1 assumes a currency. |
| T07 schedule delay | 3/3 | 3/3 | 2/3 | All use standard date parsing. Early completion as negative days or zero is an unspecified policy, not an automatic error. |
| T08 weighted ranking | 3/3 | 3/3 | 3/3 | All calculate and return rankings. C documents two repeats; missing-score/nonfinite defenses remain limited across groups. |
| T09 OEE | 3/3 | 3/3 | 3/3 | All check major denominators/quantities. Some omit NaN defense. One A and one C case describe 0..1 while allowing performance over 100%. |
| T10 BOM cost | 3/3 | 3/3 | 3/3 | C documents every repeat but has no explicit raise checks. Some A/B reject negative/nonfinite values; unspecified negative-value policy is not a mandatory requirement. |

## Concrete evidence

- `runs/r3_T05_C/production_quality.py:3` describes produced > 0 and bounded defective quantities, but lines 9–13 divide/subtract without validation. Zero production can divide by zero and defective > produced can yield negative good units. This is a static reuse risk, not a failure on supplied input. A's `r1_T05_A/quality.py:6–11` and B's `r2_T05_B/quality.py:6–13` explicitly validate types and ranges. C more consistently leaves normal/all-defective/no-defect tests; neither observation alone proves overall superiority.
- `runs/r3_T06_A/invoice_balance.py:6–10` returns Decimal, while lines 17–19 round displayed fractional amounts. Original integer input still passes. `runs/r1_T06_C/invoice_balance.py:19–21` adds an unrequested currency assumption.
- `runs/r2_T09_B/oee.py:13–19` checks major ranges but does not reject NaN. `r1_T09_A/oee.py:6,15` and `r3_T09_C/oee.py:4–5` have documentation/behavior tension around 0..1 ratios. The remedy is an accurate contract, not an invented requirement to clamp values.
- `runs/r1_T03_C/README.md:3–20` usefully records inputs, formulas, conservation, scope and execution/test commands. C's 18 standalone documents help handoff but do not by themselves establish greater correctness, defense or test quality.

## Limits and records

The conclusion applies to 10 small arithmetic/date tasks with three repeats. Maintenance, regression after changes, invalid-input recovery, installation, deployment, performance, security and user experience were not sufficiently exercised. No participant code was changed or regenerated for this review. Three over-budget recovered artifacts are included in final-source analysis and must remain separate from on-time completion. Missing token usage, unknown exact model revisions and shared filesystem limitations remain.

See `COMPLETENESS_REVIEWS.json` / `.csv` for 90 individual labels, locators and improvement notes; `COMPLETENESS_GROUP_SUMMARY.json` for counts without a total ranking; and [the English rubric](RUBRIC_FROZEN_EN.md). Raw structured study records retain their historical language. Referenced code is under the sibling `study-reference/runs/` directory. The original supplemental archive did not duplicate participant code.
