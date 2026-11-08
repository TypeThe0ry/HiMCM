"""EIC2025 CDMX aggregate-only school-time extraction; no row-level publication."""
from pathlib import Path
from collections import Counter
from zipfile import ZipFile
import csv,io,json,hashlib,math
P=Path(__file__).resolve().parent
END={str(j+1):(math.exp(-b/30) if b is not None else 0.,math.exp(-a/30)) for j,(a,b) in enumerate(zip([0,15,30,60,120],[15,30,60,120,None]))}
END.update({'6':(0.,1.),'9':(0.,1.),'':(0.,1.)})
def bounds(known,optional):
    den=sum(known.values());assert den>0
    out=[]
    for col,rev in [(0,False),(1,True)]:
        num=sum(w*END[c][col] for c,w in known.items());n=den;candidates=[num/n]
        for c,w in sorted(optional.items(),key=lambda x:END[x[0]][col],reverse=rev):
            num+=w*END[c][col];n+=w;candidates.append(num/n)
        out.append(max(candidates) if rev else min(candidates))
    return out

def main():
    manifest=json.loads((P/'manifest.json').read_text())
    for item in manifest:
        f=P/item['file'];assert f.exists(),f'Local source missing: {f}; see manifest URL'
        assert hashlib.sha256(f.read_bytes()).hexdigest()==item['sha256']
    grouped={k:{'weighted':Counter(),'sample':Counter()} for k in ['prepa_conditional','boundary3','other_optional']}
    ids=set();ages_unknown=0;rows=population=0;boroughs=set();psus=set();strata=set();target_missing=Counter()
    with ZipFile(P/'local_only/eic2025_micro_09_csv.zip') as z:
        assert 'personas09.csv' in z.namelist()
        for r in csv.DictReader(io.TextIOWrapper(z.open('personas09.csv'),encoding='utf-8-sig')):
            rows+=1;assert r['CVE_ENT']=='09'
            key=(r['ID_VIV'],r['ID_PERSONA']);assert key not in ids;ids.add(key)
            w=int(r['FACTOR']);assert w>0;population+=w
            boroughs.add(r['CVE_MUN']);psus.add((r['ESTRATO'],r['UPM']));strata.add(r['ESTRATO'])
            age=int(r['EDAD']);age_unknown=age==999
            ages_unknown+=age_unknown
            if not age_unknown and not 14<=age<=18:continue
            for f in ['ASISTEN','NIVACAD','ESCOLARI','TIE_TRASLADO_ESCU']:
                if not r[f]:target_missing[f]+=1
            if r['ASISTEN']=='3':continue
            assert r['ASISTEN'] in ('1','9','')
            lev=int(r['NIVACAD']) if r['NIVACAD'] else 99
            grade=int(r['ESCOLARI']) if r['ESCOLARI'] else 99
            prepa=lev in (4,5,7) and 0<=grade<=2
            boundary=lev==3 and grade==3
            unknown=lev==99 or grade==99
            if not (prepa or boundary or unknown):continue
            group='other_optional'
            if not age_unknown and r['ASISTEN']=='1':
                if prepa:group='prepa_conditional'
                elif boundary:group='boundary3'
            code=r['TIE_TRASLADO_ESCU'];assert code in END
            grouped[group]['weighted'][code]+=w;grouped[group]['sample'][code]+=1
    base=grouped['prepa_conditional']['weighted'];boundary=grouped['boundary3']['weighted'];other=grouped['other_optional']['weighted']
    old=bounds(base+boundary,other);revised=bounds(base,other+boundary)
    assert revised[0]<=old[0]+1e-12 and revised[1]>=old[1]-1e-12
    for d in grouped.values():d.update(sample_n=sum(d['sample'].values()),expanded_n=sum(d['weighted'].values()))
    result={'survey_year':2025,'source_publication_year':2026,'geography':'CDMX habitual residents in sampled private dwellings, CVE_ENT09, not metropolitan area','person_rows':rows,'expanded_private_household_population':population,'borough_count':len(boroughs),'stratum_count':len(strata),'stratum_UPM_count':len(psus),'unknown_age_rows':ages_unknown,'target_age_missing_field_rows':target_missing,'groups':grouped,'scenarios':{'legacy_progression':{'known_weight':sum((base+boundary).values()),'optional_weight':sum(other.values()),'utility_lower':old[0],'utility_upper':old[1]},'boundary3_optional':{'known_weight':sum(base.values()),'optional_weight':sum((other+boundary).values()),'utility_lower':revised[0],'utility_upper':revised[1]}},'time_interpretation':'Reported home-to-school duration categories; codes6,9 and blank retain [0,1]','current_stage_directly_observed':False,'age_scope':'14–18 inclusive; unspecified999 optional if otherwise possibly eligible','sampling_uncertainty_included':False,'weights':'official person FACTOR; ESTRATO/UPM available, no replicate-design CI estimated','main_admission':False,'publication':'Only aggregate bins and counts; local-only raw ZIP excluded by gitignore'}
    (P/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    aggregate={'survey_year':2025,'age_scope':'14–18; unknown age optional','groups':grouped}
    (P/'aggregate_bins.json').write_text(json.dumps(aggregate,ensure_ascii=False,indent=2)+'\n')
    (P/'aggregate_manifest.json').write_text(json.dumps({'file':'aggregate_bins.json','sha256':hashlib.sha256((P/'aggregate_bins.json').read_bytes()).hexdigest(),'raw_sha256':next(m['sha256'] for m in manifest if m['file'].endswith('.zip')),'derivation':'extract.py from verified EIC2025 CDMX persons; only category-level sample counts and expansion-weight sums'},indent=2)+'\n')
    print(json.dumps({'rows':rows,'groups':{k:(d['sample_n'],d['expanded_n']) for k,d in grouped.items()},'scenarios':result['scenarios']},indent=2))
if __name__=='__main__':main()
