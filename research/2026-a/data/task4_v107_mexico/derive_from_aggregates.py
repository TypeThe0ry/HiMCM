"""Rebuild both bounds offline from published sufficient bins; raw ZIP not needed."""
from pathlib import Path
from collections import Counter
import hashlib,json,importlib.util
P=Path(__file__).resolve().parent
def derive_from_aggregates():
    spec=importlib.util.spec_from_file_location('mexico107_local_extract',P/'extract.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    bounds=module.bounds
    m=json.loads((P/'aggregate_manifest.json').read_text())
    assert hashlib.sha256((P/m['file']).read_bytes()).hexdigest()==m['sha256']
    for entry in json.loads((P/'manifest.json').read_text()):
        if not entry['local_only']:
            assert hashlib.sha256((P/entry['file']).read_bytes()).hexdigest()==entry['sha256']
    g=json.loads((P/'aggregate_bins.json').read_text())['groups']
    for row in g.values():
        assert sum(row['sample'].values())==row['sample_n']
        assert sum(row['weighted'].values())==row['expanded_n']
    a,b,c=[Counter(g[n]['weighted']) for n in ['prepa_conditional','boundary3','other_optional']]
    result={'legacy_progression':bounds(a+b,c),'boundary3_optional':bounds(a,b+c),'main_model_admission':False,'input_aggregate_sha256':m['sha256']}
    reference=json.loads((P/'summary.json').read_text())['scenarios']
    for n in ['legacy_progression','boundary3_optional']:
        assert abs(result[n][0]-reference[n]['utility_lower'])<1e-14
        assert abs(result[n][1]-reference[n]['utility_upper'])<1e-14
    return result

if __name__=='__main__':
    result=derive_from_aggregates()
    (P/'aggregate_bounds.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
