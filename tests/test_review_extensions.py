import json
import copy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/software-process-audit/scripts'))
import audit
from connection_audit import import_connections, scan_python
from witness import record
from skill_records import register
from access_policy import project_file


class ExtensionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_sarif_keeps_suppression_location_and_unlocated_diagnostics(self):
        sarif = {'version': '2.1.0', 'runs': [{'tool': {'driver': {'name': 'fixture', 'rules': []}}, 'artifacts': [{'location': {'uri': 'a.py'}}], 'results': [
            {'ruleId': 'B001', 'message': {'text': '</script>candidate'}, 'level': 'error', 'suppressions': [{'kind': 'inSource'}],
             'locations': [{'physicalLocation': {'artifactLocation': {'index': 0}, 'region': {'startLine': 4}}}]},
            {'message': {'text': 'unlocated'}}]}]}
        path = self.root/'input.sarif';path.write_text(json.dumps(sarif))
        result = import_connections(path, 'sarif')
        self.assertEqual(len(result['findings']), 2)
        self.assertEqual(result['findings'][0]['path'], 'a.py')
        self.assertEqual(result['findings'][0]['state'], 'candidate')
        self.assertFalse(result['edges'][0]['directed'])
        self.assertEqual(result['edges'][0]['provenance']['result']['suppressions'], [{'kind': 'inSource'}])
        sarif['version'] = '1.0';path.write_text(json.dumps(sarif))
        with self.assertRaises(audit.AuditError):
            import_connections(path, 'sarif')

    def test_bare_except_pass_detected_without_confusing_reraise(self):
        (self.root/'a.py').write_text('try:\n    work()\nexcept:\n    pass\n')
        self.assertEqual([f['rule'] for f in scan_python(self.root, ['a.py'])['findings']], ['PY-SILENT-EXCEPT'])
        (self.root/'a.py').write_text('try:\n    work()\nexcept:\n    raise\n')
        self.assertEqual(scan_python(self.root, ['a.py'])['findings'], [])

    def test_sarif_repeated_metadata_cannot_expand_without_bound(self):
        data = {'version':'2.1.0','runs':[{'tool':{'driver':{'name':'fixture','description':'x'*600000}},
                'results':[{'message':{'text':'candidate'},'locations':[{}]*60}]}]}
        path = self.root/'expanded.sarif'
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(audit.AuditError,'32 MiB'):
            import_connections(path,'sarif')

    def test_sarif_rule_defaults_and_malformed_nested_values(self):
        baseline = {'version':'2.1.0', 'runs':[{'tool':{'driver':{'rules':[
            {'id':'R1','defaultConfiguration':{'level':'error'}}]}},
            'results':[{'ruleId':'R1','message':{'text':'candidate'},'locations':[{'physicalLocation':{}}]}]}]}
        path = self.root/'input.sarif'
        path.write_text(json.dumps(baseline))
        self.assertEqual(import_connections(path, 'sarif')['findings'][0]['severity'], 'high')
        for field, bad_value in [('tool', []), ('artifacts', {}), ('results', {})]:
            data = copy.deepcopy(baseline)
            data['runs'][0][field] = bad_value
            path.write_text(json.dumps(data))
            with self.subTest(field=field), self.assertRaises(audit.AuditError):
                import_connections(path, 'sarif')
        baseline['runs'][0]['results'][0]['locations'][0]['physicalLocation'] = []
        path.write_text(json.dumps(baseline))
        with self.assertRaises(audit.AuditError):
            import_connections(path, 'sarif')

    def test_skill_form_is_document_evidence_never_automatic_support(self):
        data = {'schema':'software-skill-record/1', 'revision':'r1', 'skill':'control-plan',
                'author':'Fixture author', 'status':'PASS', 'criterion_targets':['VER-01'],
                'observations':{'measurement':'Synthetic check completed'}}
        path = self.root/'form.json'
        path.write_text(json.dumps(data))
        result = register(self.root,'form.json','E1','r1')
        self.assertEqual(result['evidence']['kind'], 'document')
        self.assertNotIn('assessment', result)
        for field, value in [('observations', {}), ('status', []), ('revision','other'), ('criterion_targets',['WRONG'])]:
            invalid = {**data, field:value}
            path.write_text(json.dumps(invalid))
            with self.subTest(field=field), self.assertRaises(audit.AuditError):
                register(self.root,'form.json','E1','r1')

    def test_witness_binds_command_log_and_source(self):
        (self.root/'check.py').write_text('print("passed")')
        command = [sys.executable, 'check.py']
        receipt = record(self.root, self.root/'run', 'r1', command, ['check.py'])
        self.assertEqual(receipt['exit_code'], 0)
        m = audit.new_manifest('r1', 'witness fixture')
        evidence = audit.evidence_record(self.root, 'run/stdout.log', 'E1', 'execution', 'r1')
        evidence.update(summary='Fixture output', locator='line 1', command=json.dumps(command), exit_code=0,
                        recorded_at=receipt['recorded_at'], witness_receipt='run/receipt.json')
        m['evidence'] = [evidence]
        self.assertEqual(audit.evaluate(m,self.root,'r1')['evidence_validation']['E1']['provenance'], 'local_witness_consistent')
        original_receipt = (self.root/'run/receipt.json').read_text()
        (self.root/'run/receipt.json').write_text('[]')
        self.assertIn('witness_receipt_invalid', audit.evaluate(m,self.root,'r1')['evidence_validation']['E1']['reasons'])
        (self.root/'run/receipt.json').write_text(original_receipt)
        (self.root/'run/stderr.log').write_text('tampered')
        self.assertIn('witness_receipt_invalid', audit.evaluate(m,self.root,'r1')['evidence_validation']['E1']['reasons'])
        (self.root/'run/stderr.log').write_text('')
        denied_sources = copy.deepcopy(receipt)
        denied_sources['sources_before'] = denied_sources['sources_after'] = {'.env': '0'*64}
        (self.root/'run/receipt.json').write_text(json.dumps(denied_sources))
        result = audit.evaluate(m,self.root,'r1',path_policy=project_file)
        self.assertIn('witness_receipt_invalid', result['evidence_validation']['E1']['reasons'])
        (self.root/'run/receipt.json').write_text(original_receipt)
        (self.root/'check.py').write_text('print("changed")')
        self.assertIn('witness_receipt_invalid', audit.evaluate(m,self.root,'r1')['evidence_validation']['E1']['reasons'])

    def test_witness_records_failure_timeout_and_refuses_overwrite(self):
        (self.root/'check.py').write_text('raise SystemExit(7)')
        receipt = record(self.root, self.root/'failed', 'r1', [sys.executable,'check.py'], ['check.py'])
        self.assertEqual(receipt['exit_code'], 7)
        with self.assertRaises(FileExistsError):
            record(self.root, self.root/'failed', 'r1', [sys.executable,'check.py'], ['check.py'])
        (self.root/'check.py').write_text('import time; time.sleep(5)')
        receipt = record(self.root, self.root/'slow', 'r1', [sys.executable,'check.py'], ['check.py'], timeout=.1)
        self.assertEqual(receipt['termination_reason'], 'timeout')

    def test_short_lived_witness_cannot_bypass_output_budget(self):
        (self.root/'check.py').write_text('print("x"*4096)')
        receipt = record(self.root,self.root/'large','r1',[sys.executable,'check.py'],['check.py'],max_output=128)
        self.assertEqual(receipt['termination_reason'],'output_limit')


if __name__ == '__main__':
    unittest.main()
