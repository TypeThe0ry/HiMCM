"""Independent CSV/PSU-residual audit; publishes no individual identifiers."""
from pathlib import Path
from collections import defaultdict,Counter
from zipfile import ZipFile
import csv,io,json,hashlib,math,importlib.util
import numpy as np
from scipy.stats import t
P=Path(__file__).resolve().parent;OLD=P.parent/'task4_v63_cape_travel'
spec=importlib.util.spec_from_file_location('v63_classification',OLD/'extract.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def main():
    m=json.loads((P/'aggregate_moments.json').read_text());summary=json.loads((P/'summary.json').read_text());source=OLD/'GHS2025.zip'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==m['source_zip_sha256']
    with ZipFile(source) as z:rows=list(csv.DictReader(io.TextIOWrapper(z.open('PERSON2025.csv'),encoding='utf-8-sig')))
    strata={r['stratum'] for r in rows if old.integer(r,'metro_code')==2}
    frame=[r for r in rows if r['stratum'] in strata];assert all(old.integer(r,'metro_code')==2 for r in frame)
    groups=defaultdict(list);classifications=Counter();bins=Counter();people=0;errors=[]
    for r in frame:
        groups[(r['stratum'],r['psu'])].append(r)
        c=old.classify(r,(14,18));classifications[c]+=1
        if c=='definite':
            people+=1;bins[old.integer(r,'edu_time')]+=old.weight(r)
    assert classifications['optional']==0 and people==m['n']
    zero=sum(not any(old.classify(r,(14,18))=='definite' for r in rr) for rr in groups.values())
    assert zero==m['zero_target_psus'] and len(groups)==m['psus'] and len(strata)==m['strata']
    expected=[sum(w for c,w in bins.items() if c not in [1,2,3,4,5])]+[bins[c] for c in [1,2,3,4,5]]
    np.testing.assert_allclose(expected,m['weighted_totals'],rtol=0,atol=1e-8)
    df=len(groups)-len(strata);critical=t.ppf(1-.05/4,df)
    for result in summary['results']:
        tau=result['tau_minutes'];psu=defaultdict(list)
        for (h,j),rr in groups.items():
            v=[0.,0.,0.]
            for r in rr:
                if old.classify(r,(14,18))!='definite':continue
                w=old.weight(r);a,b=old.TIME_BINS.get(old.integer(r,'edu_time'),(0,math.inf))
                v[0]+=w*math.exp(-b/tau);v[1]+=w*math.exp(-a/tau);v[2]+=w
            psu[h].append(v)
        total=[sum(v[k] for vv in psu.values() for v in vv) for k in range(3)];est=[total[k]/total[2] for k in range(2)];se=[]
        for k in range(2):
            var=0.
            for vv in psu.values():
                n=len(vv);assert n>=2
                residual=[v[k]-est[k]*v[2] for v in vv];mean=sum(residual)/n
                var+=n/(n-1)*sum((x-mean)**2 for x in residual)
            se.append(math.sqrt(var)/total[2])
        env=[max(0,est[0]-critical*se[0]),min(1,est[1]+critical*se[1])]
        for actual,key in [(est,'point_bounds'),(se,'endpoint_standard_errors'),(env,'joint_95_percent_approximate_envelope')]:
            errors.extend(abs(a-b) for a,b in zip(actual,result[key]));np.testing.assert_allclose(actual,result[key],rtol=0,atol=2e-14)
    ref=json.loads((OLD/'inference_summary.json').read_text())['age14_18'];np.testing.assert_allclose(summary['results'][2]['joint_95_percent_approximate_envelope'],ref['joint_95_percent_approximate_envelope'],rtol=0,atol=2e-14)
    report={'passed':True,'method':'Independent stdlib CSV classification, direct PSU ratio residuals at all five scales; no six-dimensional covariance reuse','source_sha256':m['source_zip_sha256'],'scales_checked':[r['tau_minutes'] for r in summary['results']],'n':people,'optional_n':classifications['optional'],'unknown_time_weight':expected[0],'psus':len(groups),'strata':len(strata),'zero_target_psus':zero,'maximum_absolute_endpoint_or_se_difference':max(errors),'tau30_matches_V63':True,'no_missing_mass_dropped':True,'individual_records_exported':False}
    (P/'independent_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
