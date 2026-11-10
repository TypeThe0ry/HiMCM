"""Run V203 controlled analyses against the staged V204 bounds, in an isolated tree."""
import csv
import hashlib
import json
import math
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import pandas as pd
import task4_v203_extensions as base
import task4_v203_mc_precision as precision
from task4_user_v204_revision import ROOT, revised_bounds, MANIFEST, sha

OUT = ROOT / 'results/task4_user_v204_extensions'

def main():
    if OUT.exists() and any(OUT.iterdir()):
        raise ValueError('Choose an absent or empty staged output directory')
    # Existing analysis functions use their module-global factory. Their inputs,
    # sensitivity definitions, seeds, diagnostics and checks remain unchanged.
    base.revised_bounds = revised_bounds
    OUT.mkdir(parents=True, exist_ok=True)
    for name in ('preferences','future','method','diagnostics'):
        folder = OUT / name; folder.mkdir()
        getattr(base,name)(folder)
        p=folder/'summary.json'; obj=json.loads(p.read_text())
        obj['version']='V204'; obj['primary']='V204 staged'; obj['activation_status']='staged_not_active'
        if name == 'method':
            for case in obj['method_cases']: case['evidence_version']='V204'
            for filename in ('method_ranks.csv','method_components.csv'):
                frame=pd.read_csv(folder/filename); assert set(frame.evidence_version)=={'V203'}
                frame['evidence_version']='V204'; frame.to_csv(folder/filename,index=False)
        # Historical labels in produced scope strings refer to the old binding.
        for key in ('scope','interpretation'):
            if isinstance(obj.get(key),str): obj[key]=obj[key].replace('rebased to V203','rebased to V204')
        p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
        print('V204',name,'complete',flush=True)
    # Use the existing simultaneous Hoeffding-box calculation with V204 outputs.
    precision.O = OUT/'mc_precision'
    precision.TABLES = [
      ('preferences','task4_user_v204_extensions/preferences/mc_city_summary.csv',precision.PREF,['profile','concentration']),
      ('future_shocks','task4_user_v204_extensions/future/future_mc_city_summary.csv',precision.FUTURE,['scenario','weight_reference','evidence_arm']),
      ('weights_only','task4_user_v204_extensions/future/weight_mc_city_summary.csv',precision.FUTURE,['scenario','weight_reference','evidence_arm','concentration'])]
    precision.main()
    p=precision.O/'summary.json'; obj=json.loads(p.read_text())
    obj.update(version='V204',primary_science='V204 staged',activation_status='staged_not_active',
               current_paper='unchanged',reran_monte_carlo=False,changed_scientific_inputs=False)
    obj['input_sha256'][str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__))
    obj['input_sha256']['scripts/task4_user_v204_revision.py']=sha(ROOT/'scripts/task4_user_v204_revision.py')
    obj['input_sha256'][str(MANIFEST.relative_to(ROOT))]=sha(MANIFEST)
    obj['excluded']=[x.replace('primary V203 18 cases and 108 MC settings','primary V204 29 cases and 174 MC settings') for x in obj['excluded']]
    p.write_text(json.dumps(obj,indent=2)+'\n')
    groups=defaultdict(list)
    with (precision.O/'mean_bounds.csv').open() as f:
        for row in csv.DictReader(f):
            if row['metric']=='mean_decision_rank': groups[row['family'],row['setting']].append(row)
    assert len(groups)==obj['settings']
    pairs=[]; settings=[]; cities=[]
    for (family,setting),group in sorted(groups.items()):
        assert len(group)==len({r['city'] for r in group})==16
        group.sort(key=lambda r:r['city']); better=defaultdict(list); worse=defaultdict(list); local=[]
        for a,b in combinations(group,2):
            lower=float(a['lower'])-float(b['upper']); upper=float(a['upper'])-float(b['lower'])
            kind='unresolved'
            if upper < -1e-12:
                kind='a_lower_expected_mean_rank'; better[b['city']].append(a['city']); worse[a['city']].append(b['city'])
            elif lower > 1e-12:
                kind='b_lower_expected_mean_rank'; better[a['city']].append(b['city']); worse[b['city']].append(a['city'])
            local.append(dict(family=family,setting=setting,city_a=a['city'],city_b=b['city'],sample_mean_a=float(a['estimate']),sample_mean_b=float(b['estimate']),gap_a_minus_b=float(a['estimate'])-float(b['estimate']),gap_lower=lower,gap_upper=upper,classification=kind))
        front=sorted(r['city'] for r in group if not better[r['city']]); minimum=min(float(r['estimate']) for r in group)
        for row in group:
            cities.append(dict(family=family,setting=setting,city=row['city'],sample_mean=float(row['estimate']),lower=float(row['lower']),upper=float(row['upper']),certified_better_cities=json.dumps(sorted(better[row['city']])),certified_worse_cities=json.dumps(sorted(worse[row['city']])),in_unresolved_front=not better[row['city']]))
        settings.append(dict(family=family,setting=setting,pairs=len(local),certified_pairs=sum(r['classification']!='unresolved' for r in local),unresolved_pairs=sum(r['classification']=='unresolved' for r in local),sample_mean_leaders=json.dumps(sorted(r['city'] for r in group if float(r['estimate'])==minimum)),unresolved_mean_rank_front=json.dumps(front),unique_smallest_expectation_certified=len(front)==1)); pairs.extend(local)
    assert len(pairs)==len(groups)*math.comb(16,2)
    out=OUT/'mean_rank_comparisons';out.mkdir()
    for name,rows in [('pairs.csv',pairs),('settings.csv',settings),('cities.csv',cities)]: precision.write_csv(out/name,rows)
    report=dict(version='V204',activation_status='staged_not_active',settings=len(groups),unordered_within_setting_pairs=len(pairs),certified_pairs=sum(r['classification']!='unresolved' for r in pairs),unresolved_pairs=sum(r['classification']=='unresolved' for r in pairs),settings_with_unique_smallest_expected_mean_rank=sum(r['unique_smallest_expectation_certified'] for r in settings),inherited_common_event_base_means=obj['base_means'],inherited_familywise_alpha=.05,additional_multiplicity_penalty=False,scope='Conditional simulation expected decision ranks; simultaneous mean boxes do not represent real-world city win probabilities.',arithmetic='[L_a-U_b,U_a-L_b], 1e-12 guard',input_sha256={'mean_bounds.csv':sha(precision.O/'mean_bounds.csv'),'precision_summary.json':sha(precision.O/'summary.json')})
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'summary.json').write_text(json.dumps(dict(version='V204',activation_status='staged_not_active',parts=['preferences','future','method','diagnostics','mc_precision','mean_rank_comparisons'],admissions_sha256=sha(MANIFEST),script_sha256=sha(Path(__file__)),scope='Controlled extensions use unchanged V203 assumptions and staged V204 bounds; no manuscript changes.'),indent=2)+'\n')
    print('V204 controlled extensions complete',flush=True)
if __name__=='__main__': main()
