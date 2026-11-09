"""Independently verify the V189 joint-mean sensitivity insertion on V181 science."""
from pathlib import Path
import argparse,csv,hashlib,json,math,re,subprocess,xml.etree.ElementTree as E
import numpy as np
from scipy.optimize import brentq
from audit_task4_v184 import graph,norm,pdftext
from audit_task4_v186 import threshold_checks
from task4_user_v181_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';D=P/'drafts';O=R/'results/task4_v189_review';T=Path('/data/scratch')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scores(a,w):
    def one(row):
        b=math.sqrt(math.fsum(float(v)*float(x)**2 for v,x in zip(w,row)))
        g=math.sqrt(math.fsum(float(v)*(1-float(x))**2 for v,x in zip(w,row)))
        return 100*b/(g+b)
    return np.array([one(row) for row in a])
def math_checks():
    certificate=read(R/'results/task4_v187_joint_means/verification.json');assert certificate['status']=='pass'
    for field in ['source_sha256','audited_output_sha256']:
        for name,h in certificate[field].items():assert sha(R/name)==h,name
    f,l,h=revised_bounds();cities=f.city.tolist();z=cities.index('Zurich');j=NAMES.index('travel');m=f.commute_min.to_numpy(float);idx=np.flatnonzero(np.isfinite(m));assert len(idx)==12
    assert [c for i,c in enumerate(cities) if i not in idx]==['Vienna','Warsaw','Singapore','Tokyo']
    summary=read(R/'results/task4_v187_joint_means/summary.json');records=[]
    for ref,w in [('fixed',np.array([.1125]*6+[.05,.1125,.1125,.05])),('equal',np.full(10,.1))]:
        upper=scores(h,w);C=np.array([max(upper[k] for k in range(16) if k!=i) for i in range(16)])
        def values(delta):
            a=l.copy()
            for i in idx:a[i,j]=math.exp(-float(m[i])*(1+delta if i==z else 1-delta)/30)
            lower=scores(a,w);regret=np.maximum(0,C-lower)
            return regret,[cities[i] for i in range(16) if regret[i]<=regret.min()+1e-10]
        def gap(delta):
            v,_=values(delta);return float(v[z]-min(v[i] for i in range(16) if i!=z))
        assert gap(0)<0<gap(1)
        root=float(brentq(gap,0,1,xtol=5e-16,rtol=1e-15));prior=next(x for x in summary['thresholds'] if x['weight_reference']==ref)
        assert abs(root-prior['sharp_radius'])<1e-13
        assert values(root)[1]==['Zurich','Oslo']
        assert values(root-1e-7)[1]==['Zurich'] and values(root+1e-7)[1]==['Oslo']
        records.append(dict(weight_reference=ref,independent_critical_radius=root,critical_percent=root*100,binding_rival='Oslo',gap_below=gap(root-1e-7),gap_at_root=gap(root),gap_above=gap(root+1e-7)))
    return records

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expect-active',action='store_true');parser.add_argument('--source-only',action='store_true');args=parser.parse_args()
    saved=read(O/'protected_files.json');changed=[]
    for name,h in saved['paper'].items():
        if args.expect_active and name=='drafts/task4_current_review.json':changed.append(name);continue
        if args.expect_active and name=='AGENTS.md':
            value=(P/name).read_text();assert value.count('V188 is the frozen preceding review.')==1
            assert hashlib.sha256(value.replace('V188 is the frozen preceding review.','V186 is the frozen preceding review.').encode()).hexdigest()==h
            changed.append(name);continue
        assert sha(P/name)==h,name
    for name,h in saved['registries'].items():
        if args.expect_active and name=='task4_user_current_review.json':continue
        assert sha(R/'design'/name)==h,name
    for name,h in saved['science'].items():assert sha(R/name)==h,name
    frozen=read(R/'results/task4_v186_review/protected_files.json');f,l,h=revised_bounds();assert f.city.tolist()==frozen['cities']
    np.testing.assert_array_equal(l,frozen['lower']);np.testing.assert_array_equal(h,frozen['upper']);assert l.shape==h.shape==(16,10)
    model=read(R/'design/task4_user_current_model.json');extensions=read(R/'design/task4_user_current_extensions.json')
    assert model['version']=='V181' and model['module']=='task4_user_v181_revision'
    assert extensions['extension_version']==extensions['primary_evidence_version']=='V181'
    math_records=math_checks()
    tex=D/'task4_v189_paper.tex';core=D/'task4_v189_core.tex';vintage=D/'task4_v189_vintage.tex'
    old=(D/'task4_v186_vintage.tex').read_text();addition=vintage.read_text();text=norm(addition)
    assert addition.startswith(old.splitlines()[0]+'\n')
    assert addition.count('\\input{task4_v182_assets/vintage_table.tex}')==1
    assert addition.count('\\subsection')==1
    for marker in ['Point withdrawals','48 non-point bounds','28 flagged points','Berlin','Paris','13 pre-2020','Singapore or Zurich','64 post-2025','16.05 to 48.41','95-point union','All sixteen remain possible champions','screening criteria, not error probabilities',"Zurich's homicide",'Amsterdam','0.23002','0.90473','per 100,000','hypothetical rates','other inputs fixed']:
        assert norm(marker) in text,marker
    # Existing single-input and commute-withdrawal science is independently scalar checked.
    prior_checks=threshold_checks();assert len(prior_checks)==2
    assert core.read_text()==(D/'task4_v186_core.tex').read_text().replace('task4_v186_vintage.tex','task4_v189_vintage.tex')
    assert 'tcn=18213' in tex.read_text() and tex.read_text().count('task4_v189_core.tex')==1
    # Version comment aside, wrapper changes only its owned core input path.
    normalize=lambda value:'\n'.join(value.splitlines()[1:])
    assert normalize(tex.read_text())==normalize((D/'task4_v188_paper.tex').read_text()).replace('task4_v186_core.tex','task4_v189_core.tex')
    assert norm('these withdrawals retain sixteen possible champions') in text
    assert '46.59' in text and 'every nonnegative mean' in text
    for marker in ['7.14733','51.42357','Oslo','Jensen'] :assert marker in text,marker
    assert 'Singapore' in text
    # Formula and precise threshold interpretation are reviewed alongside these guards.
    assert '\\delta' in addition and '(1-' in addition and '(1+' in addition
    assert 'below' in text.lower() and 'tie' in text.lower() and ('counterexample' in text.lower() or 'counterexamples' in text.lower())
    assert 'conditional ranges' in text.lower() and 'not measured errors or future probabilities' in text.lower()
    assert not any(x in text for x in ['95%','7.15\\%','51.42\\%'])
    manifest=read(D/'task4_v189_manifest.json')
    for name,digest in manifest.get('source_sha256',{}).items():assert sha(R/name)==digest,name
    for name,digest in manifest.get('paper_input_sha256',{}).items():assert sha(P/name)==digest,name
    source_scope=dict(whole_owned5_5_compressed=True,prior_decision_results_and_material_conditions_preserved=True,removed_point_year_flag_subcounts_remain_in_frozen_V186=True,all_other_core_content_byte_preserved=True,wrapper_only_input_path_and_comment=True,sixteen_possible_scope='Withdrawal checks only; not the whole mean box domain',joint_scope='Twelve finite CSV means; unchanged Jensen uppers, SG bins, unknown travel and other criteria',joint_interpretation='Below computed boundary unique Zurich throughout box; boundary Oslo tie attainable; above a counterexample exists; radius is hypothetical')
    if args.source_only:print(json.dumps(dict(status='pass',math=math_records,scope=source_scope),indent=2));return
    pdf=D/'task4_v189_paper.pdf';proxy=T/'himcm_v189_proxy/task4_v189_review_entry.pdf'
    pages=[norm(s) for s in pdftext(pdf).split('\f') if s.strip()];assert len(pages)==27
    assert pages==[norm(s) for s in pdftext(proxy).split('\f') if s.strip()]
    aux=(T/'himcm_v189_build/task4_v189_paper.aux').read_text();oldaux=(R/'results/task4_v186_review/direct_labels.aux').read_text()
    label=lambda name:int(re.search(r'\\newlabel\{'+re.escape(name)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
    assert label('main-end')==25 and label('LastPage')==27 and [label('news-start'),label('news-end')]==[18,19]
    refs=lambda value:set(re.findall(r'\\bibcite\{([^}]+)\}',value))
    assert refs(aux)==refs(oldaux) and len(refs(aux))==53
    nodes=E.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'])).findall('.//{http://www.w3.org/1999/xhtml}page')
    for i,node in enumerate(nodes):
        assert (float(node.get('width')),float(node.get('height')))==(612,792)
        words=node.findall('.//{http://www.w3.org/1999/xhtml}word');assert not any(float(w.get('yMin'))>745 for w in words)
        top=[w for w in words if float(w.get('yMin'))<65]
        if i:
            assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
            assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
            assert any(w.text=='18213' for w in top) and f'Page {i+1} of 27' in pages[i]
        else:assert '18213' in pages[0] and 'PENDING' not in pages[0]
    for folder,name in [('himcm_v189_build','task4_v189_paper'),('himcm_v189_proxy','task4_v189_review_entry')]:
        log=(T/folder/(name+'.log')).read_text();assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning']);assert log.count('Underfull')==2
    fontxml=T/'himcm_v189_fonts.xml';subprocess.run(['pdftohtml','-xml','-hidden','-zoom','1.0',str(pdf),str(fontxml)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    fonts={};sizes=[];font_markers=set()
    for page in E.parse(fontxml).getroot().findall('page'):
        for font in page.findall('fontspec'):fonts[font.get('id')]=font.attrib
        for span in page.findall('text'):
            value=''.join(span.itertext()).strip()
            if any(x in value for x in ['7.14733','51.42357']):
                sizes.append(int(fonts[span.get('font')]['size']));font_markers.update(x for x in ['7.14733','51.42357'] if x in value)
    assert font_markers=={'7.14733','51.42357'} and min(sizes)==12
    requirements=list(csv.DictReader((R/'results/task4_v188_review/requirements.csv').open()));current=list(csv.DictReader((O/'requirements.csv').open()))
    assert len(requirements)==len(current)==47 and {x['id']:x['status'] for x in current}=={x['id']:x['status'] for x in requirements}
    pending=[x['id'] for x in current if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==13
    if args.expect_active:
        review=read(R/'design/task4_user_current_review.json');assert review==read(D/'task4_current_review.json')
        assert review['version']=='V189' and review['primary_model']=='V181' and review['pdf_sha256']==sha(pdf) and not review['submission_ready']
    value=read(R/'design/task4_user_format_reference.json');assert value['actual_control_number']=='PENDING' and value['actual_registered_number_verified'] is False
    assert value['display_control_number']=='18213' and value['display_number_provisional'] is True
    files=graph(tex)
    result=dict(version='V189',status='pass',primary_model='V181',activation_status='active' if args.expect_active else 'verified_pending_activation',total_pages=27,main_and_references_pages=25,main_page_margin=0,news_pages=[18,19],AI_pages=[26,27],compiled_references=53,prior53_reference_keys_exact=True,scientific_files_unchanged=len(saved['science']),existing_manuscript_files_unchanged=len(saved['paper'])-len(changed),owned_pointer_files_changed=changed,original_user_CSV_and_all160bounds_unchanged=True,current_model_extensions_unchanged=True,shared_main_ref_class_unchanged=True,figures_numerical_assets_references_AI_byte_unchanged=True,primary_admissions=0,actual_baseline_width_change=0,joint_threshold_checks=math_records,edit_scope_checks=source_scope,direct_root_text_equal=True,native_header_footer_checked=True,display_control_number='18213',actual_registered_number_verified=False,new_threshold_font_extractor_size_min=min(sizes),overfull_boxes=0,underfull_paragraphs_per_build=2,requirements=47,prior47_statuses_preserved=True,pending_gates_preserved=pending,submission_ready=False,server_compile_verified=False,default_main_setting_changed=False,AI_history_complete=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),joint_certificate_sha256=sha(R/'results/task4_v187_joint_means/verification.json'),verifier_sha256=sha(Path(__file__)),tex_source_sha256={str(p.relative_to(P)):sha(p) for p in sorted(files)},visual_review_scope='Separate parent raster review; this audit checks text, bounds, fonts and header/footer geometry.')
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='tex_source_sha256'},indent=2))
if __name__=='__main__':main()
