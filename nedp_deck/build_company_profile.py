"""Builds the Company Profile slide (Ref4 Dark Glow style) with embedded logos and unit photos."""
import base64, io
from PIL import Image, ImageChops

def b64(path, maxw=None, trim=False, fmt="JPEG", q=92, edge=False):
    maxw = maxw and maxw * 2
    src = Image.open(path)
    if src.mode in ("RGBA", "LA", "P"):
        src = src.convert("RGBA"); white = Image.new("RGBA", src.size, (255, 255, 255, 255))
        src = Image.alpha_composite(white, src)
    im = src.convert("RGB")
    if trim:
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b_ = px[x, y]
                if min(r, g, b_) > 196 and max(r, g, b_) - min(r, g, b_) < 18:
                    px[x, y] = (255, 255, 255)
        bg = Image.new("RGB", im.size, (255, 255, 255))
        mask = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 60 else 0)
        e = max(3, im.width // 40) if edge else 0
        from PIL import ImageDraw
        d = ImageDraw.Draw(mask)
        for r in [(0, 0, im.width, e), (0, im.height - e, im.width, im.height), (0, 0, e, im.height), (im.width - e, 0, im.width, im.height)]:
            d.rectangle(r, fill=0)
        box = mask.getbbox()
        if box:
            p = 6; box = (max(0, box[0] - p), max(0, box[1] - p), min(im.width, box[2] + p), min(im.height, box[3] + p))
        if box:
            im = im.crop(box)
    if maxw and im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, fmt, quality=q) if fmt == "JPEG" else im.save(buf, fmt)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()

L = "assets/logos/"; U = "assets/units/"
EDGE = {"utpe", "patria"}  # source images with stray corner marks / frame lines
logo = {k: b64(L + f, 420, trim=True, fmt="PNG", edge=k in EDGE) for k, f in {
    "astra": "astra_international.png", "ut": "united_tractors.png", "utpe": "utpe.png",
    "triatra": "triatra.webp", "pml": "pml.png", "pmp": "pmp.png", "patria": "patria.png", "ultra": "ultra.png"}.items()}
ph = {k: b64(U + f, w) for k, f, w in [("hero", "unit1_hero_dumptruck.webp", 1400), ("u2", "unit2_trailer.png", 390),
      ("u3", "unit3_dumpbody.png", 390), ("u4", "unit4_watertruck.png", 390), ("u5", "unit5_servicetruck.png", 390)]}

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Profile</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0B0B0B;--or:#FF5A1F;--tx:#F4F1EE;--tx2:#A9A29C;--mut:#6F6963;--line:rgba(255,255,255,.09);
 --sans:"Neue Haas Grotesk Text Pro","Inter",system-ui,sans-serif}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%;overflow:hidden;background:linear-gradient(180deg,#121212,#4a1606);font-family:var(--sans);color:var(--tx)}}
#stage{{position:fixed;inset:0}}
.slide{{position:absolute;left:50%;top:50%;width:1280px;height:720px;transform:translate(-50%,-50%);transform-origin:center;
 background:var(--bg);border-radius:22px;overflow:hidden}}
/* wide orange silhouette */
.glow{{position:absolute;inset:0;pointer-events:none;
 background:
  radial-gradient(120% 75% at 50% 118%,rgba(255,106,43,.55) 0%,rgba(210,56,15,.38) 30%,rgba(90,18,5,.22) 55%,transparent 75%),
  radial-gradient(60% 55% at 100% 0%,rgba(255,90,31,.14),transparent 70%),
  radial-gradient(50% 50% at 0% 40%,rgba(255,90,31,.08),transparent 70%)}}
.bars{{position:absolute;left:0;right:0;bottom:0;height:62%;pointer-events:none;
 background:repeating-linear-gradient(90deg,transparent 0 70px,rgba(255,140,90,.07) 70px 110px,transparent 110px 160px);
 -webkit-mask:linear-gradient(180deg,transparent,#000 75%);mask:linear-gradient(180deg,transparent,#000 75%)}}
.in{{position:absolute;inset:0;padding:30px 44px}}
.top{{display:flex;justify-content:space-between;font:600 10px var(--sans);letter-spacing:.14em;color:var(--mut)}}
.top .tag{{color:var(--or)}}
.kick{{margin-top:24px;font:500 10px var(--sans);letter-spacing:.14em;color:var(--or)}}
h1{{margin-top:6px;font-weight:500;font-size:28px;line-height:1.15;letter-spacing:-.02em;max-width:1100px;
 background:linear-gradient(90deg,#fff,#9b9590);-webkit-background-clip:text;background-clip:text;color:transparent}}
.grid{{position:absolute;left:44px;right:44px;top:132px;bottom:46px;display:grid;grid-template-columns:1.08fr 1fr;gap:26px}}
.lbl{{font:600 9.5px var(--sans);letter-spacing:.16em;color:var(--mut);margin-bottom:8px}}
.card{{background:linear-gradient(180deg,rgba(28,28,28,.92),rgba(14,14,14,.92));border:1px solid var(--line);border-radius:14px}}
.row{{display:flex;align-items:center;gap:14px;padding:7px 10px;height:68px}}
.chip{{background:#fff;border-radius:9px;height:50px;width:168px;display:flex;align-items:center;justify-content:center;padding:6px 10px;flex:none;overflow:hidden}}
.chip img{{max-width:100%;max-height:100%;width:auto;height:auto;display:block}}
.row .t{{font-size:12px;color:var(--tx2);line-height:1.35}}
.row .t b{{display:block;color:var(--tx);font-size:13px;font-weight:600}}
.vl{{width:2px;height:12px;background:rgba(255,255,255,.18);margin-left:84px}}
.kids{{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:10px;border-top:2px solid rgba(255,255,255,.18);padding-top:10px;margin-top:0}}
.kid{{padding:12px 10px;text-align:center;position:relative}}
.kid .chip{{width:100%;height:58px;margin-bottom:8px}}
.kid .t{{font-size:11px;color:var(--tx2);line-height:1.3}}
.me{{border:1.5px solid var(--or);background:linear-gradient(180deg,rgba(255,90,31,.20),rgba(30,12,6,.9));box-shadow:0 0 30px rgba(255,90,31,.35)}}
.me .t{{color:#FFD3C0}}
.badge{{position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:var(--or);color:#fff;font:700 8.5px var(--sans);
 letter-spacing:.14em;padding:3px 9px;border-radius:999px;white-space:nowrap}}
.brands{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}}
.brand{{display:flex;align-items:center;gap:12px;padding:8px 10px}}
.brand .chip{{width:140px;height:46px}}
.brand .t{{font-size:11px;color:var(--tx2);line-height:1.3}}.brand .t b{{color:var(--tx);display:block;font-size:12px}}
.photos{{display:grid;grid-template-rows:1.35fr 1fr;gap:10px;min-height:0}}
.ph{{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);min-height:0}}
.ph img{{width:100%;height:100%;object-fit:cover;display:block}}
.ph::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(0,0,0,.75))}}
.ph span{{position:absolute;left:12px;bottom:9px;z-index:1;font:600 10px var(--sans);letter-spacing:.08em}}
.ph.hero span{{font-size:12px}}
.small{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;min-height:0}}
.foot{{position:absolute;left:44px;right:44px;bottom:16px;display:flex;justify-content:space-between;font:400 10px var(--sans);
 letter-spacing:.1em;color:var(--mut);text-transform:uppercase}}.foot b{{color:var(--or)}}
</style></head><body><div id="stage"><section class="slide" id="s">
<div class="glow"></div><div class="bars"></div>
<div class="in">
 <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span>SEC/01 — COMPANY</span><span style="color:var(--tx)">TRIATRA</span></div>
 <div class="kick">COMPANY PROFILE</div>
 <h1>UTPE Builds It, Triatra Sells It — Backed by the Astra Group</h1>
</div>
<div class="grid">
 <div>
  <div class="lbl">COMPANY STRUCTURE</div>
  <div class="card row"><div class="chip"><img src="{logo['astra']}" alt="Astra International"></div><div class="t"><b>Astra International</b>Astra Heavy Equipment, Mining, Construction, and Energy</div></div>
  <div class="vl"></div>
  <div class="card row"><div class="chip"><img src="{logo['ut']}" alt="United Tractors"></div><div class="t"><b>United Tractors</b>Construction Machinery</div></div>
  <div class="vl"></div>
  <div class="card row"><div class="chip"><img src="{logo['utpe']}" alt="UTPE"></div><div class="t"><b>UTPE</b>Astra Heavy Equipment, Mining, Construction, and Energy</div></div>
  <div class="vl"></div>
  <div class="kids">
   <div class="card kid me"><span class="badge">MY COMPANY</span><div class="chip"><img src="{logo['triatra']}" alt="Triatra"></div><div class="t">Distributorship and Trading</div></div>
   <div class="card kid"><div class="chip"><img src="{logo['pml']}" alt="PML"></div><div class="t">Logistic and Energy Provider</div></div>
   <div class="card kid"><div class="chip"><img src="{logo['pmp']}" alt="PMP"></div><div class="t">Ship Building and Maintenance</div></div>
  </div>
  <div class="brands">
   <div class="card brand"><div class="chip"><img src="{logo['patria']}" alt="Patria"></div><div class="t"><b>Unit Business</b>Patria units sold by Triatra</div></div>
   <div class="card brand"><div class="chip"><img src="{logo['ultra']}" alt="Ultra"></div><div class="t"><b>Parts Business</b>Parts for Triatra &amp; UTPE</div></div>
  </div>
 </div>
 <div class="photos">
  <div class="ph hero"><img src="{ph['hero']}" alt="Patria Xpro dump vessel"><span>PATRIA XPRO DUMP VESSEL</span></div>
  <div class="small">
   <div class="ph"><img src="{ph['u2']}" alt=""><span>SIDE DUMP TRAILER</span></div>
   <div class="ph"><img src="{ph['u3']}" alt=""><span>DUMP TRUCK BODY</span></div>
   <div class="ph"><img src="{ph['u4']}" alt=""><span>WATER TRUCK</span></div>
   <div class="ph"><img src="{ph['u5']}" alt=""><span>SERVICE TRUCK</span></div>
  </div>
 </div>
</div>
<div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>03</b> / 15</span></div>
</section></div>
<script>
const s=document.getElementById('s');
function fit(){{const k=Math.min(innerWidth/1280,innerHeight/720);s.style.transform='translate(-50%,-50%) scale('+k+')'}}
addEventListener('resize',fit);fit();
</script></body></html>"""
open("NEDP_CompanyProfile_Ref4.html", "w").write(html)
print(len(html) // 1024, "KB")
