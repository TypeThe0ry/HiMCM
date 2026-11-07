"""Offline conservative school-travel bounds; never infer a one-way half-trip."""
from pathlib import Path
from itertools import combinations, permutations
from math import exp, inf
import csv, json, hashlib, re
from zipfile import ZipFile
from xml.etree import ElementTree as ET
P=Path(__file__).resolve().parent

def main():
    for r in json.loads((P/'manifest.json').read_text()):
        if r.get('sha256'):
            assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    d=json.loads((P/'mexico_official_index_extract.json').read_text())
    # The chart labels are available, but their colors/ordering could not be verified.
    # Resolve stage membership from the ONLY 5-bar subset summing to the EMS total.
    solutions=list(combinations(d['all_15_bar_counts'],5))
    groups=[x for x in solutions if sum(x)==d['ems_reported_total']]
    assert len(groups)==1, 'Ambiguous school-stage membership: do not admit'
    counts=groups[0]
    assert set(counts)==set(d['ems_counts_inferred_unique_subset'])
    missing=d['all_compulsory_total']-d['all_compulsory_reported_time']
    assert missing==77347
    denominator=d['ems_reported_total']+missing
    upper_ends=d['roundtrip_upper_end_minutes']
    utilities=[exp(-x/30) if x is not None else 0 for x in upper_ends]
    outcomes=[]
    for p in permutations(counts):
        # Use full roundtrip bound: inbound time <= full roundtrip; no /2.
        numerator=sum(n*u for n,u in zip(p,utilities))
        outcomes.append((numerator/denominator,p))
    lower,worst=min(outcomes)
    natural=sum(n*u for n,u in zip(d['unverified_natural_mapping'],utilities))/denominator
    row=dict(city='Mexico City',indicator='travel',utility_lower=lower,utility_upper=1,
        year=2015,source_url=d['source_url'],
        scope='CDMX residents age3–17 attending upper-secondary (EMS); 2015 Intercensal estimates; respondent group recovered by unique 5-count subset; all 120 bin permutations; all compulsory-school duration nonresponse allocated to EMS; inbound <= roundtrip; publication2020; not current all-age upper-secondary census',
        status='conditional_manual_primary_index_roundtrip_missing_adjusted',
        reported_students=d['ems_reported_total'],maximum_unknown_duration_students=missing,
        mapping_permutations=120,mapping_robust=True,extraction='manual_official_index',raw_pdf_archived=False)
    with (P/'bounds.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=row.keys());w.writeheader();w.writerow(row)
    diagnostics=dict(unique_ems_subset=list(counts),candidate_subsets_checked=len(solutions),
        worst_bin_assignment=list(worst),permutations_checked=len(outcomes),
        maximum_target_population=denominator,strict_archived_lower=0,strict_archived_upper=1,
        mapping_robust_lower=lower,unverified_natural_mapping_lower=natural,
        note='Natural mapping only diagnostic; never used in admitted bounds. No PDF visual check claimed.')
    (P/'bound_diagnostics.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
    # Verify Tokyo is specifically upper-secondary but is NOT the same trip target.
    ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with ZipFile(P/'japan2021_student_activity_time.xlsx') as z:
        strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        found=None
        for _,node in ET.iterparse(z.open('xl/worksheets/sheet1.xml'),events=['end']):
            if node.tag.endswith('}row'):
                if node.attrib.get('r')=='23498':
                    found={}
                    for c in node:
                        v=c.find('m:v',ns)
                        if v is not None: found[c.attrib['r']]=strings[int(v.text)] if c.attrib.get('t')=='s' else v.text
                    break
                node.clear()
    assert found['A23498']=='2_平日' and found['B23498']=='13_東京都' and found['D23498']=='3_高校'
    assert found['J23498']=='87' and found['AD23498']=='67'
    (P/'tokyo_diagnostic_row.json').write_text(json.dumps(found,ensure_ascii=False,indent=2)+'\n')
    # Containment: all possible mappings obey our final conservative lower bound.
    assert all(v>=lower-1e-15 for v,_ in outcomes)
    assert 0<lower<natural<1
    print(json.dumps(diagnostics,indent=2))
if __name__=='__main__': main()
