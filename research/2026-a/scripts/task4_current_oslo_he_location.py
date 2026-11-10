"""A conditional one-provider removal, without correcting the Oslo inventory."""
import argparse,csv,json
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES,SPEC,weights
R=Path(__file__).resolve().parents[1]

def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True)
    out=ap.parse_args().output_dir.resolve()
    if out.exists():raise FileExistsError('Use a new output directory')
    f,lo,hi=revised_bounds();cities=f.city.tolist();i=cities.index('Oslo');j=NAMES.index('research_he_density')
    raw=next(x for x in rows(R/'data/task4_v117_team_intake/city_indicators.csv') if x['city']=='Oslo')
    assert int(raw['he_count'])==25 and int(raw['population'])==727797 and SPEC[j][2]==1
    d=float((Decimal(24)*1000000/Decimal(raw['population'])).quantize(Decimal('.1'),rounding=ROUND_HALF_UP))
    campus=[x for x in rows(R/'data/current_oslo_dbh_campus/api_662.csv') if x['Institusjonskode']=='1405']
    assert len(campus)==22 and {x['Kommunenummer campus'] for x in campus}=={'0301'}
    out.mkdir(parents=True);pd.DataFrame(campus).to_csv(out/'campus_history.csv',index=False)
    cases=[];ranks=[];bounds=[]
    for scenario in ['retained_V203','conditional_count24']:
        ll=lo.copy();hh=hi.copy()
        if scenario=='conditional_count24':ll[i,j]=hh[i,j]=(d/10)/(1+d/10)
        mask=np.ones(lo.shape,dtype=bool);mask[i,j]=False
        assert np.array_equal(ll[mask],lo[mask]) and np.array_equal(hh[mask],hi[mask])
        bounds.extend(dict(scenario=scenario,city=c,indicator=n,lower=float(ll[a,b]),upper=float(hh[a,b])) for a,c in enumerate(cities) for b,n in enumerate(NAMES))
        for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t=evaluate(cities,ll,hh,w);os=t[t.city.eq('Oslo')].iloc[0]
            ranks.append(t.drop(columns=['midpoint_illustrative_score','midpoint_illustrative_rank']).assign(scenario=scenario,weight_reference=ref))
            cases.append(dict(scenario=scenario,weight_reference=ref,recommendations=t.loc[t.decision_rank.eq(1),'city'].tolist(),
                possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum()),
                mean_width=float((t.score_upper-t.score_lower).mean()),Oslo_lower=float(os.score_lower),Oslo_upper=float(os.score_upper),Oslo_regret=float(os.max_regret)))
    contrasts=[]
    for ref in ['fixed','equal']:
        base=next(x for x in cases if (x['scenario'],x['weight_reference'])==('retained_V203',ref))
        case=next(x for x in cases if (x['scenario'],x['weight_reference'])==('conditional_count24',ref))
        a=next(x for x in ranks if x.scenario.iloc[0]=='retained_V203' and x.weight_reference.iloc[0]==ref).set_index('city')
        b=next(x for x in ranks if x.scenario.iloc[0]=='conditional_count24' and x.weight_reference.iloc[0]==ref).set_index('city')
        contrasts.append(dict(weight_reference=ref,recommendation_changed=case['recommendations']!=base['recommendations'],
            decision_rank_changes=int((a.decision_rank!=b.decision_rank).sum()),
            Oslo_lower_change=case['Oslo_lower']-base['Oslo_lower'],Oslo_upper_change=case['Oslo_upper']-base['Oslo_upper'],
            mean_width_change=case['mean_width']-base['mean_width']))
    pd.concat(ranks,ignore_index=True).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'bounds.csv',index=False)
    summary=dict(primary_model='V203 unchanged',hypothetical_count=24,density_per_million=d,
        density_rule='24/retained population727797*1e6 rounded half-up to one decimal, then divide10 to per100k; utility x/(1+x).',
        assumption='One fewer provider than the supplied25, conditional diagnostic only; no assertion that Gestalt belonged to the original25 or that24 is a verified city count.',
        campus_history_rows=22,period_span=['2016spring','2026autumn'],cases=cases,contrasts=contrasts,
        primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
        scope='A point-relocation sensitivity, not a count correction, a source-certified interval, a provider-exclusion decision or a precision gain.')
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(density_per_million=d,contrasts=contrasts)))
if __name__=='__main__':main()
