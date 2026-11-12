import copy
import unittest
import test_audit_standard as fixture
from score_dimensions import assurance_dimensions


class DimensionTests(unittest.TestCase):
    def setUp(self):
        fixture.StandardTests.setUp(self)

    def result(self):
        return fixture.audit.evaluate(self.manifest, self.root, 'snapshot')

    def risk(self, severity='high', status='open'):
        return {'id': 'R1', 'severity': severity, 'status': status, 'failure_mode': 'Lost state',
                'impact': 'User data loss', 'targets': ['IMP-02', 'RSK-01'], 'owner': 'Team',
                'action': 'Test corrective recovery', 'due': '2026-01-01', 'verification': copy.deepcopy(self.review)}

    def test_documentation_cannot_raise_execution_or_close_risk(self):
        self.manifest['risks'] = [self.risk()]
        self.manifest['evidence'][0]['kind'] = 'source'
        card = self.result()['scorecard']['dimensions']
        self.assertEqual(card['documentation']['overall']['score_percent'], 100)
        self.assertEqual(card['execution']['overall']['score_percent'], 0)
        self.assertEqual(card['execution']['overall']['weighted_coverage_percent'], 0)
        self.assertEqual(card['risk_resolution']['score_percent'], 0)
        self.assertEqual(card['documentation']['by_stage']['risk']['score_percent'], 100)
        self.assertIsNone(card['execution']['by_stage']['risk']['score_percent'])

    def test_static_partial_scores_do_not_claim_execution(self):
        baseline = self.result()['scorecard']['dimensions']
        self.assertEqual(baseline['execution']['overall']['score_percent'], 100)
        self.manifest['evidence'][0]['kind'] = 'source'
        for a in self.manifest['assessments']:
            for c in a['checks']:
                c.update(status='partial', score=2)
        card = self.result()['scorecard']['dimensions']
        self.assertEqual(card['documentation']['overall']['score_percent'], 50)
        self.assertEqual(card['execution']['overall']['score_percent'], 0)
        self.assertEqual(card['execution']['overall']['scored_items'], 0)

    def test_failed_run_is_not_positive_credit(self):
        for a in self.manifest['assessments']:
            for c in a['checks']:
                c.update(status='partial', score=2)
        self.assertEqual(self.result()['scorecard']['dimensions']['execution']['overall']['score_percent'], 50)
        self.manifest['evidence'][0]['exit_code'] = 1
        result = self.result()
        card = result['scorecard']['dimensions']['execution']['overall']
        self.assertEqual(card['score_percent'], 0)
        self.assertEqual(card['weighted_coverage_percent'], 100)
        self.manifest['evidence'][0]['recorded_at'] = 'invalid'
        self.assertEqual(self.result()['scorecard']['dimensions']['execution']['overall']['weighted_coverage_percent'], 0)

    def test_registered_closure_needs_success_and_effective_closure(self):
        self.manifest['risks'] = [self.risk(status='closed')]
        self.assertEqual(self.result()['scorecard']['dimensions']['risk_resolution']['score_percent'], 100)
        self.manifest['evidence'][0]['exit_code'] = 1
        self.assertEqual(self.result()['scorecard']['dimensions']['risk_resolution']['score_percent'], 0)
        self.manifest['evidence'][0]['exit_code'] = 0
        self.manifest['risks'][0]['owner'] = ''
        self.assertEqual(self.result()['scorecard']['dimensions']['risk_resolution']['score_percent'], 0)

    def test_no_risks_is_not_perfect_closure_and_memberships_do_not_duplicate(self):
        self.assertIsNone(self.result()['scorecard']['dimensions']['risk_resolution']['score_percent'])
        self.manifest['risks'] = [self.risk(status='closed'), {**self.risk('low'), 'id': 'R2'}]
        r = self.result()['scorecard']['dimensions']['risk_resolution']
        self.assertEqual(r['score_percent'], 75)
        self.assertEqual(r['registered_risks'], 2)
        self.assertEqual(r['by_stage']['risk']['registered_risks'], 2)
        self.assertEqual(r['by_stage']['implementation']['registered_risks'], 2)

    def test_report_and_historical_projection_use_fixed_classification(self):
        report = self.result()
        self.assertEqual(report['report_template_version'], '1.1')
        self.assertIn('Separate assurance indicators', fixture.audit.markdown(report))
        self.assertEqual(report['scorecard']['dimensions']['execution']['overall']['total_items'], 27)
        self.assertEqual(report['scorecard']['dimensions']['documentation']['overall']['total_items'], 45)
        old = copy.deepcopy(report)
        for c in old['controls']:
            for q in c['checks']:
                q['evidence_mode'] = 'inspection'
        projected = assurance_dimensions(old['controls'], old['boundaries'], old['risks'], old['evidence_validation'])
        self.assertEqual(projected, report['scorecard']['dimensions'])


if __name__ == '__main__':
    unittest.main()
