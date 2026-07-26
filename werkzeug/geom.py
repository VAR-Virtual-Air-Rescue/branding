"""Zerlegt Potrace-Pfade in Subpfade und liefert Flaechen/BBox, damit man
Aussenkontur und Aussparungen getrennt verwenden kann."""
import re, json

TOK = re.compile(r'[MLCZ]|-?\d+(?:\.\d+)?')

def subpaths(d):
    parts, cur = [], []
    for chunk in re.split(r'(?=M)', d):
        if chunk.strip(): parts.append(chunk)
    return parts

def bbox(sp):
    nums = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', sp)]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), min(ys), max(xs), max(ys)

def area(sp):
    x0,y0,x1,y1 = bbox(sp)
    return (x1-x0)*(y1-y0)

if __name__ == "__main__":
    t = json.load(open("traced.json"))
    for lvl in ("fein","mittel","grob","solid"):
        d = t["heli"]["levels"][lvl]["d"]
        sps = subpaths(d)
        print(lvl, "->", len(sps), "Subpfade, Flaechen:", [round(area(s)) for s in sps])
    d = t["var"]["levels"]["mittel"]["d"]
    print("VAR ->", len(subpaths(d)), "Subpfade, Flaechen:", [round(area(s)) for s in subpaths(d)])
