"""Render all160 retained utility ranges; do not change model inputs or rankings."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, subprocess, shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from task4_v5_model import NAMES

R = Path(__file__).resolve().parents[1]
O = R.parents[2] / 'HiMCM-Overleaf' / 'drafts/task4_v198_assets'
DISPLAY = {'homicide_rate':'Homicide', 'pm25':'PM2.5',
           'cost_living_index':'Living cost', 'price_income_ratio':'Housing',
           'upper_secondary_ptr':'Pupil/teacher', 'research_he_density':'Research/HE',
           'public_transport_density':'Transit', 'travel':'Travel burden',
           'fixed_broadband_mbps':'Broadband', 'public_pool_density':'Pools'}
assert set(DISPLAY)==set(NAMES)
LABELS = [DISPLAY[n] for n in NAMES]


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    bounds = pd.read_csv(R/'results/task4_user_v197_revision/utility_bounds.csv', float_precision='round_trip')
    bounds = bounds[bounds.scenario.eq('after_conditional')]
    cities = bounds.city.drop_duplicates().tolist()
    assert len(bounds) == 160 and not bounds.duplicated(['city', 'indicator']).any()
    indexed = bounds.set_index(['city', 'indicator'])
    frame = pd.DataFrame({'city': cities})
    lo = np.array([[indexed.loc[(city, name), 'lower'] for name in NAMES] for city in cities])
    hi = np.array([[indexed.loc[(city, name), 'upper'] for name in NAMES] for city in cities])
    assert lo.shape == hi.shape == (16, 10)
    width = hi-lo
    assert np.all(width >= 0) and np.all(width <= 1)
    rows = []
    for i, city in enumerate(frame.city):
        for j, indicator in enumerate(NAMES):
            state = 'point' if lo[i,j] == hi[i,j] else ('unknown' if lo[i,j] == 0 and hi[i,j] == 1 else 'partial')
            rows.append(dict(city=city, indicator=indicator, plot_label=LABELS[j], utility_lower=float(lo[i,j]), utility_upper=float(hi[i,j]), interval_width=float(width[i,j]), state=state))
    counts = Counter(r['state'] for r in rows)
    assert counts == {'point':112, 'partial':37, 'unknown':11}
    unknowns = Counter(r['indicator'] for r in rows if r['state']=='unknown')
    assert unknowns == {'upper_secondary_ptr':8, 'travel':3}
    O.mkdir(exist_ok=True)
    with (O/'matrix.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
                         'svg.fonttype':'none', 'pdf.fonttype':3})
    cmap = LinearSegmentedColormap.from_list('identified_range', ['#f7fafb','#9dc4d2','#215c78'])
    fig = plt.figure(figsize=(6.5,6.2), facecolor='white')
    left,bottom,gridw,gridh=.19,.21,.78,.54
    cw,ch=gridw/10,gridh/16
    for i,city in enumerate(frame.city):
        fig.text(left-.01,bottom+gridh-(i+.5)*ch,city,ha='right',va='center',fontsize=10)
    for j,label in enumerate(LABELS):
        fig.text(left+(j+.5)*cw,bottom+gridh+.012,label,rotation=55,
                 ha='left',va='bottom',rotation_mode='anchor',fontsize=10)
    for row in rows:
        i = frame.city.tolist().index(row['city']); j = NAMES.index(row['indicator'])
        x,y=left+j*cw,bottom+gridh-(i+1)*ch
        fig.add_artist(Rectangle((x,y),cw,ch,transform=fig.transFigure,facecolor=cmap(width[i,j]),
                                 edgecolor='#cdd6da',linewidth=.5,clip_on=False,gid=f'cell-{i}-{j}'))
        if row['state']=='point':
            fig.add_artist(Line2D([x+cw/2],[y+ch/2],transform=fig.transFigure,marker='o',
                                  markersize=2.8,linestyle='None',color='#344751',clip_on=False))
        elif row['state']=='unknown':
            fig.text(x+cw/2,y+ch/2,'?',ha='center',va='center',color='white',fontsize=10,weight='bold')
    fig.text(.19,.977,'Identification ranges in the 16-city matrix',fontsize=12,weight='bold',va='top')
    fig.text(.19,.935,'112 point; 37 partial; 11 unknown (8 pupil/teacher, 3 travel)',fontsize=10,va='top')
    # Explicit vector swatches avoid backend-specific mesh clipping of labels.
    for k in range(64):
        fig.add_artist(Rectangle((.30+k*.58/64,.132),.58/64,.022,transform=fig.transFigure,
                                 facecolor=cmap((k+.5)/64),edgecolor='none',clip_on=False))
    fig.add_artist(Rectangle((.30,.132),.58,.022,transform=fig.transFigure,
                             facecolor='none',edgecolor='black',linewidth=.5,clip_on=False))
    for tick in [0,.5,1]:
        x=.30+tick*.58
        fig.add_artist(Line2D([x,x],[.132,.127],transform=fig.transFigure,color='black',linewidth=.5,clip_on=False))
        fig.text(x,.119,f'{tick:.1f}',ha='center',va='top',fontsize=10)
    fig.text(.59,.087,'Utility interval width (upper − lower)',ha='center',va='top',fontsize=10)
    fig.text(.025,.033,'Dot: point assumption.  ?: unknown.  Source: V197 utility bounds.',fontsize=10)
    for ext in ['pdf','svg','png']:
        fig.savefig(O/f'identification_matrix.{ext}',dpi=300,metadata={'Creator':'HiMCM research'} if ext!='png' else None)
    plt.close(fig)
    svg=O/'identification_matrix.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    text=subprocess.check_output(['pdftotext',str(O/'identification_matrix.pdf'),'-'],text=True)
    assert text.count('?')==12 and all(s in text for s in ['112 point','37 partial','11 unknown'])
    result = dict(iteration='V198', model='V197', shape=[16,10], counts=dict(counts),
                  unknown_by_indicator=dict(unknowns), city_order=frame.city.tolist(), indicator_order=NAMES,
                  plot_labels=LABELS, source='V197 audited utility_bounds.csv after_conditional; original CSV and 25 supplemented city-indicator keys retained',
                  source_csv_sha256=sha(R/'data/task4_v117_team_intake/city_indicators.csv'),
                  utility_bounds_sha256=sha(R/'results/task4_user_v197_revision/utility_bounds.csv'),
                  matrix_sha256=sha(O/'matrix.csv'), renderer_sha256=sha(Path(__file__)),
                  admissions_sha256=sha(R/'design/task4_user_v197_admissions.json'), figure_width_inches=6.5, figure_height_inches=6.2,
                  minimum_source_font_pt=10, intended_insertion_width_inches=6.5,
                  minimum_insertion_width_for9pt_inches=5.85, png_dpi=300,
                  pdf_export='Explicit vector rectangles and embedded Type3 outline fonts; RGB and grayscale review required',
                  point_interpretation='Retained point assumptions, not independent validation or zero measurement error',
                  ranges_interpretation='Identification bounds; not confidence intervals, posterior probabilities or ranking',
                  renderer_changes_source_data=False, intended_review='V198', source_state_at_creation='V197 staged',
                  output_sha256={ext:sha(O/f'identification_matrix.{ext}') for ext in ['pdf','svg','png']})
    (O/'figure_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    audit = R / 'results/task4_v198_review'
    audit.mkdir(exist_ok=True)
    (audit/'matrix_figure_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'rendered','counts':dict(counts),'unknown_by_indicator':dict(unknowns)}))


if __name__=='__main__': main()
