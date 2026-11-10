"""Match Vienna candidate routes to the operator's passenger timetable catalogue."""
import argparse,csv,json,re
from collections import Counter,defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
R=Path(__file__).resolve().parents[1];D=R/'data/current_vienna_passenger_qualification';C=R/'results/current_vienna_gtfs_candidate'
class Catalogue(HTMLParser):
    def __init__(self):super().__init__();self.depth=0;self.item=None;self.heading=False;self.items=[]
    def handle_starttag(self,t,a):
        attrs=dict(a);classes=attrs.get('class','')
        if t=='li':
            if self.item is not None:self.depth+=1
            elif 'c-download-list__item' in classes:self.item=dict(title=[],text=[],hrefs=[],kinds=set());self.depth=1
        if self.item is not None:
            if t=='h3':self.heading=True
            if t=='a' and '.pdf' in attrs.get('href',''):self.item['hrefs'].append(attrs['href'])
            for kind in ['citybus','callbus']:
                if 'traffic--'+kind in classes:self.item['kinds'].add(kind)
    def handle_data(self,s):
        if self.item is not None:
            self.item['text'].append(s)
            if self.heading:self.item['title'].append(s)
    def handle_endtag(self,t):
        if t=='h3':self.heading=False
        if t=='li' and self.item is not None:
            self.depth-=1
            if self.depth==0:self.items.append(self.item);self.item=None
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(p,rr):
    with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr)
def entries(p):
    parser=Catalogue();parser.feed(p.read_text());out=[]
    for x in parser.items:
        title=' '.join(' '.join(x['title']).split());m=re.fullmatch(r'Linie ([0-9]+A)(?: .*)?',title)
        if not m:continue
        text=' '.join(' '.join(x['text']).split());date=re.search(r'Stand:\s*([0-9.]+)',text);assert len(x['hrefs'])==1
        flags=[]
        if 'Winterfahrplan' in title:flags.append('winter')
        if 'Umleitung' in title:flags.append('detour')
        if 'Wochentagen' in title or 'Wochenenden' in title:flags.append('weekday_weekend')
        if 'callbus' in x['kinds']:flags.append('callbus_listing')
        out.append(dict(entry_number=len(out)+1,route=m[1],title=title,source_kinds_json=json.dumps(sorted(x['kinds'])),
            Stand_date=date[1] if date else '',Stand_is_not_effective_date=True,pdf_url=x['hrefs'][0],condition_flags_json=json.dumps(flags)))
    return out
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True)
    out=ap.parse_args().output_dir.resolve()
    if out.exists():raise FileExistsError('Use a new output directory')
    base=entries(D/'operator_fahrplaene.html');alias=entries(D/'operator_fahrplaene_subdomain.html')
    def comparable(rr):
        out=[]
        for r in rr:
            u=urlsplit(r['pdf_url']);assert u.hostname in ['www.wienerlinien.at','tramwm.wienerlinien.at']
            out.append(dict(r,pdf_url=u.path+'?'+u.query))
        return out
    assert comparable(base)==comparable(alias)
    witnesses=rows(C/'station_witnesses.csv');assert len(witnesses)==378
    by=defaultdict(list)
    for r in base:by[r['route']].append(r)
    route_counts=Counter(r['route_short_name'] for r in witnesses);assert len(route_counts)==88 and set(route_counts)<=by.keys()
    coverage=[];condition_ids=[]
    for route,count in sorted(route_counts.items()):
        rr=by[route];flags=sorted({flag for r in rr for flag in json.loads(r['condition_flags_json'])})
        coverage.append(dict(route=route,catalogue_entries=len(rr),selected_witness_groups=count,advertised_passenger_route=True,
            titles_json=json.dumps([r['title'] for r in rr],ensure_ascii=False),source_kinds_json=json.dumps(sorted({k for r in rr for k in json.loads(r['source_kinds_json'])})),
            condition_flags_json=json.dumps(flags),trip_level_PDF_conditions_verified=False))
        if flags:condition_ids.extend(w['DIVA'] for w in witnesses if w['route_short_name']==route)
    attempts=json.loads((D/'document_attempts.json').read_text());assert len(attempts)==14 and all(not a['PDF_magic'] and not a['admitted_PDF'] for a in attempts)
    summary=dict(status='public passenger route nature supported; full model integration not yet activated',
        candidate_DIVA_groups=378,candidate_witness_routes=88,matched_public_catalogue_routes=88,
        all_A_catalogue_entries=len(base),all_A_catalogue_routes=len(by),alias_entries_equal_after_host_normalization=True,
        condition_routes=[r['route'] for r in coverage if json.loads(r['condition_flags_json'])],
        condition_selected_witness_groups=len(condition_ids),condition_selected_DIVA_ids=sorted(condition_ids),
        conservative_selected_witness_withhold_count=378-len(condition_ids),
        inaccessible_document_attempts=14,original_PDFs_obtained=0,public_passenger_nature_supported=True,
        source_defined_scheduled_supply_supported=True,trip_level_PDF_conditions_verified=False,actual_operation_verified=False,
        primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
        scope='Operator passenger index plus existing GTFS service-day witnesses supports scheduled public facility supply, without freefare/universalaccess/no-booking/actual-operation claims. Winter, detour, day and callbus listings remain explicit; Stand is a document date. Challenged downloads are HTML, not PDFs. Withholding selected-witness groups is conservative and does not establish their absence or search for alternate witnesses.')
    out.mkdir(parents=True);write(out/'catalogue_entries.csv',base);write(out/'route_coverage.csv',coverage)
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
