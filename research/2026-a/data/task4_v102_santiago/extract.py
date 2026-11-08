"""Descriptive EPJA subgroup only; no ranking-model admission."""
import collections, csv, gzip, hashlib, io, json
from pathlib import Path
P = Path(__file__).resolve().parent
source = P.parent / 'local_only_epja' / 'epja_desidentificado_2023.csv.gz'
if not source.exists():
    raise SystemExit('Local-only source missing. Download the 2023 source URL in sources.json, verify its original_sha256, and gzip it into data/local_only_epja/. Do not publish individual records.')
raw = gzip.decompress(source.read_bytes())
manifest = next(x for x in json.loads((P / 'sources.json').read_text()) if x['file'].endswith('2023.csv.gz'))
if hashlib.sha256(raw).hexdigest() != manifest['original_sha256']:
    raise SystemExit('Source SHA256 mismatch; extraction stopped.')
# Retain only task fields in memory after reading; publish aggregate counts only.
fields = ['DS_COMUNA_ESTUDIANTE', 'DS_GRADO', 'TIEMPO_TRASLADO_EDUCACIONAL']
rows = [{k: row[k] for k in fields} for row in csv.DictReader(io.StringIO(raw.decode('utf-8-sig')), delimiter=';')]
del raw
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
