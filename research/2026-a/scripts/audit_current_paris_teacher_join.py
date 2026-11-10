"""Audit raw Paris joins without turning whole-institution FTE into city PTR."""
import csv,hashlib,json,subprocess,sys,tempfile
from collections import Counter,defaultdict
from decimal import Decimal
from pathlib import Path
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
R=Path(__file__).resolve().parents[1];G=R.parents[1];D=R/'data/current_paris_teacher_join';O=R/'results/current_paris_teacher_join'
def read(p):return json.loads(p.read_text(),parse_float=Decimal)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    a=audit_parser(__doc__).parse_args();canonical=O/'verification.json';check_output(a,canonical,G)
    before=protected_inputs();receipts=list(D.glob('*.receipt.json'));assert len(receipts)==7
    for p in receipts:
        m=read(p);body=D/p.name.removesuffix('.receipt.json')
        assert m['status']==200 and sha(body)==m['sha256'] and body.stat().st_size==m['bytes']
    assert read(D/'gt_paris.json')==read(D/'pro_paris.json')==[]
    old=R/'data/task4_v129_education';meta=read(old/'paris_teacher_metadata_original.json')
    fields={x['name']:x for x in meta['fields']};assert fields['etp_enseignants_hommes_et_femmes']['type']=='double'
    scope=meta['metas']['metadonnees-complementaires']['champ'];assert 'hospitaliers' in scope and 'publics ou privés sous contrat' in scope
    assert '75'==read(old/'paris_pupil_henriiv_original.json')['results'][0]['code_departement_pays']
    teacher=read(D/'teacher_paris2025.json');assert len(teacher)==339
    assert {x['annee_de_la_rentree_scolaire'] for x in teacher}=={'2025'} and {x['code_departement'] for x in teacher}=={'75'}
    tt={r['uai']:r for r in teacher};assert len(tt)==339
    assert sum(r['etp_enseignants_hommes_et_femmes'] is None for r in teacher)==2
    pupils=[]
    for n,count in [('gt_paris75.json',122),('pro_paris75.json',59)]:
        selected=[r for r in read(D/n) if r['rentree_scolaire']=='2025'];assert len(selected)==count
        assert len({r['numero_lycee'] for r in selected})==count
        assert all(r['nombre_d_eleves'] is not None and r['nombre_d_eleves']>0 for r in selected)
        assert {r['commune'] for r in selected}=={'PARIS'};pupils.append({r['numero_lycee']:r for r in selected})
    gt,pro=pupils;keys=set(gt)|set(pro);both=set(gt)&set(pro);assert len(keys)==154 and len(both)==27
    assert sum(r['nombre_d_eleves'] for r in gt.values())==57460
    assert sum(r['nombre_d_eleves'] for r in pro.values())==14167
    assert keys-tt.keys()=={'0754401B'} and gt['0754401B']['nombre_d_eleves']==117
    assert sum((tt[k]['etp_enseignants_hommes_et_femmes'] for k in keys&tt.keys()),Decimal(0))==Decimal('7920.09')
    assert sum((tt[k]['etp_enseignants_hommes_et_femmes'] for k in both),Decimal(0))==Decimal('1870.52')
    ann=read(D/'annuaire_paris_lycee.json');extra=read(D/'annuaire_other_types.json');assert len(ann)==243 and extra['total_count']==3
    assert {r['type_etablissement'] for r in extra['results']}=={'EREA'}
    assert {r['identifiant_de_l_etablissement'] for r in extra['results']}=={'0750828T','0752799K','0753256G'}
    by=defaultdict(list)
    for r in ann+extra['results']:by[r['identifiant_de_l_etablissement']].append(r)
    assert len(by)==240 and len({r['identifiant_de_l_etablissement'] for r in ann})==237
    assert len([k for k,v in by.items() if len(v)>1])==6
    mixed={k for k,v in by.items() if len({r['post_bac'] for r in v})>1};assert mixed=={'0750651A','0750711R','0750770E','0750787Y'}
    classified={}
    for k,v in by.items():
        flags={r['post_bac'] for r in v}
        classified[k]='mixed_site_flags' if len(flags)>1 else {None:'unknown','0':'no_postbac_flag','1':'postbac_flag'}[next(iter(flags))]
    assert Counter(classified[k] for k in keys)=={'postbac_flag':88,'no_postbac_flag':60,'mixed_site_flags':4,'unknown':2}
    joined=rows(O/'pupil_teacher_join.csv');assert len(joined)==154 and {r['UAI'] for r in joined}==keys
    for r in joined:
        k=r['UAI'];assert r['GT_record_exists']==str(k in gt) and r['PRO_record_exists']==str(k in pro)
        assert r['GT_pupils']==(str(gt[k]['nombre_d_eleves']) if k in gt else '')
        assert r['PRO_pupils']==(str(pro[k]['nombre_d_eleves']) if k in pro else '')
        assert r['teacher_record_exists']==str(k in tt) and r['original_city_PTR_admissible']=='False'
        if k in tt:
            assert Decimal(r['teacher_FTE'])==tt[k]['etp_enseignants_hommes_et_femmes']
            assert r['teacher_institution_type']==tt[k]['nature_de_l_etablissement'] and r['teacher_sector']==tt[k]['secteur']
        else:assert r['teacher_FTE']==r['teacher_institution_type']==r['teacher_sector']==''
        assert int(r['current_candidates'])==len(by[k]) and r['current_postbac_state']==classified[k]
    flat=rows(O/'annuaire_candidates.csv');assert len(flat)==246
    expected=Counter((r['identifiant_de_l_etablissement'],r['nom_etablissement'],str(r['post_bac']) if r['post_bac'] is not None else '',r['type_contrat_prive'],r['type_etablissement'],r['statut_public_prive'],r['etat'],r['date_maj_ligne']) for r in ann+extra['results'])
    assert Counter((r['UAI'],r['name'],r['post_bac'],r['contract'],r['institution_type'],r['public_private'],r['state'],r['current_row_update']) for r in flat)==expected
    review=rows(O/'annuaire_key_review.csv');assert len(review)==240
    for r in review:
        k=r['UAI'];assert int(r['current_candidate_rows'])==len(by[k]) and r['current_postbac_state']==classified[k]
        assert set(json.loads(r['current_postbac_flags_json']))=={x['post_bac'] for x in by[k]}
        assert set(json.loads(r['current_contracts_json']))=={x['type_contrat_prive'] for x in by[k]}
        assert r['teacher2025_record_exists']==str(k in tt) and r['pupil2025_record_exists']==str(k in keys)
    s=read(O/'summary.json');assert s['unique_matched_teacher_FTE']=='7920.09' and s['duplicated_FTE_if_joining_GT_and_PRO_separately']=='1870.52'
    assert s['current_HORS_CONTRAT_UAIs']==len({r['identifiant_de_l_etablissement'] for r in ann if r['type_contrat_prive']=='HORS CONTRAT'})==45
    assert s['current_partial_contract_UAIs']==len({r['identifiant_de_l_etablissement'] for r in ann if r['type_contrat_prive']=='CONTRAT ASSOCIATION PARTIE DES CLASSES'})==8
    with tempfile.TemporaryDirectory(prefix='himcm-paris-join-',dir='/data/scratch') as tmp:
        out=Path(tmp)/'replay';subprocess.run([sys.executable,str(R/'scripts/task4_current_paris_teacher_join.py'),'--output-dir',str(out)],check=True,stdout=subprocess.PIPE)
        for n in ['summary.json','pupil_teacher_join.csv','annuaire_candidates.csv','annuaire_key_review.csv']:assert (out/n).read_bytes()==(O/n).read_bytes()
    assert protected_inputs()==before
    for n,h in read(R/'results/current_paper_review/current_verification.json')['edition_source_sha256'].items():assert sha(R/n)==h,n
    files=[*sorted(D.iterdir()),*[O/n for n in ['README.md','summary.json','pupil_teacher_join.csv','annuaire_candidates.csv','annuaire_key_review.csv','peer_review.json']],
        old/'paris_teacher_metadata_original.json',old/'paris_gt_pupil_metadata_original.json',old/'paris_pro_pupil_metadata_original.json',old/'paris_pupil_henriiv_original.json',
        R/'scripts/task4_current_paris_teacher_join.py',Path(__file__)]
    report=dict(status='pass bounded exact-UAI Paris source joins',**before,edition_entries_checked=24,HTTP200_originals=7,wrong_code_empty_arrays=2,
        teacher_records_checked=339,pupil2025_UAIs=154,teacher_matches=153,teacher_missing_UAI='0754401B',teacher_missing_pupils=117,
        overlapping_GT_PRO_UAIs=27,unique_matched_teacher_FTE='7920.09',avoided_duplicate_FTE='1870.52',
        annuaire_candidate_rows=246,annuaire_distinct_UAIs=240,multiple_candidate_UAIs=6,mixed_site_flag_UAIs=4,EREA_exact_key_matches=3,
        output_files_bytewise_reproduced=4,all_provider_upper_stage_PTR_certified=False,primary_admissions=0,actual_primary_width_reduction=0,
        changes_primary_model=False,changes_manuscript=False,source_sha256={str(p.relative_to(R)):sha(p) for p in files if p.is_file()},
        scope='Count institution FTE once while retaining site candidate sets; missing/suppressed records not zero, current flags not historical allocation. No city ratio, score or hard coverage bound.')
    emit_report(report,a,canonical,G)
if __name__=='__main__':main()
