"""Independent scalar audit of the predefined V204 source-block withdrawal.

Use the locked current-check Python. --negative-controls exercises isolated malformed outputs.
"""
import argparse, hashlib, itertools, json, math, sys
from pathlib import Path
import pandas as pd
from task4_user_v204_revision import revised_bounds
from task4_v5_model import NAMES

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results/current_v204_source_block_stress'
GROUPS = {'cost_housing':('cost_living_index','price_income_ratio'), 'broadband':('fixed_broadband_mbps',), 'pm':('pm25',)}
FIELDS = {'cost_living_index':'cli','price_income_ratio':'pir','fixed_broadband_mbps':'broadband_mbps','pm25':'pm25_ugm3'}
EVIDENCE = {'cost_housing':'results/current_cost_edition_review/edition_values.csv','broadband':'data/current_all16_broadband_fields/comparison.csv','pm':'data/task4_v117_team_intake/city_indicators.csv'}
INTERPRET = {'cost_housing':'Numbeo candidate publication series; original extraction lineage unconfirmed','broadband':'Ookla four-field comparison; original extraction lineage unconfirmed','pm':'Original 2024 MODELLED PM column; publisher lineage unconfirmed'}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check(x, msg):
    if not x: raise AssertionError(msg)
def near(a,b,msg,tol=3e-13): check(math.isfinite(float(a)) and abs(float(a)-float(b))<=tol,msg+f': {a} != {b}')
def main(directory):
    summary=json.loads((directory/'summary.json').read_text()); manifest=json.loads((directory/'case_manifest.json').read_text())
    expected_inputs={'data/task4_v117_team_intake/city_indicators.csv','scripts/task4_current_v204_source_block_stress.py','results/task4_user_v204_revision/utility_bounds.csv','design/task4_user_v204_admissions.json',*EVIDENCE.values()}
    check(set(summary['input_sha256'])==expected_inputs,'input hash inventory')
    for name,h in summary['input_sha256'].items(): check(digest(ROOT/name)==h,'input digest '+name)
    check(set(summary['output_sha256'])=={'ranks.csv','bounds.csv','source_map.csv','case_manifest.json'},'output hash inventory')
    for name,h in summary['output_sha256'].items(): check(digest(directory/name)==h,'output digest '+name)
    frame,lo,hi=revised_bounds(); cities=frame.city.tolist(); names=list(NAMES)
    check(len(cities)==len(set(cities))==16 and lo.shape==hi.shape==(16,10) and len(set(names))==10,'user16 x 10')
    frozen=pd.read_csv(ROOT/'results/task4_user_v204_revision/utility_bounds.csv'); frozen=frozen[frozen.scenario.eq('after_conditional')].set_index(['city','indicator'])
    check(len(frozen)==160 and frozen.index.is_unique,'frozen input keys')
    for i,c in enumerate(cities):
        for j,n in enumerate(names):
            near(lo[i,j],frozen.loc[c,n]['lower'],'frozen lower',2e-15); near(hi[i,j],frozen.loc[c,n]['upper'],'frozen upper',2e-15)
    blocks=[b for k in range(4) for b in itertools.combinations(GROUPS,k)]
    label=lambda b: '+'.join(b) if b else 'retained_V204'
    expected_labels={label(b) for b in blocks}
    check(manifest['version']==summary['version']=='V204','version')
    check(manifest['group_definitions']=={g:dict(indicators=list(ns),point_count=16*len(ns),evidence=EVIDENCE[g]) for g,ns in GROUPS.items()},'group definitions')
    check(len(manifest['combinations'])==8 and {x['case'] for x in manifest['combinations']}==expected_labels,'manifest subsets')
    for b in blocks:
        x=next(x for x in manifest['combinations'] if x['case']==label(b))
        check(x==dict(case=label(b),groups=list(b),indicators=[n for g in b for n in GROUPS[g]],withdrawn_points=16*sum(len(GROUPS[g]) for g in b),weight_references=['fixed','equal']),'manifest case '+label(b))
    weights={r:{n:(.1 if r=='equal' else .05 if n in ('public_transport_density','public_pool_density') else .1125) for n in names} for r in ('fixed','equal')}
    check(manifest['weight_references']==weights,'weights')
    bounds=pd.read_csv(directory/'bounds.csv'); ranks=pd.read_csv(directory/'ranks.csv'); sources=pd.read_csv(directory/'source_map.csv',keep_default_na=False)
    check(len(bounds)==1280 and not bounds.duplicated(['case','city','indicator']).any() and set(bounds.case)==expected_labels,'bounds case completeness')
    check(len(ranks)==256 and not ranks.duplicated(['case','weight_reference','city']).any() and set(ranks.case)==expected_labels,'rank case completeness')
    check(len(sources)==64 and not sources.duplicated(['group','city','indicator']).any(),'source map completeness')
    bb=pd.read_csv(ROOT/EVIDENCE['broadband'],keep_default_na=False).set_index('city')
    check(bb.index.is_unique and set(bb.index)==set(cities),'broadband source keys')
    for g,ns in GROUPS.items():
        for n in ns:
            j=names.index(n); field=FIELDS[n]
            for i,c in enumerate(cities):
                check(lo[i,j]==hi[i,j],'source point '+c+' '+n)
                rows=sources[(sources.group==g)&(sources.city==c)&(sources.indicator==n)];check(len(rows)==1,'source map key'); r=rows.iloc[0]; f=frame.iloc[i]
                for key,value in [('raw_column',field),('raw_year',str(f[field+'_year'])),('raw_flag',str(f[field+'_flag'])),('evidence_file',EVIDENCE[g]),('source_interpretation',INTERPRET[g]),('field_match',bb.loc[c,'exact_match_fields'] if g=='broadband' else '')]: check(str(r[key])==str(value),'source map '+key+' '+c)
                for key,value in [('raw_value',f[field]),('retained_lower',lo[i,j]),('retained_upper',hi[i,j])]: near(r[key],value,'source map '+key)
                if g=='broadband':
                    near(bb.loc[c,'input_value_mbps'],f[field],'broadband input'); check(bb.loc[c,'original_csv_lineage']=='not_established_by_publisher_value_match','broadband lineage')
                if g=='pm': check(str(f[field+'_year'])=='2024' and f[field+'_flag']=='MODELLED','PM classification')
    editions=pd.read_csv(ROOT/EVIDENCE['cost_housing'],dtype={'edition':str})
    check(len(editions)==96 and not editions.duplicated(['edition','city','indicator']).any(),'edition keys')
    edition_matches={}
    for edition in ('2026','mid','current'):
        matches=0
        for n in GROUPS['cost_housing']:
            for i,c in enumerate(cities):
                rows=editions[(editions.edition==edition)&(editions.city==c)&(editions.indicator==n)]
                check(len(rows)==1,'edition cell');matches+=abs(float(rows.iloc[0].publisher_value)-float(frame.iloc[i][FIELDS[n]]))<1e-9
        edition_matches[edition]=matches
    check(edition_matches=={'2026':1,'mid':0,'current':28},'edition matches')
    field_counts=bb.exact_match_fields.value_counts().to_dict()
    check(field_counts=={'fixedMedian':15,'fixedMean':1},'broadband field classifications')
    for c in cities:
        field=bb.loc[c,'exact_match_fields'];near(bb.loc[c,field+'_value'],bb.loc[c,'input_value_mbps'],'broadband matched field')
        check(str(bb.loc[c,field+'_exact_value_match']).lower()=='true','broadband exact flag')
    check(set(bb.loc[bb.exact_match_fields.eq('fixedMean'),'fixedMean_geography_level'])=={'country'},'fallback geography')
    saved_bounds=bounds.set_index(['case','city','indicator']);saved_ranks=ranks.set_index(['case','weight_reference','city']); computed={}; cases=[]
    for b in blocks:
        case=label(b); selected={n for g in b for n in GROUPS[g]}
        lower=[];upper=[]
        for i,c in enumerate(cities):
            l=[];h=[]
            for j,n in enumerate(names):
                a,z=(0.,1.) if n in selected else (float(lo[i,j]),float(hi[i,j]));r=saved_bounds.loc[case,c,n]
                near(r['lower'],a,'bound lower '+case+' '+c+' '+n);near(r['upper'],z,'bound upper '+case+' '+c+' '+n);check(bool(r['withdrawn'])==(n in selected),'bound flag')
                l.append(a);h.append(z)
            lower.append(l);upper.append(h)
        for ref in weights:
            w=[weights[ref][n] for n in names]
            def score(v):
                a=math.sqrt(math.fsum(q*x*x for q,x in zip(w,v))); z=math.sqrt(math.fsum(q*(1-x)**2 for q,x in zip(w,v)));return 100*a/(a+z)
            L=[score(v) for v in lower]; U=[score(v) for v in upper]; regs=[]; result=[]
            for i,c in enumerate(cities):
                others=[j for j in range(16) if i!=j];reg=max(0.,max(U[j] for j in others)-L[i]);regs.append(reg)
                result.append(dict(score_lower=L[i],score_upper=U[i],best_rank=1+sum(L[j]>U[i]+1e-12 for j in others),worst_rank=1+sum(U[j]>L[i]+1e-12 for j in others),possible_champion=U[i]>=max(L[j] for j in others)-1e-12,necessary_champion=L[i]>=max(U[j] for j in others)-1e-12,max_regret=reg))
            for i,c in enumerate(cities):
                d=result[i];d['decision_rank']=1+sum(x<regs[i] for x in regs); row=saved_ranks.loc[case,ref,c]
                for k in ('score_lower','score_upper','max_regret'): near(row[k],d[k],f'rank {k} {case} {ref} {c}')
                for k in ('best_rank','worst_rank','possible_champion','necessary_champion','decision_rank'): check(row[k]==d[k],f'rank {k} {case} {ref} {c}')
            computed[(b,ref)]=result
            choices=[c for c,d in zip(cities,result) if d['decision_rank']==1]
            cases.append(dict(case=case,groups=list(b),withdrawn_points=16*len(selected),weight_reference=ref,choices=choices,choice_max_regret=next(d['max_regret'] for d in result if d['decision_rank']==1),mean_width=math.fsum(d['score_upper']-d['score_lower'] for d in result)/16,possible_champions=sum(d['possible_champion'] for d in result),necessary_champions=sum(d['necessary_champion'] for d in result)))
    check(len(summary['cases'])==16 and len({(x['case'],x['weight_reference']) for x in summary['cases']})==16,'summary case completeness')
    minimal={}
    for ref in weights:
        relevant=[x for x in cases if x['weight_reference']==ref];base=relevant[0]['choices'];changed=[x for x in relevant if x['choices']!=base]
        minimal[ref]=[x['groups'] for x in changed if not any(set(y['groups'])<set(x['groups']) for y in changed)]
        for x in relevant:
            x['choice_changed_from_retained']=x['choices']!=base
            candidates=[y for y in summary['cases'] if y['case']==x['case'] and y['weight_reference']==ref];check(len(candidates)==1,'summary case key');y=candidates[0]
            check(set(x)==set(y),'summary fields')
            for k,v in x.items():
                if k in ('choice_max_regret','mean_width'): near(y[k],v,'summary '+k)
                else: check(y[k]==v,'summary '+k)
    check(summary['inclusion_minimal_choice_changing_group_sets']==minimal,'minimal sets')
    check((summary['rank_rows'],summary['bounds_rows'],summary['source_map_rows'],summary['primary_admissions'],summary['actual_primary_width_reduction'])==(256,1280,64,0,0),'summary totals')
    pairs=0
    for a in blocks:
        for b in blocks:
            if set(a)<set(b):
                for ref in weights:
                    for x,y in zip(computed[(a,ref)],computed[(b,ref)]):
                        check(y['score_lower']<=x['score_lower']+3e-13 and y['score_upper']>=x['score_upper']-3e-13 and y['max_regret']>=x['max_regret']-3e-13,'nested monotonicity')
                    pairs+=1
    return dict(status='pass',city_weight_cases=256,bounds=1280,source_map_rows=64,nested_subset_weight_pairs=pairs,edition_exact_value_matches=edition_matches,broadband_exact_field_counts=field_counts,inclusion_minimal=minimal,cases=cases,scope='Conditional user16 V204 information withdrawal; frozen factory and anchored rectangular bounds. Source lineage unconfirmed; this is neither empirical correlation nor a failure probability. Selection need not be monotone. No source validity, model fitness, joint physical attainability, or external publication verified.')
def protected_inputs():
    snapshot_path=ROOT/'design/task4_user_v204_snapshot.json'
    snapshot=json.loads(snapshot_path.read_text())
    science={**snapshot['upstream_source_sha256'],**snapshot['source_sha256']}
    check(len(science)==658,'science inventory')
    protected={ROOT/n:h for n,h in science.items()}
    proof=json.loads((ROOT/'results/current_paper_review/current_verification.json').read_text())
    research=ROOT.parents[1];paper=research.parent/'HiMCM-Overleaf'
    check(len(proof['current_files_sha256'])==7,'paper dependency inventory')
    for n,h in proof['current_files_sha256'].items():
        protected[paper/n]=h;protected[research/'paper/current'/n]=h
    protected[research/'paper/current/main.pdf']=proof['pdf_sha256']
    for path,h in protected.items():check(digest(path)==h,'protected input before '+str(path))
    return protected

def negative_controls(directory):
    import csv,shutil,tempfile
    result={}
    for name,filename,field,message in [
        ('bound','bounds.csv','lower','bound lower'),
        ('regret','ranks.csv','max_regret','rank max_regret'),
        ('missing_case','ranks.csv',None,'rank case completeness')]:
        with tempfile.TemporaryDirectory(prefix='himcm-block-control-',dir='/data/scratch') as tmp:
            target=Path(tmp)
            for n in ['bounds.csv','ranks.csv','source_map.csv','case_manifest.json','summary.json']:
                shutil.copyfile(directory/n,target/n)
            with (target/filename).open() as f:
                reader=csv.DictReader(f);columns=reader.fieldnames;rows=list(reader)
            if field:rows[0][field]=str(float(rows[0][field])+0.01)
            else:rows=[row for row in rows if row['case']!='pm']
            with (target/filename).open('w') as f:
                writer=csv.DictWriter(f,fieldnames=columns,lineterminator='\n');writer.writeheader();writer.writerows(rows)
            summary=json.loads((target/'summary.json').read_text())
            summary['output_sha256'][filename]=digest(target/filename)
            (target/'summary.json').write_text(json.dumps(summary)+'\n')
            try:main(target)
            except AssertionError as error:
                check(message in str(error),'negative control failed for unexpected reason: '+str(error))
                result[name]=dict(rejected=True,failure='AssertionError: '+str(error),output_digest_recomputed=True)
            else:raise AssertionError('Negative control accepted: '+name)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input-dir',type=Path,default=OUT);p.add_argument('--report',type=Path);p.add_argument('--negative-controls',action='store_true');args=p.parse_args()
    protected=protected_inputs()
    result=main(args.input_dir)
    if args.negative_controls:result['negative_controls']=negative_controls(args.input_dir)
    result['source_sha256']={str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__).resolve(),ROOT/'design/task4_user_v204_snapshot.json',*[ROOT/n for n in json.loads((args.input_dir/'summary.json').read_text())['input_sha256']],*([args.input_dir/n for n in ('ranks.csv','bounds.csv','source_map.csv','case_manifest.json','summary.json')] if args.input_dir.resolve()==OUT.resolve() else [])]}
    for mod in list(sys.modules.values()):
        filename=getattr(mod,'__file__',None)
        if filename:
            path=Path(filename).resolve()
            if path.parent == ROOT/'scripts' and path.suffix=='.py': result['source_sha256'][str(path.relative_to(ROOT))]=digest(path)
    if (OUT/'README.md').exists() and args.input_dir.resolve()==OUT.resolve(): result['source_sha256'][str((OUT/'README.md').relative_to(ROOT))]=digest(OUT/'README.md')
    changed=[str(path) for path,h in protected.items() if not path.is_file() or digest(path)!=h]
    check(not changed,'Protected inputs changed: '+str(changed))
    result['input_protection']=dict(scientific_files=658,paper_dependencies_each_copy=7,canonical_PDF=1,changed=changed)
    if args.report: args.report.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ['status','city_weight_cases','bounds','source_map_rows','input_protection']},ensure_ascii=False))
