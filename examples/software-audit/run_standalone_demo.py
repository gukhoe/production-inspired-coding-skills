"""Run an intentionally defective toy program and audit it without external tools.

This is a demonstrator of evidence/report behavior, not a production audit.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/software-process-audit/scripts"))
import audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    program = '''def apply(balance, amount, event_id, seen):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    # Intentional demo defect: duplicate events are not checked.
    return balance + amount

if __name__ == "__main__":
    seen = set()
    first = apply(100, 10, "event-1", seen)
    second = apply(first, 10, "event-1", seen)
    print(f"normal: observed={first}, expected=110")
    print(f"duplicate: observed={second}, expected=110")
    raise SystemExit(0 if first == 110 and second == 110 else 1)
'''
    (out / "target.py").write_text(program, encoding="utf-8")
    (out / "requirements.txt").write_text("Synthetic demo only. Positive events add their amount once. Repeating the same event ID must preserve the balance. Invalid amounts must be rejected before mutation.\n", encoding="utf-8")
    revision = audit.file_hash(out / "target.py")
    command = [sys.executable, "target.py"]
    timestamp = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=out, capture_output=True, text=True, timeout=10)
    (out / "run.txt").write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode != 1 or "duplicate: observed=120, expected=110" not in result.stdout:
        raise AssertionError("Demo must reproduce the deliberate defect")
    manifest = audit.new_manifest(revision, "Synthetic standalone demonstration: one balance function; no Graphify or prior process documents")
    for eid, path, kind in [("E1", "requirements.txt", "document"), ("E2", "target.py", "source"), ("E3", "run.txt", "execution")]:
        item = audit.evidence_record(out, path, eid, kind, revision)
        item.update(locator="Entire small demo file", summary="Synthetic example evidence: " + path)
        if kind == "execution":
            item.update(command=json.dumps(command), exit_code=result.returncode, recorded_at=timestamp)
        manifest["evidence"].append(item)
    manifest["processes"] = [{"id": "balance-update", "kind": "runtime", "owner": "Demo maintainer", "input": "Balance and event", "output": "New balance"}]
    def review(status, score, evidence, rationale, finding="", improvement=""):
        return {**audit.blank_review(), "status": status, "score": score, "evidence": evidence,
                "reviewer": "Demonstration runner", "rationale": rationale, "finding": finding,
                "improvement": improvement, "owner": "Demo maintainer", "due": "Unscheduled demo"}
    manifest["scope_review"] = review("supported", 4, ["E1", "E2"], "Only the declared tiny example is in scope.")
    for criterion in manifest["assessments"]:
        if criterion["id"] == "REQ-01":
            for check in criterion["checks"]:
                check.update(review("supported", 4, ["E1", "E3"], "Expected normal and duplicate outcomes are explicit and tied to the executed scenario."))
        elif criterion["id"] == "PRE-01":
            criterion["checks"][0].update(review("partial", 2, ["E1", "E2"], "Invalid amount guard exists; duplicate prevention is incomplete."))
            criterion["checks"][1].update(review("gap", 0, ["E2", "E3"], "The actual mutation path ignores event_id and seen.", "Duplicate event increases balance twice.", "Add event admission/idempotency control before mutation."))
            criterion["checks"][2].update(review("gap", 0, ["E3"], "The duplicate scenario failed with 120 instead of 110.", "The prevention challenge is not satisfied.", "Replay this failure after correction and include adjacent cases."))
    case = audit.investigation_template("corrective", "I1", ["PRE-01"])
    case["steps"]["problem_definition"] = review("supported", 4, ["E1", "E3"], "Expected 110, observed 120 after the same event twice.")
    # A failed run proves the gap; successful verification of a full reproduction
    # protocol and root-cause/correction steps remain unverified in this small demo.
    manifest["investigations"] = [case]
    report = audit.evaluate(manifest, out, revision)
    if report["outcome"] != "needs_attention":
        raise AssertionError("A reproduced defect must not pass the audit")
    (out / "review.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (out / "report.md").write_text(audit.markdown(report), encoding="utf-8")
    print(json.dumps({"expected_target_exit": result.returncode, "audit_outcome": report["outcome"], "scores": report["scorecard"]["overall"]}))


if __name__ == "__main__":
    main()
