import importlib.util, json, pathlib, time, ast, hashlib, statistics
ROOT=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('hidden_tests',ROOT/'tests/hidden_tests.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
results={}
for group,file in [('A','a_basic.py'),('B','b_engineering.py'),('C','c_manufacturing.py')]:
    path=ROOT/'implementations'/file
    spec=importlib.util.spec_from_file_location(group,path); impl=importlib.util.module_from_spec(spec); spec.loader.exec_module(impl)
    t=time.perf_counter(); tests=mod.run(impl.evaluate); elapsed=time.perf_counter()-t
    code=path.read_text(); results[group]={'passed':sum(v['pass'] for v in tests.values()),'total':len(tests),'elapsed_ms':round(elapsed*1000,3),'source_lines':len(code.splitlines()),'source_bytes':len(code.encode()),'sha256':hashlib.sha256(code.encode()).hexdigest(),'tests':tests}
(ROOT/'results'/'results.json').write_text(json.dumps(results,indent=2))
for k,v in results.items():print(k,v['passed'],'/',v['total'],'cases;',v['source_lines'],'lines;',v['elapsed_ms'],'ms')
