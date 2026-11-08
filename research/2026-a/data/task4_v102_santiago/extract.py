"""Descriptive EPJA subgroup only; no ranking-model admission."""
import collections, csv, gzip, io, json
from pathlib import Path
P = Path(__file__).resolve().parent
with gzip.open(P / 'epja_desidentificado_2023.csv.gz', 'rt', encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f, delimiter=';'))
residents = [r for r in rows if r['DS_COMUNA_ESTUDIANTE'].strip().casefold() == 'santiago']
secondary = [r for r in residents if 'medio' in r['DS_GRADO'].lower()]
counts = collections.Counter(r['TIEMPO_TRASLADO_EDUCACIONAL'] or '(missing)' for r in secondary)
result = {
    'source_year': 2023,
    'national_EPJA_respondents': len(rows),
    'Santiago_resident_EPJA_respondents': len(residents),
    'Santiago_resident_current_secondary_EPJA_respondents': len(secondary),
    'current_grade_counts': dict(collections.Counter(r['DS_GRADO'] for r in secondary)),
    'school_trip_duration_counts_unweighted': dict(sorted(counts.items())),
    'age_filter_possible': False,
    'trip_origin': 'most frequent departure point; not necessarily home',
    'weights': 'No expansion weight identified in supplied CSV; counts are unweighted respondents',
    'admit_main_model': False,
    'Santiago_main_utility_interval_retained': [0, 1]
}
(P / 'subgroup_counts.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
