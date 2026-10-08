"""Restyle the user's edited V1 deck into the bright Ref5 theme, keeping every text/shape edit."""
import json, re, io, sys
from pptx import Presentation
from pptx.util import Emu
from PIL import Image
SRC, OUT = sys.argv[1], sys.argv[2]
H = open("/home/user/6month/nedp_deck/NEDP_Deck_Ref5_Bright.html").read()
CLS = re.findall(r'<section[^>]*class="slide([^"]*)"', H)
items = json.load(open("/tmp/claude-0/pp5/items.json"))
IMGS = json.load(open("/tmp/claude-0/pp5/imgs.json"))
import base64, copy
from PIL import ImageOps
K = 12192000 / 1280
def img_blob(d):
    b = base64.b64decode(d["src"].split(",", 1)[1]); im = Image.open(io.BytesIO(b))
    im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
    W0, H0 = im.size; c = d["crop"]
    im = im.crop((max(0, round(c[0]*W0)), max(0, round(c[1]*H0)), min(W0, round(c[2]*W0)), min(H0, round(c[3]*H0))))
    if d["inv"]:
        a = im.convert("RGBA").getchannel("A"); im = Image.new("RGBA", im.size, (255, 255, 255, 255)); im.putalpha(a)
    o = io.BytesIO()
    if im.mode == "RGBA": im.save(o, "PNG", optimize=True)
    else: im.save(o, "JPEG", quality=93)
    o.seek(0); return o
def add_imgs(s, k, after_el):
    anchor = after_el
    for d in IMGS[k]:
        pic = s.shapes.add_picture(img_blob(d), Emu(int(d["x"]*K)), Emu(int(d["y"]*K)), Emu(int(d["w"]*K)), Emu(int(d["h"]*K)))
        anchor.addnext(pic._element); anchor = pic._element
def bgjpg(k):
    im = Image.open(f"/tmp/claude-0/pp5/bg{k}.png").convert("RGB"); b = io.BytesIO(); im.save(b, "JPEG", quality=92); return b.getvalue()
htxt = [set(" ".join(r["t"] for it in s for r in it["runs"]).lower().split()) for s in items]

TXT = {"F4F1EE": "1B1B1B", "F0ECE8": "1B1B1B", "EFE9E4": "1B1B1B", "A9A29C": "5E5A55", "A79F98": "5E5A55",
       "6F6963": "9A948D", "FFD3C0": "FF5A1F", "FFB089": "FF7A45", "F5C26B": "E08A00", "F2C14E": "E08A00"}
def lum(h): r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4)); return (0.299*r + 0.587*g + 0.114*b) / 255
def fillmap(h):
    if lum(h) > 0.3: return h
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return "FFF1EA" if r - b > 25 else "FBF7F2"

p = Presentation(SRC)
W, Hh = p.slide_width, p.slide_height
white = io.BytesIO(); Image.new("RGB", (1920, 1080), "white").save(white, "PNG")
NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

def recolor_xml(el, divider=False):
    for c in el.iter(NS + "srgbClr"):
        v = c.get("val").upper(); par = c.getparent()
        tag = par.tag.split("}")[1]
        in_text = any(a.tag.split("}")[1] in ("rPr", "defRPr", "endParaRPr") for a in [par] + list(par.iterancestors())[:2])
        if divider and in_text: c.set("val", "FFFFFF"); continue
        if in_text: c.set("val", TXT.get(v, v))
        elif tag == "solidFill" or tag == "ln" or par.getparent() is not None:
            nv = fillmap(v)
            if any(a.tag.endswith("}ln") for a in par.iterancestors()) and lum(v) < 0.3: nv = "ECE6DE"
            c.set("val", nv)

def cmap(k):
    m = {}
    for it in items[k]:
        for r in it["runs"]:
            w = r["t"].strip().lower()
            if w: m.setdefault(w, r["c"])
    return m
def hexc(c):
    v = [int(float(x)) for x in re.findall(r"[\d.]+", c)[:3]]; return "%02X%02X%02X" % tuple(v)
def noautofit(root):
    for bp in root.iter(NS + "bodyPr"):
        for af in list(bp):
            if af.tag in (NS + "spAutoFit", NS + "normAutofit"): bp.remove(af)

for i, s in enumerate(p.slides):
    pics = [sh for sh in s.shapes if sh.shape_type == 13 and sh.left <= 0 and sh.top <= 0 and sh.width >= W * 0.95]
    words = set(" ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame).lower().split())
    k = max(range(len(htxt)), key=lambda j: len(words & htxt[j]) / (len(words | htxt[j]) or 1))
    score = len(words & htxt[k]) / (len(words | htxt[k]) or 1)
    native = s.slide_layout.name != "Blank" or score < 0.5
    divider = (not native) and "div" in CLS[k]
    if pics and not native:
        rId = pics[0]._element.blipFill.blip.rEmbed
        part = s.part.related_part(rId); part._blob = bgjpg(k)
        add_imgs(s, k, pics[0]._element)
    elif pics:
        part = s.part.related_part(pics[0]._element.blipFill.blip.rEmbed); part._blob = white.getvalue()
    # slide background -> white
    bg = s.background.fill; bg.solid(); 
    from pptx.dml.color import RGBColor; bg.fore_color.rgb = RGBColor(255, 255, 255)
    recolor_xml(s.shapes._spTree, divider)
    noautofit(s.shapes._spTree)
    if not native:
        m = cmap(k)
        from pptx.dml.color import RGBColor as _R
        norm = lambda t: " ".join(t.split()).lower()
        lines = {}
        for it in items[k]:
            lines.setdefault(norm("".join((r["t"].upper() if r.get("up") else r["t"]) for r in it["runs"])), it["runs"])
        for sh in s.shapes:
            if not sh.has_text_frame: continue
            runs = [r for para in sh.text_frame.paragraphs for r in para.runs]
            L = lines.get(norm("".join(r.text for r in runs)))
            for j, r in enumerate(runs):
                c = None
                if L:
                    # colour of the html run that contains this run's first word
                    w = r.text.strip().lower()
                    c = next((x["c"] for x in L if x["t"].strip().lower() == w), None) or L[min(j, len(L) - 1)]["c"]
                else:
                    c = m.get(r.text.strip().lower())
                if c: r.font.color.rgb = _R.from_string(hexc(c))
    # tables: orange header, zebra body
    for sh in s.shapes:
        if sh.has_table:
            for ri, row in enumerate(sh.table.rows):
                for cell in row.cells:
                    cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor.from_string("FF5A1F" if ri == 0 else ("FFFFFF" if ri % 2 else "FBF7F2"))
                    for para in cell.text_frame.paragraphs:
                        for r in para.runs:
                            cur = None
                            try: cur = str(r.font.color.rgb)
                            except Exception: pass
                            if ri == 0: r.font.color.rgb = RGBColor(255, 255, 255)
                            elif cur in (None, "FFFFFF", "1B1B1B", "5E5A55", "9A948D"): r.font.color.rgb = RGBColor.from_string("1B1B1B" if cur in (None, "FFFFFF", "1B1B1B") else cur)
        if sh.has_chart:
            cp = sh.chart.part
            x = cp._element
            recolor_xml(x)
    print(i + 1, "native" if native else f"html#{k+1}{' div' if divider else ''}", round(score, 2))
# chart xml text colours
for part in p.part.package.iter_parts():
    if part.partname.startswith("/ppt/charts/") and part.partname.endswith(".xml") and hasattr(part, "_element"):
        recolor_xml(part._element)
# ---- insert About Me (html slide 3) after the Personal Information divider
import re as _re
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN, MSO_AUTO_SIZE
from pptx.util import Pt
def colr(c): return RGBColor(*[int(float(x)) for x in _re.findall(r"[\d.]+", c)[:3]])
KA = 2
ns = p.slides.add_slide(p.slide_layouts[6] if len(p.slide_layouts) > 6 else p.slide_layouts[-1])
for ph in list(ns.placeholders): ph._element.getparent().remove(ph._element)
bgp = ns.shapes.add_picture(io.BytesIO(bgjpg(KA)), 0, 0, W, Hh)
add_imgs(ns, KA, bgp._element)
for t in items[KA]:
    tb = ns.shapes.add_textbox(Emu(int(t["x"]*K)), Emu(int((t["y"]-t["h"]*0.08)*K)), Emu(int((t["w"]+40)*K)), Emu(int(t["h"]*K)))
    tf = tb.text_frame; tf.word_wrap = False; tf.auto_size = MSO_AUTO_SIZE.NONE; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.TOP
    para = tf.paragraphs[0]; para.alignment = PP_ALIGN.LEFT
    for j, x in enumerate(t["runs"]):
        r = para.add_run(); r.text = (x["t"].upper() if x.get("up") else x["t"]); r.text = r.text.lstrip() if j == 0 else r.text
        r.font.size = Pt(x["fs"]*0.75*0.97); r.font.bold = x["b"]; r.font.name = "Arial"; r.font.color.rgb = colr(x["c"])
lst = p.slides._sldIdLst; el = lst[-1]; lst.remove(el); lst.insert(2, el)
p.save(OUT)
