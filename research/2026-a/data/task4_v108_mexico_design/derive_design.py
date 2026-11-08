"""Offline fixed-weight Taylor ratios from nonidentifying city-level moments."""
from pathlib import Path
import json,hashlib,math
P=Path(__file__).resolve().parent
CODES=['1','2','3','4','5','6','9','']
ENDS=[(math.exp(-b/30) if b is not None else 0.,math.exp(-a/30)) for a,b in zip([0,15,30,60,120],[15,30,60,120,None])]+[(0.,1.)]*3

def derive_from_moments():
    m=json.loads((P/'manifest.json').read_text());f=P/m['file']
    assert hashlib.sha256(f.read_bytes()).hexdigest()==m['sha256']
    d=json.loads(f.read_text());s=d['weighted_totals'];c=d['centered_crossproduct']
    def dot(x,y):return sum(a*b for a,b in zip(x,y))
    def quad(a,b):return sum(a[i]*c[i][j]*b[j] for i in range(24) for j in range(24))
    scenarios={}
    for name,known,optional in [('legacy_progression',[0,1],[2]),('boundary3_optional',[0],[1,2])]:
        results={}
        for endpoint,col,reverse in [('lower',0,False),('upper',1,True)]:
            order=sorted(range(8),key=lambda k:ENDS[k][col],reverse=reverse)
            candidates=[]
            for prefix in range(9):
                selected=set(order[:prefix]);a=[];b=[]
                for group in range(3):
                    for code in range(8):
                        inc=group in known or (group in optional and code in selected)
                        b.append(float(inc));a.append(ENDS[code][col] if inc else 0.)
                A=dot(a,s);B=dot(b,s);assert B>0
                ratio=A/B;aa=quad(a,a);ab=quad(a,b);bb=quad(b,b)
                residual=[a[k]-ratio*b[k] for k in range(24)]
                var=quad(residual,residual)/B**2
                assert var>=-1e-14
                candidates.append({'prefix':prefix,'optional_time_codes':[CODES[k] or 'blank' for k in order[:prefix]],'A':A,'B':B,'ratio':ratio,'AB_centered_crossproduct':[[aa,ab],[ab,bb]],'taylor_se':math.sqrt(max(0,var)),'numerator_coefficients':a,'denominator_coefficients':b})
            best=(max if reverse else min)(range(9),key=lambda k:candidates[k]['ratio'])
            results[endpoint]={'candidates':candidates,'extremal_prefix':best,'estimate':candidates[best]['ratio'],'selected_candidate_se':candidates[best]['taylor_se']}
        scenarios[name]=results
    return {'method':d['method'],'input_moments_sha256':m['sha256'],'diagnostics':d['diagnostics'],'scenarios':scenarios,'warning':'Selected-candidate SE is diagnostic only. Confidence coverage for an identification-bound envelope needs an explicit inferential construction; no CI is asserted here.'}

def derive():
    return derive_from_moments()

if __name__=='__main__':
    result=derive_from_moments();(P/'candidate_ratios.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({name:{side:{k:v for k,v in r.items() if k!='candidates'} for side,r in d.items()} for name,d in result['scenarios'].items()},indent=2))
