"""Reproduce a connection defect and its correction; produce two actual audit views."""
import argparse
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'skills/software-process-audit/scripts'))
import audit
from connection_audit import scan_python
from visual_report import build_view, render_html


def run(out, fixed):
    out.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).parent/'system'
    for name in ('client.py','gateway.py','exercise.py'):
        shutil.copy2(source/name, out/name)
    shutil.copy2(source/('store_fixed.py' if fixed else 'store.py'), out/'store.py')
    (out/'requirements.txt').write_text('Synthetic scope: local HTTP event submission; valid positive integer events add their amount once per event ID. Replaying an event must not repeat the mutation. Invalid amounts return 400 before mutation. A different event remains valid. Excluded: persistence, restart, concurrency, deployment, authentication, TLS and remote networks.\n', encoding='utf-8')
    (out/'design.txt').write_text('Client sends JSON over loopback HTTP to a single-threaded gateway. Gateway validates before invoking the store. Store owns balance and event IDs. Each request reads the returned result. Demo maintainer owns all three roles. A response lost after commit can cause a replay; idempotent admission must happen at the mutation boundary.\n', encoding='utf-8')
    revision = audit.file_hash(out/'store.py')
    command = [sys.executable, 'exercise.py']
    timestamp = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, cwd=out, capture_output=True, text=True, timeout=15)
    expected = 0 if fixed else 1
    if result.returncode != expected:
        raise AssertionError('Unexpected demo outcome: '+result.stdout+result.stderr)
    observations = json.loads(result.stdout)
    assert observations['checks']['duplicate_replay'] is fixed
    (out/'execution.txt').write_text(result.stdout+result.stderr, encoding='utf-8')
    m = audit.new_manifest(revision, 'Synthetic connection audit: local HTTP client → gateway → in-memory ledger. Actual replay and invalid-input checks; persistence, concurrency, restart, deployment and security remain outside this sample.')
    for eid, path, kind in [('E-REQ','requirements.txt','document'),('E-DES','design.txt','document'),('E-CLIENT','client.py','source'),('E-GATEWAY','gateway.py','source'),('E-STORE','store.py','source'),('E-RUN','execution.txt','execution')]:
        e = audit.evidence_record(out,path,eid,kind,revision)
        e.update(locator='Entire small synthetic file',summary='Directly inspected demo evidence: '+path)
        if kind=='execution':e.update(command=json.dumps(command),recorded_at=timestamp,exit_code=result.returncode)
        m['evidence'].append(e)
    def review(status,score,evidence,rationale,**extra):
        return {**audit.blank_review(),'status':status,'score':score,'evidence':evidence,'reviewer':'Synthetic example reviewer','rationale':rationale,'owner':'Demo maintainer','due':'Before accepting this demo scenario',**extra}
    m['scope_review']=review('supported',4,['E-REQ','E-DES'],'The intentionally small example and excluded behaviors are explicit.')
    m['processes']=[{'id':pid,'label':title,'kind':'runtime','owner':'Demo maintainer','input':inp,'output':output,'code_nodes':['file:'+path]}
                    for pid,title,inp,output,path in [('client','HTTP client','Event ID and amount','HTTP request','client.py'),('gateway','Gateway','JSON request','Validated event or 400','gateway.py'),('store','Ledger','Validated event','Balance response','store.py')]]
    for c in m['assessments']:
        if c['id'] in {'REQ-01','REQ-02','DES-01','MAP-01'}:
            for check in c['checks']:
                check.update(review('supported',4,['E-REQ','E-DES','E-CLIENT','E-GATEWAY','E-STORE'],'Requirements, roles and limits are explicit and matched to the small source sample. No production completeness claim.'))
        elif c['id']=='DES-02':
            for check in c['checks']:
                check.update(review('partial',2,['E-DES','E-GATEWAY','E-STORE'],'The replay boundary is identified; full contract and failure-mode coverage remains incomplete.'))
        elif c['id']=='PRE-01':
            c['checks'][0].update(review('partial',2,['E-GATEWAY'],'Positive integer admission is visible; broader authorization and threat controls are unassessed.'))
            c['checks'][1].update(review('supported' if fixed else 'gap',4 if fixed else 0,['E-STORE','E-RUN'],
                'The corrected replay returns 110 with no repeat mutation.' if fixed else 'Actual replay returns 120 instead of 110.',
                finding='' if fixed else 'Duplicate event changes state twice.',improvement='' if fixed else 'Reject previously applied event IDs before state mutation.'))
            c['checks'][2].update(review('supported' if fixed else 'gap',4 if fixed else 0,['E-RUN'],
                'Replay, invalid amount and adjacent valid event passed in this process.' if fixed else 'The replay prevention challenge fails.',
                improvement='' if fixed else 'Re-run the replay challenge and neighboring valid event after correction.'))
        elif c['id']=='VER-01':
            for check in c['checks']:
                check.update(review('partial',2,['E-REQ','E-RUN'],'Independent expected balances and rejection status are explicit; the selected scenarios are limited.'))
    reviews={'contract':review('supported',4,['E-REQ','E-DES'],'Declared event and response contract is explicit.'),
             'failure_handling':review('partial',2,['E-GATEWAY'],'Invalid input is rejected; unavailable-peer behavior remains unverified.'),
             'recovery':audit.blank_review(),
             'verification':review('partial',2,['E-RUN'],'The loopback scenario executed; timeout/disconnect/restart cases were not exercised.'),
             'observability':review('partial',2,['E-RUN'],'The scenario prints observations; operational cross-service diagnostics are unassessed.')}
    m['boundaries']=[{'id':'http-submit','source':'client','target':'gateway','failure_mode':'A response lost after commit can lead the caller to retry.','reviews':copy.deepcopy(reviews)},
                     {'id':'ledger-write','source':'gateway','target':'store','failure_mode':'A replayed event must not mutate the balance twice.','reviews':copy.deepcopy(reviews)}]
    m['boundaries'][1]['reviews']['verification']=review('supported' if fixed else 'gap',4 if fixed else 0,['E-RUN','E-STORE'],
        'Replay and adjacent event checks passed on the corrected source.' if fixed else 'Observed duplicate balance 120, expected 110.',
        finding='' if fixed else 'Mutation is not idempotent.',improvement='' if fixed else 'Check the event ID before mutation and re-run replay plus adjacent event checks.')
    m['risks']=[{'id':'R-REPLAY','severity':'high','status':'closed' if fixed else 'open','targets':['PRE-01','boundary:ledger-write'],
                'failure_mode':'Replay changes the ledger twice','impact':'An acknowledged operation can produce an incorrect balance after retry.',
                'owner':'Demo maintainer','due':'Before accepting this demo scenario','action':'Add event-ID admission before mutation and recheck replay plus adjacent valid event.',
                'verification':review('supported',4,['E-RUN','E-STORE'],'Corrected replay, invalid input and adjacent valid event passed.') if fixed else audit.blank_review()}]
    case=audit.investigation_template('corrective','I-REPLAY',['PRE-01','boundary:ledger-write'])
    case['steps']['problem_definition']=review('supported',4,['E-REQ','E-RUN'],'Regression target: replay must preserve 110. Current success only covers the declared scenario; historical failure evidence belongs to the separate before report.' if fixed else 'Expected 110, observed 120 after the same event twice.')
    m['investigations']=[case]
    connections=scan_python(out,['client.py','gateway.py','store.py'])
    report=audit.evaluate(m,out,revision)
    view=build_view(report,connections)
    for name,data in [('review.json',m),('report.json',report),('connections.json',connections),('view.json',view)]:
        (out/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    (out/'report.md').write_text(audit.markdown(report),encoding='utf-8')
    (out/'report.html').write_text(render_html(view),encoding='utf-8')
    return {'exit_code':result.returncode,'checks':observations['checks'],'outcome':report['outcome'],
            'open_high_risks':report['open_high_or_critical_risks'],'scores':report['scorecard']['overall']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args()
    out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=False)
    results={name:run(out/name,fixed) for name,fixed in [('before',False),('after',True)]}
    (out/'comparison.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
