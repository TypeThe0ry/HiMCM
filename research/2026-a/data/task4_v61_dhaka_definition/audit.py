"""Audit role versus person counts; no model mutation."""
from pathlib import Path
import hashlib,json,re,subprocess
P=Path(__file__).resolve().parent
raw=P.parent/'task4_v59_secondary_sources/bangladesh_education2025.pdf'
b=raw.read_bytes();sha=hashlib.sha256(b).hexdigest()
assert sha=='14deea1e6379de7e6e9141f8bb8f2f4b713a772905cfdd1d99579ad7911010f8'
pages=subprocess.check_output(['pdftotext','-layout',str(raw),'-']).decode().split('\f')
block=pages[303].split('Table 4.4.2:',1)[1]+pages[304].split('Table 4.4.3:',1)[0]
rows={}
for role in ['Principal','Vice Principal','Professor','Associate Professor','Assistant Professor','Senior Lecturer','Lecturer','Demonstrator','Junior Instructor']:
    line=next(x for x in block.splitlines() if x.strip().startswith(role+' '))
    ns=list(map(int,re.findall(r'\d+',line)));rows[role]={'total':ns[2],'female':ns[3]}
assert re.search(r'1033\s+411\s+440\s+165\s+511',block)
assert re.search(r'1633\s+418\s+690\s+130\s+816',block)
rows['Library and Information Science']={'total':440,'female':165}
rows['Physical Education Teacher']={'total':690,'female':130}
assert sum(x['total'] for x in rows.values())==26590
assert sum(x['female'] for x in rows.values())==7397
amb=['Principal','Vice Principal','Demonstrator','Library and Information Science','Junior Instructor']
f_cap=sum(rows[k]['female'] for k in amb)
m_cap=sum(rows[k]['total']-rows[k]['female'] for k in amb)
assert (f_cap,m_cap)==(740,2685)
assert 'Every institution was the unit of measurement' in pages[80]
assert '20 October 2025' in pages[81] and '21 November 2025' in pages[81]
counterexample={'Principal':(1195,135),'Vice Principal':(78,19),'Demonstrator':(565,416),'Library and Information Science':(165,165),'Junior Instructor':(5,5),'Lecturer':(230,230)}
assert sum(v[0] for v in counterexample.values())==2238
assert sum(v[1] for v in counterexample.values())==970
for k,(total,female) in counterexample.items():
    assert female<=rows[k]['female'] and total-female<=rows[k]['total']-rows[k]['female']
result=dict(counterexample_role_allocation={k:dict(total=v[0],female=v[1]) for k,v in counterexample.items()},source_sha256=sha,source_pages_pdf=[29,35,81,82,215,304,305,573,575],
 city_pure_hsc=dict(institutions=95,roles=2238,female_roles=970,male_roles=1268),
 national_pure_hsc_roles=rows,ambiguous_instruction_roles=amb,
 conditional_female_role_lower=max(0,970-f_cap),conditional_male_role_lower=max(0,1268-m_cap),
 conditional_role_lower=230,conditional_unique_person_lower_if_at_most_once_per_institution=3,
 person_deduplication_verified=False,one_record_per_person_per_institution_verified=False,
 strict_instruction_headcount_lower_without_extra_assumptions=0,
 date_evidence={'intro_printed2':'20.10.2024 to21.11.2024','detailed_method_printed49':'20 October2025 to21 November2025','resolved':False},
 main_admitted=False,
 warning='230 bounds eligible instructional role records under stated role classification, not unique people. 3 additionally requires within-institution uniqueness; neither assumption verified as a source-wide rule.')
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
(P/'source_extract.txt').write_text('\n\n'.join('PDF PAGE '+str(i+1)+'\n'+pages[i] for i in [28,34,80,81,214,303,304,572,574]))
print(json.dumps({k:result[k] for k in ['conditional_role_lower','conditional_unique_person_lower_if_at_most_once_per_institution','strict_instruction_headcount_lower_without_extra_assumptions']}))
if __name__=='__main__':pass
