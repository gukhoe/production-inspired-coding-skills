"""Agreement against labeled fixtures; no AI invocation or claim of model improvement."""
import argparse
import json
from pathlib import Path


def evaluate(cases):
    if not isinstance(cases, list) or not cases:
        raise ValueError('Provide a nonempty list of labeled cases')
    ids = set()
    for row in cases:
        if row.get('truth') not in {'PASS', 'FAIL'} or not row.get('id') or row['id'] in ids or not isinstance(row.get('decisions'), dict):
            raise ValueError('Each unique case needs truth PASS/FAIL and decisions by reviewer')
        if any(value not in {'PASS', 'FAIL', 'UNVERIFIED'} for value in row['decisions'].values()):
            raise ValueError('Decision must be PASS, FAIL or UNVERIFIED')
        ids.add(row['id'])
    result = {}
    for reviewer in sorted({key for row in cases for key in row['decisions']}):
        observed = [(row['truth'], row['decisions'].get(reviewer)) for row in cases if row['decisions'].get(reviewer) in {'PASS', 'FAIL'}]
        n = len(observed)
        matrix = {a+'_'+b: sum(x == a and y == b for x,y in observed) for a in ('PASS','FAIL') for b in ('PASS','FAIL')}
        agreement = sum(a == b for a,b in observed)/n if n else None
        expected = (sum(a == 'PASS' for a,b in observed)*sum(b == 'PASS' for a,b in observed)+sum(a == 'FAIL' for a,b in observed)*sum(b == 'FAIL' for a,b in observed))/(n*n) if n else None
        bad = sum(a == 'FAIL' for a,b in observed);good = n-bad
        result[reviewer] = {'n': n, 'unverified': len(cases)-n, 'confusion_matrix_truth_then_decision': matrix,
                            'agreement': agreement, 'cohen_kappa': (agreement-expected)/(1-expected) if expected is not None and expected < 1 else None,
                            'false_pass_rate': matrix['FAIL_PASS']/bad if bad else None,
                            'false_fail_rate': matrix['PASS_FAIL']/good if good else None}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate(json.loads(args.input.read_text(encoding='utf-8'))), indent=2))


if __name__ == '__main__':
    main()
