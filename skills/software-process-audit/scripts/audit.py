"""Software process audit CLI. Standard library only; never executes target code."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PureWindowsPath
import sys

if __package__:
    from .graph_adapter import AuditError, Graph, read_json
    from .audit_standard import CHECKLISTS, EXTRA_CONTROLS, GATES, INVESTIGATION_STEPS, STANDARD_VERSION, catalog, evaluate_lifecycle, next_actions, scorecard
else:
    from graph_adapter import AuditError, Graph, read_json
    from audit_standard import CHECKLISTS, EXTRA_CONTROLS, GATES, INVESTIGATION_STEPS, STANDARD_VERSION, catalog, evaluate_lifecycle, next_actions, scorecard


# Original software criteria adapted from manufacturing audit and quality practices.
CONTROLS = [
    ("REQ-01", "requirements", "Requirements have measurable acceptance criteria", False),
    ("REQ-02", "requirements", "Critical scenarios and exclusions are explicit", False),
    ("DES-01", "design", "Components have defined inputs, outputs and ownership", False),
    ("DES-02", "design", "Cross-component contracts and failure modes are reviewed", False),
    ("SUP-01", "dependencies", "External dependencies and supplier changes are controlled", False),
    ("IMP-01", "implementation", "Changes trace to requirements and reviewed source", False),
    ("IMP-02", "implementation", "Input, authorization and state invariants are enforced", True),
    ("VER-01", "verification", "Tests exercise acceptance criteria and meaningful oracles", True),
    ("VER-02", "verification", "Negative paths and interface failures are exercised", True),
    ("VER-03", "verification", "Test environment, source revision and results are traceable", True),
    ("REL-01", "release", "Release artifacts and configuration are reproducible", True),
    ("REL-02", "release", "Migration, compatibility and rollback are verified", True),
    ("OPS-01", "operations", "Failures are observable and actionable", True),
    ("OPS-02", "operations", "Recovery and degraded operation are exercised", True),
    ("CHG-01", "change", "Change impact covers connected processes and consumers", False),
    ("RSK-01", "risk", "Failure modes, impact and missing controls are documented", False),
    ("CAP-01", "improvement", "Corrective actions have ownership and verification", False),
    ("MAP-01", "scope", "Process and interface inventory completeness is reviewed", False),
]
LEGACY_CONTROLS = CONTROLS[:]
CONTROLS += EXTRA_CONTROLS
STATES = {"supported", "partial", "gap", "unverified", "not_applicable"}
ASPECTS = {"contract": False, "failure_handling": True, "recovery": True,
           "verification": True, "observability": True}
LIMITATION = ("Evidence hashes verify artifact identity, not truth or adequacy. Supported means a named "
              "reviewer attested to evidence for this scope/revision. Graph freshness and runtime behavior "
              "are not established by a graph export. Scores describe reviewed evidence maturity, not safety certification.")


def require(condition, message):
    if not condition:
        raise AuditError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def choice(value, allowed):
    return isinstance(value, str) and value in allowed


def objects(value, name):
    require(isinstance(value, list) and all(isinstance(x, dict) for x in value), f"{name} must be an array of objects")
    return value


def indexed(value, name):
    rows = objects(value, name)
    result = {}
    for row in rows:
        key = row.get("id")
        require(nonempty(key) and key not in result, f"{name} requires unique nonempty ids")
        result[key] = row
    return result


def refs(value, name):
    require(isinstance(value, list) and all(nonempty(x) for x in value), f"{name} must be an array of ids")
    require(len(value) == len(set(value)), f"{name} has duplicate ids")
    return value


def safe_file(root, relative):
    require(nonempty(relative), "Evidence path is required")
    relative_path = Path(relative)
    windows_path = PureWindowsPath(relative)
    require(not relative_path.is_absolute() and not windows_path.drive and not windows_path.root,
            "Evidence path must be relative to the audited repository")
    require(".." not in relative_path.parts and ".." not in windows_path.parts, "Evidence path cannot traverse parents")
    resolved = (root / relative_path).resolve()
    require(resolved.is_relative_to(root), "Evidence path escapes the audited repository")
    return resolved


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def evidence_record(root, relative, eid, kind, revision):
    path = safe_file(root, relative)
    require(path.is_file(), "Evidence file does not exist")
    require(kind in {"source", "document", "execution"}, "Unknown evidence kind")
    return {"id": eid, "path": relative, "sha256": file_hash(path), "kind": kind,
            "revision": revision, "locator": "", "summary": "",
            **({"command": "", "exit_code": None, "recorded_at": ""} if kind == "execution" else {})}


def blank_review():
    return {"status": "unverified", "score": None, "reviewer": "", "rationale": "", "finding": "", "improvement": "", "owner": "", "due": "", "evidence": []}


def new_manifest(revision, scope, graph=None):
    return {"schema_version": 2, "standard_version": STANDARD_VERSION, "revision": revision, "scope": scope,
            "scope_review": blank_review(), "graph_sha256": graph.sha256 if graph else None,
            "processes": [], "boundaries": [], "evidence": [], "risks": [],
            "assessments": [{"id": row[0], "checks": [{"id": f"{row[0]}.{index}", **blank_review()} for index in range(1, 4)]} for row in CONTROLS],
            "gates": [{"id": row[0], "producer": "", "receiver": "", "input_evidence": [],
                       "output_evidence": [], "review": blank_review()} for row in GATES],
            "investigations": []}


def investigation_template(mode, iid, targets):
    require(mode in INVESTIGATION_STEPS, "Unknown investigation mode")
    require(nonempty(iid), "Investigation id required")
    refs(targets, "investigation targets")
    return {"id": iid, "mode": mode, "targets": targets,
            "steps": {name: blank_review() for name in INVESTIGATION_STEPS[mode]}}


def evaluate(manifest, root, revision, graph=None):
    require(type(manifest.get("schema_version")) is int and manifest["schema_version"] in {1, 2}, "Supported audit schema_version: 1 or 2")
    current = manifest["schema_version"] == 2
    if current:
        require(manifest.get("standard_version") == STANDARD_VERSION, "Unsupported standard_version; migrate explicitly")
    applicable_controls = CONTROLS if current else LEGACY_CONTROLS
    require(nonempty(manifest.get("scope")) and nonempty(manifest.get("revision")) and nonempty(revision), "Scope and revision are required")
    root = Path(root).resolve()
    require(root.is_dir(), "Audited repository must be a directory")
    same_revision = manifest["revision"] == revision
    evidence = indexed(manifest.get("evidence"), "evidence")
    evidence_results = {}
    for eid, item in evidence.items():
        require(choice(item.get("kind"), {"source", "document", "execution"}), f"Unknown evidence kind: {eid}")
        path = safe_file(root, item.get("path"))
        expected = item.get("sha256")
        require(isinstance(expected, str) and len(expected) == 64 and all(c in "0123456789abcdef" for c in expected), f"Invalid SHA-256: {eid}")
        reasons = []
        if not path.is_file():
            reasons.append("file_missing")
        elif file_hash(path) != expected:
            reasons.append("hash_mismatch")
        if item.get("revision") != revision:
            reasons.append("revision_mismatch")
        if not nonempty(item.get("summary")) or not nonempty(item.get("locator")):
            reasons.append("evidence_description_missing")
        execution_valid = False
        if item["kind"] == "execution":
            try:
                timestamp = datetime.fromisoformat(item.get("recorded_at", "").replace("Z", "+00:00"))
                time_valid = timestamp.tzinfo is not None and timestamp <= datetime.now(timezone.utc)
            except (ValueError, TypeError, AttributeError):
                time_valid = False
            execution_valid = (nonempty(item.get("command")) and type(item.get("exit_code")) is int
                               and item["exit_code"] == 0 and time_valid)
        evidence_results[eid] = {"valid": not reasons, "reasons": reasons,
                                 "successful_execution_record": execution_valid and not reasons}

    def assess(item, execution=False):
        require(isinstance(item, dict), "Assessment must be an object")
        for field in ("reviewer", "rationale", "finding", "improvement", "owner", "due"):
            require(isinstance(item.get(field, ""), str), "Assessment " + field + " must be text")
        claimed = item.get("status")
        require(isinstance(claimed, str) and claimed in STATES, "Unknown assessment status")
        claimed_score = item.get("score") if current else None
        if current:
            valid_score = ((claimed in {"unverified", "not_applicable"} and claimed_score is None)
                           or (type(claimed_score) is int and
                               ((claimed == "supported" and claimed_score == 4) or
                                (claimed == "partial" and 1 <= claimed_score <= 3) or
                                (claimed == "gap" and claimed_score == 0))))
            require(valid_score, "Score must match status: supported=4, partial=1..3, gap=0, unverified/not_applicable=null")
        ids = refs(item.get("evidence"), "assessment evidence")
        require(all(eid in evidence for eid in ids), "Assessment references unknown evidence")
        problems = []
        if claimed in {"supported", "partial", "gap", "not_applicable"}:
            if not nonempty(item.get("reviewer")) or not nonempty(item.get("rationale")):
                problems.append("reviewer_and_rationale_required")
            if not same_revision:
                problems.append("audit_revision_mismatch")
            if not ids or any(not evidence_results[eid]["valid"] for eid in ids):
                problems.append("current_evidence_required")
            if execution and (claimed == "supported" or (current and claimed_score == 3)) and not any(evidence_results[eid]["successful_execution_record"] for eid in ids):
                problems.append("successful_execution_evidence_required")
        return {"claimed_status": claimed, "status": "unverified" if problems else claimed,
                "claimed_score": claimed_score, "score": None if problems else claimed_score,
                "reviewer": item.get("reviewer", ""), "rationale": item.get("rationale", ""),
                "finding": item.get("finding", ""), "improvement": item.get("improvement", ""),
                "owner": item.get("owner", ""), "due": item.get("due", ""),
                "evidence": ids, "issues": problems}

    assessments = indexed(manifest.get("assessments"), "assessments")
    known = {row[0] for row in applicable_controls}
    require(not set(assessments) - known, "Unknown control id")
    controls = []
    for cid, stage, title, execution in applicable_controls:
        if not current:
            controls.append({"id": cid, "stage": stage, "title": title,
                             **assess(assessments.get(cid, blank_review()), execution)})
            continue
        checks = indexed(assessments.get(cid, {}).get("checks", []), cid + " checks")
        expected = {f"{cid}.{index}" for index in range(1, 4)}
        require(not set(checks) - expected, "Unknown checkpoint id in " + cid)
        evaluated = [{"id": f"{cid}.{index}", "question": question,
                      **assess(checks.get(f"{cid}.{index}", blank_review()), execution)}
                     for index, question in enumerate(CHECKLISTS[cid], 1)]
        active = [check for check in evaluated if check["status"] != "not_applicable"]
        score = min(check["score"] for check in active) if active and all(check["score"] is not None for check in active) else None
        status = ("not_applicable" if not active else "gap" if any(c["status"] == "gap" for c in active)
                  else "unverified" if score is None else "supported" if score == 4 else "partial")
        # A known gap stays visible even when a different checkpoint is unknown.
        controls.append({"id": cid, "stage": stage, "title": title, "status": status,
                         "score": score, "checks": evaluated,
                         "rationale": "Criterion status follows its checkpoint evidence; score is the minimum of applicable checks only when all are scored.",
                         "finding": " ".join(c["finding"] for c in evaluated if c["finding"]),
                         "improvement": " ".join(c["improvement"] for c in evaluated if c["improvement"]),
                         "issues": [issue for c in evaluated for issue in c["issues"]]})
    processes = indexed(manifest.get("processes"), "processes")
    graph_used = False
    for pid, process in processes.items():
        require(choice(process.get("kind"), {"delivery", "runtime"}), f"Unknown process kind: {pid}")
        node_ids = refs(process.get("graph_nodes", []), "process graph_nodes")
        graph_used = graph_used or bool(node_ids)
        if graph:
            require(all(nid in graph.nodes for nid in node_ids), f"Unknown graph node in process {pid}")
    boundaries = indexed(manifest.get("boundaries"), "boundaries")
    boundary_results = []
    for bid, boundary in boundaries.items():
        require(choice(boundary.get("source"), processes) and choice(boundary.get("target"), processes), f"Unknown process endpoint: {bid}")
        require(nonempty(boundary.get("failure_mode")), f"Boundary failure_mode required: {bid}")
        reviews = boundary.get("reviews", {})
        require(isinstance(reviews, dict) and not set(reviews) - set(ASPECTS), f"Unknown boundary review aspect: {bid}")
        results = {key: assess(reviews.get(key, blank_review()), execution) for key, execution in ASPECTS.items()}
        boundary_results.append({"id": bid, "source": boundary["source"], "target": boundary["target"],
                                 "failure_mode": boundary["failure_mode"], "reviews": results})
    scope = assess(manifest.get("scope_review", blank_review()))
    scope_issues = []
    if scope["status"] != "supported":
        scope_issues.append("scope_completeness_unverified")
    if not processes:
        scope_issues.append("process_inventory_empty")
    for pid, process in processes.items():
        if any(not nonempty(process.get(key)) for key in ("owner", "input", "output")):
            scope_issues.append(f"process_details_missing:{pid}")
        if len(processes) > 1 and not any(pid in (b["source"], b["target"]) for b in boundary_results):
            scope_issues.append(f"isolated_process_requires_review:{pid}")
    graph_hash = manifest.get("graph_sha256")
    require(graph_hash is None or (isinstance(graph_hash, str) and len(graph_hash) == 64 and all(c in "0123456789abcdef" for c in graph_hash)), "Invalid graph_sha256")
    if graph_hash or graph_used:
        if not graph:
            scope_issues.append("referenced_graph_not_supplied")
        elif graph_hash != graph.sha256:
            scope_issues.append("graph_snapshot_mismatch")
    elif graph:
        scope_issues.append("supplied_graph_not_bound_to_audit")
    if not same_revision:
        scope_issues.append("audit_revision_mismatch")

    connections = graph.boundary_candidates(processes, boundaries) if graph else None
    if connections:
        if not connections["mapped_runtime_nodes"]:
            scope_issues.append("graph_has_no_runtime_process_mapping")
        if connections["truncated"]:
            scope_issues.append("graph_boundary_candidates_truncated")
        for candidate in connections["candidates"]:
            if not candidate["review_boundary_declared"]:
                scope_issues.append(f"graph_connection_requires_review:{candidate['source']}:{candidate['target']}")

    risks = indexed(manifest.get("risks"), "risks")
    risk_results = []
    targets = known | {"boundary:" + bid for bid in boundaries}
    for rid, risk in risks.items():
        require(choice(risk.get("severity"), {"low", "medium", "high", "critical"}), f"Unknown risk severity: {rid}")
        require(choice(risk.get("status"), {"open", "implemented", "closed"}), f"Unknown risk status: {rid}")
        require(nonempty(risk.get("failure_mode")) and nonempty(risk.get("impact")), f"Risk failure_mode and impact required: {rid}")
        linked = refs(risk.get("targets"), "risk targets")
        require(bool(linked) and all(target in targets for target in linked), f"Unknown or missing risk target: {rid}")
        verification = assess(risk.get("verification", blank_review()), execution=True)
        action_complete = all(nonempty(risk.get(key)) for key in ("owner", "action", "due"))
        closed = risk["status"] == "closed" and verification["status"] == "supported" and action_complete
        risk_results.append({**risk, "effective_status": "closed" if closed else "open",
                             "action_complete": action_complete, "verification": verification})
    gates, investigations = (evaluate_lifecycle(manifest, controls, risk_results, assess, indexed, refs, nonempty, targets)
                             if current else ([], []))
    if not current:
        scope_issues.append("legacy_schema_no_current_scoring_or_lifecycle_review")
    elif all(check["status"] == "not_applicable" for control in controls for check in control["checks"]):
        scope_issues.append("no_applicable_checkpoint")
    for case in investigations:
        if case["state"] == "open":
            scope_issues.append("open_investigation:" + case["id"])
    # A gap requires an explicit investigation; this is separate from an open potential risk.
    if current:
        investigated = {target for case in investigations for target in case["targets"]}
        for control in controls:
            if control["status"] == "gap" and control["id"] not in investigated:
                scope_issues.append("gap_requires_investigation:" + control["id"])
        for boundary in boundary_results:
            if any(r["status"] == "gap" for r in boundary["reviews"].values()) and "boundary:" + boundary["id"] not in investigated:
                scope_issues.append("gap_requires_investigation:boundary:" + boundary["id"])
    flat = controls + [review for b in boundary_results for review in b["reviews"].values()]
    counts = dict(Counter(review["status"] for review in flat))
    open_risks = [r for r in risk_results if r["effective_status"] != "closed"]
    if counts.get("gap") or counts.get("partial") or open_risks:
        outcome = "needs_attention"
    elif scope_issues or counts.get("unverified") or any(g["state"] == "blocked" for g in gates):
        outcome = "incomplete"
    else:
        outcome = "reviewed_scope_supported"
    actions = [{"target": c["id"], "status": c["status"], "next_step": "Review evidence and document a corrective action for any confirmed gap."}
               for c in controls if c["status"] not in {"supported", "not_applicable"}]
    for boundary in boundary_results:
        for aspect, review in boundary["reviews"].items():
            if review["status"] not in {"supported", "not_applicable"}:
                actions.append({"target": "boundary:" + boundary["id"], "aspect": aspect,
                                "status": review["status"], "next_step": "Inspect the handoff contract and exercise this failure scenario."})
    high_risks = [r["id"] for r in open_risks if r["severity"] in {"high", "critical"}]
    return {"schema_version": 2, "report_template_version": "1.0", "standard_version": STANDARD_VERSION, "input_schema_version": manifest["schema_version"],
            "scope": manifest["scope"], "revision": revision,
            "outcome": outcome, "status_counts": counts, "scope_issues": scope_issues,
            "scope_review": scope, "controls": controls, "boundaries": boundary_results,
            "evidence_validation": evidence_results, "risks": risk_results, "review_queue": actions,
            "evidence_index": [{"id": eid, "path": e["path"], "locator": e.get("locator", ""),
                                "sha256": e["sha256"], "kind": e["kind"], "revision": e.get("revision"),
                                **evidence_results[eid]} for eid, e in evidence.items()],
            "open_high_or_critical_risks": high_risks,
            "gates": gates, "investigations": investigations,
            "scorecard": scorecard(controls, boundary_results, high_risks) if current else None,
            "graph": graph.summary() if graph else None, "graph_connections": connections, "limitations": LIMITATION}


def markdown(report):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ").replace("<", "&lt;").replace(">", "&gt;")
    lines = ["# Software Assurance Audit Report", "", "Template: 1.0 | Standard: " + report["standard_version"], "", f"Outcome: **{report['outcome']}**", "",
             f"Scope: {cell(report['scope'])}", f"Revision: `{cell(report['revision'])}`", "", report["limitations"], "",
             "## Scope issues", ""]
    lines += ["- " + cell(issue) for issue in report["scope_issues"]] or ["No recorded scope issues."]
    if report.get("scorecard"):
        lines += ["", "## Evidence maturity scores", "", report["scorecard"]["interpretation"], "",
                  "| Stage | Observed score % | Weighted coverage % | Achievement lower bound % | Scored / total |", "|---|---|---|---|---|"]
        for stage, stats in {"overall": report["scorecard"]["overall"], **report["scorecard"]["by_stage"]}.items():
            lines.append(f"| {stage} | {stats['observed_score_percent']} | {stats['weighted_coverage_percent']} | {stats['documented_achievement_lower_bound_percent']} | {stats['scored_items']} / {stats['total_items']} |")
    lines += ["", "## Controls", "", "| Control | Stage | Status / score | Review, finding and improvement |", "|---|---|---|---|"]
    lines += [f"| {c['id']} | {c['stage']} | {c['status']} / {c.get('score')} | {cell(c['title'])}: {cell(c['rationale'])}. Finding: {cell(c.get('finding', ''))}. Improvement: {cell(c.get('improvement', ''))}. {cell(', '.join(c['issues']))} |" for c in report["controls"]]
    lines += ["", "## Standard checkpoint results", "",
              "| ID | Checkpoint | Status | Score / 4 | Evidence IDs | Reviewer / rationale | Finding | Improvement | Owner | Due | Evidence issues |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for control in report["controls"]:
        for check in control.get("checks", []):
            lines.append("| " + " | ".join(cell(value) for value in (check["id"], check["question"], check["status"],
                check["score"] if check["score"] is not None else "unscored", ", ".join(check["evidence"]),
                check["reviewer"] + ": " + check["rationale"], check["finding"], check["improvement"], check["owner"], check["due"], ", ".join(check["issues"]))) + " |")
    lines += ["", "## Stage transition review", "", "| Gate | Transition | State | Producer / receiver | Input / output evidence | Reviewer / rationale | Blockers |", "|---|---|---|---|---|---|---|"]
    lines += [f"| {g['id']} | {g['from']} → {g['to']} | {g['state']} | {cell(g['producer'])} / {cell(g['receiver'])} | {cell(', '.join(g['input_evidence']))} / {cell(', '.join(g['output_evidence']))} | {cell(g['review']['reviewer'])}: {cell(g['review']['rationale'])} | {cell(', '.join(g['blockers']))} |" for g in report.get("gates", [])]
    lines += ["", "## Investigations", ""]
    for case in report.get("investigations", []):
        lines += [f"- {cell(case['id'])} ({case['mode']}): **{case['state']}**."]
        lines += [f"  - {step}: {r['status']} / {r['score']}. {cell(r['rationale'])}" for step, r in case["steps"].items()]
    lines += ["", "## Boundary reviews", "", "| Boundary | Aspect | Status / score | Failure scenario | Evidence | Finding | Improvement | Owner / due |", "|---|---|---|---|---|---|---|---|"]
    for b in report["boundaries"]:
        lines += [f"| {cell(b['id'])} | {key} | {review['status']} / {review['score']} | {cell(b['failure_mode'])} | {cell(', '.join(review['evidence']))} | {cell(review['finding'])} | {cell(review['improvement'])} | {cell(review['owner'])} / {cell(review['due'])} |" for key, review in b["reviews"].items()]
    lines += ["", "## Risks and corrective actions", ""]
    for r in report["risks"]:
        lines += [f"- **{cell(r['id'])} / {r['severity']} / {r['effective_status']}**: {cell(r['failure_mode'])}. Impact: {cell(r['impact'])}. Action: {cell(r.get('action', ''))}. Owner: {cell(r.get('owner', ''))}. Due: {cell(r.get('due', ''))}. Verification: {r['verification']['status']}."]
    if not report["risks"]:
        lines += ["No risks recorded. This is not evidence of absence of risk."]
    lines += ["", "## Graph evidence", "", "```json", json.dumps(report["graph"], indent=2), "```", "",
              "## Graph connections requiring review", ""]
    if report["graph_connections"]:
        lines += [report["graph_connections"]["interpretation"], ""]
        arrow = "→" if report["graph"]["directed"] else "↔"
        lines += [f"- {cell(c['source'])} {arrow} {cell(c['target'])}: {c['edge_count']} graph links; declared review boundary: {c['review_boundary_declared']}; confidence: {cell(c['confidence_counts'])}." for c in report["graph_connections"]["candidates"]]
    lines += ["",
              "## Review queue", ""]
    lines += [f"- {cell(a['target'])} {a.get('aspect', '')}: {a['status']} — {a['next_step']}" for a in report["review_queue"]]
    lines += ["", "## Evidence register", "", "| ID | Path | Locator | Kind | SHA-256 | Valid |", "|---|---|---|---|---|---|"]
    lines += ["| " + " | ".join(cell(e[key]) for key in ("id", "path", "locator", "kind", "sha256", "valid")) + " |" for e in report["evidence_index"]]
    return "\n".join(line.rstrip() for line in lines) + "\n"


def write_new(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(content)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("criteria", help="Return the complete built-in questionnaire, checkpoints and scoring rubric as JSON")
    agenda = sub.add_parser("next", help="Return evidence-based next audit actions for an AI")
    agenda.add_argument("--repo", required=True)
    agenda.add_argument("--manifest", required=True)
    agenda.add_argument("--revision", required=True)
    agenda.add_argument("--graph")
    investigation = sub.add_parser("investigation", help="Return a preventive or corrective investigation template")
    investigation.add_argument("--mode", choices=list(INVESTIGATION_STEPS), required=True)
    investigation.add_argument("--id", required=True)
    investigation.add_argument("--target", action="append", required=True)
    init = sub.add_parser("init", help="Create an unverified review manifest")
    init.add_argument("--scope", required=True)
    init.add_argument("--revision", required=True)
    init.add_argument("--out", required=True)
    init.add_argument("--graph")
    record = sub.add_parser("evidence", help="Print an evidence record skeleton; does not execute commands")
    record.add_argument("--repo", required=True)
    record.add_argument("--path", required=True)
    record.add_argument("--id", required=True)
    record.add_argument("--kind", choices=["source", "document", "execution"], required=True)
    record.add_argument("--revision", required=True)
    graph_cmd = sub.add_parser("graph", help="Inspect a Graphify export without executing the audited project")
    graph_cmd.add_argument("--graph", required=True)
    graph_cmd.add_argument("--seed")
    graph_cmd.add_argument("--depth", type=int, default=2)
    graph_cmd.add_argument("--limit", type=int, default=100)
    report = sub.add_parser("report", help="Validate review evidence and generate JSON/Markdown")
    report.add_argument("--repo", required=True)
    report.add_argument("--manifest", required=True)
    report.add_argument("--revision", required=True)
    report.add_argument("--graph")
    report.add_argument("--out", required=True)
    report.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    try:
        graph = Graph(args.graph) if getattr(args, "graph", None) else None
        if args.command == "criteria":
            print(json.dumps(catalog(CONTROLS), indent=2))
        elif args.command == "investigation":
            print(json.dumps(investigation_template(args.mode, args.id, args.target), indent=2))
        elif args.command == "init":
            require(nonempty(args.scope) and nonempty(args.revision), "Scope and revision cannot be blank")
            write_new(args.out, json.dumps(new_manifest(args.revision, args.scope, graph), indent=2) + "\n")
            print("Created unverified review manifest.")
        elif args.command == "evidence":
            require(nonempty(args.id) and nonempty(args.revision), "Evidence id and revision cannot be blank")
            print(json.dumps(evidence_record(Path(args.repo).resolve(), args.path, args.id, args.kind, args.revision), indent=2))
        elif args.command == "graph":
            result = {"graph": graph.summary()}
            if args.seed:
                result["traversal"] = graph.candidates(args.seed, args.depth, args.limit)
            print(json.dumps(result, indent=2, ensure_ascii=True))
        else:
            manifest, manifest_hash = read_json(args.manifest, max_bytes=8 * 1024 * 1024)
            result = evaluate(manifest, args.repo, args.revision, graph)
            result["manifest_sha256"] = manifest_hash
            if args.command == "next":
                print(json.dumps(next_actions(result), indent=2))
                return 0
            out = Path(args.out)
            # Refuse overwrites before creating either report.
            require(not (out / "report.json").exists() and not (out / "report.md").exists(), "Report output already exists; choose a new directory")
            write_new(out / "report.json", json.dumps(result, indent=2, ensure_ascii=True) + "\n")
            write_new(out / "report.md", markdown(result))
            print(json.dumps({"outcome": result["outcome"], "status_counts": result["status_counts"]}))
            return 1 if args.strict and result["outcome"] != "reviewed_scope_supported" else 0
        return 0
    except (AuditError, OSError) as exc:
        print(f"Audit error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
