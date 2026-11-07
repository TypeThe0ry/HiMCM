"""Read-only audit of V41 sources; writes only this audit directory."""
import csv,io,json,zipfile,collections,hashlib
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parent;V=P.parent/'task4_v41_toronto'
def readmember(archive,member):
    with zipfile.ZipFile(V/archive) as z:return list(csv.DictReader(io.StringIO(z.read(next(n for n in z.namelist() if n.endswith('/'+member))).decode('utf-8-sig'))))
g9=readmember('Grade-9-2024-2025-Achievement-Results.zip','G9_2025.csv')
g10=readmember('OSSLT-2024-2025-Achievement-Results.zip','G10_2025_FTE.csv')
pe={r['SchoolMident']:r for r in readmember('OSSLT-2024-2025-Achievement-Results.zip','G10_2025_PE.csv') if r['OrgType']=='S'}
saved=json.loads((V/'summary.json').read_text());report={};cross=[]
for name,rows,num,elig in [('grade9',g9,'cntOverallM_L34','cntStudents_All'),('osslt_first_time',g10,'cntSuccessful','cntEligible')]:
    target={r['SchoolMident'] for r in csv.DictReader((V/(name+'_matched.csv')).open()) if r['Suppressed']=='0'}
    rr=[r for r in rows if r['OrgType']=='S' and r['SchoolMident'] in target];assert len(rr)==len(target)
    for r in rr:
        y,p,e=map(int,(r[num],r['cntFullyParticipating'],r[elig]));assert 0<=y<=p<=e
        if name=='grade9':
            assert y==int(r['cntOverallM_L3'])+int(r['cntOverallM_L4'])
            assert p==sum(int(r[k]) for k in ['cntOverallM_L1','cntOverallM_L2','cntOverallM_L3','cntOverallM_L4','cntOverallM_NE1'])
            assert e==p+int(r['cntNoData'])
        else:
            assert r['Administration']=='Overall' and r['Eligibility']=='1'
            assert p==y+int(r['cntNotSuccessful'])
            assert e==p+sum(int(r[k]) for k in ['cntAbsent','cntDeferred','cntOSSLC','cntInsufficientEvidence'])
    Y=sum(int(r[num]) for r in rr);N=sum(int(r['cntFullyParticipating']) for r in rr);E=sum(int(r[elig]) for r in rr);U=E-N
    lo,hi=Fraction(Y,E),Fraction(Y+U,E)
    assert lo<=Fraction(Y,N)<=hi
    assert abs(float(lo)*100-saved[name]['nonparticipation_diagnostic']['lower_percent'])<1e-10
    assert abs(float(hi)*100-saved[name]['nonparticipation_diagnostic']['upper_percent'])<1e-10
    # Unknown result count can be any integer 0..U; check all feasible completions.
    assert all(lo<=Fraction(Y+k,E)<=hi for k in range(U+1))
    unmatched=list(csv.DictReader((V/(name+'_unmatched_roster.csv')).open()))
    hits=[]
    for r in unmatched:
        sid=r['School Number'];other=pe.get(sid)
        if other:
            assert other['Eligibility']=='2' and other['Administration']=='Overall'
            hits.append(other)
            cross.append({'missing_assessment':name,'school_number':sid,'roster_school_name':r['School Name'],'present_in':'2024-25 OSSLT previously eligible Overall','previously_eligible_suppressed_code':other['Suppressed'],'interpretation':'Same-year school record exists; not evidence of school closure; wrong cohort for V41 numerator.'})
    report[name]={'verified_school_count':len(rr),'Y':Y,'P':N,'E':E,'unknown':U,'lower_exact':str(lo),'upper_exact':str(hi),'checked_binary_completion_counts':U+1,'participant_rate_within_bounds':True,'unmatched_count':len(unmatched),'unmatched_present_in_sameyear_PE':len(hits),'PE_record_suppression_codes':dict(collections.Counter(r['Suppressed'] for r in hits))}
with (P/'unmatched_other_cohort.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(cross[0]));w.writeheader();w.writerows(cross)
report['decision']='No numerical bug found. Conditional completion bounds only; no causal or full-city claim. Do not replace missing first-time/Grade9 records with previously-eligible results.'
(P/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
(P/'source_hashes.json').write_text(json.dumps({str(f.relative_to(P.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [V/'summary.json',V/'aggregate.py',V/'Grade-9-2024-2025-Achievement-Results.zip',V/'OSSLT-2024-2025-Achievement-Results.zip']},indent=2)+'\n')
print(json.dumps(report,indent=2))
