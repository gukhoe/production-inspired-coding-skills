"""Discriminating audit tests: pass the current-schema control before perturbation."""
import unittest
import copy
import test_audit_standard as fixture
audit = fixture.audit


class ReviewRegressions(unittest.TestCase):
    def setUp(self):
        fixture.StandardTests.setUp(self)

    def result(self, revision='snapshot'):
        return audit.evaluate(self.manifest, self.root, revision)

    def test_hash_validation_from_supported_baseline(self):
        self.assertEqual(self.result()['outcome'], 'reviewed_scope_supported')
        (self.root / 'result.txt').write_text('changed bytes')
        result = self.result()
        self.assertIn('hash_mismatch', result['evidence_validation']['E1']['reasons'])
        self.assertEqual(result['controls'][0]['checks'][0]['status'], 'unverified')

    def test_each_evidence_description_field_is_required(self):
        for field in ('locator', 'summary'):
            with self.subTest(field=field):
                self.assertEqual(self.result()['outcome'], 'reviewed_scope_supported')
                value = self.manifest['evidence'][0][field]
                self.manifest['evidence'][0][field] = ''
                self.assertIn('evidence_description_missing', self.result()['evidence_validation']['E1']['reasons'])
                self.manifest['evidence'][0][field] = value

    def test_manifest_revision_isolated_from_evidence_revision(self):
        self.assertEqual(self.result()['outcome'], 'reviewed_scope_supported')
        self.manifest['revision'] = 'different'
        result = self.result()
        self.assertTrue(result['evidence_validation']['E1']['valid'])
        self.assertIn('audit_revision_mismatch', result['controls'][0]['checks'][0]['issues'])
        self.assertNotEqual(result['outcome'], 'reviewed_scope_supported')

    def test_missing_reviewer_does_not_accuse_valid_gate_artifacts(self):
        self.assertEqual(self.result()['gates'][0]['state'], 'evidence_ready')
        self.manifest['gates'][0]['review']['reviewer'] = ''
        gate = self.result()['gates'][0]
        self.assertIn('handoff_review_not_supported', gate['blockers'])
        self.assertNotIn('input_evidence_invalid', gate['blockers'])
        self.assertNotIn('output_evidence_invalid', gate['blockers'])

    def test_blanket_log_cannot_support_every_question(self):
        for assessment in self.manifest['assessments']:
            for check in assessment['checks']:
                check.pop('evidence_links', None)
        result = self.result()
        self.assertNotEqual(result['outcome'], 'reviewed_scope_supported')
        self.assertLess(result['scorecard']['overall']['scored_items'], 72)

    def test_self_review_not_independent_support(self):
        self.manifest['author'] = 'Fixture reviewer'
        self.manifest['audit_context'] = {'type': 'first_party', 'relationship': 'self', 'independence_rationale': 'Same implementer'}
        self.assertNotEqual(self.result()['outcome'], 'reviewed_scope_supported')
        self.assertIn('review_accountability_unestablished', self.result()['gates'][0]['blockers'])
        from visual_report import build_view
        self.assertIn('Review independence: unestablished', build_view(self.result())['interpretation'])
        self.assertIn('| Independence | unestablished |', audit.markdown(self.result()))

    def test_alias_evidence_ids_do_not_bypass_reuse_control(self):
        self.assertEqual(self.result()['outcome'], 'reviewed_scope_supported')
        for index, assessment in enumerate(self.manifest['assessments']):
            alias = copy.deepcopy(self.manifest['evidence'][0])
            alias['id'] = f'ALIAS{index}'
            self.manifest['evidence'].append(alias)
            for check in assessment['checks']:
                check['evidence'] = [alias['id']]
                check.pop('evidence_links', None)
        self.assertEqual(self.result()['scorecard']['overall']['scored_items'], 0)


if __name__ == '__main__':
    unittest.main()
