"""Apply user-authorized provisional template tcn; preserve all V186 content."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=D/'task4_v186_paper.tex';text=old.read_text();assert text.count('tcn=PENDING')==1
    text=text.replace('% V186 owned review;','% V188 owned review; provisional template number, registration unverified;').replace('tcn=PENDING','tcn=18213')
    (D/'task4_v188_paper.tex').write_text(text)
    (D.parent/'task4_v188_review_entry.tex').write_text('% Owned independent review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v188_paper.tex}\n')
    (D/'task4_v188_manifest.json').write_text(json.dumps(dict(version='V188',primary='V181 unchanged',base_review='V186',edited_scope='Owned wrapper tcn only plus version comment; all content inputs reused byte-for-byte',display_control_number='18213',number_basis='Latest supplied template mcmsetup tcn; user authorized provisional latest-template value on2026-11-10',actual_registered_number_verified=False,submission_ready=False,source_sha256={str(p.relative_to(D.parent)):sha(p) for p in [old,Path(__file__)]}),indent=2)+'\n')
if __name__=='__main__':main()
