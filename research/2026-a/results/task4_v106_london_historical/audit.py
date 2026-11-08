"""Conditional historical subgroup LP; standard library with vertex cross-check."""
from pathlib import Path
from itertools import product
import csv,json,math
P=Path(__file__).resolve().parent
obs=json.loads((P.parents[1]/'data/task4_v106_london/historical_year10_aggregates.json').read_text())
q=[r['London_Year10_published_percent']/100 for r in obs['published_percentages']]
# Continuous closure of reported bins, open-ended tail, then missing response.
a=[0,15,30,45,60,None];b=[15,30,45,60,math.inf,None]
lower_u=[math.exp(-v/30) if v is not None else 0 for v in b]
upper_u=[math.exp(-v/30) if v is not None else 1 for v in a]
def optimize(c,lo,hi,maximize=False):
    p=lo.copy();remaining=1-sum(p)
    for j in sorted(range(len(p)),key=lambda j:c[j],reverse=maximize):
        d=min(remaining,hi[j]-lo[j]);p[j]+=d;remaining-=d
    assert abs(remaining)<1e-12 and abs(sum(p)-1)<1e-12
    assert all(l-1e-12<=x<=h+1e-12 for x,l,h in zip(p,lo,hi))
    value=sum(x*y for x,y in zip(p,c))
    # Every vertex has all but at most one coordinate at box bounds.
    values=[]
    for free in range(len(p)):
        fixed=[j for j in range(len(p)) if j!=free]
        for flags in product([0,1],repeat=len(fixed)):
            v=[0.0]*len(p)
            for j,flag in zip(fixed,flags):v[j]=hi[j] if flag else lo[j]
            v[free]=1-sum(v)
            if lo[free]-1e-12<=v[free]<=hi[free]+1e-12:values.append(sum(x*y for x,y in zip(v,c)))
    assert abs(value-(max(values) if maximize else min(values)))<1e-12
    return {'value':value,'witness_proportions':p,'feasible_vertices_checked':len(values)}
results=[]
for tolerance_pp in [0.5,1.0]:
    eps=tolerance_pp/100;lo=[max(0,x-eps) for x in q];hi=[min(1,x+eps) for x in q]
    results.append({'rounding_tolerance_percentage_points':tolerance_pp,'proportion_lower':lo,'proportion_upper':hi,'utility_lower':optimize(lower_u,lo,hi),'utility_upper':optimize(upper_u,lo,hi,True)})
assert results[1]['utility_lower']['value']<=results[0]['utility_lower']['value']
assert results[1]['utility_upper']['value']>=results[0]['utility_upper']['value']

summary=json.loads((P/'summary.json').read_text())
for actual,expected in zip(results,summary['estimates']):
    assert abs(actual['utility_lower']['value']-expected['utility_lower'])<1e-12
    assert abs(actual['utility_upper']['value']-expected['utility_upper'])<1e-12
rows=list(csv.DictReader((P/'utility_bounds.csv').open()))
ranks=list(csv.DictReader((P/'ranks.csv').open()))
certs=list(csv.DictReader((P/'recommendation_certificate.csv').open()))
cities=list(dict.fromkeys(r['city'] for r in rows))
names=list(dict.fromkeys(r['indicator'] for r in rows))
def score(v,alpha):
    w=[alpha/2 if n in ('public_transport_density','public_pool_density') else (1-alpha)/8 for n in names]
    positive=math.sqrt(sum(wi*(1-x)**2 for wi,x in zip(w,v)))
    negative=math.sqrt(sum(wi*x*x for wi,x in zip(w,v)))
    return 100*negative/(positive+negative)
scenarios={}
for label in dict.fromkeys(r['scenario'] for r in rows):
    indexed={(r['city'],r['indicator']):r for r in rows if r['scenario']==label}
    lows=[[float(indexed[c,n]['lower']) for n in names] for c in cities]
    highs=[[float(indexed[c,n]['upper']) for n in names] for c in cities]
    ls=[score(v,summary['fixed_alpha']) for v in lows];us=[score(v,summary['fixed_alpha']) for v in highs]
    regrets=[max(0,max(us[j] for j in range(len(cities)) if i!=j)-ls[i]) for i in range(len(cities))]
    for r in [x for x in ranks if x['scenario']==label]:
        i=cities.index(r['city'])
        for key,val in [('score_lower',ls[i]),('score_upper',us[i]),('max_regret',regrets[i])]:assert abs(float(r[key])-val)<1e-10
        assert int(r['decision_rank'])==1+sum(x<regrets[i] for x in regrets)
        possible=us[i]>=max(ls[j] for j in range(len(cities)) if j!=i)-1e-12
        assert (r['possible_champion']=='True')==possible
        assert possible  # fixed alpha is also an existence witness in the continuous range
    leaves=sorted([c for c in certs if c['scenario']==label],key=lambda x:float(x['alpha_lower']))
    assert float(leaves[0]['alpha_lower'])==summary['alpha_range'][0]
    assert float(leaves[-1]['alpha_upper'])==summary['alpha_range'][1]
    for previous,following in zip(leaves,leaves[1:]):assert previous['alpha_upper']==following['alpha_lower']
    margins=[]
    for leaf in leaves:
        aa,bb=float(leaf['alpha_lower']),float(leaf['alpha_upper']);pad=1e-9
        lower_end=[[score(v,a) for v in lows] for a in [aa,bb]]
        upper_end=[[score(v,a) for v in highs] for a in [aa,bb]]
        lmin=[min(x)-pad for x in zip(*lower_end)];lmax=[max(x)+pad for x in zip(*lower_end)]
        umin=[min(x)-pad for x in zip(*upper_end)];umax=[max(x)+pad for x in zip(*upper_end)]
        rl=[max(0,max(umin[j] for j in range(len(cities)) if j!=i)-lmax[i]) for i in range(len(cities))]
        rh=[max(0,max(umax[j] for j in range(len(cities)) if j!=i)-lmin[i]) for i in range(len(cities))]
        winner=int(leaf['winner']);margin=min(rl[j] for j in range(len(cities)) if j!=winner)-rh[winner]
        assert leaf['certified']=='True' and margin>1e-8 and cities[winner]=='Singapore'
        assert abs(margin-float(leaf['regret_gap_lower']))<1e-10
        margins.append(margin)
    scenarios[label]={'fixed_score_and_regret_checks':'passed','continuous_certificate_leaves':len(leaves),'min_certificate_margin':min(margins),'winner':'Singapore'}
report={'status':'passed','method':'Greedy box-simplex allocation plus independent full vertex enumeration; direct stdlib scores, regrets and alpha-endpoint certificate checks','rounding_results':results,'scenario_checks':scenarios,'main_admission':False,'certificate_limit':'Numerical endpoint enclosures with padding, not formal interval arithmetic; no claim these historic data describe current London'}
(P/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: independent rounding extrema, fixed scores/regrets/ranks, continuous certificates for three scenarios.')
