"""Exact Ministry school-ID joins; counts-only participant-weighted results."""
import csv,io,json,zipfile,collections
from pathlib import Path
P=Path(__file__).resolve().parent
with (P.parent/'task4_v40_toronto/toronto_secondary_roster.csv').open() as f:
    roster={r['School Number'].zfill(6):r for r in csv.DictReader(f) if r['Board Number'] in {'B66052','B67059','B66303','B67318'}}
assert len(roster)==155
specs=[('grade9','Grade-9-2024-2025-Achievement-Results.zip','G9_2025.csv','cntOverallM_L34','cntStudents_All'),('osslt_first_time','OSSLT-2024-2025-Achievement-Results.zip','G10_2025_FTE.csv','cntSuccessful','cntEligible')]
summary={}
for label,archive,member,num,eligible in specs:
    with zipfile.ZipFile(P/archive) as z:
        name=next(n for n in z.namelist() if n.endswith('/'+member))
        rows=list(csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig'))))
    schools=[r for r in rows if r['OrgType']=='S']
    ids=[r['SchoolMident'].zfill(6) for r in schools];assert len(set(ids))==len(ids)
    byid=dict(zip(ids,schools));matched=[];usable=[];missing=[]
    for sid,s in roster.items():
        if sid not in byid:missing.append(sid);continue
        r=byid[sid]
        assert 'B'+r['BoardMident']==s['Board Number'],(sid,r['BoardMident'],s['Board Number'])
        assert r['ApplySuppression']=='1'
        if label=='osslt_first_time':assert r['Administration']=='Overall' and r['Eligibility']=='1'
        matched.append(r)
        if r['Suppressed']=='0' and r[num].isdigit() and r['cntFullyParticipating'].isdigit():
            n,d=int(r[num]),int(r['cntFullyParticipating']);assert r[eligible].isdigit()
            ee=int(r[eligible]);assert 0<=n<=d<=ee
            if label=='grade9':assert ee==d+int(r['cntNoData'])
            else:assert ee==sum(int(r[k]) for k in ['cntFullyParticipating','cntAbsent','cntDeferred','cntOSSLC','cntInsufficientEvidence'])
            if d>0:usable.append(r)
    n=sum(int(r[num]) for r in usable);d=sum(int(r['cntFullyParticipating']) for r in usable)
    e=sum(int(r[eligible]) for r in usable if r[eligible].isdigit())
    with (P/(label+'_matched.csv')).open('w',newline='') as f:
        keys=['SchoolMident','SchoolName','BoardMident','BoardName','Language','FundingType','Suppressed',eligible,'cntFullyParticipating',num]
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:r[k] for k in keys} for r in matched)
    with (P/(label+'_unmatched_roster.csv')).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['School Number','School Name','Board Number']);w.writeheader();w.writerows({k:roster[sid][k] for k in w.fieldnames} for sid in missing)
    summary[label]={'target_school_count':155,'matched_school_count':len(matched),'usable_school_count':len(usable),'matched_suppression_codes':dict(collections.Counter(r['Suppressed'] for r in matched)),'unmatched_school_count':len(missing),'success_count':n,'fully_participating_count':d,'participant_weighted_success_percent':100*n/d,'eligible_or_allstudents_count_in_usable_schools':e,'schools_with_numeric_eligible_count':sum(r[eligible].isdigit() for r in usable),'numerator_field':num,'denominator_field':'cntFullyParticipating','population':'Fully participating students in matched, publicly reportable four-board Toronto secondary schools; not all city pupils','main_model_admission':False}
    summary[label]['nonparticipation_diagnostic']={'status':'conditional_latent_outcome_bounds_not_official_observed_rate','target':'Same usable schools only; registered Grade9 or first-time-eligible OSSLT cohort','registered_or_eligible_E':e,'fully_participating_P':d,'observed_success_Y':n,'unknown_outcome_count':e-d,'lower_percent':100*n/e,'upper_percent':100*(n+e-d)/e,'formula':'[Y/E, (Y+E-P)/E]','assumption':'Every non/partially participating eligible student has a well-defined binary potential outcome under completion of the same assessment; observed fully participating outcomes are held fixed. No missing-at-random assumption.','excluded':'Unmatched/privacy-suppressed schools and Grade9 nonregistered pupils. OSSLT exempt counts are not added to E.','per_school_checks':'Y <= P <= E; Grade9 E=P+cntNoData; OSSLT E=P+Absent+Deferred+OSSLC+InsufficientEvidence','main_model_admission':False}
    if label=='osslt_first_time':summary[label]['nonparticipation_diagnostic']['separately_reported_exempt_not_added_to_E']=sum(int(r['cntExempt']) for r in usable)
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
