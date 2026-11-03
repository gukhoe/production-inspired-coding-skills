import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/software-process-audit/scripts"))
import audit
from audit_standard import catalog, next_actions


class StandardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "result.txt").write_text("Synthetic fixture executed, not a real project audit.\n")
        evidence = audit.evidence_record(self.root, "result.txt", "E1", "execution", "snapshot")
        evidence.update(locator="line 1", summary="Synthetic fixture", command="synthetic fixture",
                        exit_code=0, recorded_at="2020-01-01T00:00:00Z")
        self.review = {**audit.blank_review(), "status": "supported", "score": 4,
                       "reviewer": "Fixture reviewer", "rationale": "Synthetic validation only", "evidence": ["E1"]}
        self.manifest = audit.new_manifest("snapshot", "Synthetic isolated tool tests")
        self.manifest["evidence"] = [evidence]
        self.manifest["scope_review"] = copy.deepcopy(self.review)
        self.manifest["processes"] = [{"id": "P1", "kind": "runtime", "owner": "Team", "input": "request", "output": "response"}]
        for item in self.manifest["assessments"]:
            for check in item["checks"]:
                check.update(copy.deepcopy(self.review))
        for gate in self.manifest["gates"]:
            gate.update(producer="Producer", receiver="Receiver", input_evidence=["E1"], output_evidence=["E1"], review=copy.deepcopy(self.review))

    def result(self):
        return audit.evaluate(self.manifest, self.root, "snapshot")

    def test_standalone_complete_without_graph_or_external_documents(self):
        result = self.result()
        self.assertEqual(result["outcome"], "reviewed_scope_supported")
        self.assertIsNone(result["graph"])
        self.assertEqual(result["scorecard"]["overall"]["observed_score_percent"], 100)
        self.assertEqual(result["scorecard"]["overall"]["scored_items"], 72)
        self.assertTrue(all(g["state"] == "evidence_ready" for g in result["gates"]))

    def test_one_checked_item_cannot_imply_full_coverage(self):
        self.manifest["assessments"] = [{"id": "REQ-01", "checks": [{"id": "REQ-01.1", **self.review}]}]
        result = self.result()
        overall = result["scorecard"]["overall"]
        self.assertEqual(overall["observed_score_percent"], 100)
        self.assertLess(overall["weighted_coverage_percent"], 2)
        self.assertEqual(overall["unverified_items"], 71)
        self.assertNotEqual(result["outcome"], "reviewed_scope_supported")

    def test_unknown_is_not_zero_defect(self):
        self.manifest["assessments"][0]["checks"][0].update(audit.blank_review())
        result = self.result()
        self.assertIsNone(result["controls"][0]["checks"][0]["score"])
        self.assertIsNone(result["controls"][0]["score"])
        self.assertEqual(result["scorecard"]["overall"]["observed_score_percent"], 100)
        self.assertLess(result["scorecard"]["overall"]["documented_achievement_lower_bound_percent"], 100)

    def test_partial_scoring_and_weakest_checkpoint(self):
        self.manifest["assessments"][0]["checks"][0].update(status="partial", score=2)
        self.assertEqual(self.result()["controls"][0]["score"], 2)
        self.assertEqual(self.result()["gates"][0]["state"], "blocked")

    def test_unsupported_high_score_is_rejected(self):
        self.manifest["assessments"][0]["checks"][0].update(status="partial", score=4)
        with self.assertRaises(audit.AuditError):
            self.result()

    def test_execution_sensitive_score_three_needs_execution(self):
        self.manifest["evidence"][0]["kind"] = "source"
        target = next(a for a in self.manifest["assessments"] if a["id"] == "IMP-02")
        target["checks"][0].update(status="partial", score=3)
        result = next(c for c in self.result()["controls"] if c["id"] == "IMP-02")
        self.assertEqual(result["checks"][0]["status"], "unverified")

    def test_known_gap_survives_another_unknown_checkpoint(self):
        self.manifest["assessments"][0]["checks"][0].update(status="gap", score=0)
        self.manifest["assessments"][0]["checks"][1].update(audit.blank_review())
        result = self.result()
        self.assertEqual(result["controls"][0]["status"], "gap")
        self.assertIn("gap_requires_investigation:REQ-01", result["scope_issues"])

    def test_omitted_gate_stays_blocked(self):
        self.manifest["gates"].pop()
        self.assertEqual(self.result()["gates"][-1]["state"], "blocked")

    def test_handoff_missing_or_stale_output_is_blocked(self):
        self.manifest["gates"][0]["output_evidence"] = []
        self.assertIn("output_evidence_required", self.result()["gates"][0]["blockers"])

    def test_high_risk_blocks_even_perfect_scores(self):
        self.manifest["risks"] = [{"id": "R1", "severity": "high", "status": "open", "failure_mode": "Data loss", "impact": "User data lost", "targets": ["IMP-02"], "verification": audit.blank_review()}]
        result = self.result()
        self.assertEqual(result["scorecard"]["overall"]["observed_score_percent"], 100)
        self.assertTrue(all(g["state"] == "blocked" for g in result["gates"]))

    def test_investigation_requires_every_step(self):
        case = audit.investigation_template("corrective", "I1", ["DIA-01"])
        case["steps"]["effectiveness"] = self.review
        self.manifest["investigations"] = [case]
        self.assertEqual(self.result()["investigations"][0]["state"], "open")
        for step in case["steps"]:
            case["steps"][step] = copy.deepcopy(self.review)
        self.assertEqual(self.result()["investigations"][0]["state"], "evidence_supported")

    def test_template_keeps_all_checkpoint_rows_and_order(self):
        self.manifest["assessments"] = []
        result = self.result()
        rows = [line for line in audit.markdown(result).splitlines() if line.startswith("| ") and any(line.startswith("| " + cid + ".") for cid, *_ in audit.CONTROLS)]
        self.assertEqual(len(rows), 72)
        self.assertTrue(rows[0].startswith("| REQ-01.1 |"))
        self.assertTrue(rows[-1].startswith("| CAP-02.3 |"))
        self.assertEqual(audit.markdown(result), audit.markdown(copy.deepcopy(result)))

    def test_report_contains_evidence_and_action_fields(self):
        check = self.manifest["assessments"][0]["checks"][0]
        check.update(status="partial", score=2, finding="Missing criterion", improvement="Define timing limit", owner="Test owner", due="2026-11-10")
        rendered = audit.markdown(self.result())
        for value in ("Missing criterion", "Define timing limit", "Test owner", "2026-11-10", "result.txt", self.manifest["evidence"][0]["sha256"]):
            self.assertIn(value, rendered)

    def test_next_actions_and_catalog_work_without_graph(self):
        self.manifest["assessments"][0]["checks"][0].update(audit.blank_review())
        agenda = next_actions(self.result())
        self.assertIn("REQ-01.1", [task["target"] for task in agenda["tasks"]])
        criteria = catalog(audit.CONTROLS)
        self.assertEqual(len(criteria["controls"]), 24)
        self.assertEqual(sum(len(c["checkpoints"]) for c in criteria["controls"]), 72)
        self.assertEqual(criteria["required_external_tools"], [])

    def test_justified_exclusions_are_separately_counted(self):
        check = self.manifest["assessments"][0]["checks"][0]
        check.update(status="not_applicable", score=None)
        counts = self.result()["scorecard"]["overall"]
        self.assertEqual(counts["not_applicable_items"], 1)
        self.assertEqual(counts["scored_items"], 71)

    def test_all_excluded_never_produces_a_perfect_score(self):
        for item in self.manifest["assessments"]:
            for check in item["checks"]:
                check.update(status="not_applicable", score=None)
        result = self.result()
        self.assertIsNone(result["scorecard"]["overall"]["observed_score_percent"])
        self.assertIsNone(result["scorecard"]["overall"]["weighted_coverage_percent"])
        self.assertTrue(all(g["state"] == "blocked" for g in result["gates"]))
        for gate in self.manifest["gates"]:
            gate["review"].update(status="not_applicable", score=None)
        self.assertEqual(self.result()["outcome"], "incomplete")

    def test_malformed_finding_is_an_input_error(self):
        self.manifest["assessments"][0]["checks"][0]["finding"] = ["not text"]
        with self.assertRaises(audit.AuditError):
            self.result()


if __name__ == "__main__":
    unittest.main()
