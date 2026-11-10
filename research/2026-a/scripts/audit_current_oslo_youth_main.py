"""Bounded source and numeric review of the Oslo2026 main-report addendum."""
import csv
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_audit_output import audit_parser,check_output,emit_report

R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_oslo_youth2026_main';O=R/'results/current_oslo_youth2026_main'
GRADES=['8. trinn','9. trinn','10. trinn','Vg1','Vg2','Vg3']
ACTIVITIES=['sports_club','youth_club','religious_association','band_choir_orchestra',
            'culture_music_school','other_organisation']
# Root transcription checked against rendered physical35 and39. This reference
# does not import or execute the extractor's internal parsing functions.
GRADE_REFERENCE=[[74,34,27,10,12,29],[68,26,41,8,10,27],[57,23,25,7,10,24],
                 [46,18,20,8,9,22],[38,12,16,5,7,19],[31,9,15,6,6,20]]
REASONS=['other_regular_activities','school_time','no_suitable_activities','not_fit_in',
         'no_companion','too_far','too_expensive','no_parental_permission']
REASON_REFERENCE=[[33,10,9,48],[22,22,27,30],[21,15,23,41],[17,13,20,50],
                  [13,12,19,55],[4,5,16,76],[3,3,8,86],[2,1,4,94]]


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def csv_rows(name):
    with (O/name).open() as f:return list(csv.DictReader(f))


def main():
    a=audit_parser(__doc__).parse_args();canonical=O/'verification.json'
    check_output(a,canonical,G);protection=protected_inputs()
    receipts=list(D.glob('*.receipt.json'));assert len(receipts)==3
    for p in receipts:
        m=read(p);body=D/p.name.removesuffix('.receipt.json')
        assert m['status']==200 and sha(body)==m['sha256'] and body.stat().st_size==m['bytes']
        assert datetime.fromisoformat(m['started_utc']).utcoffset() is not None
    metadata=read(D/'nva_metadata.json')
    assert metadata['status']=='PUBLISHED'
    entity=metadata['entityDescription']
    assert entity['mainTitle']=='Ung i Oslo 2026. Ungdomsskolen og videregående'
    assert entity['reference']['publicationContext']['seriesNumber']=='6/2026'
    assert entity['reference']['publicationInstance']['pages']['pages']=='88'
    artifact=next(x for x in metadata['associatedArtifacts'] if x['type']=='OpenFile')
    assert artifact['mimeType']=='application/pdf'
    assert artifact['size']==(D/'nova6_2026.pdf').stat().st_size==2649559
    assert artifact['license']=='https://creativecommons.org/licenses/by/4.0/'
    receipt=read(D/'nova6_2026.pdf.receipt.json')
    assert receipt['requested_url'] in (D/'kudos.html').read_text()
    assert (D/'nova6_2026.pdf').read_bytes().startswith(b'%PDF')
    info=subprocess.check_output(['/usr/bin/pdfinfo',str(D/'nova6_2026.pdf')],text=True)
    assert re.search(r'^Pages:\s+88$',info,re.M)
    methods=subprocess.check_output(['/usr/bin/pdftotext','-f','80','-l','80','-layout',
                                     str(D/'nova6_2026.pdf'),'-'],text=True)
    normal=' '.join(methods.split())
    for phrase in ['27 472','37 308','15 180','2018','566','132',
                   '79 prosent','68 prosent','verken lærlinger','sluttet i']:
        assert phrase in normal,phrase
    right=subprocess.check_output(['/usr/bin/pdftotext','-f','80','-l','80','-r','72',
        '-x','270','-y','0','-W','270','-H','780',str(D/'nova6_2026.pdf'),'-'],text=True)
    assert '12 292' in ' '.join(right.split())
    grade=csv_rows('grade_participation.csv')
    assert len(grade)==36
    indexed={(x['grade'],x['activity']):int(x['published_percent']) for x in grade}
    assert len(indexed)==36
    for g,values in zip(GRADES,GRADE_REFERENCE):
        assert [indexed[g,k] for k in ACTIVITIES]==values
    reasons=csv_rows('club_reasons.csv');assert len(reasons)==8
    cat=['very_well','well','a_little','not_at_all']
    for row,key,values in zip(reasons,REASONS,REASON_REFERENCE):
        assert row['reason']==key and [int(row[k]) for k in cat]==values
        assert int(row['summed_displayed_endorsement'])==values[0]+values[1]
    willingness=csv_rows('club_willingness.csv')
    assert [x['response'] for x in willingness]==['very_willing','maybe','probably_not','definitely_not']
    assert [int(x['published_percent']) for x in willingness]==[5,18,34,43]
    s=read(O/'summary.json')
    assert list(s['sports_club_by_grade'].values())==[74,68,57,46,38,31]
    assert s['grade8_minus_Vg3_displayed_sports_gap_pp']==43
    assert s['conditional_club_positive_willingness_sum']==23
    assert list(s['conditional_club_endorsements'].values())==[43,44,36,30,25,9,6,3]
    assert not s['earlier_upper_report_identity_mismatch_resolved']
    assert s['primary_admissions']==s['actual_primary_width_reduction']==0
    with tempfile.TemporaryDirectory(prefix='himcm-main-youth-',dir='/data/scratch') as tmp:
        out=Path(tmp)/'replay'
        subprocess.run([sys.executable,str(R/'scripts/task4_current_oslo_youth_main.py'),
                        '--output-dir',str(out)],check=True,stdout=subprocess.PIPE)
        for name in ['grade_participation.csv','club_reasons.csv','club_willingness.csv','summary.json']:
            assert (O/name).read_bytes()==(out/name).read_bytes()
    assert protected_inputs()==protection
    current=read(R/'results/current_paper_review/current_verification.json')
    for name,digest in current['edition_source_sha256'].items():assert sha(R/name)==digest
    sources=[*sorted(D.iterdir()),O/'README.md',O/'summary.json',O/'grade_participation.csv',
             O/'club_reasons.csv',O/'club_willingness.csv',O/'peer_review.json',Path(__file__),
             R/'scripts/task4_current_oslo_youth_main.py',R/'scripts/audit_current_oslo_cost_ptr_sources.py',
             R/'scripts/task4_audit_output.py']
    report=dict(status='pass bounded main-report survey review',**protection,
        edition_entries_checked=24,HTTP200_bodies=3,PDF_pages=88,
        root_visually_checked_cells=72,independent_review_selected_cells=26,
        output_files_bytewise_reproduced=4,NVA_binary_byte_identity_verified=False,
        item_denominators_obtained=False,primary_admissions=0,actual_primary_width_reduction=0,
        changes_primary_model=False,changes_manuscript=False,
        upper_district_local_identity_mismatch_resolved=False,
        source_sha256={str(p.relative_to(R)):sha(p) for p in sources if p.is_file()},
        scope='Published rounded grade/club tables and methods, metadata/receipt alignment, selected visual review and input preservation. Conditional, nonexclusive self-reports; no microdata, exact-age, causal, all-resident, pool-access or cross-report weighting equivalence certification.')
    emit_report(report,a,canonical,G)


if __name__=='__main__':main()
