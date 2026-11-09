"""Reproduce source fields and reject incompatible travel definitions."""
from pathlib import Path
import argparse,csv,hashlib,io,json,re,subprocess,tempfile,zipfile
import xml.etree.ElementTree as E
from PIL import Image,ImageChops
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PAPER=ROOT.parents[2]/'HiMCM-Overleaf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--oerok-original',type=Path,default=Path('/data/datasets/HiMCM/source_archives/task4_v141_travel/oerok_original.pdf'));a=ap.parse_args()
    source={p.name:sha(p) for p in HERE.iterdir() if p.is_file() and p.name not in {'verification.json','recheck_verification.json'}}
    if (HERE/'verification.json').exists():
        for name,digest in read(HERE/'verification.json')['source_sha256'].items():assert sha(HERE/name)==digest,name
    frozen={}
    for name,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256')]:frozen.update(read(ROOT/name)[key])
    for path in ['design/task4_user_current_model.json','design/task4_user_v137_extensions.json']:frozen[path]=sha(ROOT/path)
    paper_files=[PAPER/'main.tex',PAPER/'ref.bib',PAPER/'mcmthesis.cls',PAPER/'drafts/task4_v137_paper.pdf',*[PAPER/f'drafts/task4_v137_{k}.tex' for k in ['paper','front','core','conclusion','news','ai','references']]]
    protected_paper={str(p.relative_to(PAPER)):sha(p) for p in paper_files}
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    retrievals=read(HERE/'retrievals.json');original=a.oerok_original
    assert original.stat().st_size==retrievals[2]['bytes']==47384945 and sha(original)==retrievals[2]['sha256']
    for row in retrievals[:2]:assert sha(HERE/row['file'])==row['sha256']
    for name in ['tokyo_csv_response_headers_original.txt','tokyo_xlsx_response_headers_original.txt','oerok_response_headers_original.txt']:
        codes=re.findall(rb'HTTP/[\d.]+\s+(\d+)',(HERE/name).read_bytes());assert codes and codes[-1]==b'200',name
    ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(HERE/'tokyo_timeuse_original.xlsx') as z:
        strings=[''.join(x.text or '' for x in si.findall('m:t',ns)+si.findall('m:r/m:t',ns)) for si in E.fromstring(z.read('xl/sharedStrings.xml'))]
    assert any('2021' in t and 'DAILY AVERAGE' in t for t in strings) and any('単位' in t and '分' in t for t in strings)
    rows=list(csv.DictReader(io.StringIO((HERE/'tokyo_timeuse_original.csv').read_bytes().decode('utf-8-sig'))));selected=[r for r in rows if r['男女別階層']=='0' and r['Age']=='15-19 years old'];assert len(selected)==1
    row=selected[0];saved=read(HERE/'tokyo_selected_row.json');assert row==saved['source_row']
    key=next(k for k in row if 'Commuting to and from school or work' in k)
    assert row[key]=='62' and saved['reported_combined_daily_minutes']==62
    assert saved['estimated_age_group_population_in_thousands']==530 and row['Male female classification']=='Tokyo-to'
    scope=read(HERE/'scope_audit.json');assert len(scope)==2 and all(r['status']=='not_admitted' for r in scope)
    assert read(HERE/'observations.json')==[] and scope[0]['no_halving_or_raw_utility_conversion'] and scope[1]['no_Jensen_actual_commute_bound_derived']
    assert abs(sum(scope[1]['table31_ISCED3_reported_percentages'].values())-99.99)<1e-12
    with tempfile.TemporaryDirectory(prefix='himcm_v141_verify_',dir='/data/scratch') as tmp:
        p=Path(tmp);info=subprocess.check_output(['pdfinfo',str(original)],text=True);assert re.search(r'^Pages:\s+159$',info,re.M)
        text=subprocess.check_output(['pdftotext','-layout',str(original),'-'],text=True).split('\f')
        for n in retrievals[2]['extracted_PDF_pages']:assert text[n-1]==(HERE/f'oerok_page{n:03d}_extracted.txt').read_text(),n
        assert '2021/2022' in text[15] and 'nächstgelegenen Ziel' in text[18]
        assert '8,2' in text[75] and '62,85' in text[76] and '36,96' in text[76]
        subprocess.run(['pdftoppm','-f','76','-l','77','-r','90','-png',str(original),str(p/'source')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        for n in [76,77]:assert not ImageChops.difference(Image.open(p/f'source-{n:03d}.png').convert('RGB'),Image.open(HERE/f'oerok_page{n:03d}_source.png').convert('RGB')).getbbox(),n
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    for name,digest in protected_paper.items():assert sha(PAPER/name)==digest,name
    for name,digest in source.items():assert sha(HERE/name)==digest,name
    result=dict(status='pass',primary_admissions=0,original_HTTP_bodies_verified=3,external_full_PDF_bytes=47384945,external_PDF_pages=159,external_PDF_sha256=sha(original),external_full_PDF_required_for_reproduction=True,selected_PDF_pages_reproduced=retrievals[2]['extracted_PDF_pages'],source_page_images_pixel_identical=[76,77],Tokyo_original_XLSX_and_CSV_fields_reproduced=True,no_mismatched_mean_halving_or_Jensen_conversion=True,protected_scientific_files=len(frozen),protected_manuscript_sha256=protected_paper,source_sha256=source)
    target=HERE/('recheck_verification.json' if (HERE/'verification.json').exists() else 'verification.json');target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if not isinstance(v,dict)},indent=2))
if __name__=='__main__':main()
