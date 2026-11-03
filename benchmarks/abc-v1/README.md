# A/B/C coding verification — controlled illustrative experiment

## Important limitation
All three implementations were authored in the same assistant session. This is NOT an independent comparison of three coding models or an empirical measurement of how different skills change LLM behavior. The three implementations intentionally represent three engineering rigor levels. No LLM token usage was measured. Execution times are for tiny Python tests and are not meaningful productivity estimates.

## Task specification
Select the supplier with lowest total landed quote cost:
`total = (unit_price * quantity + freight) * (1 + duty_rate) + tooling`.
Quantity must be positive integer; all monetary inputs nonnegative and finite; duty_rate between 0 and 1 inclusive; supplier names nonempty and unique ignoring case; no mutation; deterministic alphabetic tie break; monetary result rounded HALF_UP to cents. Empty quotes invalid.

## Groups
- A: minimal straightforward implementation, basic happy-path code.
- B: standard software engineering validation and Decimal arithmetic.
- C: risk-informed engineering, explicit SOR/PFMEA failure modes and Poka-Yoke checks.

## Reproduce
`python run_benchmark.py`

## Results
See `results/results.json`. Test suite includes 18 behavioral checks, all run on all groups. Tests are fixed in advance of reporting; the suite is visible in the deliverable. It is not an external independent hidden benchmark.

## Interpretation
These results show differences between these *specific implementations* and do not establish a causal skill effect. Stronger validation can be implemented without manufacturing terminology. For a valid skill study, run independent model invocations with identical prompt, model, tools, budgets, random assignment and pre-registered unseen tests, repeat across several tasks and report token counts, latency, pass rate and error rate.
