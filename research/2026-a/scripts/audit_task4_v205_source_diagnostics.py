"""Independent controlled V205 mean-source diagnostic audit; stdout by default."""
from pathlib import Path
import hashlib,json,math
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,NAMES
from task4_user_v205_revision import revised_bounds
from audit_task4_v180_amsterdam import independent_scores
from task4_audit_output import audit_parser,check_output,emit_report
REFS={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.ones(10)/10}
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csv(p):return pd.read_csv(p,float_precision='round_trip')
def close(a,b,tol=1e-11):np.testing.assert_allclose(a,b,atol=tol,rtol=0)
def check_rows(cities,l,h,w,rows,allow_near_tie_ranks=False):
 saved=rows.set_index('city').loc[cities]; independent=independent_scores(l,h,w)
 for i,row in enumerate(independent):
  for key,value in row.items():
   if key in saved:close(saved.iloc[i][key],value)
 return len(saved)
def norms(z,w):
 positive=np.sqrt(np.sum(w*z*z,axis=-1));negative=np.sqrt(np.sum(w*(1-z)*(1-z),axis=-1));return 100*positive/(positive+negative)
def source_diagnostic_checks(frame,l,h):
    from scipy.optimize import brentq
    folder=ROOT/'results/task4_v205_source_diagnostics';report=read(folder/'summary.json')
    for p,digest in report['source_sha256'].items():assert sha(ROOT/p)==digest,p
    cities=frame.city.tolist();j=NAMES.index('travel');z=cities.index('Zurich');means=frame.commute_min.to_numpy(float);idx=np.flatnonzero(np.isfinite(means));assert len(idx)==12
    withdrawals={'retained_input':[],'withdraw_Zurich_work_commute':['Zurich'],'withdraw_Dublin_work_commute':['Dublin'],'withdraw_both_work_commute':['Zurich','Dublin'],'withdraw_all_submitted_commute_means':[cities[i] for i in idx]}
    ranks=csv(folder/'commute_withdrawal_ranks.csv');bounds=csv(folder/'commute_withdrawal_bounds.csv')
    for case,removed in withdrawals.items():
        a=l.copy()
        for city in removed:a[cities.index(city),j]=0
        b=bounds[bounds.scenario==case].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        close(b.lower.to_numpy().reshape(16,10),a,1e-15);close(b.upper.to_numpy().reshape(16,10),h,1e-15)
        for ref,w in REFS.items():check_rows(cities,a,h,w,ranks[(ranks.scenario==case)&(ranks.weight_reference==ref)])
    singles=read(folder/'mean_thresholds.json');joints=read(folder/'joint_thresholds.json');probes=csv(folder/'single_mean_probes.csv');pairs=csv(folder/'joint_pairwise_crossings.csv');cases=csv(folder/'joint_cases.csv');ncorner=0;results=[]
    for ref,w in REFS.items():
        def regrets(a):return np.array([x['max_regret'] for x in independent_scores(a,h,w)])
        def zg(u):
            a=l.copy();a[z,j]=u;r=regrets(a);return r[z]-np.delete(r,z).min()
        single=next(x for x in singles if x['weight_reference']==ref)
        for row in probes[probes.weight_reference==ref].itertuples():close(row.zurich_regret_minus_best_other,zg(row.lower_utility))
        close(single['gap_at_utility_0'],zg(0));close(single['gap_at_utility_1'],zg(1))
        if zg(0)>0>zg(1):
            u=brentq(zg,0,1,xtol=5e-16,rtol=1e-15);close(single['tie_mean_minutes'],-30*math.log(u),1e-10);assert single['status']=='finite_tie'
        else:assert single['tie_mean_minutes'] is None
        item=next(x for x in joints if x['weight_reference']==ref);target=cities.index(item['target']);assert item['target']==('Oslo' if ref=='fixed' else 'Zurich')
        def corner(delta):
            a=l.copy();a[idx,j]=np.exp(-means[idx]*(1-delta)/30)
            if target in idx:a[target,j]=math.exp(-means[target]*(1+delta)/30)
            return a
        def gap(d):
            r=regrets(corner(d));return r[target]-np.delete(r,target).min()
        close(item['gap_at_zero'],gap(0));close(item['gap_at_one'],gap(1));grid=[gap(d) for d in np.linspace(0,1,101)];assert all(b>=a-1e-10 for a,b in zip(grid,grid[1:]))
        if gap(0)<0<gap(1):
            root=brentq(gap,0,1,xtol=5e-16,rtol=1e-15);close(root,item['sharp_radius'],1e-12);assert gap(root-1e-7)<0<gap(root+1e-7)
        else:root=1;assert item['sharp_radius'] is None
        for row in pairs[pairs.weight_reference==ref].itertuples():
            k=cities.index(row.rival)
            def pg(d):r=regrets(corner(d));return r[target]-r[k]
            close(row.gap_at_zero,pg(0));close(row.gap_at_one,pg(1))
            if pd.notna(row.crossing_radius):close(row.crossing_radius,brentq(pg,0,1),1e-10)
        for row in cases[cases.weight_reference==ref].itertuples():close(row.gap,gap(row.radius))
        for delta in [.05,root]:
            bits=(np.arange(4096)[:,None]>>np.arange(12))&1;a=np.broadcast_to(l,(4096,16,10)).copy();a[:,idx,j]=np.exp(-means[idx][None,:]*(1+delta*(2*bits-1))/30)
            low=norms(a,w);upper=norms(h,w);C=np.array([np.delete(upper,i).max() for i in range(16)]);rg=np.maximum(0,C[None,:]-low);allg=rg[:,target]-np.delete(rg,target,axis=1).min(axis=1);close(allg.max(),gap(delta),1e-11);ncorner+=4096
        results.append({'reference':ref,'target':item['target'],'radius':root,'zurich_mean_tie':single['tie_mean_minutes']})
    return {'corners':ncorner,'targets':results,'withdrawal_cases':len(withdrawals)}

if __name__=='__main__':
 O=ROOT/'results/task4_v205_source_diagnostics';args=audit_parser(__doc__).parse_args();check_output(args,O/'verification.json',ROOT.parents[1])
 snapshot=ROOT/'design/task4_user_v205_snapshot.json';s=read(snapshot);bindings={**s['upstream_source_sha256'],**s['source_sha256']};assert len(bindings)==773
 for name,h in bindings.items():assert sha(ROOT/name)==h,name
 f,l,h=revised_bounds();result=source_diagnostic_checks(f,l,h)
 for name,digest in bindings.items():assert sha(ROOT/name)==digest,name
 result.update(status='pass',scope='Controlled V205 staging; independent numerical audit, no source admission or MC replay.',snapshot_sha256=sha(snapshot),science_bindings_checked=len(bindings),source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),*sorted(O.glob('*.csv')),*sorted(O.glob('*.json'))] if p.name!='verification.json'})
 emit_report(result,args,O/'verification.json',ROOT.parents[1])
