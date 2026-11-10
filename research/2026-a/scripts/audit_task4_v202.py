"""Independent staged V202 research audit; never activates registries or edits paper."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,math,html,re
from html.parser import HTMLParser
from urllib.parse import urlparse
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,NAMES,SPEC
from task4_user_v200_revision import revised_bounds as prior_bounds
from task4_user_v202_revision import revised_bounds,MANIFEST
from audit_task4_v180_amsterdam import independent_scores

O=ROOT/'results/task4_v202_transition'
P=ROOT.parents[2]/'HiMCM-Overleaf'
REFS={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.ones(10)/10}

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csv(p):return pd.read_csv(p,float_precision='round_trip')
def close(a,b,tol=1e-11):np.testing.assert_allclose(a,b,atol=tol,rtol=0)

def check_rows(cities,l,h,w,rows,allow_near_tie_ranks=False):
    saved=rows.set_index('city').loc[cities]
    independent=independent_scores(l,h,w)
    regrets=np.array([v['max_regret'] for v in independent])
    for i,r in enumerate(independent):
        for key,value in r.items():
            if key not in saved:continue
            if allow_near_tie_ranks and key=='decision_rank':
                low=1+sum(regrets<regrets[i]-1e-12);high=sum(regrets<=regrets[i]+1e-12)
                assert low<=saved.iloc[i][key]<=high
            else:close(saved.iloc[i][key],value)
    return len(saved)

def norms(u,w):
    # Independent explicit criterion reduction rather than production matrix product.
    z=np.asarray(u);ww=np.asarray(w)
    if z.ndim==2 and ww.ndim==2:z=z[None,:,:];ww=ww[:,None,:]
    positive=np.sqrt(np.sum(ww*z*z,axis=-1));negative=np.sqrt(np.sum(ww*(1-z)*(1-z),axis=-1))
    return 100*positive/(positive+negative)

def decisions(lower,upper,tol=1e-12,average=True):
    lower=np.atleast_2d(lower);upper=np.atleast_2d(upper)
    regrets=[];possible=[];necessary=[]
    for i in range(16):
        other=[j for j in range(16) if j!=i]
        regrets.append(np.maximum(0,upper[:,other].max(1)-lower[:,i]))
        possible.append(upper[:,i]>=lower[:,other].max(1)-tol)
        necessary.append(lower[:,i]>=upper[:,other].max(1)-tol)
    regret=np.stack(regrets,axis=1);possible=np.stack(possible,axis=1);necessary=np.stack(necessary,axis=1)
    rank=[];first=[];top3=[]
    for i in range(16):
        ahead=(regret<regret[:,i,None]-tol).sum(1)
        tied=(np.abs(regret-regret[:,i,None])<=tol).sum(1)
        rank.append(1+ahead+(tied-1)/2 if average else 1+ahead)
        first.append(np.clip((1-ahead)/tied,0,1));top3.append(np.clip((3-ahead)/tied,0,1))
    return dict(minimax_recommendation_frequency=np.array(first).mean(1),mean_decision_rank=np.array(rank).mean(1),top3_decision_frequency=np.array(top3).mean(1),possible_champion_frequency=possible.mean(0),necessary_champion_frequency=necessary.mean(0))

def check_mc(rows,expected,cities):
    saved=rows.set_index('city').loc[cities];assert len(saved)==16
    for key,values in expected.items():
        key='recommendation_frequency' if key=='minimax_recommendation_frequency' and key not in saved else key
        if key in saved:close(saved[key],values,1e-12)
    return len(saved)

def raw_map(l,h,factors,means):
    # Invert ordinary utility to raw values, scale raw values, then map back.
    factors=np.asarray(factors);a=np.broadcast_to(l,factors.shape).copy();b=np.broadcast_to(h,factors.shape).copy()
    for j,(name,benefit,anchor,_) in enumerate(SPEC):
        r=factors[...,j]
        for original,out in [(l,a),(h,b)]:
            if name=='travel':continue
            u=original[:,j];inner=(u>0)&(u<1)
            raw=anchor*u[inner]/(1-u[inner]) if benefit else anchor*(1/u[inner]-1)
            scaled=r[...,inner]*raw
            out[...,inner,j]=scaled/(anchor+scaled) if benefit else anchor/(anchor+scaled)
        if name=='travel':
            a[...,j]=np.where(r<1,l[:,j],l[:,j]**r)
            b[...,j]=np.where(r<1,h[:,j]**r,h[:,j])
            known=np.isfinite(means)
            a[...,known,j]=np.exp(-r[...,known]*means[known]/30)
    return a,b

def factors_for(shape,changes):
    f=np.ones(shape)
    for name,change in changes.items():f[...,NAMES.index(name)]=1+change
    return f

def precision_checks():
    folder=ROOT/'results/task4_v202_mc_precision';summary=read(folder/'summary.json');bands=csv(folder/'mean_bounds.csv')
    m=len(bands);group_count=len(bands[['family','setting']].drop_duplicates())
    assert summary['base_means']==m and summary['settings']==group_count and summary['familywise_alpha']==.05
    epsilon=math.sqrt(math.log(2*m/.05)/(2*10000))
    close(summary['normalized_half_width'],epsilon,1e-16)
    sources={'preferences':('task4_v202_preferences/mc_city_summary.csv',['profile','concentration']),
             'future_shocks':('task4_v202_future/future_mc_city_summary.csv',['scenario','weight_reference','evidence_arm']),
             'weights_only':('task4_v202_future/weight_mc_city_summary.csv',['scenario','weight_reference','evidence_arm','concentration'])}
    for name,digest in summary['input_sha256'].items():assert sha(ROOT/name)==digest,name
    assert m>0 and group_count>0
    expected_lookup={}
    for family,(file,keys) in sources.items():
        for row in csv(ROOT/'results'/file).to_dict('records'):
            setting=json.dumps({key:str(row[key]) for key in keys},sort_keys=True)
            expected_lookup[family,setting,row['city']]=row
    groups={}
    for row in bands.itertuples():
        source=expected_lookup[row.family,row.setting,row.city]
        close(row.estimate,source[row.metric],1e-15)
        a,b=(1,16) if row.metric=='mean_decision_rank' else (0,1)
        assert row.draws==10000 and row.support_lower==a and row.support_upper==b
        close(row.half_width,(b-a)*epsilon,1e-15)
        close(row.lower,max(a,row.estimate-(b-a)*epsilon),1e-15);close(row.upper,min(b,row.estimate+(b-a)*epsilon),1e-15)
        if row.metric=='mean_decision_rank':groups[row.family,row.setting,row.city]=row
    folder=ROOT/'results/task4_v202_mean_rank_comparisons';pairs=csv(folder/'pairs.csv');settings=csv(folder/'settings.csv');report=read(folder/'summary.json')
    from collections import Counter
    family_sizes=Counter((family,key) for family,key,city in groups)
    pair_count=sum(n*(n-1)//2 for n in family_sizes.values())
    assert len(pairs)==pair_count and len(pairs[['family','setting','city_a','city_b']].drop_duplicates())==pair_count
    certified=0
    for row in pairs.itertuples():
        a=groups[row.family,row.setting,row.city_a];b=groups[row.family,row.setting,row.city_b]
        low,high=a.lower-b.upper,a.upper-b.lower
        close(row.sample_mean_a,a.estimate);close(row.sample_mean_b,b.estimate);close(row.gap_a_minus_b,a.estimate-b.estimate)
        close(row.gap_lower,low);close(row.gap_upper,high)
        label='a_lower_expected_mean_rank' if high < -1e-12 else ('b_lower_expected_mean_rank' if low>1e-12 else 'unresolved')
        assert row.classification==label
        certified+=label!='unresolved'
    unique=0
    for setting in settings.itertuples():
        rows=pairs[(pairs.family==setting.family)&(pairs.setting==setting.setting)]
        assert len(rows)==120
        beaten=set(rows.loc[rows.classification=='a_lower_expected_mean_rank','city_b'])|set(rows.loc[rows.classification=='b_lower_expected_mean_rank','city_a'])
        cities={city for family,key,city in groups if family==setting.family and key==setting.setting}
        front=sorted(cities-beaten)
        assert json.loads(setting.unresolved_mean_rank_front)==front
        assert bool(setting.unique_smallest_expectation_certified)==(len(front)==1)
        unique+=len(front)==1
    assert report['certified_pairs']==certified and report['unresolved_pairs']==pair_count-certified
    assert report['settings_with_unique_smallest_expected_mean_rank']==unique
    return dict(base_means=m,settings=group_count,familywise_alpha=.05,derived_pairs=pair_count,certified_pairs=certified,unresolved_pairs=pair_count-certified,unique_minimum_settings=unique)


def source_diagnostic_checks(f,l,h):
    from scipy.optimize import brentq
    folder=ROOT/'results/task4_v202_source_diagnostics';report=read(folder/'summary.json')
    for name,digest in report['source_sha256'].items():assert sha(ROOT/name)==digest,name
    assert 'scripts/task4_user_v202_revision.py' in report['source_sha256'] and 'design/task4_user_v202_admissions.json' in report['source_sha256']
    assert 'V202 staged' in report['science'] and not report['MC_rerun']
    assert 'only' in report['point_possible_champion_scope'] and 'not asserted' in report['point_possible_champion_scope']
    cities=f.city.tolist();j=NAMES.index('travel');z=cities.index('Zurich');means=f.commute_min.to_numpy(float);idx=np.flatnonzero(np.isfinite(means));assert len(idx)==12
    def checked_bounds(saved,a,b):
        saved=saved.set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        close(saved.lower.to_numpy().reshape(16,10),a,1e-15);close(saved.upper.to_numpy().reshape(16,10),b,1e-15)
    checked_bounds(csv(folder/'retained_bounds.csv'),l,h)
    wr=csv(folder/'commute_withdrawal_ranks.csv');wb=csv(folder/'commute_withdrawal_bounds.csv');assert len(wr)==160 and len(wb)==800
    withdrawn={'retained_input':[],'withdraw_Zurich_work_commute':['Zurich'],'withdraw_Dublin_work_commute':['Dublin'],'withdraw_both_work_commute':['Zurich','Dublin'],'withdraw_all_submitted_commute_means':[cities[i] for i in idx]}
    for case,targets in withdrawn.items():
        a,b=l.copy(),h.copy()
        for city in targets:a[cities.index(city),j],b[cities.index(city),j]=0,1
        checked_bounds(wb[wb.scenario==case],a,b)
        for ref,w in REFS.items():check_rows(cities,a,b,w,wr[(wr.scenario==case)&(wr.weight_reference==ref)])
    probes=csv(folder/'single_mean_probes.csv');thresholds=read(folder/'mean_thresholds.json');joint=read(folder/'joint_thresholds.json');pairs=csv(folder/'joint_pairwise_crossings.csv')
    jr=csv(folder/'joint_corner_ranks.csv');jb=csv(folder/'joint_corner_bounds.csv');jm=csv(folder/'joint_corner_means.csv')
    assert len(probes)==202 and len(jr)==192 and len(jb)==1920 and len(jm)==144 and len(pairs)==30
    roots=[];corner_count=0;boundary_rank_rows=[]
    for ref,w in REFS.items():
        def regrets(a):return np.array([x['max_regret'] for x in independent_scores(a,h,w)])
        def sg(u):
            a=l.copy();a[z,j]=u;r=regrets(a);return float(r[z]-np.delete(r,z).min())
        single=next(x for x in thresholds if x['weight_reference']==ref)
        for row in probes[probes.weight_reference==ref].itertuples():close(row.Zurich_regret_minus_best_other,sg(row.lower_utility))
        close(single['gap_at_lower_utility0'],sg(0));close(single['gap_at_lower_utility1'],sg(1))
        if sg(0)>0>sg(1):
            u=float(brentq(sg,0,1,xtol=5e-16,rtol=1e-15));mean=-30*math.log(u)
            close(single['tie_lower_utility'],u,1e-13);close(single['tie_mean_minutes'],mean,1e-10)
            assert sg(math.exp(-(mean-1e-5)/30))<0<sg(math.exp(-(mean+1e-5)/30))
            coefficients=single['quadratic_coefficients'];close(sum(c*u**(2-i) for i,c in enumerate(coefficients)),0,1e-13)
        else:assert single['status']=='Zurich_unique_for_all_nonnegative_means' and sg(0)<0 and sg(1)<0
        def joint_bound(delta):
            a=l.copy();a[idx,j]=np.exp(-means[idx]*(1-delta)/30);a[z,j]=math.exp(-means[z]*(1+delta)/30);return a
        def gap(delta):
            r=regrets(joint_bound(delta));return float(r[z]-np.delete(r,z).min())
        root=float(brentq(gap,0,1,xtol=5e-16,rtol=1e-15));item=next(x for x in joint if x['weight_reference']==ref)
        close(item['sharp_radius'],root,1e-13);assert gap(root-1e-7)<0<gap(root+1e-7)
        r=regrets(joint_bound(root));assert abs(r[z]-np.delete(r,z).min())<1e-12;attaining=[cities[i] for i in range(16) if r[i]<=r.min()+1e-10];assert 'Zurich' in attaining and item['binding_rivals']==[c for c in attaining if c!='Zurich']
        for row in pairs[pairs.weight_reference==ref].itertuples():
            other=cities.index(row.rival)
            def pair(d):
                values=regrets(joint_bound(d));return float(values[z]-values[other])
            close(row.gap_at0,pair(0));close(row.gap_at1,pair(1))
            if pair(1)<0:assert pd.isna(row.crossing_radius)
            else:close(row.crossing_radius,brentq(pair,0,1,xtol=5e-16,rtol=1e-15),1e-13)
        for case,rows in jr[jr.weight_reference==ref].groupby('case'):
            delta=float(rows.delta.iloc[0]);assert rows.delta.nunique()==1;a=joint_bound(delta)
            check_rows(cities,a,h,w,rows,allow_near_tie_ranks=(case=='boundary'));checked_bounds(jb[(jb.weight_reference==ref)&(jb['case']==case)],a,h)
            if case=='boundary':
                rr=regrets(a);saved=rows.set_index('city').loc[cities]
                close(saved.max_regret.to_numpy(),rr,1e-12)
                actual=saved.max_regret.to_numpy()
                for k in range(16):
                    if abs(rr[k]-rr.min())>1e-12:continue
                    low=int(1+sum(rr<rr[k]-1e-12));high=int(sum(rr<=rr[k]+1e-12))
                    boundary_rank_rows.append(dict(weight_reference=ref,case=case,city=cities[k],exported_decision_rank=int(saved.iloc[k].decision_rank),independent_tolerance_rank=low,allowed_machine_tie_rank_range=[low,high],exported_regret_gap_to_Zurich=float(actual[k]-actual[z]),independent_regret_gap_to_Zurich=float(rr[k]-rr[z]),regret_absolute_difference=float(abs(actual[k]-rr[k]))))
            mm=jm[(jm.weight_reference==ref)&(jm['case']==case)].set_index('city')
            assert set(mm.index)=={cities[i] for i in idx}
            for i in idx:
                close(mm.loc[cities[i]].original_mean_minutes,means[i],1e-15)
                close(mm.loc[cities[i]].corner_mean_minutes,means[i]*(1+delta if i==z else 1-delta),1e-12)
        for delta in [.05,root]:
            bits=((np.arange(4096)[:,None]>>np.arange(12))&1);a=np.broadcast_to(l,(4096,16,10)).copy();a[:,idx,j]=np.exp(-means[idx][None,:]*(1+delta*(2*bits-1))/30)
            lows=norms(a,w);upper=norms(h,w);C=np.array([np.delete(upper,i).max() for i in range(16)]);R=np.maximum(0,C[None,:]-lows);gaps=R[:,z]-np.delete(R,z,axis=1).min(axis=1)
            close(gaps.max(),gap(delta),1e-11);corner_count+=4096
        roots.append(dict(weight_reference=ref,joint_sharp_radius=root,single_mean_minutes=single['tie_mean_minutes'],binding_rivals=item['binding_rivals']))
    return dict(withdrawal_ranks=160,withdrawal_bounds=800,single_probes=202,joint_ranks=192,joint_bounds=1920,joint_mean_vectors=144,pairwise_crossings=30,independent_corners=corner_count,roots=roots,boundary_rank_rows=boundary_rank_rows,boundary_rank_scope='Only exact-root exported decision_rank may select either ordering inside an independently verified1e-12 regret tie; scores/regrets/closed-form boundary/tie recommendation checked independently. All nonboundary ranks strict.',sharpness_scope='Declared continuous box via monotone separable self-excluded regrets; strict below, tie attainable at equality, counterexample above; not physical attainability or probability.')


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.ignore=0; self.parts=[]
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript'): self.ignore+=1
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript'): self.ignore-=1
    def handle_data(self, data):
        if not self.ignore and data.strip(): self.parts.append(' '.join(data.split()))

def visible(raw):
    p=Text(); p.feed(raw); return ' '.join(p.parts)

def source_checks(manifest):
    SG=ROOT/'data/task4_v199_sgpool'
    listing=read(SG/'manifest.json')
    for name,digest in listing.items():assert sha(SG/name)==digest,name
    assert len([n for n in listing if n.startswith('active_sg_directory_page_')])==3
    assert len([n for n in listing if n.startswith('details/')])==25
    directory=read(SG/'retrieval.json'); entries=read(SG/'venues.json')['venues']; assert len(entries)==25
    names={r['name'] for r in entries}; zips={r['postal_code'] for r in entries}; slugs={r['provider_id'] for r in entries}
    assert len(names)==len(zips)==len(slugs)==25
    cards=[]
    for page in directory['pages']:
        assert page['status']==200 and urlparse(page['url']).hostname=='www.activesgcircle.gov.sg'
        raw=(SG/page['file']).read_bytes(); assert len(raw)==page['bytes'] and hashlib.sha256(raw).hexdigest()==page['sha256']
        source=raw.decode(); updates=re.findall(r'Last updated:\s*([^<]+)',source,re.I)
        assert updates and set(' '.join(x.split()) for x in updates)=={'8 November 2026'}
        chunks=re.split(r'<div class="cst-list-item">',source)[1:]
        assert len(chunks)==({'active_sg_directory_page_1.html':10,'active_sg_directory_page_2.html':10,'active_sg_directory_page_3.html':5}[page['file']])
        for chunk in chunks:
            link=re.search(r'<a class="view-page-link" href="([^"]+)"',chunk).group(1)
            name=visible(re.search(r'<h2\b[^>]*>.*?</h2>',chunk,re.S).group())
            address=visible(re.search(r'<div class="cst-address"[^>]*>.*?</div>',chunk,re.S).group())
            postcode=re.search(r'\bSingapore\s+(\d{6})\b',address).group(1)
            cards.append((name,address,postcode,html.unescape(link)))
    assert len(cards)==25 and len(set(cards))==25
    assert set(cards)=={(r['name'],r['address'],r['postal_code'],r['provider_url']) for r in entries}
    old=read(ROOT/'data/task4_v117_singapore/summary.json'); old_zips={r['postal_code'] for r in old['venues']}
    assert len(old_zips)==7 and old_zips <= zips and len(zips-old_zips)==18
    assert next(r for r in entries if r['postal_code']=='528523')['provider_id']=='tampines-swimming-complex'
    receipts=read(SG/'detail_retrieval.json')['details']; verification=read(SG/'detail_verification.json')['pages']
    assert len(receipts)==len(verification)==25 and {r['provider_id'] for r in receipts}==slugs
    detail_text={}
    for receipt in receipts:
        assert receipt['status']==200 and receipt['error'] is None
        assert urlparse(receipt['url']).hostname==urlparse(receipt['final_url']).hostname=='www.activesgcircle.gov.sg'
        raw=(SG/receipt['file']).read_bytes();assert len(raw)==receipt['bytes'] and hashlib.sha256(raw).hexdigest()==receipt['sha256']
        entry=next(r for r in entries if r['provider_id']==receipt['provider_id'])
        assert receipt['url']==entry['provider_url']
        text=visible(raw.decode()); detail_text[receipt['provider_id']]=text
        assert entry['name'] in text and entry['address'] in text
        detail=next(r for r in verification if r['provider_id']==receipt['provider_id'])
        assert detail['detail_name']==entry['name'] and detail['detail_address']==entry['address'] and detail['detail_postal_code']==entry['postal_code']
        assert all(detail['identity_check'][k] for k in ['name_matches_catalog','address_matches_catalog','postal_code_matches_catalog'])
        assert 'Weekly Maintenance' in text
    assert len({p['provider_id'] for p in verification}) == 25
    assert all(sum(n['status_class']=='weekly-maintenance' for n in p['closure_notices'])==1 for p in verification)
    notices=[(p['provider_id'],n['date_or_schedule'],n['short_notice']) for p in verification for n in p['closure_notices'] if n['status_class']=='temporary-closure']
    assert set(notices)=={('clementi-swimming-complex','14 Sep - 10 Nov 2026','Training Pool • Clementi Swimming Complex'),('clementi-swimming-complex','11 Nov - 23 Dec 2026','Competition Pool • Clementi Swimming Complex'),('jurong-east-swimming-complex','5 Apr 2025 - 31 Dec 2026','Competition Pool • Jurong East Swimming Complex'),('katong-swimming-complex','9 Oct - 18 Dec 2026','Competition Pool • Katong Swimming Complex')}
    for slug,date,scope in notices:
        text=detail_text[slug]; assert date in text and scope.replace(' • ', ' • ') in text, (slug,date,scope)
    assert 'Partial Facility Access' in detail_text['jurong-east-swimming-complex']
    assert 'Facility is closed today' in detail_text['katong-swimming-complex'] and 'Every Tue' in detail_text['katong-swimming-complex']

    row=manifest['observations'][0]
    assert set(row['venues'])==names and set(row['provider_page_ids'])==slugs
    assert set(row['withheld_notice_venues'])=={slug for slug,_,_ in notices}
    return dict(catalog_pages=3,detail_pages=25,unique_names_postcodes_slugs=25,old_venues=7,notice_venues_withheld=3,temporary_notices=notices,inventory_not_open_count=True)

def source_checks_v202(manifest):
    from audit_sportshub_candidate import page
    D=ROOT/'data/current_sg_sportshub'
    for name in ('venue','swimming'):
        p=D/(name+'.html');m=read(D/(name+'.html.json'))
        assert m['http_status']==200 and m['bytes']==p.stat().st_size and m['sha256']==sha(p)
    assert '404' in read(D/'conditions.pdf.json')['failure']
    v=page(D/'venue.html');s=page(D/'swimming.html')
    assert all(x in v for x in ['7 Stadium Drive','397632','general public','competition and training pools open for public swimming','5 to 28 December 2026','Training Pool availability will be limited'])
    assert all(x in s for x in ['Per entry rates','Child (under 18 years old)','aged 16 years and above','applicable for all ages','15 years and below','closed every Tuesday','30 Oct'])
    old=read(ROOT/'data/task4_v199_sgpool/venues.json')['venues']; prior=read(ROOT/'design/task4_user_v200_admissions.json')['observations'][0];row=manifest['observations'][0]
    assert len(old)==25 and [x['name'] for x in old]==prior['venues']
    for x in old:
        combined=' '.join([x['name'],x['address'],x['postal_code'],x['provider_id']]).lower()
        assert all(a not in combined for a in ['ocbc','aquatic centre','sports hub','kallang','stadium drive','397632'])
    assert row['venues']==prior['venues']+['OCBC Aquatic Centre'] and row['additional_venue']['counting'].startswith('competition pool, training pool')
    assert read(ROOT/'results/current_sportshub_candidate/verification.json')['status']=='pass'
    return dict(successful_operator_pages=2,failed_conditions_pdf_404=True,distinct_old_venues=25,physical_venue_count=1,basins_not_counted_separately=True,age_and_temporal_conditions_checked=True)

def main():
    protected=read(O/'protection_snapshot.json')
    def protection():
        assert not protected['v200_binding_issues_at_capture']
        assert sha(ROOT/'design/task4_user_v200_snapshot.json')==protected['v200_snapshot_sha256']
        for name,digest in protected['v200_bindings'].items():assert sha(ROOT/name)==digest,name
        for name,digest in protected['protected_files'].items():assert sha(Path(name))==digest,name
    protection()
    snapshot_path=ROOT/'design/task4_user_v200_snapshot.json';snapshot=read(snapshot_path)
    assert len(snapshot['source_sha256'])==407
    manifest=read(MANIFEST);assert manifest['version']=='V202 staged'
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    sources=source_checks_v202(manifest)
    assert len(manifest['observations'])==1
    f,l0,h0=prior_bounds();f1,l,h=revised_bounds();pd.testing.assert_frame_equal(f,f1,check_exact=True)
    cities=f.city.tolist();j=NAMES.index('public_pool_density');z=cities.index('Singapore');transport=NAMES.index('public_transport_density')
    assert l.shape==h.shape==(16,10) and np.count_nonzero(l!=l0)==1;np.testing.assert_array_equal(h,h0)
    mask=np.ones((16,10),bool);mask[z,j]=False
    row=manifest['observations'][0];assert row['raw_count']==26 and row['raw_count_before']==25 and row['population']==6036900 and row['population_year']==2024
    for count,arr in [(26,l),(25,l0)]:close(arr[z,j],float(Fraction(count*100000,6036900+count*100000)),2e-16)
    np.testing.assert_array_equal(l[mask],l0[mask]);assert [int((l==h).sum()),int(((l<h)&((l>0)|(h<1))).sum()),int(((l==0)&(h==1)).sum())]==[112,37,11]
    from task4_user_city_indicators import build,SOURCE
    raw_l,raw_h,_=build(pd.read_csv(SOURCE));assert np.count_nonzero((l!=raw_l)|(h!=raw_h))==25
    import itertools
    for flags in itertools.product([False,True],repeat=4):
        old=prior_bounds(*flags);new=revised_bounds(False,*flags)
        pd.testing.assert_frame_equal(old[0],new[0],check_exact=True)
        np.testing.assert_array_equal(old[1],new[1]);np.testing.assert_array_equal(old[2],new[2])
    def count_case(count,**kw):
        _,a,b=revised_bounds(**kw);expected=l.copy();expected[z,j]=float(Fraction(count*100000,6036900+count*100000));close(a,expected,2e-16);np.testing.assert_array_equal(b,h);return a
    no_sg=count_case(25,include_sportshub=False)
    no_dir=count_case(8,include_sg_pool=False)
    no_all=count_case(7,include_sportshub=False,include_sg_pool=False)
    notice23=count_case(23,withhold_existing_notice_venues=True)
    notice22=count_case(22,withhold_notice_venues=True)
    _,no_z,_=revised_bounds(include_zurich_pool=False);_,no_t,_=revised_bounds(include_tokyo=False);_,no_w,_=revised_bounds(include_warsaw=False);_,no_b,bh=revised_bounds(include_tokyo=False,include_warsaw=False)
    np.testing.assert_array_equal(bh,h0)
    expected=l.copy();expected[cities.index('Zurich'),j]=prior_bounds(True,False)[1][cities.index('Zurich'),j];np.testing.assert_array_equal(no_z,expected)
    expected=l.copy();expected[cities.index('Tokyo'),transport]=0;np.testing.assert_array_equal(no_t,expected)
    expected=l.copy();expected[cities.index('Warsaw'),transport]=0;np.testing.assert_array_equal(no_w,expected)
    expected=l.copy();expected[[cities.index('Tokyo'),cities.index('Warsaw')],transport]=0;np.testing.assert_array_equal(no_b,expected)
    stage_l=l.copy();stage_h=h.copy();stage_l[cities.index('Singapore'),NAMES.index('travel')]=0;stage_h[cities.index('Singapore'),NAMES.index('travel')]=1
    amsterdam=l.copy();amsterdam[cities.index('Amsterdam'),transport]=0
    cases={'before_V200':(l0,h0),'after_conditional':(l,h),'withdraw_OCBC_venue':(no_sg,h),'withdraw_Singapore_directory_refinement':(no_dir,h),'withdraw_all_Singapore_pool_supplements':(no_all,h),'withhold_existing_three_notice_venues':(notice23,h),'withhold_all_four_notice_venues':(notice22,h),'withdraw_Zurich_pool_refinement':(no_z,h),'withdraw_Tokyo_inventory':(no_t,h),'withdraw_Warsaw_inventory':(no_w,h),'withdraw_both_inventory':(no_b,h),'withdraw_historical_stage_proxy':(stage_l,stage_h),'withdraw_Amsterdam_mapped_inventory':(amsterdam,h)}
    primary=ROOT/'results/task4_user_v202_revision';ranks=csv(primary/'all_ranks.csv');mc=csv(primary/'mc_city_summary.csv');bounds=csv(primary/'utility_bounds.csv');city_cases=0;mc_rows=0
    assert set(ranks.scenario)==set(cases) and len(ranks)==416 and len(bounds)==2080 and len(mc)==1248
    for case,(a,b) in cases.items():
        saved=bounds[bounds.scenario==case].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        close(saved.lower.to_numpy().reshape(16,10),a,1e-15);close(saved.upper.to_numpy().reshape(16,10),b,1e-15)
        for ref,w in REFS.items():city_cases+=check_rows(cities,a,b,w,ranks[(ranks.scenario==case)&(ranks.weight_reference==ref)])
    for ref,w in REFS.items():
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*w,10000)
            for case,(a,b) in cases.items():
                expected=decisions(norms(a,draws),norms(b,draws))
                mc_rows+=check_mc(mc[(mc.scenario==case)&(mc.weight_reference==ref)&(mc.concentration==concentration)],expected,cities)
    primary_summary=read(primary/'summary.json')
    assert primary_summary['admissions_sha256']==sha(MANIFEST) and primary_summary['point_cells']==112 and primary_summary['partial_cells']==37 and primary_summary['fully_missing_cells']==11
    assert primary_summary['mc_seed']==20261108 and primary_summary['mc_draws_per_setting']==10000 and primary_summary['primary_mc_settings']==78
    for report in primary_summary['results']:
        rows=ranks[(ranks.scenario==report['scenario'])&(ranks.weight_reference==report['weight_reference'])]
        close(report['mean_width'],float((rows.score_upper-rows.score_lower).mean()))
        assert report['minimax_choices']==rows.loc[rows.decision_rank==1,'city'].tolist()
        assert report['possible_champions']==rows.loc[rows.possible_champion,'city'].tolist()
        assert report['necessary_champions']==rows.loc[rows.necessary_champion,'city'].tolist()
    before=mc[mc.scenario=='before_V200'].drop(columns='scenario').reset_index(drop=True)
    old=csv(ROOT/'results/task4_user_v200_revision/mc_city_summary.csv');old=old[old.scenario=='after_conditional'].drop(columns='scenario').reset_index(drop=True)
    pd.testing.assert_frame_equal(before,old,check_exact=True)
    extension_structure_tables=0
    for part in ['preferences','future','method','diagnostics']:
        old_folder=ROOT/('results/task4_v200_'+part);new_folder=ROOT/('results/task4_v202_'+part)
        assert {p.name for p in old_folder.glob('*.csv')}=={p.name for p in new_folder.glob('*.csv')}
        for path in new_folder.glob('*.csv'):
            old_table=csv(old_folder/path.name);new_table=csv(path)
            assert list(old_table.columns)==list(new_table.columns) and old_table.shape==new_table.shape
            for column in ['city','indicator','profile','scenario','weight_reference','evidence_arm','concentration','target']:
                if column in old_table:
                    pd.testing.assert_series_equal(old_table[column],new_table[column],check_exact=True)
            extension_structure_tables+=1
    p=ROOT/'results/task4_v202_preferences';pw=csv(p/'weights.csv');pr=csv(p/'ranks.csv');pm=csv(p/'mc_city_summary.csv')
    pd.testing.assert_frame_equal(pw,csv(ROOT/'results/task4_v200_preferences/weights.csv'),check_exact=True)
    diagnostic_changes=[]
    def compare_matrices(a,b,path=()):
        if isinstance(a,dict):
            assert isinstance(b,dict) and a.keys()==b.keys()
            for key in a:compare_matrices(a[key],b[key],path+(key,))
        elif isinstance(a,list):
            assert isinstance(b,list) and len(a)==len(b)
            for i,(x,y) in enumerate(zip(a,b)):compare_matrices(x,y,path+(i,))
        elif path[:2]==('independent_living_priority','diagnostic') and len(path)==3 and path[2] in {'lambda_max','CI','CR'}:
            assert isinstance(a,(int,float)) and isinstance(b,(int,float))
            close(a,b,1e-12);diagnostic_changes.append(abs(a-b))
        else:assert type(a)==type(b) and a==b,path
    compare_matrices(read(p/'scenario_matrices.json'),read(ROOT/'results/task4_v200_preferences/scenario_matrices.json'))
    assert len(diagnostic_changes)==3
    pref_mc_rows=0
    for profile in pr.profile.unique():
        w=pw[pw.profile==profile].set_index('indicator').loc[NAMES].weight.to_numpy()
        city_cases+=check_rows(cities,l,h,w,pr[pr.profile==profile])
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*w,10000)
            pref_mc_rows+=check_mc(pm[(pm.profile==profile)&(pm.concentration==concentration)],decisions(norms(l,draws),norms(h,draws)),cities)
    from task4_v122_future import SCENARIOS,DRAWS,SEED,WEIGHT_SEED
    future=ROOT/'results/task4_v202_future';fr=csv(future/'ranks.csv');fb=csv(future/'utility_bounds.csv');fm=csv(future/'future_mc_city_summary.csv');wm=csv(future/'weight_mc_city_summary.csv')
    assert DRAWS==10000 and SEED==20261108122 and WEIGHT_SEED==[20261108,100]
    assert read(future/'summary.json')['scenario_definitions']==SCENARIOS
    means=f.commute_min.to_numpy(dtype=float);arms={'conditional':(l,h),'withdraw_historical_stage_proxy':(stage_l,stage_h)}
    future_mc_rows=0;future_weight_rows=0
    rng=np.random.default_rng(SEED);delta=.05*rng.uniform(0,1,(DRAWS,1))+.05*rng.uniform(0,1,(DRAWS,16))
    for arm,(base_l,base_h) in arms.items():
        for scenario,changes in SCENARIOS.items():
            factors=factors_for(l.shape,changes);a,b=raw_map(base_l,base_h,factors,means)
            saved=fb[(fb.evidence_arm==arm)&(fb.scenario==scenario)].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
            close(saved.lower.to_numpy().reshape(16,10),a,3e-14);close(saved.upper.to_numpy().reshape(16,10),b,3e-14)
            for ref,w in REFS.items():
                city_cases+=check_rows(cities,a,b,w,fr[(fr.evidence_arm==arm)&(fr.scenario==scenario)&(fr.weight_reference==ref)])
                draws=np.random.default_rng(np.random.SeedSequence(WEIGHT_SEED)).dirichlet(100*w,DRAWS)
                future_weight_rows+=check_mc(wm[(wm.evidence_arm==arm)&(wm.scenario==scenario)&(wm.weight_reference==ref)],decisions(norms(a,draws),norms(b,draws),tol=1e-10,average=False),cities)
                if scenario=='baseline':continue
                factors=np.ones((DRAWS,16,10))
                for name,change in changes.items():factors[...,NAMES.index(name)]=1+np.sign(change)*delta
                aa,bb=raw_map(base_l,base_h,factors,means);low,high=norms(aa,w),norms(bb,w)
                rows=fm[(fm.evidence_arm==arm)&(fm.scenario==scenario)&(fm.weight_reference==ref)]
                future_mc_rows+=check_mc(rows,decisions(low,high,tol=1e-10,average=False),cities)
                saved=rows.set_index('city').loc[cities]
                for endpoint,values,baseline in [('lower',low,norms(base_l,w)),('upper',high,norms(base_h,w))]:
                    for suffix,q in [('05',.05),('50',.5),('95',.95)]:close(saved[f'score_{endpoint}_change_p{suffix}'],np.quantile(values-baseline,q,axis=0),1e-11)
    # Independently invert and evaluate every declared conditional threshold grid point.
    scans=csv(future/'threshold_scan.csv');thresholds=csv(future/'thresholds.csv');assert len(scans)==3232 and len(thresholds)==32
    for row in scans.itertuples():
        factors=np.ones((16,10));target=cities.index(row.city)
        factors[target,[NAMES.index(name) for name in ['upper_secondary_ptr','pm25','travel']]]=row.raw_multiplier
        aa,bb=raw_map(l,h,factors,means);values=independent_scores(aa,bb,REFS[row.weight_reference])
        regret=np.array([v['max_regret'] for v in values]);close(row.regret_gap_to_best_other,regret[target]-np.delete(regret,target).min())
    for row in thresholds.itertuples():
        if row.status!='crossing_found':continue
        bracket=json.loads(row.threshold_bracket);assert bracket[0]-2e-15<=row.threshold_raw_multiplier<=bracket[1]+2e-15
        for delta,sign in [(-1e-6,-1),(1e-6,1)]:
            factors=np.ones((16,10));target=cities.index(row.city)
            factors[target,[NAMES.index(name) for name in ['upper_secondary_ptr','pm25','travel']]]=row.threshold_raw_multiplier+delta
            aa,bb=raw_map(l,h,factors,means);values=independent_scores(aa,bb,REFS[row.weight_reference])
            regret=np.array([v['max_regret'] for v in values]);assert sign*(regret[target]-np.delete(regret,target).min())>1e-10
    from task4_v137_method_country import independent_method_check,CASE_FILES
    method=ROOT/'results/task4_v202_method';mr=csv(method/'method_ranks.csv');ms=read(method/'summary.json')
    for ref,w in REFS.items():independent_method_check(mr[mr.weight_reference==ref].set_index('city').loc[cities].reset_index(),next(v for v in ms['method_cases'] if v['weight_reference']==ref),l,h,w)
    for name in CASE_FILES:assert sha(method/name)==sha(ROOT/'results/task4_v200_method'/name)
    dg=ROOT/'results/task4_v202_diagnostics';dr=csv(dg/'vintage_ranks.csv');du=csv(dg/'witness_utilities.csv');dc=csv(dg/'witness_cases.csv');points=csv(ROOT/'results/task4_v143_vintage/submitted_points.csv')
    for (scenario,ref),rows in dr.groupby(['scenario','weight_reference']):
        a,b=l.copy(),h.copy()
        for point in points.itertuples():
            early,late,flag=point.submitted_year<2020,point.submitted_year>2025,point.submitted_flag!='ok'
            remove={'baseline':False,'pre2020_points':early,'after2025_points':late,'non_ok_points':flag,'union_points':early or late or flag,'withdraw_Zurich_homicide':point.city=='Zurich' and point.indicator==NAMES[0],'withdraw_Amsterdam_homicide':point.city=='Amsterdam' and point.indicator==NAMES[0]}[scenario]
            if remove:a[cities.index(point.city),NAMES.index(point.indicator)],b[cities.index(point.city),NAMES.index(point.indicator)]=0,1
        city_cases+=check_rows(cities,a,b,REFS[ref],rows)
    for target in cities:
        u=du[du.target==target].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])].utility.to_numpy().reshape(16,10)
        close(u[l==h],l[l==h]);assert np.all(u[l<h]>l[l<h]) and np.all(u[l<h]<h[l<h])
        for ref,w in REFS.items():
            scores=norms(u,w);k=cities.index(target);margin=scores[k]-np.delete(scores,k).max();assert margin>0
            close(dc[(dc.target==target)&(dc.weight_reference==ref)].iloc[0].strict_margin,margin)
    source_diagnostics=source_diagnostic_checks(f,l,h)
    protection();precision=precision_checks()
    paths=[MANIFEST,Path(__file__),snapshot_path]+[ROOT/('scripts/'+name) for name in ['task4_user_v202_revision.py','task4_v202_extensions.py','task4_v202_mc_precision.py','task4_v202_mean_rank_comparisons.py','task4_v202_source_diagnostics.py','audit_task4_v192.py','audit_task4_v180_amsterdam.py']]
    folders=[primary,ROOT/'results/task4_v202_preferences',future,method,dg,ROOT/'results/task4_v202_mc_precision',ROOT/'results/task4_v202_mean_rank_comparisons',ROOT/'results/task4_v202_source_diagnostics']
    result=dict(version='V202 staged research',status='pass',activation_status='staged_not_active',current_primary='V200',changed_lower_cells=1,other159_cells_and_all160_uppers_exact=True,withdrawals_exact=True,point_partial_unknown=[112,37,11],cumulative_supplements=25,extension_structure_tables=extension_structure_tables,independent_scalar_city_cases=city_cases,independent_primary_MC_rows=mc_rows,primary_MC_settings_replayed=78,independent_preference_MC_rows=pref_mc_rows,independent_future_shock_MC_rows=future_mc_rows,independent_future_weight_MC_rows=future_weight_rows,draws_per_setting=10000,paired_seeds_profiles_and_scenarios_preserved=True,preference_matrix_exact_except_independent_living_diagnostic_eigenvalue_roundoff=True,preference_diagnostic_max_absolute_difference=max(diagnostic_changes),independent_future_threshold_scan_points=len(scans),threshold_crossing_sides_verified=True,historical_csvs_byte_identical=len(CASE_FILES),interior_witness_weight_cases=32,scientific_files_unchanged=len(protected['v200_bindings']),protected_files_unchanged=len(protected['protected_files']),prior_v200_snapshot_bindings=len(snapshot['source_sha256']),manuscript_changed=False,independent_raw_future_transform=True,future_shock_quantiles_verified=True,precision_and_mean_rank_audit=precision,source_diagnostics=source_diagnostics,source_counts=sources,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in paths},result_sha256={str(p.relative_to(ROOT)):sha(p) for folder in folders for p in sorted(folder.iterdir()) if p.is_file()})
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','result_sha256','source_counts']},indent=2))
if __name__=='__main__':main()
