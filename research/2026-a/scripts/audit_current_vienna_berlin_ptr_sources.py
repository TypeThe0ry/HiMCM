"""Read-only bounded source checks for Vienna9.4 and Berlin12.5 retained PTR points."""
from pathlib import Path
import csv,hashlib,json,zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs,plain_text

R=Path(__file__).resolve().parents[1];G=R.parents[1]
V=R/'data/current_vienna_ptr_point';B=R/'data/current_berlin_ptr_point'
O=R/'results/current_vienna_berlin_ptr_review/verification.json'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O,G)
    vr=read(V/'receipts.json');assert len(vr)==5
    for x in vr:
        if x['file'] is None:
            assert x['http_status'] is None and x['utc'] is None and x['bytes'] is None and x['sha256'] is None
            assert x['error'];continue
        p=V/x['file'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
        assert datetime.fromisoformat(x['utc']).utcoffset() is not None
    assert sorted(x['http_status'] for x in vr if x['file'])==[200,200,200,403]
    d=read(V/'eurostat_2023.json');assert d['id']==['freq','unit','isced11','geo','time'] and d['size']==[1,1,16,1,1]
    for dim,value in [('freq','A'),('unit','RT'),('geo','AT'),('time','2023')]:assert d['dimension'][dim]['category']['index']=={value:0}
    values={}
    for stage,expected in [('ED3',9.8),('ED1-3',10.3)]:
        index=str(d['dimension']['isced11']['category']['index'][stage]);values[stage]=d['value'][index];assert values[stage]==expected
    assert 9.4 not in d['value'].values()
    method=plain_text(V/'eurostat_method.html');assert 'expressed in full-time equivalents' in method
    bs=[]
    for receipt in sorted(B.glob('*.receipt.json')):
        x=read(receipt);p=B/x['body'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
        assert datetime.fromisoformat(x['requested_at_utc']).utcoffset() is not None;bs.append(x)
    assert len(bs)==4 and sorted(x['status'] for x in bs)==[200,200,200,429]
    assert (B/'bmbf_table_html_response.html').read_bytes().lstrip().lower().startswith(b'<!doctype html>')
    assert not (B/'bmbf_table_html_response.html').read_bytes().startswith(b'%PDF')
    blocked=next(x for x in bs if x['status']==429);assert blocked['body'].endswith('.html')
    workbook=B/'destatis_2024_25.xlsx'
    with zipfile.ZipFile(workbook) as z:
        sheets=ET.fromstring(z.read('xl/workbook.xml')).findall('.//{*}sheet')
        sheet=next(x for x in sheets if x.get('name')=='Informationen zur Statistik')
        rid=sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        rel=next(x for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels')) if x.get('Id')==rid)
        target=rel.get('Target');target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
        strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        cells={}
        for c in ET.fromstring(z.read(target)).findall('.//{*}c'):
            v=c.find('{*}v')
            if v is not None:cells[c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else v.text
    assert 'Öffentliche und nicht öffentliche allgemeinbildende Schulen' in cells['A5']
    assert cells['A11']=='Schuljahr.' and 'September bis Oktober' in cells['A12']
    assert 'Personen gezählt' in cells['A111'] and 'Vollzeitlehrereinheiten' in cells['A111'] and 'www.kmk.org' in cells['A111']
    assert 'öffentlichen Schulen' in cells['A151'] and 'privaten Ersatzschulen' in cells['A151']
    for directory,value,year in [(V,9.4,2023),(B,12.5,2025)]:
        scope=read(directory/'scope.json');assert scope['original_value']==value and scope['original_year']==year and scope['original_flag']=='ok'
        assert scope['exact_value_match'] is False and scope['original_lineage_verified'] is False and scope['target_scope_verified'] is False
    with (R/'data/task4_v117_team_intake/city_indicators.csv').open(encoding='utf-8-sig') as f:raw={x['city']:x for x in csv.DictReader(f)}
    assert raw['Vienna']['pupil_teacher_ratio']=='9.4' and raw['Berlin']['pupil_teacher_ratio']=='12.5'
    protected=protected_inputs();current=read(R/'results/current_paper_review/current_verification.json')
    for n,h in current['edition_source_sha256'].items():assert sha(R/n)==h,n
    sources=[p for directory in [V,B] for p in sorted(directory.rglob('*')) if p.is_file()]+[Path(__file__),R/'scripts/task4_audit_output.py']
    report=dict(status='pass scoped source review',**protected,edition_entries_checked=24,Vienna_original9_4_verified=False,Berlin_original12_5_verified=False,Austria_national2023_FTE_ratios=values,successful_response_bodies=6,HTTP403_bodies=1,HTTP429_bodies=1,interrupted_download_without_body=1,HTTP200_HTML_not_PDF=1,Berlin_workbook_metadata_cells_checked=['A5','A11','A12','A111','A151'],unverified_index_lead_admitted=False,primary_admissions=0,actual_primary_width_reduction=0,source_sha256={str(p.relative_to(R)):sha(p) for p in sources},scope='National Austria values are not Vienna validation. Berlin person-count metadata is not a city upper-secondary FTE ratio; indexed12.5lead remains unverified. Original points unchanged; no derived ratio, missing-data admission, classroom-contact-hour requirement or paper change.')
    emit_report(report,a,O,G)

if __name__=='__main__':main()
