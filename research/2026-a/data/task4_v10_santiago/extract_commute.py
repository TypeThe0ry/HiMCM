"""Conditional student cohort; no confirmed high-school/current-city admission."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parent

def main():
    people=pd.read_parquet(P/'personas.parquet');homes=pd.read_parquet(P/'hogares.parquet');trips=pd.read_parquet(P/'viajes.parquet')
    assert people.Persona.is_unique and homes.Hogar.is_unique and trips.Viaje.is_unique
    people=people.merge(homes[['Hogar','Comuna','TipoDia','Temporada','DirCoordX','DirCoordY']],on='Hogar',validate='many_to_one')
    select=people.Actividad.fillna('').str.split(';').apply(lambda x:'B' in x)&people.DondeEstudia.eq(4)&people.Estudios.isin([5,7])&people.TipoDia.eq(1)&people.Temporada.eq(1)
    candidates=people[select].copy()
    records=[];summary=[]
    for scope,group in [('metro',candidates),('comuna_santiago',candidates[candidates.Comuna.eq('SANTIAGO')])]:
        rows=[]
        for p in group.to_dict('records'):
            w=p['Factor_LaboralNormal'];vv=trips[trips.Persona==p['Persona']].copy()
            vv=vv[vv.Proposito.eq(3)]
            # No arbitrary distance threshold: identical archived home-origin coordinates.
            vv=vv[np.isclose(vv.OrigenCoordX,p['DirCoordX'],rtol=0,atol=1e-6)&np.isclose(vv.OrigenCoordY,p['DirCoordY'],rtol=0,atol=1e-6)]
            # Unknown/invalid departure times prevent reliable first-trip selection.
            clock=pd.to_timedelta(vv.HoraIni.astype(str)+':00',errors='coerce')
            lo=0.;hi=1.;reason='no_identified_home_to_school_trip';n=len(vv)
            if n and clock.notna().all():
                vv=vv.assign(clock=clock).sort_values(['clock','Viaje']);r=vv.iloc[0];t=r.TiempoViaje
                if r.CodigoTiempo==0 and pd.notna(t) and t>0:
                    lo=hi=float(np.exp(-t/30));reason='valid_first_direct_school_trip'
                else:reason='duration_quality_or_missing'
            elif n:reason='departure_order_unknown'
            rows.append(dict(scope=scope,person=p['Persona'],weight=w,utility_lower=lo,utility_upper=hi,status=reason,direct_trip_candidates=n))
        f=pd.DataFrame(rows);known=f.weight.notna()&f.weight.gt(0);k=f[known]
        assert np.all(k.utility_lower<=k.utility_upper)
        if len(k):
            den=k.weight.sum();lower=float((k.weight*k.utility_lower).sum()/den);upper=float((k.weight*k.utility_upper).sum()/den)
        else:lower=0.;upper=1.;den=0
        summary.append(dict(scope=scope,candidate_persons=len(f),valid_weight_persons=int(known.sum()),unknown_or_invalid_weight=int((~known).sum()),valid_duration_persons=int((k.utility_lower==k.utility_upper).sum()),weighted_denominator=float(den),utility_lower=lower,utility_upper=upper,main_admitted=False))
        records.extend(rows)
    pd.DataFrame(records).to_csv(P/'conditional_person_audit.csv',index=False)
    (P/'conditional_commute_bounds.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
