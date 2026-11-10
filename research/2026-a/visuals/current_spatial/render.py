from build import *
from matplotlib.patches import Patch
from matplotlib import cm
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'svg.fonttype':'none','savefig.facecolor':'white'})
colors=['#dcece7','#75b7a9','#338c82','#d8ae61','#a65c3d']; cmap=LinearSegmentedColormap.from_list('time',colors); norm=Normalize(0,150)
fig=plt.figure(figsize=(6.5,6.4)); fig.text(.05,.975,'Walking time across retained city grids',fontsize=13,weight='bold',color='#1b3444',va='top');fig.text(.05,.925,'Residents in grids averaging ≤30 min to 20 Learning POIs',fontsize=9,color='#455b63')
positions={'Singapore':([.05,.60,.42,.25],[.03,.245,.45,.30]),'Zurich':([.53,.60,.42,.25],[.52,.245,.45,.30])}
for city in ['Singapore','Zurich']:
 d=cities[city];bb=d['bounds'];polys=d['polys'];vals=d['vals'];good=d['good'];rec=next(r for r in records if r['city']==city); ax=fig.add_axes(positions[city][0]);ax.set_aspect('equal');ax.set_xlim(bb[0],bb[2]);ax.set_ylim(bb[1],bb[3]);ax.set_xticks([]);ax.set_yticks([])
 ax.set_facecolor('#f0f3f1')
 if city=='Zurich': ax.imshow(Image.open(P/'imagery/zurich_2024-06-27.png'),extent=[bb[0],bb[2],bb[1],bb[3]],origin='upper',interpolation='none')
 pc=PolyCollection([p for p,g in zip(polys,good) if g],array=vals[good],cmap=cmap,norm=norm,edgecolors='none',alpha=.82);ax.add_collection(pc)
 for s in ax.spines.values():s.set_color('#b6c4c2');s.set_linewidth(.5)
 lat=1.35 if city=='Singapore' else 47.38;km=5 if city=='Singapore' else 2; length=km*1000/math.cos(math.radians(lat));xx=bb[0]+.06*(bb[2]-bb[0]);yy=bb[1]+.10*(bb[3]-bb[1]);ax.plot([xx,xx+length],[yy,yy],lw=2.5,color='#182f3d');ax.text(xx,yy+.04*(bb[3]-bb[1]),f'{km} km',fontsize=9,color='#182f3d',bbox={'fc':'white','ec':'none','alpha':.85,'pad':1})
 ax.set_title(city+'  ·  '+f"{100*rec['within_30_share_of_valid']:.2f}%",loc='left',fontsize=11,fontweight='bold',color='#1b3444',pad=6)
 ax3=fig.add_axes(positions[city][1],projection='3d');dx=bb[2]-bb[0];dy=bb[3]-bb[1]; verts=[];faces=[]
 # Every populated valid cell is a quantitative extrusion. Coordinates normalized by the same horizontal scale.
 for poly,t,g in zip(polys,vals,good):
  if not g:continue
  pp=[((x-bb[0])/max(dx,dy),(y-bb[1])/max(dx,dy)) for x,y in poly[:-1]];top=[(x,y,t) for x,y in pp];verts.append(top);faces.append(cmap(norm(t)))
  for a,b in zip(pp,pp[1:]+pp[:1]):verts.append([(a[0],a[1],0),(b[0],b[1],0),(b[0],b[1],t),(a[0],a[1],t)]);c=cmap(norm(t));faces.append((c[0]*.78,c[1]*.78,c[2]*.78,1))
 coll=Poly3DCollection(verts,facecolors=faces,edgecolors='none',rasterized=True);ax3.add_collection3d(coll);ax3.set_xlim(0,dx/max(dx,dy));ax3.set_ylim(0,dy/max(dx,dy));ax3.set_zlim(0,150);ax3.set_box_aspect((dx/max(dx,dy),dy/max(dx,dy),.75));ax3.view_init(elev=25,azim=-68);ax3.set_xticks([]);ax3.set_yticks([]);ax3.set_zticks([0,75,150]);ax3.tick_params(axis='z',labelsize=9,pad=0);ax3.set_zlabel('min',fontsize=9,labelpad=-2);ax3.xaxis.pane.fill=False;ax3.yaxis.pane.fill=False;ax3.zaxis.pane.fill=False;ax3.grid(False)
fig.text(.05,.545,'Height = walking time (minutes); common 0–150 scale',fontsize=9,color='#1b3444',weight='bold')
cax=fig.add_axes([.15,.19,.7,.018]); cb=fig.colorbar(cm.ScalarMappable(norm=norm,cmap=cmap),cax=cax,orientation='horizontal',ticks=[0,30,60,90,120,150]);cb.ax.tick_params(labelsize=9,length=2);cb.outline.set_visible(False)
fig.text(.05,.095,'NASA HLS / GIBS · Zurich request 27 Jun 2024 (clouds present)',fontsize=9,color='#455b63');fig.text(.05,.06,'Grids: Bruno et al., snapshot 7 Nov 2026',fontsize=9,color='#455b63');fig.text(.05,.025,'Population: retained residents, not students',fontsize=9,color='#455b63')
for ext in ['png','pdf','svg']:fig.savefig(P/f'city_walktime.{ext}',dpi=300)
