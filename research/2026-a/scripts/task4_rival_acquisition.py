"""Best-case single-rival acquisition certificates, never observed updates.

Raise one city's lower bounds to hypothetical exact upper-endpoint outcomes.
Enumerate its subsets and certify strict dominance over continuous preferences.
This is NOT a minimum over arbitrary multi-city data acquisition strategies.
"""
import hashlib
import itertools
import json
import numpy as np
import pandas as pd
from task4_combined_evidence import combined_bounds
from task4_continuous_preferences import MAIN, AUX, feasible_preferences
from task4_v5_model import ROOT, CITIES, NAMES, summarize, weights


def polynomial_minimum(p, left=.05, right=.2):
    """Vectorized quadratic minimum on a closed interval; last axis c0,c1,c2."""
    p=np.asarray(p,float)
    value=lambda x: p[...,0]+x*(p[...,1]+x*p[...,2])
    result=np.minimum(value(left),value(right))
    vertex=np.divide(-p[...,1],2*p[...,2],out=np.zeros_like(p[...,1]),where=p[...,2]!=0)
    inside=(p[...,2]>0)&(vertex>left)&(vertex<right)
    return np.where(inside,np.minimum(result,value(vertex)),result)


def affine_terms(rows):
    a0=np.mean((1-rows[:,MAIN])**2,axis=1);a1=np.mean((1-rows[:,AUX])**2,axis=1)
    b0=np.mean(rows[:,MAIN]**2,axis=1);b1=np.mean(rows[:,AUX]**2,axis=1)
    return np.stack([a0,a1-a0],axis=-1),np.stack([b0,b1-b0],axis=-1)


def strict_certificates(rows,upper,tol=1e-12):
    a,b=affine_terms(rows);c,d=affine_terms(upper)
    # G = B_new_lower * A_candidate_upper - B_candidate_upper * A_new_lower.
    p=np.stack([b[:,0,None]*c[None,:,0]-a[:,0,None]*d[None,:,0],
        b[:,0,None]*c[None,:,1]+b[:,1,None]*c[None,:,0]-a[:,0,None]*d[None,:,1]-a[:,1,None]*d[None,:,0],
        b[:,1,None]*c[None,:,1]-a[:,1,None]*d[None,:,1]],axis=-1)
    margins=polynomial_minimum(p)
    return margins>tol,margins


def analyze(lower,upper):
    profiles=[];minimum=[None]*len(CITIES);witness=[None]*len(CITIES)
    for k,city in enumerate(CITIES):
        uncertain=np.flatnonzero(upper[k]-lower[k]>1e-12)
        subsets=[s for n in range(len(uncertain)+1) for s in itertools.combinations(uncertain,n)]
        rows=np.tile(lower[k],(len(subsets),1))
        for r,s in enumerate(subsets):rows[r,list(s)]=upper[k,list(s)]
        cert,margins=strict_certificates(rows,upper);cert[:,k]=False
        sizes=np.array([len(s) for s in subsets]);counts=cert.sum(axis=1)
        for budget in range(len(uncertain)+1):
            options=np.flatnonzero(sizes==budget);r=options[np.argmax(counts[options])]
            profiles.append(dict(source_city=city,exact_measurements=budget,max_excluded=int(counts[r]),
                tied_best_bundles=int(np.sum(counts[options]==counts[r])),
                example_indicators='|'.join(NAMES[j] for j in subsets[r]),
                excluded_candidates='|'.join(CITIES[i] for i in np.flatnonzero(cert[r]))))
        for i in range(len(CITIES)):
            eligible=np.flatnonzero(cert[:,i])
            if len(eligible):
                r=eligible[np.argmin(sizes[eligible])];n=int(sizes[r])
                if minimum[i] is None or n<minimum[i]:
                    minimum[i]=n;witness[i]=dict(source_city=city,indicators='|'.join(NAMES[j] for j in subsets[r]),minimum_polynomial_margin=float(margins[r,i]))
    targets=[dict(candidate=c,minimum_single_rival_certificate_measurements=minimum[i],**(witness[i] or {})) for i,c in enumerate(CITIES)]
    return profiles,targets


def main():
    lo,hi=combined_bounds();saved=(lo.copy(),hi.copy())
    profiles,targets=analyze(lo,hi)
    assert np.array_equal(lo,saved[0]) and np.array_equal(hi,saved[1])
    out=ROOT/'results/task4_v17_rival_acquisition';out.mkdir(parents=True,exist_ok=True)
    ranks,_=summarize(lo,hi,weights())
    ranks.to_csv(out/'current_ranks.csv',index=False)
    pd.DataFrame(profiles).to_csv(out/'budget_profiles.csv',index=False)
    pd.DataFrame(targets).to_csv(out/'target_certificates.csv',index=False)
    best=[]
    for n in range(1,max(r['exact_measurements'] for r in profiles)+1):
        eligible=[r for r in profiles if r['exact_measurements']<=n]
        best.append(dict(budget_at_most=n,**max(eligible,key=lambda r:r['max_excluded'])))
    possible=sum(feasible_preferences(hi[i],lo[np.arange(len(lo))!=i])['possible'] for i in range(len(CITIES)))
    payload=dict(new_observations=0,observed_possible_champions=possible,alpha_range=[.05,.2],tolerance=1e-12,
        scope='Best-case exact upper-endpoint measurements of one rival; strict single-rival certificates, not arbitrary multi-city optimum or acquisition guarantee',
        matrix_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),best_by_budget=best)
    (out/'summary.json').write_text(json.dumps(payload,indent=2)+'\n');print(json.dumps(payload,indent=2))

if __name__=='__main__':main()
