"""Verify original TRP handbook; preserve non-observed and missing durations."""
import hashlib,json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent

def main():
    files=json.loads((P/'manifest.json').read_text());verified=0
    for item in files:
        if 'sha256' not in item:continue
        data=(P/item['file']).read_bytes()
        assert len(data)==item['bytes']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        verified+=1
    text=subprocess.check_output(['pdftotext','-layout',str(P/'handbook2024.pdf'),'-']).decode()
    assert 'February 2024' in text
    assert 'A driving age student who attends school three or more days per week' in text
    assert '15 miles for 5 days per week' in text
    assert 'The employer receives their SA through email' in text
    assert 'Table VI – Commute Statistics at this Site' in text
    assert 'average commute time for employees coming to work' in text
    report=dict(original_files_verified=verified,driving_age_and_attendance_restriction=True,
        compliance_analysis_can_include_imputed_SOV_records=True,
        default_imputed_distance_miles=15,default_imputed_days_per_week=5,
        student_duration_distribution_obtained=False,student_response_denominator_obtained=False,
        phoenix_high_school_city_bound_changed=False,new_admissible_observations=0,
        site_summary_emailed_to_coordinator=True)
    (P/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
