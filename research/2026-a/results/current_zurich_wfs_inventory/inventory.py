import collections, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'data/current_zurich_transport/kanton_zh_wfs.geojson'
META = ROOT / 'data/current_zurich_transport/provenance.json'
OUT = Path(__file__).resolve().parent
raw = SRC.read_bytes()
data = json.loads(raw)
features = data['features']
metadata=json.loads(META.read_text())
assert hashlib.sha256(raw).hexdigest()==metadata['sha256']
assert len(features)==metadata['feature_count']==data['numberMatched']==3004
props = [f['properties'] for f in features]
z = [p for p in props if p.get('cname') == 'Zürich']
fields = {}
for p in props:
    for k,v in p.items():
        fields.setdefault(k, set()).add(type(v).__name__)
field_types = {k: sorted(v) for k,v in sorted(fields.items())}
def distribution(key):
    c=collections.Counter(str(p.get(key, '')) for p in z)
    return dict(sorted(c.items()))
ids = {key: [p.get(key) for p in z] for key in ('geodb_oid','objectid','nhstid','diva_nr')}
names=collections.Counter(p.get('chstname') for p in z)
summary = {
 'scope': 'Read-only inventory of source GeoJSON; exact properties.cname == Zürich filter only.',
 'source_sha256': hashlib.sha256(raw).hexdigest(),
 'total_features': len(features), 'zurich_exact_cname_records': len(z),
 'property_fields': field_types,
 'id_fields': {k:{'unique_non_null':len({x for x in vals if x is not None}), 'null_count':sum(x is None for x in vals), 'duplicate_values':{str(x):n for x,n in collections.Counter(vals).items() if n>1}} for k,vals in ids.items()},
 'duplicate_stop_names': {str(k):v for k,v in sorted(names.items(), key=lambda x:str(x[0])) if v>1},
 'missing_or_empty_linien_count': sum(not p.get('linien') for p in z),
 'coordinate_property_types': {k:field_types.get(k,[]) for k in ('x_koord','y_koord')},
 'service_type_distributions': {k:distribution(k) for k in ('vtyp','hsttyp','linien')},
 'interpretation_limit': 'cname is an attribute filter, not verified municipal-boundary membership. Source feature/record counts do not establish physical stop counts or eligibility.'
}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))

assert len(z)==479 and summary['missing_or_empty_linien_count']==17
inputs=[SRC,META,ROOT/'data/current_zurich_transport/check.py',Path(__file__).resolve()]
report=dict(status='pass source attribute inventory',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},output_sha256={'summary.json':hashlib.sha256((OUT/'summary.json').read_bytes()).hexdigest()},feature_count=3004,exact_cname_Zurich_records=479,missing_or_empty_linien=17,primary_admissions=0,actual_primary_width_reduction=0,scope='Record attributes only; cname is not a municipal boundary certificate and unique IDs are not physical stop qualification.')
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
