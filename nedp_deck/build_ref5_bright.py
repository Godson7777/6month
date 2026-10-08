"""Ref5 Bright: light, minimal brand-guideline theme layered over the final Ref4 deck."""
import re
SRC, OUT = "NEDP_Deck_Ref4_Streamline.html", "NEDP_Deck_Ref5_Bright.html"
CSS = r"""
/* ===== Ref5 Bright overrides ===== */
:root{--page:#E9E6E1;--bg:#FFFFFF;--panel:#FFFFFF;--panel2:#F6F2EC;--line:#ECE6DE;--grid:transparent;
 --or:#FF5A1F;--or-dim:rgba(255,90,31,.08);--or-glow:rgba(255,90,31,.18);--steel:#FF8A5C;--steel-dim:rgba(255,90,31,.06);
 --tx:#1B1B1B;--tx2:#5E5A55;--mut:#9A948D;--dash:#E2DBD2;--me-tx:#FF5A1F;--outline:transparent;--hatch:transparent}
body,html{background:#E9E6E1!important}
.slide{background:#FFFFFF!important;color:var(--tx)}
.slide::before,.slide::after{background:none!important;box-shadow:none!important}
.c{background:#FFFFFF!important;border:1px solid var(--line)!important;box-shadow:0 1px 0 rgba(0,0,0,.02)}
.c.plain,.pbox:nth-child(odd){background:var(--panel2)!important}
.slide h1,.slide h2,.slide h3,.slide h4,.slide b{color:var(--tx)}
.tag{color:var(--mut)!important}
/* section dividers = solid orange */
.slide.div{background:#FF5A1F!important}
.slide.div *{color:#FFFFFF!important;border-color:rgba(255,255,255,.35)!important}
.slide.div .big{color:rgba(255,255,255,.14)!important;-webkit-text-stroke:0!important}
.slide.div .tri{filter:brightness(0) invert(1)}
.slide.div .subs div{background:rgba(255,255,255,.12)!important}
/* opener: warm cream like the cover */
.slide.opener{background:#F5EFE6!important}
/* tables */
.pt th,.ptab th,.dt th,.sip2 th,.ex th{background:#FF5A1F!important;color:#fff!important;border:0!important;letter-spacing:.06em}
.pt td,.ptab td,.dt td,.sip2 td,.ex td{border:0!important;border-bottom:1px solid var(--line)!important;color:var(--tx2)!important;background:transparent!important}
.pt tr:nth-child(even) td,.ptab tr:nth-child(even) td,.dt tr:nth-child(even) td{background:#FBF7F2!important}
.dt tr.or td{color:#FF5A1F!important}.dt tr.bl td{color:#1D5FD0!important}.dt tr.tot td{color:var(--tx)!important;background:#FFE9DF!important}
/* org / highlight cards */
.cg .me{background:#FFF1EA!important;border:1.5px solid var(--or)!important;box-shadow:none!important}
.cg .key{background:#FBF7F2!important}
.cg .ind .n,.ph2 span,.pp span,.pp span *{color:#fff!important;-webkit-text-fill-color:#fff!important}
.ab3{background:linear-gradient(180deg,#FFF4EE,#FFD9C7)!important}
.xl{border:1px solid var(--line)}
.slide:not(.div)::before,.slide.div::before{background:none!important}
.slide h1.t{background:none!important;-webkit-text-fill-color:var(--tx)!important;color:var(--tx)!important;font-weight:600}
.slide.div h2{background:none!important;-webkit-text-fill-color:#fff!important;font-weight:600}
.c.sc{background:#FFFFFF!important}
.c::after{opacity:.0}
.opener{background:#F5EFE6!important}
.opener .otitle{background:none!important;-webkit-text-fill-color:#1B1B1B!important;color:#1B1B1B!important}
.opener .otitle b,.opener .otitle span{-webkit-text-fill-color:#FF5A1F!important}
.opener .ofloor{background:linear-gradient(180deg,#EDE4D8,#F5EFE6 70%)!important}
.opener .ohorizon{background:radial-gradient(50% 50% at 50% 50%,rgba(0,0,0,.18),transparent 75%)!important}
.opener .olineup img{filter:drop-shadow(0 12px 10px rgba(0,0,0,.18))!important;-webkit-box-reflect:unset!important}
.evbig{background:#F5EFE6!important}
.opener .mark{display:none!important}
.agt{display:flex;flex-direction:column;gap:3px}.agt b{font-size:18px;font-weight:700}.agt i{font-style:normal;font-size:11.5px;color:var(--tx2)}
.slide .body>div>.c.plain[style*="padding:14px 20px"]{flex:1;padding:6px 20px!important}
.agr{display:flex;flex-direction:column;overflow:hidden}
.agph{flex:1;position:relative;margin:14px -26px 0;background:linear-gradient(180deg,#FFF4EE,#FFD9C7);min-height:0}
.agph img{position:absolute;bottom:0;left:50%;transform:translateX(-50%);height:100%;width:auto}
.krs{width:100%;margin-top:14px;flex:1;display:flex;flex-direction:column;padding:12px 16px!important}
.kr2{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.kr2 b{display:block;font-size:13px;color:var(--or)!important;margin-bottom:6px;border-bottom:2px solid var(--or);padding-bottom:4px}
.kr2 ol{margin:0;padding-left:0;list-style:none;display:flex;flex-direction:column;justify-content:space-around;height:calc(100% - 30px)}
.kr2 li{font-size:12.5px;color:var(--tx);line-height:1.3;display:flex;gap:8px;align-items:center}.kr2 li i{font-style:normal;flex:none;width:20px;height:20px;border-radius:50%;background:#FFF1EA;color:#FF5A1F;font-weight:700;font-size:11px;display:grid;place-items:center}
.flw{margin-top:4px}.flw .lbl{margin-bottom:6px}
.fr{display:flex;align-items:center;gap:6px;flex-wrap:nowrap}
.fr span{flex:1;text-align:center;font-size:11px;font-weight:600;padding:9px 6px;border-radius:8px;background:#FBF7F2;border:1px solid var(--line);color:var(--tx)}
.fr span.l{background:#FF5A1F;color:#fff!important;border-color:#FF5A1F}
.fr em{font-style:normal;color:#FF5A1F;font-weight:700}
.org{display:flex;flex-direction:column;margin:10px 0 6px!important}
.org .cols{flex:1;align-items:start}
.org .col{gap:9px!important}
.org .col .c{padding:10px 14px!important;min-height:56px;display:flex;flex-direction:column;justify-content:center}
.org .hd{padding:10px 12px!important;width:340px!important}
.org .vl{height:14px!important}
.org .n{font-size:14px!important}.org .p,.org .r{font-size:11px!important}
.org .cols{padding-top:16px!important}
.jg{grid-template-columns:1.7fr 1fr 1fr!important}.jg .ph2:last-child{grid-column:span 2}
.opener .osub,.opener .foot,.opener .foot *{color:#5E5A55!important;-webkit-text-fill-color:#5E5A55!important;background:none!important}
.cg .me .tt,.cg .me .tt b{color:#FF5A1F!important}
.site .pin.R,.site .sn.R{background:#fff;color:var(--tx);}
.site .pin.O,.site .sn.O{border:1px solid #bbb}
.site .legend i.O{background:#fff;border:1px solid #bbb}
"""
h = open(SRC).read()

# ---------- layout upgrades: fill empty areas ----------
_src = open("build_section01.py").read(); exec(_src.split("CSS = ")[0].split("A = ")[0])
def rep(old, new, n=1):
    global h
    assert old in h, old[:60]
    h = h.replace(old, new, n)

# Agenda: descriptors under each section + presenter photo
DESC = {"Personal Information": "About me · Onboarding journey",
        "Company Profile": "Group structure · Business lines · Industries",
        "Site Operation": "Head office, site operations and representatives",
        "Organization Chart": "Marketing Unit &amp; Strategic Division",
        "Roles &amp; Responsibility": "Position &amp; products · Strategic vs supply chain",
        "Job Description Execution": "Strategic · Supply chain",
        "Project — F.lli Ferrari Crane Strategy": "Market overview · Price comparison · Advantage · Appendix"}
for k, v in DESC.items():
    rep(f'<span style="font-size:19px;font-weight:700">{k}</span></div>',
        f'<span class="agt"><b>{k}</b><i>{v}</i></span></div>')
rep('<div style="height:1px;background:var(--line);margin:22px 0"></div>\n      <div class="p">PT Triatra Sinergia Pratama<br>Marketing Unit &amp; Strategic Division</div>\n    </div>',
    f'<div class="p" style="margin-top:10px">PT Triatra Sinergia Pratama · Marketing Unit &amp; Strategic Division</div>\n      <div class="agph"><img src="{png("assets/personal/profile_photo.webp", 700)}"></div>\n    </div>')
rep('<div class="c" style="padding:26px">', '<div class="c agr" style="padding:26px 26px 0">')

# Position & Products: key responsibilities under the reporting line
rep('<div class="r" style="margin-top:8px">ASSOCIATES</div>',
    '<div class="r" style="margin-top:8px">ASSOCIATES</div>'
    '<div class="c krs"><div class="lbl">Key Responsibilities</div><div class="kr2">'
    '<div><b>Strategic</b><ol><li><i>1</i><span>Pricing &amp; Market Analysis</span></li><li><i>2</i><span>Market Study &amp; Program Development</span></li><li><i>3</i><span>Market Program for Support Sales</span></li><li><i>4</i><span>Performance Reporting</span></li><li><i>5</i><span>Innovation &amp; Development</span></li></ol></div>'
    '<div><b>Supply Chain</b><ol><li><i>1</i><span>Demand Check</span></li><li><i>2</i><span>Preliminary Drawing Review</span></li><li><i>3</i><span>Request Quote to UTE</span></li><li><i>4</i><span>Close Won → CPO</span></li><li><i>5</i><span>Monitoring</span></li></ol></div>'
    '</div></div>')

# Supply Chain 2/2: approval routes as flows
rep('<li>Close won route: Sales Manager → Marketing Associate → Marketing Manager → GM Marketing</li><li>PO Interco approval: Marketing Manager → GM Marketing → Marketing Director</li></ul></div>',
    '</ul><div class="flw"><div class="lbl">Close Won Route</div><div class="fr"><span>Sales Manager</span><em>→</em><span>Marketing Associate</span><em>→</em><span>Marketing Manager</span><em>→</em><span>GM Marketing</span></div></div>'
    '<div class="flw"><div class="lbl">PO Interco Approval</div><div class="fr"><span>Marketing Manager</span><em>→</em><span>GM Marketing</span><em>→</em><span class="l">Marketing Director</span></div></div></div>')

i = h.rfind("</style>")
h = h[:i] + CSS + h[i:]
h = h.replace("<title>", "<title>Ref5 Bright · ", 1)
open(OUT, "w").write(h)
print("built", OUT)
