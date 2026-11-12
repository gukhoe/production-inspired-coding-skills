"""Known-bad sentinels for evidence checks; this is a focused mutation set, not exhaustive testing."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = [
    ('hash', 'elif file_hash(path) != expected:', 'elif False:', 'test_hash_validation_from_supported_baseline'),
    ('description', 'if not nonempty(item.get("summary")) or not nonempty(item.get("locator")):', 'if False:', 'test_each_evidence_description_field_is_required'),
    ('revision', 'if not same_revision:\n                problems.append("audit_revision_mismatch")', 'if False:\n                problems.append("audit_revision_mismatch")', 'test_manifest_revision_isolated_from_evidence_revision'),
]


def main():
    results = []
    with tempfile.TemporaryDirectory(prefix='audit-mutations-') as directory:
        root = Path(directory)
        source = root/'skills/software-process-audit/scripts'
        shutil.copytree(ROOT/'skills/software-process-audit/scripts', source, ignore=shutil.ignore_patterns('__pycache__'))
        (root/'tests').mkdir()
        for name in ('test_review_regressions.py', 'test_audit_standard.py'):
            shutil.copy2(ROOT/'tests'/name, root/'tests'/name)
        target = source/'audit.py';original = target.read_text(encoding='utf-8')
        for name, before, after, test in MUTATIONS:
            command = [sys.executable, '-m', 'unittest', f'test_review_regressions.ReviewRegressions.{test}']
            good = subprocess.run(command, cwd=root/'tests', capture_output=True, text=True, timeout=30)
            if good.returncode:
                raise RuntimeError('Positive control failed: '+good.stderr)
            if original.count(before) != 1:
                raise RuntimeError('Mutation seam changed: '+name)
            mutated = original.replace(before, after)
            target.write_text(mutated, encoding='utf-8')
            if target.read_text(encoding='utf-8') == original:
                raise RuntimeError('Mutation did not land')
            bad = subprocess.run(command, cwd=root/'tests', capture_output=True, text=True, timeout=30)
            killed = bad.returncode != 0 and f'FAIL: {test}' in bad.stderr and 'ERROR:' not in bad.stderr
            results.append({'mutation': name, 'positive_control': 'passed', 'detected_by_intended_assertion': killed})
            target.write_text(original, encoding='utf-8')
    print(json.dumps(results, indent=2))
    return 0 if all(r['detected_by_intended_assertion'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
