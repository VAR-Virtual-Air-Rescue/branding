# Vereinfachte Heli-Silhouette fuer kleine Groessen: Fenster schliessen, Rotor verdicken.
import numpy as np, potrace, json
from PIL import Image, ImageFilter
from trace_lib import to_path

im=Image.open("extract__Image2.png").convert("RGBA")
a=np.array(im).astype(int); r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
gold=((abs(r-213)<70)&(abs(g-165)<70)&(b<110)&(al>128))
mi=Image.fromarray((gold*255).astype('uint8'))

out={}
# 1) Fenster zu + Rotor dicker: dilate 9 -> erode 5  (netto +2 px Rotor, Fenster geschlossen)
step = mi.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.MinFilter(11))
m2 = np.array(step)>127
p=potrace.Bitmap(m2).trace(turdsize=3000, alphamax=1.34, opticurve=True, opttolerance=4.0)
ys,xs=np.where(m2); sc=1000/(xs.max()-xs.min()+1)
d,n=to_path(p,xs.min(),ys.min(),sc)
out["kompakt"]={"d":d,"contours":n,"w":1000.0,"h":round((ys.max()-ys.min()+1)*sc,2)}
print("kompakt:",n,"Konturen,",len(d),"Zeichen, h=",out["kompakt"]["h"])

# 2) Extrem reduziert fuer 16px: nur Rumpf ohne Rotorspitzen -> staerker schliessen
step2 = mi.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.MinFilter(21))
m3=np.array(step2)>127
p=potrace.Bitmap(m3).trace(turdsize=8000, alphamax=1.34, opticurve=True, opttolerance=8.0)
ys,xs=np.where(m3); sc=1000/(xs.max()-xs.min()+1)
d,n=to_path(p,xs.min(),ys.min(),sc)
out["micro"]={"d":d,"contours":n,"w":1000.0,"h":round((ys.max()-ys.min()+1)*sc,2)}
print("micro:",n,"Konturen,",len(d),"Zeichen, h=",out["micro"]["h"])
json.dump(out, open("traced_simple.json","w"))
