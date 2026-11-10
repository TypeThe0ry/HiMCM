"""Paired V192/V197 effects with unchanged extension assumptions."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT
O=ROOT/'results/task4_v197_transition'
def load(p):return pd.read_csv(p,float_precision='round_trip')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report={};bindings={}
    for part in ['preferences','future','method','diagnostics']:
        prior=ROOT/('results/task4_v192_'+part);current=ROOT/('results/task4_v197_'+part)
        for p in sorted(current.glob('*.csv')):
            q=prior/p.name
            old,new=load(q),load(p)
            assert list(old.columns)==list(new.columns),(part,p.name)
            assert old.shape==new.shape,(part,p.name)
            numeric=[c for c in old.select_dtypes(include=[np.number]).columns if c in new.select_dtypes(include=[np.number]).columns]
            encoded_changes={}
            for c in set(old.columns)-set(numeric)-{'evidence_version'}:
                if c=='threshold_bracket':
                    delta=[]
                    for a,b in zip(old[c],new[c]):
                        if pd.isna(a) or pd.isna(b):assert pd.isna(a) and pd.isna(b);continue
                        aa,bb=np.array(json.loads(a),float),np.array(json.loads(b),float)
                        assert aa.shape==bb.shape==(2,) and aa[0]<=aa[1] and bb[0]<=bb[1]
                        if not np.array_equal(aa,bb):delta.append(float(np.max(np.abs(bb-aa))))
                    if delta:encoded_changes[c]=dict(rows=len(delta),max_absolute_change=max(delta),encoding='two_numeric_endpoints_JSON')
                else:pd.testing.assert_series_equal(old[c],new[c],check_exact=True)
            if 'evidence_version' in old:
                if old.evidence_version.eq('V192').all():
                    assert new.evidence_version.eq('V197').all()
                else:
                    pd.testing.assert_series_equal(old.evidence_version,new.evidence_version,check_exact=True)
            changes=dict(encoded_changes)
            for c in numeric:
                a,b=old[c].to_numpy(),new[c].to_numpy()
                equal=(a==b)|(pd.isna(a)&pd.isna(b))
                if not equal.all():
                    delta=b[~equal]-a[~equal]
                    changes[c]=dict(rows=int((~equal).sum()),max_absolute_change=float(np.nanmax(abs(delta))),min_change=float(np.nanmin(delta)),max_change=float(np.nanmax(delta)))
            report[part+'/'+p.name]=dict(rows=len(new),numeric_changes=changes)
            bindings[str(q.relative_to(ROOT))]=digest(q);bindings[str(p.relative_to(ROOT))]=digest(p)
    a=load(ROOT/'results/task4_user_v192_revision/current_ranks.csv');b=load(ROOT/'results/task4_user_v197_revision/current_ranks.csv')
    pd.testing.assert_series_equal(a.city,b.city);pd.testing.assert_series_equal(a.weight_reference,b.weight_reference)
    rank_changes={c:int((a[c]!=b[c]).sum()) for c in ['decision_rank','possible_champion','necessary_champion','midpoint_illustrative_rank']}
    for name in ['design/task4_user_v197_admissions.json','results/task4_user_v197_revision/summary.json','results/task4_user_v197_revision/current_ranks.csv']:
        bindings[name]=digest(ROOT/name)
    s=json.loads((ROOT/'results/task4_user_v197_revision/summary.json').read_text())
    summary=dict(version='V197 staged transition',active_primary='V192',active_paper='V196',activation_performed=False,primary_rank_changes=rank_changes,primary_comparisons=s['results'],extension_tables=report,source_sha256=bindings)
    (O/'comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'primary_rank_changes':rank_changes,'extension_tables':len(report),'tables_with_numeric_changes':sum(bool(v['numeric_changes']) for v in report.values())},indent=2))
if __name__=='__main__':main()
