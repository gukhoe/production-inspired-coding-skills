from pathlib import Path
import subprocess,sys,time,json,hashlib
base=Path(__file__).resolve().parent
cmd=[sys.executable,'-m','unittest','-q','test_sample']
results={}
for mode in ('naive','risk_based'):
    runs=5 if mode=='naive' else 1
    start=time.perf_counter(); outputs=[]
    for i in range(runs):
        p=subprocess.run(cmd,cwd=base,capture_output=True,text=True)
        outputs.append({'exit':p.returncode,'stderr':p.stderr[-500:]})
    results[mode]={'test_invocations':runs,'wall_seconds':round(time.perf_counter()-start,4),'all_passed':all(o['exit']==0 for o in outputs)}
results['note']='Deterministic synthetic comparison: naive reruns unchanged tests five times; risk_based once. No LLM called. Not evidence of coding quality improvement.'
print(json.dumps(results,indent=2))
