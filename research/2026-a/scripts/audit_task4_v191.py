"""Independent source and scalar-model audit of V191 transit candidates; no admission."""
from pathlib import Path
from html.parser import HTMLParser
import csv,hashlib,json,math,re,subprocess
import numpy as np
import pandas as pd
from task4_user_v181_revision import revised_bounds
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v191_candidates'
NAMES=['homicide_rate','pm25','cost_living_index','price_income_ratio','upper_secondary_ptr','research_he_density','public_transport_density','travel','fixed_broadband_mbps','public_pool_density']
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,tol=3e-11):assert abs(float(a)-float(b))<tol,(a,b)
def text_pdf(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True).split('\f')
def receipts(folder):
    values=read(folder/'retrievals.json');good=0;excluded=0
    for item in values:
        name=item.get('file')
        stamp=item.get('requested_at_utc',item.get('accessed_utc'))
        assert stamp and re.match(r'^2026-11-09T',stamp),stamp
        assert item['url'].startswith('https://')
        if name:
            p=folder/name;assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],name
            assert item['http_status']==200;good+=1
            if item.get('payload_classification'):
                assert 'Incapsula' in p.read_text() and p.stat().st_size==212;excluded+=1
        else:assert item['http_status']==403 and item.get('error');excluded+=1
    return values,good,excluded
class Stations(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.capture=False;self.buffer=[];self.names=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a' and 'elementor-accordion-title' in dict(attrs).get('class','').split():self.capture=True;self.buffer=[]
    def handle_data(self,value):
        if self.capture:self.buffer.append(value)
    def handle_endtag(self,tag):
        if tag=='a' and self.capture:
            self.capture=False;name=''.join(self.buffer).strip();m=re.fullmatch(r'Stacja\s+"([^"]+)"',name);assert m,name;self.names.append(m[1])
def sources():
    tok=R/'data/task4_v191_tokyo';war=R/'data/task4_v191_warsaw'
    tr,tgood,texcluded=receipts(tok);wr,wgood,wexcluded=receipts(war)
    a=pd.read_csv(tok/'stationlist_original.csv',encoding='cp932',keep_default_na=False,dtype=str)
    assert len(a)==38 and a['駅名'].nunique()==a['住所'].nunique()==38
    assert len(a[['緯度','経度']].drop_duplicates())==38 and a['座標系'].eq('JGD2011').all()
    assert a['駅名'].eq('都庁前').sum()==1 and a['自'].eq('●').all()
    wards={'千代田区','中央区','港区','新宿区','文京区','台東区','墨田区','江東区','品川区','目黒区','大田区','世田谷区','渋谷区','中野区','杉並区','豊島区','北区','荒川区','板橋区','練馬区','足立区','葛飾区','江戸川区'}
    observed=[]
    for address in a['住所']:
        matches=[ward for ward in wards if address.startswith(ward)];assert len(matches)==1,address;observed.extend(matches)
    assert len(set(observed))==10
    assert a['緯度'].astype(float).between(35,36).all() and a['経度'].astype(float).between(139,140).all()
    selected=pd.read_csv(tok/'named_stations.csv',keep_default_na=False,dtype=str)
    assert selected.station_name.tolist()==a['駅名'].tolist() and selected.address.tolist()==a['住所'].tolist()
    assert selected.ward.tolist()==observed
    for x,y in [('latitude','緯度'),('longitude','経度')]:np.testing.assert_array_equal(selected[x].astype(float),a[y].astype(float))
    cat=(tok/'api_catalog_original.html').read_text()
    for s in ['東京都交通局','subway_branch_o_stationlist.csv','2026/09/01 11:44:00','2026/09/04 15:00:00','自動定期券発売機','定期券発売所']:assert s in cat,s
    tobs=read(tok/'observations.json')[0];assert tobs['raw_count']==38 and tobs['inventory_reference_year'] is None and tobs['no_current_opening_status_claim']
    assert tobs['catalogue_created']=='2026/09/01 11:44:00' and tobs['catalogue_last_updated']=='2026/09/04 15:00:00'
    tf=read(tok/'findings.json');assert tf['primary_admissions']==0 and tf['catalogue_date_not_observation_date']
    line_names=[]
    for line,n in [('m1',21),('m2',18)]:
        parser=Stations();parser.feed((war/(line+'_original.html')).read_text());assert len(parser.names)==len(set(parser.names))==n,(line,parser.names)
        line_names.append(set(parser.names))
    assert line_names[0]&line_names[1]=={'Świętokrzyska'} and len(set.union(*line_names))==38
    pages=text_pdf(war/'fire_service_2025_original.pdf');assert 'za rok 2025' in pages[0] and 'luty 2026' in pages[0]
    scope=' '.join(pages[3].split());assert 'Na terenie m. st. Warszawy' in scope
    assert '21 stacji metra I linii (M1) oraz 18 stacji metra II linii (M2)' in scope
    assert 'W planach' in scope and 'M3, M4 oraz M5' in scope
    plan=' '.join(' '.join(text_pdf(war/'network_plan_original.pdf')).split())
    for name in ['Młociny','Kabaty','Bemowo','Bródno','21 stacji','18 stacji']:assert name in plan,name
    wobs=read(war/'observations.json')[0];assert wobs['raw_count']==38
    for obs,city,pop,year in [(tobs,'Tokyo',9983365,2026),(wobs,'Warsaw',1863800,2024)]:
        assert obs['city']==city and obs['indicator']=='public_transport_density' and obs['population']==pop and obs['population_year']==year
        close(obs['utility_lower'],3800000/(50*pop+3800000),1e-15);assert obs['utility_upper']==1
    return dict(Tokyo_count=38,Tokyo_wards=sorted(set(observed)),Tokyo_inventory_observation_year=None,Tokyo_catalogue_dates_not_observation_dates=True,Tokyo_source_responses=tgood,Tokyo_excluded_access_shells_or_errors=texcluded,Warsaw_M1=21,Warsaw_M2=18,Warsaw_common_station='Świętokrzyska',Warsaw_complexes=38,Warsaw_scope_pdf_page=4,Warsaw_scope_report_year=2025,Warsaw_source_responses=wgood,Warsaw_excluded_requests=wexcluded),{'Tokyo':tobs,'Warsaw':wobs}
def scalar(row,w):
    a=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))
    b=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))
    return 100*a/(a+b)
def protection():
    saved=read(O/'protected_files.json')
    for name,h in saved['paper'].items():assert sha(P/name)==h,name
    for name,h in saved['science'].items():assert sha(R/name)==h,name
    for name,h in saved['registries'].items():assert sha(R/'design'/name)==h,name
    assert read(R/'design/task4_user_current_model.json')['version']=='V181'
    assert read(R/'design/task4_user_current_review.json')['version']=='V189'
    assert sha(R/'data/task4_v117_team_intake/city_indicators.csv')=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    return saved
def model_checks(obs):
    summary=read(O/'summary.json');assert summary['primary_admissions']==0 and summary['actual_baseline_width_change']==0
    assert summary['primary']=='V181 unchanged' and summary['paper']=='V189 unchanged' and summary['current_delivery']=='V190 unchanged'
    for name,h in summary['source_sha256'].items():assert sha(R/name)==h,name
    f,lo,hi=revised_bounds();cities=f.city.tolist();assert lo.shape==hi.shape==(16,10)
    assert len(cities)==16 and {'Tokyo','Warsaw'}.issubset(cities)
    data=pd.read_csv(O/'profile_ranks.csv',float_precision='round_trip');bounds=pd.read_csv(O/'profile_bounds.csv',float_precision='round_trip')
    assert len(data)==128 and len(bounds)==640
    profiles={'retained_V181':[],'Tokyo_candidate':['Tokyo'],'Warsaw_candidate':['Warsaw'],'both_candidates':['Tokyo','Warsaw']}
    assert set(data.profile)==set(bounds.profile)==set(profiles)
    maximum=0.;records=[]
    frozen=pd.read_csv(R/'results/task4_user_v181_revision/utility_bounds.csv',float_precision='round_trip')
    frozen=frozen[frozen.scenario.eq('after_conditional')].set_index(['city','indicator'])
    for i,c in enumerate(cities):
        for j,n in enumerate(NAMES):
            close(frozen.loc[(c,n)].lower,lo[i,j],1e-15);close(frozen.loc[(c,n)].upper,hi[i,j],1e-15)
    for profile,changed in profiles.items():
        a=lo.copy()
        for c in changed:
            i=cities.index(c);population=int(f.iloc[i].population)
            assert population==obs[c]['population'] and int(f.iloc[i].population_year)==obs[c]['population_year']
            assert lo[i,6]==0 and hi[i,6]==1
            a[i,6]=3800000/(50*population+3800000)
        keep=np.ones_like(lo,dtype=bool)
        for c in changed:keep[cities.index(c),6]=False
        np.testing.assert_array_equal(a[keep],lo[keep]);assert np.count_nonzero(a!=lo)==len(changed)
        observed_bounds=bounds[bounds.profile.eq(profile)].set_index(['city','indicator']);assert len(observed_bounds)==160
        for i,c in enumerate(cities):
            for j,n in enumerate(NAMES):
                close(observed_bounds.loc[(c,n)].lower,a[i,j],1e-15);close(observed_bounds.loc[(c,n)].upper,hi[i,j],1e-15)
        restored=a.copy()
        for c in changed:restored[cities.index(c),6]=0
        np.testing.assert_array_equal(restored,lo)
        for ref,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
            L=[scalar(row,w) for row in a];U=[scalar(row,w) for row in hi];BL=[scalar(row,w) for row in lo]
            regrets=[max(0.,max(U[k] for k in range(16) if k!=i)-L[i]) for i in range(16)]
            mids=[scalar(row,w) for row in (a+hi)/2]
            result=data[data.profile.eq(profile)&data.weight_reference.eq(ref)].set_index('city');assert len(result)==16
            for i,c in enumerate(cities):
                row=result.loc[c]
                for key,value in [('score_lower',L[i]),('score_upper',U[i]),('max_regret',regrets[i]),('midpoint_illustrative_score',mids[i])]:
                    error=abs(float(row[key])-value);maximum=max(maximum,error);close(row[key],value)
                others=[k for k in range(16) if k!=i]
                assert bool(row.possible_champion)==(U[i]>=max(L[k] for k in others)-1e-12)
                assert bool(row.necessary_champion)==(L[i]>=max(U[k] for k in others)-1e-12)
                assert row.best_rank==1+sum(L[k]>U[i]+1e-12 for k in others)
                assert row.worst_rank==1+sum(U[k]>L[i]+1e-12 for k in others)
                assert row.decision_rank==1+sum(v<regrets[i] for v in regrets)
                assert row.midpoint_illustrative_rank==1+sum(v>mids[i] for v in mids)
            width=math.fsum(U[i]-L[i] for i in range(16))/16;baseline=math.fsum(U[i]-BL[i] for i in range(16))/16
            report=next(x for x in summary['profiles'] if x['profile']==profile and x['weight_reference']==ref)
            close(report['mean_width'],width);close(report['baseline_mean_width'],baseline)
            close(report['conditional_width_reduction'],baseline-width);close(report['conditional_width_reduction_percent'],100*(baseline-width)/baseline)
            selected=[cities[i] for i in range(16) if regrets[i]==min(regrets)];assert report['minimax_choices']==selected==['Zurich']
            assert report['possible_champions']==16 and report['necessary_champions']==0
            assert report['point_cells']==112 and report['fully_missing_cells']==13-len(changed) and report['partial_cells']==35+len(changed)
            records.append(dict(profile=profile,weight_reference=ref,mean_width=width,conditional_width_reduction=baseline-width,recommendation=selected,possible_champions=16,necessary_champions=0))
    assert summary['withdrawal_exactly_restores_V181'] and summary['all_upper_bounds_unchanged']
    return dict(rank_rows=128,bound_rows=640,maximum_scalar_score_or_regret_error=maximum,profiles=records,all_other158cells_and_alluppers_unchanged_in_joint_preview=True,withdrawal_restores_V181=True)
def main():
    saved=protection();source_report,obs=sources();model_report=model_checks(obs);protection()
    summary=read(O/'summary.json');paths=[O/'profile_ranks.csv',O/'profile_bounds.csv',O/'summary.json']
    result=dict(status='pass',version='V191 candidate independent audit',primary='V181 unchanged',paper='V189 unchanged',current_delivery='V190 unchanged',primary_admissions=0,actual_baseline_width_change=0,source_review=source_report,model_review=model_report,original_CSV_preserved=True,scientific_files_unchanged=len(saved['science']),paper_files_unchanged=len(saved['paper']),existing_registries_unchanged=len(saved['registries']),source_sha256={**summary['source_sha256'],str(Path(__file__).relative_to(R)):sha(Path(__file__)),'results/task4_v191_candidates/protected_files.json':sha(O/'protected_files.json')},audited_output_sha256={str(p.relative_to(R)):sha(p) for p in paths},visual_source_scope='Warsaw original network PDFp1 counts andp2 existing/planned schematic inspected from local rendered original;Świętokrzyska transfer and exclusion of dashed M2futureextension verified. MapfooterApril2024 not redated from2026uploadpath.',scope='Independent parsing verifies real directory subsets, city-address/count scope and candidate arithmetic. Tokyo catalogue dates do not date the inventory. No full-allmode coverage, contemporaneous operation, student access, forecast or real-world champion probability is established. Full extensions and paper consistency remain required before primary activation.')
    (O/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status='pass',rank_rows=128,bound_rows=640,source_counts={c:o['raw_count'] for c,o in obs.items()},scalar_max_error=model_report['maximum_scalar_score_or_regret_error'],paper_files_unchanged=len(saved['paper'])),indent=2))
if __name__=='__main__':main()
