"""Join Paris pupil/teacher records while retaining institution/site ambiguity."""
import argparse,csv,json
from collections import defaultdict,Counter
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'data/current_paris_teacher_join'
def read(n):return json.loads((D/n).read_text(),parse_float=Decimal)
def dump(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def write(p,rr):
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rr[0]),lineterminator='\n');w.writeheader();w.writerows(rr)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True)
    out=ap.parse_args().output_dir.resolve()
    if out.exists():raise FileExistsError('Use a new output directory')
    t=read('teacher_paris2025.json');assert len(t)==len({x['uai'] for x in t})
    teachers={x['uai']:x for x in t};pupils=[]
    for n in ['gt_paris75.json','pro_paris75.json']:
        selected=[x for x in read(n) if x['rentree_scolaire']=='2025']
        assert len(selected)==len({x['numero_lycee'] for x in selected})
        pupils.append({x['numero_lycee']:x for x in selected})
    gt,pro=pupils;ids=sorted(gt.keys()|pro.keys())
    candidates=defaultdict(list);flat=[]
    a=read('annuaire_paris_lycee.json');extra=read('annuaire_other_types.json')
    assert extra['total_count']==len(extra['results'])
    for file,rr in [('annuaire_paris_lycee.json',a),('annuaire_other_types.json',extra['results'])]:
        for r in rr:
            k=r['identifiant_de_l_etablissement'];candidates[k].append(r)
            flat.append(dict(UAI=k,source_file=file,candidate_index=len(candidates[k]),
                name=r['nom_etablissement'],institution_type=r['type_etablissement'],
                public_private=r['statut_public_prive'],contract=r['type_contrat_prive'],
                post_bac=r['post_bac'],state=r['etat'],current_row_update=r['date_maj_ligne']))
    review=[]
    for k,rr in sorted(candidates.items()):
        flags={x['post_bac'] for x in rr}
        state='mixed_site_flags' if len(flags)>1 else {None:'unknown','0':'no_postbac_flag','1':'postbac_flag'}[next(iter(flags))]
        review.append(dict(UAI=k,current_candidate_rows=len(rr),current_postbac_flags_json=dump(sorted(flags,key=str)),
            current_postbac_state=state,current_contracts_json=dump(sorted({x['type_contrat_prive'] for x in rr})),
            teacher2025_record_exists=k in teachers,pupil2025_record_exists=k in ids))
    states={r['UAI']:r['current_postbac_state'] for r in review};joined=[]
    for k in ids:
        tr=teachers.get(k);gg=gt.get(k);pp=pro.get(k)
        assert k in states
        joined.append(dict(UAI=k,GT_record_exists=gg is not None,PRO_record_exists=pp is not None,
            GT_pupils=None if gg is None else gg['nombre_d_eleves'],PRO_pupils=None if pp is None else pp['nombre_d_eleves'],
            teacher_record_exists=tr is not None,teacher_FTE=None if tr is None else tr['etp_enseignants_hommes_et_femmes'],
            teacher_institution_type=None if tr is None else tr['nature_de_l_etablissement'],
            teacher_sector=None if tr is None else tr['secteur'],current_candidates=len(candidates[k]),current_postbac_state=states[k],
            original_city_PTR_admissible=False))
    matched=[r for r in joined if r['teacher_record_exists']];assert all(r['teacher_FTE'] is not None for r in matched)
    overlap=set(gt)&set(pro);sum_fte=lambda keys:sum((teachers[k]['etp_enseignants_hommes_et_femmes'] for k in keys),Decimal(0))
    missing=sorted(set(ids)-teachers.keys())
    summary=dict(teacher_rows=len(t),teacher_unique_UAIs=len(teachers),teacher_null_FTE_records=sum(x['etp_enseignants_hommes_et_femmes'] is None for x in t),
        GT2025_rows=len(gt),PRO2025_rows=len(pro),GT_PRO_overlap=len(overlap),pupil_union_UAIs=len(ids),
        GT_pupils=sum(x['nombre_d_eleves'] for x in gt.values()),PRO_pupils=sum(x['nombre_d_eleves'] for x in pro.values()),
        matched_teacher_UAIs=len(matched),unmatched_teacher_UAIs=missing,
        unmatched_teacher_pupils=sum((gt[k]['nombre_d_eleves'] if k in gt else 0)+(pro[k]['nombre_d_eleves'] if k in pro else 0) for k in missing),
        unique_matched_teacher_FTE=str(sum_fte(set(ids)&teachers.keys())),duplicated_FTE_if_joining_GT_and_PRO_separately=str(sum_fte(overlap&teachers.keys())),
        annuaire_lycee_rows=len(a),annuaire_lycee_unique_UAIs=len({x['identifiant_de_l_etablissement'] for x in a}),
        annuaire_extra_EREA_records=len(extra['results']),annuaire_candidate_rows=len(flat),annuaire_unique_UAIs=len(candidates),
        multiple_candidate_UAIs=[r['UAI'] for r in review if r['current_candidate_rows']>1],
        mixed_postbac_UAIs=[r['UAI'] for r in review if r['current_postbac_state']=='mixed_site_flags'],
        pupil_union_current_postbac_states=dict(Counter(r['current_postbac_state'] for r in joined)),
        current_HORS_CONTRAT_UAIs=len({x['identifiant_de_l_etablissement'] for x in a if x['type_contrat_prive']=='HORS CONTRAT'}),
        current_partial_contract_UAIs=len({x['identifiant_de_l_etablissement'] for x in a if x['type_contrat_prive']=='CONTRAT ASSOCIATION PARTIE DES CLASSES'}),
        primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
        scope='Exact UAI source joins; institution teacher FTE counted once, no PTR or ratio computed. Current site flags are not historical2025 allocations; public/contract coverage is not all-provider coverage. Missing records and subgroup nulls remain unfilled.')
    out.mkdir(parents=True);write(out/'pupil_teacher_join.csv',joined);write(out/'annuaire_candidates.csv',flat);write(out/'annuaire_key_review.csv',review)
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
