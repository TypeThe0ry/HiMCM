"""Verify the activated V136/V137 entry and its owned compiled review artifact."""
import hashlib
import importlib
import json
from pathlib import Path
import subprocess

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT.parents[2]/'HiMCM-Overleaf'
OUT=ROOT/'results/task4_v137_delivery_audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    current=read(ROOT/'design/task4_user_current_model.json')
    ext=read(ROOT/'design/task4_user_v137_extensions.json')
    assert current['version']=='V136' and current['module']=='task4_user_v136_revision'
    assert ext['activation_status']=='active' and ext['live_primary_version']=='V136'
    assert ext['manuscript_entry']=='../HiMCM-Overleaf/drafts/task4_v137_paper.tex'
    before=read(OUT/'registry_before_activation.json');assert before['version']=='V130'
    old_registry=subprocess.check_output(['git','show','476c7a1:research/2026-a/design/task4_user_current_model.json'],cwd=ROOT.parents[1])
    assert old_registry==(OUT/'registry_before_activation.json').read_bytes()
    frame,lo,hi=getattr(importlib.import_module(current['module']),current['factory'])()
    assert len(frame)==16 and lo.shape==hi.shape==(16,10)
    assert [int(np.sum(lo==hi)),int(np.sum((lo<hi)&~((lo==0)&(hi==1)))),int(np.sum((lo==0)&(hi==1)))]==[112,33,15]
    snapshot=read(ROOT/'design/task4_user_v136_snapshot.json')
    extension=read(ROOT/'results/task4_v137_revision/audit.json')
    for source in [snapshot['source_sha256'],extension['result_sha256']]:
        for name,digest in source.items():assert sha(ROOT/name)==digest,name
    post=read(ROOT/'results/task4_user_v136_revision/recheck_audit.json');assert post['status']=='pass'
    manifest=read(PAPER/'drafts/task4_v137_assets/manifest.json')
    assert manifest['primary_evidence']=='V136 user16' and manifest['extensions']=='V137'
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    for name,digest in manifest['manuscript_source_sha256'].items():assert sha(PAPER/'drafts'/name)==digest,name
    # The previous committed paper and team files are protected against the actual
    # fetched pre-migration commit, not only a newly generated manifest.
    for name,digest in manifest['protected_files'].items():
        old=subprocess.check_output(['git','show','eacb1fb:'+name],cwd=PAPER)
        assert hashlib.sha256(old).hexdigest()==digest==sha(PAPER/name),name
    qa=read(PAPER/'drafts/task4_v137_assets/qa.json')
    pdf=PAPER/'drafts/task4_v137_paper.pdf'
    assert qa['technical_checks']=='pass' and qa['all_pages_rendered_and_visually_reviewed']
    assert qa['total_pages']==22 and qa['main_pages_including_news_and_references']==20
    assert qa['news_pages']==[15,16] and qa['ai_report_pages']==[21,22]
    assert not qa['submission_ready'] and not qa['ai_record_complete']
    assert qa['pdf_sha256']==sha(pdf) and qa['pdf_bytes']==pdf.stat().st_size
    assert qa['original_user_csv_sha256']=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
    flat=' '.join(text.split())
    for claim in ['33 partial intervals and 15 fully missing intervals','16.08933','14.47%','13.7607','0.633','153.65','1,751','PENDING']:
        assert claim in flat,claim
    ranks=pd.read_csv(ROOT/current['results']/'current_ranks.csv')
    for _,g in ranks.groupby('weight_reference'):
        assert g.loc[g.decision_rank.eq(1),'city'].tolist()==['Zurich'] and g.possible_champion.all()
    log=OUT/'compiler_stdout_stderr.txt'
    assert sha(log)==qa['compiler_output_sha256']
    for name in ['qa.json','manifest.json']:
        (OUT/('paper_'+name)).write_bytes((PAPER/'drafts/task4_v137_assets'/name).read_bytes())
    result=dict(status='pass',primary='V136',extensions='V137',primary_factory_shape=[16,10],point_partial_fully_missing=[112,33,15],original_CSV_unchanged=True,primary_snapshot_hashes_verified=len(snapshot['source_sha256']),extension_output_hashes_verified=len(extension['result_sha256']),old_manuscript_commit='eacb1fb',old_manuscript_files_byte_identical=len(manifest['protected_files']),all_22_final_pages_rendered_and_visually_reviewed=True,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),paper_qa_sha256=sha(OUT/'paper_qa.json'),paper_manifest_sha256=sha(OUT/'paper_manifest.json'),compiler_stdout_stderr_sha256=sha(log),registry_sha256=sha(ROOT/'design/task4_user_current_model.json'),extension_index_sha256=sha(ROOT/'design/task4_user_v137_extensions.json'),submission_ready=False)
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
