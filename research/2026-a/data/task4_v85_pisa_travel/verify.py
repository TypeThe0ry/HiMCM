"""Audit archived final instruments; keyword checks do not prove global absence."""
from pathlib import Path
import hashlib,json,subprocess,zipfile,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
for item in json.loads((HERE/'manifest.json').read_text()):
    raw=(HERE/item['file']).read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
txt=subprocess.check_output(['pdftotext','-layout',str(HERE/'wellbeing2018.pdf'),'-'],text=True)
assert 'WB178' in txt and 'WB032' in txt and 'WB155' in txt
assert 'commut' not in txt.lower() and 'travel' not in txt.lower()
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(HERE/'codebook2018.xlsx') as z:
    assert z.testzip() is None
    shared=[''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
    rows=ET.fromstring(z.read('xl/worksheets/sheet2.xml')).findall('m:sheetData/m:row',ns)
    labels={}
    for row in rows:
        cells={}
        for c in row:
            v=c.find('m:v',ns);value='' if v is None else v.text
            if c.attrib.get('t')=='s':value=shared[int(value)]
            cells[''.join(x for x in c.attrib['r'] if x.isalpha())]=value
        if cells.get('A') and cells.get('B') and cells['A']!='NAME':labels[cells['A']]=cells['B']
assert labels['ST001D01T']=='Student International Grade (Derived)'
travel_terms=['commut','travel time','journey time','way to school','transportation','distance to home']
matched={k:v for k,v in labels.items() if any(t in v.lower() for t in travel_terms)}
duration_candidates={k:v for k,v in labels.items() if any(t in v.lower() for t in ['commut','travel time','journey time'])}
assert not duration_candidates
study_time={k:v for k,v in labels.items() if 'how long did you study' in v.lower()}
assert len(study_time)==4
result=dict(survey_year=2018,student_variable_labels_checked=len(labels),grade_variable='ST001D01T',transport_related_fields=matched,commute_duration_candidates=duration_candidates,study_duration_field_names=list(study_time),wellbeing_final_instrument_contains_commute_duration=False,main_admitted=False,interpretation='No actual commute-duration field identified in these archived final instruments. Study-time fields, parent transport barriers and cognitive-item timing are not school journey duration. This audit does not exclude national supplements or other surveys.')
(HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
