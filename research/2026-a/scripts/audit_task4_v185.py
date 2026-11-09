"""Independently check V185 source identities and separate conditional profiles."""
from pathlib import Path
import hashlib,json,math,xml.etree.ElementTree as E
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v181_revision import revised_bounds
from task4_v5_model import ROOT,NAMES
O=ROOT/'results/task4_v185_commute_candidate';P=ROOT.parents[2]/'HiMCM-Overleaf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def close(a,b,tol=2e-11):np.testing.assert_allclose(a,b,atol=tol,rtol=0)
def jsoncell(d,selection):
    n=0
    for name,size in zip(d['id'],d['size']):
        idx=d['dimension'][name]['category']['index'];position=idx[selection[name]] if isinstance(idx,dict) else idx.index(selection[name]);n=n*size+position
    v=d['value'];return v.get(str(n)) if isinstance(v,dict) else v[n]
def raw_sources():
    identities={};success=failed=0
    for directory in ['task4_v185_dublin_bins','task4_v185_zurich_bins','task4_v185_madrid_teacher']:
        D=ROOT/'data'/directory
        for row in read(D/'retrievals.json'):
            path=D/row['file'] if row.get('file') else None;status=row.get('http_status',row.get('status'))
            if status==200:
                assert path is not None and path.is_file(),path
                assert path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],path
                if path.suffix=='.pdf':assert path.read_bytes().startswith(b'%PDF-'),path
                elif path.suffix=='.json':assert isinstance(read(path),dict),path
                elif path.suffix=='.xml':E.parse(path)
                identities[str(path.relative_to(ROOT))]=sha(path);success+=1
            else:
                assert row.get('response_body_archived') is False and (path is None or not path.exists()),path
                failed+=1
        identities[str((D/'retrievals.json').relative_to(ROOT))]=sha(D/'retrievals.json')
    D=ROOT/'data/task4_v185_dublin_bins';d=read(D/'cso_F7068_original.json')
    assert d['id']==['STATISTIC','TLIST(A1)','C02199V02655','C04104V04868']
    code=next(k for k,v in d['dimension']['C04104V04868']['category']['label'].items() if v=='Dublin City')
    values=[jsoncell(d,{'STATISTIC':f'F7068C{k:02d}','TLIST(A1)':'2011','C02199V02655':'-','C04104V04868':code}) for k in range(1,10)]
    assert values==[215384,34770,75667,57683,17420,11337,2226,16281,27.1]
    assert sum(values[1:8])==values[0]
    lowers=[0,15,30,45,60,90];uppers=[15,30,45,60,90,None]
    utility_lower=math.fsum(n*(math.exp(-t/30) if t is not None else 0) for n,t in zip(values[1:7],uppers))/values[0]
    utility_upper=(math.fsum(n*math.exp(-t/30) for n,t in zip(values[1:7],lowers))+values[7])/values[0]
    D=ROOT/'data/task4_v185_zurich_bins';root=E.parse(D/'bfs_2026_worktime_data_original.xml').getroot();ns={'g':'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic'}
    dataset=root.find('.//{*}DataSet');attrs={v.get('id'):v.get('value') for v in dataset.findall('g:Attributes/g:Value',ns)}
    assert attrs['PERIOD']=='31.12.2023' and attrs['REGION_REF']=='POLG'
    swiss={}
    for obs in dataset.findall('g:Obs',ns):
        key={v.get('id'):v.get('value') for v in obs.findall('g:ObsKey/g:Value',ns)}
        if key.get('SSV_SWISS_CITY')!='261' or key.get('COMMUTE_TIME')!='DUR':continue
        value=float(obs.find('g:ObsValue',ns).get('value'));a={v.get('id'):v.get('value') for v in obs.findall('g:Attributes/g:Value',ns)};swiss[key['STATISTICAL_OPERATION']]=(value,a)
    assert swiss['OBS'][0]==34.22050361 and swiss['OBS'][1]['UNIT_MEASURE']=='MN'
    assert swiss['CI'][0]==1.949499193 and swiss['CI'][1]['UNIT_MEASURE']=='PT'
    structure=E.parse(D/'bfs_2026_worktime_structure_original.xml').getroot();unit=next(n for n in structure.findall('.//{*}Codelist') if n.get('id')=='CL_UNIT_MEASURE');pt=next(n for n in unit.findall('{*}Code') if n.get('id')=='PT')
    assert 'Percent' in [n.text for n in pt.findall('{*}Name')]
    citycodes=next(n for n in structure.findall('.//{*}Codelist') if n.get('id')=='CL_SSV_SWISS_CITY');citynode=next(n for n in citycodes.findall('{*}Code') if n.get('id')=='261');assert 'Zürich' in [n.text for n in citynode.findall('{*}Name')]
    durcodes=next(n for n in structure.findall('.//{*}Codelist') if n.get('id')=='CL_SSV_LABMAR_08');dur=next(n for n in durcodes.findall('{*}Code') if n.get('id')=='DUR');assert 'Durchschnittliche Arbeitswegzeit' in [n.text for n in dur.findall('{*}Name')]
    return dict(successful_original_responses=success,failed_requests_without_fake_original=failed,Dublin_values=values,Dublin_utility_lower=utility_lower,Dublin_utility_upper=utility_upper,Swiss_period=attrs['PERIOD'],Swiss_mean_minutes=swiss['OBS'][0],Swiss_CI_published_value=swiss['CI'][0],Swiss_CI_unit='PT Percent',Swiss_CI_conversion_applied=False),identities

def scalar_scores(u,w):
    values=[]
    for row in u:
        a=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))
        b=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)));values.append(100*a/(a+b))
    return np.array(values)
def metrics(lo,hi,w):
    l,u=scalar_scores(lo,w),scalar_scores(hi,w);mid=scalar_scores((lo+hi)/2,w)
    r=np.array([max(0,max(u[k] for k in range(16) if k!=i)-l[i]) for i in range(16)])
    return dict(score_lower=l,score_upper=u,max_regret=r,possible_champion=np.array([u[i]>=max(l[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]),necessary_champion=np.array([l[i]>=max(u[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]),decision_rank=np.array([1+sum(r[k]<r[i]-1e-12 for k in range(16)) for i in range(16)]),best_rank=np.array([1+sum(l[k]>u[i]+1e-12 for k in range(16) if k!=i) for i in range(16)]),worst_rank=np.array([1+sum(u[k]>l[i]+1e-12 for k in range(16) if k!=i) for i in range(16)]),midpoint_illustrative_score=mid,midpoint_illustrative_rank=np.array([1+sum(mid[k]>mid[i]+1e-12 for k in range(16)) for i in range(16)]))
def protect():
    p=read(O/'protected_files.json')
    for group,root in [('science',ROOT),('paper',P),('registries',ROOT/'design')]:
        for n,h in p[group].items():assert sha(root/n)==h,n
    f,l,h=revised_bounds();assert f.city.tolist()==p['cities'];np.testing.assert_array_equal(l,p['lower']);np.testing.assert_array_equal(h,p['upper'])
    return p,f,l,h

def main():
    protected,f,lo,hi=protect();sources,bindings=raw_sources();cities=f.city.tolist();z=cities.index('Zurich');d=cities.index('Dublin');j=NAMES.index('travel')
    summary=read(O/'summary.json')
    assert summary['primary']=='V181 unchanged' and summary['paper']=='V184 unchanged'
    assert summary['primary_admissions']==0 and summary['actual_baseline_width_change']==0
    assert summary['published_mean27_1_not_used_as_moment_constraint'] and summary['original28_8_not_intersected'] and summary['profiles_are_not_nested']
    for n,h in summary['source_sha256'].items():assert sha(ROOT/n)==h,n
    lower,upper=sources['Dublin_utility_lower'],sources['Dublin_utility_upper'];close(summary['candidate_utility_bounds'],[lower,upper],3e-15)
    assert lower<lo[d,j]<upper<hi[d,j] and summary['candidate_total']==215384 and summary['candidate_unknown']==16281 and summary['candidate_known']==199103
    bins=pd.read_csv(O/'candidate_bins.csv',float_precision='round_trip');assert len(bins)==7
    assert bins['count'].tolist()==[34770,75667,57683,17420,11337,2226,16281]
    close(bins.utility_lower,[math.exp(-t/30) for t in [15,30,45,60,90]]+[0,0],3e-15)
    close(bins.utility_upper,[math.exp(-t/30) for t in [0,15,30,45,60,90]]+[1],3e-15)
    assert bins.minutes_lower.tolist()==['0','15','30','45','60','90','unknown']
    assert bins.minutes_upper.tolist()==['15','30','45','60','90','unbounded','unknown']
    refs={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.full(10,.1)}
    names=['retained_input','Dublin2011_resident_bins','Dublin2011_resident_bins_withdraw_Zurich_mean','Dublin2011_resident_bins_withdraw_other11_means']
    profiles={}
    for name in names:
        a,b=lo.copy(),hi.copy()
        if name!='retained_input':a[d,j],b[d,j]=lower,upper
        if name=='Dublin2011_resident_bins_withdraw_Zurich_mean':a[z,j],b[z,j]=0,1
        if name=='Dublin2011_resident_bins_withdraw_other11_means':
            means=np.flatnonzero(f.commute_min.notna().to_numpy());assert len(means)==12 and d in means
            for i in means:
                if i!=d:a[i,j],b[i,j]=0,1
        k=cities.index('Singapore');np.testing.assert_array_equal([a[k,j],b[k,j]],[lo[k,j],hi[k,j]])
        profiles[name]=(a,b)
    bounds=pd.read_csv(O/'profile_bounds.csv',float_precision='round_trip');ranks=pd.read_csv(O/'profile_ranks.csv',float_precision='round_trip')
    assert len(bounds)==640 and len(ranks)==128 and not bounds[['profile','city','indicator']].duplicated().any() and not ranks[['profile','weight_reference','city']].duplicated().any()
    assert set(bounds.profile)==set(names) and set(ranks.profile)==set(names)
    keys=pd.MultiIndex.from_product([cities,NAMES],names=['city','indicator']);row_checks=0
    for name,(a,b) in profiles.items():
        saved=bounds[bounds.profile==name].set_index(['city','indicator']).loc[keys]
        np.testing.assert_array_equal(saved.lower.to_numpy().reshape(16,10),a);np.testing.assert_array_equal(saved.upper.to_numpy().reshape(16,10),b)
        for ref,w in refs.items():
            expected=metrics(a,b,w);saved=ranks[(ranks.profile==name)&(ranks.weight_reference==ref)].set_index('city').loc[cities];assert len(saved)==16
            for column,value in expected.items():
                if value.dtype==bool:assert saved[column].tolist()==value.tolist(),column
                else:close(saved[column].to_numpy(),value)
            rep=next(v for v in summary['profiles'] if v['profile']==name and v['weight_reference']==ref)
            assert rep['conservative_recommendation']==[cities[k] for k in range(16) if expected['decision_rank'][k]==1]
            assert rep['possible_champions']==sum(expected['possible_champion'])==16 and rep['necessary_champions']==sum(expected['necessary_champion'])==0
            close(rep['mean_score_interval_width'],(expected['score_upper']-expected['score_lower']).mean());row_checks+=16
    thresholds=read(O/'mean_thresholds.json');assert thresholds==summary['thresholds'] and len(thresholds)==2
    probes=pd.read_csv(O/'threshold_probes.csv',float_precision='round_trip');assert len(probes)==202
    threshold_checks=[]
    for ref,w in refs.items():
        record=next(v for v in thresholds if v['weight_reference']==ref)
        def gap(u):
            a=lo.copy();a[z,j]=u;r=metrics(a,hi,w)['max_regret'];return r[z]-np.delete(r,z).min()
        initial=metrics(lo,hi,w);target=max(np.delete(initial['score_upper'],z))-np.delete(initial['max_regret'],z).min()
        close(record['target_lower_score'],target);close(record['gap_at_lower_utility0'],gap(0));close(record['gap_at_lower_utility1'],gap(1))
        ratio=(target/(100-target))**2;coef=np.asarray(record['quadratic_coefficients'])
        # Validate the declared polynomial directly against independently squared norms.
        for u in [.17,.53,.91]:
            a=lo[z].copy();a[j]=u
            positive=math.fsum(float(ww)*float(x)**2 for ww,x in zip(w,a));negative=math.fsum(float(ww)*(1-float(x))**2 for ww,x in zip(w,a))
            close(np.polyval(coef,u),positive-ratio*negative,4e-15)
        local=probes[probes.weight_reference==ref];assert len(local)==101
        close(local.lower_utility,np.linspace(0,1,101),1e-15)
        previous=float('inf')
        for row in local.itertuples():
            expected=gap(row.lower_utility);close(row.Zurich_regret_minus_best_other,expected);assert expected<=previous+1e-12;previous=expected
            if row.lower_utility==0:assert row.implied_mean_minutes=='limit_infinity'
            else:close(float(row.implied_mean_minutes),-30*math.log(row.lower_utility),1e-12)
            a=lo.copy();a[z,j]=row.lower_utility;rr=metrics(a,hi,w)['max_regret'];close(np.delete(rr,z),np.delete(initial['max_regret'],z))
        if gap(0)>0:
            root=float(brentq(gap,0,1,xtol=1e-14));minutes=-30*math.log(root)
            assert record['status']=='one_finite_mean_tie';close(record['tie_lower_utility'],root,2e-14);close(record['tie_mean_minutes'],minutes,3e-12)
            tied=lo.copy();tied[z,j]=root;tm=metrics(tied,hi,w);assert tm['decision_rank'][z]==1
            for shift,sign in [(-1e-4,-1),(1e-4,1)]:assert sign*gap(math.exp(-(minutes+shift)/30))>0
            threshold_checks.append(dict(weight_reference=ref,status='finite_tie',tie_lower_utility=root,tie_mean_minutes=minutes,both_sides_verified=True))
        else:
            # Focal regret decreases with utility; all other regrets are constant.
            # Thus negative gap at0 proves no crossing anywhere in[0,1].
            assert gap(0)<0 and gap(1)<0 and record['status']=='Zurich_unique_for_all_nonnegative_means'
            assert record['tie_lower_utility'] is None and record['tie_mean_minutes'] is None
            threshold_checks.append(dict(weight_reference=ref,status='no_crossing_nonnegative_means',maximum_gap=gap(0),endpoint_monotonicity_and_constant_other_regrets=True))
    protect()
    outputs=['summary.json','candidate_bins.csv','profile_ranks.csv','profile_bounds.csv','threshold_probes.csv','mean_thresholds.json']
    bindings.update(summary['source_sha256']);bindings[str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__))
    report=dict(version='V185 independent candidate audit',status='pass',primary='V181 unchanged',paper='V184 unchanged',primary_admissions=0,actual_baseline_width_change=0,source_checks=sources,independent_profile_rank_rows=row_checks,independent_profile_bound_rows=640,independent_threshold_probes=202,threshold_checks=threshold_checks,not_stated_mass_retained=True,unbounded_tail_without_cap=True,original_mean27_1_not_added_as_constraint=True,non_nested_profile_not_intersected_with_original28_8=True,Swiss_mean_and_unresolved_CI_not_used_in_profiles=True,Singapore_stage_distribution_unchanged_in_all_profiles=True,scientific_bindings_unchanged=len(protected['science']),existing_paper_files_unchanged=len(protected['paper']),three_registries_unchanged=True,all160active_bounds_unchanged=True,MC_rerun=False,source_sha256=bindings,audited_output_sha256={str((O/n).relative_to(ROOT)):sha(O/n) for n in outputs},verifier_sha256=sha(Path(__file__)))
    (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (O/'source_checks.json').write_text(json.dumps(dict(version='V185 independent source audit',status='pass',source_checks=sources,verifier_sha256=sha(Path(__file__)),scope='Rawresponseidentities andindependentdimensiondecode; fullcandidatechecksareinverification.json'),indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['source_sha256','audited_output_sha256']},indent=2))
if __name__=='__main__':main()
