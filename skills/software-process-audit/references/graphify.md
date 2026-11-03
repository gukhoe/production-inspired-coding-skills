# Graphify integration

Upstream: [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify). Tested export: `graphifyy 0.9.101`, schema 1. The installed package is named `graphifyy`; do not confuse similarly named projects.

## Two integration paths

- **Agent + existing MCP:** discover the tools actually exposed by the configured server. The inspected 0.9.101 server offers `query_graph`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `graph_stats`, and `shortest_path`, among other tools. Verify names/arguments against `list_tools` for the installed version. Use these read-only queries for investigation; retain source paths and reviewed findings in the manifest. Query text is not execution evidence.
- **Deterministic CLI or independent audit MCP:** consume the existing `graphify-out/graph.json`. The adapter needs no Graphify Python dependency, API key, network, or running Graphify server. Graphify MCP responses are not automatically converted into assessments. The auditor has its own MCP server and can work entirely without Graphify; export-based integration is an optional evidence source, not a Graphify proxy.

The 0.9.101 local server can be started with `graphify-mcp /absolute/path/to/graph.json`. Starting a server does not install it into an assistant's tool registry. Keep the user's existing configuration unchanged unless setup changes are requested.

## Evidence semantics

The reader accepts node-link JSON with `directed`, `multigraph`, `graph.schema_version=1`, `nodes`, and `links`. Node IDs must be unique strings; links must resolve to known endpoints. Unknown schema versions fail explicitly. The default input limit is 128 MiB. Hyperedges are counted but not traversed.

Retain `EXTRACTED`, `INFERRED`, and unknown confidence labels. Extracted means structural extraction, not observed execution. One inferred edge makes a discovery path inferred; unknown evidence stays unknown. The first discovered path is reported, not the strongest or every possible path. Parallel-edge and alternate-path completeness is not claimed.

Direction comes from the export. For undirected graphs, relationship traversal cannot establish callers, event order, causality, or a definite failure propagation path. Some projects preserve a separate directed pre-clustering graph; inspect its actual schema before using it. No silent conversion of unsupported formats.

Use graph node IDs in `processes[].graph_nodes`. Only direct graph links between explicitly mapped runtime nodes are compared with declared boundaries. An uncovered pair produces `graph_connection_requires_review`; this is a scope question, not an automatically confirmed defect. Delivery-process handoffs are manually mapped separately. Results are bounded and disclose truncation.

A graph SHA-256 binds a report to the export bytes. It does not establish that the export was built from current source. Source freshness remains unverified in graph metadata; review extraction inputs, timestamps and source hashes separately. Dynamic dispatch, reflection, HTTP, files, native boundaries and unsupported languages require additional evidence. An empty query result does not prove absence of a dependency.

## Fair comparison

Graphify already supports relationship exploration and impact investigation. Existing project FMEA/checklists may already implement process-risk analysis. The additional value here is a reusable evidence/status model and repeatable report gate across those inputs. Do not claim novel findings simply because existing documented limitations were imported into the audit report. Demonstrate improvements with paired tests on identical snapshots and deliberate evidence omissions.
