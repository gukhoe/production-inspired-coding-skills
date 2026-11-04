# Software Assurance Auditor 0.3.0a1

Public preview of independent connection-risk review. Install from the `auditor-v0.3.0a1` GitHub tag using [the CLI/MCP setup guide](MCP_SETUP.md). This is a source release, not a PyPI publication.

## Included capabilities

- Independent Python source mapper and three initial, unconfirmed risk-pattern rules.
- Eight connection-review probes covering authority, contracts, time/resource limits, duplication, containment, transport, diagnosis and recurrence prevention.
- Offline area-score summary, full supplied network, red reviewed-risk overlays, evidence details and an improvement queue.
- Bounded module layout jobs in up to four browser workers, complete cross-partition merge, pause/resume, cached layouts and explicit fallback notices.
- Lossless compressed loading for large reports, with no external browser connections.
- Twelve MCP tools; the four added tools map, import, traverse and visualize connections.
- Optional Graphify and REA evidence adapters. Neither service is required for independent operation.
- Synthetic example source and regression tests. Running the example creates local results in the directory selected by the user.

The 16 original coding skills remain separately usable. The 72 checkpoints, scoring standard 0.2.0, manifest schema 2 and fixed report template 1.0 are unchanged.

## Known limits and next improvements

Native parsing currently covers selected Python files only. C# and other-language semantic extraction, complete symbol/data-flow resolution, runtime communication tracing and before/after graph comparisons remain future work. Imported graphs may be stale or incomplete. Showing every supplied relationship is a display guarantee, not a complete model of the current program.

Static patterns are candidates for investigation. A reviewer must inspect context, exercise a discriminating scenario through authorized host tools and record actual evidence. The MCP server does not execute project commands. Scores measure evidence maturity, not safety or failure probability; read coverage and unresolved risks alongside them.

## Publication boundary

This update contains code, process definitions, blank reporting structures and installation/use documentation. It excludes project audit results, audited project snapshots, private graphs, screenshots and raw execution logs. Optional upstream tools are referenced for interoperability; their source is not incorporated.

Existing audit users can retain their schema-2 manifests. Re-evaluate them against the correct current source and save outputs to a new directory. The output set now includes `report.html` and `improvement-plan.json` alongside the fixed JSON/Markdown report. For large compressed reports, use a browser with `DecompressionStream` support.
