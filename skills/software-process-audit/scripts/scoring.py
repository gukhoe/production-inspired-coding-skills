"""Area-budget scoring: scope size cannot silently set an area's importance."""

AREA_BUDGETS = {
    'requirements': 5, 'design': 7, 'dependencies': 4, 'implementation': 12,
    'verification': 12, 'release': 7, 'operations': 7, 'change': 4,
    'risk': 6, 'improvement': 6, 'scope': 4, 'prevention': 10,
    'handoff': 4, 'diagnosis': 6, 'interfaces': 6,
}
POLICY_ID = 'balanced-area/1.0'


def summarize(items):
    applicable = [r for r in items if r['status'] != 'not_applicable']
    scored = [r for r in applicable if r['score'] is not None]
    maximum = sum(r['weight']*4 for r in applicable)
    observed_max = sum(r['weight']*4 for r in scored)
    earned = sum(r['weight']*r['score'] for r in scored)
    return {'observed_score_percent': round(100*earned/observed_max, 2) if observed_max else None,
            'weighted_coverage_percent': round(100*observed_max/maximum, 2) if maximum else None,
            'documented_achievement_lower_bound_percent': round(100*earned/maximum, 2) if maximum else None,
            'total_items': len(items), 'scored_items': len(scored),
            'unverified_items': len(applicable)-len(scored), 'not_applicable_items': len(items)-len(applicable)}


def balanced_scorecard(controls, boundaries, open_high_risks, weights, rubric):
    rows = []
    for control in controls:
        checks = control.get('checks', [control])
        # A criterion has one priority allocation, irrespective of its question count.
        rows.extend({'id': c['id'], 'stage': control['stage'], 'weight': weights.get(control['id'], 2)/len(checks),
                     'score': c.get('score'), 'status': c['status']} for c in checks)
    rows.extend({'id': 'boundary:'+b['id']+':'+aspect, 'stage': 'interfaces', 'weight': 1,
                 'score': review.get('score'), 'status': review['status']}
                for b in boundaries for aspect, review in b['reviews'].items())
    area_rows = {area: [r for r in rows if r['stage'] == area] for area in AREA_BUDGETS}
    area_max = {area: sum(r['weight'] for r in items if r['status'] != 'not_applicable')
                for area, items in area_rows.items()}
    active_budget = sum(AREA_BUDGETS[area] for area in AREA_BUDGETS if area_max[area])
    normalized = [{**r, 'weight': r['weight']*AREA_BUDGETS[r['stage']]/area_max[r['stage']]
                   if area_max[r['stage']] else 0} for r in rows]
    by_stage = {}
    for area, items in area_rows.items():
        stats = summarize(items)
        effective = AREA_BUDGETS[area]/active_budget if area_max[area] and active_budget else 0
        # Derive contribution from raw totals, not rounded display percentages.
        earned = sum(r['weight']*r['score'] for r in items if r['status'] != 'not_applicable' and r['score'] is not None)
        stats.update(budget_percent=AREA_BUDGETS[area], effective_budget_percent=round(100*effective, 4),
                     earned_contribution_percent=round(100*effective*earned/(4*area_max[area]), 4) if area_max[area] else None,
                     applicability='active' if area_max[area] else 'excluded' if items else 'not_represented')
        by_stage[area] = stats
    return {'rubric': rubric, 'policy_id': POLICY_ID, 'area_budgets_percent': dict(AREA_BUDGETS),
            'active_budget_percent': active_budget,
            'weight_policy': 'Fixed area budgets total 100. Criterion priority is distributed within its area; interface count cannot expand its area budget. Excluded or unrepresented areas are disclosed and remaining budgets are normalized. Policy priorities, not calibrated incident probabilities.',
            'overall': summarize(normalized), 'by_stage': by_stage,
            'open_high_or_critical_risks': open_high_risks,
            'interpretation': 'Documented score is the achievement lower bound over applicable scope; unknowns contribute no earned points but are not classified as defects. Observed score describes scored evidence only. Compare coverage, exclusions and area budgets. Scores do not certify safety or authorize release.'}
