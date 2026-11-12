"""Balanced software priorities without relaxing behavioral evidence or hiding gaps."""
import copy
import unittest
import test_audit_standard as fixture
from audit_standard import catalog, scorecard
from scoring import AREA_BUDGETS


class ScoreBalanceTests(unittest.TestCase):
    def setUp(self):
        fixture.StandardTests.setUp(self)

    def result(self):
        return fixture.audit.evaluate(self.manifest, self.root, 'snapshot')

    def boundaries(self, count, score):
        return [{'id': str(i), 'reviews': {a: {'score':score,'status':'supported' if score == 4 else 'gap'}
                 for a in fixture.audit.ASPECTS}} for i in range(count)]

    def test_interface_count_cannot_expand_its_importance(self):
        controls = self.result()['controls']
        for count in (1, 100):
            result = scorecard(controls, self.boundaries(count, 0), [])
            self.assertEqual(result['overall']['observed_score_percent'], 94)
            self.assertEqual(result['by_stage']['interfaces']['effective_budget_percent'], 6)
        legacy = scorecard(controls,self.boundaries(100, 0),[],'0.2.0')
        self.assertEqual(legacy['overall']['observed_score_percent'],14.16)

    def test_priority_and_contribution_are_explicit(self):
        self.assertEqual(sum(AREA_BUDGETS.values()),100)
        controls = self.result()['controls']
        scores = {}
        for cid in ('REQ-01','IMP-02'):
            changed = copy.deepcopy(controls)
            for check in next(c for c in changed if c['id']==cid)['checks']:
                check.update(score=0,status='gap')
            result = scorecard(changed,self.boundaries(1,4),[])
            scores[cid] = result['overall']['observed_score_percent']
            contributions = [s['earned_contribution_percent'] or 0 for s in result['by_stage'].values()]
            self.assertAlmostEqual(sum(contributions),result['overall']['documented_achievement_lower_bound_percent'],places=2)
        self.assertEqual(scores,{'REQ-01':97.5,'IMP-02':92.8})

    def test_question_count_does_not_expand_criterion_priority(self):
        controls = self.result()['controls']
        controls[0]['checks'][0].update(score=0,status='gap')
        before = scorecard(controls,[],[])['overall']
        controls[0]['checks'] *= 5
        after = scorecard(controls,[],[])['overall']
        self.assertEqual(before['observed_score_percent'],after['observed_score_percent'])

    def test_single_supported_question_has_small_documented_score(self):
        self.manifest['assessments'] = [self.manifest['assessments'][0]]
        self.manifest['assessments'][0]['checks'] = [self.manifest['assessments'][0]['checks'][0]]
        card = self.result()['scorecard']
        overall = card['overall']
        self.assertEqual(overall['observed_score_percent'],100)
        self.assertLess(overall['documented_achievement_lower_bound_percent'],1)
        requirements = card['by_stage']['requirements']
        self.assertEqual(requirements['observed_score_percent'],100)
        self.assertEqual(requirements['documented_achievement_lower_bound_percent'],16.67)
        self.assertEqual(requirements['weighted_coverage_percent'],16.67)

    def test_every_area_responds_to_changed_evidence_scores(self):
        baseline = self.result()['controls']
        for area in AREA_BUDGETS:
            for value in range(5):
                with self.subTest(area=area, score=value):
                    controls = copy.deepcopy(baseline)
                    boundaries = self.boundaries(1,4)
                    reviews = [check for c in controls if c['stage']==area for check in c['checks']]
                    if area == 'interfaces':
                        reviews = list(boundaries[0]['reviews'].values())
                    self.assertTrue(reviews)
                    for check in reviews:
                        check.update(score=value,status='gap' if value==0 else 'supported' if value==4 else 'partial')
                    stats = scorecard(controls,boundaries,[])['by_stage'][area]
                    self.assertEqual(stats['observed_score_percent'],25*value)
                    self.assertEqual(stats['documented_achievement_lower_bound_percent'],25*value)

    def test_inspection_and_behavior_have_different_appropriate_evidence(self):
        self.manifest['evidence'][0]['kind'] = 'source'
        result = self.result()
        checks = {check['id']:check for c in result['controls'] for check in c['checks']}
        self.assertEqual(checks['PRE-01.1']['status'],'supported')
        self.assertEqual(checks['PRE-01.3']['status'],'unverified')
        self.assertEqual(checks['CHG-01.3']['status'],'unverified')
        self.manifest['standard_version'] = '0.2.0'
        old = self.result()
        checks = {check['id']:check for c in old['controls'] for check in c['checks']}
        self.assertEqual(old['standard_version'],'0.2.0')
        self.assertEqual(checks['PRE-01.1']['status'],'unverified')
        self.assertEqual(checks['CHG-01.3']['status'],'supported')
        self.assertEqual(old['scorecard']['policy_id'],'checkpoint-weight/0.2.0')

    def test_catalog_exposes_all_evidence_modes_and_anchors(self):
        criteria = catalog(fixture.audit.CONTROLS)
        self.assertEqual(criteria['standard_version'],'0.3.0')
        self.assertEqual(criteria['scoring_policy']['area_budgets_percent'],AREA_BUDGETS)
        checks = [check for c in criteria['controls'] for check in c['checkpoints']]
        self.assertEqual(len(checks),72)
        self.assertEqual(sum(c['evidence_mode']=='execution' for c in checks),27)
        self.assertTrue(all(c['score_3_anchor'] and c['score_4_anchor'] for c in checks))

    def test_excluded_areas_and_empty_interface_scope_are_visible(self):
        for assessment in self.manifest['assessments']:
            if assessment['id'].startswith('REQ-'):
                for check in assessment['checks']:
                    check.update(status='not_applicable',score=None)
        result = self.result()['scorecard']
        self.assertEqual(result['by_stage']['requirements']['applicability'],'excluded')
        self.assertEqual(result['by_stage']['interfaces']['applicability'],'not_represented')
        self.assertEqual(result['active_budget_percent'],89)
        self.assertAlmostEqual(sum(s['effective_budget_percent'] for s in result['by_stage'].values()),100,places=2)


if __name__ == '__main__':
    unittest.main()
