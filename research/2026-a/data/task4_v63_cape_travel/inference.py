"""Apply the reviewed stratified-PSU endpoint envelope to the 2025 wave."""
import importlib.util,json,hashlib
from pathlib import Path
from zipfile import ZipFile
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ghs_endpoint_inference',HERE/'../task4_v30_cape_town/inference.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
endpoint_envelope=module.endpoint_envelope


def main():
    for item in json.loads((HERE/'manifest.json').read_text()):
        assert hashlib.sha256((HERE/item['file']).read_bytes()).hexdigest()==item['sha256']
    descriptive=json.loads((HERE/'summary.json').read_text())
    assert descriptive['ages14_18']['optional']['n']==0
    assert descriptive['all_ages']['optional']['n']==0
    with ZipFile(HERE/'GHS2025.zip') as z:full=pd.read_csv(z.open('PERSON2025.csv'))
    assert not full[['uqnr','personnr']].duplicated().any()
    strata=full.loc[full.metro_code==2,'stratum'].unique()
    frame=full.loc[full.stratum.isin(strata)].reset_index(drop=True)
    assert (frame.metro_code==2).all()  # Retains all sampled PSUs of every relevant stratum.
    assert (frame.groupby('psu').stratum.nunique()==1).all()
    domain=((frame.metro_code==2)&(frame.edu_attend==1)&(frame.edu_edui==2)&(frame.edu_corr==2)&frame.edu_grde.isin([10,11,12]))
    edges={1:(0,15),2:(15,30),3:(30,60),4:(60,90),5:(90,np.inf)}
    lo=frame.edu_time.map({k:np.exp(-b/30) for k,(_,b) in edges.items()}).fillna(0)
    hi=frame.edu_time.map({k:np.exp(-a/30) for k,(a,_) in edges.items()}).fillna(1)
    result={name:endpoint_envelope(frame,mask,lo,hi) for name,mask in {'all_age':domain,'age14_18':domain&frame.age.between(14,18)}.items()}
    for name,key in [('all_age','all_ages'),('age14_18','ages14_18')]:
        np.testing.assert_allclose(result[name]['point_bounds'],[descriptive[key]['utility_lower'],descriptive[key]['utility_upper']],rtol=0,atol=1e-14)
    result['utility']='exp(-one_way_minutes/30); conservative bin closures, no within-bin imputation'
    result['unknown_time_rule']='[0,1] for any unknown time; zero optional membership verified in this wave'
    result['year_comparison']='Repeated surveys are not a matched pupil panel; no causal change or significance claim.'
    (HERE/'inference_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['age14_18'],indent=2))

if __name__=='__main__':main()
