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
.cg .ind .n,.ph2 span{color:#fff!important}
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
.opener .osub,.opener .foot,.opener .foot *{color:#5E5A55!important;-webkit-text-fill-color:#5E5A55!important;background:none!important}
.cg .me .tt,.cg .me .tt b{color:#FF5A1F!important}
.site .pin.R,.site .sn.R{background:#fff;color:var(--tx);}
.site .pin.O,.site .sn.O{border:1px solid #bbb}
.site .legend i.O{background:#fff;border:1px solid #bbb}
"""
h = open(SRC).read()
i = h.rfind("</style>")
h = h[:i] + CSS + h[i:]
h = h.replace("<title>", "<title>Ref5 Bright · ", 1)
open(OUT, "w").write(h)
print("built", OUT)
