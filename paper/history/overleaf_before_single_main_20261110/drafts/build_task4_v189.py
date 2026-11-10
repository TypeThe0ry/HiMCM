"""Insert the proven joint-mean sensitivity boundary in the owned source-policy section."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parent.parent/'HiMCM/research/2026-a'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    folder=R/'results/task4_v187_joint_means';cert=json.loads((folder/'verification.json').read_text());assert cert['status']=='pass'
    summary=json.loads((folder/'summary.json').read_text());rows={x['weight_reference']:x for x in summary['thresholds']}
    assert all(r['binding_rivals']==['Oslo'] for r in rows.values())
    old=D/'task4_v186_vintage.tex';text=old.read_text();cut=text.index('Replace selected commute intervals')
    paragraph=r"""\subsection{Sensitivity to the accepted input information}\label{sec:sourcepolicy}
Point withdrawals replace selected point utilities by $[0,1]$, keeping weights,
supplements and the 48 non-point bounds fixed. Test pre-2020 dates, post-2025
dates, non-\texttt{ok} flags and their union, counting overlaps once.

\input{task4_v182_assets/vintage_table.tex}

Withdrawing 28 flagged points selects Berlin (baseline weights) or Paris
(equal weights); removing 13 pre-2020 points selects Singapore or Zurich,
respectively. Removing 64 post-2025 points retains Zurich under both,
widening the baseline mean range from 16.05 to 48.41; the 95-point union
selects Singapore under both. All sixteen remain possible champions.
Dates and flags are screening criteria, not error probabilities.

Withholding Zurich's homicide point selects Singapore (baseline) or Oslo
(equal); withholding Amsterdam's retains Zurich under both. Varying only
Zurich's rate gives regret ties near 0.23002 and 0.90473 per 100,000,
respectively: Zurich uniquely minimizes regret below each cutoff and is
excluded above. These are hypothetical rates, with other inputs fixed.

Withdrawing Zurich's commute interval, both identified proxies or all twelve
supplied means selects Singapore (baseline), retaining Zurich under equal
weights. Dublin alone changes neither choice; these withdrawals retain sixteen
possible champions. Varying only Zurich's mean under Jensen bounds gives a baseline tie
near 46.59 minutes: Zurich below, Singapore above; equal weights retain
Zurich for every nonnegative mean, with other inputs fixed.

Jointly allow each of the twelve means $t_i$ to vary independently in
$[(1-\delta)t_i,(1+\delta)t_i]$, $0\leq\delta\leq1$; retain Jensen upper bounds,
Singapore's stage bins, unknown travel and other entries. Fixed upper scores
make each regret increase with its own mean: Zurich's largest mean and the
other eleven smallest means maximize its regret minus the best rival's.
The critical radii are approximately FIXED\% (baseline) and EQUAL\% (equal).
Below each boundary Zurich uniquely minimizes regret throughout the box;
at it Oslo can tie, and above it a counterexample exists.
These conditional ranges are not measured errors or future probabilities.
""".replace('FIXED',f"{rows['fixed']['sharp_radius_percent']:.5f}").replace('EQUAL',f"{rows['equal']['sharp_radius_percent']:.5f}")
    (D/'task4_v189_vintage.tex').write_text(paragraph)
    core=D/'task4_v186_core.tex';assert core.read_text().count('task4_v186_vintage.tex')==1
    (D/'task4_v189_core.tex').write_text(core.read_text().replace('task4_v186_vintage.tex','task4_v189_vintage.tex'))
    paper=D/'task4_v188_paper.tex';s=paper.read_text();assert s.count('task4_v186_core.tex')==1
    (D/'task4_v189_paper.tex').write_text(s.replace('% V188 owned review;','% V189 owned review;').replace('task4_v186_core.tex','task4_v189_core.tex'))
    (D.parent/'task4_v189_review_entry.tex').write_text('% Owned independent review; default main setting unchanged.\n\\RequirePackage{import}\n\\import{drafts/}{task4_v189_paper.tex}\n')
    manifest=dict(version='V189',primary='V181 unchanged',base_review='V188',edited_scope='Owned5.5compressedwithdecisionresultsretainedandjointcommuteboundaryadded;inputpaths/versioncomment',joint_means_critical_radii={k:v['sharp_radius'] for k,v in rows.items()},rounded_percentages={k:f"{v['sharp_radius_percent']:.5f}" for k,v in rows.items()},display_control_number='18213',actual_registered_number_verified=False,baseline_data_changed=False,figures_references_AI_changed=False,project_settings_changed=False,source_sha256={str(p.relative_to(R)):sha(p) for p in [folder/'verification.json',folder/'summary.json',folder/'proof_review.md',R/'scripts/task4_v187_joint_means.py']},paper_input_sha256={str(p.relative_to(D.parent)):sha(p) for p in [old,core,paper,Path(__file__)]})
    (D/'task4_v189_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('V189generated;old/newcommuteblockwords',len(text.split()),len(paragraph.split()))
if __name__=='__main__':main()
