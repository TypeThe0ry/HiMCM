"""Conditional integer bounds from rounded SIMCE school percentages.

Assumptions: reported test-taker count is the percentage denominator and published
one-decimal percentages are nearest-rounded. Endpoints include both half ties.
Neither assumption is upgraded to an identified population fact by a good fit.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'task4_v88_pisa_regions'
LEVELS=('ins','ele','ade')


def integer_ranges(n, percentages):
    if n <= 0 or n != int(n):
        raise ValueError('Positive integer denominator required')
    n=int(n)
    p=np.asarray(percentages,dtype=float)
    if p.shape != (3,) or not np.isfinite(p).all() or np.any((p<0)|(p>100)):
        raise ValueError('Invalid level percentages')
    q=np.rint(10*p).astype(int)
    if not np.allclose(q/10,p,atol=1e-10,rtol=0):
        raise ValueError('Expected tenths of a percent')
    # 2000*k lies between (2*q-1)*n and (2*q+1)*n, inclusively.
    lower=[max(0,((2*int(v)-1)*n+1999)//2000) for v in q]
    upper=[min(n,((2*int(v)+1)*n)//2000) for v in q]
    if any(l>u for l,u in zip(lower,upper)) or sum(lower)>n or sum(upper)<n:
        return None
    coupled_lower=[max(lower[k], n-sum(upper[h] for h in range(3) if h!=k)) for k in range(3)]
    coupled_upper=[min(upper[k], n-sum(lower[h] for h in range(3) if h!=k)) for k in range(3)]
    return coupled_lower,coupled_upper


def main():
    manifest=json.loads((SOURCE/'simce_members.json').read_text())
    filename='simce2m2024_rbd_final.csv'
    path=SOURCE/filename
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest==manifest[filename]['sha256']
    data=pd.read_csv(path,sep=';',encoding='latin1')
    rows=[];audit=[];results=[]
    for subject in ('lect','mate'):
        status_counts={};city=[]
        for row in data.to_dict('records'):
            n=row[f'nalu_{subject}2m_rbd']
            p=[row[f'palu_eda_{k}_{subject}2m_rbd'] for k in LEVELS]
            finite=np.isfinite([n,*p]).all() and n>0
            allzero=finite and all(v==0 for v in p)
            reconstructed=integer_ranges(n,p) if finite and not allzero else None
            status=('missing' if not finite else 'all_zero_uninterpreted' if allzero else 'compatible' if reconstructed else 'incompatible')
            status_counts[status]=status_counts.get(status,0)+1
            if row['cod_com_rbd'] != 13101:
                continue
            assert finite,'This observed-cohort calculation needs every selected reported denominator'
            flag=row[f'marca_{subject}2m_rbd']
            usable=status=='compatible' and pd.isna(flag)
            # Keep every listed pupil in the target observed-test cohort denominator.
            n=int(n)
            if usable:
                lower,upper=reconstructed
            else:
                lower,upper=[0]*3,[n]*3
            rec=dict(subject=subject,rbd=int(row['rbd']),n=n,status=status,quality_flag=None if pd.isna(flag) else str(flag),
                used_percentages=usable,at_least_elementary_lower=n-upper[0],at_least_elementary_upper=n-lower[0],
                adequate_lower=lower[2],adequate_upper=upper[2])
            rows.append(rec);city.append((rec,p))
        audit.append(dict(subject=subject,school_records=len(data),statuses=status_counts))
        n_total=sum(r['n'] for r,p in city)
        unknown=sum(r['n'] for r,p in city if not r['used_percentages'])
        item=dict(subject=subject,schools=len(city),reported_test_takers=n_total,
            unknown_quality_or_zero_pupils=unknown,
            unique_reconstructed_schools=sum(r['used_percentages'] and r['adequate_lower']==r['adequate_upper'] and r['at_least_elementary_lower']==r['at_least_elementary_upper'] for r,p in city),
            omitted_unknown_cohort_fraction=unknown/n_total)
        for outcome in ('at_least_elementary','adequate'):
            a=sum(r[f'{outcome}_lower'] for r,p in city)
            b=sum(r[f'{outcome}_upper'] for r,p in city)
            item[outcome]=dict(count_lower=a,count_upper=b,proportion_lower=a/n_total,proportion_upper=b/n_total)
        item['naive_zero_and_flags_included_adequate']=sum(r['n']*p[2]/100 for r,p in city)/n_total
        item['interpretation']='Conditional rounded-count bounds for listed test-takers; not sampling confidence limits, resident/enrolled cohort coverage, or cross-test proficiency equivalence.'
        results.append(item)
    pd.DataFrame(rows).to_csv(HERE/'school_count_bounds.csv',index=False)
    result=dict(main_admitted=False,source_sha256=digest,source=str(path.relative_to(HERE.parent)),
        denominator_assumption='nalu test-takers equal the denominator of the three published proficiency percentages',
        rounding_assumption='Nearest rounding to0.1percentagepoint; half ties allowed at both endpoints',
        aggregate_scope='Santiago school commune13101, Segundo medio2024 listed test-takers; unknown flags/all-zero rows retained in denominator',
        national_compatibility=audit,outcomes=results)
    (HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
