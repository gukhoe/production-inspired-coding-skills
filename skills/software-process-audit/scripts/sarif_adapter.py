"""Bounded SARIF 2.1.0 findings import; locations are data, never file reads."""
import json


def from_sarif(data, sha, error):
    def obj(value, name):
        if not isinstance(value, dict):
            raise error('SARIF '+name+' must be an object')
        return value

    if not isinstance(data, dict) or data.get('version') != '2.1.0' or not isinstance(data.get('runs'), list):
        raise error('Expected a SARIF 2.1.0 log with runs')
    nodes, edges, findings, notices = [], [], [], []
    count = 0
    for ri, run in enumerate(data['runs']):
        if not isinstance(run, dict) or not isinstance(run.get('results', []), list):
            raise error('SARIF runs/results must be objects/arrays')
        driver = obj(obj(run.get('tool', {}), 'tool').get('driver', {}), 'driver')
        artifacts = run.get('artifacts', [])
        rules = driver.get('rules', [])
        if not isinstance(artifacts, list) or not isinstance(rules, list):
            raise error('SARIF artifacts/rules must be arrays')
        defaults = {}
        for rule_record in rules:
            rule_record = obj(rule_record, 'rule')
            default_level = obj(rule_record.get('defaultConfiguration', {}), 'defaultConfiguration').get('level', 'warning')
            defaults[str(rule_record.get('id', ''))] = default_level
        for index, result in enumerate(run.get('results', [])):
            count += 1
            if count > 10000:
                raise error('SARIF limit: 10000 results; split the input')
            if not isinstance(result, dict) or not isinstance(result.get('message'), dict):
                raise error('SARIF result requires a message object')
            key = f'sarif:{ri}:{index}'
            rule = str(result.get('ruleId', 'unidentified-rule'))
            message = str(result['message'].get('text', result['message'].get('markdown', 'No plain message')))
            provenance = {'provider': 'SARIF', 'export_sha256': sha, 'run_index': ri, 'result_index': index,
                          'tool': driver, 'result': result, 'originalUriBaseIds': run.get('originalUriBaseIds', {}),
                          'versionControlProvenance': run.get('versionControlProvenance', [])}
            nodes.append({'id': key, 'label': rule, 'kind': 'static diagnostic', 'provenance': provenance})
            locations = result.get('locations', [])
            if not isinstance(locations, list) or len(locations) > 100:
                raise error('SARIF limit: 100 locations per result')
            if not locations:
                notices.append(f'{key}: no source location; retained as an unlocated diagnostic')
                locations = [{}]
            for li, location in enumerate(locations):
                if len(edges) >= 50000:
                    raise error('SARIF limit: 50000 locations; split the input')
                if not isinstance(location, dict):
                    raise error('SARIF locations must be objects')
                physical = obj(location.get('physicalLocation', {}), 'physicalLocation')
                artifact = obj(physical.get('artifactLocation', {}), 'artifactLocation')
                artifact_index = artifact.get('index')
                if artifact_index is not None:
                    if type(artifact_index) is not int or not 0 <= artifact_index < len(artifacts):
                        raise error('SARIF artifact index is out of range')
                    entry = obj(artifacts[artifact_index], 'artifact')
                    artifact = {**obj(entry.get('location', {}), 'artifact location'), **artifact}
                uri = str(artifact.get('uri', ''))
                line = obj(physical.get('region', {}), 'region').get('startLine')
                loc_id = f'{key}:location:{li}'
                nodes.append({'id': loc_id, 'label': uri or 'Unlocated finding', 'kind': 'SARIF location', 'path': uri, 'line': line,
                              'provenance': {'artifactLocation': artifact, 'location': location}})
                edge_id = f'{key}:edge:{li}'
                edges.append({'id': edge_id, 'source': key, 'target': loc_id, 'relation': 'diagnostic location (not a call)',
                              'directed': False, 'confidence': 'UNKNOWN', 'provenance': provenance})
                level = result.get('level', defaults.get(rule, 'warning'))
                if not isinstance(level, str) or level not in {'error', 'warning', 'note', 'none'}:
                    raise error('SARIF diagnostic level is invalid')
                suppressed = bool(result.get('suppressions'))
                severity = {'error': 'high', 'warning': 'medium', 'note': 'low', 'none': 'low'}.get(level, 'medium')
                findings.append({'id': f'{key}:finding:{li}', 'edge_id': edge_id, 'state': 'candidate', 'severity': severity,
                                 'rule': rule, 'title': message, 'failure_scenario': 'Imported static diagnostic; inspect context and reproduce. '+('Suppression metadata present; do not silently discard or confirm.' if suppressed else ''),
                                 'improvement': 'Review the original rule and affected boundary before changing code.',
                                 'verification': 'Exercise a discriminating failure case and an adjacent valid case.', 'path': uri, 'line': line})
    normalized = {'schema': 'software-assurance-connections/1', 'provider': 'SARIF 2.1.0', 'source_sha256': sha,
            'nodes': nodes, 'edges': edges, 'findings': findings,
            'coverage': {'status': 'unknown', 'runs': len(data['runs']), 'results': count},
            'limitations': ['SARIF is an interchange format, not verification of scanner truth, freshness or completeness.',
                           'URI/base IDs and suppression/fingerprint/code-flow metadata are retained as data. No URI is fetched and no referenced file is read.',
                           'Location edges describe diagnostics, not program calls. Markdown messages are rendered as inert text.'] + notices}
    # Large rule catalogs/code flows can otherwise multiply at every diagnostic location.
    size = 0
    for chunk in json.JSONEncoder(ensure_ascii=True).iterencode(normalized):
        size += len(chunk)
        if size > 32*1024*1024:
            raise error('SARIF normalized evidence exceeds 32 MiB; split the input')
    return normalized
