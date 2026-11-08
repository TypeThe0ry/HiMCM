"""Independent long-double endpoint enclosures; no model or root-solver imports."""
import csv, hashlib, itertools, json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
D=np.longdouble

def rows(p):
    with p.open() as f:return list(csv.DictReader(f))

def score(x,a):
    w=np.full(10,(1-a)/8,dtype=D);w[[6,9]]=a/2
    pos=np.sqrt((w*x*x).sum(axis=1));neg=np.sqrt((w*(1-x)**2).sum(axis=1))
    return 100*pos/(pos+neg)

s=json.loads((P/'summary.json').read_text())
prior=P.parent/'task4_v103_joint_acquisition'
assert hashlib.sha256((prior/'summary.json').read_bytes()).hexdigest()==s['source_summary_sha256']
raw=rows(P.parent/'task4_v102_intake/utility_bounds.csv')
cities=list(dict.fromkeys(r['city'] for r in raw));names=list(dict.fromkeys(r['indicator'] for r in raw))
lo=np.array([D(r['lower']) for r in raw]).reshape(25,10);hi=np.array([D(r['upper']) for r in raw]).reshape(25,10)
assert hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()==s['input_bounds_sha256']
mask=np.zeros_like(lo,dtype=bool);mask[:,[names.index(x) for x in s['measured_indicators']]]=True
required=tuple(cities.index(c) for c in s['required_cities'])
worst=np.where(mask,lo,hi);rivalbest=np.where(mask,hi,lo)
mandatory=[]
for r in rows(prior/'unavoidable_certificates.csv'):
    if r['scenario']==s['scenario'] and r['continuous_unavoidable']=='True':
        i=int(r['index']);a=D(r['witness_alpha'])
        gap=score(worst,a)[i]-np.delete(score(rivalbest,a),i).max()
        assert gap>D('1e-8')
        mandatory.append({'city':cities[i],'alpha':float(a),'strict_gap':float(gap)})
assert tuple(cities.index(r['city']) for r in mandatory)==required
expected={tuple(sorted(required+extra)) for n in (0,1) for extra in itertools.combinations([i for i in range(25) if i not in required],n)}
assert len(expected)==23 and {tuple(r['keep_indices']) for r in s['records']}==expected
assert len(s['records'])==23
negative=[];positive=[];leaf_count=0;minimum_gap=D('100')
for r in s['records']:
    keep=r['keep_indices'];assert r['size']==len(keep)
    chosen=np.zeros(25,bool);chosen[keep]=True
    point=np.where(chosen[:,None],hi,lo)
    lower=np.where(mask,point,lo);upper=np.where(mask,point,hi)
    assert np.all(lower[mask]==upper[mask])
    if r['status']=='excluded_by_strict_witness':
        i=r['outside_index'];a=D(r['alpha']);assert i not in keep and D('.05')<=a<=D('.2')
        gap=score(upper,a)[i]-score(lower,a)[keep].max()
        assert gap>D('1e-8') and abs(gap-D(r['score_gap']))<D('1e-11')
        negative.append({'keep':keep,'outsider':cities[i],'alpha':float(a),'strict_gap':float(gap)})
    else:
        assert r['status']=='feasible_survivor_superset'
        outsiders=np.flatnonzero(~chosen)
        # Each individual TOPSIS score is monotone in alpha: its squared
        # positive/negative-distance ratio is linear-fractional. Endpoint
        # extrema therefore enclose each score throughout each subinterval.
        stack=[(D('.05'),D('.2'),0)];leaves=[]
        while stack:
            a,b,depth=stack.pop()
            ls=np.array([score(lower,t)[keep] for t in (a,b)])
            us=np.array([score(upper,t)[outsiders] for t in (a,b)])
            gap=ls.min(axis=0).max()-us.max(axis=0).max()-D('2e-9')
            if gap>D('1e-8'):
                leaves.append({'lower':float(a),'upper':float(b),'gap_lower':float(gap)})
                minimum_gap=min(minimum_gap,gap)
            else:
                assert depth<24, 'Could not independently certify an exclusion interval'
                mid=(a+b)/2;stack.extend([(a,mid,depth+1),(mid,b,depth+1)])
        leaves.sort(key=lambda x:x['lower']);assert leaves[0]['lower']==.05 and leaves[-1]['upper']==.2
        assert all(x['upper']==y['lower'] for x,y in zip(leaves,leaves[1:]))
        leaf_count+=len(leaves);positive.append({'keep':keep,'leaves':leaves})
assert len(negative)==22 and len(positive)==1
assert positive[0]['keep']==[1,7,22,23]
assert s['successful_sets']==[x['keep'] for x in positive]
assert s['certified_minimum']==s['attained_upper_bound']==4 and s['minimum_proved']
result=dict(method='Independent long-double score evaluation and adaptive endpoint enclosures, no main model or polynomial solver imports',
 input_hash_verified=True,mandatory_three_strict_witnesses=mandatory,all_23_candidate_sets_verified=True,
 excluded_sets=negative,feasible_sets=positive,continuous_exclusion_leaves=leaf_count,
 minimum_continuous_score_gap_lower=float(minimum_gap),certified_minimum=4,
 successful_city_sets=s['successful_city_sets'],
 logic_review='Outsider upper score is compared to maximum lower score within K. Endpoint reduction and shared-alpha quantifiers are valid in the independent rectangular model. Minimum relies on verified mandatory three and exclusion of their unique size-three superset.',
 limitation='Numerical padded enclosures, not formally directed-rounded interval arithmetic; conditional hypothetical endpoint revelations, no observed-data admission.')
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('excluded_sets','feasible_sets')},indent=2))
