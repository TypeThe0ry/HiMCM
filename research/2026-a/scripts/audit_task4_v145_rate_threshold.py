"""Scalar-score bisection and original-source checks independent of Brent generator."""
from pathlib import Path
import csv,gzip,hashlib,html,json,math,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/task4_v145_rate_threshold'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def score(row,w):
    a=math.sqrt(math.fsum(wi*x*x for wi,x in zip(w,row)));b=math.sqrt(math.fsum(wi*(1-x)**2 for wi,x in zip(w,row)));return 100*a/(a+b)
def main():
    s=read(OUT/'summary.json');frozen=s['source_sha256']
    for n,h in frozen.items():assert sha(ROOT/n)==h,n
    data=ROOT/'data/task4_v145_zurich_scope';v=read(data/'verification.json');assert sha(data/'extract.py')==v['extractor_sha256']
    for meta in read(data/'retrievals.json'):
        raw=(data/meta['file']).read_bytes();raw=gzip.decompress(raw) if meta['file'].endswith('.gz') else raw
        assert len(raw)==meta['raw_bytes'] and hashlib.sha256(raw).hexdigest()==meta['raw_sha256']
    text=' '.join(html.unescape(re.sub('<[^>]+>',' ',gzip.decompress((data/'victim_scope_original.html.gz').read_bytes()).decode('utf-8'))).split())
    for phrase in ['Opfer im Alter von 90 Jahren oder älter','Zahlen kleiner als fünf Personen','zweimal im Datensatz erfasst']:assert phrase in text
    assert read(data/'observations.json')==[]
    raw=rows(ROOT/'data/task4_v117_team_intake/city_indicators.csv');cities=[x['city'] for x in raw];assert next(x for x in raw if x['city']=='Zurich')['homicide_per_100k']=='0.14'
    bounds=[x for x in rows(ROOT/'results/task4_user_v136_revision/utility_bounds.csv') if x['scenario']=='after_conditional'];assert len(bounds)==160
    names=list(dict.fromkeys(x['indicator'] for x in bounds));grid={(x['city'],x['indicator']):(float(x['lower']),float(x['upper'])) for x in bounds};assert names[0]=='homicide_rate'
    def state(r,w):
        lower={c:[2/(2+r) if (c,n)==('Zurich','homicide_rate') else grid[c,n][0] for n in names] for c in cities}
        upper={c:[2/(2+r) if (c,n)==('Zurich','homicide_rate') else grid[c,n][1] for n in names] for c in cities}
        low={c:score(lower[c],w) for c in cities};high={c:score(upper[c],w) for c in cities};regret={c:max(0,max(high[d] for d in cities if d!=c)-low[c]) for c in cities}
        return low,high,regret,lower,upper
    def gap(r,w):
        _,_,regret,_,_=state(r,w);return regret['Zurich']-min(v for c,v in regret.items() if c!='Zurich')
    output=rows(OUT/'probes.csv');assert len(output)==224
    checks=0;verified=[]
    for ref,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
        t=next(x for x in s['thresholds'] if x['weight_reference']==ref);lo,hi=0.,5.;assert gap(lo,w)<0<gap(hi,w)
        for _ in range(80):
            mid=(lo+hi)/2
            if gap(mid,w)<=0:lo=mid
            else:hi=mid
        root=(lo+hi)/2;assert abs(root-t['rate_per100000'])<2e-11 and t['numerical_bracket_lower']<root<t['numerical_bracket_upper']
        assert gap(t['numerical_bracket_lower'],w)<0<gap(t['numerical_bracket_upper'],w)
        low,high,regret,_,_=state(root,w);other=sorted(((v,c) for c,v in regret.items() if c!='Zurich'))
        assert other[0][1]==t['alternative'] and other[1][0]-other[0][0]>1e-6
        assert abs(regret['Zurich']-other[0][0])<2e-11
        assert abs(regret['Zurich']-t['zurich_max_regret'])<2e-11
        assert abs(other[0][0]-t['alternative_max_regret'])<2e-11
        assert state(0,w)[2]['Zurich']>0
        probes={x['probe']:float(x['hypothetical_rate']) for x in output if x['weight_reference']==ref};assert set(probes)=={'zero','low_neighbor','retained_point','high_neighbor','bracket_below','bracket_above','high_probe'}
        assert probes['retained_point']==.14 and probes['bracket_below']==t['numerical_bracket_lower'] and probes['bracket_above']==t['numerical_bracket_upper']
        for label,r in probes.items():
            low,high,regret,lower,upper=state(r,w);saved=[x for x in output if x['weight_reference']==ref and x['probe']==label];assert len(saved)==16 and {x['city'] for x in saved}==set(cities)
            for x in saved:
                c=x['city'];midpoints={d:score([(a+b)/2 for a,b in zip(lower[d],upper[d])],w) for d in cities}
                expected={'score_lower':low[c],'score_upper':high[c],'max_regret':regret[c],'decision_rank':1+sum(z<regret[c] for z in regret.values()),'best_rank':1+sum(low[d]>high[c]+1e-12 for d in cities if d!=c),'worst_rank':1+sum(high[d]>low[c]+1e-12 for d in cities if d!=c),'midpoint_illustrative_score':midpoints[c],'midpoint_illustrative_rank':1+sum(z>midpoints[c] for z in midpoints.values())}
                for k,value in expected.items():assert abs(float(x[k])-value)<2e-11,(ref,label,c,k)
                assert (x['possible_champion']=='True')==(high[c]>=max(low[d] for d in cities if d!=c)-1e-12)
                assert (x['necessary_champion']=='True')==(low[c]>=max(high[d] for d in cities if d!=c)-1e-12)
                checks+=1
            choices=[c for c in cities if regret[c]==min(regret.values())]
            if label in {'zero','low_neighbor','retained_point','high_neighbor','bracket_below'}:assert choices==['Zurich']
            if label=='bracket_above':assert choices==[t['alternative']]
        verified.append(dict(weight_reference=ref,independent_bisection_rate=root,alternative=t['alternative'],sign_bracket_width=t['numerical_bracket_upper']-t['numerical_bracket_lower']))
    for n,h in frozen.items():assert sha(ROOT/n)==h,n
    result=dict(status='pass',independent_city_cases=checks,independent_score_bounds=checks*2,independent_bisections=verified,other_159_entries_fixed_in_every_probe=True,original_source_scope_verified=True,primary_data_admissions=0,result_sha256={str(p.relative_to(ROOT)):sha(p) for p in OUT.iterdir() if p.suffix in {'.csv','.json'} and p.name not in {'verification.json','recheck_verification.json'}},verifier_sha256=sha(Path(__file__)))
    target=OUT/('recheck_verification.json' if (OUT/'verification.json').exists() else 'verification.json');target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
