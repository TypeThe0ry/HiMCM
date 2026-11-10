"""Summarize visible public DBH campus/mode records; no provider-total inference."""
from pathlib import Path
from collections import Counter
import csv,json,hashlib
D=Path(__file__).resolve().parent
def rows(p,delimiter=','):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=delimiter))
def key(r):return tuple(r[k] for k in ['Årstall','Semester','Institusjonskode','Stedkode campus'])
def main():
    campus=rows(D/'api_662.csv');enrol=rows(D/'enrolment_response.csv',';')
    assert len(enrol)==203 and all(r['Kommunenummer campus']=='0301' for r in enrol)
    lookup={key(r):r for r in campus};assert len(lookup)==len(campus)
    out=[]
    for r in enrol:
        assert r['Antall'].isdigit()
        k=key(r);match=lookup.get(k)
        assert match is not None and match['Kommunenummer campus']=='0301',k
        out.append(dict(r,registry_key_match=True,positive_public_value=int(r['Antall'])>0,
                        institution_or_study_site_mode=r['Organisering_kode'] in ['1','4']))
    with (D/'enrolment_classified.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]),lineterminator='\n');w.writeheader();w.writerows(out)
    periods=[]
    for year,semester in [('2025','1'),('2025','3'),('2026','1'),('2026','3')]:
        er=[r for r in enrol if (r['Årstall'],r['Semester'])==(year,semester)]
        cr=[r for r in campus if (r['Årstall'],r['Semester'],r['Kommunenummer campus'])==(year,semester,'0301')]
        ids={r['Institusjonskode'] for r in er};registered={r['Institusjonskode'] for r in cr}
        positive={r['Institusjonskode'] for r in er if int(r['Antall'])>0}
        site={r['Institusjonskode'] for r in er if int(r['Antall'])>0 and r['Organisering_kode'] in ['1','4']}
        periods.append(dict(year=int(year),semester=int(semester),campus_registry_rows=len(cr),registry_distinct_institution_codes=len(registered),
                            enrolment_rows=len(er),returned_institution_codes=len(ids),positive_any_mode_codes=len(positive),
                            positive_mode1_or4_codes=len(site),registry_codes_not_returned=sorted(registered-ids),
                            positive_any_mode_code_list=sorted(positive),positive_mode1_or4_code_list=sorted(site)))
    modes=sorted({(r['Organisering_kode'],r['Organisering']) for r in enrol})
    summary=dict(scope='Counts of visible DBH records and distinct reported codes, not complete Oslo HE-provider totals or unrounded student counts.',
                 enrolment_rows=len(enrol),periods=periods,mode_labels=dict(modes),
                 site_mode_filter=['1','4'],other_modes_not_assumed_nonphysical=True,
                 privacy_GDPR_metadata_flag=1,exact_query_privacy_transformation_verified=False,
                 municipal_inventory_verified=False,original25_lineage_verified=False,
                 primary_admissions=0,actual_primary_width_reduction=0,
                 source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'api_662.csv',D/'api_002.csv',D/'enrolment_response.csv',D/'enrolment_query.json',Path(__file__)]})
    (D/'enrolment_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in p.items() if not k.endswith('list')} for p in periods]))
if __name__=='__main__':main()
