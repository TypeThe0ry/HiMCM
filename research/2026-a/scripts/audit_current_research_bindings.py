"""Read-only registered research file-integrity check; not source semantic review."""
from pathlib import Path
import sys
sys.dont_write_bytecode=True
from task4_current_research_bindings import verify_current_research,digest
from task4_audit_output import audit_parser,check_output,emit_report
R=Path(__file__).resolve().parents[1];G=R.parents[1]
O=R/'results/current_research_integrity/verification.json'
def main():
    a=audit_parser(__doc__).parse_args();check_output(a,O,G)
    summary,protected=verify_current_research(R)
    for p in [Path(__file__),R/'scripts/task4_audit_output.py',R/'scripts/task4_current_reproduce.py',R/'scripts/test_current_audit_readonly.py',R/'scripts/test_current_research_bindings.py']:
        protected[str(p.resolve())]=digest(p)
    changed=[n for n,h in protected.items() if not Path(n).is_file() or digest(Path(n))!=h]
    if changed:raise ValueError('Research inputs changed: '+str(changed))
    report=dict(summary,source_sha256={str(Path(n).relative_to(R)):h for n,h in protected.items()},
                protected_inputs_changed=changed,primary_admissions=0,actual_primary_width_reduction=0,
                changes_primary_model=False,changes_manuscript=False)
    emit_report(report,a,O,G)
if __name__=='__main__':main()
