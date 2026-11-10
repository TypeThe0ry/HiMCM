"""Extract published resident-district tables; do not modify the primary model.

The two upper-stage reports disagree with the local district identity of one
report. Preserve those tables separately, without using their grade contrasts.
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = R / 'data/current_oslo_youth2026'
DISTRICTS = ['Stovner', 'Grorud', 'Alna', 'Søndre Nordstr.', 'Gamle Oslo',
             'Grünerløkka', 'Bjerke', 'Sagene', 'Østensjø', 'St. Hanshaugen',
             'Frogner', 'Nordstrand', 'Ullern', 'Nordre Aker', 'Vestre Aker']
MEASURES = ['meeting_places_good', 'sports_facilities_good',
            'cultural_provision_good', 'public_transport_good',
            'sports_club_previous_month', 'parents_lack_activity_money']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pages(p):
    return subprocess.check_output(['/usr/bin/pdftotext', '-layout', str(p), '-'],
                                   text=True).split('\f')


def table(page, heading, width, columns):
    body = page.split(heading, 1)[1]
    rows = {}
    for line in body.splitlines():
        if len(rows) == len(DISTRICTS):
            break
        line = line[:width].strip() if width else line.strip()
        for district in DISTRICTS:
            if line.startswith(district + ' '):
                numbers = re.findall(r'\b\d+\b', line[len(district):])
                if district in rows or len(numbers) != columns:
                    raise ValueError((district, line, numbers))
                rows[district] = [int(v) for v in numbers]
    assert set(rows) == set(DISTRICTS), rows.keys()
    assert all(0 <= v <= 100 for row in rows.values() for v in row)
    return rows


def extract(p):
    pp = pages(p)
    provision = table(pp[20], 'Prosentandel i bydelene som opplever', None, 4)
    sports = table(pp[27], 'Prosentandel i bydelene som deltok', None, 6)
    # Left panel only; the right panel contains unrelated bar-chart numbers.
    money = table(pp[12], 'Prosentandel i ulike bydeler som er fornøyd med', 70, 2)
    return {d: provision[d] + [sports[d][0], money[d][1]] for d in DISTRICTS}, pp


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    out = args.output_dir.resolve()
    if out.exists():
        raise FileExistsError('Use a new output directory')
    out.mkdir(parents=True)
    rows = []
    summaries = {}
    for stage in ['lower', 'upper']:
        a, pp = extract(D / f'sondre_{stage}.pdf')
        b, qq = extract(D / f'alna_{stage}.pdf')
        assert a == b, f'District-table mismatch: {stage}'
        assert 'Bydel Søndre Nordstrand' in pp[0]
        assert 'Bydel Alna' in qq[0]
        assert 'Januar-april 2026' in pp[4]
        assert 'bostedsbydel' in pp[3]
        if stage == 'lower':
            assert 'vektet' in pp[2] and 'tre klassetrinnene' in pp[2]
            assert '13 og 16 år' in pp[2]
        else:
            assert '16 og 19 år' in pp[2]
            assert 'Alna' in pp[20].split('Prosentandel i bydelene som opplever')[0]
        for district in DISTRICTS:
            for k, measure in enumerate(MEASURES):
                rows.append(dict(stage=stage, district=district, measure=measure,
                                 published_percent=a[district][k],
                                 physical_page=21 if k < 4 else 28 if k == 4 else 13,
                                 printed_page=18 if k < 4 else 25 if k == 4 else 10,
                                 use_status='descriptive_context' if stage == 'lower'
                                 else 'quarantined_local_identity_mismatch'))
        summaries[stage] = {}
        for k, measure in enumerate(MEASURES):
            v = {d: a[d][k] for d in DISTRICTS}
            summaries[stage][measure] = dict(min_percent=min(v.values()),
                max_percent=max(v.values()), spread_percentage_points=max(v.values())-min(v.values()),
                minimum_districts=[d for d, n in v.items() if n == min(v.values())],
                maximum_districts=[d for d, n in v.items() if n == max(v.values())])
    with (out / 'published_district_values.csv').open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    summary = dict(observation_period='January-April2026', districts=15,
        published_cells=180, lower_stage_context_cells=90, upper_stage_quarantined_cells=90,
        independent_respondent_replications=0,
        duplicate_publication_tables_match=True,
        lower_stage_weighting='Report states even distribution across three school grades',
        percentages='Publisher rounded whole percentages; item denominators unavailable',
        population='School survey respondents grouped by self-reported residential district',
        scope='Descriptive contextual evidence; no student-level access, causal or exact-age contrast',
        upper_local_identity_issue='Søndre upper cover identifies Søndre; local charts identify Alna',
        lower_stage_ranges=summaries['lower'], upper_stage_ranges_quarantined=summaries['upper'],
        primary_admissions=0, actual_primary_width_reduction=0,
        changes_primary_model=False, changes_manuscript=False)
    (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: summary[k] for k in ['districts', 'published_cells',
          'lower_stage_context_cells', 'upper_stage_quarantined_cells']}, indent=2))


if __name__ == '__main__':
    main()
