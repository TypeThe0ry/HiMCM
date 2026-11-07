from pathlib import Path
from PIL import Image, ImageDraw
import pandas as pd,json
H=Path(__file__).resolve().parent; A=H.parent/'award_atlas'
df=pd.read_csv(A/'index.csv').fillna('')
choices={13719:[4,8,10,11,12,15,16,17,21,22],13643:[11,12,13,14,15,21],14632:[3,8,12,13,19,22],14995:[4,14,18,21],15504:[6,13,16,18,19],15926:[16,19,20,21,22],16738:[9,10,13,17,20,23,24],16442:[14,16,17],16739:[9,15,19,21,22]}
rows=[]
for team,pages in choices.items():
 for page in pages:
  r=df[(df.team==team)&(df.pdf_page==page)]
  if len(r):rows.append(r.iloc[0].to_dict())
for start in range(0,len(rows),12):
 part=rows[start:start+12];im=Image.new('RGB',(1600,1680),'#eeece7');draw=ImageDraw.Draw(im)
 for i,r in enumerate(part):
  p=Image.open(A/r['image']);p.thumbnail((386,510));x=i%4*400+(400-p.width)//2;y=i//4*560+30;im.paste(p,(x,y));draw.text((i%4*400+10,i//4*560+8),f"{r['year']} / {r['team']} / p.{r['pdf_page']}",fill='black')
 im.save(H/f'survey_{start//12+1:02d}.jpg',quality=93)
(H/'survey_pages.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(len(rows),'pages', (len(rows)+11)//12,'sheets')
