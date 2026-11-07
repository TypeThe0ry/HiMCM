"""Recover official 2015 upper-secondary travel bins directly from CDMX microdata.

No guessed chart colors, midpoint times, half-roundtrip assumption, or missing deletion.
"""
from pathlib import Path
from zipfile import ZipFile
from math import exp
from collections import Counter
import csv, io, json, hashlib
P=Path(__file__).resolve().parent
SOURCE='https://www.inegi.org.mx/contenidos/programas/intercensal/2015/microdatos/eic2015_09_csv.zip'

def main():
    for r in json.loads((P/'manifest.json').read_text()):
        if r.get('sha256'):
            assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    # Preserve and validate the actual question wording and codebook, not a guessed metric.
    for name,expected in [('school_time_metadata.html',['Hasta 15 minutos','No se traslada','No especificado']),
                          ('education_level_metadata.html',['NIVACAD','Preparatoria o bachillerato general']),
                          ('school_attendance_metadata.html',['ASISTEN']),('factor_metadata.html',['FACTOR'])]:
        text=(P/name).read_text()
        assert all(s in text for s in expected),(name,expected)
    weighted=Counter(); sample=Counter(); municipalities=Counter(); grades=Counter()
    all_attenders=0; all_rows=0; weighted_all=0
    with ZipFile(P/'eic2015_09_csv.zip') as z:
        assert 'TR_PERSONA09.CSV' in z.namelist()
        for row in csv.DictReader(io.TextIOWrapper(z.open('TR_PERSONA09.CSV'),encoding='latin1')):
            all_rows+=1; assert row['ENT']=='09'
            w=int(row['FACTOR']);assert w>0
            weighted_all+=w
            if not row['EDAD'].isdigit() or not 3<=int(row['EDAD'])<=17 or row['ASISTEN']!='5':continue
            all_attenders+=w
            level=int(row['NIVACAD']); grade=int(row['ESCOLARI'])
            # Last completed level/grade. Reconstruct the currently attended stage;
            # exact five-bin agreement with official Evalua2015 EMS tabulation is audited.
            ems=(level==3 and grade==3) or (level in (4,5,7) and grade<3)
            if not ems:continue
            code=row['TIE_TRASLADO_ESCU']
            assert code in ('1','2','3','4','5','6','9')
            weighted[code]+=w;sample[code]+=1
            municipalities[row['MUN']]+=w;grades[(level,grade)]+=w
    official=[39240,79954,77881,29661,2231]
    assert [weighted[str(i)] for i in range(1,6)]==official
    assert all_attenders==1645951
    assert weighted['6']==640 and weighted['9']==8857
    assert sum(weighted.values())==238464
    lower_minutes=[0,15,30,60,120]; upper_minutes=[15,30,60,120,None]
    records=[]; numer_lo=0; numer_hi=0
    for i,(a,b) in enumerate(zip(lower_minutes,upper_minutes),1):
        ul=exp(-b/30) if b is not None else 0.;uh=exp(-a/30)
        n=weighted[str(i)];numer_lo+=n*ul;numer_hi+=n*uh
        records.append(dict(code=i,weighted_students=n,sample_rows=sample[str(i)],minutes_lower=a,
                            minutes_upper=b,utility_lower=ul,utility_upper=uh))
    # Code6 remote/no trip is a structural absence, not a measured zero-minute trip.
    # Keep it [0,1], together with nonresponse, to preserve the same population as V6.
    unknown=weighted['6']+weighted['9'];N=sum(weighted.values())
    lo=numer_lo/N;hi=(numer_hi+unknown)/N
    for code,why in [('6','No se traslada: no school trip, often remote learning'),('9','Duration not specified')]:
        records.append(dict(code=int(code),weighted_students=weighted[code],sample_rows=sample[code],
                            minutes_lower=None,minutes_upper=None,utility_lower=0,utility_upper=1))
    with (P/'travel_bins.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
    old=next(csv.DictReader((P.parent/'task4_v6_commute/bounds.csv').open()))
    assert old['city']=='Mexico City' and float(old['utility_lower'])<=lo<=hi<=float(old['utility_upper'])
    row=dict(city='Mexico City',indicator='travel',utility_lower=lo,utility_upper=hi,year=2015,
        source_url=SOURCE,
        scope='CDMX/Distrito Federal private-household residents age3–17; attending reconstructed upper-secondary stage; FACTOR weighted; exact reproduction of official EMS time bins; household-proxy reported direct home-to-school time; 640 no-trip and8857 unspecified remain [0,1]; historical2015',
        status='observed_official_microdata_school_travel_bound',mapping_robust=True,
        extraction='archived_official_microdata_and_codebooks',raw_data_archived=True,
        raw_pdf_archived=False,reported_students=sum(official),unknown_duration_students=unknown)
    with (P/'bounds.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=row.keys());w.writeheader();w.writerow(row)
    audit=dict(person_rows=all_rows,weighted_private_household_population=weighted_all,
        age3_17_attenders=all_attenders,upper_secondary_population=N,
        upper_secondary_sample_rows=sum(sample.values()),weighted_time_code_counts=dict(weighted),
        source_chart_bins_exact_match=official,all_16_municipalities=len(municipalities),
        weighted_school_stage_groups={f'NIVACAD={a};ESCOLARI={b}':n for (a,b),n in sorted(grades.items())},
        old_lower=float(old['utility_lower']),old_upper=float(old['utility_upper']),new_lower=lo,new_upper=hi,
        nested=True,notes=['No design-based confidence interval estimated','Current stage reconstructed from completed grade; matches official EMS tabulation exactly','Remote/nonresponse not discarded or assigned midpoint','No comparison of new years assumed nested'])
    (P/'extraction_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    assert len(municipalities)==16 and sum(r['weighted_students'] for r in records)==N
    # Endpoint arithmetic and all-bin Monte Carlo containment check, deterministic seed.
    import random
    rng=random.Random(2015)
    for _ in range(1000):
        s=sum(r['weighted_students']*rng.uniform(r['utility_lower'],r['utility_upper']) for r in records)/N
        assert lo-1e-12<=s<=hi+1e-12
    print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
