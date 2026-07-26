def to_path(path, ox, oy, scale, nd=2):
    f=lambda v:(f"{v:.{nd}f}".rstrip('0').rstrip('.')) or "0"
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
