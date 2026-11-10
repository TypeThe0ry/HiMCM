"""Reproduce grade participation and conditional youth-club survey tables."""
import argparse
import csv
import json
import re
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = R/'data/current_oslo_youth2026_main'
GRADES = ['8. trinn','9. trinn','10. trinn','Vg1','Vg2','Vg3']
ACTIVITIES = ['sports_club','youth_club','religious_association','band_choir_orchestra',
              'culture_music_school','other_organisation']
REASONS = ['other_regular_activities','school_time','no_suitable_activities',
           'not_fit_in','no_companion','too_far','too_expensive','no_parental_permission']
CATEGORIES = ['very_well','well','a_little','not_at_all']


def pdf_text(page, mode):
    return subprocess.check_output(['/usr/bin/pdftotext','-f',str(page),'-l',str(page),
                                    mode,str(D/'nova6_2026.pdf'),'-'],text=True)


def write_csv(path, rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n')
        w.writeheader();w.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    out=parser.parse_args().output_dir.resolve()
    if out.exists():raise FileExistsError('Use a new output directory')
    grade_page=pdf_text(35,'-layout')
    body=grade_page.split('Prosentandel som deltok i en organisert aktivitet den siste måneden',1)[1]
    grade_rows=[];sport=[]
    for grade in GRADES:
        line=next(x.strip() for x in body.splitlines() if x.strip().startswith(grade+' '))
        values=[int(v) for v in re.findall(r'\b\d+\b',line[len(grade):])]
        assert len(values)==6
        sport.append(values[0])
        grade_rows.extend(dict(grade=grade,activity=a,published_percent=v,physical_page=35,
                               printed_page=33) for a,v in zip(ACTIVITIES,values))
    # Raw mode separates the adjacent tiny2/1 labels which layout mode merges.
    raw=pdf_text(39,'-raw')
    reason_body=raw.split('Grunner til at ungdom ikke går på klubb\n',1)[1]
    match=re.match(r'((?:\d+\n){32})',reason_body)
    assert match and reason_body[match.end():].startswith('Jeg får ikke lov')
    numbers=list(map(int,match[1].split()))
    reason_rows=[]
    for i,reason in enumerate(REASONS):
        values=[numbers[c*8+7-i] for c in range(4)]
        assert 99<=sum(values)<=101
        reason_rows.append(dict(reason=reason,**dict(zip(CATEGORIES,values)),
                                summed_displayed_endorsement=values[0]+values[1],
                                physical_page=39,printed_page=37))
    willingness=re.search(r'\n((?:\d+\n){4})Ja, veldig gjerne',raw)
    assert willingness
    willingness_values=list(map(int,willingness[1].split()))
    assert sum(willingness_values)==100
    willingness_rows=[dict(response=k,published_percent=v,physical_page=39,printed_page=37)
                      for k,v in zip(['very_willing','maybe','probably_not','definitely_not'],
                                     willingness_values)]
    assert all(0<=int(r['published_percent'])<=100 for r in grade_rows+willingness_rows)
    summary=dict(source='NOVA6/2026',observation_period='January-April2026',
        published_numeric_cells=72,grade_participation_cells=36,club_reason_cells=32,
        club_willingness_cells=4,sports_club_by_grade=dict(zip(GRADES,sport)),
        grade8_minus_Vg3_displayed_sports_gap_pp=sport[0]-sport[-1],
        conditional_club_endorsements={r['reason']:r['summed_displayed_endorsement'] for r in reason_rows},
        conditional_club_positive_willingness_sum=sum(willingness_values[:2]),
        percentage_arithmetic='Sums/differences of publisher-rounded percentages; not unrounded estimates',
        grade_population='School survey respondents by grade; cross-sectional, not exact-age or longitudinal change',
        club_population='Respondents who had not visited a youth club in the previous month',
        reasons='Separate nonexclusive self-reports; neither causal effects nor all-facility barriers',
        item_denominators_obtained=False,primary_admissions=0,actual_primary_width_reduction=0,
        changes_primary_model=False,changes_manuscript=False,
        earlier_upper_report_identity_mismatch_resolved=False)
    out.mkdir(parents=True)
    write_csv(out/'grade_participation.csv',grade_rows)
    write_csv(out/'club_reasons.csv',reason_rows)
    write_csv(out/'club_willingness.csv',willingness_rows)
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'published_numeric_cells':72,'sports_club_by_grade':summary['sports_club_by_grade'],
                      'primary_admissions':0},ensure_ascii=False))


if __name__=='__main__':main()
