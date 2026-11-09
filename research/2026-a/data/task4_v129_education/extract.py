"""Verify two V129 nonadmissions without calculating or writing model bounds."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
ROOT = REPO / 'research/2026-a'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(n):
    return json.loads((HERE / n).read_text())


def main():
    registry = ROOT / 'design/task4_user_current_model.json'
    current = json.loads(registry.read_text())
    live = [registry, ROOT / current['source_csv'], ROOT / current['admissions'],
            ROOT / 'scripts' / (current['module'] + '.py'),
            ROOT / current['results'] / 'summary.json']
    before = {str(p.relative_to(REPO)): sha(p) for p in live}
    immutable = read('immutable_source_sha256.json')
    assert all(sha(REPO / n) == h for n,h in immutable.items())
    archive = read('archive_sha256.json')
    assert all(sha(HERE / n) == h for n,h in archive.items())
    sources = read('sources.json')
    for row in sources:
        if row.get('file'):
            assert sha(HERE / row['file']) == row['sha256']
    meta = read('paris_teacher_metadata_original.json')
    scope = meta['metas']['metadonnees-complementaires']['champ']
    assert 'privés sous contrat' in scope and 'établissements du second degré' in scope
    fields = {r['name']: r for r in meta['fields']}
    assert fields['etp_enseignants_hommes_et_femmes']['type'] == 'double'
    assert not any('cycle' in k or 'formation' in k for k in fields)
    assert read('paris_teacher_sample_original.json')['total_count'] == 0
    teachers = read('paris_teacher_henriiv_original.json')['results']
    selected = [r for r in teachers if r['uai']=='0750654D' and r['annee_de_la_rentree_scolaire']=='2025']
    assert len(selected)==1 and selected[0]['etp_enseignants_hommes_et_femmes']==153.65
    assert selected[0]['code_departement']=='75'
    pupils = [r for r in read('paris_pupil_henriiv_original.json')['results']
              if r['numero_lycee']=='0750654D' and r['rentree_scolaire']=='2025']
    assert len(pupils)==1 and pupils[0]['nombre_d_eleves']==794
    annuaire = read('paris_annuaire_henriiv_original.json')['results']
    assert len(annuaire)==1 and annuaire[0]['identifiant_de_l_etablissement']=='0750654D'
    assert annuaire[0]['post_bac']=='1' and annuaire[0]['code_departement']=='075'
    assert annuaire[0]['nom_commune']=='Paris'
    madrid = '\n'.join(b.get('text','') for b in read('madrid_provider_capture.json')['content'])
    assert 'ESO)/Bachillerato' in madrid and 'Unidad: Número' in madrid
    attempts = read('attempts.json')
    assert len(attempts)==2 and all(not r['admitted'] for r in attempts)
    assert read('observations.json')==[]
    assert all(sha(REPO / n)==h for n,h in before.items())
    report = dict(status='pass', access_date='2026-11-09', inspected_routes=2,
        admitted_cells=0, observations_empty=True, no_PTR_or_utility_computed=True,
        archived_files_verified=len(archive),
        original_HTTP_sources_verified=sum(bool(r.get('file')) and r.get('representation','').startswith('original HTTP') for r in sources),
        separate_provider_representations_verified=sum(bool(r.get('file')) and r.get('representation','').startswith('Exa') for r in sources),
        Paris_matched_UAI_year_but_not_stage=True, Paris_teacher_ETP_real=True,
        Paris_private_hors_contrat_not_in_declared_scope=True,
        Paris_school_post_bac_flag_is_current_scope_warning_not_2025_workload=True,
        Madrid_unit_and_combined_stage_provider_representation_verified=True,
        Madrid_original_table_not_recovered=True,
        immutable_live_source_hashes_verified=immutable,
        current_registry_version=current['version'], current_run_before_after_hashes_verified=before,
        registry_may_advance_between_runs=True, model_inputs_written=False)
    (HERE / 'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
