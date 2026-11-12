"""Turn a portable skill form into document evidence without assigning scores."""


def register(root, path, eid, revision):
    if __package__:
        from .audit import safe_file, evidence_record, CONTROLS, AuditError
        from .graph_adapter import read_json
    else:
        from audit import safe_file, evidence_record, CONTROLS, AuditError
        from graph_adapter import read_json
    data, _ = read_json(safe_file(root, path), max_bytes=1024*1024)
    if not isinstance(data, dict) or data.get('schema') != 'software-skill-record/1' or data.get('revision') != revision:
        raise AuditError('Skill record schema/revision mismatch')
    if not all(isinstance(data.get(key), str) and data[key].strip() for key in ('skill', 'author', 'status')) or data['status'] not in {'PASS','FAIL','BLOCKED','UNVERIFIED'}:
        raise AuditError('Skill record needs skill, author and an explicit check status')
    targets = data.get('criterion_targets')
    if not isinstance(targets, list) or not targets or any(not isinstance(t,str) or t not in {c[0] for c in CONTROLS} for t in targets):
        raise AuditError('Skill record requires known criterion targets')
    observations = data.get('observations')
    if not isinstance(observations, dict) or not observations or not any(isinstance(v,str) and v.strip() for v in observations.values()):
        raise AuditError('Blank skill forms are not assessed evidence')
    evidence = evidence_record(root,path,eid,'document',revision)
    evidence.update(locator='observations', summary='Reviewer-authored '+str(data['skill'])+' record; claimed '+data['status']+' is not an execution attestation.')
    return {'evidence': evidence, 'criterion_targets': targets, 'note': 'Document evidence only. Register raw source/execution separately; no assessment or risk is automatically closed.'}
