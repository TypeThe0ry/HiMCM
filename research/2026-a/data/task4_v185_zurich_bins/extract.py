"""Offline identity and dimension checks for bounded Swiss commute-source research."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as E
D=Path(__file__).resolve().parent
G='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}'
S='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}'
C='{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}'
LANG='{http://www.w3.org/XML/1998/namespace}lang'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    receipts=json.loads((D/'retrievals.json').read_text());successful=[x for x in receipts if x.get('status')==200]
    for x in successful:
        p=D/x['file'];assert len(p.read_bytes())==x['bytes'] and sha(p)==x['sha256'],p.name
    root=E.parse(D/'bfs_2026_worktime_structure_original.xml').getroot()
    maps={}
    for cl in root.iter(S+'Codelist'):
        if cl.get('id') in ['CL_SSV_SWISS_CITY','CL_SSV_LABMAR_08','CL_UNIT_MEASURE','CL_STATISTICAL_OPERATION']:
            maps[cl.get('id')]={code.get('id'):{t.get(LANG):t.text for t in code.findall(C+'Name')} for code in cl.findall(S+'Code')}
    assert maps['CL_SSV_SWISS_CITY']['261']['en']=='Zürich'
    assert maps['CL_UNIT_MEASURE']['PT']['en']=='Percent'
    assert maps['CL_UNIT_MEASURE']['MN']['en']=='Minute'
    assert maps['CL_STATISTICAL_OPERATION']['CI']['en']=='Confidence interval (+/-)'
    data=E.parse(D/'bfs_2026_worktime_data_original.xml').getroot();dataset=next(x for x in data.iter() if x.tag.split('}')[-1]=='DataSet')
    dataset_attributes={x.get('id'):x.get('value') for x in dataset.find(G+'Attributes')}
    assert dataset_attributes['PERIOD']=='31.12.2023' and dataset_attributes['REGION_REF']=='POLG'
    selected=[]
    for obs in data.iter(G+'Obs'):
        key={x.get('id'):x.get('value') for x in obs.find(G+'ObsKey')}
        if key.get('SSV_SWISS_CITY')=='261':selected.append(dict(key=key,value=obs.find(G+'ObsValue').get('value'),attributes={x.get('id'):x.get('value') for x in obs.find(G+'Attributes')}))
    assert len(selected)==4
    mean=next(x for x in selected if x['key']['STATISTICAL_OPERATION']=='OBS' and x['key']['COMMUTE_TIME']=='DUR')
    ci=next(x for x in selected if x['key']['STATISTICAL_OPERATION']=='CI' and x['key']['COMMUTE_TIME']=='DUR')
    assert mean['value']=='34.22050361' and mean['attributes']['UNIT_MEASURE']=='MN'
    assert ci['value']=='1.949499193' and ci['attributes']['UNIT_MEASURE']=='PT'
    result=dict(status='pass',successful_original_responses=len(successful),city_code='261',city_name='Zürich',dataset_attributes=dataset_attributes,municipal_observations=selected,mean_time_minutes=mean['value'],CI_published_value=ci['value'],CI_unit_code='PT',CI_unit_label='Percent',CI_confidence_level_explicitly_established=False,CI_conversion_applied=False,matching_original_39_9_identified=False,duration_bin_distribution_obtained=False,primary_admissions=0,actual_baseline_width_change=0,source_sha256={x['file']:x['sha256'] for x in successful},extractor_sha256=sha(Path(__file__)))
    (D/'extraction.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','municipal_observations']},indent=2))
if __name__=='__main__':main()
