from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
H=Path(__file__).resolve().parent;O=H/'figures';O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'Times New Roman','font.size':10,'axes.linewidth':.6,'pdf.fonttype':42,'svg.fonttype':'none','savefig.dpi':300})
df=pd.read_csv(H/'candidate_city_locations.csv');assert len(df)==25
pc=ccrs.PlateCarree();proj=ccrs.Robinson(central_longitude=10)
land='#EEEDE7';sea='#F4F7F8';line='#A9B2B6';navy='#304E61';accent='#AD604E'
fig=plt.figure(figsize=(12.8,6.8));ax=fig.add_axes([.025,.07,.95,.86],projection=proj);ax.set_global();ax.set_extent([-178,179,-58,80],crs=pc);ax.set_facecolor(sea)
reader=Reader(H/'basemap_cache/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
ax.add_geometries(list(reader.geometries()),pc,facecolor=land,edgecolor=line,linewidth=.35,zorder=1)
ax.gridlines(crs=pc,xlocs=[-120,-60,0,60,120],ylocs=[-30,0,30,60],linewidth=.4,color='#BCC7CC',alpha=.6,linestyle=(0,(2,4)),zorder=0)
ax.spines['geo'].set_linewidth(.6);ax.spines['geo'].set_edgecolor('#AAB5B9')
focus={'Copenhagen','Toronto','Dubai','Shanghai'};europe={'Copenhagen','London','Barcelona','Warsaw','Athens','Istanbul'}
offsets={'Toronto':(-9,17),'Phoenix':(-13,5),'New York':(13,-3),'Mexico City':(-9,-17),'Bogota':(9,-5),'Sao Paulo':(10,-3),'Santiago':(8,-9),'Nairobi':(11,1),'Lagos':(-12,6),'Cape Town':(12,-8),'Dubai':(-14,10),'Mumbai':(-17,-14),'Delhi':(-10,17),'Dhaka':(13,4),'Tokyo':(13,5),'Shanghai':(11,-10),'Singapore':(-15,-17),'Jakarta':(13,-17),'Melbourne':(12,-10)}
locations=[]
for _,r in df.iterrows():
 col=accent if r.city in focus else navy
 ax.scatter(r.longitude,r.latitude,transform=pc,s=28 if r.city in focus else 20,facecolor=col,edgecolor='white',lw=.75,zorder=4)
 if r.city not in europe:
  x,y=proj.transform_point(r.longitude,r.latitude,pc);dx,dy=offsets[r.city]
  t=ax.annotate(r.city,(x,y),xytext=(dx,dy),textcoords='offset points',ha='left' if dx>0 else 'right',va='center',fontsize=10.5,color='#283D49',arrowprops=dict(arrowstyle='-',color='#7A8E99',lw=.55,shrinkA=2,shrinkB=4),zorder=5)
  t.set_path_effects([pe.withStroke(linewidth=2.6,foreground='white',alpha=.95)])
 locations.append({'city':r.city,'longitude':r.longitude,'latitude':r.latitude,'label_panel':'Europe inset' if r.city in europe else 'world','case_study':r.city in focus})
# Show the exact geographical extent enlarged by the inset.
boxlon=[-12,36,36,-12,-12];boxlat=[33,33,61,61,33]
ax.plot(boxlon,boxlat,transform=pc,color='#768D99',lw=.6,linestyle=(0,(3,2)),zorder=3)
# Europe enlarges the crowded region, not the point symbols.
ei=fig.add_axes([.008,.083,.205,.303],projection=ccrs.LambertConformal(central_longitude=12,central_latitude=47,standard_parallels=(35,60)));ei.set_extent([-12,36,33,61],crs=pc);ei.set_facecolor(sea)
ei.add_geometries(list(Reader(H/'basemap_cache/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp').geometries()),pc,facecolor=land,edgecolor=line,linewidth=.35,zorder=1)
ei.spines['geo'].set_edgecolor('#8FA0A8');ei.spines['geo'].set_linewidth(.65)
eoff={'London':(-8,4),'Copenhagen':(-8,9),'Warsaw':(8,4),'Barcelona':(-7,-8),'Athens':(-7,-9),'Istanbul':(10,1)}
for _,r in df[df.city.isin(europe)].iterrows():
 col=accent if r.city in focus else navy;ei.scatter(r.longitude,r.latitude,transform=pc,s=22,facecolor=col,edgecolor='white',lw=.65,zorder=3)
 x,y=ei.projection.transform_point(r.longitude,r.latitude,pc);dx,dy=eoff[r.city];t=ei.annotate(r.city,(x,y),xytext=(dx,dy),textcoords='offset points',ha='left' if dx>0 else 'right',va='center',fontsize=11,color='#283D49',zorder=4);t.set_path_effects([pe.withStroke(linewidth=2,foreground='white')])
ei.text(.025,.96,'Europe & Istanbul',transform=ei.transAxes,fontsize=11,va='top',color='#3B515F',bbox=dict(facecolor='white',edgecolor='none',alpha=.8,pad=1))
fig.text(.04,.975,'Geographical distribution of the 25 candidate cities',fontsize=16,fontweight='normal',color='#273B47')
fig.text(.04,.942,'Study locations from the archived city index',fontsize=11,fontstyle='italic',color='#667981')
handles=[Line2D([],[],marker='o',ms=5,color='none',mfc=navy,mec='white',label='Candidate city'),Line2D([],[],marker='o',ms=6,color='none',mfc=accent,mec='white',label='City accessibility case study')]
fig.legend(handles=handles,loc='upper left',bbox_to_anchor=(.04,.875),fontsize=11,frameon=False,handletextpad=.4,labelspacing=.65)
fig.text(.32,.05,'25 cities  ·  all candidates shown  ·  Europe enlarged for legibility',fontsize=11,color='#52656E')
fig.text(.98,.025,'Made with Natural Earth  |  Robinson projection  |  Urban-area reference locations',ha='right',fontsize=11,color='#65757C')
for ext in ['png','pdf','svg']:fig.savefig(O/f'01_global_candidates.{ext}',bbox_inches='tight',pad_inches=.08,facecolor='white')
plt.close(fig);(H/'global_map_audit.json').write_text(json.dumps({'count':len(locations),'locations':locations,'coordinates':'candidate_city_locations.csv','basemap':'Natural Earth 110m; Europe inset 50m','note':'Source urban-area locator coordinates; not independently surveyed municipal centres'},indent=2))
print('Global map exported; 25 candidate markers and 25 city labels (19 world + 6 inset).')
