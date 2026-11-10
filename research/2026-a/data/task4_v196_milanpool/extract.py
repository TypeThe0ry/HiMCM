"""Independent original-PDF check of frozen Milan tariff venue subset."""
from pathlib import Path
import hashlib,json,re,subprocess
P=Path(__file__).resolve().parent
OLD=P.parent/'task4_v118_pools'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return re.sub(r'\s+','',s.upper().replace('’',"'"))
def main():
 meta=json.loads((P/'retrieval.json').read_text());pdf=P/'tariff_original.pdf'
 assert pdf.read_bytes().startswith(b'%PDF') and pdf.stat().st_size==meta['bytes'] and sha(pdf)==meta['sha256']
 raw=subprocess.check_output(['pdftotext','-raw',str(pdf),'-']).decode();compact=norm(raw)
 a=re.findall(r'VALIDANELLEPISCINE(ARIOLIVENEGONI-[A-Z\'-]+SUZZANI)',compact)
 b=re.findall(r'VALIDANELLEPISCINE(BACONE-COZZI-PROCIDA-SOLARI)',compact)
 assert len(a)==len(b)==2 and len(set(a))==len(set(b))==1
 names_a=a[0].split('-');names_b=b[0].split('-');names=names_a+names_b
 assert len(names_a)==13 and len(names_b)==4 and len(set(names))==17
 obs=next(r for r in json.loads((OLD/'observations.json').read_text()) if r['city']=='Milan')
 assert set(names)=={norm(n) for n in obs['venues']} and obs['raw_count']==17
 frozen=json.loads((OLD/'milan_provider_capture.json').read_text())
 text='\n'.join(c.get('text','') for c in frozen['result']['content'])
 assert all(n in norm(text) for n in names)
 layout=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode()
 assert 'IN VIGORE DAL 1 GIUGNO 2025' in layout
 assert 'aggiornato al 9 settembre 2025' in layout
 report=dict(status='pass',role='Evidence representation and source metadata verification; no admission or model update',named_count=17,tariff_A_count=13,tariff_B_count=4,normalized_names=names,frozen_venue_set_identical=True,population_retained=obs['population'],population_year_retained=obs['population_year'],utility_bound_retained=obs['utility_after'],tariff_effective_date='2025-06-01',printed_update_date='2025-09-09',filename_contains='agg-9-10-2025',date_conflict='The URL filename does not match the printed document update month; use the printed September date for the retrieved document, without inferring a URL upload date.',original_bytes_in_frozen_V118_package=False,previous_representation='Provider-extracted text',current_representation='HTTP200 original PDF bytes; metadata and 17 venue names checked from PDF',visual_inspection='Single page rendered at1800px and viewed; bottom-right date and venue lists legible',source_sha256={p.name:sha(p) for p in [pdf,P/'retrieval.json',Path(__file__)]},historical_source_sha256={p.name:sha(p) for p in [OLD/'observations.json',OLD/'milan_provider_capture.json',OLD/'manifest.json']},primary_admissions=0,actual_score_width_reduction=0,limits='Named tariff subset, not complete city inventory, current continuous operation, teenager access, or original population verification.')
 (P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ['source_sha256','historical_source_sha256','normalized_names']},indent=2))
if __name__=='__main__':main()
