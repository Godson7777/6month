"""Section 01 (Intro, Company Profile, Business Line & Industries) in Ref4 Dark Glow style, assets embedded."""
import base64, io, re

src = open("build_company_profile.py").read()
exec(src.split("L = ")[0])  # reuse b64() helper

def png(path, maxw):
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

A = "assets/"
logo = {k: b64(A + "logos/" + f, 420, trim=True, fmt="PNG", edge=k in {"utpe", "patria"}) for k, f in {
    "astra": "astra_international.png", "ut": "united_tractors.png", "utpe": "utpe.png", "triatra": "triatra.webp",
    "pml": "pml.png", "pmp": "pmp.png", "patria": "patria.png", "ultra": "ultra.png"}.items()}
tri = png(A + "cutout/triatra_logo.png", 300)
units = [png(A + f"cutout/u{i}.png", 700) for i in range(1, 6)]
ind = [b64(A + "industries/" + f, 900) for f in ["01_coal_mining.webp", "02_construction.png",
       "03_agro_forestry_PLACEHOLDER.png", "04_maritime_PLACEHOLDER.png"]]

CSS = """
:root{--bg:#0B0B0B;--or:#FF5A1F;--tx:#F4F1EE;--tx2:#A9A29C;--mut:#6F6963;--line:rgba(255,255,255,.09);
 --sans:"Neue Haas Grotesk Text Pro","Inter",system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:linear-gradient(180deg,#121212,#4a1606);font-family:var(--sans);color:var(--tx)}
body{padding:16px;display:flex;flex-direction:column;gap:16px}
/* No-JS default: every slide stacked, scaled by its SVG viewBox */
.frame{display:block;width:100%;height:auto}
.slide{position:relative;width:1280px;height:720px;background:var(--bg);border-radius:22px;overflow:hidden}
/* Presenter mode (JS on): one slide at a time, fit to window */
html.present,html.present body{height:100%;overflow:hidden}
html.present body{padding:0;display:grid;place-items:center}
html.present .frame{display:none;width:min(100vw,calc(100vh*16/9));height:auto}
html.present .frame.on{display:block}
.glow{position:absolute;inset:0;pointer-events:none;background:
 radial-gradient(120% 75% at 50% 118%,rgba(255,106,43,.55) 0%,rgba(210,56,15,.38) 30%,rgba(90,18,5,.22) 55%,transparent 75%),
 radial-gradient(60% 55% at 100% 0%,rgba(255,90,31,.14),transparent 70%),
 radial-gradient(50% 50% at 0% 40%,rgba(255,90,31,.08),transparent 70%)}
.bars{position:absolute;left:0;right:0;bottom:0;height:62%;pointer-events:none;
 background:repeating-linear-gradient(90deg,transparent 0 70px,rgba(255,140,90,.07) 70px 110px,transparent 110px 160px);
 -webkit-mask:linear-gradient(180deg,transparent,#000 75%);mask:linear-gradient(180deg,transparent,#000 75%)}
.hdr{position:absolute;left:44px;right:44px;top:28px;display:flex;justify-content:space-between;align-items:center;
 font:600 10px var(--sans);letter-spacing:.14em;color:var(--or)}
.hdr img{height:30px;display:block}
.kick{position:absolute;left:44px;top:84px;font:500 10px var(--sans);letter-spacing:.14em;color:var(--or)}
h1{position:absolute;left:44px;top:100px;font-weight:500;font-size:34px;letter-spacing:-.02em;
 background:linear-gradient(90deg,#fff,#9b9590);-webkit-background-clip:text;background-clip:text;color:transparent}
.foot{position:absolute;left:44px;right:44px;bottom:16px;display:flex;justify-content:space-between;font:400 10px var(--sans);
 letter-spacing:.1em;color:var(--mut);text-transform:uppercase}.foot b{color:var(--or)}
.lbl{font:600 9.5px var(--sans);letter-spacing:.16em;color:var(--mut);margin-bottom:10px}
.card{background:linear-gradient(180deg,rgba(28,28,28,.92),rgba(14,14,14,.92));border:1px solid var(--line);border-radius:14px}
.chip{background:#fff;border-radius:9px;display:flex;align-items:center;justify-content:center;padding:6px 10px;flex:none;overflow:hidden}
.chip img{max-width:100%;max-height:100%;width:auto;height:auto;display:block}
/* intro */
.intro .sec{position:absolute;left:0;right:0;top:92px;text-align:center;font:600 12px var(--sans);letter-spacing:.32em;color:var(--or)}
.intro h2{position:absolute;left:0;right:0;top:112px;text-align:center;font-weight:600;font-size:76px;letter-spacing:-.03em;
 background:linear-gradient(180deg,#fff 30%,#a7a19b);-webkit-background-clip:text;background-clip:text;color:transparent}
.intro .sub{position:absolute;left:0;right:0;top:214px;text-align:center;font-size:15px;color:var(--tx2)}
.lineup{position:absolute;left:30px;right:30px;top:290px;height:230px;display:flex;align-items:flex-end;justify-content:center;gap:26px}
.lineup .u{display:flex;flex-direction:column;align-items:center}
.lineup img{display:block;height:var(--h);width:auto;filter:drop-shadow(0 18px 18px rgba(0,0,0,.65))}
.lineup span{margin-top:12px;font:600 9px var(--sans);letter-spacing:.14em;color:var(--tx2);white-space:nowrap}
.road{position:absolute;left:0;right:0;top:500px;height:2px;background:linear-gradient(90deg,transparent,rgba(255,140,90,.55),transparent)}
.brandrow{position:absolute;left:0;right:0;bottom:56px;display:flex;justify-content:center;gap:14px}
.brandrow .chip{width:150px;height:46px}
.agenda{position:absolute;left:0;right:0;bottom:118px;text-align:center;font:500 11px var(--sans);letter-spacing:.2em;color:var(--tx2)}
.agenda b{color:var(--or);font-weight:600}
/* structure */
.tree{position:absolute;left:50%;transform:translateX(-50%);top:178px;width:900px}
.row{display:flex;align-items:center;gap:18px;padding:8px 12px;height:80px;width:640px;margin:0 auto}
.row .chip{width:180px;height:54px}
.t{font-size:12.5px;color:var(--tx2);line-height:1.35}.t b{display:block;color:var(--tx);font-size:14px;font-weight:600}
.vl{width:2px;height:14px;background:rgba(255,255,255,.2);margin:0 auto}
.kids{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;border-top:2px solid rgba(255,255,255,.2);padding-top:16px;margin:0 140px 0 140px;width:auto}
.kids{margin:0}
.kid{padding:14px 12px;text-align:center;position:relative}
.kid .chip{width:100%;height:64px;margin-bottom:10px}
.me{border:1.5px solid var(--or);background:linear-gradient(180deg,rgba(255,90,31,.22),rgba(30,12,6,.9));box-shadow:0 0 34px rgba(255,90,31,.38)}
.me .t{color:#FFD3C0}
.badge{position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:var(--or);color:#fff;font:700 8.5px var(--sans);
 letter-spacing:.14em;padding:3px 10px;border-radius:999px;white-space:nowrap}
/* business lines */
.bl{position:absolute;left:44px;right:44px;top:168px;bottom:52px;display:grid;grid-template-columns:1fr 1.35fr;gap:26px}
.brands{display:grid;grid-template-rows:1fr 1fr;gap:14px;min-height:0}
.bcard{padding:20px 22px;display:flex;flex-direction:column;justify-content:center}
.bcard .chip{width:210px;height:70px;margin-bottom:16px}
.bcard .k{font:600 10px var(--sans);letter-spacing:.14em;color:var(--or);margin-bottom:6px}
.bcard .h{font-size:20px;font-weight:600}
.bcard .d{font-size:13px;color:var(--tx2);margin-top:6px;line-height:1.45}
.inds{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;min-height:0}
.ind{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line)}
.ind img{width:100%;height:100%;object-fit:cover;display:block}
.ind::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 40%,rgba(0,0,0,.82))}
.ind .n{position:absolute;left:16px;bottom:14px;z-index:1;display:flex;align-items:baseline;gap:10px}
.ind .n b{font-size:22px;color:var(--or);font-weight:600}.ind .n span{font-size:16px;font-weight:600}
#nav{display:none;position:fixed;bottom:10px;left:50%;transform:translateX(-50%);display:flex;gap:6px;z-index:5;opacity:.5}
html.present #nav{display:flex}
#nav button{background:#1b1a18;border:1px solid #34312c;color:#eee;width:34px;height:30px;cursor:pointer}
"""

def frame(inner, n, cls=""):
    return f'''<svg class="frame" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg"><foreignObject width="1280" height="720"><section xmlns="http://www.w3.org/1999/xhtml" class="slide {cls}"><div class="glow"></div><div class="bars"></div>
<div class="hdr"><span>[ INTERNAL USE ONLY ]</span><img src="{tri}" alt="Triatra"></div>
{inner}<div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>{n:02d}</b> / 15</span></div></section></foreignObject></svg>'''

names = ["Dump Vessel", "Side Dump Trailer", "Dump Truck Body", "Water Truck", "Service Truck"]
heights = [128] * 5  # uniform height so the line-up reads as one fleet
lineup = "".join(f'<div class="u"><img src="{u}" style="--h:{h}px" alt="{n}"><span>{n.upper()}</span></div>'
                 for u, n, h in zip(units, names, heights))
s1 = frame(f'''<div class="sec">SECTION 01</div><h2>Company Profile</h2>
<div class="sub">Who we are, where we sit in the Astra group, and the markets we serve</div>
<div class="road"></div><div class="lineup">{lineup}</div>
<div class="agenda"><b>01</b> Company Structure &nbsp;·&nbsp; <b>02</b> Business Line &amp; Industries</div>
<div class="brandrow"><div class="chip"><img src="{logo['triatra']}"></div><div class="chip"><img src="{logo['utpe']}"></div>
<div class="chip"><img src="{logo['patria']}"></div><div class="chip"><img src="{logo['ultra']}"></div></div>''', 2, "intro")

s2 = frame(f'''<div class="kick">COMPANY STRUCTURE</div><h1>Company Profile</h1>
<div class="tree">
 <div class="card row"><div class="chip"><img src="{logo['astra']}"></div><div class="t"><b>Astra International</b>Astra Heavy Equipment, Mining, Construction, and Energy</div></div>
 <div class="vl"></div>
 <div class="card row"><div class="chip"><img src="{logo['ut']}"></div><div class="t"><b>United Tractors</b>Construction Machinery</div></div>
 <div class="vl"></div>
 <div class="card row"><div class="chip"><img src="{logo['utpe']}"></div><div class="t"><b>UTPE</b>Astra Heavy Equipment, Mining, Construction, and Energy</div></div>
 <div class="vl"></div>
 <div class="kids">
  <div class="card kid me"><span class="badge">MY COMPANY</span><div class="chip"><img src="{logo['triatra']}"></div><div class="t">Distributorship and Trading</div></div>
  <div class="card kid"><div class="chip"><img src="{logo['pml']}"></div><div class="t">Logistic and Energy Provider</div></div>
  <div class="card kid"><div class="chip"><img src="{logo['pmp']}"></div><div class="t">Ship Building and Maintenance</div></div>
 </div>
</div>''', 3)

inds = "".join(f'<div class="ind"><img src="{src}"><div class="n"><b>{i+1:02d}</b><span>{t}</span></div></div>'
               for i, (src, t) in enumerate(zip(ind, ["Coal &amp; Mineral Mining", "Construction", "Forestry &amp; Agro", "Maritime"])))
s3 = frame(f'''<div class="kick">COMPANY PROFILE</div><h1>Business Line &amp; Industries</h1>
<div class="bl">
 <div><div class="lbl">BUSINESS LINE</div><div class="brands" style="height:calc(100% - 22px)">
  <div class="card bcard"><div class="chip"><img src="{logo['patria']}"></div><div class="k">UNIT</div><div class="h">PATRIA</div><div class="d">International &amp; domestic trader of UTPE units</div></div>
  <div class="card bcard"><div class="chip"><img src="{logo['ultra']}"></div><div class="k">PART, COMPONENT &amp; SERVICES</div><div class="h">ULTRA</div><div class="d">After-sales services, including maintenance and remanufacturing</div></div>
 </div></div>
 <div><div class="lbl">INDUSTRIES</div><div class="inds" style="height:calc(100% - 22px)">{inds}</div></div>
</div>''', 4)

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Section 01 · Company Profile</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{s1}{s2}{s3}
<div id="nav"><button id="pv">‹</button><button id="nx">›</button></div>
<script>
document.documentElement.classList.add('present');
const S=[...document.querySelectorAll('.frame')];let i=0;
function show(n){{i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,k)=>s.classList.toggle('on',k===i))}}
show(0);
addEventListener('keydown',e=>{{if(['ArrowRight','PageDown',' '].includes(e.key))show(i+1);if(['ArrowLeft','PageUp'].includes(e.key))show(i-1)}});
document.getElementById('pv').onclick=()=>show(i-1);document.getElementById('nx').onclick=()=>show(i+1);
</script></body></html>'''
open("NEDP_Section01_Ref4.html", "w").write(html)
print(len(html) // 1024, "KB")
