import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/software-process-audit/scripts"
sys.path.insert(0, str(SCRIPTS))
import audit
from graph_adapter import AuditError, Graph


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "evidence.txt").write_text("Synthetic test record: 3 checks passed.\n", encoding="utf-8")
        self.record = audit.evidence_record(self.root, "evidence.txt", "E1", "execution", "rev1")
        self.record.update(summary="Synthetic regression", locator="line 1", command="synthetic fixture",
                           exit_code=0, recorded_at="2020-01-01T00:00:00+00:00")
        self.review = {"status": "supported", "reviewer": "Fixture reviewer", "rationale": "Synthetic test assertion only", "evidence": ["E1"]}
        self.manifest = audit.new_manifest("rev1", "Synthetic fixture only")
        self.manifest["schema_version"] = 1
        self.manifest["evidence"] = [self.record]
        self.manifest["scope_review"] = copy.deepcopy(self.review)
        self.manifest["processes"] = [{"id": "P1", "kind": "runtime", "owner": "team", "input": "request", "output": "response", "graph_nodes": ["a"]}]
        self.manifest["processes"][0]["graph_nodes"] = []
        self.manifest["assessments"] = [{"id": c[0], **copy.deepcopy(self.review)} for c in audit.LEGACY_CONTROLS]

    def run_audit(self):
        return audit.evaluate(self.manifest, self.root, "rev1")

    def test_legacy_review_cannot_claim_current_standard(self):
        self.assertEqual(self.run_audit()["outcome"], "incomplete")

    def test_init_cannot_pass(self):
        result = audit.evaluate(audit.new_manifest("rev1", "empty"), self.root, "rev1")
        self.assertEqual(result["outcome"], "incomplete")
        self.assertEqual(result["status_counts"]["unverified"], len(audit.CONTROLS))

    def test_missing_control_is_unverified(self):
        self.manifest["assessments"].pop()
        self.assertEqual(self.run_audit()["controls"][-1]["status"], "unverified")

    def test_unknown_control_rejected(self):
        self.manifest["assessments"][0]["id"] = "TYPO"
        with self.assertRaises(AuditError):
            self.run_audit()

    def test_duplicate_id_rejected(self):
        self.manifest["evidence"].append(self.record)
        with self.assertRaises(AuditError):
            self.run_audit()

    def test_hash_mismatch_cannot_pass(self):
        (self.root / "evidence.txt").write_text("modified", encoding="utf-8")
        self.assertEqual(self.run_audit()["outcome"], "incomplete")

    def test_missing_evidence_file_cannot_pass(self):
        (self.root / "evidence.txt").unlink()
        self.assertIn("file_missing", self.run_audit()["evidence_validation"]["E1"]["reasons"])

    def test_current_revision_required(self):
        result = audit.evaluate(self.manifest, self.root, "rev2")
        self.assertEqual(result["status_counts"]["unverified"], len(audit.LEGACY_CONTROLS))

    def test_execution_sensitive_controls_reject_source_only(self):
        self.record["kind"] = "source"
        result = self.run_audit()
        control = next(c for c in result["controls"] if c["id"] == "VER-01")
        self.assertEqual(control["status"], "unverified")
        self.assertEqual(result["controls"][0]["status"], "supported")

    def test_failed_future_or_incomplete_execution_cannot_pass(self):
        for field, value in [("exit_code", 1), ("exit_code", False), ("recorded_at", "2099-01-01T00:00:00Z"), ("recorded_at", "2020-01-01"), ("command", "")]:
            with self.subTest(field=field, value=value):
                original = self.record[field]
                self.record[field] = value
                self.assertGreater(self.run_audit()["status_counts"].get("unverified", 0), 0)
                self.record[field] = original

    def test_reviewer_and_rationale_required_for_na(self):
        self.manifest["assessments"][0].update(status="not_applicable", rationale="")
        self.assertEqual(self.run_audit()["controls"][0]["status"], "unverified")

    def test_path_traversal_and_absolute_paths_rejected(self):
        for path in ("../outside", "..\\outside", "C:\\outside", "C:outside", "\\outside", "/outside"):
            with self.subTest(path=path), self.assertRaises(AuditError):
                audit.safe_file(self.root, path)

    def test_symlink_escape_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "secret"
            target.write_text("private", encoding="utf-8")
            link = self.root / "escape"
            try:
                link.symlink_to(target)
            except OSError:
                self.skipTest("Symlink creation unavailable on this host")
            with self.assertRaises(AuditError):
                audit.safe_file(self.root, "escape")

    def test_boundary_aspects_cannot_be_silently_omitted(self):
        self.manifest["processes"].append({"id": "P2", "kind": "runtime", "owner": "team", "input": "event", "output": "write"})
        self.manifest["boundaries"] = [{"id": "B1", "source": "P1", "target": "P2", "failure_mode": "Lost event", "reviews": {}}]
        result = self.run_audit()
        self.assertEqual(result["status_counts"]["unverified"], 5)
        self.assertEqual(len(result["review_queue"]), 5)

    def test_closed_high_risk_requires_verified_action(self):
        risk = {"id": "R1", "severity": "high", "status": "closed", "failure_mode": "Lost write", "impact": "Data loss", "targets": ["VER-01"], "owner": "team", "action": "Test recovery", "due": "2026-01-01"}
        self.manifest["risks"] = [risk]
        self.assertEqual(self.run_audit()["open_high_or_critical_risks"], ["R1"])
        risk["verification"] = copy.deepcopy(self.review)
        self.assertEqual(self.run_audit()["risks"][0]["effective_status"], "closed")
        risk["owner"] = ""
        self.assertEqual(self.run_audit()["risks"][0]["effective_status"], "open")

    def test_gap_remains_attention_even_if_risk_closed(self):
        self.manifest["assessments"][0]["status"] = "gap"
        self.assertEqual(self.run_audit()["outcome"], "needs_attention")

    def test_unknown_evidence_and_risk_targets_rejected(self):
        self.manifest["assessments"][0]["evidence"] = ["missing"]
        with self.assertRaises(AuditError):
            self.run_audit()

    def test_invalid_enum_rejected(self):
        self.manifest["assessments"][0]["status"] = "PASS"
        with self.assertRaises(AuditError):
            self.run_audit()

    def test_cli_exit_codes_and_no_overwrite(self):
        path = self.root / "audit.json"
        path.write_text(json.dumps(audit.new_manifest("rev1", "demo")), encoding="utf-8")
        args = [sys.executable, str(SCRIPTS / "audit.py"), "report", "--repo", str(self.root), "--manifest", str(path), "--revision", "rev1", "--out", str(self.root / "report"), "--strict"]
        run = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stderr)
        report = json.loads((self.root / "report/report.json").read_text())
        self.assertEqual(report["outcome"], "incomplete")
        run = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(run.returncode, 2)
        self.assertIn("already exists", run.stderr)


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = {"directed": False, "multigraph": True,
                     "graph": {"schema_version": 1, "graphify_version": "0.9.101"},
                     "nodes": [{"id": x, "label": x} for x in "abc"],
                     "links": [{"source": "a", "target": "b", "relation": "calls", "confidence": "EXTRACTED"},
                               {"source": "b", "target": "c", "relation": "references", "confidence": "INFERRED"}], "hyperedges": []}

    def graph(self):
        path = self.root / "graph.json"
        path.write_text(json.dumps(self.data), encoding="utf-8")
        return Graph(path)

    def test_actual_graphify_schema_and_weakest_path_evidence(self):
        graph = self.graph()
        result = graph.candidates("a")
        self.assertEqual(result["candidates"][-1]["path_evidence"], "INFERRED")
        self.assertEqual(graph.summary()["source_freshness"], "unverified")

    def test_undirected_is_not_runtime_direction(self):
        self.assertEqual(len(self.graph().candidates("c")["candidates"]), 3)
        self.data["directed"] = True
        self.assertEqual(len(self.graph().candidates("c")["candidates"]), 1)

    def test_bounds_are_disclosed(self):
        self.assertTrue(self.graph().candidates("a", limit=1)["capacity_truncated"])
        self.assertTrue(self.graph().candidates("a", depth=0)["depth_truncated"])
        with self.assertRaises(AuditError):
            self.graph().candidates("a", depth=7)

    def test_unknown_confidence_stays_unknown(self):
        self.data["links"][0]["confidence"] = "CUSTOM"
        self.assertEqual(self.graph().candidates("a")["candidates"][-1]["path_evidence"], "UNKNOWN")

    def test_bad_schema_duplicate_nodes_and_missing_endpoints_rejected(self):
        original = copy.deepcopy(self.data)
        mutations = [lambda d: d["graph"].update(schema_version=2),
                     lambda d: d["graph"].update(schema_version=True),
                     lambda d: d["nodes"].append({"id": "a"}),
                     lambda d: d["links"][0].update(target="missing")]
        for mutate in mutations:
            self.data = copy.deepcopy(original)
            mutate(self.data)
            with self.assertRaises(AuditError):
                self.graph()

    def test_unmapped_runtime_connection_requires_review(self):
        graph = self.graph()
        manifest = audit.new_manifest("rev1", "demo", graph)
        manifest["processes"] = [{"id": "P1", "kind": "runtime", "graph_nodes": ["a"]}, {"id": "P2", "kind": "runtime", "graph_nodes": ["b"]}]
        report = audit.evaluate(manifest, self.root, "rev1", graph)
        self.assertIn("graph_connection_requires_review:P1:P2", report["scope_issues"])
        self.assertFalse(report["graph_connections"]["candidates"][0]["review_boundary_declared"])

    def test_declared_boundary_matches_undirected_reverse(self):
        processes = {"P1": {"kind": "runtime", "graph_nodes": ["a"]}, "P2": {"kind": "runtime", "graph_nodes": ["b"]}}
        result = self.graph().boundary_candidates(processes, {"B1": {"source": "P2", "target": "P1"}})
        self.assertTrue(result["candidates"][0]["review_boundary_declared"])

    def test_graph_snapshot_mismatch_disclosed(self):
        graph = self.graph()
        manifest = audit.new_manifest("rev1", "demo", graph)
        self.data["links"].pop()
        report = audit.evaluate(manifest, self.root, "rev1", self.graph())
        self.assertIn("graph_snapshot_mismatch", report["scope_issues"])

    def test_graph_referenced_but_absent_disclosed(self):
        manifest = audit.new_manifest("rev1", "demo", self.graph())
        self.assertIn("referenced_graph_not_supplied", audit.evaluate(manifest, self.root, "rev1")["scope_issues"])

    def test_markdown_preserves_graph_direction(self):
        self.data["directed"] = True
        graph = self.graph()
        manifest = audit.new_manifest("rev1", "demo", graph)
        manifest["processes"] = [{"id": "P1", "kind": "runtime", "graph_nodes": ["a"]}, {"id": "P2", "kind": "runtime", "graph_nodes": ["b"]}]
        report = audit.evaluate(manifest, self.root, "rev1", graph)
        self.assertIn("P1 → P2", audit.markdown(report))
        self.assertNotIn("P1 ↔ P2", audit.markdown(report))


if __name__ == "__main__":
    unittest.main()
