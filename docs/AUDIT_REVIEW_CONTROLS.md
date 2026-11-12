# Review accountability and evidence controls

Source preview 0.3.0a2 adds assurance policy 1.0 to manifest schema 2.
New reviews use standard 0.3.0 with [balanced area budgets and checkpoint-specific
evidence requirements](SCORING_BALANCE.md); declared standard 0.2.0 retains its
original scoring policy. Read assurance, scoring and template versions together:
stricter evidence validation can reduce scores without a product regression.

## Review context

Record the implementation/change `author`, `audit_context.type` (`first_party`,
`second_party`, `third_party`), `audit_context.relationship` (`independent`, `self`,
or `unverified`) and an `independence_rationale`. First-party audits can have an
independent reviewer; third-party labeling alone does not prove independence.
Missing context, self review, or an author matching a supported-check reviewer
prevents `reviewed_scope_supported` and blocks handoff promotion. A self-review
can still produce useful findings and partial evidence; it is visibly distinct.

These names and declarations are not authenticated identity. The software does
not claim ISO/IATF/VDA compliance or mechanically prove auditor independence.
Producer and receiver may be the same operational role; reviewer accountability
is assessed separately from artifact integrity.

## Evidence reused across checkpoints

When the same content hash supports more than three scored/excluded checkpoints,
each supported or excluded checkpoint needs `evidence_links` naming the evidence,
a precise locator and a checkpoint-specific rationale. Aliasing the same file
under new evidence IDs does not avoid the reuse check. Example structure:

```json
{"evidence_links": [{"evidence_id": "E1", "locator": "test result case: rejects expired session", "rationale": "The actual receiver rejects the stale identity before mutation, supporting PRE-01.3."}]}
```

Three is a review policy threshold, not a statistical assurance level or an upper
bound on legitimate reuse. A single structured execution log can support many
questions when its distinct relevant cases are identified. Fabricated rationales
can still be fabricated: the engine checks record consistency; a reviewer must
judge substantive adequacy. Missing links downgrade the affected supported claim
to unverified, not to a confirmed defect.

## Local witness recording

The CLI has an explicit opt-in execution recorder. The MCP server remains read-only
and has no witness/execute tool. Run only an authorized command against selected
inputs, for example:

```sh
software-audit witness --repo /project --out /project/.audit/run-001 --revision SNAPSHOT --source tests/check.py --timeout 60 -- python tests/check.py
```

The command is an argument list with no shell; it executes with the local user's
permissions and is not a sandbox. The output directory must be new. Logs and a
receipt record argv, working directory, start/end times, exit code, termination
reason, output hashes and before/after hashes of the selected source files.
Timeouts and excessive output trigger termination. The output budget is polled,
so bursts can exceed it before the child is stopped. Background/detached processes
and hostile code require a real OS sandbox; use isolated fixtures.

Register stdout.log as execution evidence and set `witness_receipt` to its
repository-relative receipt.json. Copy the exact JSON serialization of receipt
`command`, `recorded_at` and `exit_code` into the evidence. Validation checks both
logs, metadata and unchanged selected inputs. A changed/missing receipt or selected
source invalidates the witness evidence. Unselected files are outside its binding.

`local_witness_consistent` is stronger than a hand-entered command but is **not** a
signature or tamper-proof attestation. A same-user writer can forge all local files.
GitHub artifact-attestation verification and trusted CI identity are future work;
an uploaded CI log is not automatically authenticated. Reports retain execution
provenance separately from semantic adequacy and scores.

## Static analysis interoperability

```sh
software-audit import-connections --format sarif --input scanner.sarif --out connections.json
```

The adapter accepts [SARIF 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html),
preserves rule/tool/result provenance, suppression and code-flow metadata, and
retains results without a source location. Artifact indices are resolved from the
same run. URIs/base IDs remain data; no file or network URI is fetched. Diagnostic
location edges are not invented function calls. All imported findings remain
unconfirmed candidates. Limits: 16 MiB JSON input, 32 MiB normalized output,
10,000 results, 100 locations per result and 50,000 total locations. Expanded
provenance counts toward the output budget; split large exports rather than
silently dropping findings.

Use a scanner/exporter that actually emits SARIF. Native Bandit JSON is a different
format and needs a separate conversion; it is not silently treated as SARIF. The
built-in Python mapper adds a narrow `except: pass` diagnostic to its initial
timeout/TLS/shell rules. It remains a partial scanner, not a Bandit/Semgrep/CodeQL
replacement, and does not claim to detect arbitrary eval/pickle/SQL/retry risks.

## Verification and CI

The workflow tests installed MCP on Python 3.11–3.13 and Linux/Windows, checks
graph-partition invariants, mutation sentinels, generated skill drift and original
archive provenance, and runs focused Ruff, Bandit and complexity visibility checks.
Ruff is configured for correctness errors and unused imports, not every style rule;
Bandit handles the dedicated security pass. Intentional local subprocess execution
is narrowly annotated and covered by failure/timeout tests. Complexity reporting
does not equate a low number with safety. CI execution is only established after
the workflow actually runs; adding YAML alone is not a CI PASS.

No generated audit reports, private project files or raw artifacts are uploaded by
the workflow. The three fixed mutation sentinels challenge hash, description and
revision checks; they do not claim exhaustive mutation coverage.
