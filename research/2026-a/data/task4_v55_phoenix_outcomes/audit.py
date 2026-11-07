"""Verify directly reported PXU district cohort; do not sum overlapping subgroups."""
from pathlib import Path
import hashlib,json,subprocess,csv
P=Path(__file__).resolve().parent

def main():
    for item in json.loads((P/'manifest.json').read_text()):
        raw=(P/item['file']).read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    rows=json.loads((P/'pxu_graduation_fy2025.json').read_text())
    assert all(r['fiscalYear']==2025 and r['educationOrganizationId']==4286 for r in rows)
    assert len({r['studentGroupDescription'] for r in rows})==len(rows)
    groups={r['studentGroupDescription']:r for r in rows}
    row=groups['All'];n,g=row['numInCohort'],row['numGraduated']
    assert n==6285 and g==4813 and 0<=g<=n
    # Sex rows provide an independent total check, never extra aggregate records.
    assert groups['Female']['numInCohort']+groups['Male']['numInCohort']==n
    assert groups['Female']['numGraduated']+groups['Male']['numGraduated']==g
    assert json.loads((P/'pxu_graduation_fy2026.json').read_text())==[]
    entity=json.loads((P/'pxu_entity_requested2025.json').read_text())
    assert len(entity)==1 and entity[0]['educationOrganizationId']==4286
    assert entity[0]['entityType']=='LEA' and entity[0]['nces']=='0406330'
    assert entity[0]['fiscalYear']==2026
    js=(P.parent/'task4_v9_phoenix/app.min.js').read_text()
    marker='this.fourYearGraduationRate.barChart.title="Graduation Rate: "'
    start=js.index(marker);snippet=js[start:start+220]
    assert 'parseInt(n.data[0].fiscalYear-1)' in snippet
    text=subprocess.check_output(['pdftotext','-layout',str(P/'pxu_fact_sheet2025.pdf'),'-'],text=True)
    assert '23 Schools Total' in text and '1 Digital Academy' in text
    digital_rows=json.loads((P/'../task4_v9_phoenix/spatial_responses/875776.json').read_text())
    digital=next(r for r in digital_rows if r['studentGroupDescription']=='All')
    assert digital['fiscalYear']==2025 and digital['educationOrganizationId']==875776
    assert (digital['numInCohort'],digital['numGraduated'])==(485,286)
    with (P/'../task4_v42_phoenix_coverage/arizona_school_audit.csv').open() as handle:
        district_schools=[r for r in csv.DictReader(handle) if r['LEAID']=='0406330']
    assert len(district_schools)==21
    assert all(r['within_current_phoenix_boundary']=='True' for r in district_schools)
    assert sum(r['nonvirtual']=='False' for r in district_schools)==1
    result=dict(entity_id=4286,nces_lea='0406330',entity_name=entity[0]['nameOfInstitution'],
        requested_fiscal_year=2025,graduation_returned_fiscal_year=2025,entity_returned_fiscal_year=2026,
        cohort_year=2024,period='four-year',cohort=n,graduates=g,known_non_graduates=n-g,
        observed_district_rate=g/n,published_integer_percent=row['gradRate'],
        scope='Direct PXU LEA administrative aggregate, not all Phoenix city residents or the earlier physical-school union',
        frontend_title_excerpt=snippet,fy2026_graduation_rows=0,
        fact_sheet_scope=dict(schools=23,digital_academies=1,profile_label='2024-2025'),
        digital_academy=dict(entity_id=875776,cohort=485,graduates=286,non_graduates=199),
        current_nces_district_schools=len(district_schools),
        subtraction_route=dict(admitted=False,hypothetical_graduates_lower=g-286,
            hypothetical_non_graduates_lower=n-g-199,
            reason='Requires complete cohort-era excluded-school set and consistent unique-person district/school status; current NCES21 versus profile23 is unreconciled.'),
        main_admitted=False,city_bound_changed=False,
        limitations=['District aggregate includes broader provision, including a digital academy; no city-resident membership or physical-school-only cohort established.',
        'No claim that all earlier city school records are disjoint or that published district counts certify their linkage.',
        'Fact sheet enrollment25108 is not the graduation cohort denominator; its76.5% is not substituted for this exact API ratio.',
        'FY2026 empty response is unavailable data, not zero graduates.'])
    (P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['cohort_year','cohort','graduates','known_non_graduates','observed_district_rate','main_admitted']},indent=2))
if __name__=='__main__':main()
