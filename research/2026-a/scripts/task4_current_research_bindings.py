"""Read-only current research binding checks with explicit historical boundaries."""
from pathlib import Path,PurePosixPath
import hashlib,json,re,subprocess

REGISTRIES=('design/task4_user_current_extensions.json','design/task4_user_current_acquisition.json')
CONTRACT='design/task4_current_research_integrity.json'
HEX=re.compile(r'[0-9a-f]{64}\Z')
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def verify_current_research(analysis):
    """Return (summary, absolute-path protection map); never modify inputs."""
    analysis=Path(analysis).resolve();repo=analysis.parents[1]
    protected={};bindings={};origins={};paired_reports=set();aliases=[];maps=0;pairs=0
    def path_for(name):
        if not isinstance(name,str) or not name or '\\' in name:raise ValueError('Invalid relative research path: '+str(name))
        pure=PurePosixPath(name)
        if pure.is_absolute() or '..' in pure.parts or pure.as_posix()!=name:raise ValueError('Unsafe research path: '+name)
        p=analysis
        for part in pure.parts:
            p=p/part
            if p.is_symlink():raise ValueError('Symlink research input: '+name)
        if not p.resolve().is_relative_to(analysis) or not p.is_file():raise ValueError('Missing/non-file research input: '+name)
        return p
    def valid_hash(h):
        if not isinstance(h,str) or not HEX.fullmatch(h):raise ValueError('Malformed SHA256: '+str(h))
    def add(name,h,origin):
        valid_hash(h);p=path_for(name)
        if name in bindings and bindings[name]!=h:raise ValueError('Conflicting research hashes: '+name)
        if str(p) in protected and protected[str(p)]!=h:raise ValueError('Metadata/source hash conflict: '+name)
        if name not in bindings:
            if digest(p)!=h:raise ValueError('Research hash differs: '+name)
            bindings[name]=h;protected[str(p)]=h
        origins.setdefault(name,[]).append(origin)
    def metadata(name):
        p=path_for(name);raw=p.read_bytes();protected[str(p)]=hashlib.sha256(raw).hexdigest();return json.loads(raw)
    contract=metadata(CONTRACT)
    if contract.get('schema_version')!=1 or contract.get('registries')!=list(REGISTRIES):raise ValueError('Unexpected research binding contract')
    policies=contract.get('reports',{});history=contract.get('historical_sources',[])
    if not isinstance(policies,dict) or not isinstance(history,list):raise ValueError('Malformed research policies')
    historical={}
    for record in history:
        key=(record['report'],record['source_path'])
        if key in historical:raise ValueError('Duplicate historical policy')
        historical[key]=record
    def walk(node,where):
        nonlocal maps,pairs
        if isinstance(node,list):
            for i,v in enumerate(node):walk(v,where+f'[{i}]')
        elif isinstance(node,dict):
            for k,v in node.items():
                if k in ['source_sha256','source_hashes']:
                    if not isinstance(v,dict):raise ValueError('Non-map registry source hashes: '+where+'.'+k)
                    maps+=1
                    for name,h in v.items():add(name,h,where+'.'+k)
                    continue
                if k.endswith('_sha256'):
                    if not isinstance(v,str):raise ValueError('Unexpected hash field: '+where+'.'+k)
                    base=k[:-7];target=node.get(base)
                    if target is None and k=='verification_sha256' and isinstance(node.get('audit'),str):
                        target=node['audit'];aliases.append(where+'.verification_sha256 -> audit')
                    if not isinstance(target,str):raise ValueError('Unpaired hash field: '+where+'.'+k)
                    add(target,v,where+'.'+k);pairs+=1
                    if target.endswith('.json'):paired_reports.add(target)
                elif isinstance(v,(dict,list)):walk(v,where+'.'+k)
    for name in REGISTRIES:walk(metadata(name),name)
    protected[str(Path(__file__).resolve())]=digest(Path(__file__).resolve())
    for name,h in contract.get('live_source_sha256',{}).items():add(name,h,'contract.live_source_sha256')
    if paired_reports!=set(policies):raise ValueError('Unclassified/stale report policy: '+str(sorted(paired_reports^set(policies))))
    historical_used=set();historical_checked=[];expanded_maps=0
    for report_name in sorted(paired_reports):
        p=path_for(report_name);raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=bindings[report_name]:raise ValueError('Report changed during read: '+report_name)
        report=json.loads(raw);policy=policies[report_name]
        if not isinstance(policy,dict):raise ValueError('Malformed report policy: '+report_name)
        fields=policy.get('expand_source_maps')
        actual=sorted(k for k in ['source_sha256','source_hashes'] if k in report)
        if not isinstance(fields,list) or sorted(fields)!=actual:raise ValueError('Report source-map policy differs: '+report_name)
        for field in fields:
            source=report[field]
            if not isinstance(source,dict):raise ValueError('Non-map report source hashes: '+report_name)
            expanded_maps+=1
            for name,h in source.items():
                valid_hash(h)
                record=historical.get((report_name,name))
                if record is None:add(name,h,report_name+'.'+field);continue
                path_for(name)  # The current counterpart must also be independently pinned.
                if name not in contract.get('live_source_sha256',{}):raise ValueError('Historical counterpart lacks current binding: '+name)
                commit=record['commit'];git_path=record['git_path']
                if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}',commit) or git_path!='research/2026-a/'+name or record['sha256']!=h:raise ValueError('Invalid historical source policy: '+name)
                try:
                    top=subprocess.check_output(['git','-C',str(repo),'rev-parse','--show-toplevel'],stderr=subprocess.PIPE,text=True).strip()
                    if Path(top).resolve()!=repo:raise ValueError('Historical repository differs')
                    subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',commit,'HEAD'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    old=subprocess.check_output(['git','-C',str(repo),'show',commit+':'+git_path],stderr=subprocess.PIPE)
                except subprocess.CalledProcessError as e:raise ValueError('Historical Git object unavailable/not in history: '+commit) from e
                if hashlib.sha256(old).hexdigest()!=h:raise ValueError('Historical Git bytes differ: '+name)
                historical_used.add((report_name,name));historical_checked.append(dict(report=report_name,source_path=name,commit=commit,sha256=h))
    if historical_used!=set(historical):raise ValueError('Unused historical research policy')
    return dict(status='pass registered research integrity',registries_checked=list(REGISTRIES),contract=CONTRACT,
                registry_source_maps=maps,hash_path_pairs=pairs,current_reports_checked=len(paired_reports),
                report_direct_source_maps=expanded_maps,live_bound_files=len(bindings),protected_files=len(protected),
                aliases=aliases,historical_source_versions_checked=historical_checked,
                transitive_historical_report_graphs_expanded=False,source_semantics_revalidated=False,
                saved_numeric_results_recomputed=False,MC_replayed=False,
                scope='Registry hashes and each explicitly classified current report direct source map; upstream report bytes pinned without interpreting their historical source graphs.'),protected
