"""Verify the owned one-block candidate, its rendered scope, and frozen inputs."""
from pathlib import Path
import hashlib,json,re,subprocess
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
P=Path('/data/projects/HiMCM-Overleaf')
O=R/'results/task4_v159_review'
T=Path('/data/scratch')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p):return subprocess.check_output(['pdftotext',str(p),'-'],text=True)

def main():
    prior=json.loads((R/'results/task4_v158_joint_gap/summary.json').read_text())
    snapshot=json.loads((R/'design/task4_user_v154_snapshot.json').read_text())['source_sha256']
    for n,h in snapshot.items():assert sha(R/n)==h,n
    names=subprocess.check_output(['git','-C',str(P),'ls-files','-z']).decode().split('\0')
    guard=O/'protected_files.json'
    protected=(json.loads(guard.read_text())['manuscript'] if guard.exists() else {n:sha(P/n) for n in names if n})
    for n,h in protected.items():assert sha(P/n)==h,n
    for n,h in prior['manuscript_files_unchanged_sha256'].items():assert protected[n]==h,n
    delivery=json.loads((R/'results/task4_v158_joint_gap/delivery.json').read_text())
    for n,h in delivery['selected_file_sha256'].items():assert protected[n]==h,n
    core=(P/'drafts/task4_v154_core.tex').read_text();new=(P/'drafts/task4_v159_core.tex').read_text()
    a=core.index('For future access measurement,');z=core.index('\\AgeCase',a)
    assert new.startswith(core[:a]) and new.endswith(core[z:])
    for value in ['0.226686','0.374445','0.147759']:
        assert value in new
    row=next(x for x in prior['rows'] if x['alpha']==.2)
    for k,v in [('sharp_joint_lower','0.226686'),('witness_mean','0.374445'),('witness_lower_tail','0.147759')]:assert f'{row[k]:.6f}'==v
    pdf=P/'drafts/task4_v159_paper.pdf';proxy=T/'himcm_v159_proxy/task4_v159_review_entry.pdf'
    pages=text(pdf).split('\f');pages=[x for x in pages if x.strip()]
    assert len(pages)==24
    normalize=lambda x:re.sub(r'\s+',' ',x).strip()
    assert normalize(text(pdf))==normalize(text(proxy))
    assert '0.226686' in pages[13] and '2012' in pages[13]
    unchanged=[];changed=[]
    for i in range(1,25):
        old=Image.open(T/f'himcm_v159_base_render/base-{i:02}.png').convert('RGB')
        current=Image.open(T/f'himcm_v159_render/final-{i:02}.png').convert('RGB')
        (unchanged if old.size==current.size and ImageChops.difference(old,current).getbbox() is None else changed).append(i)
    assert changed==[9,14],changed
    basepages=text(P/'drafts/task4_v154_paper.pdf').split('\f')
    for i in range(24):
        if i!=13: assert normalize(basepages[i])==normalize(pages[i]),i+1
    log=(O/'direct_build.log').read_text()
    assert not re.search(r'Overfull|Underfull|LaTeX Warning|undefined',log)
    aux=(T/'himcm_v159_build/task4_v159_paper.aux').read_text()
    assert len(re.findall(r'\\bibcite\{',aux))==47
    for label,page in [('news-start',16),('news-end',17),('main-end',22),('LastPage',24)]:
        match=re.search(r'\\newlabel\{'+label+r'\}\{\{[^}]*\}\{(\d+)\}',aux)
        assert match and int(match[1])==page,(label,match)
    assert 'framework.png' in (O/'shared_main_stdout.txt').read_text()
    result=dict(status='pass',iteration='V159 candidate',active_model_and_paper='V154 unchanged',pages=24,main_and_references_pages=22,provisional_AI_pages=2,compiled_references=47,
                changed_rendered_pages=changed,unchanged_rendered_pages=unchanged,
                unchanged_text_pages=[i for i in range(1,25) if i!=14],
                page9_difference='One unchanged equation-definition line has glyph spacing differences; normalized text identical; bbox at 1050px: [79,190,655,206]',render_scale_to_pixels=1050,all_pages_visually_reviewed=True,page14_full_view_reviewed=True,
                direct_warnings=0,root_proxy_text_equal=True,root_proxy_server_compile_verified=False,shared_main_existing_failure='framework.png missing',
                protected_scientific_files=len(snapshot),protected_manuscript_files=len(protected),
                team_control_number='PENDING',AI_history_complete=False,submission_ready=False,project_settings_changed=False,
                primary_data_admissions=0,primary_score_width_change=0,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),
                old_pdf_sha256=sha(P/'drafts/task4_v154_paper.pdf'),verifier_sha256=sha(Path(__file__)))
    (O/'protected_files.json').write_text(json.dumps({'science':snapshot,'manuscript':protected},indent=2)+'\n')
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
