"""Separate Mexico period/membership revision from sampling-envelope effects."""
import json,hashlib
import numpy as np
from task4_v5_model import ROOT,CITIES,NAMES
from task4_copenhagen_institution_revision import copenhagen_bounds
from task4_mexico_2025_revision import mexico_2025_bounds
from task4_mexico_sampling_revision import mexico_sampling_bounds
from task4_joint_acquisition_minima import analyse
from task4_survivor_set_search import search
from task4_survivor_precision import frontier

def main():
    rows=[]
    for version,factory in [('V102',copenhagen_bounds),('V107',mexico_2025_bounds),('V108',mexico_sampling_bounds)]:
        lo,hi=factory();mask=np.zeros_like(lo,bool);mask[:,[NAMES.index(n) for n in ['upper_secondary_ptr','travel','homicide_rate']]]=True
        cert,answers=analyse(lo,hi,mask,preferred_anchor=CITIES.index('Singapore'))
        case=answers[1][3];required=[r['index'] for r in cert if r['continuous_unavoidable']]
        s=search(lo,hi,mask,required,case['attained_count_upper_bound'])
        sets=[]
        for k in s['successful_sets']:
            f=frontier(lo,hi,mask,k)
            sets.append(dict(cities=[CITIES[i] for i in k],feasible_width=f['feasible']['delta'],infeasible_width=f['infeasible']['delta']))
        rows.append(dict(model_version=version,input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),canonical_upper=case['attained_count_upper_bound'],minimum=s['certified_minimum'],sets=sets))
    out=ROOT/'results/task4_v109_survivor_search/attribution.json'
    out.write_text(json.dumps(dict(scenarios=rows,scope='Only Mexico travel changes between these frozen inputs. V107 changes period and optional school-stage membership together; V108 adds sampling uncertainty. Wider hypothetical revelation choices do not imply improved real observations.'),indent=2)+'\n')
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
