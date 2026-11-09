"""Independent scalar audit of deterministic V181 information-acquisition limits."""
from pathlib import Path
import hashlib,json,math,subprocess
from itertools import combinations
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v181_revision import revised_bounds
from task4_v5_model import ROOT,NAMES,SPEC
O=ROOT/'results/task4_v183_priority'
P=ROOT.parents[2]/'HiMCM-Overleaf'
TOL=1e-12

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def table(name):return pd.read_csv(O/(name+'.csv'),float_precision='round_trip').fillna('')
def close(a,b,tol=2e-10):np.testing.assert_allclose(a,b,rtol=0,atol=tol)
def scalar_scores(u,w):
    out=[]
    for row in u:
        a=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))
        b=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))
        out.append(100*a/(a+b))
    return np.array(out)
def decision(l,u):
    r=np.array([max(0.,max(u[k] for k in range(16) if k!=i)-l[i]) for i in range(16)])
    possible=[u[i]>=max(l[k] for k in range(16) if k!=i)-TOL for i in range(16)]
    necessary=[l[i]>=max(u[k] for k in range(16) if k!=i)-TOL for i in range(16)]
    return dict(regret=r,risk=float(r.min()),choices=[i for i in range(16) if r[i]<=r.min()+TOL],possible=possible,necessary=necessary)
def raw(j,x):
    if NAMES[j]=='travel':return None
    _,benefit,anchor,_=SPEC[j]
    return anchor*x/(1-x) if benefit and x<1 else (float('inf') if benefit or not x else anchor*(1-x)/x)
def main():
    f,lo,hi=revised_bounds();cities=f.city.tolist();start=np.stack([lo,hi]).copy()
    assert lo.shape==hi.shape==(16,10)
    missing=(lo==0)&(hi==1);assert [int((lo==hi).sum()),int(((lo<hi)&~missing).sum()),int(missing.sum())]==[112,35,13]
    registries={n:sha(ROOT/'design'/n) for n in ['task4_user_current_model.json','task4_user_current_extensions.json','task4_user_current_review.json']}
    tracked=subprocess.check_output(['git','-C',str(P),'ls-files','-z']).decode().split('\0')[:-1]
    paper={n:sha(P/n) for n in tracked}
    summary=read(O/'summary.json');assert summary['fully_missing_cells']==13 and summary['protected_nonfullymissing_cells']==147
    assert summary['point_cells']==112 and summary['partial_interval_cells']==35
    assert summary['no_MC_or_random_missing_value_completion']
    assert summary['version']=='V183 acquisition diagnosis on active V181 user16'
    for n,h in summary['source_sha256'].items():assert sha(ROOT/n)==h,n
    current=read(ROOT/'design/task4_user_current_model.json');assert current['version']=='V181' and current['module']=='task4_user_v181_revision'
    refs={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.full(10,.1)}
    expected={(ref,cities[i],NAMES[j]) for ref in refs for i,j in zip(*np.where(missing))}
    pr=table('priority');assert len(pr)==26
    assert set(zip(pr.weight_reference,pr.city,pr.indicator))==expected
    missing_rows=table('missing_cells');assert set(zip(missing_rows.city,missing_rows.indicator))=={(c,n) for _,c,n in expected}
    count=0
    def case(ref,city,indicators,x,exact=True):
        nonlocal count
        i=cities.index(city);js=[NAMES.index(n) for n in indicators.split(';')]
        assert all(missing[i,j] for j in js)
        a,b=lo.copy(),hi.copy();a[i,js]=x
        if exact:b[i,js]=x
        np.testing.assert_array_equal(a[~missing],lo[~missing]);np.testing.assert_array_equal(b[~missing],hi[~missing])
        l,u=scalar_scores(a,refs[ref]),scalar_scores(b,refs[ref]);count+=1
        return i,l,u,decision(l,u)
    baselines={}
    for ref,w in refs.items():
        l,u=scalar_scores(lo,w),scalar_scores(hi,w);d=decision(l,u);baselines[ref]=(l,u,d)
        saved=next(r for r in summary['baseline'] if r['weight_reference']==ref)
        close(saved['minimax_regret'],d['risk']);close(saved['mean_score_interval_width'],(u-l).mean())
        assert saved['choices']==[cities[i] for i in d['choices']]==['Zurich']
    for row in pr.itertuples():
        base=baselines[row.weight_reference][2]['risk']
        def branches(x):
            i,_,_,d=case(row.weight_reference,row.city,row.indicator,x)
            return float(d['regret'][i]),float(np.delete(d['regret'],i).min())
        def difference(x):a,b=branches(x);return a-b
        candidates=[0.,1.]
        if difference(0)*difference(1)<0:candidates.append(brentq(difference,0,1,xtol=1e-14))
        best=min(min(branches(x)) for x in [0.,1.]);worst=max(min(branches(x)) for x in candidates)
        close([row.best_post_regret,row.worst_post_regret],[best,worst])
        close([row.guaranteed_exact_resolution_regret_reduction,row.best_possible_exact_resolution_regret_reduction],[base-worst,base-best])
        endpoint=[case(row.weight_reference,row.city,row.indicator,x)[3] for x in [0.,1.]]
        assert row.optimistic_champion_exclusions==max(16-sum(d['possible']) for d in endpoint)
        close(row.current_focal_upper,baselines[row.weight_reference][1][cities.index(row.city)])
        for x in np.linspace(0,1,101):
            _,_,_,d=case(row.weight_reference,row.city,row.indicator,float(x))
            assert best-2e-10<=d['risk']<=worst+2e-10
    # All saved endpoints and partial-information probes use independently computed scores.
    endpoints=table('endpoint_information');joints=table('joint_endpoint_information');lower=table('lower_only_information')
    for name,data,is_exact in [('endpoint',endpoints,True),('joint',joints,True),('lower_only',lower,False)]:
        for row in data.to_dict('records'):
            indicators=row.get('indicator',row.get('indicators'));x=row.get('resolved_utility',row.get('observed_utility_lower'))
            i,l,u,d=case(row['weight_reference'],row['city'],indicators,x,is_exact)
            assert row['possible_count']==sum(d['possible'])
            assert row['excluded_cities']==';'.join(cities[k] for k in range(16) if not d['possible'][k])
            assert row['minimax_choices']==';'.join(cities[k] for k in d['choices'])
            close(row['minimax_regret_after'],d['risk']);close(row['minimax_regret_reduction'],baselines[row['weight_reference']][2]['risk']-d['risk'])
            close(row.get('focal_lower',row.get('focal_score_lower')),l[i]);close(row.get('focal_upper',row.get('focal_score_upper')),u[i])
            if 'focal_score_width_reduction' in row:
                before_l,before_u,_=baselines[row['weight_reference']]
                close(row['focal_score_width_reduction'],(before_u[i]-before_l[i])-(u[i]-l[i]))
            if not is_exact:assert row['retained_utility_upper']==1 and u[i]==baselines[row['weight_reference']][1][i]
    thresholds=table('exclusion_thresholds')
    for row in thresholds.itertuples():
        x=row.utility_threshold;target=cities.index(row.excluded_city)
        for dx in [-1e-7,1e-7]:
            i,l,u,d=case(row.weight_reference,row.source_city,row.indicator,x+dx)
            if row.direction=='lower_above':gap=l[i]-u[target]
            else:gap=u[i]-max(np.delete(l,i))
            assert gap*dx>0,(row,gap,dx)
        val=raw(NAMES.index(row.indicator),x)
        if val is not None:close(row.raw_PTR_or_density_threshold,val)
    switches=table('recommendation_thresholds')
    for row in switches.itertuples():
        x=row.utility_threshold;exact=row.acquisition=='exact_utility'
        for dx in [-1e-7,1e-7]:
            i,l,u,d=case(row.weight_reference,row.city,row.indicators,x+dx,exact)
            gap=d['regret'][i]-np.delete(d['regret'],i).min()
            assert gap*dx<0,(row,gap,dx)
        if row.indicators=='travel' and not exact:close(row.matched_mean_minutes_upper_for_Jensen_lower,-30*math.log(x))
    joint_limits=table('joint_subset_limits')
    expected_groups=set()
    for ref in refs:
        for i,city in enumerate(cities):
            indices=np.flatnonzero(missing[i]).tolist()
            for size in range(1,len(indices)+1):
                for group in combinations(indices,size):expected_groups.add((ref,city,';'.join(NAMES[j] for j in group)))
    assert set(zip(joint_limits.weight_reference,joint_limits.city,joint_limits.indicators))==expected_groups
    pd.testing.assert_frame_equal(table('joint_priority').reset_index(drop=True),joint_limits[joint_limits.all_city_full_missing_cells].reset_index(drop=True),check_exact=True)
    for row in joint_limits.itertuples():
        i=cities.index(row.city);js=row.indicators.split(';')
        assert row.cell_count==len(js) and row.all_city_full_missing_cells==(len(js)==int(missing[i].sum()))
        subset=joints[(joints.weight_reference==row.weight_reference)&(joints.city==row.city)&(joints.indicators==row.indicators)]
        assert len(subset)==2
        assert row.optimistic_champion_exclusions==max(16-subset.possible_count)
        close(row.best_endpoint_regret_reduction,subset.minimax_regret_reduction.max())
    partial=table('partial_priority');partial_endpoints=table('partial_endpoints');partial_summary=read(O/'partial_summary.json')
    for n,h in partial_summary['source_sha256'].items():assert sha(ROOT/n)==h,n
    partial_mask=(lo<hi)&~missing;assert int(partial_mask.sum())==35
    expected_partial={(ref,cities[i],NAMES[j]) for ref in refs for i,j in zip(*np.where(partial_mask))}
    assert len(partial)==70 and set(zip(partial.weight_reference,partial.city,partial.indicator))==expected_partial
    def partial_case(ref,city,indicator,x):
        nonlocal count
        i,j=cities.index(city),NAMES.index(indicator);assert partial_mask[i,j] and lo[i,j]<=x<=hi[i,j]
        a,b=lo.copy(),hi.copy();a[i,j]=b[i,j]=x
        mask=np.ones((16,10),bool);mask[i,j]=False
        np.testing.assert_array_equal(np.stack([a,b])[:,mask],start[:,mask])
        l,u=scalar_scores(a,refs[ref]),scalar_scores(b,refs[ref]);count+=1
        return i,l,u,decision(l,u)
    for row in partial.itertuples():
        i,j=cities.index(row.city),NAMES.index(row.indicator)
        close([row.current_lower,row.current_upper],[lo[i,j],hi[i,j]],2e-15)
        def branches(x):
            k,_,_,d=partial_case(row.weight_reference,row.city,row.indicator,x)
            return float(d['regret'][k]),float(np.delete(d['regret'],k).min())
        def difference(x):a,b=branches(x);return a-b
        left,right=float(lo[i,j]),float(hi[i,j]);candidates=[left,right]
        if difference(left)*difference(right)<0:candidates.append(brentq(difference,left,right,xtol=1e-14))
        best=min(min(branches(x)) for x in [left,right]);worst=max(min(branches(x)) for x in candidates)
        close([row.best_post_regret,row.worst_post_regret],[best,worst])
        base=baselines[row.weight_reference][2]['risk']
        close([row.guaranteed_exact_resolution_regret_reduction,row.best_possible_exact_resolution_regret_reduction],[base-worst,base-best])
        endpoints_case=[partial_case(row.weight_reference,row.city,row.indicator,x)[3] for x in [left,right]]
        assert row.optimistic_champion_exclusions==max(16-sum(d['possible']) for d in endpoints_case)
        for x in np.linspace(left,right,31):
            _,_,_,d=partial_case(row.weight_reference,row.city,row.indicator,float(x))
            assert best-2e-10<=d['risk']<=worst+2e-10
            assert 16-sum(d['possible'])<=row.optimistic_champion_exclusions
    assert len(partial_endpoints)==140
    for row in partial_endpoints.itertuples():
        _,_,_,d=partial_case(row.weight_reference,row.city,row.indicator,row.resolved_utility)
        close(row.minimax_regret,d['risk']);assert row.possible_count==sum(d['possible'])
        assert row.conservative_recommendation==';'.join(cities[k] for k in d['choices'])
        assert row.excluded_cities==';'.join(cities[k] for k in range(16) if not d['possible'][k])
    combined=table('all_uncertain_priority');assert len(combined)==96
    assert set(zip(combined.weight_reference,combined.city,combined.indicator))==expected|expected_partial
    cols=['guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','optimistic_champion_exclusions','worst_post_regret','best_post_regret']
    keys=['weight_reference','city','indicator']
    for source in [pr,partial]:
        joined=combined.merge(source,on=keys,suffixes=('_combined','_source'),validate='one_to_one')
        assert len(joined)==len(source)
        for col in cols:close(joined[col+'_combined'],joined[col+'_source'],2e-14)
    comparison=table('V155_comparison');old=pd.read_csv(ROOT/'results/task4_v155_priority/priority.csv',float_precision='round_trip')
    removed=comparison[comparison._merge=='right_only'];assert set(zip(removed.city,removed.indicator))=={('Amsterdam','public_transport_density')}
    assert len(removed)==2 and len(comparison[comparison._merge=='both'])==26 and not any(comparison._merge=='left_only')
    for metric in ['guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','optimistic_champion_exclusions']:
        joined=pr.merge(old,on=['weight_reference','city','indicator'],suffixes=('_new','_old'),validate='one_to_one')
        close(summary['V155_comparison']['maximum_absolute_metric_changes'][metric],abs(joined[metric+'_new']-joined[metric+'_old']).max())
    new_originals={};retrieval_manifests={};failed_responses=0
    for folder in ['task4_v183_teacher','task4_v183_travel']:
        directory=ROOT/'data'/folder;manifest=directory/'retrievals.json';retrieval_manifests[str(manifest.relative_to(ROOT))]=sha(manifest)
        for record in read(manifest):
            status=record.get('http_status',record.get('status'))
            path=directory/record['file']
            if status==200:
                assert path.is_file() and path.stat().st_size==record['bytes'] and sha(path)==record['sha256'],record['file']
                assert record['url'].startswith('https://') and record['accessed_utc']
                new_originals[str(path.relative_to(ROOT))]=sha(path)
            else:
                assert status==403 and record['response_body_archived'] is False and not path.exists()
                failed_responses+=1
    assert len(new_originals)==3 and failed_responses==1
    travel_findings_path=ROOT/'data/task4_v183_travel/findings.json'
    travel_findings=read(travel_findings_path)
    tokyo=next(r for r in travel_findings['sources'] if r['file']=='tokyo2024_timeuse_original.csv')
    tokyo_lines=(ROOT/'data/task4_v183_travel/tokyo2024_timeuse_original.csv').read_bytes().decode('utf-8-sig').splitlines()
    assert 'TOKYO STATISTICAL YEARBOOK' in tokyo_lines[53] and '( 2024 )' in tokyo_lines[53]
    assert 'DAILY AVERAGE OF FULL WEEK' in tokyo_lines[54] and '( 2021 )' in tokyo_lines[54] and '令和3年' in tokyo_lines[54]
    assert tokyo['yearbook_edition']==2024 and tokyo['observation_year']==2021
    assert 'line55' in tokyo['year_evidence'] and '2024 is yearbook edition' in tokyo['year_evidence']
    assert tokyo['admission']=='rejected_for_current_school_travel' and travel_findings['primary_admissions']==0
    travel_findings_sha256=sha(travel_findings_path)
    np.testing.assert_array_equal(np.stack(revised_bounds()[1:]),start)
    for n,h in registries.items():assert sha(ROOT/'design'/n)==h,n
    for n,h in paper.items():assert sha(P/n)==h,n
    for n,h in summary['source_sha256'].items():assert sha(ROOT/n)==h,n
    outputs={str(p.relative_to(ROOT)):sha(p) for p in O.iterdir() if p.is_file() and p.name!='verification.json'}
    result=dict(version='V183 priority independent audit',status='pass',primary='V181 unchanged',paper='V182 unchanged',missing_cells=13,protected_nonfullymissing_cells=147,exact_resolution_envelopes_independently_optimized=96,fullymissing_envelopes=26,partial_envelopes=70,partial_endpoint_rows=140,partial_interior_probes=2170,combined_priority_rows=96,scalar_conditioned_evaluations=count,single_envelope_grid_points=2626,endpoint_rows=len(endpoints),joint_endpoint_rows=len(joints),lower_only_rows=len(lower),exclusion_thresholds=len(thresholds),recommendation_switches=len(switches),all_saved_rows_independently_recomputed=True,other147cells_and_current160bounds_unchanged=True,three_current_registries_unchanged=True,existing_paper_files_unchanged=len(paper),only_removed_missing_key=['Amsterdam','public_transport_density'],V155_remaining_paired_rows=26,raw_scope='Exact utility identification and limiting closed endpoints; no source availability probabilities or observed improvement; lower-only cases retain upper1',verifier_sha256=sha(Path(__file__)),source_sha256=summary['source_sha256'],new_original_response_hashes_checked=new_originals,retrieval_manifest_sha256=retrieval_manifests,failed_response_without_archived_body_checked=failed_responses,tokyo_observation_year_independently_verified=2021,tokyo_yearbook_edition_independently_verified=2024,travel_findings_sha256=travel_findings_sha256,original_response_audit_scope='Archived response bytes/status/length/SHA and Tokyo observation-year footer verified; remaining semantic admissibility reviewed separately',audited_output_sha256=outputs)
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','audited_output_sha256']},indent=2))
if __name__=='__main__':main()
