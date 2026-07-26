import numpy as np, potrace, json
from PIL import Image

def mask_gold(im):
    a=np.array(im.convert("RGBA")).astype(int); r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
    return (abs(r-213)<70)&(abs(g-165)<70)&(b<110)&(al>128)

def mask_dark(im):   # Stratos wordmark
    a=np.array(im.convert("RGBA")).astype(int); r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
    return (r<70)&(g<70)&(b<110)&(al>128)

def to_path(path, ox, oy, scale, nd=2):
    f=lambda v: (f"{v:.{nd}f}".rstrip('0').rstrip('.')) or "0"
    T=lambda pt:(f((pt.x-ox)*scale), f((pt.y-oy)*scale))
    out=[];n=0
    for c in path:
        n+=1; sx,sy=T(c.start_point); out.append(f"M{sx} {sy}")
        for seg in c:
            if seg.is_corner:
                cx,cy=T(seg.c); ex,ey=T(seg.end_point); out.append(f"L{cx} {cy}L{ex} {ey}")
            else:
                a1,b1=T(seg.c1); a2,b2=T(seg.c2); ex,ey=T(seg.end_point)
                out.append(f"C{a1} {b1} {a2} {b2} {ex} {ey}")
        out.append("Z")
    return "".join(out), n

def run(src, maskfn, levels, target_w, name):
    im=Image.open(src); m=maskfn(im)
    ys,xs=np.where(m); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    sc=target_w/(x1-x0+1)
    res={"bbox":[int(x0),int(y0),int(x1),int(y1)],
         "w":round((x1-x0+1)*sc,2),"h":round((y1-y0+1)*sc,2),"levels":{}}
    for lab,(am,ot,td) in levels.items():
        p=potrace.Bitmap(~m).trace(turdsize=td, alphamax=am, opticurve=True, opttolerance=ot)
        d,n=to_path(p,x0,y0,sc)
        res["levels"][lab]={"d":d,"contours":n,"chars":len(d)}
        print(f"  {name}/{lab}: {n} Konturen, {len(d)} Zeichen")
    return res

out={}
out["heli"]=run("extract__Image2.png", mask_gold,
    {"fein":(1.0,0.2,30),"mittel":(1.3,2.0,600),"grob":(1.34,6.0,4000),"solid":(1.34,10.0,80000)},
    1000,"heli")
out["var"]=run("extract__Image4.png", mask_dark,
    {"fein":(1.0,0.2,30),"mittel":(1.2,1.0,200)},
    1000,"var")
json.dump(out, open("traced.json","w"))
print("\nheli w/h:", out["heli"]["w"], out["heli"]["h"])
print("var  w/h:", out["var"]["w"], out["var"]["h"])
