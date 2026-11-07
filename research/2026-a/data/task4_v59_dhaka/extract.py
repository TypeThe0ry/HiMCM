"""Extract city counts and national contamination caps from BANBEIS originals."""
import hashlib,json,re,subprocess
from pathlib import Path
import pandas as pd

P=Path(__file__).resolve().parent
SOURCE=P.parent/'task4_v59_secondary_sources/bangladesh_education2025.pdf'

def main():
    raw=SOURCE.read_bytes()
    text=subprocess.check_output(['pdftotext','-layout',str(SOURCE),'-']).decode()
    pages=text.split('\f');city=pages[214]
    assert 'Dhaka' in city and 'City Total' in city
    # Table 4.1.10, PDF215/printed182, Total rows within the Dhaka city block.
    values=[('school_college_section',170,26,4837,1991,103904,55627),
            ('higher_secondary_college',95,4,2238,970,37191,17425),
            ('degree_pass',11,2,396,186,12965,2755),
            ('degree_honors',22,6,967,462,36057,15138),
            ('masters',36,14,3578,2105,236783,122682),
            ('city_total',334,52,12016,5714,426900,213627)]
    for name,*numbers in values:
        pattern=r'\bTotal\s+'+r'\s+'.join(map(str,numbers))+r'\b'
        assert re.search(pattern,city),(name,numbers)
    cols=['program','institutions','girls_institutions','teacher_roles','female_teacher_roles','students','girls']
    frame=pd.DataFrame(values,columns=cols)
    for col in cols[1:]:assert frame.iloc[:-1][col].sum()==frame.iloc[-1][col]
    frame.to_csv(P/'city_college_counts.csv',index=False)
    # National same-category cross-tab: the first two Total rows after heading.
    national=pages[296].split('Table 4.3.3:',1)[1]
    total_lines=[line for line in national.splitlines() if re.match(r'^\s*Total\s+\d',line)]
    school=[int(n) for n in re.findall(r'\d+',total_lines[0])]
    pure=[int(n) for n in re.findall(r'\d+',total_lines[1])]
    assert school==[401970,218775,152,3,601,256,0,0,402723,219034,1556,219]
    assert pure==[375288,199368,0,0,0,0,0,0,375288,199368,1434,212]
    contamination=sum(school[k] for k in [2,4,6]);assert contamination==753
    assert school[0]+contamination==school[8]
    roles=pages[303].split('Table 4.4.2:',1)[1]
    caps={}
    for role in ['Principal','Vice Principal']:
        line=next(s for s in roles.splitlines() if s.strip().startswith(role+' '))
        nums=[int(n) for n in re.findall(r'\d+',line)]
        caps[role]=nums[2]
    assert caps=={'Principal':1195,'Vice Principal':78}
    nmin=37191+max(0,103904-contamination);nmax=426900
    tmin=max(0,2238-sum(caps.values()));tmax=12016
    assert (nmin,nmax,tmin,tmax)==(140342,426900,965,12016)
    result=dict(source_edition=2025,table='4.1.10',pdf_page=215,printed_page=182,
        geography='Source-defined Dhaka City Corporation area; boundary crosswalk unverified',
        school_college_non_hsc_national_cap=contamination,
        national_pure_hsc_head_roles=caps,known_pure_hsc_teacher_roles=2238,
        students_lower=nmin,students_upper=nmax,teachers_lower=tmin,teachers_upper=tmax,
        education_lower=15*tmin/(nmax+15*tmin),education_upper=15*tmax/(nmin+15*tmax),
        reported_role_lower=15*2238/(nmax+15*2238),
        target='General higher-secondary provision in listed college institutions, grades11-12; not all14-18residents, madrasa or technical streams',
        date_caveat='2025 edition and table labels; methods prints collection20Oct2024-21Nov2024. Actual census date not resolved.',
        source_sha256=hashlib.sha256(raw).hexdigest(),source_bytes=len(raw),
        national_values_used_as_city_estimates=False)
    (P/'observation.json').write_text(json.dumps(result,indent=2)+'\n')
    manifest=[dict(file='../task4_v59_secondary_sources/bangladesh_education2025.pdf',
        bytes=len(raw),sha256=result['source_sha256'],
        url='https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-banbeis/2026/8/3ad8a7f7-d233-4753-b8cc-7a6f69f4e80e.pdf')]
    (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
