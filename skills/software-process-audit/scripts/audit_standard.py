"""Built-in Software Assurance Auditor criteria and lifecycle review rules."""
if __package__:
    from .graph_adapter import AuditError
else:
    from graph_adapter import AuditError

STANDARD_VERSION = "0.2.0"
EXTRA_CONTROLS = [
    ("PRE-01", "prevention", "Invalid actions are prevented before harmful state changes", True),
    ("PRE-02", "prevention", "Detected failures stop or contain affected work safely", True),
    ("GAT-01", "handoff", "Stage transitions have reviewed entry and exit evidence", False),
    ("DIA-01", "diagnosis", "Failure reproduction distinguishes observations from hypotheses", True),
    ("DIA-02", "diagnosis", "Root-cause claims survive discriminating counterexamples", True),
    ("CAP-02", "improvement", "Corrections prevent recurrence without breaking adjacent behavior", True),
]
GATES = [
    ("G1", "requirements", "design", ["REQ-01", "REQ-02", "RSK-01"]),
    ("G2", "design", "implementation", ["DES-01", "DES-02", "SUP-01", "GAT-01"]),
    ("G3", "implementation", "verification", ["IMP-01", "IMP-02", "PRE-01", "CHG-01"]),
    ("G4", "verification", "release", ["VER-01", "VER-02", "VER-03", "PRE-02", "REL-01", "REL-02"]),
    ("G5", "release", "operations", ["OPS-01", "OPS-02", "CAP-01", "CAP-02"]),
]
INVESTIGATION_STEPS = {
    "preventive": {"failure_scenario": False, "prevention_design": False,
                   "challenge_test": True, "effectiveness": True},
    "corrective": {"problem_definition": False, "containment": False,
                   "reproduction": True, "root_cause": True,
                   "correction": False, "effectiveness": True},
}
PROBES = {
    "requirements": "Trace one promised outcome to an observable acceptance criterion; identify an excluded and an adverse scenario.",
    "design": "Follow one input across a boundary; check its owner, output contract, stale data and failure path.",
    "dependencies": "Inspect a version/configuration change or unavailable dependency and the compatibility decision.",
    "implementation": "Try invalid, duplicate and unauthorized input at the actual state-changing boundary.",
    "verification": "Challenge the test oracle with a deliberately wrong result; compare failing baseline and correction where available.",
    "release": "Exercise interrupted deployment, version mismatch and rollback in an isolated environment.",
    "operations": "Exercise a timeout or stale observation; check detection, bounded recovery and the next useful action.",
    "change": "Trace upstream callers, downstream consumers and shared state from current source; test an adjacent workflow.",
    "risk": "Describe a credible failure, propagation and user impact before accepting a control as sufficient.",
    "improvement": "Replay the original adverse condition and an adjacent non-regression case; retain unresolved effects.",
    "scope": "Compare declared processes and interfaces to source and intended workflows; record unmapped areas.",
    "prevention": "Challenge the admission guard before mutation, then the stop/containment path; verify data and other users remain protected.",
    "handoff": "Verify that the receiving stage can use the identified outputs and that acceptance evidence matches this revision.",
    "diagnosis": "State competing causes and a test that separates them; preserve observations that disprove the favored cause.",
}

# Fixed initial policy weights, not empirically calibrated incident probabilities.
WEIGHTS = {"IMP-02": 3, "PRE-01": 3, "PRE-02": 3, "VER-02": 3,
           "REL-02": 3, "OPS-02": 3, "CAP-02": 3}
CHECKLISTS = {
    "REQ-01": ["Identify the user-visible outcome", "Define observable acceptance limits before implementation", "Trace each selected requirement to a verification scenario"],
    "REQ-02": ["State critical use and misuse scenarios", "Record exclusions and affected users", "Define unacceptable data/state outcomes"],
    "DES-01": ["Name inputs and outputs", "Identify accountable owner and consumer", "Define state and lifetime invariants"],
    "DES-02": ["Review both sides of each selected interface", "Specify error, timeout and cancellation behavior", "Trace shared-state and version compatibility assumptions"],
    "SUP-01": ["Identify external services and version/configuration dependencies", "Review change and outage handling", "Record provenance and replacement/recovery strategy"],
    "IMP-01": ["Link source changes to acceptance requirements", "Review changed and shared paths", "Preserve source identity and review rationale"],
    "IMP-02": ["Reject invalid or unauthorized actions before mutation", "Handle duplicate/stale observations", "Test protected data and other-user isolation"],
    "VER-01": ["Use observable assertions tied to requirements", "Show the oracle rejects an incorrect result", "Explain fixture limitations and untested behaviors"],
    "VER-02": ["Exercise malformed/failed inputs", "Exercise delay, cancellation and partial completion", "Verify the downstream state after failure and recovery"],
    "VER-03": ["Bind results to source and environment", "Retain exact commands and raw outputs", "Distinguish fresh runs from historical claims"],
    "REL-01": ["Identify reproducible build inputs and output artifacts", "Verify configuration and dependency provenance", "Distinguish candidate from installed and live evidence"],
    "REL-02": ["Test backward/forward compatibility as applicable", "Interrupt a migration or installation safely", "Verify rollback restores a consistent usable state"],
    "OPS-01": ["Detect failed and stalled work", "Provide actionable diagnostics without sensitive leakage", "Distinguish healthy service response from useful workflow progress"],
    "OPS-02": ["Bound recovery and retries", "Test degraded mode and cancellation", "Verify progress resumes without harming adjacent users"],
    "CHG-01": ["Trace callers and downstream consumers", "Check shared data/configuration/process boundaries", "Exercise an affected neighboring workflow"],
    "RSK-01": ["State failure and user impact", "Identify prevention, detection and containment gaps", "Preserve unknown likelihood and unresolved severe effects"],
    "CAP-01": ["Assign corrective action owner and due date", "Link action to a specific finding", "Require effectiveness evidence before closure"],
    "MAP-01": ["Map intended workflows and development stages", "Compare the map to actual source and interfaces", "Explain sampling, missing links and exclusions"],
    "PRE-01": ["Identify a harmful action before it occurs", "Place a fail-safe admission guard at the actual boundary", "Challenge the guard with invalid, stale or competing inputs"],
    "PRE-02": ["Define a stop/containment trigger", "Preserve recoverable state and isolate affected work", "Exercise safe stop and controlled resumption"],
    "GAT-01": ["Record stage entry/exit criteria", "Identify versioned handoff inputs and outputs", "Have the receiving owner review unresolved exceptions"],
    "DIA-01": ["Define expected versus observed behavior", "Reproduce or explicitly retain reproduction as unknown", "Separate observations from competing explanations"],
    "DIA-02": ["Propose a cause and a falsifying experiment", "Compare affected and unaffected conditions", "Confirm the cause through the actual failing path"],
    "CAP-02": ["Replay the original failure condition after correction", "Exercise recurrence prevention and adjacent regressions", "Update the durable control/test and preserve residual risk"],
}
RUBRIC = {
    "0": "A current, evidenced failure or missing required control; status gap.",
    "1": "Intent/design is documented, implementation or execution is not established; status partial.",
    "2": "Control is implemented with limited/static evidence; required scenarios remain incomplete; status partial.",
    "3": "Relevant normal scenarios are verified, but adverse/recovery or adjacent checks remain incomplete; status partial. Execution-sensitive controls require a successful run.",
    "4": "All checkpoints applicable to this criterion are reviewed and supported, including adverse/recurrence evidence where relevant; status supported.",
    "unverified": "No defensible current score. Excluded from observed score, included in coverage denominator.",
    "not_applicable": "Evidence-backed scope exclusion. Excluded from scoring denominators and counted separately.",
}


def catalog(controls):
    return {"name": "Software Assurance Auditor", "standard_version": STANDARD_VERSION,
            "manifest_schema_version": 2,
            "report_language": "en",
            "narrative_policy": "Write scope, assessments, findings, improvements and summaries in English. Preserve evidence paths, identifiers, hashes and original quotations; explain non-English quotations in English. The renderer preserves supplied narrative and does not translate it.",
            "purpose": "An initial translation of manufacturing audit and quality practices into software assurance criteria for AI-assisted review.",
            "required_external_tools": [],
            "scoring_rubric": RUBRIC,
            "controls": [{"id": cid, "stage": stage, "criterion": title,
                          "audit_question": "What current evidence establishes that " + title[0].lower() + title[1:] + "?",
                          "checkpoints": [{"id": f"{cid}.{index}", "question": question} for index, question in enumerate(CHECKLISTS[cid], 1)], "weight": WEIGHTS.get(cid, 2),
                          "challenge": PROBES[stage], "successful_execution_required_for_support": execution}
                         for cid, stage, title, execution in controls],
            "stage_gates": [{"id": gid, "from": source, "to": target, "required_controls": required}
                            for gid, source, target, required in GATES],
            "investigation_steps": INVESTIGATION_STEPS,
            "agent_contract": "Inspect evidence content, record a reasoned assessment, run authorized discriminating checks, then use report/next to retain open work. Tool outcomes are not authorization to deploy."}


def evaluate_lifecycle(manifest, controls, risks, assess, indexed, refs, nonempty, targets):
    """Assess handoffs and investigations using the same evidence validator as controls."""
    by_control = {row["id"]: row for row in controls}
    gates = indexed(manifest.get("gates", []), "gates")
    known = {gate[0] for gate in GATES}
    if set(gates) - known:
        raise AuditError("Unknown stage gate id")
    gate_results = []
    high_risks = [risk["id"] for risk in risks if risk["effective_status"] != "closed" and risk["severity"] in {"high", "critical"}]
    default = {"status": "unverified", "score": None, "reviewer": "", "rationale": "", "evidence": []}
    for gid, source, target, required in GATES:
        row = gates.get(gid, {})
        review = assess(row.get("review", default))
        blockers = []
        if review["status"] == "not_applicable":
            state = "not_applicable"
        else:
            if review["status"] != "supported":
                blockers.append("handoff_review_not_supported")
            if not nonempty(row.get("producer")) or not nonempty(row.get("receiver")):
                blockers.append("producer_and_receiver_required")
            for field in ("input_evidence", "output_evidence"):
                evidence_ids = refs(row.get(field, []), field)
                if not evidence_ids:
                    blockers.append(field + "_required")
                else:
                    # Validate every handoff artifact, including its revision and locator.
                    checked = assess({**row.get("review", default), "status": "supported", "score": 4, "evidence": evidence_ids})
                    if checked["status"] != "supported":
                        blockers.append(field + "_invalid")
            for cid in required:
                if by_control[cid]["status"] not in {"supported", "not_applicable"}:
                    blockers.append("control:" + cid)
            if not any(by_control[cid]["status"] == "supported" for cid in required):
                blockers.append("no_applicable_supported_control")
            blockers += ["open_high_risk:" + rid for rid in high_risks]
            state = "blocked" if blockers else "evidence_ready"
        gate_results.append({"id": gid, "from": source, "to": target,
                             "producer": row.get("producer", ""), "receiver": row.get("receiver", ""),
                             "input_evidence": row.get("input_evidence", []), "output_evidence": row.get("output_evidence", []),
                             "state": state, "blockers": blockers, "review": review})

    investigations = indexed(manifest.get("investigations", []), "investigations")
    case_results = []
    for iid, case in investigations.items():
        mode = case.get("mode")
        if not isinstance(mode, str) or mode not in INVESTIGATION_STEPS:
            raise AuditError("Investigation mode must be preventive or corrective")
        linked = refs(case.get("targets", []), "investigation targets")
        if not linked or any(target not in targets for target in linked):
            raise AuditError("Investigation requires known control/boundary targets")
        steps = case.get("steps", {})
        if not isinstance(steps, dict) or set(steps) - set(INVESTIGATION_STEPS[mode]):
            raise AuditError("Unknown investigation step")
        reviews = {name: assess(steps.get(name, default), execution)
                   for name, execution in INVESTIGATION_STEPS[mode].items()}
        # No reproduction/effectiveness waiver can silently finish an investigation.
        complete = all(review["status"] == "supported" for review in reviews.values())
        case_results.append({"id": iid, "mode": mode, "targets": linked,
                             "state": "evidence_supported" if complete else "open", "steps": reviews})
    return gate_results, case_results


def scorecard(controls, boundaries, open_high_risks):
    rows = [{"id": check["id"], "stage": c["stage"], "weight": WEIGHTS.get(c["id"], 2),
             "score": check.get("score"), "status": check["status"]}
            for c in controls for check in c.get("checks", [c])]
    rows += [{"id": "boundary:" + b["id"] + ":" + aspect, "stage": "interfaces", "weight": 2,
              "score": review.get("score"), "status": review["status"]}
             for b in boundaries for aspect, review in b["reviews"].items()]
    def summarize(items):
        applicable = [r for r in items if r["status"] != "not_applicable"]
        scored = [r for r in applicable if r["score"] is not None]
        denominator = sum(r["weight"] * 4 for r in applicable)
        observed_max = sum(r["weight"] * 4 for r in scored)
        earned = sum(r["weight"] * r["score"] for r in scored)
        return {"observed_score_percent": round(100 * earned / observed_max, 2) if observed_max else None,
                "weighted_coverage_percent": round(100 * observed_max / denominator, 2) if denominator else None,
                "documented_achievement_lower_bound_percent": round(100 * earned / denominator, 2) if denominator else None,
                "total_items": len(items), "scored_items": len(scored),
                "unverified_items": len(applicable) - len(scored), "not_applicable_items": len(items) - len(applicable)}
    return {"rubric": RUBRIC, "weight_policy": "Initial fixed policy: listed high-impact controls weight 3; other controls and boundary aspects weight 2. Not calibrated defect probabilities.",
            "overall": summarize(rows), "by_stage": {stage: summarize([r for r in rows if r["stage"] == stage]) for stage in sorted({r["stage"] for r in rows})},
            "open_high_or_critical_risks": open_high_risks,
            "interpretation": "Scores describe reviewed evidence maturity, not failure probability or release authorization. Unknowns lower coverage; their zero contribution to the achievement lower bound is not a defect verdict."}


def next_actions(report):
    """Machine-readable agenda for an AI; never run suggested actions automatically."""
    tasks = [{"type": "scope", "target": issue, "action": "Resolve or document this scope/evidence issue before making a completeness claim."}
             for issue in report["scope_issues"]]
    for control in report["controls"]:
        for check in control.get("checks", [control]):
            if check["status"] not in {"supported", "not_applicable"}:
                tasks.append({"type": "checkpoint", "target": check["id"], "status": check["status"],
                              "question": check.get("question", control["title"]), "action": PROBES[control["stage"]]})
    for boundary in report["boundaries"]:
        for aspect, review in boundary["reviews"].items():
            if review["status"] not in {"supported", "not_applicable"}:
                tasks.append({"type": "boundary", "target": boundary["id"], "aspect": aspect,
                              "action": "Inspect both sides and exercise " + aspect + " against: " + boundary["failure_mode"]})
    for risk in report["risks"]:
        if risk["effective_status"] != "closed":
            tasks.append({"type": "risk", "target": risk["id"], "severity": risk["severity"],
                          "action": risk.get("action") or "Define an owned corrective/preventive action and a discriminating verification scenario."})
    for gate in report.get("gates", []):
        if gate["state"] == "blocked":
            tasks.append({"type": "gate", "target": gate["id"], "action": "Resolve handoff blockers; retain stage-transition evidence.", "blockers": gate["blockers"]})
    for case in report.get("investigations", []):
        for step, review in case["steps"].items():
            if review["status"] != "supported":
                tasks.append({"type": "investigation", "target": case["id"], "step": step,
                              "action": "Investigate and substantiate this step; distinguish observations from hypotheses and retain unsuccessful attempts."})
    return {"standard_version": STANDARD_VERSION, "outcome": report["outcome"],
            "tasks": tasks, "execution_policy": "Suggested review work only. Execute tests and changes within existing user authorization."}
