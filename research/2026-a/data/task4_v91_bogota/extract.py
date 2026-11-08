"""Reproduce a minimal age 14–18 Bogotá extract from checksum-pinned mirror CSVs."""
import argparse
import hashlib
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent

def numeric(s):
    text = s.astype(str).str.strip()
    # Only strip periods in validated European thousands groups.
    grouped = text.str.fullmatch(r'[+-]?[0-9]{1,3}(?:\.[0-9]{3})+(?:,[0-9]+)?', na=False)
    text = text.where(~grouped, text.str.replace('.', '', regex=False))
    return pd.to_numeric(text.str.replace(',', '.', regex=False), errors='coerce')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw-dir', type=Path, required=True, help='Directory with bogota91_{hogares,personas,viajes}.csv')
    ap.add_argument('--output-dir', type=Path, default=HERE)
    args = ap.parse_args()
    manifest = json.loads((HERE / 'source_manifest.json').read_text())
    frames = {}
    for item in manifest['files']:
        path = args.raw_dir / ('bogota91_' + item['module'] + '.csv')
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], path
        frame = pd.read_csv(path, sep=';', encoding='cp1252', low_memory=False)
        frame.columns = frame.columns.str.strip()
        assert len(frame) == item['rows']
        frames[item['module']] = frame
    h, p, v = [frames[k] for k in ['hogares', 'personas', 'viajes']]
    assert h.cod_hog.is_unique and p.cod_per.is_unique and v.cod_vj.is_unique
    assert p.cod_hg.isin(h.cod_hog).all() and v.cod_pers.isin(p.cod_per).all()
    p = p.merge(h[['cod_hog', 'cod_mpio_hg']], left_on='cod_hg', right_on='cod_hog', validate='many_to_one')
    s = p[p.edad.between(14, 18) & (p.cod_mpio_hg == 11001)].copy()
    assert s.nom_mun_hg.eq('Bogotá').all()
    hm = {key: f'H{i:04}' for i, key in enumerate(s.cod_hg.drop_duplicates(), 1)}
    pm = {key: f'P{i:04}' for i, key in enumerate(s.cod_per, 1)}
    people = pd.DataFrame({
        'person_id': s.cod_per.map(pm), 'household_id': s.cod_hg.map(hm),
        'age': s.edad, 'highest_education_reported': s.max_nivel_edu.str.strip(),
        'principal_activity_reported': s.ocupacion_principal.str.strip(),
        'person_expansion_weight': numeric(s['fexp_per>5años']),
        'reported_makes_trips': s.realiza_desplazamientos.str.strip(),
    })
    people['principal_school_activity'] = people.principal_activity_reported.eq('Colegio o escuela')
    people['conditional_media_incomplete_group'] = people.principal_school_activity & people.highest_education_reported.eq('Media incompleta (10° y 11°)')
    people['direct_current_grade_available'] = False
    t = v[v.cod_pers.isin(pm)].copy()
    assert t.cod_hg.map(hm).notna().all()
    trips = pd.DataFrame({
        'trip_id': [f'T{i:05}' for i in range(1,len(t)+1)],
        'person_id': t.cod_pers.map(pm), 'household_id': t.cod_hg.map(hm),
        'trip_order': numeric(t.orden_vj), 'purpose_reported': t.motivo_viaje.str.strip(),
        'duration_minutes': numeric(t.duracion_min),
        'mode_group_reported': t.modo_principal_agrupado.str.strip(),
        'trip_expansion_weight': numeric(t.fexp_vj),
        'direct_home_origin_available': False,
    })
    hs = h[h.cod_hog.isin(hm)]
    households = pd.DataFrame({'household_id': hs.cod_hog.map(hm), 'residence_municipality_code': hs.cod_mpio_hg, 'household_expansion_weight': numeric(hs.fexp_hg)})
    linked = trips.merge(people, on=['person_id','household_id'], validate='many_to_one')
    assert len(linked) == len(trips), 'Trip/person household disagreement'
    study = linked[linked.purpose_reported.eq('A Estudiar')]
    summary = dict(
        source_rows={k:len(f) for k,f in frames.items()},
        all_source_person_household_and_trip_person_join_coverage=1.0,
        bogota_age14_18_persons=len(people), bogota_age14_18_households=len(households),
        bogota_age14_18_all_trips=len(trips), bogota_age14_18_study_destination_trips=len(study),
        principal_school_activity_persons=int(people.principal_school_activity.sum()),
        conditional_media_incomplete_persons=int(people.conditional_media_incomplete_group.sum()),
        principal_school_activity_study_destination_trips=int(study.principal_school_activity.sum()),
        conditional_media_incomplete_study_destination_trips=int(study.conditional_media_incomplete_group.sum()),
        direct_current_grade_count=0, direct_home_origin_count=0,
        missing_duration_count=int(trips.duration_minutes.isna().sum()),
        nonpositive_duration_count=int(trips.duration_minutes.le(0).sum()),
        duration_min=float(trips.duration_minutes.min()),duration_max=float(trips.duration_minutes.max()),
        missing_household_weight_count=int(households.household_expansion_weight.isna().sum()),
        nonpositive_household_weight_count=int(households.household_expansion_weight.le(0).sum()),
        missing_person_weight_count=int(people.person_expansion_weight.isna().sum()),
        nonpositive_person_weight_count=int(people.person_expansion_weight.le(0).sum()),
        missing_trip_weight_count=int(trips.trip_expansion_weight.isna().sum()),
        nonpositive_trip_weight_count=int(trips.trip_expansion_weight.le(0).sum()),
        admitted_to_main_model=False,
        reason='Third-party processed mirror; highest education and principal activity do not directly identify current grade; home-origin flags absent.'
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, df in [('persons_age14_18',people),('households_age14_18',households),('trips_age14_18',trips)]:
        df.to_csv(args.output_dir/(name+'.csv'), index=False)
    people.groupby(['principal_school_activity','highest_education_reported'],dropna=False).size().rename('persons').reset_index().to_csv(args.output_dir/'education_inventory.csv',index=False)
    (args.output_dir/'extraction_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
