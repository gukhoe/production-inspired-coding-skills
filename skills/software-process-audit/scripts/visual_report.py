"""Evidence-preserving view model and offline HTML report. No graph changes scores."""
import base64
import gzip
import json
from pathlib import Path

if __package__:
    from .graph_adapter import AuditError
    from .connection_audit import validate_connections, connection_catalog, digest
else:
    from graph_adapter import AuditError
    from connection_audit import validate_connections, connection_catalog, digest


def build_view(report, connections=None):
    if report.get("schema_version") != 2 or report.get("report_template_version") != "1.0":
        raise AuditError("Visual report requires evaluated report template 1.0")
    if connections is not None:
        validate_connections(connections)
    risks = report.get('risks', [])
    boundaries = report.get('boundaries', [])
    processes = {p['id']: p for p in report.get('processes', [])}
    for boundary in boundaries:
        for endpoint in (boundary['source'], boundary['target']):
            processes.setdefault(endpoint, {'id': endpoint, 'kind': 'runtime', 'owner': '', 'input': '', 'output': ''})
    process_nodes = [{'id': pid, 'label': p.get('label', pid), 'kind': p.get('kind', 'runtime'),
                      'owner': p.get('owner', ''), 'input': p.get('input', ''), 'output': p.get('output', ''),
                      'mapped_nodes': p.get('code_nodes', p.get('graph_nodes', []))} for pid, p in processes.items()]
    handoffs, tasks, mapped_risks = [], [], set()
    for boundary in boundaries:
        target = 'boundary:' + boundary['id']
        linked = [r for r in risks if target in r['targets']]
        mapped_risks.update(r['id'] for r in linked)
        active_risks = [r for r in linked if r['effective_status'] != 'closed']
        reviews = boundary['reviews']
        states = {r['status'] for r in reviews.values()}
        high = any(r['severity'] in {'high', 'critical'} for r in active_risks)
        state = ('risk' if high or 'gap' in states else 'review' if active_risks or states & {'partial', 'unverified'}
                 else 'supported' if states <= {'supported', 'not_applicable'} and 'supported' in states else 'unknown')
        evidence_ids = sorted({eid for r in reviews.values() for eid in r['evidence']})
        handoffs.append({'id': target, 'source': boundary['source'], 'target': boundary['target'], 'directed': True,
                         'relation': 'declared handoff', 'confidence': 'DECLARED', 'state': state,
                         'failure_mode': boundary['failure_mode'], 'reviews': reviews, 'risks': linked,
                         'evidence_ids': evidence_ids, 'provenance': {'provider': 'Reviewed audit manifest'},
                         'interpretation': 'Declared process direction. Red means an open high risk or assessed gap, not demonstrated exploitation.'})
        for aspect, review in reviews.items():
            if review['status'] in {'supported', 'not_applicable'}: continue
            tasks.append({'id': target+':'+aspect, 'priority': 'high' if state == 'risk' else 'medium',
                          'target': target, 'title': aspect.replace('_', ' ').capitalize()+' needs evidence',
                          'state': review['status'], 'finding': review['finding'] or boundary['failure_mode'],
                          'action': review['improvement'] or 'Inspect both ends of the handoff and document the missing control or verification.',
                          'owner': review['owner'], 'due': review['due'], 'evidence_ids': review['evidence'],
                          'acceptance': 'Execute a discriminating failure scenario and an adjacent valid case; re-evaluate the manifest with current evidence.'})
    for risk in risks:
        if risk['effective_status'] == 'closed': continue
        tasks.append({'id': 'risk:'+risk['id'], 'priority': risk['severity'], 'target': ', '.join(risk['targets']),
                      'title': risk['failure_mode'], 'state': risk['effective_status'], 'finding': risk['impact'],
                      'action': risk.get('action', '') or 'Define and assign a corrective action.', 'owner': risk.get('owner', ''),
                      'due': risk.get('due', ''), 'evidence_ids': risk['verification']['evidence'],
                      'acceptance': risk['verification']['rationale'] or 'Reproduce the issue, verify correction and adjacent regression, then re-evaluate closure.'})
    for control in report.get('controls', []):
        for check in control.get('checks', []):
            if check['status'] not in {'gap', 'partial', 'unverified'}: continue
            tasks.append({'id': check['id'], 'priority': 'high' if check['status'] == 'gap' else 'medium',
                          'target': check['id'], 'title': check['question'], 'state': check['status'],
                          'finding': check['finding'] or check['rationale'], 'action': check['improvement'] or 'Review the missing evidence and define a proportionate improvement.',
                          'owner': check['owner'], 'due': check['due'], 'evidence_ids': check['evidence'],
                          'acceptance': 'Supply current evidence for the original checkpoint and re-evaluate; do not close an issue from a diagram.'})
    source_nodes, source_edges, notices = [], [], []
    if connections:
        all_nodes = {n['id']: n for n in connections['nodes']}
        mappings = {}
        for node in process_nodes:
            for nid in node['mapped_nodes']:
                if nid in all_nodes:
                    mappings.setdefault(nid, set()).add(node['id'])
                else:
                    notices.append('Mapped source node absent: '+str(nid))
        by_pair = {}
        for edge in handoffs:
            by_pair.setdefault((edge['source'], edge['target']), []).append(edge)
        by_edge = {}
        for finding in connections.get('findings', []):
            by_edge.setdefault(finding['edge_id'], []).append(finding)
            tasks.append({'id': finding['id'], 'priority': finding['severity'], 'target': finding['edge_id'],
                          'title': finding['title'], 'state': 'candidate', 'finding': finding['failure_scenario'],
                          'action': finding['improvement'], 'owner': '', 'due': '', 'evidence_ids': [],
                          'acceptance': finding['verification'], 'source': {k: finding.get(k) for k in ('path','line','sha256')}})
        for edge in connections['edges']:
            linked = []
            for a in mappings.get(edge['source'], ()):
                for b in mappings.get(edge['target'], ()):
                    linked.extend(by_pair.get((a,b), []))
                    if not edge['directed']: linked.extend(by_pair.get((b,a), []))
            candidates = by_edge.get(edge['id'], [])
            state = 'risk' if any(e['state']=='risk' for e in linked) else 'review' if candidates or linked else 'unknown'
            source_edges.append({**edge, 'state': state, 'candidates': candidates,
                                 'linked_handoffs': sorted({e['id'] for e in linked}),
                                 'risks': list({r['id']:r for e in linked for r in e['risks']}.values()),
                                 'evidence_ids': sorted({eid for e in linked for eid in e['evidence_ids']}),
                                 'interpretation': 'Source relationship; mapping a risk does not prove runtime propagation. Candidate findings need review.'})
        # Export the entire accepted graph, including isolated nodes and parallel edges.
        # Rendering/zoom controls must never silently sample the evidence network.
        source_nodes = list(all_nodes.values())
        notices.append('All supplied source nodes and edges are included. Source extraction coverage may still be incomplete; this is not a claim that every runtime connection was discovered.')
        notices.extend(connections['limitations'])
        notices.append('Source map freshness is not established by matching export hashes. Review the selected snapshot and evidence identities.')
    else:
        notices.append('No source graph supplied. The process map still shows the declared audit boundaries.')
    severity_order = {'critical':0, 'high':1, 'medium':2, 'low':3}
    tasks.sort(key=lambda item:(severity_order[item['priority']], not item['id'].startswith('risk:'), item['id']))
    scorecard = report.get('scorecard')
    return {'schema': 'software-assurance-visual/1', 'report_template_version': report['report_template_version'],
            'standard_version': report['standard_version'], 'scope': report['scope'], 'revision': report['revision'],
            'outcome': report['outcome'], 'report_digest': digest(report), 'connection_digest': digest(connections) if connections else None,
            'scorecard': scorecard, 'gates': report.get('gates', []), 'process_nodes': process_nodes, 'handoffs': handoffs,
            'source_nodes': source_nodes, 'source_edges': source_edges, 'source_coverage': connections.get('coverage') if connections else None,
            'source_totals': {'nodes': len(connections['nodes']), 'edges': len(connections['edges'])} if connections else {'nodes':0,'edges':0},
            'evidence': report.get('evidence_index', []), 'risks': risks,
            'unmapped_risks': [r['id'] for r in risks if r['id'] not in mapped_risks],
            'tasks': tasks, 'probes': connection_catalog(), 'notices': notices,
            'scope_issues': report.get('scope_issues', []),
            'interpretation': 'Evidence maturity, not a reliability percentage. Coverage includes static/design evidence. Red marks reviewed risk; amber marks partial review or an unconfirmed candidate. Graph reachability is not runtime causality.'}


def render_html(view):
    """Data is inert JSON; all target text is rendered using textContent."""
    template = (Path(__file__).parent / 'assets' / 'audit-view.html').read_text(encoding='utf-8')
    raw = json.dumps(view, ensure_ascii=True, allow_nan=False, separators=(',', ':')).encode('utf-8')
    # Large evidence networks travel as a compressed inert payload, avoiding an
    # enormous JavaScript object literal. All graph/evidence fields are retained.
    if len(raw) > 1024 * 1024:
        data = json.dumps({'encoding': 'gzip/base64', 'payload': base64.b64encode(gzip.compress(raw, compresslevel=3, mtime=0)).decode('ascii')})
    else:
        data = raw.decode('utf-8')
    data = data.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    network = (Path(__file__).parent / 'assets' / 'layout-worker.js').read_text(encoding='utf-8') + '\n' + (Path(__file__).parent / 'assets' / 'network.js').read_text(encoding='utf-8')
    return template.replace('/*__NETWORK_RENDERER__*/', network).replace('/*__AUDIT_DATA__*/null', data)
