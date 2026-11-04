"""Portable connection evidence and review questions, independent of graph vendors.

Static extraction never establishes a runtime interaction or a confirmed vulnerability.
"""
import ast
from collections import deque
import hashlib
import json
from pathlib import Path

if __package__:
    from .graph_adapter import AuditError, Graph, read_json
else:
    from graph_adapter import AuditError, Graph, read_json

SCHEMA = "software-assurance-connections/1"
PROBES = [
    ("CON-01", "Identity and authorization", "Can an untrusted caller impersonate a peer or perform an unauthorized operation?", "Exercise missing, expired and wrong-scope credentials at the receiving side."),
    ("CON-02", "Input and contract", "Do producer and consumer agree on schema, units, versions and valid state?", "Send malformed, oversized, out-of-order and version-mismatched messages; verify rejection before mutation."),
    ("CON-03", "Time and resource bounds", "Are timeout, cancellation, queue capacity and resource ownership bounded?", "Delay or disconnect the peer and exhaust the queue; measure bounded completion and cleanup."),
    ("CON-04", "Retry and duplication", "Can retries or reconnects repeat a state-changing operation?", "Lose the response after commit, retry the same operation, and verify exactly the intended final state."),
    ("CON-05", "Failure containment", "Does a partial failure leave consistent state and a recoverable boundary?", "Interrupt each side before and after commit; verify rollback, compensation or controlled resumption."),
    ("CON-06", "Transport and sensitive data", "Are peer identity, transport integrity and sensitive data protected?", "Challenge certificate/peer validation and inspect logs for unnecessary sensitive fields."),
    ("CON-07", "Diagnosis and ownership", "Can the failing operation be correlated across both ends and assigned to an owner?", "Correlate an injected failure across sender, receiver and recovery logs without exposing secrets."),
    ("CON-08", "Change and recurrence", "Do changes preserve adjacent consumers and prevent the observed failure recurring?", "Run the reproducer, a valid neighboring workflow and version/rollback checks after correction."),
]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def connection_catalog():
    return [{"id": key, "title": title, "question": question, "verification": verification}
            for key, title, question, verification in PROBES]


def validate_connections(data):
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise AuditError("Unsupported connection evidence schema")
    nodes, edges = data.get("nodes"), data.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list) or len(nodes) > 100000 or len(edges) > 300000:
        raise AuditError("Connection graph requires arrays within 100000 nodes / 300000 edges")
    ids, eids = set(), set()
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("id"), str) or not node["id"] or node["id"] in ids:
            raise AuditError("Connection nodes require unique string IDs")
        if not isinstance(node.get("label"), str):
            raise AuditError("Connection node label must be text")
        ids.add(node["id"])
    for edge in edges:
        if (not isinstance(edge, dict) or not isinstance(edge.get("id"), str) or not edge["id"] or edge["id"] in eids
                or not isinstance(edge.get("source"), str) or not isinstance(edge.get("target"), str)
                or edge["source"] not in ids or edge["target"] not in ids):
            raise AuditError("Connection edge has a duplicate ID or unknown endpoint")
        if type(edge.get("directed")) is not bool or edge.get("confidence") not in ("EXTRACTED", "INFERRED", "UNKNOWN"):
            raise AuditError("Connection direction/confidence must be explicit; runtime is assessed separately")
        if not isinstance(edge.get("relation"), str) or not isinstance(edge.get("provenance"), dict):
            raise AuditError("Connection relation and provenance required")
        eids.add(edge["id"])
    if (not isinstance(data.get("coverage"), dict) or not isinstance(data.get("limitations"), list)
            or any(not isinstance(item, str) for item in data["limitations"])):
        raise AuditError("Connection coverage and limitations required")
    findings = data.get("findings", [])
    if not isinstance(findings, list):
        raise AuditError("Connection findings must be an array")
    seen = set()
    for finding in findings:
        if (not isinstance(finding, dict) or not isinstance(finding.get("id"), str) or not finding["id"]
                or finding["id"] in seen or not isinstance(finding.get("edge_id"), str) or finding["edge_id"] not in eids
                or finding.get("state") != "candidate" or finding.get("severity") not in ("low", "medium", "high", "critical")):
            raise AuditError("Connection findings must be unique candidates linked to known edges")
        if any(not isinstance(finding.get(key), str) for key in ('title', 'failure_scenario', 'improvement', 'verification')):
            raise AuditError("Connection finding narrative must be text")
        seen.add(finding["id"])
    return data


def import_connections(path, format):
    data, sha = read_json(path)
    if format == "native":
        return validate_connections(data)
    nodes, edges, limitations = [], [], []
    if format == "graphify":
        graph = Graph(path)
        nodes = [{"id": nid, "label": str(n.get("label", nid)), "kind": str(n.get("type", "code")),
                  "path": n.get("source_file", n.get("file", "")), "line": n.get("line", n.get("start_line")),
                  "group": n.get("community_name", n.get("community")), "original": n}
                 for nid, n in graph.nodes.items()]
        for index, edge in enumerate(graph.edges):
            edges.append({**edge, "id": "graphify:" + str(index), "directed": graph.directed,
                          "confidence": edge["confidence"] if edge["confidence"] in {"EXTRACTED", "INFERRED"} else "UNKNOWN",
                          "provenance": {"provider": "Graphify", "export_sha256": sha, "original_confidence": edge["confidence"]}})
        coverage = {"status": "unknown", "source_freshness": "unverified", "hyperedges_not_traversed": graph.hyperedge_count}
        limitations = ["Export bytes identified; source freshness and runtime behavior remain unverified.",
                       "Direction follows the export; undirected links cannot establish call direction or failure propagation."]
        provider = "Graphify"
    elif format == "rea":
        if data.get("operation") != "analyze_javascript_application":
            raise AuditError("REA adapter supports complete analyze_javascript_application Evidence only")
        result = data.get("normalized_result", {})
        graph = result.get("graph", {})
        if graph.get("schema") != "JavaScriptApplicationGraph":
            raise AuditError("REA summary receipts are not complete graph evidence")
        contexts = {c["context_id"]: c for c in result.get("semantic_graph", {}).get("evidence_contexts", [])}
        def provenance(evidence):
            return {"provider": "REA", "evidence_id": data.get("evidence_id"), "export_sha256": sha,
                    **contexts.get(evidence.get("context_id"), {}), **evidence}
        def location(evidence):
            value = evidence.get("location", {}).get("value", {})
            return value.get("source", value.get("path", "")), value.get("start", {}).get("line")
        for node in graph.get("nodes", []):
            obs = (node.get("observations") or [{}])[0]
            ev = provenance(obs.get("evidence", {}))
            source, line = location(ev)
            nodes.append({"id": node["node_id"], "label": obs.get("label", node["node_id"]),
                          "kind": node.get("kind", "unknown"), "path": source, "line": line, "provenance": ev})
        semantic = result.get("semantic_graph", {})
        if semantic and semantic.get("schema") != "JavaScriptSemanticRelationGraph":
            raise AuditError("Unsupported REA semantic graph schema")
        for node in semantic.get("nodes", []):
            ev = provenance(node.get("evidence", {}))
            source, line = location(ev)
            nodes.append({"id": node["node_id"], "label": node.get("label", node["node_id"]),
                          "kind": node.get("kind", "unknown"), "path": source, "line": line,
                          "properties": node.get("properties", {}), "provenance": ev})
        for edge in graph.get("edges", []) + semantic.get("relations", []):
            ev = provenance(edge.get("evidence", {}))
            tag = "INFERRED" if ev.get("state") == "inferred" or edge.get("resolution") == "candidate" else "EXTRACTED" if ev.get("state") == "observed" else "UNKNOWN"
            edges.append({"id": edge.get("edge_id", edge.get("relation_id")), "source": edge["source_node_id"],
                          "target": edge["target_node_id"], "relation": edge["relation"], "directed": True,
                          "confidence": tag, "provenance": ev, "properties": edge.get("properties", {})})
        coverage = {"status": "unknown", "application": graph.get("coverage"), "semantic": semantic.get("coverage"),
                    "source_selection": result.get("source_selection"), "integrity_contradictions": result.get("integrity_contradictions", [])}
        limitations = list(data.get("limitations", [])) + ["REA observed/static facts are not runtime communication proof. No target was executed by this import."]
        provider = "REA"
    else:
        raise AuditError("Connection format must be native, graphify or rea")
    return validate_connections({"schema": SCHEMA, "provider": provider, "source_sha256": sha,
                                 "nodes": nodes, "edges": edges, "findings": [], "coverage": coverage, "limitations": limitations})


def scan_python(root, paths):
    """Inspect explicitly selected UTF-8 Python files without importing/executing them."""
    if __package__:
        from .audit import safe_file
    else:
        from audit import safe_file
    root = Path(root).resolve()
    if not isinstance(paths, list) or not 1 <= len(paths) <= 500 or not all(isinstance(p, str) and p for p in paths) or len(set(paths)) != len(paths):
        raise AuditError("Select 1..500 distinct Python source paths")
    paths = [Path(p).as_posix() for p in paths]
    if len(set(paths)) != len(paths):
        raise AuditError("Selected source paths must be distinct after normalization")
    nodes, edges, edge_ids, findings, examined, errors = {}, [], set(), [], [], []
    total_bytes = 0
    selected = {Path(p).as_posix() for p in paths}
    def node(nid, label, kind, **extra):
        nodes.setdefault(nid, {"id": nid, "label": label, "kind": kind, **extra})
        nodes[nid].update(extra)
        return nid
    for relative in paths:
        path = safe_file(root, relative)
        if path.suffix != ".py" or not path.is_file() or path.is_symlink():
            raise AuditError("Select existing .py source files only")
        raw = path.read_bytes() if path.stat().st_size <= 2 * 1024 * 1024 else None
        if raw is None:
            raise AuditError("Selected Python file exceeds 2 MiB")
        total_bytes += len(raw)
        if total_bytes > 16 * 1024 * 1024:
            raise AuditError("Selected source exceeds 16 MiB")
        sha = hashlib.sha256(raw).hexdigest()
        examined.append({"path": relative, "sha256": sha})
        try:
            tree = ast.parse(raw.decode("utf-8-sig"), filename=relative)
        except (SyntaxError, UnicodeError, RecursionError) as exc:
            errors.append({"path": relative, "error": type(exc).__name__})
            continue
        file_id = node("file:" + relative, relative, "module", path=relative, line=1, sha256=sha)
        def import_target(module, level=0):
            stem = module.replace('.', '/')
            parent = Path(relative).parent
            for _ in range(max(0, level-1)):
                parent = parent.parent
            candidates = {(parent/(stem+'.py')).as_posix(), (parent/stem/'__init__.py').as_posix()}
            if not level:
                candidates |= {stem+'.py', stem+'/__init__.py'}
            matches = sorted(candidates & selected)
            if len(matches) == 1:
                return node('file:'+matches[0], matches[0], 'module', path=matches[0]), 'INFERRED'
            name = '.'*level+module
            return node('import:'+name, name, 'import'), 'EXTRACTED'
        aliases = {}
        for statement in tree.body:
            if isinstance(statement, ast.Import):
                for alias in statement.names:
                    aliases[alias.asname or alias.name.split('.')[0]] = alias.name if alias.asname else alias.name.split('.')[0]
            elif isinstance(statement, ast.ImportFrom) and not statement.level:
                for alias in statement.names:
                    if alias.name != '*': aliases[alias.asname or alias.name] = (statement.module or '') + '.' + alias.name
        shadowed = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
        shadowed |= {n.arg for n in ast.walk(tree) if isinstance(n, ast.arg)}
        shadowed |= {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        aliases = {k: v for k, v in aliases.items() if k not in shadowed}
        def add_edge(source, target, relation, line, confidence="EXTRACTED"):
            eid = "py:" + digest([relative, line, source, target, relation])[:24]
            if eid not in edge_ids:
                edge_ids.add(eid)
                edges.append({"id": eid, "source": source, "target": target, "relation": relation,
                              "directed": True, "confidence": confidence,
                              "provenance": {"provider": "Python AST", "path": relative, "line": line, "sha256": sha}})
            return eid
        class Visitor(ast.NodeVisitor):
            current = file_id
            def visit_FunctionDef(self, item):
                parent = self.current
                self.current = node(f"python:{relative}:{item.lineno}:{item.name}", item.name, "function", path=relative, line=item.lineno, sha256=sha)
                add_edge(parent, self.current, "defines", item.lineno)
                self.generic_visit(item)
                self.current = parent
            visit_AsyncFunctionDef = visit_FunctionDef
            def visit_Import(self, item):
                for alias in item.names:
                    target, confidence = import_target(alias.name)
                    add_edge(self.current, target, "imports", item.lineno, confidence)
            def visit_ImportFrom(self, item):
                target, confidence = import_target(item.module or '', item.level)
                add_edge(self.current, target, "imports", item.lineno, confidence)
            def visit_Call(self, item):
                def dotted(value):
                    if isinstance(value, ast.Name): return value.id
                    if isinstance(value, ast.Attribute):
                        base = dotted(value.value)
                        return base+'.'+value.attr if base else ''
                    return ''
                expression = dotted(item.func)
                if expression:
                    head, *rest = expression.split('.')
                    resolved = '.'.join([aliases.get(head, head), *rest])
                    # The endpoint is an expression, not a claim of full symbol resolution.
                    target = node("expression:"+relative+":"+expression, resolved, "call expression", path=relative, line=item.lineno)
                    eid = add_edge(self.current, target, "calls expression", item.lineno)
                    kwargs = {k.arg: k.value for k in item.keywords}
                    rules = []
                    http = head in aliases and resolved in {"requests."+method for method in ('get','post','put','patch','delete','head','options','request')}
                    if http and (('timeout' not in kwargs and None not in kwargs) or isinstance(kwargs.get('timeout'), ast.Constant) and kwargs['timeout'].value is None):
                        rules.append(("PY-TIMEOUT", "medium", "HTTP request has no explicit timeout", "CON-03", "An unavailable peer may occupy a worker indefinitely; inspect wrappers and runtime configuration before confirming.", "Set a finite timeout and exercise a delayed/disconnected peer."))
                    if http and isinstance(kwargs.get('verify'), ast.Constant) and kwargs['verify'].value is False:
                        rules.append(("PY-TLS", "high", "TLS peer verification is explicitly disabled", "CON-06", "An untrusted peer may be accepted if this path executes; deployment exposure remains unverified.", "Restore peer verification and exercise invalid-certificate rejection."))
                    if head in aliases and resolved in {'subprocess.run','subprocess.call','subprocess.Popen','subprocess.check_call','subprocess.check_output'} and isinstance(kwargs.get('shell'), ast.Constant) and kwargs['shell'].value is True:
                        rules.append(("PY-SHELL", "high", "Command crosses a shell interpretation boundary", "CON-02", "Trace whether untrusted data can reach the command; shell=True alone does not prove injection.", "Prefer an argument list with shell disabled; verify hostile argument data remains inert."))
                    for rule, severity, title, probe, failure, action in rules:
                        findings.append({"id": rule+":"+eid, "rule": rule, "edge_id": eid, "severity": severity,
                                         "state": "candidate", "title": title, "probe": probe, "failure_scenario": failure,
                                         "improvement": action, "verification": next(p[3] for p in PROBES if p[0] == probe),
                                         "path": relative, "line": item.lineno, "sha256": sha})
                self.generic_visit(item)
        Visitor().visit(tree)
        if len(nodes) > 10000 or len(edges) > 50000:
            raise AuditError("Selected source exceeds 10000 nodes / 50000 connections; narrow the selection")
    return validate_connections({"schema": SCHEMA, "provider": "Python AST", "source_sha256": digest(examined),
        "nodes": list(nodes.values()), "edges": edges, "findings": findings,
        "coverage": {"status": "partial", "selected_files": examined, "parse_errors": errors, "scope": "Explicitly selected Python files only"},
        "limitations": ["No code was imported or executed. Calls identify syntax expressions, not fully resolved runtime callees.",
                        "Only three initial connection rules are implemented. No finding does not establish security or completeness.",
                        "Dynamic dispatch, wrappers, inter-file aliasing, generated code and non-Python files remain unassessed.",
                        "Import alias shadowing is conservatively suppressed across the file. Candidates require semantic review and authorized tests."]})


def related_paths(graph, seed, depth=2, limit=100, direction="outgoing"):
    validate_connections(graph)
    ids = {n['id'] for n in graph['nodes']}
    if seed not in ids or type(depth) is not int or not 0 <= depth <= 6 or type(limit) is not int or not 1 <= limit <= 1000 or direction not in {"outgoing", "incoming", "both"}:
        raise AuditError("Select a known seed, depth 0..6, limit 1..1000 and outgoing/incoming/both direction")
    adjacent = {nid: [] for nid in ids}
    for edge in graph['edges']:
        if direction in {"outgoing", "both"} or not edge['directed']:
            adjacent[edge['source']].append((edge['target'], edge['id']))
        if direction in {"incoming", "both"} or not edge['directed']:
            adjacent[edge['target']].append((edge['source'], edge['id']))
    paths, queue, truncated = {seed: []}, deque([seed]), False
    while queue:
        current = queue.popleft()
        for other, eid in adjacent[current]:
            if other in paths: continue
            if len(paths[current]) >= depth or len(paths) >= limit:
                truncated = True
                continue
            paths[other] = paths[current] + [eid]
            queue.append(other)
    return {"seed": seed, "direction": direction, "paths": paths, "truncated": truncated,
            "interpretation": "One bounded relationship path per node, not a proven failure propagation path. Undirected relations can be traversed both ways."}
