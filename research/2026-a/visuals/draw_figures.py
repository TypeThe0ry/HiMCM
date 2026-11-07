from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; OUT=HERE/'figures';OUT.mkdir(exist_ok=True)
R=BASE/'results/task4_access_revision'
plt.rcParams.update({'font.family':'serif','font.serif':['DejaVu Serif'],'font.size':9,'axes.titlesize':11,'axes.labelsize':9,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.65,'xtick.major.width':.6,'ytick.major.width':.6,'savefig.dpi':240,'pdf.fonttype':42,'svg.fonttype':'none'})
blue='#365F78'; orange='#B87945';gray='#9AA3A9'; green='#647D69'
files=[]
def save(fig,name,note):
 fig.text(.02,.012,note,fontsize=7,color='#555555',ha='left',va='bottom')
 for ext in ['png','pdf','svg']:fig.savefig(OUT/(name+'.'+ext),bbox_inches='tight',facecolor='white')
 files.append(name);plt.close(fig)
rank=pd.read_csv(R/'point_rankings.csv').sort_values('V3_rank'); cities=rank.city.tolist()
# 1. Full sample rank trajectories.
fig,ax=plt.subplots(figsize=(7.2,8.4));x=np.arange(3)
for _,r in rank.iterrows():
 ys=[r.V0_rank_common_sample,r.access_mean_only_rank,r.V3_rank]
 color=orange if r.city=='Dubai' else blue if r.city in ['Toronto','Copenhagen','Tokyo'] else '#B9BFC3'
 ax.plot(x,ys,'o-',color=color,lw=1.5 if color!='#B9BFC3' else .7,ms=3,zorder=3 if color!='#B9BFC3' else 1)
 ax.text(-.06,ys[0],f'{r.city}  {int(ys[0])}',ha='right',va='center',fontsize=8,color=color if color!='#B9BFC3' else '#444')
 ax.text(2.06,ys[2],f'{int(ys[2])}  {r.city}',ha='left',va='center',fontsize=8,color=color if color!='#B9BFC3' else '#444')
ax.set(xticks=x,xticklabels=['Four proxies\nV0','Add mean\naccessibility','Add lower-tail\npenalty (V3)'],ylim=(26,0),xlim=(-.04,2.04),yticks=[])
ax.spines[['left','bottom']].set_visible(False);ax.tick_params(axis='x',length=0);ax.set_title('Rank changes after adding learning-facility accessibility',pad=18)
fig.subplots_adjust(left=.26,right=.74,bottom=.12)
save(fig,'01_rank_revision','25-city archived analysis. Ranking changes reflect a changed evaluation model, not measured improvement.')
# 2. Mechanism.
a=pd.read_csv(R/'learning_access_measures.csv').set_index('city').loc[cities]
fig,ax=plt.subplots(figsize=(7.2,7.8));y=np.arange(len(a))
ax.hlines(y,a.lower_quintile_utility,a.mean_utility_lower,color='#C4C8CB',lw=1.2)
ax.scatter(a.mean_utility_lower,y,s=27,color=blue,label='Population mean',zorder=3)
ax.scatter(a.lower_quintile_utility,y,s=24,color=orange,marker='s',label='Lowest-access 20%',zorder=3)
ax.scatter(a.q_low,y,s=30,color='white',edgecolor=green,marker='D',label='Combined Q (lower bound)',zorder=4)
ax.set(yticks=y,yticklabels=a.index,xlim=(0,1),xlabel='Accessibility utility (dimensionless; higher is better)');ax.invert_yaxis();ax.grid(axis='x',color='#EAEAEA',lw=.5);ax.legend(loc='lower right',frameon=False,fontsize=8);ax.set_title('City averages conceal differences in access')
fig.subplots_adjust(left=.23,bottom=.12)
save(fig,'02_accessibility_gap','Model-derived resident learning-facility proxy; not school quality. Walking; tau = 30 min; tail weight = 0.30.')
# 3. Matched information intervals.
b=pd.read_csv(R/'matched_information_rank_bounds.csv');before=b[b.stage=='before_two_unknown'].set_index('city').loc[cities];after=b[b.stage!='before_two_unknown'].set_index('city').loc[cities]
fig,axes=plt.subplots(1,2,figsize=(9,8),sharey=True,sharex=True)
for ax,df,title,color in zip(axes,[before,after],['Before: access + education unknown','After: access observed; education unknown'],[gray,blue]):
 for j,(city,r) in enumerate(df.iterrows()):
  ax.plot([r.score_lower,r.score_upper],[j,j],lw=2,color=color)
  ax.plot([r.score_lower,r.score_upper],[j,j],'|',color=color,ms=5)
  if r.possible_champion:ax.scatter(r.score_upper,j,marker='o',s=24,facecolors='white',edgecolors=orange,zorder=4)
 ax.set_title(title,fontsize=10);ax.set_xlabel('Feasible score interval');ax.grid(axis='x',color='#EEEEEE',lw=.5)
axes[0].set(yticks=y,yticklabels=cities,ylim=(24.7,-.7));axes[1].plot([],[],'o',mfc='white',mec=orange,label='Possible champion');axes[1].legend(frameon=False,loc='lower right',fontsize=8)
fig.subplots_adjust(left=.17,bottom=.12,wspace=.1)
save(fig,'03_information_bounds','Same model and weights in both panels: four proxies 80%, access 10%, unknown education 10%. Not confidence intervals.')
# 4. Evidence heatmap.
z=pd.read_csv(BASE/'results/task4_real/normalized_indicators.csv').set_index('city').loc[cities]
z.columns=['Safety','Cleanliness','Housing\naffordability','Commute'];z['Learning\naccess (Q)']=a.q_low
fig,ax=plt.subplots(figsize=(7,8.2));im=ax.imshow(z.values,vmin=0,vmax=1,cmap='YlGnBu',aspect='auto')
ax.set(xticks=np.arange(5),xticklabels=z.columns,yticks=y,yticklabels=cities);ax.tick_params(length=0)
for i in range(len(z)):
 for j in range(5):ax.text(j,i,f'{z.iloc[i,j]:.2f}',ha='center',va='center',fontsize=7,color='white' if z.iloc[i,j]>.63 else '#25313B')
ax.set_title('Five proxy indicators across the 25-city sample',pad=14);fig.colorbar(im,ax=ax,fraction=.035,pad=.035,label='Oriented utility / normalized score')
fig.subplots_adjust(left=.23,bottom=.13)
save(fig,'04_indicator_heatmap','Columns are proxy measures, not direct student outcomes. Higher is better. City order follows the V3 ranking.')
# 5. Error assumptions.
stress=json.loads((R/'proxy_error_stress.json').read_text());xx=[r['assumed_access_utility_error'] for r in stress];nn=[len(r['possible_champions']) for r in stress]
fig,ax=plt.subplots(figsize=(6.4,3.7));ax.plot(xx,nn,'o-',color=blue,lw=1.5,ms=5)
for xv,n in zip(xx,nn):ax.annotate(str(n),(xv,n),xytext=(0,8),textcoords='offset points',ha='center')
ax.set(xticks=xx,ylim=(0,12),yticks=[0,3,6,9,12],xlabel='Assumed additional access-utility error (±)',ylabel='Number of possible champions',title='The shortlist depends on proxy accuracy');ax.grid(axis='y',lw=.5,color='#E7E7E7');fig.subplots_adjust(bottom=.24)
save(fig,'05_proxy_error','Stress assumptions, not estimated measurement errors. Education remains unknown; this is not a probability curve.')
# 6. Plain academic workflow, no decorative illustration.
fig,ax=plt.subplots(figsize=(9,4.5));ax.set(xlim=(0,10),ylim=(0,5));ax.axis('off')
boxes=[(.2,3.2,'Define the comparison','25 cities; teenager perspective'),(3.6,3.2,'Construct a baseline','Four city-level proxy indicators'),(7,3.2,'Diagnose missing evidence','Access distribution; education'),(.2,.8,'Measure local accessibility','Population mean +\nlowest-access tail'),(3.6,.8,'Separate two experiments','A: revise ranking\nB: add evidence at fixed weights'),(7,.8,'Conditional conclusions','Rank shifts; feasible winners\nProxy-error sensitivity')]
for x0,y0,title,sub in boxes:
 ax.add_patch(Rectangle((x0,y0),2.8,1.15,facecolor='#F5F7F8',edgecolor=blue,lw=.85));ax.text(x0+1.4,y0+.83,title,ha='center',va='center',fontsize=9,fontweight='bold');ax.text(x0+1.4,y0+.38,sub,ha='center',va='center',fontsize=8,linespacing=1.5)
for p,q in [((3,3.78),(3.6,3.78)),((6.4,3.78),(7,3.78)),((3,1.38),(3.6,1.38)),((6.4,1.38),(7,1.38))]:ax.annotate('',xy=q,xytext=p,arrowprops=dict(arrowstyle='->',lw=.9,color=blue))
ax.plot([8.4,8.4,1.6,1.6],[3.2,2.65,2.65,2.0],color=blue,lw=.9);ax.annotate('',xy=(1.6,1.95),xytext=(1.6,2.15),arrowprops=dict(arrowstyle='->',color=blue,lw=.9))
ax.set_title('An evidence-led revision of the city evaluation model',pad=10)
save(fig,'06_model_workflow','Research workflow proposal. Education quality, eligibility and teenager-specific travel remain unresolved.')
# Compact preview of all charts.
canvas=Image.new('RGB',(1800,1800),'#EEEDE9');draw=ImageDraw.Draw(canvas)
for k,name in enumerate(files):
 im=Image.open(OUT/(name+'.png')).convert('RGB');im.thumbnail((870,550));x=(k%2)*900+(900-im.width)//2;y=(k//2)*600+35;canvas.paste(im,(x,y));draw.text(((k%2)*900+20,(k//2)*600+12),name,fill='#334455')
canvas.save(HERE/'figure_preview.jpg',quality=92)
print('Created',len(files),'figures as PDF / SVG / PNG')
