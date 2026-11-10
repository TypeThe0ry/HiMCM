"""Reject public-body and aggregate-count corruption in temporary manifests."""
from pathlib import Path
import argparse,contextlib,hashlib,io,json,sys,tempfile
import audit_current_ai_continuation2 as audit
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--session',type=Path,required=True);ap.add_argument('--output',type=Path);a=ap.parse_args()
 original=audit.M;args=sys.argv[:];report={}
 try:
  for label,expected in [('public_body','inventory schema'),('model_count','aggregate counts')]:
   m=json.loads(original.read_text())
   if label=='public_body':m['selected_message_inventory'][0]['text_parts']=['synthetic forbidden body']
   else:m['recorded_root_model_counts']['gpt-6.1-sol']+=1
   with tempfile.TemporaryDirectory(prefix='himcm-ai-negative-',dir='/data/scratch') as tmp:
    p=Path(tmp)/'manifest.json';p.write_text(json.dumps(m));audit.M=p
    sys.argv=['audit_current_ai_continuation2.py','--session',str(a.session)]
    try:
     with contextlib.redirect_stdout(io.StringIO()):audit.main()
    except RuntimeError as e:
     assert expected in str(e);report[label]=dict(rejected=True,failure=str(e))
    else:raise AssertionError('Corrupted manifest accepted: '+label)
 finally:audit.M=original;sys.argv=args
 result=dict(status='pass semantic negative controls',negative_controls=report,source_sha256={str(p.relative_to(R)):sha(p) for p in [Path(__file__),R/'scripts/audit_current_ai_continuation2.py',original]},private_text_published=False,scope='Scratch metadata only. Checks schema rejection of a synthetic message body and source-derived rejection of an altered model total; fixed real manifest and private exports are not modified.')
 if a.output:a.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result['negative_controls']))
if __name__=='__main__':main()
