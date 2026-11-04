# Connection risk review

Public preview: package `0.3.0a1`, tag `auditor-v0.3.0a1`. The earlier `auditor-v0.2.0` tag does not include this extension. Scoring standard `0.2.0`, manifest schema `2` and fixed report template `1.0` remain unchanged.

See [the preview release notes](RELEASE_0_3_0_PREVIEW.md). Project audit results and private validation artifacts are excluded from this update.

## Independent operation

Software Assurance Auditor runs without Graphify, REA, a graph database or an analysis service. Its CLI uses Python's standard library. The optional MCP entry point requires the MCP SDK; the AI host supplies its own model and authorized execution tools. The original 16 coding skills remain independently usable.

The core owns the questionnaire, evidence checks, scores, stage gates, connection questions, investigations, improvement records and reports. Its built-in Python analyzer extracts selected source relationships and three initial risk patterns. AI reviewers can inspect other languages and declare interfaces in the same manifest; those languages do not receive automatic extraction or security validation from the Python analyzer.

Graphify and REA exports are optional evidence inputs. Importing them neither changes the rubric nor completes an assessment. No upstream service is started or contacted.

## Connection questions

A line between two files is a starting point. Review both ends of an operation: accepted input, authority, state transition, failure response, recovery contract, owner and verification evidence. Turn a weakness into a reproducible failure scenario, corrective action and regression check.

Eight probes guide that investigation. They are unscored prompts, not eight checkpoints silently added to the existing 72:

| ID | Area | Discriminating check |
|---|---|---|
| CON-01 | Identity and authorization | Missing, expired or wrong-scope credentials are rejected at the receiver |
| CON-02 | Input and contract | Malformed, oversized, out-of-order or incompatible input is rejected before mutation |
| CON-03 | Time and resource bounds | A delayed/disconnected peer or full queue has bounded completion and cleanup |
| CON-04 | Retry and duplication | A repeated request after commit produces only the intended state change |
| CON-05 | Failure containment | Interruption before/after commit leaves recoverable, consistent state |
| CON-06 | Transport and sensitive data | Invalid peers are rejected and logs avoid unnecessary sensitive fields |
| CON-07 | Diagnosis and ownership | The same failed operation can be traced across both endpoints and assigned |
| CON-08 | Change and recurrence | The reproducer and neighboring valid workflow pass after correction |

Record results in applicable existing checkpoints and boundary reviews. An import, empty finding list or connected diagram is not test evidence.

## Standalone workflow

1. Declare scope, source snapshot and exclusions. Inspect intended behavior and actual code.
2. Run the built-in mapper on explicit Python files, or declare processes and handoffs directly for any language. Record unresolved connections.
3. Inspect material handoffs using the probes. Automatic patterns remain candidates until their context and consequences are reviewed.
4. Use authorized host tools to run a safe reproducer and an adjacent valid case. The audit server itself never runs project commands.
5. Record findings, evidence locators/hashes, owner, correction and acceptance conditions. Link risks explicitly to `boundary:<id>`.
6. Generate the fixed report, visual summary, connection view and improvement plan.
7. Apply an authorized correction, repeat discriminating checks, update evidence and re-evaluate. Exporting a task or changing a diagram never closes it.

```sh
# From this checkout; no pip install or external analyzer required.
python skills/software-process-audit/scripts/audit.py map-source --repo /project --path client.py --path gateway.py --path store.py --out connections.json
python skills/software-process-audit/scripts/audit.py report --repo /project --manifest review.json --revision SNAPSHOT --connections connections.json --out reports/run-001 --strict
python skills/software-process-audit/scripts/audit.py connection-path --input connections.json --seed file:gateway.py --direction outgoing --depth 2
```

Create and assess the manifest using the [standard workflow](software-process-audit.md). Optional process `code_nodes` lists map processes to normalized source IDs, for example `"code_nodes": ["file:gateway.py"]`. Source risk overlays require explicitly mapped boundary endpoints. Unmapped risks remain in the report and improvement queue. Run [the independent HTTP replay demonstration](../examples/connection-audit/README.md) for a complete example.

## Outputs

`report` writes four new files and refuses existing outputs: `report.json`, `report.md`, `report.html`, and `improvement-plan.json`. The HTML embeds its data, has no external scripts or network requests, and opens offline. Its print button produces an A4 landscape summary. Browser settings and unusually long narrative can affect pagination; inspect the export.

| View | Contents |
|---|---|
| Summary | Area score diagram, coverage, high-impact risks, handoffs, gates and priority actions |
| Full network (default) | Every supplied node and edge, red reviewed-risk overlays, search/filter, pan/zoom, paginated keyboard-accessible list and evidence details |
| Improvement queue | Stable target IDs, finding, action, owner, due field, evidence references and verification condition; JSON export |

Red means an open reviewed high/critical risk or assessed gap. Amber means incomplete review or an unconfirmed static candidate. Dashed lines indicate inferred or unknown source relationships. Neither red nor reachability proves an exploit or runtime failure propagation.

Scores measure evidence maturity, not reliability or defect probability. Read score, scorable coverage and achievement lower bound together. Unknowns stay unscored. The visual layer does not change scores.

The printable summary shows up to 16 processes, admitting risk endpoints first. The default interactive source network retains every supplied node and edge, including isolates and parallel links. The former 240-node/2,000-edge display cap has been removed. Explicit search/filters change the visible subset; **Show all / fit** restores the complete graph. Labels are decluttered at low zoom, without removing nodes or edges. CLI path queries still use explicit traversal bounds and return one path per reached node.

### Partitioned preparation and merge

The renderer partitions nodes by source group/module, then splits groups larger than 600 nodes. A node belongs to exactly one job. Each edge is assigned either to one local job or to a separate cross-partition list. Up to four browser workers compute independent local layouts; small jobs are batched to reduce worker overhead. Stable node IDs place returned coordinates into the complete network, including every cross-partition connection.

The initial complete topology is visible while batches finish. Progress reports completed/total partitions; pause stops further dispatch while in-flight batches finish. Completed coordinates are reused when switching maps. A task timeout or worker error leaves its provisional coordinates visible and explicitly reports incomplete partitions. Worker-unavailable environments use incremental local processing. Neither case deletes graph records or changes assessment results.

Large reports embed gzip-compressed evidence using Python's standard library. Modern browsers decompress it locally; there is no server or external network dependency. Local Blob workers are permitted by the report's content policy; external connections remain disabled. All provenance fields survive compression. MCP returns one complete graph in the HTML plus summary metadata, avoiding a second large graph in the tool response.

This parallelism accelerates graph preparation, not independent AI assessment of every module. Semantic judgments, source verification and audit scoring keep their existing evidence requirements. Extraction coverage is distinct from display completeness: showing all supplied relationships does not establish that every runtime connection was discovered.

## Built-in analysis limits

The Python AST scanner reads selected UTF-8 files without importing or executing them. It records files, functions, import expressions, call expressions and unambiguous selected local-module candidates, with hashes and line numbers. Local import resolution remains inferred; call expressions are not a complete call graph.

Initial candidate rules: recognized `requests` calls with no explicit timeout or `timeout=None`; `verify=False`; and recognized `subprocess` calls with `shell=True`. Wrappers, dynamic arguments, shadowing and runtime configuration can affect their meaning. No findings does not establish security.

Limits: 500 selected files, 2 MiB/file, 16 MiB total, 10,000 nodes and 50,000 edges. Parse failures stay visible. Dynamic dispatch, full inter-file symbol resolution, binary analysis, non-Python parsing, taint analysis, live traffic capture and comprehensive vulnerability detection are not implemented in this preview.

## Optional import contract

```sh
software-audit import-connections --format graphify --input graph.json --out connections.json
software-audit import-connections --format rea --input complete-evidence.json --out connections.json
software-audit visualize --report report.json --connections connections.json --out review.html
```

Native schema `software-assurance-connections/1` requires unique `nodes` and `edges`, explicit directedness, confidence (`EXTRACTED`, `INFERRED`, `UNKNOWN`), relation, provenance, coverage and limitations; candidate findings are optional. Parallel links remain distinct. Export hashes do not establish source freshness.

The Graphify adapter accepts node-link schema 1. Unknown confidence remains unknown; undirected relationships do not gain call direction. Hyperedges are disclosed but not traversed.

The REA adapter accepts complete `analyze_javascript_application` evidence with `JavaScriptApplicationGraph` and optional `JavaScriptSemanticRelationGraph`. Summary receipts are rejected. Evidence contexts, artifact references, coverage, limitations and contradictions are retained. An `observed` source relation remains static evidence. Other REA operations and binary evidence need separate adapters.

## Functional benchmark

Graphify was inspected at commit [`59b5ab1`](https://github.com/Graphify-Labs/graphify/tree/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0), package `0.9.102`. Its [analysis module](https://github.com/Graphify-Labs/graphify/blob/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0/graphify/analyze.py) includes structural diagnostics and graph differences; its [query/path tools](https://github.com/Graphify-Labs/graphify/blob/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0/graphify/serve.py) and [interactive exporter](https://github.com/Graphify-Labs/graphify/blob/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0/graphify/exporters/html.py) make relationships explorable. This extension independently implements an audit-focused view and [export-format interoperability](https://github.com/Graphify-Labs/graphify/blob/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0/graphify/export.py); it incorporates no Graphify source.

The contribution is a review loop around relationships: standardized questions, explicit unknowns, reproducible failures, risk ownership, preventive controls and verified correction. Density or centrality alone is not scored as a defect. Full graph-difference analysis and automatic verified repair remain future work.
