"""Independent acquisition proof replay from saved bounds; no model imports."""
import csv,hashlib,itertools,json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
D=np.longdouble
TOL=D('1e-11')

def rows(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))

def score(x,a):
    w=np.full(10,(1-a)/8,dtype=D);w[[6,9]]=a/2
    plus=np.sqrt(np.sum(w*x*x,axis=1));minus=np.sqrt(np.sum(w*(1-x)**2,axis=1))
    return 100*plus/(plus+minus)

def regrets(lower,upper):
    return np.array([max(D(0),max(np.delete(upper,i))-lower[i]) for i in range(len(lower))])

def margin(lo,hi,city,a):
    r=regrets(score(lo,a),score(hi,a));return min(np.delete(r,city))-r[city]

def reveal(lo,hi,i,subset):
    l=lo.copy();l[i,list(subset)]=hi[i,list(subset)];return l

def enclosure(lo,hi,a,b):
    ls=np.array([score(lo,t) for t in (a,b)]);us=np.array([score(hi,t) for t in (a,b)])
    low=regrets(ls.max(axis=0)+D('1e-9'),us.min(axis=0)-D('1e-9'))
    high=regrets(ls.min(axis=0)-D('1e-9'),us.max(axis=0)+D('1e-9'))
    return low,high

def main():
    s=json.loads((P/'summary.json').read_text());saved=rows(P/'utility_bounds.csv')
    cities=list(dict.fromkeys(r['city'] for r in saved));names=list(dict.fromkeys(r['indicator'] for r in saved))
    assert len(cities)==25 and len(names)==10
    assert [(r['city'],r['indicator']) for r in saved]==[(c,n) for c in cities for n in names]
    lo=np.array([D(r['lower']) for r in saved]).reshape(25,10);hi=np.array([D(r['upper']) for r in saved]).reshape(25,10)
    assert np.all((0<=lo)&(lo<=hi)&(hi<=1))
    assert hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()==s['input_bounds_sha256']
    baseline=rows(P.parent/'task4_v100_intake/utility_bounds.csv')
    assert saved==baseline
    evaluated=rows(P/'bundle_evaluations.csv');certs=rows(P/'bundle_certificates.csv');minimum=rows(P/'minimum_bundles.csv')
    assert len(minimum)==25 and [r['city'] for r in minimum]==cities
    lookup={};groups={};maxerr=D(0);negative=0;positive=0
    def decode(r):
        city=cities.index(r['city']);subset=tuple(names.index(n) for n in r['indicators'].split('|') if n)
        assert len(subset)==len(set(subset)) and list(subset)==sorted(subset)
        assert all(hi[city,j]-lo[city,j]>D('1e-12') for j in subset)
        return city,subset
    for r in evaluated:
        key=decode(r);assert key not in lookup;lookup[key]=r;i,js=key
        assert int(r['size'])==len(js);l=reveal(lo,hi,i,js)
        if r['status']=='excluded_by_witness':
            a=D(r['witness_alpha']);assert D('.05')<=a<=D('.2')
            gap=margin(l,hi,i,a);assert gap < -D('1e-8');maxerr=max(maxerr,abs(gap-D(r['witness_margin'])));negative+=1
        else:assert r['status']=='certified_outer_box';positive+=1
    for leaf in certs:
        key=decode(leaf);assert lookup[key]['status']=='certified_outer_box'
        i,js=key;a,b=D(leaf['alpha_lower']),D(leaf['alpha_upper'])
        assert leaf['certified']=='True' and int(leaf['winner'])==i and D('.05')<=a<b<=D('.2')
        l=reveal(lo,hi,i,js);low,high=enclosure(l,hi,a,b);gap=min(np.delete(low,i))-high[i]
        assert gap>D('1e-8');maxerr=max(maxerr,abs(gap-D(leaf['regret_gap_lower'])))
        groups.setdefault(key,[]).append((a,b,gap))
    for key,r in lookup.items():
        if r['status']=='certified_outer_box':
            leaves=sorted(groups[key]);last=D('.05')
            for a,b,_ in leaves:assert a==last;last=b
            assert last==D('.2')
            maxerr=max(maxerr,abs(min(g for _,_,g in leaves)-D(r['minimum_margin_bound'])))
    fixed_enumerated=0
    for i,summary in enumerate(minimum):
        unknown=tuple(np.flatnonzero(hi[i]-lo[i]>D('1e-12')))
        n=int(summary['smallest_certified_continuous_bundle'])
        expected={(i,js) for k in range(n+1) for js in itertools.combinations(unknown,k)}
        actual={key for key in lookup if key[0]==i};assert expected==actual
        successes=[key for key in expected if lookup[key]['status']=='certified_outer_box']
        assert successes and all(len(key[1])==n for key in successes)
        assert len(successes)==int(summary['certified_minimal_bundles'])
        assert summary['minimum_proved_in_outer_model']=='True'
        assert int(summary['unresolved_smaller_bundles'])==int(summary['unresolved_at_smallest_certified_size'])==0
        found=[];fixed_n=None
        for k in range(len(unknown)+1):
            for js in itertools.combinations(unknown,k):
                fixed_enumerated+=1
                if margin(reveal(lo,hi,i,js),hi,i,D('.1'))>D('1e-9'):found.append(js)
            if found:fixed_n=k;break
        assert fixed_n==int(summary['fixed_alpha_minimum']) and len(found)==int(summary['fixed_alpha_minimal_bundles'])
    rank=rows(P/'ranks.csv');lower,upper=score(lo,D('.1')),score(hi,D('.1'));rr=regrets(lower,upper)
    assert [r['city'] for r in rank]==cities
    for i,r in enumerate(rank):
        for name,value in [('score_lower',lower[i]),('score_upper',upper[i]),('max_regret',rr[i])]:maxerr=max(maxerr,abs(value-D(r[name])))
        assert int(r['decision_rank'])==1+sum(rr<rr[i])
        assert (r['possible_champion']=='True')==(upper[i]>=max(np.delete(lower,i))-D('1e-12'))
    assert maxerr<TOL and len(evaluated)==s['evaluated_bundles'] and s['unresolved_bundles']==0
    prior=P.parent/'task4_v91_current_acquisition';ps=json.loads((prior/'summary.json').read_text())
    assert s['previous_model_version']==ps['model_version']=='V91' and s['model_version']=='V96'
    assert hashlib.sha256((prior/'minimum_bundles.csv').read_bytes()).hexdigest()==s['previous_minimum_bundles_sha256']
    pb=rows(prior/'utility_bounds.csv');pl=np.array([D(r['lower']) for r in pb]).reshape(25,10);ph=np.array([D(r['upper']) for r in pb]).reshape(25,10)
    assert [(r['city'],r['indicator']) for r in pb]==[(r['city'],r['indicator']) for r in saved]
    changes=[dict(city=cities[i],indicator=names[j]) for i,j in zip(*np.where((lo!=pl)|(hi!=ph)))]
    pe=rows(prior/'bundle_evaluations.csv');prior_lookup={decode(r):r for r in pe}
    assert set(prior_lookup)==set(lookup)
    status_changes=[dict(city=cities[k[0]],indicators='|'.join(names[j] for j in k[1])) for k in lookup if lookup[k]['status']!=prior_lookup[k]['status']]
    assert not status_changes and minimum==rows(prior/'minimum_bundles.csv')
    deltas=[]
    for (i,js),r in lookup.items():
        dl=[margin(reveal(lo,hi,i,js),hi,i,D(a))-margin(reveal(pl,ph,i,js),ph,i,D(a)) for a in ['.05','.1','.2']]
        if max(abs(x) for x in dl)>TOL:deltas.append(dict(city=cities[i],indicators='|'.join(names[j] for j in js),minimum_margin_change=float(min(dl)),maximum_margin_change=float(max(dl))))
    result=dict(independent_method='Longdouble from saved250bounds; independent subset enumeration; no model imports',input_hash_verified=True,baseline_v100_matches=True,
        checked_evaluated_bundles=len(evaluated),negative_witnesses=negative,certified_bundles=positive,continuous_certificate_leaves=len(certs),all25city_continuous_minimalities_verified=True,
        independently_enumerated_fixed_bundles=fixed_enumerated,maximum_numerical_discrepancy=float(maxerr),
        changed_input_cells_vs_V91=changes,identical_bundle_sets_statuses_and_all_minimum_summary_fields=True,
        previous_continuous_certificate_leaves=len(rows(prior/'bundle_certificates.csv')),
        changed_shared_point_margin_bundles=len(deltas),shared_point_margin_changes=deltas,
        scope='Upper-endpoint hypothetical exact revelations only; neither observed data nor guaranteed real acquisition benefits or necessary performance champions.')
    (P/'independent_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='shared_point_margin_changes'},indent=2))

if __name__=='__main__':main()
