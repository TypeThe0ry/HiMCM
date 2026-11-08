"""Independent saved-result replay; no model or source-extractor imports."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
D=np.longdouble

def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def score(x,alpha):
    w=np.full(10,(1-alpha)/8,dtype=D);w[[6,9]]=alpha/2
    good=np.sqrt(np.sum(w*x*x,axis=1));bad=np.sqrt(np.sum(w*(1-x)*(1-x),axis=1))
    return 100*good/(good+bad)

def regret(l,h):return np.array([max(D(0),max(np.delete(h,i))-l[i]) for i in range(len(l))])

def main():
    summary=json.loads((P/'summary.json').read_text());raw=rows(P/'utility_bounds.csv');rank=rows(P/'ranks.csv')
    source=P.parent.parent/'data/task4_v99_tokyo'
    assert hashlib.sha256((source/'summary.json').read_bytes()).hexdigest()==summary['source_summary_sha256']
    for rec in json.loads((source/'manifest.json').read_text()):
        b=(source/rec['file']).read_bytes();assert len(b)==rec['bytes'] and hashlib.sha256(b).hexdigest()==rec['sha256']
    labels=['v96_current','matched_narrow_2025','matched_narrow_2026']
    assert len(raw)==750 and len(rank)==75
    cities=list(dict.fromkeys(r['city'] for r in raw));names=list(dict.fromkeys(r['indicator'] for r in raw))
    assert len(cities)==25 and len(names)==10
    ti,tj=cities.index('Tokyo'),names.index('upper_secondary_ptr');changed=np.zeros((25,10),bool);changed[ti,tj]=True
    arrays={};values={};maxerror=D(0)
    for label in labels:
        rr=[r for r in raw if r['scenario']==label]
        assert [(r['city'],r['indicator']) for r in rr]==[(c,n) for c in cities for n in names]
        lo=np.array([D(r['lower']) for r in rr]).reshape(25,10);hi=np.array([D(r['upper']) for r in rr]).reshape(25,10)
        assert np.all((0<=lo)&(lo<=hi)&(hi<=1));arrays[label]=(lo,hi)
        if label=='v96_current':
            assert hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()==summary['input_bounds_sha256']
        else:
            for x,b in zip((lo,hi),arrays['v96_current']):assert np.array_equal(x[~changed],b[~changed])
            year=int(label[-4:]);hs=[r for r in rows(source/'gk26pv0701.csv') if r['種別']=='総数（国・公・私立）' and r['地域階層']=='0' and r['西暦（年度）']==str(year)]
            ss=[r for r in rows(source/'gk26pv0901.csv') if r['種別']=='総数（国・公立）' and r['地域階層']=='0' and r['西暦（年度）']==str(year)]
            assert len(hs)==len(ss)==1
            n=D(hs[0]['生徒数（人）'])+D(ss[0]['後期課程／生徒数（全日制）（人）']);t=D(hs[0]['教員数（本務者）（人）']);pool=D(ss[0]['教員数（本務者）（人）'])
            assert abs(lo[ti,tj]-15*t/(n+15*t))<D('1e-15')
            assert abs(hi[ti,tj]-15*(t+pool)/(n+15*(t+pool)))<D('1e-15')
        lower,upper=score(lo,D('.1')),score(hi,D('.1'));reg=regret(lower,upper);ranks=np.array([1+sum(reg<x) for x in reg]);values[label]=(lower,upper,reg,ranks)
        rf=[r for r in rank if r['scenario']==label];assert [r['city'] for r in rf]==cities
        for i,r in enumerate(rf):
            for key,x in [('score_lower',lower[i]),('score_upper',upper[i]),('max_regret',reg[i])]:maxerror=max(maxerror,abs(x-D(r[key])))
            assert int(r['decision_rank'])==ranks[i]
            ol,oh=np.delete(lower,i),np.delete(upper,i)
            assert int(r['best_rank'])==1+sum(ol>upper[i]+D('1e-12'))
            assert int(r['worst_rank'])==1+sum(oh>lower[i]+D('1e-12'))
            assert (r['possible_champion']=='True')==(upper[i]>=max(ol)-D('1e-12'))
            assert (r['necessary_champion']=='True')==(lower[i]>=max(oh)-D('1e-12'))
        report=next(r for r in summary['scenarios'] if r['scenario']==label)
        assert report['choice']==[cities[k] for k in np.flatnonzero(reg<=reg.min()+D('1e-12'))]
        # All 25 have an actual common alpha=.1 possibility witness, inside the continuous range.
        assert report['possible_champions']==report['continuous_possible_champions']==cities
        assert all(upper[k]>=max(np.delete(lower,k)) for k in range(25))
    assert maxerror<D('1e-11')
    old,new=values[labels[1]],values[labels[2]]
    assert sum(old[3]!=new[3])==summary['paired_year_changed_ranks']==0
    assert abs(D(str(summary['paired_year_kendall_tau']))-1)<D('1e-15')
    for idx,name in [(0,'lower'),(1,'upper')]:assert abs((new[idx][ti]-old[idx][ti])-D(str(summary[f'paired_year_tokyo_{name}_change'])))<D('1e-11')
    cert=rows(P/'recommendation_certificate.csv');gaperror=D(0)
    for label in labels:
        leaves=[r for r in cert if r['scenario']==label];last=D('.05');lo,hi=arrays[label]
        for r in leaves:
            a,b=D(r['alpha_lower']),D(r['alpha_upper']);assert a==last and a<b<=D('.2');last=b
            ls=np.array([score(lo,x) for x in [a,b]]);us=np.array([score(hi,x) for x in [a,b]])
            low=regret(ls.max(axis=0)+D('1e-9'),us.min(axis=0)-D('1e-9'))
            high=regret(ls.min(axis=0)-D('1e-9'),us.max(axis=0)+D('1e-9'))
            winner=int(r['winner']);gap=min(np.delete(low,winner))-high[winner]
            assert cities[winner]=='Singapore' and r['certified']=='True' and gap>D('1e-8')
            gaperror=max(gaperror,abs(gap-D(r['regret_gap_lower'])))
        assert last==D('.2')
    assert len(cert)==6 and gaperror<D('1e-11')
    result=dict(independent_method='Longdouble scoring from saved bounds; direct CSV source counts; no model imports',checked_rank_rows=75,checked_bounds=750,unchanged_other_cells_each_alternative=249,source_hashes_verified=True,continuous_possible_city_witnesses=75,continuous_recommendation_leaves=6,maximum_score_or_regret_error=float(maxerror),maximum_certificate_gap_error=float(gaperror),paired_year_rank_changes=0,scope='Matched narrower school-headcount alternatives only; current V96 coverage remains unchanged.')
    (P/'independent_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
