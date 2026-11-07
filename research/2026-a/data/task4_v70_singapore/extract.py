"""Audit Singapore grouped travel scope and reproduce a subgroup counterexample."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent


def subgroup_extreme(counts, utilities, mass, maximize=False):
    # Fractional count allocation is valid for weighted published survey counts.
    assert 0 < mass <= sum(counts)
    order=sorted(range(len(counts)),key=lambda k:utilities[k],reverse=maximize)
    remaining=mass; allocation=[0.]*len(counts)
    for k in order:
        allocation[k]=min(remaining,counts[k]);remaining-=allocation[k]
        if remaining==0:break
    assert remaining==0 and sum(allocation)==mass
    return sum(a*u for a,u in zip(allocation,utilities))/mass,allocation


def extract():
    for item in json.loads((ROOT/'manifest.json').read_text()):
        if 'sha256' not in item:continue
        b=(ROOT/item['file']).read_bytes()
        assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
    spec=importlib.util.spec_from_file_location('sg70_xlsx_reader',ROOT.parent/'task4_v68_singapore/extract.py')
    reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    mapping=reader.sheets(ROOT.parent/'task4_v68_singapore/isced2011_mapping.xlsx')['Sheet1']
    assert mapping['R18']=='453' and mapping['R19']=='454'
    text=subprocess.check_output(['pdftotext','-layout',str(ROOT/'census2020_sr1.pdf'),'-']).decode()
    page=text.split('\f')[231]
    assert 'Secondary 1 to 5' in page and 'Skills Certificate' in page
    old=ROOT.parent/'task4_school'
    records=json.loads((old/'sg_travel_api.json').read_text())['result']['records']
    assert len(records)==6
    counts=[int(r['Secondary_Total']) for r in records if r['Number']!='Total']
    assert counts==[46434,71367,31872,17246,5568] and sum(counts)==172487
    lower=[math.exp(-x/30) for x in (15,30,45,60,float('inf'))]
    upper=[math.exp(-x/30) for x in (0,15,30,45,60)]
    broad=[]
    for field in ('Secondary_Total','Post_Secondary_Non_Tertiary_Total'):
        c=[int(r[field]) for r in records if r['Number']!='Total']
        broad.append([sum(n*u for n,u in zip(c,lower))/sum(c),sum(n*u for n,u in zip(c,upper))/sum(c)])
    envelope=[min(x[0] for x in broad),max(x[1] for x in broad)]
    age=json.loads((ROOT/'age_level2020_api.json').read_text())['result']
    assert age['total']==len(age['records'])==8
    sec=next(r for r in age['records'] if r['Number']=='Secondary')
    ages={k:int(sec[k]) for k in ('Total_Total_Total','Total_10_14Years_Total','Total_15_19Years_Total','Total_20YearsandOver_Total')}
    assert ages['Total_Total_Total']==174298 and ages['Total_15_19Years_Total']==74241
    assert ages['Total_Total_Total']!=sum(counts)
    low,lowalloc=subgroup_extreme(counts,lower,80000)
    high,highalloc=subgroup_extreme(counts,upper,80000,True)
    assert low < envelope[0] and high > envelope[1]
    # Without a positive target-mass lower bound, arbitrarily small subgroups
    # fit in either nonempty extreme bin. These are infimum/supremum limits.
    assert counts[0]>0 and counts[-1]>0 and lower[-1]==0 and upper[0]==1
    return dict(city='Singapore',source_year=2020,
        previous_mixed_stage_envelope=envelope,
        secondary_whole_group_interval=broad[0],postsecondary_whole_group_interval=broad[1],
        secondary_counts=counts,secondary_travel_total=sum(counts),secondary_age_table=ages,
        target='Age 14-18 current upper-secondary students; no same-universe current-grade by age by travel-bin allocation available',
        target_mass_interval=[0,sum(counts)],target_mass_positive_but_no_identified_positive_lower_bound=True,
        revised_travel_interval=[0,1],
        counterexample_mass80000=dict(hypothetical=True,mass=80000,lower=low,upper=high,
            lower_bin_allocation=lowalloc,upper_bin_allocation=highalloc,
            meaning='Constructed subgroup assignments under published bin capacities, not observed high-school counts or trips'),
        limits_are_infimum_supremum=True,
        population_exclusions='Travel table excludes home study and students overseas at least six months; age-level table denominator is different.',
        classification_evidence=dict(census2020_pdf_page=232,census2020_printed_page=215,
            ghs2025_pdf_page=130,ghs2025_printed_page=115,
            ghs2025_definition_visually_checked=True,
            census_secondary='Secondary 1 to 5 plus vocational/technical/commercial secondary courses including ITE Skills Certificate'),
        ghs2025_not_used_as_target_observation=True,
        nitec_mapping=dict(reference_year=2023,National_ITE_Certificate='453',Higher_National_ITE_Certificate='454',cells='Sheet1!R18:R19'),
        counterexample_scope='Secondary is one broad group containing ordinary upper-secondary students; this does not assert all target programmes belong to Secondary. Target programme and age allocation are unresolved.')

if __name__=='__main__':
    r=extract();(ROOT/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
