"""Final Ref4 (Dark Glow) deck: rebuilds the skin, replaces slides 2-3 with the new Section 01 design,
widens the orange glow, and makes every slide render without JavaScript (SVG-scaled frames)."""
import re, runpy

runpy.run_path("build_ref_skins.py")                      # fresh NEDP_Deck_Ref4_Streamline.html
src = open("build_section01.py").read()
exec(src.split("CSS = ")[0])                               # helpers + embedded assets: logo, tri, units, ind

OUT = "NEDP_Deck_Ref4_Streamline.html"
html = open(OUT).read()

# ---------- slide 02: GGE-style section opener with the unit line-up ----------
order = [1, 3, 0, 2, 4]                                    # trailer, water truck, dump vessel (centre), dump body, service truck
heights = [118, 136, 172, 136, 118]
lineup = "".join(f'<img src="{units[k]}" style="height:{h}px" alt="">' for k, h in zip(order, heights))
# Slide 2: live-rendered opener (crisp at any resolution), modelled on the approved artwork.
hd = [png(A + f"cutout/u{i}.png", 900) for i in range(1, 6)]
order = [1, 3, 0, 2, 4]                                    # trailer, water truck, dump vessel (centre), dump body, service truck
heights = [118, 134, 172, 134, 124]
lineup = "".join(f'<img src="{hd[k]}" style="height:{h}px" alt="">' for k, h in zip(order, heights))
slide2 = f'''<section class="slide opener"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span></span><img class="tri" src="{tri}" alt="Triatra"></div>
  <img class="mark" src="{tri}" alt="">
  <div class="osec">SECTION 01</div>
  <h2 class="otitle">Company Profile</h2>
  <div class="osub">Part of the UTPE Group · Distributor of PATRIA and ULTRA</div>
  <div class="ofloor"></div><div class="ohorizon"></div>
  <div class="olineup">{lineup}</div>
  <div class="obrands"><div class="chip"><img src="{logo['patria']}"></div><div class="chip"><img src="{logo['ultra']}"></div></div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>02</b> / 15</span></div>
</div></section>'''

# ---------- slide 03: Company Group & Business ----------
inds = "".join(
    f'<div class="ind">{"<span class=newtag>NEW · 2025</span>" if t == "Maritime" else ""}<img src="{p}"><div class="n"><b>{i+1:02d}</b><span>{t}</span></div></div>'
    for i, (p, t) in enumerate(zip(ind, ["Coal &amp; Mineral Mining", "Construction", "Forestry &amp; Agroindustry", "Maritime"])))
slide3 = f'''<section class="slide cg"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span>SEC/01 — COMPANY</span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="kick">Company Group &amp; Business</div>
  <h1 class="t">Company Profile</h1>
  <div class="keys">
   <div class="key"><b>01</b>Triatra is part of the UTPE Group and AHEMCE, focusing on Distributorship and Trading.</div>
   <div class="key"><b>02</b>Starting in 2025, Triatra develops a new business line in Marine.</div>
  </div>
  <div class="cgrid">
   <div class="cleft">
    <div class="lbl">CORPORATE ENTITY STRUCTURE</div>
    <p class="intro">PT Triatra Sinergia Pratama is one of the entities within the UTPE Group, part of the UT Group and the AHEMCE business line of PT Astra International Tbk.</p>
    <div class="c row"><div class="chip"><img src="{logo['astra']}"></div><div class="tt"><b>Astra International</b>Astra Heavy Equipment, Mining, Construction, and Energy</div></div>
    <div class="vl"></div>
    <div class="c row"><div class="chip"><img src="{logo['ut']}"></div><div class="tt"><b>United Tractors</b>Construction Machinery</div></div>
    <div class="vl"></div>
    <div class="c row"><div class="chip"><img src="{logo['utpe']}"></div><div class="tt"><b>UTPE</b>Engineering Solution &amp; Marine</div></div>
    <div class="vl"></div>
    <div class="kids">
     <div class="c kid me"><span class="badge">MY COMPANY</span><div class="chip"><img src="{logo['triatra']}"></div><div class="tt">Distributorship and Trading</div></div>
     <div class="c kid"><div class="chip"><img src="{logo['pml']}"></div><div class="tt">Ship Owner &amp; Operator</div></div>
     <div class="c kid"><div class="chip"><img src="{logo['pmp']}"></div><div class="tt">Ship Building and Repair</div></div>
    </div>
   </div>
   <div class="cright">
    <div class="lbl">PT TRIATRA SINERGIA PRATAMA</div>
    <div class="c about">Distributor of <b>PATRIA</b> and <b>ULTRA</b> products for mining, construction, agriculture, forestry and maritime. Triatra offers both equipment units and full after-sales support, from spare parts and remanufacturing to maintenance services.</div>
    <div class="blines">
     <div class="c bl"><div class="chip"><img src="{logo['patria']}"></div><div class="tt"><b>Unit</b>International &amp; domestic trader of UTPE units</div></div>
     <div class="c bl"><div class="chip"><img src="{logo['ultra']}"></div><div class="tt"><b>Part, Component &amp; Services</b>After-sales maintenance &amp; remanufacturing</div></div>
    </div>
    <div class="lbl" style="margin-top:12px">INDUSTRY COVERAGE</div>
    <div class="inds">{inds}</div>
   </div>
  </div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>03</b> / 15</span></div>
</div></section>'''

# ---------- slide 05: Site Operation & Support ----------
mapimg = png(A + "indonesia_neon.png", 1600)
SITES = [  # (no, name, address, type, x, y) — x/y in source outline px (695x287); type H/O/R
 (1, "Head Office", "Jl. Raya Bekasi KM 22, Cakung, Jakarta Timur, 13910", "H", 191, 210),
 (2, "Jakarta", "Jl. Raya Bekasi KM 22, Cakung, Jakarta Timur, 13910", "O", 179, 200),
 (3, "Tanjung Enim", "Jl. Lingga Raya 10, Kel. Muara Enim, Sumatera Selatan, 31711", "R", 140.5, 171.2),
 (4, "Pekanbaru", "Jl. Soekarno Hatta KM 3,5 No. 151, Pekanbaru, Riau, 28291", "R", 106.5, 110.2),
 (5, "Banjarmasin", "Jl. Ahmad Yani KM 13,5 Gambut, Banjarmasin, Kalimantan Selatan, 70652", "R", 296.7, 165.0),
 (6, "Sungai Danau", "Ds. Karang Indah RT 12/RW 03, Kec. Angsana, Tanah Bambu, Kalimantan Selatan", "R", 309.4, 170.9),
 (7, "Tanjung Tabalong", "Jl. A. Yani KM 7,5 Maburai, Kec. Murung Pudak, Kab. Tabalong, Kalimantan Selatan", "O", 308.8, 148.3),
 (8, "Batu Kajang", "Jl. Negara KM 140 Batukajang, Kec. Batu Sopang, Kab. Paser, Kalimantan Timur", "R", 317.8, 143.3),
 (9, "Muara Teweh", "Jl. Ahmad Yani No. 85, Kel. Melayu, Kab. Barito Utara, Kalimantan Tengah", "R", 301.0, 131.1),
 (10, "Balikpapan", "Jl. Jenderal Sudirman No. 844, Balikpapan, Kalimantan Timur, 76114", "O", 329.1, 135.2),
 (11, "Melak", "D/A PT Tambang Raya Usaha Tama, Hauling Road Trubaindo, Muara Lawa, Kutai Barat, Kalimantan Timur", "R", 314.6, 120.8),
 (12, "Tabang", "Site Indonesia Pratama, Workshop Buma Km 6, Hauling Road Baratabang, Kec. Muara", "R", 317.5, 109.6),
 (13, "Tanjung Redeb", "Jl. Gunung Panjang RT.04 No. 101B, Kab. Berau, 77311", "R", 338.7, 86.7),
 (14, "Sangatta", "Jl. HDRS Tango Delta KPC, Mine Site Sangatta, Kutai Timur, 75683", "O", 339.5, 110.3),
 (15, "Sumbawa", "Memco Area Tongo, Sekongkang, West Sumbawa, Nusa Tenggara Barat, 84457", "R", 378, 247),
 (16, "Timika", "Jl. Kuala Tembaga E-4 LIP Kuala Kencana, Timika, 99920", "O", 619, 185),
]
pins = "".join(f'<div class="pin {t}" style="left:{(x-16)/663*100:.2f}%;top:{(y-33)/242*100:.2f}%">{n}</div>' for n, _, _, t, x, y in SITES)
items = "".join(f'<div class="si"><span class="sn {t}">{n}</span><div><b>{nm}</b>{ad}</div></div>' for n, nm, ad, t, _, _ in SITES)
slide5 = f'''<section class="slide site"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span>SEC/02 — SITE</span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="kick">Site Operation &amp; Support</div>
  <h1 class="t">Site Operation</h1>
  <div class="ssub">Triatra covers many areas in Indonesia, with the Head Office in Jakarta, 5 Site Operations and Site Representatives.</div>
  <div class="map"><img src="{mapimg}" alt="Indonesia">{pins}</div>
  <div class="legend"><span><i class="H"></i>Head Office</span><span><i class="O"></i>Site Operation</span><span><i class="R"></i>Site Representative</span></div>
  <div class="slist">{items}</div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>05</b> / 15</span></div>
</div></section>'''

# ---------- swap slides 2 and 3 ----------
parts = re.split(r'(?=<!-- \d\d [^>]*-->\s*<section)', html)
idx = [k for k, p in enumerate(parts) if re.match(r'<!-- 0[23] ', p)]
i5 = [k for k, p in enumerate(parts) if re.match(r'<!-- 05 ', p)][0]
parts[i5] = "<!-- 05 SITE -->\n" + slide5 + "\n\n"
assert len(idx) == 2, idx
parts[idx[0]] = "<!-- 02 OPENER -->\n" + slide2 + "\n\n"
parts[idx[1]] = "<!-- 03 COMPANY -->\n" + slide3 + "\n\n"
html = "".join(parts)

# ---------- Triatra logo (no background) top-right on every slide ----------
html = html.replace('<span class="brand"><i></i>TRIATRA</span>', f'<img class="tri" src="{tri}" alt="Triatra">')
html = html.replace('.top img.tri', '.top img.tri') 

# ---------- no-JS rendering: wrap each slide in an SVG frame ----------
html = html.replace('<div id="stage"><div class="deck" id="deck">', '<main id="deck">')
html = re.sub(r'</div></div>\s*<div id="nav">', '</main>\n<div id="nav">', html, count=1)
html = re.sub(r'<section class="slide([^"]*)">(.*?)</section>',
              lambda m: f'<svg class="frame" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg"><foreignObject width="1280" height="720">'
                        f'<section xmlns="http://www.w3.org/1999/xhtml" class="slide{m.group(1).replace(" on", "")}">{m.group(2)}</section></foreignObject></svg>',
              html, flags=re.S)

EXTRA = """
/* ===== final Ref4 overrides ===== */
html,body{height:auto!important;overflow:auto!important}
body{padding:16px;display:flex;flex-direction:column;gap:16px}
#deck{display:flex;flex-direction:column;gap:16px}
.frame{display:block;width:100%;height:auto}
.frame .slide{position:relative!important;inset:auto!important;width:1280px;height:720px;opacity:1!important;transform:none!important;pointer-events:auto!important}
html.present,html.present body{height:100%!important;overflow:hidden!important}
html.present body{padding:0;display:grid;place-items:center}
html.present #deck{display:contents}
html.present .frame{display:none;width:min(100vw,calc(100vh*16/9))}
html.present .frame.on{display:block}
#nav,#bar{display:none}html.present #nav,html.present #bar{display:flex}html.present #bar{display:block}
/* wider orange silhouette on every slide */
.slide:not(.div)::before{background:
 radial-gradient(120% 70% at 50% 120%,rgba(255,106,43,.42) 0%,rgba(210,56,15,.26) 32%,rgba(90,18,5,.14) 56%,transparent 76%),
 radial-gradient(60% 55% at 100% 0%,rgba(255,90,31,.12),transparent 70%),
 radial-gradient(50% 50% at 0% 40%,rgba(255,90,31,.07),transparent 70%)!important}
.top img.tri{height:26px;display:block}
.chip{background:#fff;border-radius:9px;display:flex;align-items:center;justify-content:center;padding:4px 8px;flex:none;overflow:hidden}
.chip img{max-width:100%;max-height:100%;width:auto;height:auto;display:block}
/* opener (modelled on approved artwork) */
.opener{background:
 radial-gradient(70% 45% at 50% 0%,rgba(60,70,90,.35),transparent 70%),
 radial-gradient(140% 85% at 50% 100%,#FF7A2E 0%,#E84A12 22%,#A8280A 42%,#4a1205 62%,#0B0B0B 82%)!important}
.opener::before{display:none}
.opener .mark{position:absolute;left:50%;top:118px;transform:translateX(-50%);width:640px;opacity:.13;mix-blend-mode:screen;filter:saturate(.4)}
.opener .osec{position:absolute;left:0;right:0;top:82px;text-align:center;font:600 13px var(--sans);letter-spacing:.32em;color:var(--or)}
.opener .otitle{position:absolute;left:0;right:0;top:104px;text-align:center;font-weight:700;font-size:84px;letter-spacing:-.03em;
 background:linear-gradient(180deg,#fff 35%,#b9b3ad);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 6px 18px rgba(0,0,0,.45))}
.opener .osub{position:absolute;left:0;right:0;top:214px;text-align:center;font-size:17px;font-weight:500;color:#efe9e4}
.opener .ofloor{position:absolute;left:0;right:0;top:528px;bottom:0;background:
 linear-gradient(180deg,rgba(255,120,50,.55),rgba(232,74,18,.25) 30%,transparent 70%)}
.opener .ohorizon{position:absolute;left:3%;right:3%;top:524px;height:6px;border-radius:50%;
 background:radial-gradient(50% 50% at 50% 50%,rgba(255,220,180,.9),rgba(255,120,40,.5) 40%,transparent 75%);filter:blur(2px)}
.opener .olineup{position:absolute;left:30px;right:30px;top:300px;height:230px;display:flex;align-items:flex-end;justify-content:center}
.opener .olineup img{display:block;width:auto;margin:0 -10px;filter:drop-shadow(0 14px 10px rgba(0,0,0,.55));
 -webkit-box-reflect:below 0 linear-gradient(transparent 62%,rgba(0,0,0,.28))}
.opener .olineup img:nth-child(3){position:relative;z-index:2}
.opener .olineup img:nth-child(2),.opener .olineup img:nth-child(4){position:relative;z-index:1}
.opener .obrands{position:absolute;left:0;right:0;bottom:70px;display:flex;justify-content:center;gap:18px}
.opener .obrands .chip{width:190px;height:56px;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.35)}
.opener .foot{color:rgba(255,255,255,.7)}
/* site operation */
.site .ssub{position:absolute;left:44px;top:156px;font-size:12px;color:var(--tx2)}
.site .map{position:absolute;left:150px;right:150px;top:180px;height:300px}
.site .map img{width:100%;height:100%;object-fit:fill;display:block;filter:drop-shadow(0 0 4px rgba(255,110,40,.9)) drop-shadow(0 0 14px rgba(255,90,31,.55))}
.site .pin{position:absolute;transform:translate(-50%,-50%);width:17px;height:17px;border-radius:50%;display:grid;place-items:center;font:700 8px var(--sans)}
.site .pin.H,.site .sn.H{background:var(--or);color:#fff;box-shadow:0 0 12px var(--or)}
.site .pin.O,.site .sn.O{background:#fff;color:#111;box-shadow:0 0 10px rgba(255,255,255,.7)}
.site .pin.R,.site .sn.R{background:#111;color:#fff;border:1.5px solid var(--or)}
.site .legend{position:absolute;right:44px;top:150px;display:flex;gap:16px;font-size:10.5px;color:var(--tx2)}
.site .legend span{display:flex;align-items:center;gap:6px}
.site .legend i{width:11px;height:11px;border-radius:50%;display:inline-block}
.site .legend i.H{background:var(--or)}.site .legend i.O{background:#fff}.site .legend i.R{background:#111;border:1.5px solid var(--or)}
.site .slist{position:absolute;left:44px;right:44px;top:492px;bottom:40px;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-auto-flow:column;grid-template-rows:repeat(4,auto);gap:5px 14px}
.site .si{display:flex;gap:7px;font-size:8.3px;line-height:1.3;color:var(--tx2)}
.site .si b{display:block;color:var(--tx);font-size:9.5px}
.site .sn{flex:none;width:16px;height:16px;border-radius:50%;display:grid;place-items:center;font:700 7.5px var(--sans)}
/* company group & business */
.cg .keys{position:absolute;left:44px;right:44px;top:146px;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.cg .key{font-size:11.5px;color:var(--tx2);line-height:1.35;padding:8px 12px;border:1px solid var(--line);border-radius:10px;background:rgba(255,255,255,.03);display:flex;gap:10px;align-items:center}
.cg .key b{color:var(--or);font-size:13px}
.cg .cgrid{position:absolute;left:44px;right:44px;top:200px;bottom:44px;display:grid;grid-template-columns:1fr 1.08fr;gap:24px}
.cg .cleft,.cg .cright{display:flex;flex-direction:column;min-height:0}
.cg .lbl{margin-bottom:6px}
.cg .intro{font-size:10.5px;color:var(--tx2);line-height:1.4;margin-bottom:8px}
.cg .row{display:flex;align-items:center;gap:12px;padding:6px 10px;height:66px}
.cg .row .chip{width:140px;height:48px}
.cg .tt{font-size:10.5px;color:var(--tx2);line-height:1.3}.cg .tt b{display:block;color:var(--tx);font-size:12px;font-weight:600}
.cg .vl{width:2px;height:10px;background:rgba(255,255,255,.2);margin-left:78px}
.cg .kids{flex:1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;border-top:2px solid rgba(255,255,255,.2);padding-top:12px;min-height:0}
.cg .kid{padding:12px 8px 8px;text-align:center;position:relative;display:flex;flex-direction:column;justify-content:center}
.cg .kid .chip{width:100%;height:54px;margin-bottom:6px}
.cg .kid .tt{font-size:10px}
.cg .me{border:1.5px solid var(--or);background:linear-gradient(180deg,rgba(255,90,31,.22),rgba(30,12,6,.9));box-shadow:0 0 30px rgba(255,90,31,.38)}
.cg .me .tt{color:#FFD3C0}
.cg .badge{position:absolute;top:-9px;left:50%;transform:translateX(-50%);background:var(--or);color:#fff;font:700 8px var(--sans);letter-spacing:.14em;padding:3px 9px;border-radius:999px;white-space:nowrap}
.cg .about{font-size:11px;color:var(--tx2);line-height:1.45;padding:10px 12px}.cg .about b{color:var(--tx)}
.cg .blines{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
.cg .bl{display:flex;align-items:center;gap:10px;padding:8px 10px}
.cg .bl .chip{width:104px;height:36px}
.cg .inds{flex:1;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:repeat(2,minmax(0,1fr));gap:8px;min-height:0}
.cg .ind{position:relative;border-radius:12px;overflow:hidden;border:1px solid var(--line)}
.cg .ind img{width:100%;height:100%;object-fit:cover;display:block}
.cg .ind::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 40%,rgba(0,0,0,.85))}
.cg .ind .n{position:absolute;left:12px;right:10px;bottom:8px;z-index:1;display:flex;align-items:baseline;gap:8px}
.cg .ind .n b{font-size:15px;color:var(--or);font-weight:600}.cg .ind .n span{font-size:12px;font-weight:600;line-height:1.25}
.cg .newtag{position:absolute;top:8px;right:8px;z-index:2;background:var(--or);color:#fff;font:700 8px var(--sans);letter-spacing:.12em;padding:3px 7px;border-radius:999px}
"""
html = html.replace("</style>\n</head>", EXTRA + "</style>\n</head>", 1)

JS = """<script>
document.documentElement.classList.add('present');
const S=[...document.querySelectorAll('.frame')],bar=document.getElementById('bar');
let i=0;try{i=Math.min(+(location.hash.slice(1)||1)-1,S.length-1)||0}catch(e){}
function show(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,k)=>s.classList.toggle('on',k===i));bar.style.width=((i+1)/S.length*100)+'%';try{history.replaceState(null,'','#'+(i+1))}catch(e){}}
show(i);
addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key))show(i+1);if(['ArrowLeft','PageUp'].includes(e.key))show(i-1);if(e.key==='Home')show(0);if(e.key==='End')show(S.length-1)});
document.getElementById('pv').onclick=()=>show(i-1);document.getElementById('nx').onclick=()=>show(i+1);
S.forEach(f=>f.addEventListener('click',e=>{const r=f.getBoundingClientRect();show(e.clientX>r.left+r.width/2?i+1:i-1)}));
</script>"""
html = re.sub(r"<script>.*?</script>", lambda m: JS, html, count=1, flags=re.S)
open(OUT, "w").write(html)
print("built", OUT, len(html) // 1024, "KB")
