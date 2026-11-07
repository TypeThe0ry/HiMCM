"""Shanghai year replacement and Warsaw teacher-allocation bounds; V30 baseline."""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_cape_town_revision import cape_bounds
from task4_continuous_preferences import feasible_preferences

def school_bounds(shanghai=True,warsaw=True):
    lo,hi=cape_bounds();j=NAMES.index('upper_secondary_ptr')
    if shanghai:
        source=ROOT/'data/task4_v32_shanghai'
        for m in json.loads((source/'manifest.json').read_text()):
            assert hashlib.sha256((source/m['file']).read_bytes()).hexdigest()==m['sha256']
        r=json.loads((source/'extracted.json').read_text());i=CITIES.index('Shanghai')
        assert r['city']=='Shanghai' and r['year']==2025
        np.testing.assert_allclose([lo[i,j],hi[i,j]],[15/(15+224186/22686)]*2,atol=1e-12,rtol=0)
        np.testing.assert_allclose(r['utility'],15/(15+r['students']/r['teachers']),atol=1e-12,rtol=0)
        lo[i,j]=hi[i,j]=r['utility']
    if warsaw:
        source=ROOT/'data/task4_v32_education';r=json.loads((source/'observation.json').read_text());i=CITIES.index('Warsaw')
        assert hashlib.sha256((source/'warsaw_2024.pdf').read_bytes()).hexdigest()==r['pdf_sha256']
        assert r['city']=='Warsaw' and r['school_year']=='2023/24'
        assert lo[i,j]==0 and hi[i,j]==1 and r['utility_lower']==0
        np.testing.assert_allclose(r['utility_upper'],15/(15+r['youth_pupils']/r['teacher_fte_upper_with_release_precision']),atol=1e-12,rtol=0)
        lo[i,j],hi[i,j]=r['utility_lower'],r['utility_upper']
    return lo,hi

def main():
    lo,hi=cape_bounds();base,_=summarize(lo,hi,weights());frames=[];bounds=[];stats=[]
    for label,s,w in [('v30_before',False,False),('shanghai_only',True,False),('warsaw_only',False,True),('both',True,True)]:
        l,h=school_bounds(s,w);keep=np.ones(l.shape,bool);j=NAMES.index('upper_secondary_ptr')
        for city,changed in [('Shanghai',s),('Warsaw',w)]:
            if changed:keep[CITIES.index(city),j]=False
        np.testing.assert_array_equal(l[keep],lo[keep]);np.testing.assert_array_equal(h[keep],hi[keep]);assert np.all((0<=l)&(l<=h)&(h<=1))
        f,d=summarize(l,h,weights());f['scenario']=label;frames.append(f)
        possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        stats.append(dict(scenario=label,choices=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_alpha_possible_champions=possible,changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),kendall_tau=float(kendalltau(f.decision_rank,base.decision_rank).statistic),cities=f[f.city.isin(['Shanghai','Warsaw','Phoenix','Cape Town'])][['city','decision_rank','score_lower','score_upper']].to_dict('records')))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=float(l[i,j]),upper=float(h[i,j])) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    out=ROOT/'results/task4_v32_school_stage';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    inputs=['data/task4_v32_shanghai/manifest.json','data/task4_v32_shanghai/extracted.json','data/task4_v32_shanghai/extract.py','data/task4_v32_education/observation.json','data/task4_v32_education/extract.py']
    summary=dict(main_admitted=False,new_city_indicator_cells=1,updated_year_cells=1,primary_scenario='both',alpha=.1,alpha_sensitivity=[.05,.2],scope='Regular high-school resource ratio. Warsaw youth schools with unknown teacher allocation, FTE versus other cities headcounts; conditional comparison, not direct educational attainment or causal quality.',sources=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in inputs],scenarios=stats)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k!='continuous_alpha_possible_champions'} for r in stats],indent=2))
if __name__=='__main__':main()
