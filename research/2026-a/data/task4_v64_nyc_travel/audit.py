"""Verify pilot's observed scope; do not promote it to city high-school data."""
import hashlib,json,re,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
for item in json.loads((P/'manifest.json').read_text()):
 b=(P/item['file']).read_bytes()
 assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
text=subprocess.check_output(['pdftotext','-layout',str(P/'smartphone_pilot_report2022.pdf'),'-'],text=True)
pages=text.split('\f')
assert 'November 2, 2020 through November 30, 2020' in pages[4]
assert re.search(r'264\s+172\s+1,848\s+4,843\s+82,043',pages[4])
assert re.search(r'17 and under\s+25% \(66\)',pages[15])
assert 'should not use these' in pages[14] and 'results for regional analysis' in pages[14]
assert 'Work/School' in text
index=(P/'survey_index.html').read_text()
assert '2010/2011' in index and 'RHTS RFI Key Takeaways' in index
result=dict(source='NYMTC smartphone pilot report',fieldwork='2020-11-02 through 2020-11-30',
 report_date='Presentation cover May8,2021; filename FinalReport9-26-2022 is not observation year',
 total_participants=264,age17_and_under=66,travel_days=1848,recorded_trips=4843,
 source_pages_pdf=dict(overview=5,regional_analysis_warning=15,age_profile=16),
 current_high_school_by_nyc_geography_and_duration_available=False,
 regional_inference_explicitly_discouraged_by_source=True,
 source_index_currently_lists_rhts_2010_2011_and_rfi_2023=True,
 newer_rhts_public_microdata_found=False,
 cms2024_prior_audit='../task4_v20_nyc_school_survey/README.md',
 new_admitted_observations=0,changed_model_cells=0,main_admitted=False,
 conclusion='New pilot source does not establish a replacement for the historical current-high-school travel interval; preserve existing bounds and year limitation.')
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
