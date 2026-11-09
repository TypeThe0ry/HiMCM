"""Independent Decimal arithmetic, source coverage and immutable-file checks."""
from pathlib import Path
from decimal import Decimal, localcontext
import ast, csv, hashlib, json
R=Path(__file__).resolve().parents[1]; O=R/'results/task4_v169_mc_precision'; P=R.parents[2]/'HiMCM-Overleaf'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def csvrows(p):
    with p.open() as f: return list(csv.DictReader(f))
def literal_constants(path):
    result={}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node,ast.Assign):
            try: value=ast.literal_eval(node.value)
            except (ValueError,TypeError): continue
            for target in node.targets:
                if isinstance(target,ast.Name): result[target.id]=value
                elif isinstance(target,ast.Tuple): result.update(zip([x.id for x in target.elts],value))
    return result
s=read(O/'summary.json'); bounds=csvrows(O/'mean_bounds.csv')
assert len(bounds)==2064
with localcontext() as ctx:
    ctx.prec=50
    epsilon=((Decimal(2*2064)/Decimal('.05')).ln()/Decimal(20000)).sqrt()
assert abs(float(epsilon)-s['normalized_half_width'])<1e-16
assert literal_constants(R/'scripts/task4_v122_preferences.py')['DRAWS']==10000
assert literal_constants(R/'scripts/task4_v122_future.py')['DRAWS']==10000
specs={
 'preferences':('task4_v154_preferences/mc_city_summary.csv', ['profile','concentration'], ['minimax_recommendation_frequency','mean_decision_rank','top3_decision_frequency','possible_champion_frequency','necessary_champion_frequency'],144),
 'future_shocks':('task4_v154_future/future_mc_city_summary.csv',['scenario','weight_reference','evidence_arm'],['recommendation_frequency','possible_champion_frequency','mean_decision_rank'],192),
 'weights_only':('task4_v154_future/weight_mc_city_summary.csv',['scenario','weight_reference','evidence_arm','concentration'],['recommendation_frequency','possible_champion_frequency','mean_decision_rank'],256)}
keys=set()
for family,(name,fields,metrics,count) in specs.items():
    raw=csvrows(R/'results'/name); assert len(raw)==count
    source={(json.dumps({k:x[k] for k in fields},sort_keys=True),x['city']):x for x in raw}
    for x in [x for x in bounds if x['family']==family]:
        key=(family,x['setting'],x['city'],x['metric']); assert key not in keys; keys.add(key)
        assert x['metric'] in metrics
        original=source[(x['setting'],x['city'])]
        assert float(x['estimate'])==float(original[x['metric']])
        a,b=(1,16) if x['metric']=='mean_decision_rank' else (0,1)
        h=(b-a)*float(epsilon); v=float(x['estimate'])
        assert abs(float(x['half_width'])-h)<1e-15
        assert float(x['lower'])==max(a,v-h) and float(x['upper'])==min(b,v+h)
    assert sum(x['family']==family for x in bounds)==len(raw)*len(metrics)
for n,h in s['input_sha256'].items(): assert sha(R/n)==h
science=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
for n,h in science.items(): assert sha(R/n)==h,n
protected=read(O/'protected_files.json')['manuscript']
for n,h in protected.items(): assert sha(P/n)==h,n
source=read(O/'source.json'); assert sha(O/'hoeffding_1963.pdf')==source['sha256']
examples=csvrows(O/'published_examples.csv'); assert len(examples)==5
assert all(x in bounds for x in examples)
assert s['reran_monte_carlo']==s['changed_manuscript']==s['changed_scientific_inputs']==False
verification=dict(version='V169',passed=True,base_means_checked=len(bounds),
 frequency_means=1472,mean_rank_means=592,draws_per_setting=10000,
 science_files_unchanged=len(science),existing_overleaf_files_unchanged=len(protected),
 checks=['50-digit Decimal formula','AST sample-size constants','complete metric/city/setting coverage',
 'every estimate matched to frozen CSV','all clipped endpoints and ranges','input SHA256',
 '187 science snapshot hashes','all existing manuscript hashes','original theorem scan SHA256',
 'five published examples matched'],
 independent_agent_review='education: counts, formula, bounded fractional ties, rank ranges and shared-draw assumptions independently reviewed read-only.',
 current_paper='V168 unchanged; no compile repeated because no manuscript or assets changed',
 raw_draws_replayed=False,submission_ready=False)
(O/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps(verification))
