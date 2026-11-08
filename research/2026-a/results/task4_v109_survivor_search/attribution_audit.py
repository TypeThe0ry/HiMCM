"""Independent frozen-input attribution and precision audit; no core imports."""
from pathlib import Path
import csv,hashlib,itertools,json
import numpy as np
P=Path(__file__).resolve().parent
D=np.longdouble
MAIN,AUX=[0,1,2,3,4,5,7,8],[6,9]
def score(x, alpha):
    x = np.asarray(x, dtype=D); alpha = D(str(alpha))
    w = np.full(10, (1-alpha)/8, dtype=D); w[AUX] = alpha/2
    pos = np.sqrt(np.sum(w*x*x, axis=-1))
    neg = np.sqrt(np.sum(w*(1-x)**2, axis=-1))
    return 100*pos/(pos+neg)


def polynomial(x, y):
    def terms(z):
        z = np.asarray(z, dtype=D)
        p0, p1 = np.mean(z[MAIN]**2), np.mean(z[AUX]**2)
        q0, q1 = np.mean((1-z[MAIN])**2), np.mean((1-z[AUX])**2)
        return p0, p1-p0, q0, q1-q0
    p0, p1, q0, q1 = terms(x); a0, a1, b0, b1 = terms(y)
    return (p0*b0-a0*q0, p0*b1+p1*b0-a0*q1-a1*q0, p1*b1-a1*q1)


def feasible(x, rivals, amin, amax):
    polys = [polynomial(x, y) for y in rivals]
    cuts = {D(str(amin)), D(str(amax))}
    for c, b, a in polys:
        roots = []
        if a == 0:
            if b != 0: roots = [-c/b]
        else:
            disc = b*b-4*a*c
            if disc >= 0:
                q = -(b+np.copysign(np.sqrt(disc), b))/2
                roots = [q/a, c/q] if q != 0 else [-b/(2*a)]
        cuts.update(r for r in roots if amin < r < amax)
    cuts = sorted(cuts)
    points = cuts+[(a+b)/2 for a, b in zip(cuts[:-1], cuts[1:])]
    return any(all(c+t*b+t*t*a >= -D('1e-12') for c, b, a in polys) for t in points)


def read_bounds(version):
    sources={'V102':('task4_v102_copenhagen_revision','v102_copenhagen_resources'),'V107':('task4_v107_mexico_revision','v107_2025_transition_optional'),'V108':('task4_v108_mexico_sampling','v108_outer')}
    folder,scenario=sources[version]
    rows=[r for r in csv.DictReader((P.parent/folder/'utility_bounds.csv').open()) if r['scenario']==scenario]
    cities=list(dict.fromkeys(r['city'] for r in rows));names=list(dict.fromkeys(r['indicator'] for r in rows))
    assert len(rows)==250 and len(cities)==25 and len(names)==10
    assert [(r['city'],r['indicator']) for r in rows]==[(c,n) for c in cities for n in names]
    return cities,names,np.array([[D(r[k]) for r in rows] for k in ['lower','upper']]).reshape(2,25,10)

def completion(lo,hi,js,keep,width):
    lower,upper=lo.copy(),hi.copy();keep=set(keep)
    for i in range(25):
        for j in js:
            w=min(D(str(width)),hi[i,j]-lo[i,j])
            if i in keep:lower[i,j]=hi[i,j]-w
            else:upper[i,j]=lo[i,j]+w
    return lower,upper

def outsiders(lo,hi,js,keep,width):
    l,h=completion(lo,hi,js,keep,width)
    return [i for i in range(25) if i not in keep and feasible(h[i],l[list(keep)],D('.05'),D('.2'))]

def main():
    attribution=json.loads((P/'attribution.json').read_text());assert [r['model_version'] for r in attribution['scenarios']]==['V102','V107','V108']
    checked=[];previous=None
    for row in attribution['scenarios']:
        version=row['model_version'];cities,names,mat=read_bounds(version);lo,hi=mat
        digest=hashlib.sha256(mat.astype('<f8').tobytes()).hexdigest();assert digest==row['input_bounds_sha256']
        js=[names.index(n) for n in ['upper_secondary_ptr','travel','homicide_rate']]
        if previous is not None:
            changes=np.argwhere(np.any(mat!=previous,axis=0))
            assert changes.tolist()==[[cities.index('Mexico City'),names.index('travel')]]
        previous=mat.copy()
        worst,best=hi.copy(),lo.copy();worst[:,js]=lo[:,js];best[:,js]=hi[:,js]
        required=[i for i in range(25) if feasible(worst[i],np.delete(best,i,axis=0),D('.05'),D('.2'))]
        assert len(required)==3
        assert outsiders(lo,hi,js,required,0), 'Three-set must fail for minimum4'
        success=[];enumerated=0
        for extra in itertools.combinations([i for i in range(25) if i not in required],4-len(required)):
            keep=sorted(required+list(extra));enumerated+=1
            if not outsiders(lo,hi,js,keep,0):success.append([cities[i] for i in keep])
        assert row['minimum']==4 and success==[s['cities'] for s in row['sets']]
        precision=[]
        for item in row['sets']:
            keep=[cities.index(c) for c in item['cities']]
            a,b=item['feasible_width'],item['infeasible_width'];assert 0<=a<b<=1 and b-a<=1e-4
            assert not outsiders(lo,hi,js,keep,a)
            fails=outsiders(lo,hi,js,keep,b);assert fails
            precision.append(dict(cities=item['cities'],feasible_width=a,infeasible_width=b,infeasible_outsiders=[cities[i] for i in fails]))
        checked.append(dict(version=version,input_hash_verified=True,unavoidable_cities=[cities[i] for i in required],minimum=4,three_set_rejected=True,four_sets_enumerated=enumerated,successful_sets=precision))
    result=dict(passed=True,scenarios=checked,input_attribution_sha256=hashlib.sha256((P/'attribution.json').read_bytes()).hexdigest(),method='Independent longdouble TOPSIS comparison quadratics, exhaustive root-partition feasibility and mandatory-plus-four-set enumeration; finite-width completion independently reconstructed. No project algorithm imports.',qualification='Numerical certificates, not directed-rounding formal arithmetic. Wider hypothetical revelation choices are not real data improvements; V107 combines period and membership changes and does not isolate either alone.')
    (P/'attribution_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
