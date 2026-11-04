# Independent connection-audit demonstration

This example uses Python's standard library. No Graphify, REA, MCP server, external AI service or installed third-party package is needed.

```sh
python -S examples/connection-audit/run_demo.py --out .process-audit/my-connection-demo
```

Use a new output directory. The script copies the bundled synthetic example, starts a temporary HTTP server on loopback with an ephemeral port, runs four real request checks, shuts down the server, and writes before/after audit reports. It never executes an arbitrary audited repository.

Open `before/report.html` and `after/report.html` in that directory. Each includes a score summary, connection inspection and improvement queue. Fixed Markdown/JSON reports, source maps, manifests and execution evidence are alongside them. `comparison.json` contains observed outcomes.

## Defect and correction

A client submits an event to a gateway, which validates input and calls an in-memory ledger. The original ledger applies the same event twice. The correction checks its ID before mutation. This represents retry risk: the example sends an explicit replay, without simulating a lost response.

The fixture checks a normal event, an explicit replay, rejection of a negative amount and a different valid event. Inspect the locally generated request logs and before/after reports to review the outcomes. Generated audit results are not distributed with this example.

The example supplies explicit reviewer assessments for the replay boundary. The report engine checks those assessments against local evidence; it does not automatically estimate reliability. Unknown checkpoints, incomplete boundary reviews and blocked lifecycle gates remain visible after a local correction.

The fixture is single-threaded and in-memory. Persistence, concurrent admission, restart, authentication, TLS, deployment and remote-network behavior are excluded. The correction is not a production idempotency implementation. Python syntax analysis does not automatically discover the replay defect; the behavioral test supplies that evidence.

## Static pattern example

`static_before.py` and `static_after.py` are inert source samples; do not execute them. The mapper finds three candidates in the first and none of those patterns in the second:

```sh
python -S skills/software-process-audit/scripts/audit.py map-source --repo examples/connection-audit --path static_before.py --out .process-audit/pattern-before.json
python -S skills/software-process-audit/scripts/audit.py map-source --repo examples/connection-audit --path static_after.py --out .process-audit/pattern-after.json
```

Findings concern missing explicit timeout, disabled TLS verification and shell interpretation. An empty scan does not validate behavior or security.

`rea-fixture/` is a separate, optional JavaScript import-compatibility fixture. It is not used in the independent demonstration or executed. Complete REA evidence was tested locally; raw exports containing local paths are not published.

See [connection review usage and limits](../../docs/CONNECTION_RISK_REVIEW.md).
