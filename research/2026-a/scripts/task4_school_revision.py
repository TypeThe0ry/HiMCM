"""V4: school-stage evidence, explicit scope transfer, and interval decisions.

Run offline. Missing observations are sets, never random imputed values.
The conditional model measures local diploma completion, not teaching causality.
"""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import rankdata, kendalltau
from task4_real_analysis import scores
from task4_interval_decision import interval_decision, voi_1d

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/task4_school'
OUT = ROOT / 'results/task4_school_revision'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def xlsx_sheet(path, sheet=2):
    """Read the archived simple data sheet without modifying the workbook."""
    with ZipFile(path) as z:
        strings = [''.join(si.itertext()) for si in ET.fromstring(
            z.read('xl/sharedStrings.xml')).findall('m:si', NS)]
        rows = []
        for row in ET.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml')).findall('.//m:row', NS):
            values = {}
            for cell in row:
                v = cell.find('m:v', NS)
                if v is None:
                    continue
                values[''.join(c for c in cell.get('r') if c.isalpha())] = (
                    strings[int(v.text)] if cell.get('t') == 's' else v.text)
            rows.append(values)
    columns = rows[0]
    return pd.DataFrame([{columns[k]: v for k, v in r.items() if k in columns} for r in rows[1:]])


def grouped_utility(counts, tau=30):
    """Sharp infimum/supremum for rounded-minute bins; no invented midpoints.

    Adjacent boundaries broaden 16--30 to (15,30], etc., conservatively.
    More-than-60 has no finite upper time cap, so its minimum utility is zero.
    """
    counts = np.asarray(counts, float)
    assert counts.shape == (5,) and np.all(counts >= 0) and counts.sum() > 0
    p = counts / counts.sum()
    return float(p @ np.exp(-np.array([15, 30, 45, 60, np.inf])/tau)), float(
        p @ np.exp(-np.array([0, 15, 30, 45, 60])/tau))


def extract_evidence():
    for row in json.loads((DATA/'manifest.json').read_text()):
        if 'sha256' in row:
            assert hashlib.sha256((DATA/row['file']).read_bytes()).hexdigest() == row['sha256']
    sg = pd.DataFrame(json.loads((DATA/'sg_travel_api.json').read_text())['result']['records'])
    groups = []
    for field in ['Secondary_Total', 'Post_Secondary_Non_Tertiary_Total']:
        counts = sg.loc[sg.Number != 'Total', field].astype(float).to_numpy()
        total = float(sg.loc[sg.Number == 'Total', field].iloc[0])
        assert abs(counts.sum()-total) <= 1  # published rounding, no hidden imputation
        lo, hi = grouped_utility(counts)
        groups.append(dict(city='Singapore', stage=field, year=2020,
                           count=int(counts.sum()), utility_lower=lo, utility_upper=hi,
                           within45_share=float(counts[:3].sum()/counts.sum())))
    pd.DataFrame(groups).to_csv(OUT/'singapore_stage_bounds.csv', index=False)
    sg.to_csv(OUT/'singapore_travel_counts.csv', index=False)
    nyc = xlsx_sheet(DATA/'nyc_graduation2025.xlsx')
    nyc.to_csv(OUT/'nyc_graduation_extracted.csv', index=False)
    row = nyc[(nyc['Category']=='All Students') & (nyc['Cohort Year']=='2021') &
              (nyc['Cohort']=='4 year August')].iloc[0]
    rate = float(row['# Grads'])/float(row['# Total Cohort'])
    assert abs(rate-float(row['% Grads'])/100) < 1e-7
    # Examination pass rates are genuinely upper-secondary evidence, but the
    # selected examination-taker denominator is NOT a grade-9 entrant cohort.
    exam = json.loads((DATA/'sg_alevel_api.json').read_text())['result']['records'][0]
    pd.DataFrame([dict(city='Singapore', year=2024, indicator='3H2 plus GP/KI among A-level takers',
                       value=float(exam['2024'])/100, admitted_to_completion_score=False),
                  dict(city='New York', year=2025, indicator='4-year August diploma among grade-9 entrants; non-charter',
                       value=rate, admitted_to_completion_score=True)]).to_csv(OUT/'education_outcomes.csv', index=False)
    from pypdf import PdfReader
    page=PdfReader(DATA/'denmark_youth2022.pdf').pages[9].extract_text()
    line=next(line for line in page.splitlines() if line.startswith('København '))
    percentages=[int(s[:-1]) for s in line.split() if s.endswith('%')]
    assert percentages == [92,100,100,81,100,100,53,100,100,66,100,100]
    pd.DataFrame([dict(city='Copenhagen',year=2022,age='15-19',programme=programme,
        nearest_school_15min_percent=percentages[3*i],nearest_school_30min_percent=percentages[3*i+1],
        nearest_school_45min_percent=percentages[3*i+2],admitted_as_actual_commute=False)
        for i,programme in enumerate(['STx','HF','HHx','HTx'])]).to_csv(OUT/'copenhagen_nearest_school_only.csv',index=False)
    return groups, rate


def score_bounds(z, lower, upper, education_weight=.1, travel_weight=.1):
    w = np.r_[np.full(4, (1-education_weight-travel_weight)/4), education_weight, travel_weight]
    return (scores(np.column_stack([z, lower]), w[None,:])[0],
            scores(np.column_stack([z, upper]), w[None,:])[0])


def rank_bounds(names, lo, hi, stage):
    exact=interval_decision(lo,hi)
    rows=[]
    for i, name in enumerate(names):
        other=np.arange(len(names))!=i
        rows.append(dict(city=name, stage=stage, score_lower=100*lo[i], score_upper=100*hi[i],
            best_rank=1+int(np.sum(lo[other]>hi[i]+1e-12)),
            worst_rank=1+int(np.sum(hi[other]>lo[i]+1e-12)),
            possible_champion=bool(hi[i]>=lo[other].max()-1e-12),
            necessary_champion=bool(lo[i]>=hi[other].max()-1e-12),
            max_regret=100*max(0., hi[other].max()-lo[i])))
    out=pd.DataFrame(rows)
    assert np.array_equal(out.best_rank.to_numpy(),exact['best_rank'])
    assert np.allclose(out.max_regret.to_numpy()/100,exact['max_regret'])
    out['decision_rank']=rankdata(out.max_regret, method='min').astype(int)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    groups, nyc_rate = extract_evidence()
    # Independent feasible within-bin time distributions must lie inside bounds.
    rng=np.random.default_rng(20261107)
    counts=np.array([3,7,11,5,2])
    gl,gh=grouped_utility(counts)
    for _ in range(100):
        t=np.r_[rng.uniform(0,15,3),rng.uniform(15,30,7),rng.uniform(30,45,11),
                rng.uniform(45,60,5),rng.uniform(60,600,2)]
        assert gl <= np.exp(-t/30).mean() <= gh
        assert np.exp(-t.mean()/30) <= np.exp(-t/30).mean()+1e-12
    old=pd.read_csv(ROOT/'results/task4_real/normalized_indicators.csv', index_col=0)
    names=old.index.to_numpy();z=old.to_numpy();n=len(names)
    lower=np.zeros((n,2));upper=np.ones((n,2));idx={name:i for i,name in enumerate(names)}
    # Conditional published-population transfer scenario; strict current-age
    # inference is separately reported and does not treat these as universal.
    lower[idx['New York'],0]=upper[idx['New York'],0]=nyc_rate
    lower[idx['New York'],1]=np.exp(-31.5/30)
    lower[idx['Singapore'],1]=min(r['utility_lower'] for r in groups)
    upper[idx['Singapore'],1]=max(r['utility_upper'] for r in groups)
    # Additional audited data, when present, are explicit rows with bounds.
    toronto=pd.read_csv(ROOT/'data/task4_school_quality_extra/toronto_extracted.csv')
    lower[idx['Toronto'],0]=float(toronto.four_year_completion.min())-.0005
    upper[idx['Toronto'],0]=float(toronto.four_year_completion.max())+.0005
    melbourne=pd.read_csv(ROOT/'data/task4_school_commute_extra/melbourne_summary.csv')
    mr=melbourne[melbourne.group=='secondary_15_19'].iloc[0]
    lower[idx['Melbourne'],1]=upper[idx['Melbourne'],1]=mr.mean_exp_utility_tau30
    assert np.all(lower>=0) and np.all(lower<=upper) and np.all(upper<=1)
    pd.DataFrame(dict(city=names,education_lower=lower[:,0],education_upper=upper[:,0],
                      travel_lower=lower[:,1],travel_upper=upper[:,1])).to_csv(OUT/'admitted_bounds.csv',index=False)
    before=score_bounds(z,np.zeros_like(lower),np.ones_like(upper))
    after=score_bounds(z,lower,upper)
    assert np.all(after[0]>=before[0]-1e-12) and np.all(after[1]<=before[1]+1e-12)
    b=rank_bounds(names,*before,'same_model_before_school_evidence')
    a=rank_bounds(names,*after,'conditional_school_evidence')
    pd.concat([b,a],ignore_index=True).to_csv(OUT/'rank_intervals.csv',index=False)
    previous=pd.read_csv(ROOT/'results/task4_access_revision/point_rankings.csv')
    comparison=a.merge(b[['city','best_rank','worst_rank','decision_rank']],on='city',suffixes=('_after','_before'))
    comparison=comparison.merge(previous[['city','V0_rank_common_sample','V3_rank']],on='city')
    comparison.sort_values('decision_rank_after').to_csv(OUT/'ranking_comparison.csv',index=False)
    stress=[]
    for eps in [0,.05,.1,.2]:
        l=np.maximum(0,lower-eps);h=np.minimum(1,upper+eps)
        r=rank_bounds(names,*score_bounds(z,l,h),f'utility_error_{eps}')
        stress.append(dict(assumed_utility_error=eps,possible_champions=r[r.possible_champion].city.tolist(),
                           minimax_choices=r[r.max_regret<=r.max_regret.min()+1e-10].city.tolist()))
    (OUT/'scope_and_time_stress.json').write_text(json.dumps(stress,indent=2)+'\n')
    boot=pd.read_csv(ROOT/'data/task4_school_commute_extra/melbourne_exploratory_bootstrap.csv')
    br=boot[(boot.group=='secondary_15_19')&(boot.statistic=='mean_exp_utility_tau30')].iloc[0]
    bl,bh=lower.copy(),upper.copy()
    bl[idx['Melbourne'],1]=br.exploratory_cluster_bootstrap_p025
    bh[idx['Melbourne'],1]=br.exploratory_cluster_bootstrap_p975
    bootstrap=rank_bounds(names,*score_bounds(z,bl,bh),'exploratory_melbourne_household_bootstrap')
    bootstrap.to_csv(OUT/'melbourne_sampling_sensitivity.csv',index=False)
    no_adult_w=np.r_[np.full(3,.8/3),.1,.1][None,:]
    no_adult=rank_bounds(names,
        scores(np.column_stack([z[:,:3],lower]),no_adult_w)[0],
        scores(np.column_stack([z[:,:3],upper]),no_adult_w)[0], 'adult_commute_removed')
    no_adult.to_csv(OUT/'adult_commute_ablation.csv',index=False)
    # No claimed extrapolation bound for unmatched exact ages, sectors or years.
    # Under a strict all-sector/current-14--18 target, those transfers are removed.
    b.assign(stage='strict_current_14_18_no_unverified_transfer').to_csv(OUT/'strict_scope_rank_intervals.csv',index=False)
    acquisition=[]
    for k,name in enumerate(names):
        for j,dimension in enumerate(['education','travel']):
            if upper[k,j]-lower[k,j] < 1e-12:
                continue
            def callback(x):
                ll,hh=lower.copy(),upper.copy()
                ll[k,j]=hh[k,j]=x
                return score_bounds(z,ll,hh)
            value=voi_1d(callback,k,float(lower[k,j]),float(upper[k,j]),baseline=after)
            acquisition.append(dict(city=name,dimension=dimension,
                guaranteed_regret_reduction_points=100*value['guaranteed_gain'],
                best_possible_regret_reduction_points=100*value['best_possible_gain'],
                worst_measurement_value=value['worst_x'],iterations=value['iterations']))
    pd.DataFrame(acquisition).sort_values(['guaranteed_regret_reduction_points','best_possible_regret_reduction_points'],
        ascending=False).to_csv(OUT/'evidence_acquisition_priority.csv',index=False)
    sensitivity=[]
    for ew in [.05,.1,.2]:
        for tw in [.05,.1,.2]:
            rr=rank_bounds(names,*score_bounds(z,lower,upper,ew,tw),'weights')
            sensitivity.append(dict(education_weight=ew,travel_weight=tw,
                possible_count=int(rr.possible_champion.sum()),possible_champions=';'.join(rr[rr.possible_champion].city),
                minimax_choice=';'.join(rr[rr.max_regret<=rr.max_regret.min()+1e-10].city)))
    pd.DataFrame(sensitivity).to_csv(OUT/'weight_sensitivity.csv',index=False)
    summary=dict(cities=n,conditional_education_observations=int(np.sum(upper[:,0]-lower[:,0]<1)),
        conditional_travel_observations=int(np.sum(upper[:,1]-lower[:,1]<1)),
        before_possible=b[b.possible_champion].city.tolist(),after_possible=a[a.possible_champion].city.tolist(),
        necessary_after=a[a.necessary_champion].city.tolist(),
        mean_interval_width_before=float((b.score_upper-b.score_lower).mean()),
        mean_interval_width_after=float((a.score_upper-a.score_lower).mean()),
        rank_intervals_changed=int(np.sum((a.best_rank!=b.best_rank)|(a.worst_rank!=b.worst_rank))),
        decision_ranks_changed=int(np.sum(a.decision_rank!=b.decision_rank)),
        kendall_decision_ranks=float(kendalltau(a.decision_rank,b.decision_rank).statistic),
        minimax_before=float(b.max_regret.min()),minimax_after=float(a.max_regret.min()),
        recommended=a[a.max_regret<=a.max_regret.min()+1e-10].city.tolist(),
        bootstrap_possible=bootstrap[bootstrap.possible_champion].city.tolist(),
        strict_scope_possible=b[b.possible_champion].city.tolist(),
        adult_commute_removed_possible=no_adult[no_adult.possible_champion].city.tolist(),
        warning='Conditional transfer of published cohorts/years; not a complete current 14-18 city ranking')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    selected=['Copenhagen','Dubai','Melbourne','Toronto','New York','Singapore','Tokyo']
    fig,ax=plt.subplots(1,2,figsize=(13,5.8),gridspec_kw={'width_ratios':[1.3,1]})
    for y,name in enumerate(selected):
        rb=b[b.city==name].iloc[0];ra=a[a.city==name].iloc[0]
        ax[0].plot([rb.score_lower,rb.score_upper],[y-.12,y-.12],color='#b3bec7',lw=6)
        ax[0].plot([ra.score_lower,ra.score_upper],[y+.12,y+.12],color='#087e8b',lw=6)
    ax[0].set_yticks(range(len(selected)),selected);ax[0].invert_yaxis()
    ax[0].set(xlabel='TOPSIS score bounds (gray: before; teal: after)',title='Same V4 weights: evidence update')
    ac=pd.read_csv(OUT/'evidence_acquisition_priority.csv').head(6)
    yy=np.arange(len(ac))
    ax[1].barh(yy,ac.best_possible_regret_reduction_points,color='#b3bec7',label='Best possible gain')
    ax[1].barh(yy,ac.guaranteed_regret_reduction_points,color='#087e8b',label='Guaranteed gain')
    ax[1].set_yticks(yy,ac.city+' / '+ac.dimension);ax[1].invert_yaxis()
    ax[1].set(xlabel='Potential regret reduction (score points)',title='Which exact measurement next?')
    ax[1].legend(fontsize=8)
    fig.suptitle('School-stage evidence with explicit cohort transfer\n12 possible champions remain; information value is prospective, not an observed improvement',fontsize=11)
    fig.tight_layout();fig.savefig(OUT/'school_revision.png',dpi=180);plt.close(fig)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
