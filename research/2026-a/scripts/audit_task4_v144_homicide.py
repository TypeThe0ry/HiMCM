"""Independent source inclusion checks and scalar recalculation of targeted withdrawals."""
from pathlib import Path
import csv,gzip,hashlib,json,math,re,subprocess,tempfile,zipfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results/task4_v144_homicide_sensitivity';DATA=ROOT/'data/task4_v144_homicide'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def score(row,w):
    a=math.sqrt(math.fsum(x*x*v for x,v in zip(row,w)));b=math.sqrt(math.fsum((1-x)**2*v for x,v in zip(row,w)));return 100*a/(a+b)
def main():
    summary=read(OUT/'summary.json');frozen=summary['source_sha256']
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    receipt=read(DATA/'verification.json');assert sha(DATA/'extract.py')==receipt['source_extractor_sha256']
    for meta in read(DATA/'retrievals.json'):
        raw=(DATA/meta['file']).read_bytes();raw=gzip.decompress(raw) if meta['file'].endswith('.gz') else raw
        assert len(raw)==meta['raw_bytes'] and hashlib.sha256(raw).hexdigest()==meta['raw_sha256']
    # Independently check the exact XML cells and period header in the archived workbook.
    ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(DATA/'cbs2022_original.xlsx') as z:
        strings=[''.join(t.itertext()) for t in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        root=ET.fromstring(z.read('xl/worksheets/sheet7.xml'));values={}
        for c in root.findall('.//m:c',ns):
            v=c.find('m:v',ns)
            if v is not None:values[c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else v.text
        assert '2018-2022*' in values['A1'] and values['A24']=='Amsterdam' and int(values['B24'])==68 and float(values['F24'])==1.55
    annual=read(DATA/'cbs_annual_table_extracted.json');assert next(x for x in annual if x[0]=='2022*')==['2022*','10','16','3']
    # Verify an original HTML table row, not the extraction receipt alone.
    html=gzip.decompress((DATA/'cbs_news2022_original.html.gz').read_bytes()).decode('utf-8')
    assert re.search(r'<tr[^>]*>\s*<t[dh][^>]*>\s*2022\*\s*</t[dh]>\s*<td[^>]*>\s*10\s*</td>\s*<td[^>]*>\s*16\s*</td>\s*<td[^>]*>\s*3\s*</td>',html,re.I), 'Original annual city row'
    notes=read(DATA/'cbs_cells_extracted.json')['Toelichting']['cells'];assert 'niet-ingezetenen' in notes['A4']
    with tempfile.TemporaryDirectory(prefix='himcm_v144_audit_',dir='/data/scratch') as t:
        pdf=Path(t)/'original.pdf';pdf.write_bytes(gzip.decompress((DATA/'zurich2025_original.pdf.gz').read_bytes()))
        for page in [117,118,120]:assert subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(pdf),'-'])==(DATA/f'zurich_page_{page:03d}_extracted.txt').read_bytes()
    text=(DATA/'zurich_page_117_extracted.txt').read_text();assert 'Stadt Zürich gesamt' in text and re.search(r'2021\s+2022\s+2023\s+2024\s+2025',text)
    assert re.search(r'Tötungsdelikte vollendet\s+3\s+4\s+4\s+1\s+2',text)
    assert re.search(r'Tötungsdelikte versucht\s+14\s+14\s+18\s+17\s+20',text)
    assert 'ungeachtet der Anzahl geschädigter Personen' in ' '.join((DATA/'zurich_page_118_extracted.txt').read_text().split())
    source=rows(ROOT/'data/task4_v117_team_intake/city_indicators.csv');cities=[x['city'] for x in source]
    bounds=[x for x in rows(ROOT/'results/task4_user_v136_revision/utility_bounds.csv') if x['scenario']=='after_conditional'];assert len(bounds)==160
    names=list(dict.fromkeys(x['indicator'] for x in bounds));assert names[0]=='homicide_rate'
    grid={(x['city'],x['indicator']):(float(x['lower']),float(x['upper'])) for x in bounds}
    targets={'retained':[],'withdraw_Amsterdam_homicide':['Amsterdam'],'withdraw_Zurich_homicide':['Zurich'],'withdraw_both_homicides':['Amsterdam','Zurich']}
    output=rows(OUT/'ranks.csv');assert len(output)==128
    changes=rows(OUT/'withdrawn_cells.csv');assert len(changes)==4
    count=0
    for scenario,selected in targets.items():
        mask={(c,'homicide_rate') for c in selected};listed=[x for x in changes if x['scenario']==scenario];assert {(x['city'],x['indicator']) for x in listed}==mask and len(listed)==len(mask)
        for x in listed:assert (float(x['old_lower']),float(x['old_upper']))==grid[x['city'],x['indicator']] and float(x['new_lower'])==0 and float(x['new_upper'])==1
        lower={c:[0 if (c,n) in mask else grid[c,n][0] for n in names] for c in cities};upper={c:[1 if (c,n) in mask else grid[c,n][1] for n in names] for c in cities}
        for ref,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
            lows={c:score(lower[c],w) for c in cities};highs={c:score(upper[c],w) for c in cities};regret={c:max(0,max(highs[d] for d in cities if d!=c)-lows[c]) for c in cities}
            mid={c:score([(a+b)/2 for a,b in zip(lower[c],upper[c])],w) for c in cities}
            saved=[x for x in output if x['scenario']==scenario and x['weight_reference']==ref];assert len(saved)==16 and {x['city'] for x in saved}==set(cities)
            for x in saved:
                c=x['city'];values={'score_lower':lows[c],'score_upper':highs[c],'max_regret':regret[c],'midpoint_illustrative_score':mid[c],'decision_rank':1+sum(v<regret[c] for v in regret.values()),'best_rank':1+sum(lows[d]>highs[c]+1e-12 for d in cities if d!=c),'worst_rank':1+sum(highs[d]>lows[c]+1e-12 for d in cities if d!=c),'midpoint_illustrative_rank':1+sum(v>mid[c] for v in mid.values())}
                for k,v in values.items():assert abs(float(x[k])-v)<2e-11,(scenario,c,k)
                assert (x['possible_champion']=='True')==(highs[c]>=max(lows[d] for d in cities if d!=c)-1e-12)
                assert (x['necessary_champion']=='True')==(lows[c]>=max(highs[d] for d in cities if d!=c)-1e-12)
                count+=1
            case=next(x for x in summary['cases'] if x['scenario']==scenario and x['weight_reference']==ref)
            assert case['minimax_choices']==[c for c in cities if regret[c]==min(regret.values())] and case['withdrawn_point_cells']==len(mask)
            assert case['possible_champions']==16 and case['necessary_champions']==0 and abs(case['mean_interval_width']-math.fsum(highs[c]-lows[c] for c in cities)/16)<2e-11
    assert read(DATA/'observations.json')==[]
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    result=dict(status='pass',independent_city_cases=count,independent_score_bounds=count*2,source_workbook_cells_verified=['A1','A24','B24','F24'],cbs_original_annual_HTML_row_verified=True,cbs_annual_and_five_year_periods_distinct=True,zurich_original_three_pages_reextracted=True,zurich_offence_vs_person_definition_verified=True,primary_admissions=0,source_hashes_before_after_match=True,result_sha256={str(p.relative_to(ROOT)):sha(p) for p in OUT.iterdir() if p.suffix in {'.csv','.json'} and p.name not in {'verification.json','recheck_verification.json'}},verifier_sha256=sha(Path(__file__)))
    target=OUT/('recheck_verification.json' if (OUT/'verification.json').exists() else 'verification.json');target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
