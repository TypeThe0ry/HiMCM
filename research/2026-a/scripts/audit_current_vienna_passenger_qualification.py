"""Bound the public-route qualification independently of model activation."""
import csv,hashlib,html,json,re,subprocess,sys,tempfile
from collections import Counter,defaultdict
from pathlib import Path
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
R=Path(__file__).resolve().parents[1];G=R.parents[1];D=R/'data/current_vienna_passenger_qualification';O=R/'results/current_vienna_passenger_qualification';C=R/'results/current_vienna_gtfs_candidate'
def read(p):return json.loads(p.read_text())
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    a=audit_parser(__doc__).parse_args();canonical=O/'verification.json';check_output(a,canonical,G);before=protected_inputs()
    for n in ['operator_fahrplaene.html','operator_fahrplaene_subdomain.html']:
        m=read(D/(n+'.receipt.json'));p=D/n;assert m['status']==200 and sha(p)==m['sha256'] and p.stat().st_size==m['bytes']
        text=p.read_text();assert '<title>Netzpläne, Fahrpläne - Wiener Linien</title>' in text and 'alle Fahrpläne unserer U-Bahnen, Straßenbahnen und Busse' in text
    attempts=read(D/'document_attempts.json');assert len(attempts)==14
    for m in attempts:
        p=D/m['stored_body'];assert m['status']==200 and p.stat().st_size==m['bytes']==118395 and sha(p)==m['sha256']
        assert not m['PDF_magic'] and not m['admitted_PDF'] and not p.read_bytes().startswith(b'%PDF')
    assert len({m['sha256'] for m in attempts})==14
    # A separate regex reads route headings from raw blocks rather than importing the production parser.
    text=(D/'operator_fahrplaene.html').read_text();heads=[]
    for b in re.findall(r'<li class="c-download-list__item[^>]*>(.*?)</li>',text,re.S):
        m=re.search(r'<h3[^>]*>Linie ([0-9]+A)([^<]*)</h3>',b)
        if m:heads.append((m[1],m[2].strip(),b))
    assert len(heads)==93 and len({h[0] for h in heads})==89
    saved=rows(O/'catalogue_entries.csv');assert len(saved)==93
    for (route,suffix,block),r in zip(heads,saved):
        assert r['route']==route and r['title']==html.unescape('Linie '+route+(' '+suffix if suffix else ''))
        assert r['Stand_is_not_effective_date']=='True' and r['pdf_url'] in html.unescape(block)
        flags=[]
        for needle,flag in [('Winterfahrplan','winter'),('Umleitung','detour')]:
            if needle in r['title']:flags.append(flag)
        if 'Wochentagen' in r['title'] or 'Wochenenden' in r['title']:flags.append('weekday_weekend')
        if 'traffic--callbus' in block:flags.append('callbus_listing')
        assert json.loads(r['condition_flags_json'])==flags
        assert json.loads(r['source_kinds_json'])==[k for k in ['callbus','citybus'] if 'traffic--'+k in block]
    coverage=rows(O/'route_coverage.csv');witnesses=rows(C/'station_witnesses.csv');counts=Counter(w['route_short_name'] for w in witnesses)
    assert len(coverage)==len(counts)==88 and sum(counts.values())==378
    expected_routes={'41A','43A','56A','58A','73A','74A','86A','89A','92A'};condition=set()
    for r in coverage:
        route=r['route'];assert int(r['selected_witness_groups'])==counts[route]
        assert r['advertised_passenger_route']=='True' and r['trip_level_PDF_conditions_verified']=='False'
        rr=[x for x in saved if x['route']==route];assert len(rr)==int(r['catalogue_entries'])>0
        assert json.loads(r['titles_json'])==[x['title'] for x in rr]
        flags=sorted({f for x in rr for f in json.loads(x['condition_flags_json'])});assert flags==json.loads(r['condition_flags_json'])
        if flags:condition.add(route)
    assert condition==expected_routes
    s=read(O/'summary.json');ids=sorted(w['DIVA'] for w in witnesses if w['route_short_name'] in condition)
    assert s['condition_selected_DIVA_ids']==ids and len(ids)==36 and s['conservative_selected_witness_withhold_count']==342
    assert s['public_passenger_nature_supported'] and s['source_defined_scheduled_supply_supported']
    assert not s['trip_level_PDF_conditions_verified'] and not s['actual_operation_verified']
    prior=read(C/'verification.json')
    for n,h in prior['source_sha256'].items():assert sha(R/n)==h,n
    with tempfile.TemporaryDirectory(prefix='himcm-vienna-public-',dir='/data/scratch') as tmp:
        out=Path(tmp)/'replay';subprocess.run([sys.executable,str(R/'scripts/task4_current_vienna_passenger_qualification.py'),'--output-dir',str(out)],check=True,stdout=subprocess.PIPE)
        for n in ['catalogue_entries.csv','route_coverage.csv','summary.json']:assert (out/n).read_bytes()==(O/n).read_bytes()
    assert protected_inputs()==before
    for n,h in read(R/'results/current_paper_review/current_verification.json')['edition_source_sha256'].items():assert sha(R/n)==h,n
    files=[*sorted(D.iterdir()),*[O/n for n in ['README.md','catalogue_entries.csv','route_coverage.csv','summary.json','peer_review.json']],
        C/'verification.json',C/'station_witnesses.csv',R/'scripts/task4_current_vienna_passenger_qualification.py',Path(__file__)]
    report=dict(status='pass public-route nature qualification for source-defined scheduled supply',**before,edition_entries_checked=24,
        successful_passenger_index_originals=2,catalogue_entries=93,catalogue_A_routes=89,witness_routes_matched=88,witness_groups=378,
        unusable_HTML_document_responses=14,original_PDFs_obtained=0,condition_routes=sorted(condition),condition_selected_witnesses=36,
        conservative_withhold_count=342,public_passenger_nature_supported=True,trip_level_PDF_conditions_verified=False,actual_operation_verified=False,
        output_files_bytewise_reproduced=3,primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
        source_sha256={str(p.relative_to(R)):sha(p) for p in files if p.is_file()},
        scope='Public facility supply qualification, not universal access, fare/booking exclusion, actual operation or PDF validation. Prior structural report frozen; activation remains separate.')
    emit_report(report,a,canonical,G)
if __name__=='__main__':main()
