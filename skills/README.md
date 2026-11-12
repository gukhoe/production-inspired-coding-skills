# Manufacturing Process Control for AI Coding

16 independently installable v2 Agent Skills, each with a blank Markdown form and portable JSON record under assets/. Activate only relevant skills. Original supplied texts remain in the source ZIP; historical experiment results apply to those originals, not automatically to v2.

## Recommended routing
- Repeatable coding workflow: standard-work, scaled to the task; control-plan when checks need selection.
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
Edit procedures in scripts/skill_catalog.py and run scripts/build_skills.py. CI checks generated output drift so shared packaging changes cannot silently diverge. Copy the complete skill folder when installing it; no sibling skill or mandatory shared runtime is needed. See [v2 workflow and evaluation](../docs/SKILL_V2.md).

`python benchmark/benchmark.py` runs a deterministic demonstration of redundant-test elimination. It does not measure model token savings or real LLM code quality. For real comparison run paired tasks with the same model, prompts, budgets, repository state and scoring; record tokens, wall time, defects and regressions.
