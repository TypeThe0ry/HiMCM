#!/usr/bin/env python3
"""Reconcile manually transcribed official PXU roster against V42 NCES evidence.
Run from any working directory. Requires pdftotext (Poppler); no network.
The catalog roster is an embedded image: visual transcription, NOT PDF-text extraction.
"""
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

def read_csv(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream))

def normalize(address):
    # Catalog omits ST for Wilson's Fillmore address; retain explicit alias.
    address = address.upper().replace('3005 E FILLMORE ST', '3005 E FILLMORE')
    return re.sub(r'[^A-Z0-9]', '', address)

def main():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for source in manifest:
        raw = (HERE / source['file']).read_bytes()
        assert len(raw) == source['bytes'], source['file']
        assert hashlib.sha256(raw).hexdigest() == source['sha256'], source['file']
    roster = read_csv(HERE / 'roster_join.csv')
    nces = {r['NCESSCH']: r for r in read_csv(HERE / '../task4_v42_phoenix_coverage/arizona_school_audit.csv') if r['LEAID'] == '0406330'}
    assert len(roster) == 24 and len(nces) == 21
    assert set(int(r['catalog_number']) for r in roster) == set(range(1, 25))
    assert {r['nces_id'] for r in roster} == set(nces)
    assert sorted(int(r['profile_number']) for r in roster if r['profile_number']) == list(range(1, 24))
    assert sum(r['relation'] == 'co_located_program' for r in roster) == 3
    assert sum(r['nonvirtual'] == 'True' for r in nces.values()) == 20
    assert all(r['within_current_phoenix_boundary'] == 'True' for r in nces.values())
    for row in roster:
        entity = nces[row['nces_id']]
        campus = nces[row['catalog_campus_nces_id']]
        assert normalize(row['catalog_address']) == normalize(campus['LSTREET1']), row['catalog_name']
        assert row['nces_name'] == entity['SCH_NAME']
        assert row['nces_member'] == entity['MEMBER']
        assert campus['within_current_phoenix_boundary'] == row['catalog_campus_current_boundary'] == 'True'
        assert (row['digital_excluded'] == 'True') == (entity['nonvirtual'] == 'False')
    prep = next(r for r in roster if r['catalog_number'] == '23')
    assert prep['profile_number'] == '' and prep['nces_member'] == '0'
    assert prep['catalog_campus_nces_id'] == '040633000538'
    history = (HERE / 'pxu_history.html').read_text()
    assert 'Educator Preparatory, 2023 (closed 2024)' in history
    assert 'Cyber High School' in history and 'closed 2010' in history
    application = subprocess.check_output(['pdftotext', '-layout', str(HERE / 'montessori_application2024.pdf'), '-'], text=True)
    assert 'register online to Camelback High School' in application
    catalog = subprocess.check_output(['pdftotext', '-layout', str(HERE / 'course_catalog2023_24.pdf'), '-'], text=True)
    assert 'C-131' in catalog.split('\f')[138]
    # Reproduce subtraction only; this is conditional arithmetic, not admitted city data.
    counts = []
    for filename, entity_id in [('../task4_v55_phoenix_outcomes/pxu_graduation_fy2025.json', 4286), ('../task4_v9_phoenix/spatial_responses/875776.json', 875776)]:
        rows = [r for r in json.loads((HERE / filename).read_text()) if r['studentGroupDescription'] == 'All']
        assert len(rows) == 1
        row = rows[0]
        assert row['fiscalYear'] == 2025 and row['educationOrganizationId'] == entity_id
        counts.append((row['numGraduated'], row['numInCohort'] - row['numGraduated']))
    (g_district, f_district), (g_digital, f_digital) = counts
    assert counts == [(4813, 1472), (286, 199)]
    result = {
        'official_catalog_school_year': '2023-2024',
        'catalog_roster_pdf_page': 139,
        'catalog_roster_printed_page': 'C-131',
        'catalog_roster_update_date': '2023-07-21',
        'transcription_method': 'Manual visual reading of embedded-image roster; rerender original page139 to inspect. CSV join and hashes are automated.',
        'catalog_named_school_program_count': len(roster),
        'later_profile_school_program_count': 23,
        'nces_survey_year': sorted({r['SURVYEAR'] for r in nces.values()}),
        'nces_entity_count': len(nces),
        'co_located_program_count_without_separate_nces_entity': 3,
        'programs': [r['catalog_name'] for r in roster if r['relation'] == 'co_located_program'],
        'difference_identity': '2023-24 catalog24 = NCES21 + 3co-locatedprograms; 2024-25 profile23 = catalog24 - EducatorPreparatory(closed2024)',
        'roster_unit_discrepancy_resolved': True,
        'all_catalog_addresses_match_current_city_verified_campuses': True,
        'nonvirtual_nces_entities': 20,
        'digital_excluded_nces_id': '040633003578',
        'educator_prep_historical_campus_nces_id': prep['catalog_campus_nces_id'],
        'montessori_parent_registration_confirmed': True,
        'microprogram_graduation_accountability_linkage_confirmed': False,
        'historical_cohort_responsibility_complete': False,
        'conditional_graduate_count': g_district - g_digital,
        'conditional_nongraduate_count': f_district - f_digital,
        'conditional_arithmetic_provenance': 'Exact outcome counts audited in task4_v55_phoenix_outcomes; source JSON retained and hashed here.',
        'main_admitted': False,
        'city_bound_changed': False,
        'remaining_conditions': [
            'District and Digital School cohorts must be linked under compatible unique-person and graduate/non-graduate status rules before status-specific subtraction.',
            'Prove all excluded cohort responsibility is covered, including historical closed entities and off-campus or district-level special placements; current enrollment roster alone is insufficient.',
            'Historical addresses are checked against current Phoenix municipal geometry, not a reconstructed 2023-24 boundary.',
            'Catalog program co-location does not independently establish accountability ownership; Montessori registration evidence applies to that program only.',
            'Inference targets schools physically in Phoenix; open enrollment means city-resident outcomes are a different target.'
        ],
        'source_hashes_verified': len(manifest),
        'no_core_files_modified': True
    }
    (HERE / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('catalog_named_school_program_count', 'nces_entity_count', 'roster_unit_discrepancy_resolved', 'main_admitted', 'city_bound_changed')}, indent=2))

if __name__ == '__main__':
    main()
