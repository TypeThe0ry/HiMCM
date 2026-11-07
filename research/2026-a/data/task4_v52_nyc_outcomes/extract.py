"""Extract directly published NYC county aggregates, never suppressed school cells.
Requires access-parser==0.0.6; raw source stays in the official ZIP.
"""
from pathlib import Path
import csv
import hashlib
import json
import tempfile
import zipfile
from access_parser import AccessParser

P=Path(__file__).resolve().parent
TABLE='GRAD_RATE_AND_OUTCOMES_2025'
COUNTIES={'31','32','33','34','35'}
OUTCOMES=['GRAD_CNT','NON_DIPLOMA_CREDENTIAL_CNT','STILL_ENR_CNT','GED_CNT','DROPOUT_CNT']


def integer(x):
    assert x is not None and str(x) not in ('-','')
    value=float(x)
    assert value>=0 and value.is_integer()
    return int(value)


def extract(table,mdb_sha):
    rows=[dict(zip(table,values)) for values in zip(*table.values())]
    assert len(rows)==224734
    chosen=[]; summaries={}
    for membership,label in [(11,'august2025'),(9,'june2025')]:
        selected=[r for r in rows if r['REPORT_SCHOOL_YEAR']=='2024-25'
                  and r['AGGREGATION_INDEX']=='2' and r['NYC_IND']=='1'
                  and r['MEMBERSHIP_CODE']==membership and r['subgroup_code']=='01']
        assert len(selected)==5 and {r['COUNTY_CODE'] for r in selected}==COUNTIES
        assert len({r['AGGREGATION_CODE'] for r in selected})==5
        for r in selected:
            assert r['SUBGROUP_NAME']=='All Students'
            n=integer(r['ENROLL_CNT']); y=integer(r['GRAD_CNT'])
            assert integer(r['LOCAL_CNT'])+integer(r['REG_CNT'])+integer(r['REG_ADV_CNT'])==y
            residual=n-sum(integer(r[k]) for k in OUTCOMES)
            assert residual>=0 and y<=n
            chosen.append(dict(period=label,county_code=r['COUNTY_CODE'],county=r['AGGREGATION_NAME'],
                               aggregation_code=r['AGGREGATION_CODE'],cohort=n,graduates=y,
                               unclassified_residual=residual,
                               **{k:integer(r[k]) for k in OUTCOMES[1:]}))
        n=sum(integer(r['ENROLL_CNT']) for r in selected)
        g=sum(integer(r['GRAD_CNT']) for r in selected)
        residual=n-sum(integer(r[k]) for r in selected for k in OUTCOMES)
        summaries[label]=dict(cohort=n,graduates=g,unknown_outcomes=residual,
                              lower=g/n,upper=(g+residual)/n,
                              interpretation='Upper bound assigns possible diploma outcomes to arithmetic unclassified residual; this is not an official NYSED unknown-outcome category.')
    district=[r for r in rows if r['REPORT_SCHOOL_YEAR']=='2024-25' and r['AGGREGATION_INDEX']=='1'
              and r['AGGREGATION_CODE']=='000000000001' and r['MEMBERSHIP_CODE']==11
              and r['subgroup_code']=='01']
    assert len(district)==1
    old=json.loads((P.parent/'task4_v18_nyc_quality/graduation_summary.json').read_text())['scopes']['2025']
    result=dict(main_admitted=False,table=TABLE,source_mdb_sha256=mdb_sha,source_rows=len(rows),
                scope='NYSED 2024-25 published accountability aggregates for five NYC counties: districts including homebound/OODP plus charter schools; not all resident adolescents',
                period='2021 entry cohort, four-year August 2025',**summaries['august2025'],
                nyc_counties=summaries['august2025'],
                other_period=summaries['june2025'],
                nysed_nyc_district_reference=dict(cohort=integer(district[0]['ENROLL_CNT']),graduates=integer(district[0]['GRAD_CNT'])),
                doe_v18_reference=dict(cohort=old['cohort'],graduates=old['graduates'],unknown_outcomes=old['unknown_outcomes']),
                aggregation_note='Sum only five directly published county rows. Do not sum school/borough/NRC/district tables into them or infer suppressed school outcomes.',
                metadata_note='ZIP ReadMe ENROLL_CNT prose retains stale 2023/2019 dates. Actual 2024-25 record field, membership11 and 2025 Business Rules establish 2021-entry August2025 target.',
                residual_note='Known listed statuses are retained; residual56 is conservatively unclassified. Official observed diploma fraction is G/N; residual-envelope interpretation is conditional.')
    with (P/'county_outcomes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(chosen[0]));w.writeheader();w.writerows(chosen)
    (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


def main():
    for source in json.loads((P/'manifest.json').read_text()):
        data=(P/source['file']).read_bytes()
        assert len(data)==source['bytes'] and hashlib.sha256(data).hexdigest()==source['sha256']
    with zipfile.ZipFile(P/'gradrate_2025.zip') as z, tempfile.TemporaryDirectory() as d:
        name=next(n for n in z.namelist() if n.endswith('.mdb'))
        raw=z.read(name);path=Path(d)/'source.mdb';path.write_bytes(raw)
        table=AccessParser(str(path)).parse_table(TABLE)
        extract(table,hashlib.sha256(raw).hexdigest())


if __name__=='__main__':main()
