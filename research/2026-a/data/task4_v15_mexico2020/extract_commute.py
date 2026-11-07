"""Version-specific 2020 school travel, with conditional stage reconstruction."""
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
from math import exp
import csv,io,json,hashlib
P=Path(__file__).resolve().parent

def reconstructed_ems(row):
    if row['ASISTEN']!='1':return False
    if not row['NIVACAD'].isdigit() or not row['ESCOLARI'].isdigit():return False
    level,grade=int(row['NIVACAD']),int(row['ESCOLARI'])
    return (level==3 and grade==3) or (level in (4,5,7) and 0<=grade<3)

def bounds(counts):
    lower=[exp(-x/30) for x in [15,30,60,120]]+[0.]
    upper=[exp(-x/30) for x in [0,15,30,60,120]]
    n=sum(counts.values());assert n>0
    unknown=counts['6']+counts['9']
    return sum(counts[str(k+1)]*v for k,v in enumerate(lower))/n,(sum(counts[str(k+1)]*v for k,v in enumerate(upper))+unknown)/n

def optional_membership(counts,optional):
    """Exact prefix extrema, conditional on the stated known/optional partition."""
    n=sum(counts.values());lo,hi=bounds(counts)
    endpoints={str(i+1):(exp(-b/30) if b is not None else 0.,exp(-a/30))
               for i,(a,b) in enumerate(zip([0,15,30,60,120],[15,30,60,120,None]))}
    endpoints.update({'6':(0.,1.),'9':(0.,1.),'':(0.,1.)})
    result=[]
    for col,base,reverse in [(0,lo,False),(1,hi,True)]:
        numerator=n*base;denominator=n;candidates=[base]
        for code,w in sorted(optional.items(),key=lambda x:endpoints[x[0]][col],reverse=reverse):
            numerator+=w*endpoints[code][col];denominator+=w
            candidates.append(numerator/denominator)
        result.append(max(candidates) if reverse else min(candidates))
    assert result[0]<=lo+1e-12 and result[1]>=hi-1e-12
    return result

def main():
    for r in json.loads((P/'manifest.json').read_text()):
        assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    groups={s:dict(weighted=Counter(),sample=Counter(),municipalities=set(),grades=Counter(),unknown_age_weight=0) for s in ['age3_17','all_age3plus']}
    ids=set();n=0;population=0;ambiguous_stage=Counter();optional={s:Counter() for s in groups}
    with ZipFile(P/'Censo2020_CA_cdmx_csv.zip') as z:
        for row in csv.DictReader(io.TextIOWrapper(z.open('Personas09.CSV'),encoding='utf-8-sig')):
            n+=1;assert row['ENT']=='09' and row['ID_PERSONA'] not in ids;ids.add(row['ID_PERSONA'])
            w=int(row['FACTOR']);assert w>0;population+=w
            age=int(row['EDAD']);age_known=3<=age<=130
            if row['ASISTEN']=='1' and (row['NIVACAD']=='99' or row['ESCOLARI']=='99'):
                ambiguous_stage['all_age3plus']+=w
                optional['all_age3plus'][row['TIE_TRASLADO_ESCU']]+=w
                if 3<=age<=17:ambiguous_stage['age3_17']+=w
                if 3<=age<=17:optional['age3_17'][row['TIE_TRASLADO_ESCU']]+=w
            if not reconstructed_ems(row):continue
            scopes=['all_age3plus']+(['age3_17'] if 3<=age<=17 else [])
            code=row['TIE_TRASLADO_ESCU'];assert code in ['1','2','3','4','5','6','9']
            for scope in scopes:
                g=groups[scope];g['weighted'][code]+=w;g['sample'][code]+=1;g['municipalities'].add(row['MUN']);g['grades'][(row['NIVACAD'],row['ESCOLARI'])]+=w
                if not age_known:g['unknown_age_weight']+=w
    independent=json.loads((P/'independent_counts.json').read_text());assert n==independent['total_rows']
    result=dict(year=2020,person_rows=n,weighted_private_household_population=population,current_stage_directly_observed=False,stage_definition='ASISTEN1 and completed secondary3 or completed grades0-2 at levels4/5/7; conditional progression reconstruction',scopes={})
    for scope,g in groups.items():
        assert dict(g['weighted'])==independent['weighted_bins'][scope]
        assert sum(g['sample'].values())==independent['samples'][scope]
        assert len(g['municipalities'])==16
        lo,hi=bounds(g['weighted']);assert 0<=lo<=hi<=1
        result['scopes'][scope]=dict(utility_lower=lo,utility_upper=hi,sample_rows=sum(g['sample'].values()),weighted_students=sum(g['weighted'].values()),weighted_time_bins=dict(g['weighted']),sample_time_bins=dict(g['sample']),unknown_age_weight=g['unknown_age_weight'],all_attenders_with_unspecified_stage_weight=ambiguous_stage[scope],scope_note='Classifiable reconstructed stage only; unknown stages are not demonstrated non-high-school students.')
        ml,mh=optional_membership(g['weighted'],optional[scope])
        result['scopes'][scope].update(optional_stage_time_bins=dict(optional[scope]),membership_utility_lower=ml,membership_utility_upper=mh)
        n_known=sum(g['weighted'].values());m=ambiguous_stage[scope]
        coarse_lo=lo*n_known/(n_known+m);coarse_hi=(hi*n_known+m)/(n_known+m)
        assert coarse_lo<=ml+1e-12 and mh<=coarse_hi+1e-12
        result['scopes'][scope].update(coarse_optional_lower=coarse_lo,coarse_optional_upper=coarse_hi,membership_width_reduction_vs_coarse=1-(mh-ml)/(coarse_hi-coarse_lo))
    (P/'commute_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
