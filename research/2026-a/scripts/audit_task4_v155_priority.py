"""Independent deterministic information-value audit on the current V154 bounds."""
from pathlib import Path
import hashlib,json,math
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v154_revision import revised_bounds
from task4_v5_model import ROOT,NAMES

O=ROOT/'results/task4_v155_priority'
P=Path('/data/projects/HiMCM-Overleaf')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())

def decisions(lo,hi,w):
    def scores(z):
        a=np.linalg.norm(z*np.sqrt(w),axis=1)
        b=np.linalg.norm((1-z)*np.sqrt(w),axis=1)
        return 100*a/(a+b)
    L,U=scores(lo),scores(hi)
    regret=np.array([max(0,np.delete(U,k).max()-L[k]) for k in range(16)])
    possible=np.array([U[k]>=np.delete(L,k).max()-1e-12 for k in range(16)])
    return L,U,regret,possible


def main():
    f,lo,hi=revised_bounds();cities=f.city.tolist();summary=read(O/'summary.json');residual=read(O/'milan_residual_summary.json')
    for n,h in summary['source_sha256'].items():assert sha(ROOT/n)==h,n
    for n,h in residual['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert sha(ROOT/'scripts/task4_v155_milan_residual.py')==residual['generator_sha256']
    assert sha(O/'milan_residual_grid.csv')==residual['result_sha256']['milan_residual_grid.csv']
    missing={(cities[i],NAMES[j]) for i,j in np.argwhere((lo==0)&(hi==1))}
    recorded=pd.read_csv(O/'missing_cells.csv')
    assert len(missing)==len(recorded)==14
    assert set(zip(recorded.city,recorded.indicator))==missing
    assert ('Milan','public_transport_density') not in missing
    priority=pd.read_csv(O/'priority.csv');assert len(priority)==28
    refs={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.ones(10)/10}
    evaluations=0
    for row in priority.itertuples():
        i,j=cities.index(row.city),NAMES.index(row.indicator);w=refs[row.weight_reference]
        L,U,r,p=decisions(lo,hi,w);base=r.min()
        def at(x):
            nonlocal evaluations
            a,b=lo.copy(),hi.copy();a[i,j]=b[i,j]=x
            v=decisions(a,b,w);evaluations+=1
            return v
        def gap(x):
            rr=at(x)[2]
            return rr[i]-np.delete(rr,i).min()
        candidates=[0.,1.]
        if gap(0)*gap(1)<0:candidates.append(float(brentq(gap,0,1,xtol=1e-14)))
        risks=[at(x)[2].min() for x in candidates]
        best,worst=min(risks),max(risks)
        np.testing.assert_allclose([row.guaranteed_exact_resolution_regret_reduction,row.best_possible_exact_resolution_regret_reduction,row.best_post_regret,row.worst_post_regret],
                                   [base-worst,base-best,best,worst],atol=1e-9,rtol=0)
        exclusions=max(16-int(at(x)[3].sum()) for x in [0,1])
        assert exclusions==row.optimistic_champion_exclusions
        for x in np.linspace(0,1,11):
            value=at(float(x));assert best-1e-9<=value[2].min()<=worst+1e-9
            assert 16-int(value[3].sum())<=exclusions
    comparison=pd.read_csv(O/'V138_comparison.csv')
    removed=comparison[comparison._merge=='right_only']
    assert set(zip(removed.city,removed.indicator))=={('Milan','public_transport_density')}
    assert len(removed)==2 and len(comparison[comparison._merge=='both'])==28
    residual_grid=pd.read_csv(O/'milan_residual_grid.csv')
    assert len(residual_grid)==1848
    m=cities.index('Milan');t=NAMES.index('public_transport_density');q=NAMES.index('upper_secondary_ptr')
    for row in residual_grid.itertuples():
        a,b=lo.copy(),hi.copy();a[m,t]=row.transport_utility
        if row.mode=='exact':b[m,t]=row.transport_utility
        if not pd.isna(row.teacher_utility):
            a[m,q]=row.teacher_utility
            if row.mode=='exact':b[m,q]=row.teacher_utility
        w=refs[row.weight_reference];L,U,rr,pp=decisions(a,b,w);risk=decisions(lo,hi,w)[2].min()
        np.testing.assert_allclose([row.minimax_regret,row.regret_reduction,row.milan_score_lower,row.milan_score_upper],
                                   [rr.min(),risk-rr.min(),L[m],U[m]],atol=1e-10,rtol=0)
        assert row.possible_count==pp.sum()
        assert set(str(row.minimax_choices).split(';'))=={cities[k] for k in range(16) if rr[k]<=rr.min()+1e-12}
        evaluations+=1
    analytic=[]
    for ref,w in refs.items():
        L,U,rr,pp=decisions(lo,hi,w)
        # Across all lower-bound-only joint evidence, only Milan's lower score
        # increases. At its maximum, no other upper score is overtaken.
        a=lo.copy();a[m,[t,q]]=1
        max_L,_,_,_=decisions(a,hi,w)
        other=np.arange(16)!=m
        assert max_L[m]<U[other].min()
        assert U[m]>L[other].max()
        # For transport-only exact information, its lowest possible upper and
        # highest possible lower scores also leave all16 possible.
        endpoint=[]
        for x in [lo[m,t],1.]:
            a,b=lo.copy(),hi.copy();a[m,t]=b[m,t]=x
            endpoint.append(decisions(a,b,w))
        assert endpoint[0][1][m]>=L[other].max()
        assert endpoint[1][0][m]<=U[other].min()
        # Milan never becomes the best action even at its maximum transport
        # utility. Other actions' minimum regret is nondecreasing in that
        # utility; equal endpoint minima force it to be constant throughout.
        low_regret,high_regret=endpoint[0][2],endpoint[1][2]
        assert high_regret[m]>=np.delete(high_regret,m).min()
        assert abs(np.delete(low_regret,m).min()-np.delete(high_regret,m).min())<1e-12
        expected=next(x for x in residual['cases'] if x['weight_reference']==ref)
        grid=residual_grid[(residual_grid.weight_reference==ref)&(residual_grid.group=='transport_and_PTR')]
        assert (16-grid.possible_count).max()<=expected['joint_optimistic_champion_exclusions']
        assert grid.regret_reduction.max()<=expected['joint_endpoint_best_risk_reduction']+1e-10
        analytic.append(dict(weight_reference=ref,lower_only_joint_exclusion_ceiling=0,
                             exact_transport_exclusion_ceiling=0,exact_transport_regret_gain_ceiling=0,
                             max_joint_Milan_lower=float(max_L[m]),minimum_other_upper=float(U[other].min())))
    prior=read(ROOT/'results/task4_v151_shared_entry/verification.json');papers=dict(prior['manuscript_files_unchanged_sha256'])
    for folder,key in [('task4_v151_shared_entry','support_file_sha256'),('task4_v152_tail_access','selected_file_sha256'),('task4_v153_milan_proposal','selected_file_sha256'),('task4_v154_transition','selected_file_sha256')]:papers.update(read(ROOT/'results'/folder/'delivery.json')[key])
    for n,h in papers.items():assert sha(P/n)==h,n
    snapshot=read(ROOT/'design/task4_user_v154_snapshot.json')
    for n,h in snapshot['source_sha256'].items():assert sha(ROOT/n)==h,n
    result_files={p.name:sha(p) for p in sorted(O.iterdir()) if p.is_file() and p.suffix in ['.json','.csv'] and p.name not in ['verification.json','delivery.json','sync.json']}
    result=dict(status='pass',version='V155',primary='V154 unchanged',fully_missing_cells=14,nonfullymissing_protected_cells=146,
                exact_single_cell_cases=28,independent_score_and_decision_evaluations=evaluations,residual_grid_cases=1848,
                analytic_partial_information_limits=analytic,current_snapshot_files_unchanged=len(snapshot['source_sha256']),
                existing_manuscript_files_unchanged=len(papers),new_data_admissions=0,primary_score_width_reduction=0,
                primary_pdf_sha256=sha(P/'drafts/task4_v154_paper.pdf'),no_MC_or_missing_value_imputation=True,
                result_sha256=result_files,verifier_sha256=sha(Path(__file__)))
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','exact_single_cell_cases','residual_grid_cases','independent_score_and_decision_evaluations','current_snapshot_files_unchanged','existing_manuscript_files_unchanged']},indent=2))

if __name__=='__main__':main()
