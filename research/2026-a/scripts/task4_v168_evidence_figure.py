"""Derive the owned paper asset with a travel label matching mixed source scope."""
from pathlib import Path
import json
import task4_v167_evidence_figure as base
R=Path(__file__).resolve().parents[1]
def main():
 base.O=R/'results/task4_v168_review/figure_asset'
 base.O.mkdir(parents=True,exist_ok=True)
 base.DISPLAY=dict(base.DISPLAY,travel='Travel burden')
 base.LABELS=[base.DISPLAY[n] for n in base.NAMES]
 base.main()
 p=base.O/'figure_manifest.json';d=json.loads(p.read_text())
 d.update(iteration='V168',derived_from='Frozen V167 figure generator',label_revision='Travel burden includes retained school-travel and general-commute proxy scopes',current_review='Owned V168 review; primary V154 unchanged')
 p.write_text(json.dumps(d,indent=2)+'\n')
if __name__=='__main__':main()
