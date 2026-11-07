"""Conservative first-study-trip diagnostic using reported return-home chains."""
import json
from pathlib import Path
import pandas as pd
import numpy as np
P=Path(__file__).resolve().parent

def minute(s):
    try:
        h,m=map(int,str(s).split(':'));return h*60+m if 0<=h<24 and 0<=m<60 else np.nan
    except (ValueError,TypeError):return np.nan

def classify(v,home):
    v=v.copy();v['start']=v.HoraIni.map(minute);v['end']=v.HoraFin.map(minute)
    study=v[v.Proposito.eq(3)]
    if study.empty:return 0.,1.,'no_study_trip'
    if v.start.isna().any():return 0.,1.,'unresolved_trip_order'
    first=study.start.min();target=study[study.start==first]
    if len(target)!=1:return 0.,1.,'tied_first_study_departure'
    r=target.iloc[0]
    direct=np.isclose(r.OrigenCoordX,home[0],rtol=0,atol=1e-6) and np.isclose(r.OrigenCoordY,home[1],rtol=0,atol=1e-6)
    chain=False;earlier=v[v.start<first]
    if len(earlier):
        prev=earlier[earlier.start==earlier.start.max()]
        if len(prev)==1:
            q=prev.iloc[0]
            chain=(q.Proposito==7 and pd.notna(q.end) and q.start<=q.end<=first and np.isclose(q.DestinoCoordX,r.OrigenCoordX,rtol=0,atol=1e-6) and np.isclose(q.DestinoCoordY,r.OrigenCoordY,rtol=0,atol=1e-6))
    if not(direct or chain):return 0.,1.,'first_study_origin_unconfirmed'
    if r.CodigoTiempo!=0 or pd.isna(r.TiempoViaje) or r.TiempoViaje<=0:return 0.,1.,'invalid_duration'
    u=float(np.exp(-r.TiempoViaje/30));return u,u,'home_coordinate' if direct else 'reported_return_home_chain'

def main():
    old=pd.read_csv(P/'conditional_person_audit.csv');people=pd.read_parquet(P/'personas.parquet');homes=pd.read_parquet(P/'hogares.parquet');trips=pd.read_parquet(P/'viajes.parquet')
    joined=people.merge(homes[['Hogar','DirCoordX','DirCoordY']],on='Hogar',validate='many_to_one').set_index('Persona')
    rows=[]
    for r in old.to_dict('records'):
        p=joined.loc[r['person']];a,b,status=classify(trips[trips.Persona==r['person']],(p.DirCoordX,p.DirCoordY))
        rows.append(dict(scope=r['scope'],person=r['person'],weight=r['weight'],utility_lower=a,utility_upper=b,status=status,previous_lower=r['utility_lower'],previous_upper=r['utility_upper']))
    f=pd.DataFrame(rows);assert not f.duplicated(['scope','person']).any();assert (f.weight>0).all()
    f.to_csv(P/'trip_chain_person_audit.csv',index=False);s=[]
    for scope,g in f.groupby('scope'):
        s.append(dict(scope=scope,persons=len(g),identified=int((g.utility_lower==g.utility_upper).sum()),new_chain_identified=int((g.status=='reported_return_home_chain').sum()),changed_intervals=int(((g.utility_lower-g.previous_lower).abs()>1e-12).sum()|0),utility_lower=float((g.weight*g.utility_lower).sum()/g.weight.sum()),utility_upper=float((g.weight*g.utility_upper).sum()/g.weight.sum()),main_admitted=False))
    (P/'trip_chain_summary.json').write_text(json.dumps(s,indent=2));print(json.dumps(s,indent=2))
if __name__=='__main__':main()
