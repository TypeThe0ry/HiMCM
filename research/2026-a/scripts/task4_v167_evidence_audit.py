"""Independently compare160 plotted cells, original school tables and protected files."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, re, subprocess, zlib, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v167_evidence'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    snapshot=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
    for n,h in snapshot.items():assert sha(R/n)==h,n
    protected=read(O/'protected_files.json')['manuscript']
    for n,h in protected.items():assert sha(P/n)==h,n
    with (R/'results/task4_user_v154_revision/utility_bounds.csv').open() as f:
        old={(r['city'],r['indicator']):(float(r['lower']),float(r['upper'])) for r in csv.DictReader(f) if r['scenario']=='after_conditional'}
    rows=list(csv.DictReader((O/'matrix.csv').open()));assert len(rows)==len(old)==160
    assert len({(r['city'],r['indicator']) for r in rows})==160
    states=[];unknown=Counter()
    labels={'homicide_rate':'Homicide','pm25':'PM2.5','cost_living_index':'Living cost',
            'price_income_ratio':'Housing','upper_secondary_ptr':'Pupil/teacher',
            'research_he_density':'Research/HE','public_transport_density':'Transit',
            'travel':'School trip','fixed_broadband_mbps':'Broadband','public_pool_density':'Pools'}
    for r in rows:
        assert r['plot_label']==labels[r['indicator']]
        a,b=old[r['city'],r['indicator']]
        assert abs(float(r['utility_lower'])-a)<2e-15 and abs(float(r['utility_upper'])-b)<2e-15
        assert abs(float(r['interval_width'])-(b-a))<3e-15
        state='point' if a==b else ('unknown' if a==0 and b==1 else 'partial')
        assert r['state']==state
        states.append(state)
        if state=='unknown':unknown[r['indicator']]+=1
    assert Counter(states)=={'point':112,'partial':34,'unknown':14}
    assert unknown=={'upper_secondary_ptr':8,'travel':3,'public_transport_density':3}
    manifest=read(O/'figure_manifest.json');assert manifest['matrix_sha256']==sha(O/'matrix.csv')
    for ext,h in manifest['output_sha256'].items():assert sha(O/f'identification_matrix.{ext}')==h
    svg=ET.parse(O/'identification_matrix.svg').getroot();ns={'s':'http://www.w3.org/2000/svg'}
    assert not svg.findall('.//s:image',ns),'Matrix must remain vector'
    cells=[x for x in svg.findall('.//s:g',ns) if x.get('id','').startswith('cell-')]
    assert {x.get('id') for x in cells}=={f'cell-{i}-{j}' for i in range(16) for j in range(10)}
    assert all(len(x.findall('s:path',ns))==1 for x in cells)
    info=subprocess.check_output(['pdfinfo',str(O/'identification_matrix.pdf')],text=True)
    assert re.search(r'Pages:\s+1\b',info) and re.search(r'Page size:\s+468 x 446\.4 pts',info)
    images=subprocess.check_output(['pdfimages','-list',str(O/'identification_matrix.pdf')],text=True)
    assert len(images.strip().splitlines())==2
    # Type3 bbox heights in pdftohtml are not nominal point sizes. Inspect the
    # PDF text-font operators and standard font matrices instead.
    pdfbytes=(O/'identification_matrix.pdf').read_bytes();sizes=[]
    for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream',pdfbytes,re.S):
        try:decoded=zlib.decompress(stream)
        except zlib.error:continue
        sizes.extend(float(s) for s in re.findall(rb'/F\d+\s+([\d.]+)\s+Tf',decoded))
    matrices=re.findall(rb'/FontMatrix\s*\[([^]]+)\]',pdfbytes)
    assert matrices and all([float(v) for v in m.split()]==[.001,0,0,.001,0,0] for m in matrices)
    assert set(sizes)=={10,12} and 10*5.85/6.5>=9-1e-12
    text=subprocess.check_output(['pdftotext',str(O/'identification_matrix.pdf'),'-'],text=True)
    assert text.count('?')==15 #14 cells plus footer key
    for marker in ['112 point','34 partial','14 unknown','Utility interval width']:assert marker in text
    receipts=0
    for folder in ['task4_v167_kzn','task4_v167_kvz']:
        d=R/'data'/folder
        for row in read(d/'retrieval.json'):
            assert row['status']==200 and sha(d/row['file'])==row['sha256'];receipts+=1
    pages=subprocess.check_output(['pdftotext','-layout',str(R/'data/task4_v167_kzn/kzn_annual_2024_2025_original.pdf'),'-'],text=True).split('\f')
    assert re.search(r'Untergymnasium\s+225\s+201\s+426',pages[36]) and 'Per 15. September 2024' in pages[36]
    assert 'Personenanzahl' in pages[37] and re.search(r'Lehrpersonen\s*\(\s*exklusiv acht Schulleitende\s*\)\s+284',pages[37])
    assert '301' in pages[5] and 301-(284+8)==9
    pages=subprocess.check_output(['pdftotext','-layout',str(R/'data/task4_v167_kvz/annual_2024_25_original.pdf'),'-'],text=True).split('\f')
    assert re.search(r'Vollzeitstellen im Jahresdurchschnitt.*',pages[35])
    assert '(und im Vorjahr) unter 250' in pages[35]
    assert re.search(r'Erfolgsrechnung\s*\(\s*in CHF\s*\)',pages[32]) and '31.12.2024' in pages[32]
    assert '28’462’596' in pages[32]
    visual=read(O/'visual_review.json');assert visual['pdf_sha256']==sha(O/'identification_matrix.pdf') and visual['accepted']
    result=dict(status='pass',iteration='V167',protected_scientific_files=len(snapshot),protected_manuscript_files=len(protected),
        source_original_responses=receipts,plotted_cells_independently_compared=160,vector_matrix_paths=160,embedded_raster_images_in_SVG=0,
        counts=dict(Counter(states)),unknown_by_indicator=dict(unknown),minimum_font_pt_at6_5in=min(sizes),minimum_insertion_width_for9pt=5.85,
        color_and_grayscale_visually_reviewed=True,source_pdf_pages_visually_reviewed={'KZN':[6,37,38],'KVZ':[33,36]},
        primary_data_admissions=0,primary_score_width_change=0,current_model='V154 unchanged',current_paper='V166 unchanged',
        paper_body_or_settings_changed=False,new_figure_integrated_into_paper=False,pdf_sha256=sha(O/'identification_matrix.pdf'))
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
