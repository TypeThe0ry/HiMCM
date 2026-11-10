"""Common-publisher-edition alternatives; retained user16 V203 stays authoritative."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES,weights
from audit_current_oslo_cost_ptr_sources import table_rows

R=Path(__file__).resolve().parents[1];O=R/'results/current_cost_edition_review'
S=R/'data/city_matrix_25_audit/sources'
SPECS=[('cost-of-living','Cost of Living Index','cost_living_index',100),('property-investment','Price To Income Ratio','price_income_ratio',10)]
EDITIONS=['2026','mid','current']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    f,low,high=revised_bounds();cities=f.city.tolist();assert len(cities)==16
    scenarios={'retained_V203':(low,high)};values=[];source_files=[];changed={}
    for edition in EDITIONS:
        ll=low.copy();hh=high.copy()
        for kind,header,name,anchor in SPECS:
            path=S/f'{kind}_{edition}.html';source_files.append(path)
            table=table_rows(path);heads=[r for r in table if 'City' in r and header in r];assert len(heads)==1
            ci=heads[0].index('City');vi=heads[0].index(header)
            for i,row in f.iterrows():
                country='Czech Republic' if row.country=='Czechia' else row.country
                label=row.city+', '+country
                selected=[r for r in table if len(r)>vi and r[ci]==label];assert len(selected)==1,label
                v=float(selected[0][vi]);j=NAMES.index(name)
                ll[i,j]=hh[i,j]=anchor/(anchor+v)
                values.append(dict(edition=edition,city=row.city,indicator=name,source_label=label,publisher_value=v))
        mask=np.ones(low.shape,dtype=bool);mask[:,[NAMES.index(x[2]) for x in SPECS]]=False
        assert np.array_equal(ll[mask],low[mask]) and np.array_equal(hh[mask],high[mask])
        changed[edition]=int(np.count_nonzero(ll!=low));scenarios[edition]=(ll,hh)
    tables=[];bounds=[];cases=[]
    for scenario,(ll,hh) in scenarios.items():
        bounds.extend(dict(scenario=scenario,city=city,indicator=name,lower=float(ll[i,j]),upper=float(hh[i,j])) for i,city in enumerate(cities) for j,name in enumerate(NAMES))
        for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t=evaluate(cities,ll,hh,w)
            tables.append(t.drop(columns=['midpoint_illustrative_score','midpoint_illustrative_rank']).assign(scenario=scenario,weight_reference=ref))
            cases.append(dict(scenario=scenario,weight_reference=ref,recommendations=t.loc[t.decision_rank.eq(1),'city'].tolist(),top_three=t.sort_values('decision_rank').head(3).city.tolist(),mean_width=float((t.score_upper-t.score_lower).mean()),possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum())))
    ranks=pd.concat(tables,ignore_index=True);contrasts=[]
    for ref in ['fixed','equal']:
        before=ranks[ranks.scenario.eq('retained_V203')&ranks.weight_reference.eq(ref)].set_index('city').loc[cities]
        for edition in EDITIONS:
            after=ranks[ranks.scenario.eq(edition)&ranks.weight_reference.eq(ref)].set_index('city').loc[cities]
            contrasts.append(dict(edition=edition,weight_reference=ref,changed_decision_ranks=int((before.decision_rank!=after.decision_rank).sum()),changed_cities=after.index[before.decision_rank!=after.decision_rank].tolist(),mean_width_change=float((after.score_upper-after.score_lower).mean()-(before.score_upper-before.score_lower).mean()),largest_absolute_lower_score_change=float((after.score_lower-before.score_lower).abs().max()),largest_absolute_upper_score_change=float((after.score_upper-before.score_upper).abs().max())))
    O.mkdir(exist_ok=True)
    for name,table in [('ranks.csv',ranks),('bounds.csv',pd.DataFrame(bounds)),('edition_values.csv',pd.DataFrame(values))]:table.to_csv(O/name,index=False)
    summary=dict(primary_model='V203 unchanged',scenario='Replace only the32cost/housing points by matching named-city values from one archived publisher edition at a time',editions=EDITIONS,targeted_point_cells=32,actually_changed_point_cells=changed,other128cells_unchanged=True,rank_rows=128,bound_rows=640,publisher_value_rows=96,cases=cases,contrasts=contrasts,primary_admissions=0,actual_primary_width_reduction=0,source_sha256={str(p.relative_to(R)):sha(p) for p in source_files+[R/'data/task4_v117_team_intake/city_indicators.csv',R/'data/city_matrix_25_audit/provenance.json',R/'scripts/audit_current_oslo_cost_ptr_sources.py',Path(__file__)]},output_sha256={name:sha(O/name) for name in ['ranks.csv','bounds.csv','edition_values.csv']},scope='Source-edition sensitivity, not an input correction, temporal trend, annual-calendar measurement, original extraction lineage, household-budget validation or municipal-boundary harmonization. Fixed ideal points, original weights and other128ranges retained; no Monte Carlo replay or missing-data admission. Current is the archived snapshot, not a live table.')
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'changed_point_cells':changed,'contrasts':contrasts,'choices':[(x['scenario'],x['weight_reference'],x['recommendations']) for x in cases]}))

if __name__=='__main__':main()
