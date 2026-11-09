"""Display all frozen auxiliary contrasts; never enter legacy25 as the primary model."""
from pathlib import Path
import csv,hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
R=Path(__file__).resolve().parents[1];O=R/'results/task4_v172_country_review/figure_asset'
LABELS={'homicide_rate':'Homicide','pm25':'PM2.5','cost_living_index':'Living cost',
 'price_income_ratio':'Housing','upper_secondary_ptr':'School proxy','research_he_density':'Research/HE',
 'public_transport_density':'Transit','travel':'Travel burden','fixed_broadband_mbps':'Broadband','public_pool_density':'Pools'}
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 O.mkdir(parents=True,exist_ok=True)
 ip=R/'results/task4_v154_method/country_indicator_bounds.csv';sp=R/'results/task4_v154_method/country_score_comparison.csv'
 data=rows(ip);score=rows(sp);out=[]
 for x in data:
  lo=float(x['a_lower'])-float(x['b_upper']);hi=float(x['a_upper'])-float(x['b_lower'])
  out.append(dict(country=x['country'],city_a=x['city_a'],city_b=x['city_b'],indicator=x['indicator'],
   plot_label=LABELS[x['indicator']],difference_lower=lo,difference_upper=hi,
   sign_identified=lo>0 or hi<0,first_city_advantage=lo>0,second_city_advantage=hi<0))
 assert len(out)==20 and sum(x['sign_identified'] for x in out)==7
 with (O/'contrasts.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(out[0]),lineterminator='\n');w.writeheader();w.writerows(out)
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'svg.fonttype':'none'})
 fig=plt.figure(figsize=(6.5,4.1),facecolor='white')
 top=fig.add_axes([.27,.73,.68,.20]);y=3
 for pair in score:
  for prefix,city in [('a',pair['city_a']),('b',pair['city_b'])]:
   lo,hi=[float(pair[f'{prefix}_score_{side}']) for side in ['lower','upper']]
   top.plot([lo,hi],[y,y],color='#536778',lw=2,solid_capstyle='butt')
   top.plot([lo,hi],[y,y],'|',color='#536778',ms=7,mew=1.2)
   top.text(102,y,f'{lo:.2f}-{hi:.2f}',ha='right',va='center',fontsize=9.5)
   y-=1
 top.set(xlim=(0,104),ylim=(-.6,3.6),yticks=[3,2,1,0],yticklabels=['Phoenix','New York','Mumbai','Delhi'],xticks=[0,25,50,75,100])
 top.set_xlabel('TOPSIS score (0-100)',fontsize=10,labelpad=2)
 top.tick_params(axis='both',labelsize=10,length=0,pad=4)
 top.grid(axis='x',alpha=.20,lw=.6);top.set_axisbelow(True)
 for spine in top.spines.values():spine.set_visible(False)
 fig.text(.03,.985,'A  Historical score intervals',fontsize=11.5,weight='bold',va='top')
 heading_b=fig.text(.03,.59,'B  Contrasts',fontsize=11.5,weight='bold',va='top')
 for k,pair in enumerate(score):
  ax=fig.add_axes([.27 if k==0 else .66,.115,.29,.40])
  group=[x for x in out if x['city_a']==pair['city_a']]
  for y,x in enumerate(group):
   lo,hi=x['difference_lower'],x['difference_upper']
   colour='#1d6d8b' if lo>0 else '#b05c29' if hi<0 else '#a4abb2'
   if abs(hi-lo)<1e-14:ax.plot([lo],[y],'o',color=colour,ms=4)
   else:
    ax.plot([lo,hi],[y,y],color=colour,lw=2 if x['sign_identified'] else 1.2)
    ax.plot([lo,hi],[y,y],'|',color=colour,ms=5,mew=1)
  ax.axvline(0,color='#37434c',lw=.7,ls='--')
  ax.set(xlim=(-1.04,1.04),ylim=(9.6,-.6),yticks=range(10),
   yticklabels=[x['plot_label'] for x in group] if k==0 else [],xticks=[-1,0,1])
  ax.set_title(pair['city_a']+' - '+pair['city_b'],fontsize=10.5,pad=6)
  ax.tick_params(axis='both',length=0,labelsize=10,pad=4)
  ax.set_xlabel('Utility difference',fontsize=10,labelpad=3)
  ax.grid(axis='x',alpha=.13,lw=.6);ax.set_axisbelow(True)
  for spine in ax.spines.values():spine.set_visible(False)
 fig.canvas.draw()
 renderer=fig.canvas.get_renderer()
 assert all(not heading_b.get_window_extent(renderer).overlaps(ax.title.get_window_extent(renderer)) for ax in fig.axes[1:])
 for ext in ['pdf','svg','png']:fig.savefig(O/f'country_contrasts.{ext}',dpi=300,metadata={'Creator':'HiMCM V172'} if ext=='pdf' else None)
 fonts=[t.get_fontsize() for t in fig.findobj(match=matplotlib.text.Text) if t.get_text()]
 plt.close(fig)
 manifest=dict(version='V172',source_dataset='Frozen auxiliary legacy25 V117; never primary16',
  source_sha256={str(ip.relative_to(R)):sha(ip),str(sp.relative_to(R)):sha(sp)},
  contrasts=20,sign_identified=7,unresolved=13,figure_inches=[6.5,4.1],minimum_font_pt=min(fonts),
  definition='difference interval=[a_lower-b_upper,a_upper-b_lower]; utility scale, not score contribution or confidence interval',
  output_sha256={ext:sha(O/f'country_contrasts.{ext}') for ext in ['pdf','svg','png']})
 (O/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
if __name__=='__main__':main()
