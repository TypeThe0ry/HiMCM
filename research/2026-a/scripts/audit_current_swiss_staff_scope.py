"""Verify reuse of earlier Swiss staff sources without admitting a teacher cap."""
import hashlib
import json
import subprocess
import zipfile
import xml.etree.ElementTree as E
from pathlib import Path
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_audit_output import audit_parser,check_output,emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES

R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_swiss_staff2024_scope'
O=R/'results/current_swiss_staff_scope_review/verification.json'
BOOK=R/'data/task4_v170_zurich/bfs_staff_2024_25_original.xlsx'
MANUAL=R/'data/task4_v171_bfs_scope/bfs_SSP_2024_25_manual_original.pdf'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())


def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O,G)
    protection=protected_inputs();bodies=[]
    receipts=list(D.glob('*.receipt.json'));assert len(receipts)==4
    for p in receipts:
        m=read(p);body=R/m['archived_body'] if 'archived_body' in m else D/p.name.removesuffix('.receipt.json')
        assert m['status']==200 and body.stat().st_size==m['bytes'] and sha(body)==m['sha256']
        bodies.append(body)
    assert sha(BOOK)=='3b395bb02b639746c1270da4674b70971e0f488904e528e688304cd8ffccf553'
    assert sha(MANUAL)=='5a88f11fa5a6e0879fbfc371601088d2ad1eda52ab8ce917f3327ebaa889e2aa'
    assert not (D/'schoolpersonnel2024_25.xlsx').exists()
    assert not (D/'ssp_handbook2024_25.pdf').exists()
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(BOOK) as z:
        strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
        rel={x.get('Id'):x.get('Target') for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheets={x.get('name'):'xl/'+rel[x.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
                for x in E.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns)}
        cells={}
        for name in ['T8','T10','T11']:
            cells[name]={}
            for c in E.fromstring(z.read(sheets[name])).findall('.//s:c',ns):
                v=c.find('s:v',ns)
                if v is not None:cells[name][c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else v.text
        assert 'öffentliche Schulen' in cells['T8']['B3']
        assert cells['T10']['A10']=='Privatschulen'
        assert 'Schulleitungspersonal' in cells['T11']['C3']
        for sheet,cell,value in [('T8','H7',13797.7),('T10','J7',86866.4),
                                 ('T10','J11',10242.2),('T10','I11',3453.2)]:
            assert abs(float(cells[sheet][cell])-value)<1e-10
    pp=subprocess.check_output(['/usr/bin/pdftotext','-layout',str(MANUAL),'-'],text=True).split('\f')
    for page,phrases in {6:['einschliesslich der Privatschulen','vollständig erfasst'],
                         9:['Stellvertretungen','eine vakante Stelle'],
                         10:['zwischen dem Beginn des Schuljahres','31. Dezember','koordiniert'],
                         19:['VZÄ = C.7/C.8','derselben Einheit'],
                         20:['Basis Vollzeit','Wochenstunden/Wochenlektionen']}.items():
        normal=' '.join(pp[page-1].split())
        assert all(x in normal for x in phrases),(page,phrases)
    f,lo,hi=revised_bounds();i=f.city.tolist().index('Zurich');j=NAMES.index('upper_secondary_ptr')
    assert [float(lo[i,j]),float(hi[i,j])]==[0,1]
    assert protected_inputs()==protection
    current=read(R/'results/current_paper_review/current_verification.json')
    for n,h in current['edition_source_sha256'].items():assert sha(R/n)==h
    sources=[*sorted(D.iterdir()),*bodies,Path(__file__),
             R/'data/task4_v170_zurich/source_scope.json',R/'data/task4_v170_zurich/README.md',
             R/'data/task4_v171_bfs_scope/verification.json',R/'data/task4_v171_bfs_scope/README.md',
             R/'data/task4_v157_zurich_school/scope_audit.json',
             R/'scripts/audit_current_oslo_cost_ptr_sources.py',R/'scripts/task4_audit_output.py']
    report=dict(status='pass reuse and bounded eligibility review',**protection,
        edition_entries_checked=24,fresh_HTTP200_receipts=4,reused_binary_products=2,
        new_numeric_observations=0,new_handbook_product=False,
        selected_teacher_FTE_cells={'T8!H7':13797.7,'T10!J7':86866.4,
                                    'T10!J11':10242.2,'T10!I11':3453.2},
        handbook_physical_pages_checked=[6,9,10,19,20],
        collection_design_public_private_confirmed=True,
        actual_all_target_activities_in_published_total_certified=False,
        generic_year_mismatch_used_as_rejection=False,
        old_Eurostat_private_warning_used_to_reject_BFS=False,
        T9_qualification_missingness_used_to_infer_T10_total_missingness=False,
        teacher_cap_or_PTR_computed=False,Zurich_PTR_utility=[0,1],
        primary_admissions=0,actual_primary_width_reduction=0,
        changes_primary_model=False,changes_manuscript=False,
        source_sha256={str(p.relative_to(R)):sha(p) for p in sources if p.is_file()},
        scope='Receipt/archive identity, selected published cells and handbook definitions, existing-input preservation. Prior-source routing repaired; no publication-completeness or outward-precision certificate and no new measurement.')
    emit_report(report,a,O,G)


if __name__=='__main__':main()
