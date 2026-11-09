"""Independently verify the provisional-number-only owned V188 review."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,xml.etree.ElementTree as E
import numpy as np
from audit_task4_v184 import graph,norm,pdftext
from task4_user_v181_revision import revised_bounds
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';D=P/'drafts';O=R/'results/task4_v188_review';T=Path('/data/scratch')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bbox(pdf):
    raw=subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'])
    return E.fromstring(raw).findall('.//{http://www.w3.org/1999/xhtml}page')
def words(node):return node.findall('.//{http://www.w3.org/1999/xhtml}word')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expect-active',action='store_true');args=parser.parse_args()
    saved=read(O/'protected_files.json');changed=[]
    for name,h in saved['paper'].items():
        if args.expect_active and name=='drafts/task4_current_review.json':changed.append(name);continue
        if args.expect_active and name=='AGENTS.md':
            value=(P/name).read_text();assert value.count('V186 is the frozen preceding review.')==1
            assert hashlib.sha256(value.replace('V186 is the frozen preceding review.','V184 is the frozen preceding review.').encode()).hexdigest()==h
            changed.append(name);continue
        assert sha(P/name)==h,name
    for name,h in saved['registries'].items():
        if args.expect_active and name=='task4_user_current_review.json':continue
        assert sha(R/'design'/name)==h,name
    v186=read(R/'results/task4_v186_review/protected_files.json')
    for name,h in v186['science'].items():assert sha(R/name)==h,name
    f,l,u=revised_bounds();assert f.city.tolist()==v186['cities'];np.testing.assert_array_equal(l,v186['lower']);np.testing.assert_array_equal(u,v186['upper'])
    assert l.shape==u.shape==(16,10)
    model=read(R/'design/task4_user_current_model.json');extensions=read(R/'design/task4_user_current_extensions.json')
    assert model['version']=='V181' and model['module']=='task4_user_v181_revision'
    assert extensions['extension_version']==extensions['primary_evidence_version']=='V181'
    tex=D/'task4_v188_paper.tex';old=D/'task4_v186_paper.tex'
    expected=old.read_text().replace('% V186 owned review;','% V188 owned review; provisional template number, registration unverified;').replace('tcn=PENDING','tcn=18213')
    assert tex.read_text()==expected and tex.read_text().count('tcn=18213')==1
    new_graph=graph(tex);old_graph=graph(old)
    assert new_graph-{tex.resolve()}==old_graph-{old.resolve()}
    manifest=read(D/'task4_v188_manifest.json');assert manifest['display_control_number']=='18213' and not manifest['actual_registered_number_verified'] and not manifest['submission_ready']
    for name,h in manifest['source_sha256'].items():assert sha(P/name)==h,name
    pdf=D/'task4_v188_paper.pdf';proxy=T/'himcm_v188_proxy/task4_v188_review_entry.pdf'
    pages=[norm(s) for s in pdftext(pdf).split('\f') if s.strip()]
    oldpages=[norm(s) for s in pdftext(D/'task4_v186_paper.pdf').split('\f') if s.strip()]
    proxypages=[norm(s) for s in pdftext(proxy).split('\f') if s.strip()]
    assert pages==proxypages and len(pages)==len(oldpages)==27
    for a,b in zip(pages,oldpages):assert a.replace('18213','PENDING')==b
    aux=(T/'himcm_v188_build/task4_v188_paper.aux').read_text()
    oldaux=(R/'results/task4_v186_review/direct_labels.aux').read_text()
    labels=lambda value:dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',value))
    newlabels=labels(aux);assert newlabels==labels(oldaux)
    assert newlabels['main-end']=='25' and newlabels['LastPage']=='27' and newlabels['news-start']=='18' and newlabels['news-end']=='19'
    refs=lambda value:set(re.findall(r'\\bibcite\{([^}]+)\}',value))
    assert refs(aux)==refs(oldaux) and len(refs(aux))==53
    nodes=bbox(pdf);oldnodes=bbox(D/'task4_v186_paper.pdf');assert len(nodes)==27
    for i,(node,oldnode) in enumerate(zip(nodes,oldnodes)):
        assert (float(node.get('width')),float(node.get('height')))==(612,792)
        ww=words(node);assert not any(float(w.get('yMin'))>745 for w in ww)
        top=[w for w in ww if float(w.get('yMin'))<65]
        if i:
            assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
            assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
            assert any(w.text=='18213' for w in top)
            assert f'Page {i+1} of 27' in pages[i]
            body=[w for w in ww if float(w.get('yMin'))>=65]
            oldbody=[w for w in words(oldnode) if float(w.get('yMin'))>=65]
            assert len(body)==len(oldbody)
            for a,b in zip(body,oldbody):
                assert a.text==b.text
                for k in ['xMin','xMax','yMin','yMax']:assert abs(float(a.get(k))-float(b.get(k)))<1e-5,(i+1,a.text,k)
        else:
            assert not any(w.text=='Page' for w in top)
            assert not any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
            assert '18213' in pages[0] and 'PENDING' not in pages[0]
    for folder,name in [('himcm_v188_build','task4_v188_paper'),('himcm_v188_proxy','task4_v188_review_entry')]:
        log=(T/folder/(name+'.log')).read_text()
        assert not any(s in log for s in ['Overfull','undefined','LaTeX Warning'])
        assert log.count('Underfull')==2
    import csv
    requirements=list(csv.DictReader((R/'results/task4_v186_review/requirements.csv').open()))
    assert len(requirements)==47
    current_requirements=list(csv.DictReader((O/'requirements.csv').open()))
    assert {x['id']:x['status'] for x in current_requirements}=={x['id']:x['status'] for x in requirements}
    assert len(current_requirements)==47
    pending=[x['id'] for x in requirements if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}]
    assert len(pending)==13 and 'CI-control' in pending
    if args.expect_active:
        review=read(R/'design/task4_user_current_review.json');assert review==read(D/'task4_current_review.json')
        assert review['version']=='V188' and review['primary_model']=='V181' and review['pdf_sha256']==sha(pdf) and not review['submission_ready']
        value=read(R/'design/task4_user_format_reference.json')
        assert value['actual_control_number']=='PENDING' and not value['actual_registered_number_verified']
        assert value['display_control_number']=='18213' and value['display_number_provisional'] is True
    else:assert sha(R/'design/task4_user_format_reference.json')==saved['format_reference']
    source_files=[tex,old,D/'task4_v188_manifest.json',D/'build_task4_v188.py',P/'task4_v188_review_entry.tex',Path(__file__),O/'protected_files.json']
    result=dict(version='V188',status='pass',primary_model='V181',activation_status='active' if args.expect_active else 'verified_pending_activation',edit_scope='Owned wrapper provisional tcn and version comment only; all content dependencies unchanged',display_control_number='18213',actual_registered_number_verified=False,provisional_control_number=True,total_pages=27,main_and_references_pages=25,main_page_margin=0,news_pages=[18,19],AI_pages=[26,27],compiled_references=53,prior53_reference_keys_exact=True,body_text_all27pages_exact_except_summary_number=True,body_word_positions_pages2to27_exact=True,all_content_input_paths_unchanged=True,direct_root_text_equal=True,native_header_footer_checked=True,summary_native_number_updated=True,overfull_boxes=0,underfull_paragraphs_per_build=2,scientific_files_unchanged=len(v186['science']),existing_manuscript_files_unchanged=len(saved['paper'])-len(changed),owned_pointer_files_changed=changed,original_user_CSV_and_all160bounds_unchanged=True,current_model_extensions_unchanged=True,shared_main_ref_class_unchanged=True,figures_numerical_assets_references_AI_byte_unchanged=True,primary_admissions=0,actual_baseline_width_change=0,requirements=47,prior47_statuses_preserved=True,pending_gates_preserved=pending,submission_ready=False,server_compile_verified=False,default_main_setting_changed=False,AI_history_complete=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),tex_source_sha256={str(p.relative_to(P)):sha(p) for p in sorted(new_graph)},source_sha256={str(p):sha(p) for p in source_files},visual_review_scope='Parent visual review separate; this verifier checks bbox/text preservation and native header/footer geometry, not raster appearance.')
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'source_sha256','tex_source_sha256'}},indent=2))
if __name__=='__main__':main()
