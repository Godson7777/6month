"""Builds four reference-inspired skins of the HTML deck from NEDP_Deck_Industrial.html."""
base = open('NEDP_Deck_Industrial.html').read()
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Oswald:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'

COMMON = """
.slide{font-family:var(--sans)}
"""

SKINS = {
"Ref1_GradStroy": ("Bold Orange", """
:root{--page:#2A2A2A;--bg:#FFFFFF;--panel:#F6F5F3;--panel2:#EFEDE9;--line:#E5E2DC;--grid:transparent;
 --or:#F0501E;--or-dim:#FFEDE5;--or-glow:rgba(240,80,30,.18);--steel:#2B2B2B;--steel-dim:#EEE;
 --tx:#141414;--tx2:#4A4A4A;--mut:#8F8F8F;--dash:#CFCBC4;--me-tx:#7A2208;--outline:#F0501E;--hatch:rgba(0,0,0,.02);
 --sans:"Inter",system-ui,sans-serif;--mono:"Inter",system-ui,sans-serif}
.c::after{display:none}.c{border:none;border-radius:0}
.kick{font:600 10px var(--sans);letter-spacing:.06em;text-transform:none;color:var(--mut)}
.kick::before{width:6px;height:6px;border-radius:50%}
h1.t{font-weight:600;font-size:28px;letter-spacing:-.01em}
.brand{background:var(--or);color:#fff;padding:5px 10px;font:700 12px "Oswald",sans-serif;letter-spacing:.04em}.brand i{display:none}
.top{font-family:var(--sans);letter-spacing:.02em;text-transform:none}
.num{clip-path:none;font-family:"Oswald",sans-serif;font-size:14px}
.c .lbl,.lbl{font-family:var(--sans);letter-spacing:.08em}
.pill{border:none;background:var(--or);color:#fff}.pill.s{background:#2B2B2B;color:#fff}
.div{background:radial-gradient(120% 140% at 85% 30%,#FF6A2B 0%,#E8461A 45%,#B82A0A 100%)!important}
.div::before{background-image:repeating-linear-gradient(90deg,transparent 0 212px,rgba(255,255,255,.35) 212px 213px)!important;background-size:auto!important}
.div .big{display:none}.div .haz{height:2px;background:rgba(255,255,255,.5);bottom:96px}
.div h2{font:700 104px/0.95 "Oswald",sans-serif;text-transform:uppercase;color:#fff;max-width:1000px;top:200px;letter-spacing:-.01em}
.div .sec{color:#fff;top:170px;font-family:var(--sans)}
.div .subs{color:rgba(255,255,255,.7);top:470px!important;font-family:var(--sans)}.div .subs .a{color:#fff}
.div .top .tag,.div .foot,.div .foot b{color:rgba(255,255,255,.8)}
.div .brand{background:#fff;color:var(--or)}
.me{box-shadow:none}
span[style*="font:700 30px var(--mono)"],span[style*="font:700 20px var(--mono)"]{font-family:"Oswald",sans-serif!important;font-size:38px!important;font-weight:500!important}
"""),
"Ref2_ProjectM": ("Monochrome Engineering", """
:root{--page:#1E1E1E;--bg:#0A0A0A;--panel:rgba(255,255,255,.055);--panel2:rgba(255,255,255,.09);--line:rgba(255,255,255,.12);--grid:transparent;
 --or:#FF7A2F;--or-dim:rgba(255,122,47,.12);--or-glow:rgba(255,122,47,.25);--steel:#BDBDBD;--steel-dim:rgba(255,255,255,.06);
 --tx:#F2F2F2;--tx2:#A6A6A6;--mut:#6E6E6E;--dash:#4A4A4A;--me-tx:#FFD9C4;--outline:rgba(255,255,255,.18);--hatch:rgba(255,255,255,.015);
 --sans:"Inter",system-ui,sans-serif;--mono:"Inter",system-ui,sans-serif}
.slide::before{background-image:repeating-linear-gradient(90deg,transparent 0 319px,rgba(255,255,255,.08) 319px 320px)!important;background-size:auto!important}
.slide::after{content:"";position:absolute;left:0;right:0;bottom:-120px;height:260px;background:radial-gradient(50% 60% at 70% 100%,rgba(255,110,40,.18),transparent 70%);pointer-events:none}
h1.t{font-weight:400;font-size:30px;letter-spacing:-.02em}
.kick{font:400 12px var(--sans);letter-spacing:.02em;text-transform:none;color:var(--tx2)}
.kick::before{content:"[";width:auto;height:auto;background:none}.kick::after{content:"]"}
.c{border:none;border-radius:0;backdrop-filter:blur(4px)}
.c::after{background:linear-gradient(#777,#777) top left/6px 6px no-repeat,linear-gradient(#777,#777) bottom right/6px 6px no-repeat!important}
.c.plain::after{display:block}
.n{font-weight:500}.r,.lbl,.top,.foot{font-family:var(--sans)}
.num{clip-path:none;background:transparent;border:1px solid var(--or);color:var(--or)!important;font-weight:400}
.sc .num{border-color:#BDBDBD;color:#BDBDBD!important}
.brand{font:500 13px var(--sans);letter-spacing:.2em}.brand i{background:var(--tx);clip-path:polygon(0 100%,35% 0,100% 0,65% 100%)}
.div .big{-webkit-text-stroke:1px rgba(255,255,255,.35);font-weight:300;font-size:430px;right:auto;left:30px;top:20px;letter-spacing:-.04em}
.div .haz{display:none}
.div h2{font-weight:400;font-size:62px;left:auto;right:44px;top:300px;text-align:right;letter-spacing:-.03em}
.div .sec{left:auto;right:44px;top:270px;color:var(--tx2);font-family:var(--sans)}
.div .subs{left:auto;right:44px;text-align:right;font-family:var(--sans)}
.div::after{bottom:-60px;height:400px;background:radial-gradient(40% 60% at 30% 100%,rgba(255,110,40,.35),transparent 70%)}
.pill{border-color:rgba(255,255,255,.3);color:var(--tx2)}
"""),
"Ref3_Luma": ("Gradient Proposal", """
:root{--page:#D9D9D9;--bg:#FFFFFF;--panel:#FFFFFF;--panel2:#4A4A4A;--line:#E3E3E3;--grid:transparent;
 --or:#F2600F;--or-dim:#FFF0E6;--or-glow:rgba(242,96,15,.2);--steel:#3D3D3D;--steel-dim:#EFEFEF;
 --tx:#1A1A1A;--tx2:#555;--mut:#9A9A9A;--dash:#D0D0D0;--me-tx:#7A2A00;--outline:rgba(255,255,255,.9);--hatch:rgba(0,0,0,.015);
 --sans:"Inter",system-ui,sans-serif;--mono:"Inter",system-ui,sans-serif}
.slide:not(.div)::after{content:"";position:absolute;left:0;right:0;bottom:0;height:10px;background:linear-gradient(90deg,#1a0d06,#8a2c05 35%,#F2600F 70%,#FF9A4D)}
h1.t{font-weight:300;font-size:32px;letter-spacing:-.025em}
.kick{font:500 10px var(--sans);letter-spacing:.14em}
.kick::before{display:none}
.c{border:none;border-radius:2px;box-shadow:0 2px 10px rgba(0,0,0,.08)}.c::after{display:none}
.org .head{background:#4A4A4A!important}.org .head .n{color:#fff}.org .head .r{color:#CFCFCF}
.num{clip-path:none;border-radius:50%;background:var(--or)}
.sc .num{background:#3D3D3D}
.r,.lbl,.top,.foot{font-family:var(--sans)}
.brand i{border-radius:50%;clip-path:none;background:conic-gradient(var(--or) 0 25%,#fff 0 30%,var(--or) 0 55%,#fff 0 60%,var(--or) 0 80%,#fff 0)}
.pill{border:none;background:linear-gradient(90deg,#8a2c05,#F2600F);color:#fff}.pill.s{background:#3D3D3D;color:#fff}
.div{background:linear-gradient(115deg,#120804 0%,#5a1d04 38%,#E85410 72%,#FF8A3D 100%)!important}
.div .big{color:#fff;-webkit-text-stroke:0;font-weight:200;font-size:300px;top:auto;bottom:90px;right:44px;opacity:.95}
.div .haz{display:none}
.div h2{color:#fff;font-weight:300;font-size:60px;top:120px;letter-spacing:-.03em}
.div .sec{top:90px;color:#FFB585;font-family:var(--sans)}
.div .subs{top:330px!important;color:rgba(255,255,255,.6);font-family:var(--sans)}.div .subs .a{color:#fff}
.div .top .tag,.div .foot,.div .foot b,.div .brand{color:#fff}
span[style*="font:700 30px var(--mono)"]{font-weight:200!important;font-size:38px!important;color:var(--tx)!important}
"""),
"Ref4_Streamline": ("Dark Glow", """
:root{--page:linear-gradient(180deg,#141414,#5a1c08);--bg:#0B0B0B;--panel:linear-gradient(180deg,#171717,#0F0F0F);--panel2:#1D1D1D;--line:rgba(255,255,255,.09);--grid:transparent;
 --or:#FF5A1F;--or-dim:rgba(255,90,31,.12);--or-glow:rgba(255,90,31,.35);--steel:#FFB089;--steel-dim:rgba(255,176,137,.1);
 --tx:#F4F1EE;--tx2:#A9A29C;--mut:#6F6963;--dash:#3A3633;--me-tx:#FFD3C0;--outline:transparent;--hatch:rgba(255,255,255,.012);
 --sans:"Inter",system-ui,sans-serif;--mono:"Inter",system-ui,sans-serif}
html,body{background:linear-gradient(180deg,#121212,#4a1606)!important}
.slide{border-radius:22px}
.slide::before{background:radial-gradient(60% 50% at 100% 0%,rgba(255,90,31,.10),transparent 70%)!important;background-size:auto!important}
h1.t{font-weight:500;font-size:30px;letter-spacing:-.02em;background:linear-gradient(90deg,#fff,#9b9590);-webkit-background-clip:text;background-clip:text;color:transparent}
.kick{font:500 10px var(--sans);letter-spacing:.14em}.kick::before{display:none}
.c{border-radius:14px;border:1px solid var(--line);background:var(--panel)}.c::after{display:none}
.c.sc{background:linear-gradient(180deg,#1a1512,#0f0d0c)}
.num{clip-path:none;border-radius:8px}
.r,.lbl,.top,.foot{font-family:var(--sans)}
.foot{text-transform:uppercase;letter-spacing:.1em}
.ev{border-radius:12px;background:repeating-linear-gradient(90deg,rgba(255,90,31,.0) 0 26px,rgba(255,90,31,.06) 26px 30px)}
.pill{border-radius:999px}
.div{background:radial-gradient(90% 120% at 75% 115%,#FF6A2B 0%,#D2380F 28%,#5a1205 55%,#0B0B0B 80%)!important}
.div::before{background:repeating-linear-gradient(90deg,transparent 0 70px,rgba(255,140,90,.10) 70px 110px,transparent 110px 160px)!important;
  -webkit-mask:linear-gradient(180deg,transparent 0%,#000 60%);mask:linear-gradient(180deg,transparent 0%,#000 60%)}
.div .big{-webkit-text-stroke:0;color:rgba(255,255,255,.08);font-weight:600}
.div .haz{display:none}
.div h2{font-weight:500;font-size:62px;background:linear-gradient(90deg,#fff,#a7a19b);-webkit-background-clip:text;background-clip:text;color:transparent;top:150px}
.div .sec{top:120px;font-family:var(--sans)}
.div .subs{top:330px!important;font-family:var(--sans)}
"""),
}

for key, (name, css) in SKINS.items():
    s = base.replace('<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">', FONTS)
    s = s.replace("</style>\n</head>", "</style>\n<style>" + COMMON + css + "</style>\n</head>", 1)
    s = s.replace("<title>NEDP Mid Year Review</title>", f"<title>NEDP Review — {name}</title>")
    open(f"NEDP_Deck_{key}.html", "w").write(s)
    print("built", key)
