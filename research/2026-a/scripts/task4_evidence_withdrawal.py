"""Exhaustive minimum cell-withdrawal audit, not probabilities of source failure."""
from itertools import combinations
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,score,weights,summarize
from task4_saopaulo_age_revision import saopaulo_age_bounds


def regrets(ls,us):
    rivals=np.broadcast_to(us,(len(us),len(us))).copy()
    np.fill_diagonal(rivals,-np.inf)
    return np.maximum(0,rivals.max(axis=1)-ls)


def winners(ls,us):
    r=regrets(ls,us)
    return np.flatnonzero(r<=r.min()+1e-10).tolist()


def withdraw(lo,hi,cells):
    l,h=lo.copy(),hi.copy()
    for i,j in cells:l[i,j],h[i,j]=0.,1.
    return l,h


def main():
    source=ROOT/'data/task4_v51_phoenix'
    for item in json.loads((source/'manifest.json').read_text()):
        raw=(source/item['file']).read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    lo,hi=saopaulo_age_bounds();w=weights()
    ls,us=score(lo,w),score(hi,w)
    champion=CITIES.index('Singapore');assert winners(ls,us)==[champion]
    cells=[tuple(map(int,x)) for x in np.argwhere((lo>0)|(hi<1))]
    single=[];single_scores={}
    for i,j in cells:
        l,h=withdraw(lo,hi,[(i,j)])
        a,b=score(l,w),score(h,w);single_scores[(i,j)]=(a[i],b[i])
        win=winners(a,b)
        single.append(dict(city=CITIES[i],indicator=NAMES[j],changed=win!=[champion],
                           winners=';'.join(CITIES[k] for k in win)))
    assert not any(r['changed'] for r in single)
    changed=[];tested=0
    for first,second in combinations(cells,2):
        a,b=ls.copy(),us.copy();i,j=first;k,m=second
        if i!=k:
            a[i],b[i]=single_scores[first];a[k],b[k]=single_scores[second]
        else:
            l,h=withdraw(lo,hi,[first,second])
            a[i],b[i]=score(l[i:i+1],w)[0],score(h[i:i+1],w)[0]
        win=winners(a,b);tested+=1
        if win!=[champion]:
            changed.append(dict(city1=CITIES[i],indicator1=NAMES[j],city2=CITIES[k],indicator2=NAMES[m],
                                winners=';'.join(CITIES[t] for t in win)))
    assert changed  # All singles tested: at least one pair establishes minimum two.
    pair=changed[0]
    paircells=[(CITIES.index(pair['city1']),NAMES.index(pair['indicator1'])),
               (CITIES.index(pair['city2']),NAMES.index(pair['indicator2']))]
    scenarios=[('baseline',[],.1),('singapore_safety_withdrawal',[(champion,0)],.1),
               ('singapore_safety_withdrawal_alpha005',[(champion,0)],.05),
               ('first_minimum_pair',paircells,.1),
               ('singapore_education_travel_withdrawal',[(champion,4),(champion,7)],.1)]
    frames=[];stats=[]
    for label,removed,alpha in scenarios:
        l,h=withdraw(lo,hi,removed)
        assert np.all(l<=lo) and np.all(h>=hi)
        f,d=summarize(l,h,weights(alpha));f['scenario']=label;frames.append(f)
        actual=winners(score(l,weights(alpha)),score(h,weights(alpha)))
        assert actual==list(d['minimax_choices'])
        stats.append(dict(scenario=label,alpha=alpha,withdrawn=[dict(city=CITIES[i],indicator=NAMES[j]) for i,j in removed],
                          winners=[CITIES[k] for k in actual],possible_champions=int(f.possible_champion.sum())))
    assert stats[2]['winners']==['Tokyo']
    previous=pd.read_csv(ROOT/'results/task4_v50_continuous_recommendation/ranks.csv')
    for col in ['score_lower','score_upper','max_regret','decision_rank']:
        np.testing.assert_allclose(frames[0][col],previous[col],rtol=0,atol=1e-12)
    # Independent scoring path validates the cached pair optimization for witnesses.
    for row in changed:
        removed=[(CITIES.index(row['city1']),NAMES.index(row['indicator1'])),
                 (CITIES.index(row['city2']),NAMES.index(row['indicator2']))]
        l,h=withdraw(lo,hi,removed)
        assert ';'.join(CITIES[k] for k in winners(score(l,w),score(h,w)))==row['winners']
    out=ROOT/'results/task4_v51_evidence_withdrawal';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(single).to_csv(out/'single_withdrawals.csv',index=False)
    pd.DataFrame(changed).to_csv(out/'minimum_pairs.csv',index=False)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    result=dict(baseline='V48 with V49 and V50 unchanged main inputs',admitted_cells_changed=0,
                informative_cells=len(cells),single_changes=0,pairs_tested=tested,changing_pairs=len(changed),
                minimum_withdrawals_fixed_alpha010=2,minimum_withdrawals_some_alpha005_020=1,
                interpretation='Hypothetical loss of all information in city-indicator cells, not independent source failures or observed errors',
                main_admitted=False,scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
