"""Isolated previews of two real station-directory subsets; no primary admission."""
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_user_v181_revision import revised_bounds
from task4_user_city_indicators import SOURCE,evaluate
from task4_v5_model import ROOT,NAMES,weights
O=ROOT/'results/task4_v191_candidates'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    O.mkdir(exist_ok=True);frame,lo,hi=revised_bounds();cities=frame.city.tolist();j=NAMES.index('public_transport_density')
    observations=[];source_paths=[]
    for target,pop,year in [('tokyo',9983365,2026),('warsaw',1863800,2024)]:
        D=ROOT/('data/task4_v191_'+target);rows=json.loads((D/'observations.json').read_text());assert len(rows)==1
        row=rows[0];city=target.title();assert row['city']==city and row['indicator']=='public_transport_density'
        assert row['raw_count']==38 and row['population']==pop and row['population_year']==year
        i=cities.index(city);assert frame.iloc[i].population==pop and lo[i,j]==0 and hi[i,j]==1
        density=38*100000/pop;u=density/(50+density)
        np.testing.assert_allclose(row['utility_lower'],u,atol=1e-16,rtol=0);assert row['utility_upper']==1
        observations.append(dict(city=city,count=38,population=pop,population_year=year,density_per100000=density,utility_lower=u,utility_upper=1,inventory_reference_year=row.get('inventory_reference_year'),source_scope=row['source_scope']))
        source_paths.extend(p for p in D.iterdir() if p.is_file())
    profiles={'retained_V181':[],'Tokyo_candidate':['Tokyo'],'Warsaw_candidate':['Warsaw'],'both_candidates':['Tokyo','Warsaw']}
    ranks=[];bounds=[];reports=[]
    for profile,targets in profiles.items():
        a=lo.copy()
        for row in observations:
            if row['city'] in targets:a[cities.index(row['city']),j]=row['utility_lower']
        unchanged=np.ones((16,10),bool)
        for city in targets:unchanged[cities.index(city),j]=False
        np.testing.assert_array_equal(a[unchanged],lo[unchanged]);assert np.all(a>=lo)
        for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t=evaluate(cities,a,hi,w);ranks.append(t.assign(profile=profile,weight_reference=ref))
            baseline=evaluate(cities,lo,hi,w);width=float((t.score_upper-t.score_lower).mean());before=float((baseline.score_upper-baseline.score_lower).mean())
            reports.append(dict(profile=profile,weight_reference=ref,minimax_choices=t.loc[t.decision_rank.eq(1),'city'].tolist(),possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),mean_width=width,baseline_mean_width=before,conditional_width_reduction=before-width,conditional_width_reduction_percent=100*(before-width)/before,point_cells=int(np.isclose(a,hi,atol=1e-15,rtol=0).sum()),fully_missing_cells=int(((a==0)&(hi==1)).sum()),partial_cells=int(((a<hi)&~((a==0)&(hi==1))).sum())))
        bounds.extend(dict(profile=profile,city=c,indicator=n,lower=a[i,k],upper=hi[i,k]) for i,c in enumerate(cities) for k,n in enumerate(NAMES))
        # Withdrawal of exactly the admitted-to-preview cells restores V181.
        restored=a.copy()
        for city in targets:restored[cities.index(city),j]=0
        np.testing.assert_array_equal(restored,lo)
    pd.concat(ranks,ignore_index=True).to_csv(O/'profile_ranks.csv',index=False);pd.DataFrame(bounds).to_csv(O/'profile_bounds.csv',index=False)
    paths=[Path(__file__),SOURCE,ROOT/'scripts/task4_user_v181_revision.py',ROOT/'scripts/task4_user_city_indicators.py',ROOT/'scripts/task4_v5_model.py',ROOT/'scripts/task4_interval_decision.py']+source_paths
    summary=dict(version='V191 candidates',primary='V181 unchanged',paper='V189 unchanged',current_delivery='V190 unchanged',primary_admissions=0,actual_baseline_width_change=0,changed_cells_in_joint_preview=2,unchanged_cells_in_joint_preview=158,all_upper_bounds_unchanged=True,original_CSV_sha256=sha(SOURCE),observations=observations,profiles=reports,rank_rows=128,bound_rows=640,withdrawal_exactly_restores_V181=True,scope='Real provider directory subsets, not complete or contemporaneous all-mode inventories, observed teenage access or a city population revision. Tokyo inventory date unknown; catalogue metadata is separate. Conditional previews only; full extensions/manuscript consistency and explicit activation are still required before any primary-model change.',source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(paths))})
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');_,a,b=revised_bounds();np.testing.assert_array_equal(a,lo);np.testing.assert_array_equal(b,hi)
    print(json.dumps(reports,indent=2))
if __name__=='__main__':main()
