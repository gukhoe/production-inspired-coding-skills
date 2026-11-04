import copy
import base64
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'skills/software-process-audit/scripts'))
import audit
from connection_audit import SCHEMA, import_connections, related_paths, scan_python, validate_connections
from visual_report import build_view, render_html


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def scan(self, text):
        (self.root/'source.py').write_text(text, encoding='utf-8')
        return scan_python(self.root, ['source.py'])

    def graph(self, directed=True):
        return {'schema':SCHEMA,'provider':'fixture','nodes':[{'id':n,'label':n} for n in 'ABC'],
                'edges':[{'id':a+b,'source':a,'target':b,'relation':'calls','directed':directed,'confidence':'EXTRACTED','provenance':{}} for a,b in [('A','B'),('B','C')]],
                'findings':[],'coverage':{'status':'unknown'},'limitations':['Synthetic fixture']}

    def report(self):
        m=audit.new_manifest('snapshot','Synthetic test scope')
        m['processes']=[{'id':p,'kind':'runtime','owner':'Team','input':'request','output':'response','code_nodes':[p]} for p in 'ABC']
        m['boundaries']=[{'id':'AB','source':'A','target':'B','failure_mode':'Replay may duplicate a mutation','reviews':{}}]
        m['risks']=[{'id':'R1','severity':'high','status':'open','failure_mode':'Replay duplicates mutation','impact':'Incorrect state','targets':['boundary:AB'],'verification':audit.blank_review()}]
        return audit.evaluate(m,self.root,'snapshot')

    def test_source_scan_does_not_execute_target(self):
        graph=self.scan("raise RuntimeError('must never execute')\nimport requests\ndef f(url):\n return requests.get(url, verify=False)\n")
        self.assertEqual({f['rule'] for f in graph['findings']},{'PY-TLS','PY-TIMEOUT'})
        self.assertTrue(all(f['state']=='candidate' for f in graph['findings']))
        self.assertTrue(all(f['sha256']==graph['coverage']['selected_files'][0]['sha256'] for f in graph['findings']))

    def test_aliases_and_explicit_unbounded_timeout(self):
        g=self.scan('from requests import get as fetch\nfetch(url, timeout=None)\n')
        self.assertEqual([f['rule'] for f in g['findings']],['PY-TIMEOUT'])

    def test_explicit_controls_remove_only_known_patterns(self):
        g=self.scan('import requests\nimport subprocess\nrequests.get(url, timeout=5, verify=True)\nsubprocess.run(args, shell=False)\n')
        self.assertEqual(g['findings'],[])
        self.assertEqual(g['coverage']['status'],'partial')
        self.assertIn('No finding', ' '.join(g['limitations']))

    def test_shadowed_import_not_mistaken_for_real_library(self):
        self.assertEqual(self.scan('import requests\ndef f(requests):\n return requests.get(url,verify=False)\n')['findings'],[])

    def test_dynamic_kwargs_do_not_claim_missing_timeout(self):
        self.assertEqual(self.scan('import requests\nrequests.get(url, **options)\n')['findings'],[])

    def test_malformed_source_remains_visible(self):
        g=self.scan('def broken(:\n')
        self.assertEqual(g['coverage']['parse_errors'][0]['error'],'SyntaxError')
        self.assertEqual(g['coverage']['status'],'partial')

    def test_path_escape_and_invalid_input_rejected(self):
        with self.assertRaises(audit.AuditError):scan_python(self.root,['../outside.py'])
        with self.assertRaises(audit.AuditError):scan_python(self.root,[{}])

    def test_directed_paths_and_reverse_paths_are_distinct(self):
        self.assertEqual(set(related_paths(self.graph(),'C')['paths']),{'C'})
        self.assertEqual(set(related_paths(self.graph(),'C',direction='incoming')['paths']),set('ABC'))
        self.assertEqual(set(related_paths(self.graph(False),'C')['paths']),set('ABC'))

    def test_limits_disclose_incomplete_traversal(self):
        r=related_paths(self.graph(),'A',depth=1)
        self.assertTrue(r['truncated'])
        self.assertNotIn('C',r['paths'])

    def test_parallel_edges_remain_distinct(self):
        g=self.graph();g['edges'].append({**g['edges'][0],'id':'parallel','relation':'imports'})
        self.assertEqual(len(validate_connections(g)['edges']),3)

    def test_malformed_candidate_and_confidence_raise_audit_error(self):
        g=self.graph();g['edges'][0]['confidence']=[]
        with self.assertRaises(audit.AuditError):validate_connections(g)
        g=self.graph();g['findings']=[{'id':'F','edge_id':[],'state':'candidate','severity':'high'}]
        with self.assertRaises(audit.AuditError):validate_connections(g)

    def test_native_local_import_connects_selected_modules(self):
        (self.root/'gateway.py').write_text('from store import apply_event\napply_event(event)\n')
        (self.root/'store.py').write_text('def apply_event(event):\n return event\n')
        g=scan_python(self.root,['gateway.py','store.py'])
        edge=next(e for e in g['edges'] if e['relation']=='imports')
        self.assertEqual((edge['source'],edge['target']),('file:gateway.py','file:store.py'))
        self.assertEqual(edge['confidence'],'INFERRED')

    def test_invalid_endpoints_or_runtime_labels_rejected(self):
        g=self.graph();g['edges'][0]['target']='missing'
        with self.assertRaises(audit.AuditError):validate_connections(g)
        g=self.graph();g['edges'][0]['confidence']='RUNTIME_OBSERVED'
        with self.assertRaises(audit.AuditError):validate_connections(g)

    def test_graphify_preserves_undirected_and_unknown_confidence(self):
        d={'graph':{'schema_version':1},'directed':False,'multigraph':True,'nodes':[{'id':'A'},{'id':'B'}],
           'links':[{'source':'A','target':'B','confidence':'AMBIGUOUS','relation':'calls'}]}
        p=self.root/'export.json';p.write_text(json.dumps(d))
        g=import_connections(p,'graphify')
        self.assertFalse(g['edges'][0]['directed'])
        self.assertEqual(g['edges'][0]['confidence'],'UNKNOWN')
        self.assertEqual(g['edges'][0]['provenance']['original_confidence'],'AMBIGUOUS')

    def test_rea_observed_means_static_not_runtime(self):
        # Minimal portable shape from actual REA JavaScript application evidence.
        d={'operation':'analyze_javascript_application','evidence_id':'fixture','limitations':[],
           'normalized_result':{'graph':{'schema':'JavaScriptApplicationGraph','nodes':[
               {'node_id':n,'kind':'javascript-module','observations':[{'label':n,'evidence':{}}]} for n in 'AB'],
               'edges':[{'edge_id':'E','source_node_id':'A','target_node_id':'B','relation':'calls','evidence':{'state':'observed','authority':'ast-static-analysis'}}],
               'coverage':{'status':'partial'}}}}
        p=self.root/'rea.json';p.write_text(json.dumps(d));g=import_connections(p,'rea')
        self.assertEqual(g['edges'][0]['confidence'],'EXTRACTED')
        self.assertEqual(g['coverage']['status'],'unknown')
        self.assertIn('not runtime',' '.join(g['limitations']))
        d['normalized_result']={'kind':'summary'};p.write_text(json.dumps(d))
        with self.assertRaises(audit.AuditError):import_connections(p,'rea')

    def test_visual_risk_mapping_does_not_change_scores(self):
        r=self.report();before=copy.deepcopy(r);v=build_view(r,self.graph())
        self.assertEqual(v['handoffs'][0]['state'],'risk')
        self.assertEqual(v['source_edges'][0]['state'],'risk')
        self.assertEqual(v['source_edges'][0]['risks'][0]['id'],'R1')
        self.assertEqual(v['tasks'][0]['id'],'risk:R1')
        self.assertTrue(any(t['state']=='unverified' for t in v['tasks']))
        self.assertEqual(r,before)
        self.assertEqual(v['scorecard'],r['scorecard'])

    def test_undirected_mapping_does_not_invent_causality(self):
        r=self.report();g=self.graph(False);g['edges'][0]['source']='B';g['edges'][0]['target']='A'
        v=build_view(r,g)
        edge=next(e for e in v['source_edges'] if e['id']=='AB')
        self.assertEqual(edge['state'],'risk');self.assertFalse(edge['directed'])

    def test_closed_risk_does_not_hide_unknown_reviews(self):
        r=self.report();r['risks'][0]['effective_status']='closed'
        v=build_view(r)
        self.assertEqual(v['handoffs'][0]['state'],'review')

    def test_unmapped_risks_remain_visible(self):
        r=self.report();r['risks'][0]['targets']=['IMP-02']
        v=build_view(r)
        self.assertEqual(v['unmapped_risks'],['R1'])
        self.assertTrue(any(t['id']=='risk:R1' for t in v['tasks']))

    def test_candidates_do_not_become_confirmed_red_risks(self):
        g=self.scan('import requests\nrequests.get(url,verify=False)\n')
        v=build_view(self.report(),g)
        self.assertTrue(any(e['state']=='review' for e in v['source_edges']))
        self.assertFalse(any(e['state']=='risk' for e in v['source_edges']))
        self.assertTrue(any(t['state']=='candidate' for t in v['tasks']))

    def test_full_view_preserves_nodes_edges_and_isolates_beyond_old_caps(self):
        g=self.graph();g['nodes'] += [{'id':str(i),'label':str(i)} for i in range(1200)]
        g['edges'] += [{**g['edges'][0], 'id':str(i), 'source':str(i%1199), 'target':str((i+1)%1199)} for i in range(3000)]
        v=build_view(self.report(),g)
        self.assertEqual({n['id'] for n in v['source_nodes']},{n['id'] for n in g['nodes']})
        self.assertEqual({e['id'] for e in v['source_edges']},{e['id'] for e in g['edges']})
        self.assertEqual(len(v['source_edges']),3002)
        self.assertEqual(v['source_totals'],{'nodes':1203,'edges':3002})
        self.assertTrue(any('All supplied' in n for n in v['notices']))

    def test_html_does_not_execute_target_markup(self):
        r=self.report();r['scope']='</script><script>window.injected=true</script>'
        html=render_html(build_view(r))
        self.assertNotIn(r['scope'],html)
        self.assertIn('\\u003c/script',html)
        self.assertIn("connect-src 'none'",html)
        self.assertNotIn('innerHTML',html)

    def test_large_payload_roundtrip_preserves_all_evidence(self):
        view=build_view(self.report(),self.graph())
        view['notices'].append('Evidence text '+('x'*1100000))
        html=render_html(view)
        encoded=html.split('const D=await readAuditData(',1)[1].split(');',1)[0]
        payload=json.loads(encoded)
        self.assertEqual(payload['encoding'],'gzip/base64')
        decoded=json.loads(gzip.decompress(base64.b64decode(payload['payload'])))
        self.assertEqual(decoded,view)
        self.assertLess(len(html),len(view['notices'][-1]))

    def test_cli_outputs_html_and_preserves_overwrite_guard(self):
        m=audit.new_manifest('snapshot','Unassessed test')
        manifest=self.root/'review.json';manifest.write_text(json.dumps(m))
        out=self.root/'result'
        args=['report','--repo',str(self.root),'--manifest',str(manifest),'--revision','snapshot','--out',str(out)]
        self.assertEqual(audit.main(args),0)
        self.assertTrue((out/'report.html').exists())
        self.assertTrue((out/'improvement-plan.json').exists())
        self.assertEqual(audit.main(args),2)


if __name__=='__main__':unittest.main()
