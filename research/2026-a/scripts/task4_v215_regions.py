"""Regional grouping of the 44-city sample (V215, TT 15 Nov: one extra page)."""
import json
import pandas as pd
from task4_v5_model import ROOT

REGION = {
    'Europe': ['Luxembourg', 'Zurich', 'Reykjavik', 'Madrid', 'Milan', 'Dublin', 'Paris', 'Helsinki', 'Copenhagen',
               'Prague', 'Oslo', 'London', 'Amsterdam', 'Berlin', 'Stockholm', 'Warsaw', 'Vienna'],
    'East Asia': ['Macao SAR', 'Hong Kong SAR', 'Guangzhou', 'Beijing', 'Shenzhen', 'Shanghai', 'Tokyo', 'Seoul'],
    'Gulf and Türkiye': ['Dubai', 'Abu Dhabi', 'Istanbul'],
    'Southeast Asia and Oceania': ['Singapore', 'Kuala Lumpur', 'Sydney'],
    'North America': ['Toronto', 'San Francisco', 'New York', 'Los Angeles', 'Chicago'],
    'Latin America': ['Buenos Aires', 'Sao Paulo', 'Mexico City'],
    'South Asia': ['New Delhi', 'Mumbai'],
    'Africa': ['Cairo', 'Nairobi', 'Johannesburg'],
}
CATS = ['Safety and environment', 'Cost of living', 'Education', 'Mobility', 'Daily life']


def regions():
    m = pd.read_csv(ROOT / 'results/task4_v214_final/main_ranking.csv')
    m['region'] = m.city.map({c: r for r, cs in REGION.items() for c in cs})
    assert m.region.notna().all() and len(m) == 44
    g = m.groupby('region')
    out = pd.DataFrame({'n': g.size(), 'median_score': g.score.median(), 'best': g.apply(lambda d: d.loc[d.score.idxmax(), 'city']),
                        'best_rank': g['rank'].min(), 'worst': g.apply(lambda d: d.loc[d.score.idxmin(), 'city']), 'worst_rank': g['rank'].max()})
    out = out.join(g[CATS].mean()).sort_values('median_score', ascending=False)
    return m, out


if __name__ == '__main__':
    m, out = regions()
    p = ROOT / 'results/task4_v214_final/regions.csv'
    out.round(3).to_csv(p)
    print(out.round(2).to_string())
    top10 = m.nsmallest(10, 'rank').region.value_counts().to_dict()
    json.dump({'top10_by_region': top10}, open(ROOT / 'results/task4_v214_final/regions_top10.json', 'w'), indent=1)
    print(top10)
