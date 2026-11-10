"""Render owned V201 pages/contact sheets for manual layout review."""
from pathlib import Path
import argparse,hashlib,json,subprocess
from PIL import Image,ImageOps,ImageDraw

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--pdf',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
 assert not a.output_dir.exists() or not any(a.output_dir.iterdir()),'Use a new/empty output directory'
 a.output_dir.mkdir(parents=True,exist_ok=True)
 subprocess.run(['pdftoppm','-r','96','-png',str(a.pdf),str(a.output_dir/'page')],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 pages=sorted(a.output_dir.glob('page-*.png'))
 for start in range(0,len(pages),9):
  selected=pages[start:start+9];sheet=Image.new('RGB',(1020,1425),'#d9dce2');draw=ImageDraw.Draw(sheet)
  for i,path in enumerate(selected):
   with Image.open(path) as source:thumb=ImageOps.contain(source,(324,430))
   x=12+(i%3)*336;y=25+(i//3)*470
   sheet.paste(thumb,(x,y));draw.text((x,y-17),f'Page {start+i+1}',fill='black')
  sheet.save(a.output_dir/f'contact-{start//9+1}.png')
 report=dict(pdf_sha256=hashlib.sha256(a.pdf.read_bytes()).hexdigest(),pages=len(pages),render_dpi=96,contact_sheets=[str(p) for p in sorted(a.output_dir.glob('contact-*.png'))],manual_review_completed=False)
 (a.output_dir/'render.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
