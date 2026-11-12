"""Real stdio MCP tests against the installed package, without Graphify or skills."""
import asyncio
import copy
import hashlib
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
                self.assertEqual(names, {"audit_criteria", "audit_initialize", "audit_inventory", "audit_read_file", "audit_evidence", "audit_investigation", "audit_evaluate", "audit_graph_candidates", "audit_scan_connections", "audit_import_connections", "audit_connection_path", "audit_visualize"})

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
                for name in ('.env', '.ENV.local', 'key.pem', '.git/config', '.aws/credentials', '.env.py'):
                    secret_path = root / name
                    secret_path.parent.mkdir(parents=True, exist_ok=True)
                    secret_path.write_text('SECRET=synthetic-test-value')
                    for tool, args in [('audit_read_file', {'path': name}),
                                       ('audit_evidence', {'path': name, 'evidence_id': 'secret', 'kind': 'source', 'revision': 'fixture'}),
                                       ('audit_import_connections', {'path': name, 'format': 'native'})]:
                        denied = await client.call_tool(tool, args)
                        self.assertTrue(denied.is_error, tool+' must deny '+name)
                denied = await client.call_tool('audit_scan_connections', {'paths': ['.env.py']})
                self.assertTrue(denied.is_error)
                evidence = await call("audit_evidence", {"path": "source.py", "evidence_id": "E1", "kind": "source", "revision": "fixture"})
                self.assertEqual(evidence["sha256"], source["sha256"])
                blocked_manifest = copy.deepcopy(manifest)
                blocked_record = {**evidence, 'path': '.env', 'sha256': hashlib.sha256((root/'.env').read_bytes()).hexdigest(),
                                  'summary': 'Synthetic protected fixture', 'locator':'line 1'}
                blocked_manifest['evidence'] = [blocked_record]
                for tool in ('audit_evaluate', 'audit_visualize'):
                    denied = await client.call_tool(tool, {'manifest': blocked_manifest, 'revision':'fixture'})
                    self.assertTrue(denied.is_error, tool+' must protect nested evidence')
                (root/'.env').write_text(json.dumps(manifest))
                for tool in ('audit_evaluate', 'audit_visualize'):
                    denied = await client.call_tool(tool, {'manifest_path':'.env', 'revision':'fixture'})
                    self.assertTrue(denied.is_error, tool+' must protect manifest input')
                case = await call("audit_investigation", {"mode": "corrective", "investigation_id": "I1", "targets": ["DIA-01"]})
                self.assertIn("root_cause", case["steps"])
                evaluated = await call("audit_evaluate", {"manifest": manifest, "revision": "fixture"})
                self.assertEqual(evaluated['report']['report_template_version'], '1.1')
                dimensions = evaluated['report']['scorecard']['dimensions']
                self.assertEqual(dimensions['policy_id'], 'assurance-dimensions/1.0')
                self.assertEqual(dimensions['documentation']['overall']['score_percent'], 0)
                self.assertEqual(dimensions['execution']['overall']['score_percent'], 0)
                self.assertIsNone(dimensions['risk_resolution']['score_percent'])
                (root/'manifest.json').write_text(json.dumps(manifest))
                via_path = await call('audit_evaluate', {'manifest_path': 'manifest.json', 'revision': 'fixture'})
                self.assertEqual(via_path['report'], evaluated['report'])
                ambiguous = await client.call_tool('audit_evaluate', {'manifest': manifest, 'manifest_path': 'manifest.json', 'revision': 'fixture'})
                self.assertTrue(ambiguous.is_error)
                self.assertEqual(evaluated["report"]["outcome"], "incomplete")
                self.assertEqual(evaluated["report"]["scorecard"]["overall"]["unverified_items"], 72)
                self.assertIn("| REQ-01.1 |", evaluated["report_markdown"])
                self.assertIn("| CAP-02.3 |", evaluated["report_markdown"])
                self.assertIn("# Software Assurance Audit", evaluated["report_markdown"])
                self.assertTrue(evaluated["next_actions"]["tasks"])
                scanned = await call("audit_scan_connections", {"paths": ["source.py"]})
                self.assertEqual(scanned["connections"]["provider"], "Python AST")
                self.assertEqual(len(scanned["probes"]), 8)
                # The host saves tool data; the MCP service itself performs no writes.
                (root / "connections.json").write_text(json.dumps(scanned["connections"]))
                imported = await call("audit_import_connections", {"path": "connections.json", "format": "native"})
                node = imported["connections"]["nodes"][0]["id"]
                traced = await call("audit_connection_path", {"path": "connections.json", "seed": node})
                self.assertIn(node, traced["paths"])
                visual = await call("audit_visualize", {"manifest": manifest, "revision": "fixture", "connections_path": "connections.json"})
                visual_path = await call('audit_visualize', {'manifest_path':'manifest.json', 'revision':'fixture', 'connections_path':'connections.json'})
                self.assertEqual(visual['view'], visual_path['view'])
                self.assertEqual(visual["view"]["outcome"], "incomplete")
                self.assertIn("Connection risk review", visual["report_html"])
                self.assertEqual(visual["view"]["scorecard"], evaluated["report"]["scorecard"])
                (root / "connections.json").unlink()
                escaped = await client.call_tool("audit_read_file", {"path": "../outside.txt"})
                self.assertTrue(escaped.is_error)
                malformed = await client.call_tool("audit_evaluate", {"manifest": {"schema_version": 999}, "revision": "fixture"})
                self.assertTrue(malformed.is_error)
                missing_graph = await client.call_tool("audit_graph_candidates", {"graph_path": "missing.json", "seed": "x"})
                self.assertTrue(missing_graph.is_error)
                (root/'manifest.json').unlink()
                for name in ('.env', '.ENV.local', 'key.pem', '.git/config', '.aws/credentials', '.env.py'):
                    (root/name).unlink()
                (root/'.git').rmdir()
                (root/'.aws').rmdir()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.py").write_text("def f():\n    return 1\n", encoding="utf-8")
            before = sorted(p.name for p in root.iterdir())
            asyncio.run(run(root))
            self.assertEqual(before, sorted(p.name for p in root.iterdir()))


if __name__ == "__main__":
    unittest.main()
