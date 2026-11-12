import sys
import json
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from build_skills import outputs
from evaluate_reviewers import evaluate
from historical_sources import original_bytes


class SkillTests(unittest.TestCase):
    def test_generated_skills_are_current_and_templates_local(self):
        root = Path(__file__).resolve().parents[1]
        files = list(outputs())
        self.assertEqual(len(files), 48)
        for relative, expected in files:
            self.assertEqual((root/relative).read_text(encoding='utf-8'), expected, relative)

    def test_original_skill_is_still_read_from_immutable_archive(self):
        root = Path(__file__).resolve().parents[1]
        self.assertIn(b'High severity overrides low RPN', original_bytes(root,'skills/pfmea-risk/SKILL.md'))
        self.assertNotIn('High severity overrides low RPN', (root/'skills/pfmea-risk/SKILL.md').read_text())

    def test_blank_report_forms_match_current_engine(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/software-process-audit/scripts'))
        import audit
        root = Path(__file__).resolve().parents[1]
        folder = root/'examples/software-audit'
        manifest = audit.new_manifest('UNASSESSED-SNAPSHOT', 'Blank standard form; no project has been audited')
        self.assertEqual(json.loads((folder/'blank-review.json').read_text()), manifest)
        report = audit.evaluate(manifest, root, 'UNASSESSED-SNAPSHOT')
        self.assertEqual(json.loads((folder/'blank-report.json').read_text()), report)
        self.assertEqual((folder/'blank-report.md').read_text(encoding='utf-8'), audit.markdown(report))

    def test_always_pass_reviewer_has_false_passes_and_zero_kappa(self):
        result = evaluate([{'id': 'good','truth':'PASS','decisions':{'weak':'PASS','oracle':'PASS'}},
                           {'id': 'bad','truth':'FAIL','decisions':{'weak':'PASS','oracle':'FAIL'}}])
        self.assertEqual(result['weak']['false_pass_rate'], 1)
        self.assertEqual(result['weak']['cohen_kappa'], 0)
        self.assertEqual(result['oracle']['cohen_kappa'], 1)

    def test_degenerate_agreement_is_not_fabricated_kappa(self):
        result = evaluate([{'id':'one','truth':'PASS','decisions':{'r':'PASS','missing':'UNVERIFIED'}}])
        self.assertIsNone(result['r']['cohen_kappa'])
        self.assertIsNone(result['missing']['agreement'])


if __name__ == '__main__':
    unittest.main()
