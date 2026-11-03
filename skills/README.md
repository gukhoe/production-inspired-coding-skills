# Manufacturing Process Control for AI Coding

16 independent, concise Agent Skills. Activate only relevant skills; do not load all 16 for every task. The skills are original synthesis, not copied from linked repositories.

## Recommended routing
- Every task: standard-work; control-plan only when checks need selection.
- New feature: sor-requirements.
- Changed business logic: pfmea-risk.
- Bug: eight-d-root-cause.
- Risky edit: ecn-change-control, poka-yoke.
- Critical failure: andon-jidoka, containment.
- High-risk release: ppap-release-evidence, apqp-stage-gates.
- Unreliable checks: msa-test-reliability.
- Repeated delivery: spc-quality-trends, line-balancing, kanban-wip.
- Generated templates: first-article.

## Important limitations
Skills are instructions, not sandbox implementations. Use actual test runners and isolate untrusted code. A passing sandbox test does not prove production compatibility. Cache only when source, dependencies, config, inputs, and environment match.

## Benchmark
`python benchmark/benchmark.py` runs a deterministic demonstration of redundant-test elimination. It does not measure model token savings or real LLM code quality. For real comparison run paired tasks with the same model, prompts, budgets, repository state and scoring; record tokens, wall time, defects and regressions.
