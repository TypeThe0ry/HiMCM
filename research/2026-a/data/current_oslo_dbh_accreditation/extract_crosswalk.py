"""Named DBH/NOKUT identity bridges; failed responses never confirm identity."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from collections import Counter
import csv,hashlib,json,re,unicodedata,zipfile
D=Path(__file__).resolve().parent;R=D.parents[1]
def rows(p,sep=','):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=sep))
def norm(s):return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',s).casefold() if not unicodedata.combining(c)).split())
def host(s):return (urlsplit(s).hostname or '').casefold().removeprefix('www.')
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,t,a):
        if t in ['script','style']:self.skip+=1
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip=max(0,self.skip-1)
    def handle_data(self,s):
        if not self.skip:self.parts.append(s)
def text(p):
    t=Text();t.feed(p.read_text(errors='replace'));return ' '.join(' '.join(t.parts).split())
def main():
    national=rows(R/'data/current_oslo_he_crosswalk/national_roster.csv')
    campus=rows(R/'data/current_oslo_dbh_campus/api_662.csv')
    selected=[x for x in campus if x['Årstall'] in ['2025','2026'] and x['Kommunenummer campus']=='0301']
    names={}
    for x in selected:names.setdefault(x['Institusjonskode'],set()).add(x['Institusjonsnavn'])
    assert len(names)==27 and all(len(v)==1 for v in names.values())
    names={k:next(iter(v)) for k,v in names.items()}
    with zipfile.ZipFile(R/'data/task4_v5_resources/ror_2026_10_06.zip') as z:records=json.loads(z.read('v2.14-2026-10-06-ror-data.json'))
    index={}
    for r in records:
        if r['status']=='active':
            for n in r['names']:index.setdefault(norm(n['value']),[]).append(r)
    receipts=json.loads((D/'retrieval.json').read_text())
    output=[]
    for code,name in sorted(names.items()):
        evidence={}
        def add(n,e):evidence.setdefault(n['display_name'],(n,[]))[1].append(e)
        for n in national:
            if norm(n['display_name'])==norm(name):add(n,dict(method='exact_NOKUT_display_name',value=name))
            for r in index.get(norm(name),[]):
                same_names=[x['value'] for x in r['names'] if norm(x['value'])==norm(n['display_name'])]
                sites=[x['value'] for x in r['links'] if x['type']=='website' and host(x['value'])==host(n['url'])]
                if same_names or sites:add(n,dict(method='same_ROR_record_name_or_official_host',ror_id=r['id'],DBH_name=name,NOKUT_matching_ROR_names=same_names,NOKUT_matching_ROR_websites=sites))
            for receipt in receipts:
                if receipt['DBH_code']!=code or receipt.get('status')!=200:continue
                if host(receipt['requested_url'])!=host(n['url']) or host(receipt['final_url'])!=host(n['url']):continue
                body=text(D/receipt['file']);normal=norm(body)
                m=re.search(r'(?<!\w)'+re.escape(norm(name))+r'(?!\w)',normal)
                if m:add(n,dict(method='NOKUT_linked_official_page_exact_DBH_name',file=receipt['file'],matched_name=name))
        assert len(evidence)<=1,(code,evidence)
        n,proof=next(iter(evidence.values())) if evidence else ({},[])
        output.append(dict(DBH_code=code,DBH_name=name,NOKUT_name=n.get('display_name',''),NOKUT_category=n.get('category_heading',''),
                           NOKUT_scope=n.get('accreditation_scope',''),NOKUT_url=n.get('url',''),identity_evidence_json=json.dumps(proof,ensure_ascii=False),
                           category_time_aligned=False,complete_city_inventory_verified=False,decision='archived_national_identity_match' if proof else 'unresolved_primary_identity_bridge'))
    with (D/'crosswalk.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]),lineterminator='\n');w.writeheader();w.writerows(output)
    matched={x['DBH_code']:x for x in output if x['NOKUT_name']}
    assert len(matched)==25 and set(names)-set(matched)=={'1404','1405'}
    es=json.loads((R/'data/current_oslo_dbh_campus/enrolment_summary.json').read_text())
    periods=[]
    for p in es['periods']:
        ids=set(p['positive_any_mode_code_list']);verified=ids&set(matched)
        periods.append(dict(year=p['year'],semester=p['semester'],positive_any_mode_codes=len(ids),identity_matched_codes=len(verified),
                            unresolved_codes=sorted(ids-set(matched)),identity_matched_code_list=sorted(verified),
                            identity_only_vs_mode1or4=sorted(verified-set(p['positive_mode1_or4_code_list'])),
                            mode1or4_only_vs_identity=sorted(set(p['positive_mode1_or4_code_list'])-verified),
                            archived_NOKUT_categories=dict(sorted(Counter(matched[i]['NOKUT_category'] for i in verified).items()))))
    summary=dict(registry_codes=27,national_identity_matches=25,unresolved_codes=['1404','1405'],periods=periods,
                 original25_lineage_verified=False,complete_city_inventory_verified=False,category_time_alignment_verified=False,
                 primary_admissions=0,actual_primary_width_reduction=0,
                 scope='Identity bridge to an archived national category; not accreditation at every historical semester, campus/provider completeness or input replacement.')
    (D/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary))
if __name__=='__main__':main()
