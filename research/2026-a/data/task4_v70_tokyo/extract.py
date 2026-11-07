"""Reconcile official Tokyo totals and select named teaching posts consistently."""
import hashlib
import importlib.util
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
KEEP=['主幹教諭','指導教諭','教諭','助教諭','講師']
DROP=['校長','副校長','教頭','養護教諭','養護助教諭','栄養教諭']

def sheets(path):
    result={}
    with ZipFile(path) as z:
        strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sh in ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS):
            target=rels[sh.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
            target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            cells={}
            for c in ET.fromstring(z.read(target)).findall('.//s:c',NS):
                v=c.find('s:v',NS)
                if v is not None:cells[c.attrib['r']]=strings[int(v.text)] if c.attrib.get('t')=='s' else v.text
            result[sh.attrib['name']]=cells
    return result

def extract():
    for item in json.loads((ROOT/'manifest.json').read_text()):
        raw=(ROOT/item['file']).read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    # Recompute the existing pupil coverage from its original sources, not a typed count.
    path=ROOT.parent/'task4_v69_tokyo/extract.py'
    spec=importlib.util.spec_from_file_location('tokyo69_evidence',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    old=mod.extract();assert old==json.loads((path.parent/'summary.json').read_text())
    records=[]
    specifications=[('high','ey0175-1',5,19,'A','B',19446),('integrated','188(4-1)',3,22,'B','C',555),('special','ey0220-1',6,20,'A','B',7018)]
    for kind,sheet,header,row,place,total_col,expected in specifications:
        cells=sheets(ROOT/(kind+'_roles2025.xlsx'))[sheet]
        assert cells[place+str(row)]=='東京都'
        if kind=='high':assert cells['A3']=='計\u3000計'
        if kind=='integrated':assert cells['A22']=='令和7年度' and cells['A2']=='1．\u3000計'
        if kind=='special':assert cells['A3']=='計' and cells['B5']=='本務者'
        cols={}
        for key,value in cells.items():
            if key.rstrip('0123456789')+str(header)==key and value in KEEP+DROP:
                col=key.rstrip('0123456789')
                if cells.get(col+str(header+1))=='計':cols[value]=col
        assert set(cols)==set(KEEP+DROP)
        values={role:int(cells[col+str(row)]) for role,col in cols.items()}
        total=int(cells[total_col+str(row)]);assert total==expected==sum(values.values())
        selected=sum(values[r] for r in KEEP);excluded=sum(values[r] for r in DROP)
        assert total==selected+excluded
        records.append(dict(school_type=kind,sheet=sheet,tokyo_row=row,total_main_post=total,roles=values,role_cells={r:c+str(row) for r,c in cols.items()},selected_teaching_posts=selected,excluded_posts=excluded))
    assert [r['selected_teaching_posts'] for r in records]==[17983,515,6680]
    grades=sheets(ROOT/'grade_students2025.xlsx')
    g=grades['135(8-1)']; assert g['B23']=='東京都' and g['A23']=='令和7年度'
    assert [g[c+'3'] for c in ('F','Q','R','S','T')]==['本科','専攻科','専攻科','別科','別科']
    assert [int(g[c+'23']) for c in ('C','F','Q','R','S','T')]==[303528,303468,0,60,0,0]
    # All advanced pupils are private/full-time; national/public have none.
    private=grades['135(8-7)']; assert private['B19']=='東京都'
    assert int(private['O19'])+int(private['P19'])==60 and int(private['Q19'])+int(private['R19'])==0
    for name,row,cols in [('135(8-4)',19,['O','P','Q','R']),('135(8-5)',19,['O','P','Q','R']),('135(8-6)',19,['Q','R','S','T'])]:
        q=grades[name]; assert q['B'+str(row)]=='東京都' and sum(int(q[c+str(row)]) for c in cols)==0
    hs=sheets(ROOT/'high_roles2025.xlsx')
    by_owner={}
    for name,label in [('ey0175-2','national'),('ey0175-3','public'),('ey0175-4','private')]:
        q=hs[name]; assert q['A19']=='東京都'
        by_owner[label]=sum(int(q[c+'19']) for c in ['N','Q','T','W','AI'])
    assert by_owner==dict(national=196,public=8587,private=9200)
    assert sum(by_owner.values())==records[0]['selected_teaching_posts']
    gm=sheets(ROOT/'municipal_students2025.xlsx')['東京都']; pm=sheets(ROOT/'municipal_private_roles2025.xlsx')['東京都']
    assert gm['B29']==pm['B28']=='江戸川区' and gm['A29']==pm['A28']=='123'
    assert gm['U3']=='専攻科' and gm['X3']=='別科' and pm['A1'].endswith('計　私立')
    assert gm['U6']==gm['U29']=='60' and gm['X6']=='0'
    municipal_rows=[k[1:] for k,v in gm.items() if k.startswith('A') and k[1:].isdigit() and v.isdigit()]
    assert sum(int(gm['U'+r]) for r in municipal_rows)==60
    assert sum(int(gm['X'+r]) for r in municipal_rows)==0
    assert [gm['B'+r] for r in municipal_rows if int(gm['U'+r])>0]==['江戸川区']
    assert pm['C5']=='9959' and pm['C28']=='175'
    local_pool=sum(int(pm[c+'28']) for c in ['O','R','U','X','AJ']); assert local_pool==166
    n0,n1=old['expanded_students_interval'];coarse_t0=by_owner['national']+by_owner['public'];t1=sum(r['selected_teaching_posts'] for r in records)
    role_only=[records[0]['selected_teaching_posts'],t1]
    municipal=[role_only[0]-local_pool,t1];t0=municipal[0]
    return dict(city='Tokyo',date='2025-05-01',selected_roles=KEEP,excluded_roles=DROP,school_types=records,
        coarse_teachers_interval=[coarse_t0,t1],coarse_utility_interval=[15*coarse_t0/(n1+15*coarse_t0),15*t1/(n0+15*t1)],
        ordinary_selected_roles_by_ownership=by_owner,ordinary_advanced_students=60,ordinary_other_students=0,
        edogawa_private_selected_pool=local_pool,role_only_teachers_interval=role_only,municipality_conditioned_teachers_interval=municipal,
        role_only_utility_interval=[15*role_only[0]/(n1+15*role_only[0]),15*t1/(n0+15*t1)],
        municipality_conditioned_utility_interval=[15*municipal[0]/(n1+15*municipal[0]),15*t1/(n0+15*t1)],
        students_interval=[n0,n1],teachers_interval=[t0,t1],utility_interval=[15*t0/(n1+15*t0),15*t1/(n0+15*t1)],
        prior_teachers_interval=old['expanded_teachers_interval'],prior_utility_interval=old['expanded_utility_interval'],
        scope='Named teaching-post main-duty headcounts in the existing V69 school/course coverage. Not actual classroom teaching hours, active-duty FTE, or all-city high-school coverage. The main lower bound treats selected posts outside the sole municipality/ownership cell with enrolled advanced students as honka resources; it is a statistical attribution condition, not a measured teaching allocation. Leave/substitute treatment is unchanged; managers and health/nutrition staff may also teach but are outside the selected-post definition.')

if __name__=='__main__':
    r=extract();(ROOT/'summary.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
