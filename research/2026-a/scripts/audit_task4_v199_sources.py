"""Read-only audit of V199 physical-venue source packages; no admission."""
import csv
import hashlib
import html
import json
import math
import numpy as np
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from task4_v5_model import ROOT, NAMES
from task4_user_v197_revision import revised_bounds

SG = ROOT/'data/task4_v199_sgpool'
OSLO = ROOT/'data/task4_v199_oslopool'
OUT = ROOT/'results/task4_v199_priority/source_verification.json'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
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

def main():
    snapshot=read(ROOT/'design/task4_user_v197_snapshot.json')['source_sha256']; assert len(snapshot)==361
    nav=[f'design/task4_user_current_{n}.json' for n in ['model','extensions','review','delivery']]
    baseline=read(ROOT/'results/task4_v199_priority/summary.json')['source_sha256']
    for name,digest in snapshot.items(): assert sha(ROOT/name)==digest, name
    for name in nav: assert sha(ROOT/name)==baseline[name],name
    files = [p for p in list(SG.rglob('*'))+list(OSLO.rglob('*')) if p.is_file()]
    files += [ROOT/'scripts/task4_v199_candidate.py', ROOT/'results/task4_v199_priority/candidate_preview.json', ROOT/'results/task4_v199_priority/candidate_scores.csv']
    before={str(p.relative_to(ROOT)):sha(p) for p in files}
    for name,digest in read(SG/'manifest.json').items(): assert sha(SG/name)==digest, name
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
    om=read(OSLO/'retrieval_manifest.json')
    for r in om['sources']:
        assert r['http_status']==200 and sha(OSLO/r['raw_file'])==r['sha256']
    search=read(OSLO/'directory_search_retrieval.json'); sr=OSLO/'directory_search_response_original.json'
    assert search['status']==200 and search['sha256']==sha(sr) and search['response_bytes']==sr.stat().st_size
    base='https://www.oslo.kommune.no/natur-kultur-og-fritid/svommehaller-i-oslo/'
    excluded={'Svømmehaller i Oslo','Kapasitet i svømmehallene','Billettpriser for Oslo kommunes bad','Ordensregler for Oslo kommunes bad'}
    hits=[h for h in read(sr)['hits'] if (h.get('meta') or {}).get('url','').startswith(base) and h.get('name') not in excluded]
    derived=read(OSLO/'directory_facilities_extracted.json')
    assert len(hits)==len(derived)==9 and {h['name'] for h in hits}=={r['name'] for r in derived}
    assert len({h['name'] for h in hits})==9 and sum(r['facility_type']=='outdoor_seasonal' for r in derived)==1
    with (ROOT/'data/task4_v117_team_intake/city_indicators.csv').open(newline='', encoding='utf-8-sig') as fp:
        original=next(r for r in csv.DictReader(fp) if r['city']=='Oslo')
    assert float(original['pools_per_100k'])==5.29 and float(original['pools_per_100k_year'])==2021 and original['pools_per_100k_flag']=='ok'
    assert float(original['pool_count'])==37 and int(original['population'])==727797 and int(original['population_year'])==2025
    # Independently recompute all candidate decision rows and summaries.
    preview=read(ROOT/'results/task4_v199_priority/candidate_preview.json')
    for name,digest in preview['source_sha256'].items(): assert sha(ROOT/name)==digest,name
    with (ROOT/'results/task4_v199_priority/candidate_scores.csv').open(newline='') as fp: candidate=list(csv.DictReader(fp))
    assert len(candidate)==96 and len({(r['scenario'],r['weight_reference'],r['city']) for r in candidate})==96
    frame,lo,hi=revised_bounds(); saved=np.stack([lo,hi]).copy(); cities=frame.city.tolist()
    i,j=cities.index('Singapore'),NAMES.index('public_pool_density'); population=int(frame.iloc[i].population)
    assert population==6036900 and int(frame.iloc[i].population_year)==2024
    def score(matrix,w):
        result=[]
        for row in matrix:
            good=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))
            bad=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))
            result.append(100*good/(good+bad))
        return result
    for scenario,count in [('retained_V197',7),('inventory25_partial_closure_flags',25),('withhold3_notice_venues22',22)]:
        low=lo.copy(); density=count*100000/population;low[i,j]=density/(1+density)
        mask=np.ones_like(low,dtype=bool);mask[i,j]=False
        np.testing.assert_array_equal(low[mask],lo[mask])
        if count==7: np.testing.assert_allclose(low,lo,atol=1e-15,rtol=0)
        for ref,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
            lower,upper,middle=score(low,w),score(hi,w),score((low+hi)/2,w)
            regret=[max(0,max(upper[k] for k in range(16) if k!=a)-lower[a]) for a in range(16)]
            possible=[upper[a]>=max(lower[k] for k in range(16) if k!=a)-1e-12 for a in range(16)]
            necessary=[lower[a]>=max(upper[k] for k in range(16) if k!=a)-1e-12 for a in range(16)]
            rows=[r for r in candidate if r['scenario']==scenario and r['weight_reference']==ref]
            assert len(rows)==16 and {r['city'] for r in rows}==set(cities)
            for r in rows:
                a=cities.index(r['city']);others=[k for k in range(16) if k!=a]
                for field,value in [('score_lower',lower[a]),('score_upper',upper[a]),('max_regret',regret[a]),('midpoint_illustrative_score',middle[a])]: assert abs(float(r[field])-value)<3e-10,(scenario,ref,r['city'],field)
                for field,value in [('best_rank',1+sum(lower[k]>upper[a]+1e-12 for k in others)),('worst_rank',1+sum(upper[k]>lower[a]+1e-12 for k in others)),('decision_rank',1+sum(x<regret[a] for x in regret)),('midpoint_illustrative_rank',1+sum(x>middle[a] for x in middle))]: assert int(r[field])==value,(scenario,ref,r['city'],field)
                assert (r['possible_champion']=='True')==possible[a] and (r['necessary_champion']=='True')==necessary[a]
            summary=next(x for x in preview['summaries'] if x['scenario']==scenario and x['weight_reference']==ref)
            expected={'count':count,'utility_lower':low[i,j],'mean_score_width':sum(b-a for a,b in zip(lower,upper))/16,'minimax_regret':min(regret),'Singapore_regret_gap_to_best_other':regret[i]-min(regret[k] for k in range(16) if k!=i),'possible_count':sum(possible),'necessary_count':sum(necessary)}
            for field,value in expected.items(): assert abs(summary[field]-value)<3e-10,(scenario,ref,field)
            assert summary['conservative_recommendation']==';'.join(cities[k] for k in range(16) if regret[k]<=min(regret)+1e-12)
    _,a,b=revised_bounds(); np.testing.assert_array_equal(saved,np.stack([a,b]))
    for name,digest in {**snapshot,**before}.items(): assert sha(ROOT/name)==digest,name
    for name in nav: assert sha(ROOT/name)==baseline[name],name
    result={'status':'pass','scope':'Source identity and notices audit; no model admission. Directory count is a named public-venue inventory candidate, not a count of open or accessible venues; absence of notice is not proof of opening or universal teen access.','singapore':{'directory_cards':25,'unique_names_addresses_postcodes_and_slugs':25,'old_article_postcodes_in_directory':7,'additional_legacy_union_count':0,'page_last_updated':'8 November 2026 (page metadata, not inventory date)','detail_receipts_200_and_identity_matched':25,'weekly_maintenance_pages':25,'pool_specific_temporary_notices':notices,'partial_access_banner':'Jurong East','unknown_current_open_or_access_count':True},'oslo':{'user_point':5.29,'point_year':2021,'helper_count':37,'separate_population':727797,'population_year':2025,'current_municipal_directory_venues':9,'directory_role':'2026 corroboration only; not replacement or 2021 inventory'},'candidate_scenarios':3,'candidate_weight_city_rows_independently_checked':96,'candidate_preview_not_admitted':True,'snapshot_bindings':361,'four_navigation_files_match_v199_baseline':True,'primary_admissions':0,'source_sha256':{**before,**{n:sha(ROOT/n) for n in nav},str(Path(__file__).relative_to(ROOT)):sha(Path(__file__))}}
    OUT.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},indent=2,ensure_ascii=False))
if __name__=='__main__': main()
