"""Same-scope 2026 provisional Tokyo update, with 2025 final controls."""
import csv
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader
P = Path(__file__).resolve().parent

def rows(name):
    with (P/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def total(data, year, kind):
    candidates = [r for r in data if r['種別']==kind and r['地域階層']=='0'
                  and r['地域']=='総数' and r['西暦（年度）']==str(year)]
    assert len(candidates)==1
    return candidates[0]

def value(r, col):
    return 0 if r[col]=='-' else int(r[col])

def extract():
    for r in json.loads((P/'manifest.json').read_text()):
        b=(P/r['file']).read_bytes()
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    h=rows('gk26pv0701.csv'); s=rows('gk26pv0901.csv')
    high_kind='総数（国・公・私立）'; six_kind='総数（国・公立）'
    pupil='生徒数（人）';teacher='教員数（本務者）（人）';upper='後期課程／生徒数（全日制）（人）'
    a,b=total(h,2026,high_kind),total(s,2026,six_kind)
    for rr in [a,total(h,2026,'公立'),total(h,2026,'私立')]:
        assert value(rr,pupil)==value(rr,'生徒数／男（人）')+value(rr,'生徒数／女（人）')
        assert value(rr,pupil)==value(rr,'生徒数／全日制（人）')+value(rr,'生徒数／定時制（人）')
        for stage, grades in [('全日制',3),('定時制',4)]:
            assert value(rr,'生徒数／'+stage+'（人）')==sum(value(rr,f'生徒数／{stage}／{g}学年（人）') for g in range(1,grades+1))
        assert value(rr,teacher)==value(rr,'教員数（本務者）／男（人）')+value(rr,'教員数（本務者）／女（人）')
    for col in [pupil,teacher,'学校数（校）']:
        assert value(a,col)>=sum(value(total(h,2026,k),col) for k in ['公立','私立']) # national component not separately listed
        assert value(a,col)==sum(value(r,col) for r in h if r['種別']==high_kind and r['西暦（年度）']=='2026' and r['地域階層']=='1')
    for col in [upper,teacher,'学校数（校）','前期課程／生徒数（人）']:
        assert value(b,col)==sum(value(total(s,2026,k),col) for k in ['国立','公立'])
        assert value(b,col)==sum(value(r,col) for r in s if r['種別'] in ['国立','公立'] and r['西暦（年度）']=='2026' and r['地域階層']=='1')
    for rr in [b,total(s,2026,'国立'),total(s,2026,'公立')]:
        assert value(rr,upper)==sum(value(rr,f'後期課程／生徒数（全日制）／{g}学年（人）') for g in [1,2,3])
        assert value(rr,upper)==sum(value(rr,f'後期課程／生徒数（全日制）／{sex}（人）') for sex in ['男','女'])
    old_a=total(rows('../task4_v46_tokyo/gk25qv0711.csv'),2025,high_kind)
    old_b=total(rows('../task4_v47_tokyo_coverage/gk25qv0911.csv'),2025,six_kind)
    for col in [pupil,teacher,'学校数（校）']:
        assert old_a[col]==total(h,2025,high_kind)[col]
    assert old_b['後期課程／生徒数（人）']==total(s,2025,six_kind)[upper]
    assert old_b[teacher]==total(s,2025,six_kind)[teacher]
    notes=''.join(x.extract_text() for x in PdfReader(P/'gk26pf0001.pdf').pages)
    methods=''.join(x.extract_text() for x in PdfReader(P/'gk26pf0002.pdf').pages)
    assert '速報値' in notes and '本務者のみ' in notes and '本科在籍者のみ' in notes
    assert '令和８年５月１日現在' in methods and '全数調査' in methods
    raw=(P/'gk26pv0901.csv').read_text(encoding='utf-8-sig')
    assert '私立には中等教育学校はない' in raw and '定時制の課程を設置している中等教育学校はない' in raw
    scenarios=[]
    for year in [2025,2026]:
        hr,sr=total(h,year,high_kind),total(s,year,six_kind)
        n=value(hr,pupil)+value(sr,upper);t=value(hr,teacher);pool=value(sr,teacher)
        scenarios.append(dict(year=year,status='final_control' if year==2025 else 'provisional',
            ordinary_students=value(hr,pupil),ordinary_main_duty_teachers=t,
            integrated_upper_students=value(sr,upper),integrated_all_stage_teachers=pool,
            students=n,teacher_bounds=[t,t+pool],utility_bounds=[15*t/(n+15*t),15*(t+pool)/(n+15*(t+pool))]))
    return dict(date='2026-05-01',geography='Tokyo Metropolis school location',
        scenarios=scenarios,main_admitted=False,admitted_cells_changed=0,
        scope='Ordinary full/part-time high schools plus integrated-secondary upper courses; same conditional coverage as V47.',
        exclusions=['correspondence','special-needs upper departments','specialized-training upper courses'],
        teacher_definition='Main-duty school-assigned persons, not FTE; integrated upper-stage allocation unknown.',
        verification='Raw hashes, integrated-school ownership sums, high-school geography/grade/sex sums and 2025 final controls checked.',
        interpretation='Provisional year sensitivity only. No source for shrinking stage-allocation bounds or actual high-school commute.')

if __name__=='__main__':
    result=extract();(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
