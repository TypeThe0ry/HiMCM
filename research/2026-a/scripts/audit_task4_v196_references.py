"""Inventory V193 bibliography/citation identities; not source-quality certification."""
import collections,csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT.parents[2]/'HiMCM-Overleaf'
OUT=ROOT/'results/task4_v196_references'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def group(s,start):
    assert s[start]=='{';depth=0
    for k in range(start,len(s)):
        if s[k]=='{' and (k==0 or s[k-1]!='\\'):depth+=1
        if s[k]=='}' and (k==0 or s[k-1]!='\\'):
            depth-=1
            if depth==0:return s[start+1:k],k+1
    raise ValueError('Unclosed group')
def main():
    pdf=P/'drafts/task4_v193_paper.pdf'
    assert sha(pdf)=='fb9b2d0f95f544c41f2de02e15a58673f15a8ac8efc4dcadb173f0a272474dae'
    seen={}
    def include(path):
        path=path.resolve()
        assert path.is_relative_to(P)
        if path in seen:return
        s=path.read_text();seen[path]=s
        for match in re.finditer(r'\\input\{([^}]+)\}',s):
            name=match[1];name=name if Path(name).suffix else name+'.tex'
            q=path.parent/name
            if not q.exists():q=P/'drafts'/name
            include(q)
    include(P/'drafts/task4_v193_paper.tex')
    refs=P/'drafts/task4_v193_references.tex';gen=P/'drafts/task4_v193_generated.tex'
    g=seen[gen];m=re.search(r'\\newcommand\{\\CaseReferences\}',g);assert m
    case,_=group(g,m.end())
    expanded=seen[refs].replace('\\CaseReferences',case)
    matches=list(re.finditer(r'\\bibitem\{([^}]+)\}',expanded));keys=[m[1] for m in matches]
    assert len(keys)==56 and len(set(keys))==56
    casekeys=set(re.findall(r'\\bibitem\{([^}]+)\}',case));assert len(casekeys)==3
    aux=(OUT/'compiled.aux').read_text()
    compiled=re.findall(r'\\bibcite\{([^}]+)\}\{([^}]+)\}',aux)
    assert [k for k,n in compiled]==keys and [int(n) for k,n in compiled]==list(range(1,57))
    used=set(k.strip() for chunk in re.findall(r'\\citation\{([^}]+)\}',aux) for k in chunk.split(','))
    assert not used-set(keys)
    # Source locations are collected from the reachable TeX closure. Generated
    # macro citations are separately labelled as definition locations.
    sites=collections.defaultdict(list)
    for path,s in seen.items():
        for m in re.finditer(r'\\cite(?:[a-zA-Z*]*)\s*(?:\[[^]]*\]\s*)*\{([^}]+)\}',s):
            for key in m[1].split(','):
                sites[key.strip()].append(dict(file=str(path.relative_to(P)),line=s[:m.start()].count('\n')+1,location_kind='macro_definition' if path==gen else 'source_citation'))
    assert used<=set(sites)
    inventory=[]
    for i,m in enumerate(matches):
        key=m[1];end=matches[i+1].start() if i+1<len(matches) else expanded.index('\\end{thebibliography}')
        block=expanded[m.end():end];source=gen if key in casekeys else refs
        raw=seen[source];origin=re.search(r'\\bibitem\{'+re.escape(key)+r'\}',raw);assert origin
        inventory.append(dict(number=i+1,key=key,used_in_compiled_citations=key in used,bibliography_source=str(source.relative_to(P)),source_line=raw[:origin.start()].count('\n')+1,urls=re.findall(r'\\url\{([^}]+)\}',block),citation_locations=sites.get(key,[])))
    (OUT/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    with (OUT/'inventory.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['number','key','used_in_compiled_citations','bibliography_source','source_line','url_count','urls']);w.writeheader()
        for r in inventory:w.writerow({k:r[k] for k in ['number','key','used_in_compiled_citations','bibliography_source','source_line']}|dict(url_count=len(r['urls']),urls=' | '.join(r['urls'])))
    report=dict(status='pass',review='V193',references=56,unique_keys=56,compiled_cited_keys=len(used),unused_keys=sorted(set(keys)-used),missing_keys=[],duplicate_keys=[],url_occurrences=sum(len(r['urls']) for r in inventory),keys_without_url=[r['key'] for r in inventory if not r['urls']],source_tex_files=len(seen),compiled_bibliography_order_matches_source=True,pdf_sha256=sha(pdf),compiled_aux_sha256=sha(OUT/'compiled.aux'),source_sha256={str(p.relative_to(P)):sha(p) for p in seen},audit_sha256=sha(Path(__file__)),scope='Compiled citation/key/URL identity and exact source locations only. URL presence does not establish availability, source authenticity, measurement compatibility or claim support. No live crawl, all-input certification or model/paper change.',method_metadata='Four method entries contain no apparent internal bibliographic contradiction. Publisher DOI metadata was not revalidated in this bounded local audit.')
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'},indent=2))
if __name__=='__main__':main()
