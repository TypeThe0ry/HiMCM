from pathlib import Path
import json,zipfile,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyArrowPatch
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap,Normalize
from matplotlib.lines import Line2D
from PIL import Image,ImageDraw,ImageFont
import pymupdf as fitz
H=Path(__file__).resolve().parent;B=H.parents[1];O=H/'figures';O.mkdir(exist_ok=True)
R=B/'results/task4_access_revision';D=B/'data/task4_access'
plt.rcParams.update({'font.family':'Times New Roman','mathtext.fontset':'stix','font.size':10,'axes.labelsize':10,'axes.titlesize':10,'xtick.labelsize':9,'ytick.labelsize':9,'axes.linewidth':.65,'lines.linewidth':1.25,'xtick.direction':'in','ytick.direction':'in','xtick.major.size':3,'ytick.major.size':3,'legend.fontsize':9,'legend.frameon':False,'pdf.fonttype':42,'svg.fonttype':'none','savefig.dpi':300})
navy='#46566F';rose='#B33561';gold='#E9A33B';mint='#78B3A0';salmon='#E99478';lav='#8D83B6';ink='#25262A'
cs={'Copenhagen':navy,'Toronto':gold,'Dubai':rose};names=['Copenhagen','Toronto','Dubai']
rank=pd.read_csv(R/'point_rankings.csv').sort_values('V3_rank');cities=rank.city.tolist()
a=pd.read_csv(R/'learning_access_measures.csv').set_index('city')
b=pd.read_csv(R/'matched_information_rank_bounds.csv');before=b[b.stage=='before_two_unknown'].set_index('city');after=b[b.stage!='before_two_unknown'].set_index('city')
records=[]
def save(fig,name,caption,inputs,reference):
 for ext in ['pdf','svg','png']:fig.savefig(O/f'{name}.{ext}',bbox_inches='tight',pad_inches=.04,facecolor='white')
 records.append(dict(name=name,caption=caption,inputs=inputs,style_reference=reference));plt.close(fig)
def panel(ax,label,title):
 ax.set_title(f'({label})  {title}',loc='left',pad=9,fontweight='normal')
def lighten(hex,f=.84):
 import matplotlib.colors as co
 v=np.array(co.to_rgb(hex));return tuple(v*(1-f)+f)
# Load only three demonstrative cities, keeping archived source grids.
manifest=json.loads((D/'manifest.json').read_text());grids={};gridchecks=[]
for row in manifest:
 if row['city'] not in names:continue
 with zipfile.ZipFile(D/row['file']) as z:features=json.loads(z.read('hexes.geojson'))['features']
 features=[f for f in features if f['properties']['population']>0]
 pop=np.array([f['properties']['population'] for f in features]);time=np.array([f['properties']['c_f'] for f in features]);assert np.isfinite(time).all() and (time>0).all()
 u=np.exp(-time/30);mu=np.average(u,weights=pop);ii=np.argsort(u);mass=pop[ii];take=np.clip(.2*mass.sum()-(np.cumsum(mass)-mass),0,mass);tail=np.dot(u[ii],take)/(.2*mass.sum())
 assert np.isclose(mu,a.loc[row['city'],'mean_utility_lower']) and np.isclose(tail,a.loc[row['city'],'lower_quintile_utility'])
 grids[row['city']]=(features,pop,time,u)
 gridchecks.append({'city':row['city'],'cells':len(features),'mean_verified':float(mu),'lower_tail_verified':float(tail),'source_sha256':hashlib.sha256((D/row['file']).read_bytes()).hexdigest()})
# 01: source-style structured model overview. Small type, coloured functional groups, dashed enclosures.
fig,ax=plt.subplots(figsize=(10.2,6.35));ax.set(xlim=(0,100),ylim=(0,62));ax.axis('off')
def text(x,y,s,size=9,**kw):return ax.text(x,y,s,fontsize=size,ha='center',va='center',color=ink,**kw)
def box(x,y,w,h,s,col,size=9):
 ax.add_patch(Rectangle((x,y),w,h,facecolor=lighten(col,.78),edgecolor=col,lw=.65));text(x+w/2,y+h/2,s,size)
def arr(p,q,c='#6B6B6B'):ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=8,lw=.65,color=c))
def frame(x,y,w,h,title,c):
 ax.add_patch(Rectangle((x,y),w,h,fill=False,edgecolor='#8F8F8F',lw=.8,linestyle=(0,(3,2))))
 ax.add_patch(Rectangle((x+.15,y+h-4.3),w-.3,4.1,facecolor=lighten(c,.91),edgecolor='none'))
 ax.text(x+1.3,y+h-2.1,title,fontsize=10,ha='left',va='center',color=ink,fontweight='bold')
frame(1,33,47.5,28,'1. Define the comparison and its evidence',salmon)
frame(51.5,33,47.5,28,'2. Establish the city-level baseline',gold)
frame(1,1,47.5,29,'3. Measure access beyond the city average',lav)
frame(51.5,1,47.5,29,'4. Separate model revision from information gain',mint)
box(3,41.5,12,9,'25 cities\nCommon sample',lav);arr((15,46),(18,46))
for k,s in enumerate(['Safety','Cleanliness','Housing burden','Adult commute']):box(18,51-k*4.3,17,3.3,s,salmon,8.5)
ax.plot([36,37.2,37.2,36],[54.3,54.3,37.8,37.8],lw=.7,color='#555')
box(39,41,7.3,10,'Proxy\nmatrix\n'+r'$z_{ij}$',salmon,9);arr((37.3,46),(39,46))
text(25,35.6,'Age-specific education evidence remains missing.',8.4,fontstyle='italic')
box(54,49,18,6,'Orient and normalize\nbenefit / cost indicators',gold,8.8);arr((72,52),(77,52));box(77,49,19,6,'Equal baseline weights\n'+r'$w_j=1/4$',gold,9)
arr((86.5,49),(86.5,45.3));box(65,39,31,6,'Fixed-ideal TOPSIS\n'+r'$C_i=D_i^-/(D_i^-+D_i^+)$',gold,10)
arr((65,42),(61,42));box(54,38.3,7,7.4,'V0\nranking',salmon,9)
text(75,35.6,'Baseline winner: Copenhagen',8.8,fontstyle='italic')
box(3,17,12,7,'Resident grids\n'+r'$(p_{ir},t_{ir})$',lav,9);arr((15,20.5),(18,20.5))
box(18,17,27,7,'Travel time to learning POIs\n'+r'$u_{ir}=\exp(-t_{ir}/30)$',lav,10)
arr((25,17),(16,13));arr((34,17),(36,13))
box(4,8,22,5,'Population mean  '+r'$\mu_i$',lav,9.2);box(29,8,17,5,'Lowest 20%  '+r'$L_i$',lav,9.2)
arr((15,8),(21,5.8));arr((36,8),(29,5.8));text(25,4.2,r'$Q_i=0.7\mu_i+0.3L_i$',12)
# Two clearly separate experiments rather than a single chain.
box(54,18,19,6,'A. Change the model\nFive proxies, 20% each',mint,9)
box(77,18,19,6,'B. Hold weights fixed\n80% + 10% + 10%',mint,9)
arr((63.5,18),(63.5,15));arr((86.5,18),(86.5,15))
box(54,10,19,5,'16 / 25 ranks change',mint,9.5)
box(77,10,19,5,'Possible winners: 12 → 3',mint,9)
text(63.5,6.5,'Measurement + lower tail',8.3);text(86.5,6.5,'Education stays unknown',8.3)
text(75.5,3.4,'Check parameter choices and proxy-error assumptions.',8.3,fontstyle='italic')
arr((48.6,47),(51.4,47));arr((24,32.8),(24,30.2));arr((75.5,32.8),(75.5,30.2));arr((48.6,16),(51.4,16))
save(fig,'01_framework','Model construction and revision. The two experiments in Panel 4 answer different questions; the accessibility proxy does not measure high-school quality or admission eligibility.',['point_rankings.csv','summary.json'],'2024 Team 14995, PDF p.4, Figure 1; 2024 Team 15504, PDF p.13')
# 02: spatial triptych. Authentic polygons, no invented basemap.
cmap=LinearSegmentedColormap.from_list('access',['#eee9dd','#d3d9bf','#94b7a3','#4d8e88','#36566f'])
fig,axs=plt.subplots(1,3,figsize=(9.5,3.65));fig.subplots_adjust(left=.03,right=.98,top=.88,bottom=.21,wspace=.10)
for j,(ax,n) in enumerate(zip(axs,names)):
 fs,p,t,u=grids[n];coords=[np.array(f['geometry']['coordinates'][0]) for f in fs];pts=np.concatenate(coords);origin=pts.mean(axis=0)
 scale=np.array([111.32*np.cos(np.radians(origin[1])),111.32]);polys=[(v-origin)*scale for v in coords];allp=np.concatenate(polys)
 collection=PolyCollection(polys,array=u,cmap=cmap,norm=Normalize(0,1),linewidths=0,rasterized=False);ax.add_collection(collection)
 lo=allp.min(axis=0);hi=allp.max(axis=0);center=(lo+hi)/2;span=max(hi-lo)*1.12
 ax.set(xlim=(center[0]-span/2,center[0]+span/2),ylim=(center[1]-span/2,center[1]+span/2),aspect='equal',xticks=[],yticks=[])
 for sp in ax.spines.values():sp.set_color('#A3A3A3');sp.set_linewidth(.55)
 ax.set_title(f'({chr(97+j)})  {n}',loc='left',fontsize=11,pad=7)
 x0=center[0]-span*.42;y0=center[1]-span*.42;length=2 if span<30 else 10
 ax.plot([x0,x0+length],[y0,y0],color=ink,lw=1.2);ax.plot([x0,x0],[y0-span*.008,y0+span*.008],color=ink,lw=.65);ax.plot([x0+length,x0+length],[y0-span*.008,y0+span*.008],color=ink,lw=.65);ax.text(x0+length/2,y0+span*.025,f'{length} km',ha='center',fontsize=8)
 ax.annotate('N',xy=(.91,.91),xytext=(.91,.77),xycoords='axes fraction',ha='center',fontsize=8,arrowprops=dict(arrowstyle='->',lw=.65))
 ax.text(.5,-.065,r'$\mu$'+f' = {a.loc[n,"mean_utility_lower"]:.3f}     '+r'$L$'+f' = {a.loc[n,"lower_quintile_utility"]:.3f}',transform=ax.transAxes,ha='center',fontsize=9)
cbax=fig.add_axes([.32,.055,.36,.028]);cb=fig.colorbar(collection,cax=cbax,orientation='horizontal',ticks=[0,.25,.5,.75,1]);cb.set_label(r'Learning-facility accessibility, $u=\exp(-t/30)$',fontsize=9,labelpad=3);cb.outline.set_linewidth(.5)
save(fig,'02_spatial_access','Learning-facility accessibility in three illustrative cities. Each populated source grid is coloured by model utility. Blank space is outside retained populated grids, not necessarily water or missing facilities. Panel extents differ; local distance conversion and scale bars are approximate. Cases illustrate a stable leader (Copenhagen), upward revision (Toronto) and downward revision (Dubai), not a representative city sample.',['data/task4_access/{1958,8814,2406}_hexes.zip','learning_access_measures.csv'],'2023 Team 13719, PDF p.15, Figure 5.6: aligned spatial panels; 2025 Team 16738, PDF p.9: shared geographical colour scale')
# 03: small multiples using source's navy / rose / amber lines and narrow serif labels.
fig,axs=plt.subplots(1,3,figsize=(10.1,3.25));fig.subplots_adjust(left=.055,right=.99,bottom=.22,top=.88,wspace=.35)
for n in names:
 fs,p,t,u=grids[n];order=np.argsort(u);v=u[order];F=np.cumsum(p[order])/p.sum()
 axs[0].step(np.r_[0,v],np.r_[0,F],where='post',color=cs[n],label=n,lw=1.35)
axs[0].axhline(.2,color='#777',ls=(0,(3,3)),lw=.6);axs[0].text(.98,.215,'Lowest-access 20%',ha='right',fontsize=8,color='#666')
axs[0].set(xlim=(0,1),ylim=(0,1),xlabel='Accessibility utility, $u$',ylabel='Cumulative population share',xticks=[0,.25,.5,.75,1],yticks=[0,.2,.4,.6,.8,1]);axs[0].legend(loc='upper left',fontsize=8,handlelength=1.6,labelspacing=.25);panel(axs[0],'a','Population-weighted distribution')
xx=np.arange(3);width=.22
for k,(col,label,fc) in enumerate([('mean_utility_lower','Mean','#8898B7'),('lower_quintile_utility','Lowest 20%','#AAC39E'),('q_low','Combined $Q$','#80B7B5')]):
 vals=a.loc[names,col];bars=axs[1].bar(xx+(k-1)*width,vals,width*.87,color=lighten(fc,.35),edgecolor=fc,lw=.55,label=label)
 for rect,val in zip(bars,vals):axs[1].text(rect.get_x()+rect.get_width()/2,val+.014,f'{val:.2f}',ha='center',fontsize=7)
axs[1].set(xticks=xx,xticklabels=names,ylim=(0,1),ylabel='Utility',yticks=[0,.2,.4,.6,.8,1]);axs[1].tick_params(axis='x',labelsize=8);axs[1].legend(loc='upper right',fontsize=7.8,handlelength=1.3,labelspacing=.25);panel(axs[1],'b','Mean and lower-tail aggregation')
lam=np.linspace(0,1,101)
for n in names:
 mu=a.loc[n,'mean_utility_lower'];tail=a.loc[n,'lower_quintile_utility'];axs[2].plot(lam,(1-lam)*mu+lam*tail,color=cs[n],label=n,lw=1.35);axs[2].plot(.3,a.loc[n,'q_low'],'o',ms=3.5,color=cs[n])
axs[2].axvline(.3,color='#888',ls=(0,(3,3)),lw=.6);axs[2].text(.32,.86,r'$\lambda=0.3$',fontsize=9);axs[2].set(xlim=(0,1),ylim=(0,1),xlabel=r'Lower-tail weight, $\lambda$',ylabel=r'$Q=(1-\lambda)\mu+\lambda L$',xticks=[0,.3,.6,1],yticks=[0,.2,.4,.6,.8,1]);panel(axs[2],'c','Effect of the equity preference')
save(fig,'03_access_mechanism','Accessibility distributions and the lower-tail mechanism for three illustrative cities. Distributions are weighted by retained all-age population. Panel (c) varies only the normative lower-tail weight; the curves are not fitted empirical relationships. All plotted statistics were checked against the archived analysis.',['learning_access_measures.csv','three archived spatial ZIPs'],'2023 Team 13719, PDF p.16, Figure 5.7: Times typography, thin boxed axes and navy/rose/amber lines; 2024 Team 15504, PDF p.18, Figure 8: grouped bars with direct values')
# 04: complete 25-city ranking; linked two-panel data figure, more compact than a tall generic slope chart.
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(8.6,6.3),gridspec_kw={'width_ratios':[1.25,1]});fig.subplots_adjust(left=.15,right=.95,top=.90,bottom=.10,wspace=.49)
y=np.arange(25);high={'Copenhagen':navy,'Toronto':gold,'Dubai':rose}
colors=[high.get(n,'#8BB5AA') for n in cities]
ax1.barh(y,rank.V3_score_lower,height=.62,color=colors,edgecolor='white',lw=.3)
for j,s in enumerate(rank.V3_score_lower):ax1.text(s+.8,j,f'{s:.1f}',va='center',fontsize=8)
ax1.set(yticks=y,yticklabels=cities,ylim=(24.7,-.7),xlim=(0,84),xticks=[0,20,40,60,80],xlabel='Revised TOPSIS score');ax1.tick_params(axis='y',length=0);ax1.spines[['top','right']].set_visible(False);panel(ax1,'a','Five-proxy ranking (all 25 cities)')
for j,(_,r) in enumerate(rank.iterrows()):
 color=high.get(r.city,'#9A9A9A');ax2.plot([r.V0_rank_common_sample,r.access_mean_only_rank,r.V3_rank],[j-.19,j,j+.19],color=color,lw=.8,alpha=.9)
 ax2.plot(r.V0_rank_common_sample,j-.19,'o',mfc='white',mec=color,ms=3.4,mew=.75);ax2.plot(r.access_mean_only_rank,j,'s',mfc='white',mec=color,ms=3,mew=.7);ax2.plot(r.V3_rank,j+.19,'o',color=color,ms=3.4)
 if r.city in high:ax2.text(26,j,f'{int(r.V0_rank_common_sample)} → {int(r.access_mean_only_rank)} → {int(r.V3_rank)}',fontsize=8,va='center',color=color)
ax2.set(ylim=(24.7,-.7),yticks=[],xlim=(.3,30.2),xticks=[1,5,10,15,20,25],xlabel='Rank (1 = highest)');ax2.spines[['top','right','left']].set_visible(False);ax2.grid(axis='x',lw=.45,color='#E5E5E5');panel(ax2,'b','Decomposing the rank change')
handles=[Line2D([],[],marker='o',mfc='white',mec='#555',color='none',ms=4,label='Baseline'),Line2D([],[],marker='s',mfc='white',mec='#555',color='none',ms=4,label='+ mean access'),Line2D([],[],marker='o',color='#555',linestyle='none',ms=4,label='+ lower tail')]
ax2.legend(handles=handles,loc='upper center',bbox_to_anchor=(.42,1.02),ncol=1,fontsize=8,handletextpad=.4,labelspacing=.35,borderaxespad=1.2)
# Avoid legend masking rows: place between panel title and plot, outside axes.
ax2.get_legend().remove();fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.73,.995),ncol=3,fontsize=8,columnspacing=.8,handletextpad=.3)
save(fig,'04_city_ranking','Conditional ranking under the five-proxy model, with all 25 cities shown. Panel (b) separates the baseline, the addition of mean learning accessibility, and the lower-tail adjustment; vertical offsets separate the three markers for each city and carry no numerical meaning. Score changes across different models are not improvements in city conditions.',['point_rankings.csv'],'2023 Team 13719, PDF p.22, Figure 6.3: ordered bars with meaningful colour groups; 2025 Team 16739, PDF p.9, Figure 6: horizontal ranking and direct values')
# 05: overlapping nested ranges, full sample + sensitivity. No false CIs.
fig=plt.figure(figsize=(8.7,6.3));gs=fig.add_gridspec(1,2,width_ratios=[1.4,1],left=.15,right=.98,bottom=.10,top=.91,wspace=.40);ax=fig.add_subplot(gs[0]);sub=gs[1].subgridspec(2,1,hspace=.52);bx=fig.add_subplot(sub[0]);cx=fig.add_subplot(sub[1])
for j,n in enumerate(cities):
 r=before.loc[n];s=after.loc[n];ax.plot([r.score_lower,r.score_upper],[j,j],color='#D4D4D4',lw=3.3,solid_capstyle='butt');ax.plot([s.score_lower,s.score_upper],[j,j],color=rose if s.possible_champion else navy,lw=1.45,solid_capstyle='butt')
 if s.possible_champion:ax.plot(s.score_upper,j,'o',ms=3,mfc='white',mec=rose,mew=.8)
ax.set(yticks=y,yticklabels=cities,ylim=(24.7,-.7),xlim=(float(before.score_lower.min())-1,82),xticks=[20,40,60,80],xlabel='Feasible score');ax.tick_params(axis='y',length=0);ax.spines[['right','top']].set_visible(False);panel(ax,'a','Observed access narrows the score bounds')
ax.plot([],[],color='#D4D4D4',lw=3,label='Before');ax.plot([],[],color=navy,lw=1.5,label='After');ax.plot([],[],'o',mfc='white',mec=rose,ms=3,label='Possible champion');ax.legend(loc='lower right',fontsize=8)
vals=[before.possible_champion.sum(),after.possible_champion.sum()];bx.bar([0,1],vals,width=.5,color=[lighten(navy,.6),lighten(rose,.35)],edgecolor=[navy,rose],lw=.6)
for i,v in enumerate(vals):bx.text(i,v+.35,str(v),ha='center',fontsize=11)
bx.set(xticks=[0,1],xticklabels=['Before','After'],ylim=(0,14),yticks=[0,3,6,9,12],ylabel='Possible champions');panel(bx,'b','Same model, additional evidence')
stress=json.loads((R/'proxy_error_stress.json').read_text());xx=[r['assumed_access_utility_error'] for r in stress];nn=[len(r['possible_champions']) for r in stress]
cx.plot(xx,nn,'o-',color=rose,lw=1.3,ms=4,mfc='white',mew=1)
for x,v in zip(xx,nn):cx.annotate(str(v),(x,v),xytext=(0,7),textcoords='offset points',ha='center',fontsize=9)
cx.set(xlim=(-.015,.315),ylim=(0,12),xticks=xx,yticks=[0,3,6,9,12],xlabel=r'Assumed proxy error, $\pm\varepsilon$',ylabel='Possible champions');panel(cx,'c','Sensitivity to proxy error')
save(fig,'05_evidence_uncertainty','Information gain under fixed weights: baseline proxies 80%, learning accessibility 10%, unobserved education 10%. Intervals are feasible bounds, not confidence intervals. The three possible champions after observation are Copenhagen, Dubai and Melbourne. Additional proxy-error widths are stress assumptions, not estimated errors.',['matched_information_rank_bounds.csv','proxy_error_stress.json'],'2023 Team 13719, PDF pp.16 and 22: restrained linework, grouped panels and consistent scales')
# 06: compact, horizontal indicator matrix, a less monotonous alternative to the portrait first version.
z=pd.read_csv(B/'results/task4_real/normalized_indicators.csv').set_index('city').loc[cities];z['Learning access']=a.loc[cities,'q_low']
fig,ax=plt.subplots(figsize=(10.3,3.8));fig.subplots_adjust(left=.11,right=.97,top=.95,bottom=.35)
cm=LinearSegmentedColormap.from_list('muted_matrix',['#FAF7F2','#D9E5DB','#8AB9AD','#476F83'])
im=ax.imshow(z.values.T,cmap=cm,vmin=0,vmax=1,aspect='auto');ax.set(xticks=np.arange(25),xticklabels=cities,yticks=np.arange(5),yticklabels=['Safety','Cleanliness','Housing affordability','Commute','Learning access'])
plt.setp(ax.get_xticklabels(),rotation=55,ha='right',rotation_mode='anchor',fontsize=8);ax.tick_params(length=0,labelsize=8)
for i in range(5):
 for j in range(25):ax.text(j,i,f'{z.iloc[j,i]:.2f}',ha='center',va='center',fontsize=7,color='white' if z.iloc[j,i]>.72 else '#29383D')
ax.set_xticks(np.arange(-.5,25,1),minor=True);ax.set_yticks(np.arange(-.5,5,1),minor=True);ax.grid(which='minor',color='white',lw=.65);ax.tick_params(which='minor',length=0)
for sp in ax.spines.values():sp.set_visible(False)
cbax=fig.add_axes([.37,.045,.32,.025]);cb=fig.colorbar(im,cax=cbax,orientation='horizontal',ticks=[0,.25,.5,.75,1]);cb.set_label('Oriented proxy score / utility (higher is better)',fontsize=9);cb.outline.set_linewidth(.5)
save(fig,'06_indicator_matrix','Five proxy indicators for all 25 cities, ordered by the revised ranking. Columns retain every city; the scale is bounded from zero to one. These are oriented proxy scores, not measurements of student outcomes.',['normalized_indicators.csv','learning_access_measures.csv'],'2025 Team 16739, PDF p.8, Figure 1: annotated cells and explicit colour scale; adapted to a horizontal five-indicator layout')
(H/'figure_manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));(H/'spatial_checks.json').write_text(json.dumps(gridchecks,indent=2))
# View-ready previews use sans labels outside the artwork, never embedded in the actual paper figure.
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
for group,selected in [('overview',[records[0],records[1],records[2]]),('results',records[3:])]:
 widths=1800;heights=[];imgs=[]
 for r in selected:
  im=Image.open(O/(r['name']+'.png')).convert('RGB');im.thumbnail((1720,1020));imgs.append(im);heights.append(im.height+70)
 sheet=Image.new('RGB',(widths,sum(heights)+30),'#F0EFEB');dr=ImageDraw.Draw(sheet);yy=20
 for r,im,h in zip(selected,imgs,heights):
  dr.text((40,yy),r['name'],font=font,fill='#555555');sheet.paste(im,((widths-im.width)//2,yy+35));yy+=h
 sheet.save(H/f'preview_{group}.jpg',quality=94)
doc=fitz.open()
for r in records:
 with fitz.open(O/(r['name']+'.pdf')) as s:doc.insert_pdf(s)
doc.save(H/'redesigned_figures.pdf')
print('Created 6 redesigned figures; verified three spatial aggregates against archived results.')
