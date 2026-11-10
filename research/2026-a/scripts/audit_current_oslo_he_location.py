"""Independent scalar check of a conditional24-provider diagnostic."""
import csv,hashlib,json,math,subprocess,sys,tempfile
from pathlib import Path
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];G=R.parents[1]
D=R/'data/current_oslo_he_location';O=R/'results/current_oslo_he_location'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def close(a,b):assert math.isclose(float(a),float(b),rel_tol=0,abs_tol=2e-11),(a,b)
def score(u,w):
    a=math.sqrt(math.fsum(v*x*x for v,x in zip(w,u)));b=math.sqrt(math.fsum(v*(1-x)**2 for v,x in zip(w,u)))
    return 100*a/(a+b)
def page(n):return ' '.join(subprocess.check_output(['/usr/bin/pdftotext','-f',str(n),'-l',str(n),'-layout',str(D/'ngi_2026.pdf'),'-'],text=True).split())
def main():
    a=audit_parser(__doc__).parse_args();canonical=O/'verification.json';check_output(a,canonical,G)
    before=protected_inputs();receipt=read(D/'ngi_2026.pdf.receipt.json');pdf=D/'ngi_2026.pdf'
    assert receipt['status']==200 and sha(pdf)==receipt['sha256'] and pdf.stat().st_size==receipt['bytes']
    assert pdf.read_bytes().startswith(b'%PDF')
    assert '29. april 2026' in page(3) and 'Det systematiske kvalitetsarbeidet ved Norsk Gestaltinstitutt Høyskole er tilfredsstillende.' in page(3)
    assert 'Høyskolen holder til i Sandvika i Bærum kommune.' in page(8)
    assert 'Ved tilsynet i 2023/24' in page(8) and 'Som høyskole uten institusjonsakkreditering' in page(9)
    fail=read(D/'failed_interview_attempt.json')
    assert fail['status']==403 and not fail['body_retained'] and not fail['retried'] and not fail['admitted_as_relocation_evidence']
    old=R/'data/current_oslo_dbh_campus';cr=[x for x in rows(old/'api_662.csv') if x['Institusjonskode']=='1405']
    assert cr==rows(O/'campus_history.csv') and len(cr)==22
    assert {(x['Årstall'],x['Semester']) for x in cr}=={(str(y),s) for y in range(2016,2027) for s in ['1','3']}
    assert {x['Kommunenummer campus'] for x in cr}=={'0301'}
    address=next(x for x in rows(old/'api_211.csv') if x['Institusjonskode']=='1405')
    assert address['Adresse']=='Kjørbokollen 30' and address['Postnummer']=='1337'
    prior=read(R/'results/current_oslo_he_identity_completion/verification.json')
    for n,h in prior['source_sha256'].items():assert sha(R/n)==h,n
    f,lo,hi=revised_bounds();cities=f.city.tolist();oslo=cities.index('Oslo');he=NAMES.index('research_he_density')
    saved_bounds=rows(O/'bounds.csv');saved_ranks=rows(O/'ranks.csv');s=read(O/'summary.json')
    assert len(saved_bounds)==320 and len(saved_ranks)==64 and s['density_per_million']==33.0
    # 24/727797*1e6 lies strictly inside the one-decimal rounding cell [32.95,33.05).
    assert 32.95<24/727797*1e6<33.05
    independent={}
    for scenario in ['retained_V203','conditional_count24']:
        ll=lo.tolist();hh=hi.tolist()
        if scenario=='conditional_count24':ll[oslo][he]=hh[oslo][he]=3.3/4.3
        b={(x['city'],x['indicator']):x for x in saved_bounds if x['scenario']==scenario};assert len(b)==160
        for i,c in enumerate(cities):
            for j,n in enumerate(NAMES):close(b[c,n]['lower'],ll[i][j]);close(b[c,n]['upper'],hh[i][j])
        for ref in ['fixed','equal']:
            w=[.1]*10 if ref=='equal' else [.05 if j in [6,9] else .1125 for j in range(10)]
            lower=[score(x,w) for x in ll];upper=[score(x,w) for x in hh]
            regrets=[max(0,max(upper[k] for k in range(16) if k!=i)-lower[i]) for i in range(16)]
            ranks=[1+sum(v<r-1e-10 for v in regrets) for r in regrets]
            t={x['city']:x for x in saved_ranks if (x['scenario'],x['weight_reference'])==(scenario,ref)};assert len(t)==16
            for i,c in enumerate(cities):
                for n,v in [('score_lower',lower[i]),('score_upper',upper[i]),('max_regret',regrets[i])]:close(t[c][n],v)
                assert int(t[c]['decision_rank'])==ranks[i]
                assert t[c]['possible_champion']==str(upper[i]>=max(lower[k] for k in range(16) if k!=i)-1e-12)=='True'
                assert t[c]['necessary_champion']==str(lower[i]>=max(upper[k] for k in range(16) if k!=i)-1e-12)=='False'
                assert int(t[c]['best_rank'])==1+sum(lower[k]>upper[i]+1e-12 for k in range(16) if k!=i)
                assert int(t[c]['worst_rank'])==1+sum(upper[k]>lower[i]+1e-12 for k in range(16) if k!=i)
            choices=[cities[i] for i,r in enumerate(regrets) if r<=min(regrets)+1e-12]
            case=next(x for x in s['cases'] if (x['scenario'],x['weight_reference'])==(scenario,ref))
            assert case['recommendations']==choices==(['Oslo'] if ref=='fixed' else ['Zurich'])
            assert case['possible_champions']==16 and case['necessary_champions']==0
            width=math.fsum(b-a for a,b in zip(lower,upper))/16
            for n,v in [('mean_width',width),('Oslo_lower',lower[oslo]),('Oslo_upper',upper[oslo]),('Oslo_regret',regrets[oslo])]:close(case[n],v)
            independent[scenario,ref]=(ranks,case)
    for x in s['contrasts']:
        ref=x['weight_reference'];rr,c=independent['conditional_count24',ref];br,b=independent['retained_V203',ref]
        assert x['decision_rank_changes']==sum(a!=b for a,b in zip(rr,br))==0
        assert not x['recommendation_changed']
        for n,v in [('Oslo_lower_change',c['Oslo_lower']-b['Oslo_lower']),('Oslo_upper_change',c['Oslo_upper']-b['Oslo_upper']),('mean_width_change',c['mean_width']-b['mean_width'])]:close(x[n],v)
    with tempfile.TemporaryDirectory(prefix='himcm-he-location-',dir='/data/scratch') as tmp:
        out=Path(tmp)/'replay'
        subprocess.run([sys.executable,str(R/'scripts/task4_current_oslo_he_location.py'),'--output-dir',str(out)],check=True,stdout=subprocess.PIPE)
        for n in ['campus_history.csv','bounds.csv','ranks.csv','summary.json']:assert (out/n).read_bytes()==(O/n).read_bytes()
    assert protected_inputs()==before
    for n,h in read(R/'results/current_paper_review/current_verification.json')['edition_source_sha256'].items():assert sha(R/n)==h,n
    files=[*sorted(D.iterdir()),*[O/n for n in ['README.md','campus_history.csv','bounds.csv','ranks.csv','summary.json','peer_review.json']],
        old/'api_662.csv',old/'api_211.csv',R/'results/current_oslo_he_identity_completion/verification.json',
        R/'results/current_point_source_ledger/verification.json',R/'scripts/task4_current_oslo_he_location.py',Path(__file__)]
    report=dict(status='pass bounded location and conditional count24 review',**before,edition_entries_checked=24,
        HTTP200_original_PDFs=1,failed_interview_original_downloads=1,relocation_date_admitted=False,
        relevant_PDF_pages_checked=[3,8,9],campus_history_rows=22,utility_bound_rows=320,scalar_city_cases=64,
        all_other159_ranges_preserved=True,all_decision_ranks_unchanged=True,output_files_bytewise_reproduced=4,
        original25_lineage_verified=False,city_count_corrected=False,primary_admissions=0,actual_primary_width_reduction=0,
        changes_primary_model=False,changes_manuscript=False,contrasts=s['contrasts'],
        source_sha256={str(p.relative_to(R)):sha(p) for p in files if p.is_file()},
        scope='Administrative campus-history discrepancy and hypothetical one-provider sensitivity; quality-work approval is not institutional accreditation, retained background is not a new campus census.')
    emit_report(report,a,canonical,G)
if __name__=='__main__':main()
