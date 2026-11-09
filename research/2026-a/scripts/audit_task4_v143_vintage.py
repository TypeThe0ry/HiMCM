"""Verify withdrawal masks from raw CSV labels and all bounds with scalar TOPSIS."""
import csv,hashlib,json,math
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/task4_v143_vintage'
FIELDS=['homicide_per_100k','pm25_ugm3','cli','pir','pupil_teacher_ratio','he_per_million',None,'commute_min','broadband_mbps','pools_per_100k']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def score(values,w):
    a=math.sqrt(math.fsum(v*v*x for v,x in zip(values,w)));b=math.sqrt(math.fsum((1-v)**2*x for v,x in zip(values,w)));return 100*a/(a+b)
def main():
    s=read(OUT/'summary.json');frozen=s['source_sha256']
    for n,h in frozen.items():assert sha(ROOT/n)==h,n
    raw=rows(ROOT/'data/task4_v117_team_intake/city_indicators.csv');cities=[x['city'] for x in raw]
    bounds=[x for x in rows(ROOT/'results/task4_user_v136_revision/utility_bounds.csv') if x['scenario']=='after_conditional'];assert len(bounds)==160
    # Indicator order is recovered from the frozen bounds, not from the generator.
    names=list(dict.fromkeys(x['indicator'] for x in bounds));assert len(names)==10
    grid={(x['city'],x['indicator']):(float(x['lower']),float(x['upper'])) for x in bounds}
    source={(x['city'],names[j]):(x,field) for x in raw for j,field in enumerate(FIELDS) if field}
    point={k:(int(row[field+'_year']),row[field+'_flag']) for k,(row,field) in source.items() if row[field] and grid[k][0]==grid[k][1]}
    assert len(point)==112
    expected={
      'baseline':set(),
      'pre2020_points':{k for k,(year,flag) in point.items() if year<2020},
      'after2025_points':{k for k,(year,flag) in point.items() if year>2025},
      'non_ok_points':{k for k,(year,flag) in point.items() if flag!='ok'}}
    expected['union_points']=set.union(*(expected[k] for k in list(expected)[1:]))
    assert [len(x) for x in expected.values()]==[0,13,64,28,95]
    assert dict(Counter(str(v[0]) for v in point.values()))==s['point_year_counts']
    assert dict(Counter(v[1] for v in point.values()))==s['point_flag_counts']
    entries=rows(OUT/'submitted_points.csv');assert len(entries)==112 and {(x['city'],x['indicator']) for x in entries}==set(point)
    for x in entries:
        key=(x['city'],x['indicator']);row,field=source[key];year,flag=point[key]
        assert int(x['submitted_year'])==year and x['submitted_flag']==flag and float(x['submitted_value'])==float(row[field])
        assert float(x['utility'])==grid[key][0]
    withdrawn=rows(OUT/'withdrawn_cells.csv');assert len(withdrawn)==200
    for case,mask in expected.items():
        saved=[x for x in withdrawn if x['scenario']==case];assert len(saved)==len(mask) and {(x['city'],x['indicator']) for x in saved}==mask
        for x in saved:
            key=(x['city'],x['indicator']);assert (float(x['old_lower']),float(x['old_upper']))==grid[key] and float(x['new_lower'])==0 and float(x['new_upper'])==1
    saved=rows(OUT/'ranks.csv');assert len(saved)==160
    checks=0
    for case,mask in expected.items():
        lower={c:[0 if (c,j) in mask else grid[c,j][0] for j in names] for c in cities};upper={c:[1 if (c,j) in mask else grid[c,j][1] for j in names] for c in cities}
        for ref,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
            lows={c:score(lower[c],w) for c in cities};highs={c:score(upper[c],w) for c in cities}
            regret={c:max(0,max(highs[d] for d in cities if d!=c)-lows[c]) for c in cities}
            current=[x for x in saved if x['scenario']==case and x['weight_reference']==ref];assert len(current)==16 and {x['city'] for x in current}==set(cities)
            for x in current:
                c=x['city'];expect={'score_lower':lows[c],'score_upper':highs[c],'max_regret':regret[c],'decision_rank':1+sum(v<regret[c] for v in regret.values()),'midpoint_illustrative_score':score([(a+b)/2 for a,b in zip(lower[c],upper[c])],w)}
                for k,v in expect.items():assert abs(float(x[k])-v)<2e-11,(case,c,k)
                assert (x['possible_champion']=='True')==(highs[c]>=max(lows.values()))
                assert (x['necessary_champion']=='True')==(lows[c]>=max(highs[d] for d in cities if d!=c))
                checks+=1
            summary=next(x for x in s['cases'] if x['scenario']==case and x['weight_reference']==ref)
            assert summary['minimax_choices']==[c for c in cities if regret[c]==min(regret.values())]
            assert summary['withdrawn_point_cells']==len(mask) and summary['points_remaining']==112-len(mask) and summary['partial_cells']==33 and summary['fully_unknown_cells']==15+len(mask)
            assert abs(summary['mean_interval_width']-math.fsum(highs[c]-lows[c] for c in cities)/16)<2e-11
            assert summary['possible_champions']==16 and summary['necessary_champions']==0
    for n,h in frozen.items():assert sha(ROOT/n)==h,n
    result=dict(status='pass',independently_recomputed_city_cases=checks,independent_score_bounds=checks*2,raw_point_labels_checked=112,withdrawn_cells_checked=len(withdrawn),uncertain_bounds_preserved_in_all_cases=48,mask_sizes={k:len(v) for k,v in expected.items()},source_hashes_before_after_match=True,result_sha256={str(p.relative_to(ROOT)):sha(p) for p in OUT.iterdir() if p.suffix in {'.csv','.json'} and p.name not in {'verification.json','recheck_verification.json'}},verifier_sha256=sha(Path(__file__)))
    target=OUT/('recheck_verification.json' if (OUT/'verification.json').exists() else 'verification.json');target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
