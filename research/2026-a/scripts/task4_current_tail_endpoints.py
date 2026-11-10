"""Decimal endpoint certificate for the existing fractional-mass tail gap."""
import argparse
import csv
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

R=Path(__file__).resolve().parents[1]
SOURCE=R/'data/task4_v116_ibb/aggregate_results.json'


def dec(f):return Decimal(f.numerator)/Decimal(f.denominator)
def csv_write(p,rows):
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n')
        w.writeheader();w.writerows(rows)


def calculate():
    source=json.loads(SOURCE.read_text())
    groups=sorted((int(t),int(v['weight'])) for t,v in source['duration_histogram'].items())
    W=sum(w for t,w in groups);U=source['summary']['weight_unknown']
    B=source['optional_membership']['weight_total'];N=W+U+B
    assert len(groups)==49 and (W,U,B,N)==(499950,177066,4487,681503)
    alpha=Decimal(1)/5
    q=[(-Decimal(t)/30).exp() for t,w in groups]
    weights=[Decimal(w) for t,w in groups]
    knots=sorted({Decimal(0),Decimal(1),*q});assert len(knots)==51
    minutes={u:t for u,(t,w) in zip(q,groups)}
    budgets=[Fraction(0),Fraction(1,100),Fraction(1,20),Fraction(1,10),
             Fraction(1,5),Fraction(1,2),Fraction(W-max(w for t,w in groups),W)]
    results=[];thresholds=[];witnesses=[]
    for case,delta in enumerate(budgets):
        retain=dec((1-delta)*W);best=None
        for z in knots:
            costs=[u-z if u>=z else (1/alpha-1)*(z-u) for u in q]
            remaining=retain;kept=[Decimal(0)]*len(groups)
            for i in sorted(range(len(groups)),key=lambda i:(costs[i],groups[i][0])):
                kept[i]=min(remaining,weights[i]);remaining-=kept[i]
                if not remaining:break
            assert remaining==0
            gap=sum(k*c for k,c in zip(kept,costs))/N
            thresholds.append(dict(case=case,threshold_utility=str(z),gap=str(gap)))
            if best is None or gap<best[0]:best=(gap,z,kept)
        gap,z,kept=best
        edited=Decimal(W)-sum(kept)
        completion=list(zip(q,kept))+[(z,Decimal(U+B)+edited)]
        mean=sum(u*w for u,w in completion)/N
        left=alpha*N;tail_total=Decimal(0)
        for u,w in sorted(completion):
            take=min(left,w);tail_total+=take*u;left-=take
            if not left:break
        assert left==0
        tail=tail_total/(alpha*N)
        assert abs(mean-tail-gap)<Decimal('1e-70')
        assert edited==dec(delta*W)
        assert z in minutes, 'The seven retained scenarios must have finite-duration witnesses'
        results.append(dict(case=case,delta=float(delta),delta_exact=str(delta),
            sharp_gap=str(gap),attaining_minutes=minutes[z],
            witness_mean=str(mean),witness_lower_tail=str(tail),edited_weight=str(edited)))
        witnesses.extend(dict(case=case,original_minutes=t,original_weight=w,
                              kept_weight=str(k),edited_weight=str(Decimal(w)-k),
                              reassigned_minutes=minutes[z]) for (t,w),k in zip(groups,kept))
    old=json.loads((R/'results/task4_v162_tail_error/summary.json').read_text())
    assert len(old['rows'])==len(results)==7
    errors=[abs(float(row['sharp_gap'])-prior['sharp_gap_in_fractional_mass_set'])
            for row,prior in zip(results,old['rows'])]
    assert max(errors)<1e-12
    summary=dict(scope='Istanbul2012 retained aggregate; fractional observed-utility mass errors only',
        alpha='1/5',observed_groups=49,observed_weight=W,known_unknown_weight=U,
        optional_weight=B,max_denominator=N,decimal_precision=80,
        old_thresholds=old['breakpoints'],endpoint_thresholds=len(knots),
        budget_cases=7,endpoint_evaluations=len(thresholds),rows=results,
        max_gap_difference_from_frozen_V162=max(errors),
        exact_zero_gap_budget=str(budgets[-1]),
        source_representation_upgraded=False,error_rates_estimated=False,
        whole_person_sharpness_claimed=False,primary_admissions=0,
        actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
        scope_note='Concavity between observed utility knots eliminates pair-cost crossings; numerical precision is not a directed-rounding or data-accuracy certificate')
    return summary,thresholds,witnesses


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True)
    out=p.parse_args().output_dir.resolve()
    if out.exists():raise FileExistsError('Use a new output directory')
    with localcontext() as ctx:
        ctx.prec=80;summary,thresholds,witnesses=calculate()
    out.mkdir(parents=True)
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    csv_write(out/'endpoint_values.csv',thresholds);csv_write(out/'witnesses.csv',witnesses)
    print(json.dumps({k:summary[k] for k in ['endpoint_thresholds','budget_cases',
                       'endpoint_evaluations','max_gap_difference_from_frozen_V162']}))


if __name__=='__main__':main()
