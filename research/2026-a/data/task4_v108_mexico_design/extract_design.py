"""Publish only city-level sufficient moments; retain PSU aggregates locally."""
from pathlib import Path
from collections import defaultdict,Counter
from zipfile import ZipFile
import csv,io,json,hashlib
P=Path(__file__).resolve().parent
SOURCE=P.parent/'task4_v107_mexico'
CODES=['1','2','3','4','5','6','9','']
GROUPS=['prepa_conditional','boundary3','other_optional']
LABELS=[f'{g}:{c or "blank"}' for g in GROUPS for c in CODES]
def main():
    raw=SOURCE/'local_only/eic2025_micro_09_csv.zip'
    original=json.loads((SOURCE/'aggregate_manifest.json').read_text())['raw_sha256']
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==original
    psu={};weights=defaultdict(set);rows=0;age_attend=Counter();ids=set()
    with ZipFile(raw) as z:
        for r in csv.DictReader(io.TextIOWrapper(z.open('personas09.csv'),encoding='utf-8-sig')):
            rows+=1;assert r['CVE_ENT']=='09'
            rid=r['ID_VIV'],r['ID_PERSONA'];assert rid not in ids;ids.add(rid)
            key=r['ESTRATO'],r['UPM'];v=psu.setdefault(key,[0]*24)
            w=int(r['FACTOR']);assert w>0;weights[key].add(w)
            age=int(r['EDAD']);unknown_age=age==999
            if not unknown_age and not 14<=age<=18:continue
            if r['ASISTEN']=='1':age_attend[key]+=1
            if r['ASISTEN']=='3':continue
            assert r['ASISTEN'] in ('1','9','')
            level=int(r['NIVACAD']) if r['NIVACAD'] else 99
            grade=int(r['ESCOLARI']) if r['ESCOLARI'] else 99
            prepa=level in (4,5,7) and 0<=grade<=2
            boundary=level==3 and grade==3
            unknown=level==99 or grade==99
            if not (prepa or boundary or unknown):continue
            group=2
            if not unknown_age and r['ASISTEN']=='1':
                if prepa:group=0
                elif boundary:group=1
            v[group*8+CODES.index(r['TIE_TRASLADO_ESCU'])]+=w
    assert all(len(w)==1 for w in weights.values())
    strata=defaultdict(list)
    for (h,j),v in psu.items():strata[h].append(v)
    assert all(len(v)>1 for v in strata.values()),'Singleton requires separate treatment'
    totals=[sum(v[k] for v in psu.values()) for k in range(24)]
    old=json.loads((SOURCE/'aggregate_bins.json').read_text())['groups']
    assert totals==[old[g]['weighted'].get(c,0) for g in GROUPS for c in CODES]
    cross=[[0.]*24 for _ in range(24)]
    for vv in strata.values():
        n=len(vv);means=[sum(v[k] for v in vv)/n for k in range(24)]
        for v in vv:
            d=[v[k]-means[k] for k in range(24)]
            for k in range(24):
                for l in range(24):cross[k][l]+=n/(n-1)*d[k]*d[l]
    diag={'person_rows':rows,'strata_n':len(strata),'psu_n':len(psu),'singleton_strata_n':0,'degrees_freedom':len(psu)-len(strata),'stratum_psu_count_distribution':dict(Counter(len(v) for v in strata.values())),'psus_no_attending_age14_18':sum(age_attend[k]==0 for k in psu),'psus_zero_target_vector':sum(sum(v)==0 for v in psu.values()),'psus_factor_one':sum(w=={1} for w in weights.values()),'strata_all_factor_one':sum(all(weights[k]=={1} for k in psu if k[0]==h) for h in strata),'weights_constant_within_psu':True}
    (P/'local_only').mkdir(exist_ok=True)
    (P/'local_only/psu_weighted_bins.json').write_text(json.dumps([{'stratum':h,'psu':j,'weighted_bins':v} for (h,j),v in psu.items()]))
    result={'method':'Fixed final person FACTOR, stratified ultimate-cluster with-replacement approximation; FPC omitted','source_raw_sha256':original,'labels':LABELS,'weighted_totals':totals,'centered_crossproduct':cross,'crossproduct_definition':'sum_h n_h/(n_h-1) sum_j (z_hj-mean_h)(z_hj-mean_h)^T; all observed CDMX PSUs including target-zero PSUs','diagnostics':diag,'sampling_interval_official':False,'remaining_limitations':['N_h and natural weights not recovered from final nonresponse-adjusted FACTOR','No FPC, calibration or weight-estimation uncertainty adjustment','Only observed person-file PSUs; wholly nonresponding sampled PSUs not enumerated','Membership assumptions inherited from V107; not direct current-stage observation']}
    f=P/'design_moments.json';f.write_text(json.dumps(result,indent=2)+'\n')
    (P/'manifest.json').write_text(json.dumps({'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source_raw_sha256':original,'source_design_sha256':hashlib.sha256((SOURCE/'eic2025_sampling_design.pdf').read_bytes()).hexdigest(),'source_dictionary_sha256':hashlib.sha256((SOURCE/'eic2025_micro_fd.xlsx').read_bytes()).hexdigest()},indent=2)+'\n')
    print(json.dumps(diag,indent=2))
if __name__=='__main__':main()
