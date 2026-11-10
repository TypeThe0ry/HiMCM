"""Compress only the owned collection subsection; retain all other prose and assets."""
from pathlib import Path
import hashlib,json,re
D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def keys(s):return sorted({k for group in re.findall(r'\\cite\{([^}]+)\}',s) for k in group.split(',')})
def main():
 old=(D/'task4_v172_core.tex').read_text();a=old.index('\\subsection{Collection problems and their resolution}');b=old.index('Figure~\\ref{fig:identification-matrix}')
 section=(D/'task4_v173_collection.tex').read_text();assert section.startswith('\\subsection{Collection problems and their resolution}')
 assert keys(section)==keys(old[a:b])
 (D/'task4_v173_core.tex').write_text(old[:a]+section+old[b:])
 (D/'task4_v173_paper.tex').write_text((D/'task4_v172_paper.tex').read_text().replace('% V172 owned review;','% V173 owned review;').replace('task4_v172_core.tex','task4_v173_core.tex'))
 (D.parent/'task4_v173_review_entry.tex').write_text('% Independent owned review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v173_paper.tex}\n')
 oldcount=len(re.findall(r'\S+',old[a:b]));newcount=len(re.findall(r'\S+',section))
 manifest=dict(version='V173',primary='V154 unchanged',base_review='V172 frozen',
  changed_scope='Owned section4.2 only; other prose,assets,weights,numerical inputs and template retained',
  base_core_sha256=sha(D/'task4_v172_core.tex'),collection_sha256=sha(D/'task4_v173_collection.tex'),
  before_whitespace_tokens=oldcount,after_whitespace_tokens=newcount,reduction_fraction=1-newcount/oldcount,
  citation_keys=keys(section),shared_class_sha256=sha(D.parent/'mcmthesis.cls'),
  project_settings_changed=False)
 (D/'task4_v173_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(f'Generated V173 candidate: collection {oldcount} -> {newcount}; same citation keys')
if __name__=='__main__':main()
