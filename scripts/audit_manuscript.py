"""Read-only inventory of manuscript dependencies and editorial hazards."""
from pathlib import Path
import argparse,re,json
RESEARCH_ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--manuscript-root',type=Path,default=RESEARCH_ROOT.parent/'HiMCM-Overleaf')
ROOT=parser.parse_args().manuscript_root.expanduser().resolve()
text=(ROOT/'main.tex').read_text()
active=re.sub(r'\\begin\{comment\}.*?\\end\{comment\}','',text,flags=re.S)
active=re.sub(r'(?<!\\)%[^\n]*','',active)
images=re.findall(r'\\includegraphics(?:\[[^]]*\])?\s*\{([^}]+)\}',active)
labels=set(re.findall(r'\\label\{([^}]+)\}',active))
refs=[r.strip() for g in re.findall(r'\\(?:c|C)?ref\{([^}]+)\}',active) for r in g.split(',')]
keys=set(re.findall(r'@\w+\s*\{([^,]+),',(ROOT/'ref.bib').read_text()))
citations=[k.strip() for g in re.findall(r'\\cite\{([^}]+)\}',active) for k in g.split(',')]
report={
 'scope':'Local manuscript checkout; not the live Overleaf session',
 'manuscript_root':str(ROOT),
 'referenced_graphics':images,
 'missing_graphics':[p for p in images if not (ROOT/p).exists()],
 'undefined_references':sorted(set(refs)-labels),
 'undefined_citations':sorted(set(citations)-keys),
 'topic_markers':{q:len(re.findall(re.escape(q),active,re.I)) for q in ['high school','Super Bowl','Grand Prix','Beidaihe']},
 'caption_setup':re.findall(r'\\captionsetup(?:\[[^]]*\])?\{([^}]+)\}',active),
 'requires_source_review':['mixed task topics and team identifiers','entropy proportion denominator mixes normalized numerator and raw denominator','weight-vector versus fusion-coefficient notation and score scaling','missing original graphics prevent complete manuscript rendering'],
}
out=RESEARCH_ROOT/'docs/reviews/manuscript_audit.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k] for k in ['missing_graphics','undefined_references','undefined_citations']},indent=2))
