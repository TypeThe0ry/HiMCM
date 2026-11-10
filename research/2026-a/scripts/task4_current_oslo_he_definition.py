"""DBH count-definition scenarios in temporary copies of user16 V203."""
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP
import csv,hashlib,json
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES,SPEC,weights
R=Path(__file__).resolve().parents[1];D=R/'data/current_oslo_dbh_campus'
O=R/'results/current_oslo_dbh_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def density(n,pop):return float((Decimal(n)*1000000/Decimal(pop)).quantize(Decimal('0.1'),rounding=ROUND_HALF_UP))
def main():
    source=json.loads((D/'enrolment_summary.json').read_text())
    with (R/'data/task4_v117_team_intake/city_indicators.csv').open(encoding='utf-8-sig') as f:raw=next(r for r in csv.DictReader(f) if r['city']=='Oslo')
    f,low,high=revised_bounds();cities=f.city.tolist();i=cities.index('Oslo');j=NAMES.index('research_he_density')
    pop=int(raw['population']);assert pop==727797 and int(raw['he_count'])==25 and float(raw['he_per_million'])==34.4
    assert density(25,pop)==34.4
    anchor=SPEC[j][2];assert anchor==1
    original_d=float(raw['he_per_million'])/10
    assert low[i,j]==high[i,j]==original_d/(anchor+original_d)
    definitions={23:'positive public values in institution/study-site modes1or4, each examined semester; narrow mode screen',
                 25:'positive public values in any mode, each examined semester',
                 26:'campus-registry codes,2025spring/fall or2026spring',
                 27:'campus-registry codes,2026fall'}
    assert {p['positive_any_mode_codes'] for p in source['periods']}=={25}
    assert {p['positive_mode1_or4_codes'] for p in source['periods']}=={23}
    assert [p['registry_distinct_institution_codes'] for p in source['periods']]==[26,26,26,27]
    scenarios=[('retained_V203',None)]+[(f'DBH_code_count_{n}',n) for n in definitions]
    allbounds=[];tables=[];cases=[]
    for scenario,n in scenarios:
        ll=low.copy();hh=high.copy();d=None
        if n is not None:
            d=density(n,pop)/10;ll[i,j]=hh[i,j]=d/(anchor+d)
        if n==25:assert np.array_equal(ll,low) and np.array_equal(hh,high)
        mask=np.ones(low.shape,dtype=bool);mask[i,j]=False
        assert np.array_equal(ll[mask],low[mask]) and np.array_equal(hh[mask],high[mask])
        allbounds.extend(dict(scenario=scenario,city=c,indicator=name,lower=float(ll[a,b]),upper=float(hh[a,b])) for a,c in enumerate(cities) for b,name in enumerate(NAMES))
        for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t=evaluate(cities,ll,hh,w);os=t[t.city.eq('Oslo')].iloc[0]
            tables.append(t.drop(columns=['midpoint_illustrative_score','midpoint_illustrative_rank']).assign(scenario=scenario,weight_reference=ref))
            cases.append(dict(scenario=scenario,weight_reference=ref,count=n,density_per_million=None if n is None else density(n,pop),
                recommendations=t.loc[t.decision_rank.eq(1),'city'].tolist(),possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),
                mean_width=float((t.score_upper-t.score_lower).mean()),Oslo_lower=float(os.score_lower),Oslo_upper=float(os.score_upper),Oslo_regret=float(os.max_regret),Oslo_rank=int(os.decision_rank)))
    contrasts=[]
    for c in cases:
        if c['scenario']=='retained_V203':continue
        base=next(x for x in cases if x['scenario']=='retained_V203' and x['weight_reference']==c['weight_reference'])
        a=next(t for t in tables if t.scenario.iloc[0]=='retained_V203' and t.weight_reference.iloc[0]==c['weight_reference']).set_index('city')
        b=next(t for t in tables if t.scenario.iloc[0]==c['scenario'] and t.weight_reference.iloc[0]==c['weight_reference']).set_index('city')
        contrasts.append(dict(scenario=c['scenario'],weight_reference=c['weight_reference'],decision_rank_changes=int((a.decision_rank!=b.decision_rank).sum()),
            recommendation_changed=c['recommendations']!=base['recommendations'],Oslo_lower_change=c['Oslo_lower']-base['Oslo_lower'],Oslo_upper_change=c['Oslo_upper']-base['Oslo_upper'],mean_width_change=c['mean_width']-base['mean_width']))
    O.mkdir(exist_ok=True);pd.concat(tables,ignore_index=True).to_csv(O/'ranks.csv',index=False);pd.DataFrame(allbounds).to_csv(O/'bounds.csv',index=False)
    summary=dict(primary_model='V203 unchanged',definitions=definitions,density_rule='Count/population727797*1e6,half-up to original one-decimal precision;divide10forper100k;utilityx/(1+x). This is a labeled counterfactual, not an admitted official density.',
        changed_cell='Oslo research_he_density only; other159ranges and weights fixed',cases=cases,contrasts=contrasts,
        rank_rows=160,bound_rows=800,primary_admissions=0,actual_primary_width_reduction=0,
        scope='DBH reported-code definition sensitivity, not true-provider bounds, empirical error probabilities or future trends. No primary input replacement.',
        source_sha256={str(p.relative_to(R)):sha(p) for p in [D/'enrolment_summary.json',D/'enrolment_response.csv',R/'data/task4_v117_team_intake/city_indicators.csv',Path(__file__)]},
        output_sha256={n:sha(O/n) for n in ['ranks.csv','bounds.csv']})
    (O/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(contrasts))
if __name__=='__main__':main()
