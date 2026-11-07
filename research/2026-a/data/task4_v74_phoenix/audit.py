"""Audit dated catalogue labels separately from administrative cohort membership."""
import csv,hashlib,json,re
from pathlib import Path
from pypdf import PdfReader
P=Path(__file__).resolve().parent
# Manually transcribed from the rendered updated-2023-09-07 visible roster.
LABELS=[(1,'Alhambra','040633000538'),(2,'Trevor G. Browne','040633000554'),(3,'Camelback','040633000540'),(4,'Central','040633000542'),(5,'Cesar Chavez','040633001882'),(6,'Betty H. Fairfax','040633002854'),(7,'Carl Hayden','040633000541'),(8,'Maryvale','040633000549'),(9,'Metro Tech','040633000539'),(10,'North','040633001244'),(11,'The Academies at South Mountain','040633000552'),(12,'Linda Abril','040633002138'),(13,'ARCH',None),(14,'Bostrom','040633001382'),(15,'Camelback Montessori',None),(16,'Desiderata','040633001429'),(17,'Franklin Police and Fire','040633002859'),(18,'Phoenix Coding Academy','040633003509'),(19,'Bioscience','040633002670'),(20,'Maryvale Gifted and Talented',None),(21,'Wilson College Prep','040633003555'),(22,'Phoenix Digital Academy','040633003578'),(23,'Phoenix Educator Preparatory','040633003806'),(24,'PXU City','040633003701')]

def audit():
    for row in json.loads((P/'manifest.json').read_text()):
        assert hashlib.sha256((P/row['file']).read_bytes()).hexdigest()==row['sha256']
    source=P.parent/'task4_v42_phoenix_coverage/phoenix_all_school_roster.csv'
    rows=[r for r in csv.DictReader(source.open()) if r['LEAID']=='0406330']
    assert len(rows)==21
    assert {x[2] for x in LABELS if x[2]}=={r['NCESSCH'] for r in rows}
    assert [x[0] for x in LABELS]==list(range(1,25))
    reader=PdfReader(P/'course_catalog2024.pdf')
    camel=' '.join(reader.pages[84].extract_text().split())
    assert 'school- within-a-school' in camel and 'Camelback Montessori' in camel
    history=(P/'pxu_history.html').read_text()
    assert 'Educator Preparatory, 2023 (closed 2024)' in history
    edu=next(r for r in rows if r['NCESSCH']=='040633003806')
    assert edu['MEMBER']=='0' and float(edu['FTE'])<0
    result=dict(new_originals=3,visible_map_school_labels=24,visible_map_support_labels=[25,26],map_date='2023-09-07',matched_nces_directory_records=21,additional_map_program_labels=[x[1] for x in LABELS if not x[2]],closure_year_from_official_page_payload=2024,catalogue_count_after_one_closure=23,cohort_membership_resolved=False,education_cell_changed=False,source_roster_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),limitations='Visible roster manually transcribed and visually checked; PDF has overlapping old text layers. Shared addresses and school-within-school language do not prove cohort membership or teacher deduplication. History closure is serialized page content, not static HTML body; no exact closure date given.')
    with (P/'catalogue_crosswalk.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['visible_number','visible_label','matched_nces_id']);w.writerows(LABELS)
    (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result
if __name__=='__main__':audit()
