"""Real stdio MCP tests against the installed package, without Graphify or skills."""
import asyncio
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

HAS_MCP = importlib.util.find_spec("mcp") is not None and importlib.util.find_spec("software_assurance_auditor") is not None


@unittest.skipUnless(HAS_MCP, 'Install the project with [mcp] to run real stdio integration tests')
class MCPIntegrationTests(unittest.TestCase):
    def test_standalone_tools_and_fixed_report_over_stdio(self):
        from mcp import Client, StdioServerParameters

        async def run(root):
            params = StdioServerParameters(command=sys.executable, args=["-m", "software_assurance_auditor.mcp_server", "--repo-root", str(root)], cwd=str(root))
            async with Client(params) as client:
                listed = await client.list_tools()
                tools = listed if isinstance(listed, list) else listed.tools
                names = {tool.name for tool in tools}
                self.assertEqual(names, {"audit_criteria", "audit_initialize", "audit_inventory", "audit_read_file", "audit_evidence", "audit_investigation", "audit_evaluate", "audit_graph_candidates"})

                async def call(name, args):
                    result = await client.call_tool(name, args)
                    self.assertFalse(result.is_error, str(result))
                    value = result.structured_content
                    # SDK versions may wrap non-object results; all our tools return objects.
                    return value.get("result", value) if isinstance(value, dict) else value

                criteria = await call("audit_criteria", {})
                self.assertEqual(criteria["report_language"], "en")
                self.assertIn("English", criteria["narrative_policy"])
                self.assertEqual(len(criteria["controls"]), 24)
                self.assertEqual(sum(len(c["checkpoints"]) for c in criteria["controls"]), 72)
                manifest = await call("audit_initialize", {"scope": "Isolated empty project", "revision": "fixture"})
                inventory = await call("audit_inventory", {})
                self.assertIn("source.py", inventory["files"])
                source = await call("audit_read_file", {"path": "source.py"})
                self.assertIn("return 1", source["text"])
                evidence = await call("audit_evidence", {"path": "source.py", "evidence_id": "E1", "kind": "source", "revision": "fixture"})
                self.assertEqual(evidence["sha256"], source["sha256"])
                case = await call("audit_investigation", {"mode": "corrective", "investigation_id": "I1", "targets": ["DIA-01"]})
                self.assertIn("root_cause", case["steps"])
                evaluated = await call("audit_evaluate", {"manifest": manifest, "revision": "fixture"})
                self.assertEqual(evaluated["report"]["outcome"], "incomplete")
                self.assertEqual(evaluated["report"]["scorecard"]["overall"]["unverified_items"], 72)
                self.assertIn("| REQ-01.1 |", evaluated["report_markdown"])
                self.assertIn("| CAP-02.3 |", evaluated["report_markdown"])
                self.assertIn("# Software Assurance Audit", evaluated["report_markdown"])
                self.assertTrue(evaluated["next_actions"]["tasks"])
                escaped = await client.call_tool("audit_read_file", {"path": "../outside.txt"})
                self.assertTrue(escaped.is_error)
                malformed = await client.call_tool("audit_evaluate", {"manifest": {"schema_version": 999}, "revision": "fixture"})
                self.assertTrue(malformed.is_error)
                missing_graph = await client.call_tool("audit_graph_candidates", {"graph_path": "missing.json", "seed": "x"})
                self.assertTrue(missing_graph.is_error)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.py").write_text("def f():\n    return 1\n", encoding="utf-8")
            before = sorted(p.name for p in root.iterdir())
            asyncio.run(run(root))
            self.assertEqual(before, sorted(p.name for p in root.iterdir()))


if __name__ == "__main__":
    unittest.main()
