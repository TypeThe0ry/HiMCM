from pathlib import Path
import json,hashlib,difflib
D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=D/'task4_v201_manifest.json'; m=json.loads(p.read_text())
m['numeric_source_manifest']='task4_v201_assets/manifest.json';m['figure_source_manifest']='task4_v201_assets/figure_manifest.json'
m['quantitative_diff']='task4_v201_quantitative_diff.txt'
parts=[]
for n in ['generated.tex','assets/baseline.tex','assets/preferences.tex','assets/revision.tex','assets/vintage_table.tex']:
 a=D/('task4_v198_'+n);b=D/('task4_v201_'+n)
 parts.extend(difflib.unified_diff(a.read_text().splitlines(keepends=True),b.read_text().splitlines(keepends=True),fromfile=str(a.name),tofile=str(b.name)))
(D/'task4_v201_quantitative_diff.txt').write_text(''.join(parts))
paths=[*D.glob('task4_v201_*.tex'),*D.glob('build_task4_v201*.py'),D/'task4_v201_prose_diff.txt',D/'task4_v201_quantitative_diff.txt',D/'task4_v201_paper.pdf',D.parent/'task4_v201_review_entry.tex']
m['output_sha256']={str(x.relative_to(D.parent)):sha(x) for x in sorted(paths)}
m['render_check']='PDF pages 1, 9, 10, 11 and 13 inspected at page scale; V200 identification and score figures 10 pt and 12.5 pt source, respectively, at 6.5 inch insertion.'
m['compile']='tectonic --only-cached -Z search-path=.. from drafts; 27 pages including 2 AI report pages; provisional 18213'
p.write_text(json.dumps(m,indent=2)+'\n')
