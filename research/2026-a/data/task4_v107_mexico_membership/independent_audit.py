"""Independent raw-record classification and exhaustive fractional-box vertex audit.
No production classifier, aggregation, or scoring functions are imported.
"""
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
from itertools import product
from math import exp
import csv, hashlib, io, json
P=Path(__file__).resolve().parent
S=P.parent/'task4_v15_mexico2020'

def extrema(fixed, uncertain):
    endpoint={'1':(exp(-.5),1.),'2':(exp(-1),exp(-.5)),
              '3':(exp(-2),exp(-1)),'4':(exp(-4),exp(-2)),
              '5':(0.,exp(-4)),'6':(0.,1.),'9':(0.,1.),'':(0.,1.)}
    assert set(fixed)|set(uncertain)<=set(endpoint)
    n=sum(fixed.values());assert n>0
    # Linear-fractional objective with positive denominator attains extrema
    # at box vertices; enumerate all inclusion subsets, without prefix sorting.
    keys=list(uncertain); candidates=[[],[]]
    for mask in product((0,1),repeat=len(keys)):
        den=n+sum(uncertain[k]*b for k,b in zip(keys,mask))
        for side in (0,1):
            num=sum(w*endpoint[k][side] for k,w in fixed.items())
            num+=sum(uncertain[k]*b*endpoint[k][side] for k,b in zip(keys,mask))
            candidates[side].append(num/den)
    return [min(candidates[0]),max(candidates[1])],2**len(keys)

def audit():
    expected=json.loads((P/'summary.json').read_text())
    for name,sha in expected['source_hashes'].items():
        assert hashlib.sha256((S/name).read_bytes()).hexdigest()==sha
    for name,needle in [('completed_grade_metadata.html','vacaciones por terminación de ciclo escolar'),('completed_grade_metadata.html','grado y nivel que acaba de aprobar')]:
        assert needle in (S/name).read_text()
    groups={k:Counter() for k in ('conditional_classified','transition_optional','optional')}
    samples=Counter();seen=set();rows=0;leading_zero_transition=0
    with ZipFile(S/'Censo2020_CA_cdmx_csv.zip') as z:
        for r in csv.DictReader(io.TextIOWrapper(z.open('Personas09.CSV'),encoding='utf-8-sig')):
            rows+=1;assert r['ENT']=='09' and r['ID_PERSONA'] not in seen;seen.add(r['ID_PERSONA'])
            w=int(r['FACTOR']);assert w>0
            age=int(r['EDAD'])
            if age!=999 and not 14<=age<=18:continue
            if r['ASISTEN'] not in ('1','9'):continue
            att,lev,gr=(int(r[k]) for k in ('ASISTEN','NIVACAD','ESCOLARI'))
            hs=lev in (4,5,7) and 0<=gr<=2
            transition=lev==3 and gr==3
            missing=lev==99 or gr==99
            if not (hs or transition or missing):continue
            if age==999 or att==9 or not (hs or transition):g='optional'
            elif hs:g='conditional_classified'
            else:
                g='transition_optional'
                leading_zero_transition+=r['ESCOLARI']=='03'
            groups[g][r['TIE_TRASLADO_ESCU']]+=w;samples[g]+=1
    assert rows==276007==expected['person_rows']
    for g,c in groups.items():
        assert dict(c)==expected['groups'][g]['weighted_time_bins']
        assert samples[g]==expected['groups'][g]['sample_rows']
        assert sum(c.values())==expected['groups'][g]['expanded_weight']
    old=json.loads((P.parent/'task4_v72_mexico/summary.json').read_text())['scopes']['age14_18']
    oldfixed=groups['conditional_classified']+groups['transition_optional']
    assert dict(oldfixed)==old['known'] and dict(groups['optional'])==old['optional']
    assert samples['conditional_classified']+samples['transition_optional']==old['n_known']
    assert samples['optional']==old['n_optional']
    before,nv0=extrema(oldfixed,groups['optional'])
    after,nv1=extrema(groups['conditional_classified'],groups['transition_optional']+groups['optional'])
    errors=[abs(x-y) for x,y in zip(before,expected['old_utility'])]+[abs(x-y) for x,y in zip(after,expected['revised_utility'])]
    errors += [abs(before[0]-old['utility_lower']),abs(before[1]-old['utility_upper'])]
    assert max(errors)<1e-14 and after[0]<=before[0] and after[1]>=before[1]
    assert leading_zero_transition==samples['transition_optional']
    return {'passed':True,'raw_rows':rows,'groups':{g:dict(sample_rows=samples[g],expanded_weight=sum(c.values())) for g,c in groups.items()},'leading_zero_grade_03_transition_rows':leading_zero_transition,'old_interval':before,'revised_interval':after,'exhaustive_vertices_per_endpoint':{'old':nv0,'revised':nv1},'max_absolute_discrepancy':max(errors),'source_sha256_verified':True,'holiday_last_approved_clause_verified':True,'method':'Independent raw CSV predicate; exhaustive inclusion-box vertices, no production imports. Positive fixed denominator makes linear-fractional box extrema attained at vertices.','interpretation':'Removes assumed progression after completed lower secondary; does not estimate a misclassification rate. Upper-secondary levels 4/5/7 grade 0–2 remain conditionally interpreted. Bounds omit sampling uncertainty; optional membership has no assigned probability.'}

if __name__=='__main__':
    result=audit();(P/'independent_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
