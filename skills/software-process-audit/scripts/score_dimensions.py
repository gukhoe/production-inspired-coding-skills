"""Separate review maturity, demonstrated behavior and verified risk closure."""
if __package__:
    from .scoring import AREA_BUDGETS, summarize
else:
    from scoring import AREA_BUDGETS, summarize

DIMENSION_POLICY = 'assurance-dimensions/1.0'
SEVERITY_WEIGHTS = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}


def _dimension(rows):
    areas = {}
    normalized = []
    for area, budget in AREA_BUDGETS.items():
        selected = [r for r in rows if r['stage'] == area]
        maximum = sum(r['weight'] for r in selected if r['status'] != 'not_applicable')
        stats = summarize(selected)
        stats['score_percent'] = stats['documented_achievement_lower_bound_percent']
        stats['applicability'] = 'active' if maximum else 'excluded' if selected else 'not_represented'
        areas[area] = stats
        normalized.extend({**r, 'weight': r['weight'] * budget / maximum if maximum else 0} for r in selected)
    overall = summarize(normalized)
    overall['score_percent'] = overall['documented_achievement_lower_bound_percent']
    return {'overall': overall, 'by_stage': areas, 'items': rows}


def _closure(risks, evidence):
    items = []
    for risk in risks:
        review = risk.get('verification', {})
        successful = any(evidence.get(eid, {}).get('successful_execution_record', False)
                         for eid in review.get('evidence', []))
        closed = risk.get('effective_status') == 'closed' and review.get('status') == 'supported' and successful
        items.append({'id': risk['id'], 'severity': risk['severity'],
                      'weight': SEVERITY_WEIGHTS[risk['severity']], 'verified_closed': closed})
    total = sum(r['weight'] for r in items)
    earned = sum(r['weight'] for r in items if r['verified_closed'])
    return {'score_percent': round(100 * earned / total, 2) if total else None,
            'registered_risks': len(items), 'verified_closed_risks': sum(r['verified_closed'] for r in items),
            'unresolved_risks': sum(not r['verified_closed'] for r in items),
            'total_severity_weight': total, 'closed_severity_weight': earned,
            'applicability': 'registered_risks' if items else 'no_registered_risks', 'items': items}


def assurance_dimensions(controls, boundaries, risks, evidence):
    # Fixed classification permits explicit historical projections under the same policy.
    if __package__:
        from .audit_standard import EXECUTION_CHECKPOINTS, WEIGHTS
    else:
        from audit_standard import EXECUTION_CHECKPOINTS, WEIGHTS
    documentation, execution = [], []

    def add(check, identifier, stage, weight, behavioral):
        row = {'id': identifier, 'stage': stage, 'weight': weight,
               'score': check.get('score'), 'status': check['status'],
               'reviewed_score': check.get('score'), 'evidence': check.get('evidence', [])}
        if behavioral:
            linked = [evidence.get(eid, {}) for eid in row['evidence']]
            success = any(e.get('valid') and e.get('successful_execution_record') for e in linked)
            recorded = success or any(e.get('valid') and e.get('recorded_execution_record') for e in linked)
            row.update(successful_execution=success, recorded_execution=recorded)
            if row['status'] != 'not_applicable' and row['score'] is not None and not success:
                row.update(score=0 if recorded else None, status='gap' if recorded else 'unverified')
            execution.append(row)
        else:
            documentation.append(row)

    for control in controls:
        checks = control.get('checks', [])
        for check in checks:
            add(check, check['id'], control['stage'], WEIGHTS.get(control['id'], 2) / len(checks),
                check['id'] in EXECUTION_CHECKPOINTS)
    for boundary in boundaries:
        for aspect, review in boundary['reviews'].items():
            add(review, 'boundary:' + boundary['id'] + ':' + aspect, 'interfaces', 1, aspect != 'contract')
    closure = _closure(risks, evidence)
    stages = {c['id']: c['stage'] for c in controls}
    stages.update({'boundary:' + b['id']: 'interfaces' for b in boundaries})
    closure['by_stage'] = {area: _closure([r for r in risks if area in {stages.get(t) for t in r['targets']}], evidence)
                           for area in AREA_BUDGETS}
    closure['severity_weights'] = dict(SEVERITY_WEIGHTS)
    return {'policy_id': DIMENSION_POLICY,
            'documentation': _dimension(documentation), 'execution': _dimension(execution),
            'risk_resolution': closure,
            'interpretation': 'Three independent indicators; never average them into a safety score. Documentation/design review uses inspection checkpoints only. Execution uses behavioral checkpoints and boundary aspects; positive credit requires linked successful current execution plus the assessed score. Unknowns earn no points, but are not failures. Closure counts only registered risks with effective closure and supported successful verification. No registered risks means N/A, never 100%. Area closure memberships may overlap; the overall register counts each risk once. Scores reflect reviewer-scoped evidence, not reliability probabilities, native/live acceptance or authenticated test adequacy.'}
