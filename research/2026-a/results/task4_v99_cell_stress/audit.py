"""Independent longdouble check of single-cell perturbations and domain cover."""
import csv,hashlib,json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
D=np.longdouble

def rows(name):
    with (P/name).open(newline='') as f:return list(csv.DictReader(f))

def score(x,a):
    w=np.full(10,(1-a)/8,dtype=D);w[[6,9]]=a/2
    b=np.sqrt((w*x*x).sum(axis=1));g=np.sqrt((w*(1-x)**2).sum(axis=1))
    return 100*b/(b+g)

def regret(l,h):return np.array([max(D(0),max(np.delete(h,i))-l[i]) for i in range(len(l))])

def expand(l,h,e,key):
    l,h=l.copy(),h.copy();l[key]=max(0,l[key]-e);h[key]=min(1,h[key]+e)
    return l,h

def enclosure(lo,hi,e0,e1,a0,a1,key):
    sl,sh=expand(lo,hi,e0,key);ll,lh=expand(lo,hi,e1,key);p=D('1e-9')
    lmin=np.minimum(score(ll,a0),score(ll,a1))-p;lmax=np.maximum(score(sl,a0),score(sl,a1))+p
    umin=np.minimum(score(sh,a0),score(sh,a1))-p;umax=np.maximum(score(lh,a0),score(lh,a1))+p
    return regret(lmax,umin),regret(lmin,umax)

def main():
    s=json.loads((P/'summary.json').read_text());b=rows('baseline_bounds.csv')
    cities=list(dict.fromkeys(r['city'] for r in b));names=list(dict.fromkeys(r['indicator'] for r in b))
    assert len(cities)==25 and len(names)==10 and [(r['city'],r['indicator']) for r in b]==[(c,n) for c in cities for n in names]
    lo=np.array([D(r['lower']) for r in b]).reshape(25,10);hi=np.array([D(r['upper']) for r in b]).reshape(25,10)
    assert hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()==s['input_bounds_sha256']
    choice=cities.index(s['baseline_choice']);tol=D('1e-11');maxerr=D(0)
    def key(r):
        k=int(r['city_index']),int(r['indicator_index'])
        assert r['target_city']==cities[k[0]] and r['target_indicator']==names[k[1]]
        return k
    cases=rows('point_cases.csv');cache={};failures=set()
    for r in cases:
        k=key(r);e,a=D(r['epsilon']),D(r['alpha']);l,h=expand(lo,hi,e,k)
        ls,us=score(l,a),score(h,a);rr=regret(ls,us);gap=min(np.delete(rr,choice))-rr[choice]
        case=(k,e,a);assert case not in cache;cache[case]=(ls,us,rr)
        values=[(gap,r['baseline_choice_gap']),(min(rr),r['minimum_regret']),(rr[choice],r['baseline_choice_regret'])]
        maxerr=max(maxerr,max(abs(x-D(y)) for x,y in values))
        assert abs(rr[cities.index(r['minimum_regret_city'])]-min(rr))<tol
        assert (r['strict_failure_witness']=='True')==(gap < -D('1e-8'))
        if gap < -D('1e-8'):failures.add(case)
    expected={( (i,j),D(e),D(a)) for i in range(25) for j in range(10) for e in ['.2','1'] for a in ['.05','.1','.2']}
    assert set(cache)==expected
    fr=rows('failure_witness_ranks.csv');seen=set()
    for r in fr:
        case=(key(r),D(r['epsilon']),D(r['alpha']));assert case in failures
        idx=cities.index(r['city']);assert (case,idx) not in seen;seen.add((case,idx))
        ls,us,rr=cache[case]
        for field,value in [('score_lower',ls[idx]),('score_upper',us[idx]),('max_regret',rr[idx])]:maxerr=max(maxerr,abs(value-D(r[field])))
        assert int(r['decision_rank'])==1+sum(rr<rr[idx])
        assert (r['possible_champion']=='True')==(us[idx]>=max(np.delete(ls,idx))-D('1e-12'))
    assert len(seen)==25*len(failures)
    pre=rows('prefix_certificates.csv');wd=rows('withdrawal_certificates.csv');pg={};wg={};unresolved=0
    for r in pre:
        k=key(r);v=tuple(D(r[x]) for x in ['epsilon_lower','epsilon_upper','alpha_lower','alpha_upper'])
        e0,e1,a0,a1=v;assert 0<=e0<e1<=D('.2') and D('.05')<=a0<a1<=D('.2')
        low,high=enclosure(lo,hi,*v,k);gap=min(np.delete(low,choice))-high[choice]
        maxerr=max(maxerr,abs(gap-D(r['gap_lower'])))
        assert (r['certified']=='True')==(gap>D('1e-8'))
        pg.setdefault(k,[]).append(v)
    for r in wd:
        k=key(r);a0,a1=D(r['alpha_lower']),D(r['alpha_upper'])
        low,high=enclosure(lo,hi,D(1),D(1),a0,a1,k)
        margins=np.array([min(np.delete(low,i))-high[i] for i in range(25)])
        if r['certified']=='True':
            winner=int(float(r['winner']));assert cities[winner]==r['winner_city'] and margins[winner]>D('1e-8')
            maxerr=max(maxerr,abs(margins[winner]-D(r['regret_gap_lower'])))
        else:
            unresolved+=1;assert r['winner']=='' and r['winner_city']=='' and max(margins)<=D('1e-8')+tol
        wg.setdefault(k,[]).append((a0,a1))
    assert set(pg)==set(wg)=={(i,j) for i in range(25) for j in range(10)}
    for k,rect in pg.items():
        assert abs(sum((e1-e0)*(a1-a0) for e0,e1,a0,a1 in rect)-D('.03'))<D('1e-16')
        for i,(e0,e1,a0,a1) in enumerate(rect):
            for f0,f1,b0,b1 in rect[i+1:]:assert min(e1,f1)<=max(e0,f0) or min(a1,b1)<=max(a0,b0)
        cursor=D('.05')
        for a,b in sorted(wg[k]):assert a==cursor and a<b;cursor=b
        assert cursor==D('.2')
    cells=rows('cells.csv');assert len(cells)==250 and len({key(r) for r in cells})==250
    for r in cells:
        k=key(r);assert D(r['initial_lower'])==lo[k] and D(r['initial_upper'])==hi[k]
        assert int(r['prefix_leaves'])==len(pg[k]) and int(r['withdrawal_leaves'])==len(wg[k])
    assert maxerr<tol
    assert len(cases)==s['point_cases'] and len(failures)==s['failure_point_cases'] and unresolved==s['withdrawal_unresolved']
    assert len(pre)==s['prefix_leaves'] and len(wd)==s['withdrawal_leaves']
    assert s['informative_cells']==int(((lo!=0)|(hi!=1)).sum())
    result=dict(input_hash_verified=True,point_cases=len(cases),failure_rank_rows=len(fr),prefix_leaves=len(pre),withdrawal_leaves=len(wd),withdrawal_unresolved=unresolved,all_250_domains_cover_without_overlap=True,maximum_longdouble_discrepancy=float(maxerr),model_imports_used=False)
    (P/'independent_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
