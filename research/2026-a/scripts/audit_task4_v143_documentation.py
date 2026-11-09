"""Check source-policy sensitivity delivery while freezing V136/V137 science."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1];PAPER=ROOT.parents[2]/'HiMCM-Overleaf';OUT=ROOT/'results/task4_v143_documentation';BASE='043ab6f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=PAPER)
def main():
    frozen={}
    for file,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(read(ROOT/file)[key])
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    report=read(ROOT/'results/task4_v143_vintage/verification.json');summary=read(ROOT/'results/task4_v143_vintage/summary.json')
    assert report['status']=='pass' and report['independently_recomputed_city_cases']==160
    for name,digest in report['result_sha256'].items():assert sha(ROOT/name)==digest,name
    assert sha(ROOT/'scripts/audit_task4_v143_vintage.py')==report['verifier_sha256']
    assets='drafts/task4_v137_assets/'
    previous=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',assets],cwd=PAPER,text=True).splitlines()
    retained=[name for name in previous if Path(name).name not in {'manifest.json','qa.json','README.md'}]
    retained += ['drafts/task4_v137_generated.tex']+[f'drafts/task4_v137_{n}.tex' for n in ['paper','ai','references']]
    for name in retained:assert (PAPER/name).read_bytes()==old(name),name
    manifest=read(PAPER/assets/'manifest.json');qa=read(PAPER/assets/'qa.json');pdf=PAPER/'drafts/task4_v137_paper.pdf'
    assert manifest['documentation_revision']==qa['documentation_revision']=='V143'
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    for name,digest in manifest['protected_files'].items():assert sha(PAPER/name)==digest,name
    for name,digest in manifest['manuscript_source_sha256'].items():assert sha(PAPER/'drafts'/name)==digest,name
    for name,digest in manifest['generated_vintage_sha256'].items():assert sha(PAPER/assets/name)==digest,name
    assert sha(PAPER/assets/'revision.tex')==manifest['generated_revision_sha256']
    for dest,src in [('summary.json','summary.json'),('verification.json','verification.json'),('points.csv','submitted_points.csv')]:assert (PAPER/assets/('vintage_'+dest)).read_bytes()==(ROOT/'results/task4_v143_vintage'/src).read_bytes()
    labels={'baseline':'Retained input','pre2020_points':'Before 2020','after2025_points':'After 2025','non_ok_points':'Non-ok flags','union_points':'Union'}
    table=(PAPER/assets/'vintage_table.tex').read_text()
    for case,label in labels.items():
        a=next(x for x in summary['cases'] if x['scenario']==case and x['weight_reference']=='fixed');b=next(x for x in summary['cases'] if x['scenario']==case and x['weight_reference']=='equal')
        expected=' & '.join([label,str(a['withdrawn_point_cells']),'/'.join(a['minimax_choices']),'/'.join(b['minimax_choices']),f"{a['mean_interval_width']:.2f}"])
        assert expected in table,case
    text=' '.join(subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split())
    for claim in ['64 are labelled 2026','28 flagged points','Paris under equal weights','48.43','95-entry union','16.08933','4.966','5.306']:assert claim in text,claim
    assert qa['technical_checks']=='pass' and qa['all_pages_rendered_and_visually_reviewed']
    assert qa['total_pages']==23 and qa['main_pages_including_news_and_references']==21 and qa['news_pages']==[16,17] and qa['ai_report_pages']==[22,23]
    assert qa['pdf_sha256']==sha(pdf) and qa['pdf_bytes']==pdf.stat().st_size and qa['compilation_warnings']==0
    assert not qa['submission_ready'] and not qa['ai_record_complete'] and qa['control_number']=='PENDING - not verified'
    assert sha(OUT/'compiler_stdout_stderr.txt')==qa['compiler_output_sha256']
    assert len(list(Path('/data/scratch/himcm_v143_render').glob('page-*.png')))==23
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    for name in ['manifest.json','qa.json']:(OUT/('paper_'+name)).write_bytes((PAPER/assets/name).read_bytes())
    result=dict(status='pass',documentation_revision='V143',primary_evidence='V136',controlled_extensions='V137',primary_data_admissions=0,protected_scientific_files=len(frozen),unchanged_previous_assets_and_sections=len(retained),protected_historical_manuscript_files=len(manifest['protected_files']),all_23_final_pages_rendered_and_visually_reviewed=True,mean_baseline_interval_width_unchanged=16.089333559065736,source_policy_withdrawal_cases=10,new_table_rows_verified=5,previous_overleaf_commit=BASE,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),paper_manifest_sha256=sha(OUT/'paper_manifest.json'),paper_qa_sha256=sha(OUT/'paper_qa.json'),submission_ready=False)
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
