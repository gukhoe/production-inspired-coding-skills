"""Review accountability and evidence reuse: attestations, never identity proof."""
from collections import defaultdict

POLICY_VERSION = '1.0'
REUSE_THRESHOLD = 3


def reuse_index(manifest, evidence):
    usage = defaultdict(set)
    for criterion in manifest.get('assessments', []):
        if not isinstance(criterion, dict) or not isinstance(criterion.get('checks', []), list):
            continue
        for check in criterion.get('checks', []):
            if not isinstance(check, dict) or not isinstance(check.get('evidence', []), list):
                continue
            if isinstance(check.get('status'), str) and check['status'] in {'supported', 'partial', 'gap', 'not_applicable'}:
                for eid in check.get('evidence', []):
                    if isinstance(eid, str) and eid in evidence and isinstance(check.get('id'), str):
                        usage[evidence[eid]['sha256']].add(check['id'])
    return usage


def reuse_issues(item, evidence, usage):
    if item.get('status') not in {'supported', 'not_applicable'} or not item.get('id'):
        return []
    links = item.get('evidence_links', [])
    if not isinstance(links, list):
        return ['checkpoint_evidence_links_invalid']
    for eid in item.get('evidence', []):
        if len(usage.get(evidence[eid]['sha256'], ())) <= REUSE_THRESHOLD:
            continue
        if not any(isinstance(link, dict) and link.get('evidence_id') == eid and
                   isinstance(link.get('locator'), str) and link['locator'].strip() and
                   isinstance(link.get('rationale'), str) and link['rationale'].strip()
                   for link in links):
            return ['reused_evidence_needs_checkpoint_locator_and_rationale']
    return []


def accountability(manifest):
    author = manifest.get('author', '')
    context = manifest.get('audit_context', {})
    issues = []
    if not isinstance(author, str) or not author.strip():
        issues.append('audit_author_required')
    if not isinstance(context, dict):
        context = {}
    if not isinstance(context.get('type'), str) or context['type'] not in {'first_party', 'second_party', 'third_party'}:
        issues.append('audit_type_required')
    rationale = context.get('independence_rationale', '')
    if context.get('relationship') != 'independent' or not isinstance(rationale, str) or not rationale.strip():
        issues.append('independent_review_not_established')
    reviewers = {c['reviewer'].strip().casefold() for a in manifest.get('assessments', []) if isinstance(a, dict) and isinstance(a.get('checks', []), list)
                 for c in a.get('checks', []) if isinstance(c, dict) and c.get('status') == 'supported' and isinstance(c.get('reviewer'), str)}
    if isinstance(author, str) and author.strip().casefold() in reviewers:
        issues.append('author_is_checkpoint_reviewer')
    return {'policy_version': POLICY_VERSION, 'author': author, 'audit_context': context,
            'issues': issues, 'independence': 'declared' if not issues else 'unestablished',
            'execution_provenance': 'Self-reported unless a local witness receipt is separately verified; no CI identity attestation is verified.',
            'limitation': 'Names, relationships and locator rationales are reviewer assertions, not authenticated identity or semantic proof. The engine cannot establish that a log is truthful or adequate.'}
