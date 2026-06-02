import os, glob
import win32com.client
HERE = os.path.dirname(os.path.abspath(__file__))
PPTX = os.path.join(HERE, "Task-Management-System.pptx")
OUT = os.path.join(HERE, "_render"); os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, "*.png")): os.remove(f)
app = win32com.client.Dispatch("PowerPoint.Application")
try: app.Visible = True
except Exception: pass
pres = app.Presentations.Open(PPTX, ReadOnly=True, WithWindow=False)
n = pres.Slides.Count
for i in range(1, n + 1):
    pres.Slides(i).Export(os.path.join(OUT, f"slide-{i:02d}.png"), "PNG", 1920, 1080)
PDF = os.path.splitext(PPTX)[0] + ".pdf"
try: pres.SaveAs(PDF, 32); print("PDF ->", PDF)
except Exception as e: print("PDF failed:", e)
pres.Close(); app.Quit()
from PIL import Image
files = sorted(glob.glob(os.path.join(OUT, "slide-*.png")))
cols = 4; tw = 820; th = int(tw*9/16); gap = 14; pad = 18
rows = (len(files)+cols-1)//cols
sheet = Image.new("RGB", (pad*2+cols*tw+(cols-1)*gap, pad*2+rows*th+(rows-1)*gap), (228, 228, 228))
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
    r, c = divmod(i, cols); sheet.paste(im, (pad+c*(tw+gap), pad+r*(th+gap)))
sheet.save(os.path.join(OUT, "_contact.jpg"), quality=85)
print("DONE", n, "slides")
