"""Independent longdouble scale/scoring audit and Mexico moment reconstruction."""
from pathlib import Path
import csv,hashlib,itertools,json
import numpy as np
from scipy.stats import t
P=Path(__file__).resolve().parent;ROOT=P.parents[1];D=np.longdouble

def rows(p):return list(csv.DictReader(p.open()))
def score(x,a):
    a=D(str(a));w=np.full(10,(1-a)/8,dtype=D);w[[6,9]]=a/2
    pos=np.sqrt(np.sum(w*x*x,axis=1));neg=np.sqrt(np.sum(w*(1-x)**2,axis=1));return 100*pos/(pos+neg)
def regret(l,h):return np.array([max(D(0),max(np.delete(h,i))-l[i]) for i in range(25)])
def near(a,b):assert abs(D(str(a))-D(str(b)))<D('1e-10'),(a,b)

def mexico():
    source=ROOT/'data/task4_v108_mexico_design';m=json.loads((source/'manifest.json').read_text());raw=(source/m['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==m['sha256']
    d=json.loads(raw);s=np.array(d['weighted_totals'],dtype=D);c=np.array(d['centered_crossproduct'],dtype=D)
    critical=D(str(t.ppf(.975,d['diagnostics']['psu_n']-d['diagnostics']['strata_n'])))
    out=json.loads((ROOT/'data/task4_v111_mexico_scale/summary.json').read_text());n=0
    for r in out['scenarios']:
        tau=D(str(r['tau_minutes']));ends=[(np.exp(-D(b)/tau) if b else D(0),np.exp(-D(a)/tau)) for a,b in [(0,15),(15,30),(30,60),(60,120),(120,None)]]+[(D(0),D(1))]*3
        assert r['input_moments_sha256']==m['sha256']
        for side,col in [('lower',0),('upper',1)]:
            order=sorted(range(8),key=lambda k:ends[k][col],reverse=bool(col));vals=[];ratios=[]
            cs=r['candidates'][side]['candidates'];assert len(cs)==9
            for k,old in enumerate(cs):
                included=set(order[:k]);b=np.array([int(g==0 or j in included) for g in range(3) for j in range(8)],dtype=D);a=np.array([b[z]*ends[z%8][col] for z in range(24)])
                X=b@s;Y=a@s;q=Y/X;e=a-q*b;se=np.sqrt(max(D(0),e@c@e/X**2))
                near(q,old['ratio']);near(se,old['taylor_se']);near(X,old['B']);near(Y,old['A']);n+=1
                vals.append(q+(-1 if col==0 else 1)*critical*se);ratios.append(q)
            opt=min if col==0 else max;near(r['utility_'+side],min(D(1),max(D(0),opt(vals))));near(r['point_'+side],opt(ratios))
    return n

def audit():
    summary=json.loads((P/'summary.json').read_text());mx=mexico();direct={}
    for src in summary['source_summaries']:
        p=ROOT/src['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==src['sha256']
        for r in json.loads(p.read_text())['scenarios']:direct[r['city'],r['tau_minutes']]=(r['utility_lower'],r['utility_upper'])
    base=[r for r in rows(P.parent/'task4_v108_mexico_sampling/utility_bounds.csv') if r['scenario']=='v108_outer']
    cities=list(dict.fromkeys(r['city'] for r in base));names=list(dict.fromkeys(r['indicator'] for r in base));j=names.index('travel')
    baseline=np.array([[D(r[k]) for r in base] for k in ['lower','upper']]).reshape(2,25,10)
    assert hashlib.sha256(baseline.astype('<f8').tobytes()).hexdigest()==summary['input_bounds_sha256']
    br=rows(P/'utility_bounds.csv');rr=rows(P/'ranks.csv');cert=rows(P/'recommendation_certificate.csv');assert len(br)==2500 and len(rr)==250
    known=np.any(baseline[:,:,j]!=np.array([[0],[1]]),axis=0);assert known.sum()==5
    base_regret=regret(score(baseline[0],.1),score(baseline[1],.1));base_rank=np.array([1+sum(base_regret<x) for x in base_regret]);reports=[]
    for case in summary['scenarios']:
        method,tau=case['method'],case['tau_minutes'];select=lambda r:r['method']==method and int(r['tau_minutes'])==tau
        b=[r for r in br if select(r)];ranks=[r for r in rr if select(r)];leaves=[r for r in cert if select(r)]
        assert len(b)==250 and len(ranks)==25
        mat=np.array([[D(r[k]) for r in b] for k in ['lower','upper']]).reshape(2,25,10)
        assert np.all(mat[:,:,np.arange(10)!=j]==baseline[:,:,np.arange(10)!=j])
        assert np.all(mat[0,~known,j]==0) and np.all(mat[1,~known,j]==1)
        for i,c in enumerate(cities):
            l,h=baseline[:,i,j];power=D(30)/tau
            expected=direct[c,tau] if method=='direct' and known[i] else ([l**power,h] if power>=1 else [l,h**power])
            if method=='direct' and not known[i]:expected=[0,1]
            near(mat[0,i,j],expected[0]);near(mat[1,i,j],expected[1])
        if tau==30:assert np.max(abs(mat-baseline))<D('1e-12')
        ls,us=score(mat[0],.1),score(mat[1],.1);reg=regret(ls,us);rank=np.array([1+sum(reg<x) for x in reg])
        for i,r in enumerate(ranks):
            assert r['city']==cities[i]
            for k,v in [('score_lower',ls[i]),('score_upper',us[i]),('max_regret',reg[i])]:near(r[k],v)
            best=1+sum(np.delete(ls,i)>us[i]);worst=1+sum(np.delete(us,i)>ls[i])
            assert int(r['decision_rank'])==rank[i] and int(r['best_rank'])==best and int(r['worst_rank'])==worst
            assert (r['possible_champion']=='True')==(best==1) and (r['necessary_champion']=='True')==(worst==1)
        assert case['changed_ranks']==sum(rank!=base_rank)
        concordant=sum((rank[a]-rank[b])*(base_rank[a]-base_rank[b])>0 for a,b in itertools.combinations(range(25),2))
        discordant=sum((rank[a]-rank[b])*(base_rank[a]-base_rank[b])<0 for a,b in itertools.combinations(range(25),2))
        assert len(set(rank))==25 and len(set(base_rank))==25;near(case['kendall_tau'],(concordant-discordant)/300)
        near(case['mean_score_width'],np.mean(us-ls));assert case['choice']==['Singapore'] and case['possible_champions']==25
        assert set(case['continuous_possible_champions'])==set(cities)
        assert all(us[i]>=max(np.delete(ls,i)) for i in range(25))
        end=D('.05');gaps=[]
        for leaf in sorted(leaves,key=lambda r:float(r['alpha_lower'])):
            a,b=D(leaf['alpha_lower']),D(leaf['alpha_upper']);assert a==end and a<b;end=b
            l=np.array([score(mat[0],v) for v in (a,b)]);h=np.array([score(mat[1],v) for v in (a,b)])
            lower=regret(l.max(axis=0)+D('1e-9'),h.min(axis=0)-D('1e-9'));upper=regret(l.min(axis=0)-D('1e-9'),h.max(axis=0)+D('1e-9'))
            winner=int(leaf['winner']);gap=min(np.delete(lower,winner))-upper[winner];near(leaf['regret_gap_lower'],gap)
            assert gap>D('1e-8') and leaf['certified']=='True' and cities[winner]=='Singapore';gaps.append(float(gap))
        assert end==D('.2') and case['continuous_recommendation']==dict(unresolved=0,winners=['Singapore'])
        reports.append(dict(method=method,tau_minutes=tau,rank_changes=int(sum(rank!=base_rank)),certificate_leaves=len(leaves),minimum_certified_gap=min(gaps)))
    return dict(passed=True,mexico_prefix_ratios_and_SE_verified=mx,interval_cells_verified=2500,rank_rows_verified=250,unchanged_nontravel_cells_per_scenario=225,unknown_travel_cells_preserved_per_scenario=20,tau30_matches_v108=True,scenarios=reports,method='Independent longdouble scalar TOPSIS/regret, Mexico coefficient/Taylor reconstruction from hashed moments, Jensen moment bounds, endpoint-monotonic continuous-alpha certificate replay; no project scoring imports.',scope='Five discrete tau scenarios; certificates extend only across alpha, not tau. Direct source sampling envelopes and propagated baseline envelopes are not asserted nested.',source_result_hashes={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['summary.json','utility_bounds.csv','ranks.csv','recommendation_certificate.csv']})
if __name__=='__main__':
    result=audit();(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
