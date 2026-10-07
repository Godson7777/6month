# Slides 10 and 15 for the Ref4 deck; exec'd by build_ref4_final.py (needs `tri` in scope).
def band(n, label, body):
    return f'<div class="band"><div class="bh"><b>{n}</b><span>{label}</span></div>{body}</div>'

def ul(items, cls=""):
    return f'<ul class="b {cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

sip_rows = [("SUPPLY CHAIN", "s", ["BC / Sales, UTE (Patria), non-Patria vendors, forwarders", "PCR demand, preliminary drawing, PO / PJB, QFD",
             "Quote request → close won → PO Interco → production monitoring → billing", "Quotation, PO Interco, BAST / BAPB, invoice", "Sales team, end customer, Finance"]),
            ("STRATEGIC", "o", ["CRM, sales &amp; GP data, market sources, UTPE", "Market data, competitor specs, price history, GP results",
             "Market study, price analysis, sales programs, GP &amp; PICA reporting", "Market study, CRM price list, sales tools, GP / PICA report", "Management / BOD, Sales team"])]
sip = '<table class="sip2"><tr><th></th>' + "".join(f'<th class="{"pc" if h == "Process" else ""}">{h}</th>' for h in ["Supplier", "Input", "Process", "Output", "Customer"]) + "</tr>"
for lab, c, cells in sip_rows:
    sip += f'<tr><td class="rl {c}">{lab}</td>' + "".join(f'<td class="{"pc" if k == 2 else ""}">{v}</td>' for k, v in enumerate(cells)) + "</tr>"
sip += "</table>"

def ex_table(title, sub, cls, rows):
    body = "".join(f"<tr><td>{a}</td><td>{r}</td></tr>" for a, r in rows)
    return (f'<div class="c side {cls}"><div class="sh"><b>{title}</b><span>{sub}</span></div>'
            f'<table class="ex"><tr><th>Example activities</th><th>End result</th></tr>{body}</table></div>')

# Condensed from the official Position Description (Roles & Responsibilities + End Result)
STRAT = [
 ("Price &amp; market analysis simulation", "Basis for pricing strategy"),
 ("Market data, competitor mapping, new product analysis", "Market size / share, segmentation, positioning &amp; targeting"),
 ("Sales tools, campaigns, seasonal promo, CRM price list, event support", "Sales programs ready for the sales team"),
 ("GP Report, Performance Report, PICA analysis", "Periodic reports for performance evaluation &amp; management decisions"),
 ("Innovation Project Charter, Patria Mover training, site visit report", "Innovation framework; field conditions documented"),
]
SUPPLY = [
 ("Quotation to vendors / third parties; price request (Patria &amp; non-Patria)", "Logistics cost estimate; Patria &amp; non-Patria price info"),
 ("Supporting data for price request &amp; PO", "Complete, accurate data for PO submission"),
 ("Production planning update, cross-team coordination, site / factory visit", "Production issues identified; actual unit condition documented"),
 ("QFD with UTPE, pickup / delivery &amp; LOCO, BAST / BAPB &amp; billing follow-up", "Valid billing documents for invoicing"),
 ("Daily briefing; weekly S&amp;M, production, billing, forecast, QFD &amp; HANSEI meetings", "Coordinated daily agenda &amp; follow-ups"),
]
sides = ('<div class="two">' + ex_table("A. STRATEGIC", "Sets the direction · for management decisions", "o", STRAT)
         + ex_table("B. SUPPLY CHAIN", "Runs the transaction · for operations", "s", SUPPLY) + '</div>')
boxes = ('<div class="three">'
  '<div class="c box"><h4>Dimensions</h4>' + ul(["<b>Financial:</b> non-Patria procurement budget, COGS per unit, target margin per PO", "<b>Non-financial:</b> vendors &amp; customers, documents verified, report frequency, meetings &amp; site visits"]) + '</div>'
  '<div class="c box"><h4>Working Relationships</h4>' + ul(["<b>Internal:</b> Sales &amp; Marketing, Warehouse, Finance &amp; Accounting, Legal, Procurement", "<b>External:</b> customers, Patria &amp; non-Patria vendors, forwarders, UTPE"]) + '</div>'
  '<div class="c box"><h4>Work Challenges</h4>' + ul(["Keep pricing, procurement and report data accurate", "Align many functions on tight, shifting deadlines", "Adapt to changing market and stakeholder needs"]) + '</div></div>')

slide10 = f'''<section class="slide rr2"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span></span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="kick">Section 04 · Roles &amp; Responsibility · B</div>
  <h1 class="t">Strategic vs Supply Chain</h1>
  <div class="bands">{band(1, "Strategic vs Supply Chain", sides)}{band(2, "SIPOC", sip)}{band(3, "Dimensions, Working Relationships &amp; Work Challenges", boxes)}</div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>10</b> / 15</span></div>
</div></section>'''

def chain(steps, last_hl=False):
    return "".join(f'<div class="ck{" hl" if last_hl and k == len(steps) - 1 else ""}"><i>{k+1}</i>{t}</div>' for k, t in enumerate(steps))

ute = ["PO Interco", "PRO", "PR", "PO", "Drawing", "BOM", "LPPB", "PB", "Fabrication", "Assembly", "QC passed", "GR Teco", "GI"]
tri_chain = ["GR", "DO / TO", "GI", "BAST", "BAST approval", "Invoice"]
step4 = ul(["Check PO / prelim / PJB in CRM; request QFD from UTE; collect special requests &amp; painting style from BC", "RFD from QFD becomes the PO Interco due date",
            "Close won: Sales Mgr → Mkt Associate → Mkt Mgr → GM Mkt", "PO Interco approval: Mkt Mgr → GM Mkt → Mkt Director"], "s")
step5 = ul(["Track production &amp; update sales (factory visit or photos from Nandu)", "Match QFD vs actual; escalate when RFD is at risk",
            "Request &amp; monitor painting style ≥1 month before RFD", "Accompany BC at customer FAT"], "s")
slide15 = f'''<section class="slide sc2"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span></span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="kick" style="color:var(--steel)">Section 05 · Job Description Execution · B</div>
  <h1 class="t">Supply Chain (2/2)</h1>
  <div class="pill s">MAIN PROCESS · STEPS 4–5</div>
  <div class="sc2b">
   <div class="two">
    <div class="c sc stp"><div class="sth"><span class="num">4</span><b>Close Won → CPO</b></div>{step4}</div>
    <div class="c sc stp"><div class="sth"><span class="num">5</span><b>Monitoring</b></div>{step5}</div>
   </div>
   <div><div class="lbl">INTERNAL MONITORING</div><div class="mon">
    <div class="c mo"><b>Pipeline–OSPO</b><span>Dashboard, updated monthly</span></div>
    <div class="c mo"><b>CRM Staging Pipeline</b><span>No prelim = early talks; prelim = validate &amp; quote to UTPE</span></div>
    <div class="c mo"><b>Quote Price to UTE</b><span>Detail, average SLA, initial price</span></div>
    <div class="c mo"><b>Progress Billing</b><span>Check staging, escalate</span></div></div></div>
   <div class="bill"><div class="lbl">BILLING PROCESS CHAIN</div>
    <div class="crow"><div class="cl s">AT UTE</div><div class="cks">{chain(ute)}</div></div>
    <div class="crow"><div class="cl o">AT TRIATRA</div><div class="cks">{chain(tri_chain, True)}</div></div>
   </div>
  </div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>15</b> / 15</span></div>
</div></section>'''

TITLES = [
 ('<span>NEDP / MID YEAR REVIEW 2026</span>', '<span></span>'),
 ('<div class="kick">Agenda</div>', '<div class="kick">NEDP Mid Year Review 2026</div>'),
 ('Five Sections Prove I Know the Company,<br>My Products and How I Execute', 'Agenda'),
 ('<div class="kick">Company Group &amp; Business</div>', '<div class="kick">Section 01 · Company Profile</div>'),
 ('<div class="kick">Site Operation &amp; Support</div>', '<div class="kick">Section 02 · Site Operation</div>'),
 ('<h1 class="t">Site Operation</h1>', '<h1 class="t">Site Operation &amp; Support</h1>'),
 ('<div class="kick">Organization Chart</div>', '<div class="kick">Section 03 · Organization Chart</div>'),
 ('Each Associate Owns a Distinct Product Group — Mine Is Small Suppeq and Truck Others', 'Organization Structure'),
 ('<div class="kick">Roles &amp; Responsibility · Position &amp; Products</div>', '<div class="kick">Section 04 · Roles &amp; Responsibility · A</div>'),
 ('I Report Through the Deputy Head and Own Two Product Groups End to End', 'Position &amp; Products'),
 ('<div class="subs" style="top:420px"><div class="a">Strategic</div><div>Supply Chain</div></div>', '<div class="subs" style="top:420px"><div class="a">A — Strategic</div><div>B — Supply Chain</div></div>'),
 ('<div class="kick">Job Description Execution · Strategic (1/2)</div>', '<div class="kick">Section 05 · Job Description Execution · A</div>'),
 ('Strategy Starts With Data: I Frame the Question Before I Read the Market', 'Strategic (1/2)'),
 ('<div class="kick">Job Description Execution · Strategic (2/2)</div>', '<div class="kick">Section 05 · Job Description Execution · A</div>'),
 ('Analysis Only Counts When It Turns Into Tools, Reports and Decisions', 'Strategic (2/2)'),
 ('<div class="kick" style="color:var(--steel)">Job Description Execution · Supply Chain (1/2)</div>', '<div class="kick" style="color:var(--steel)">Section 05 · Job Description Execution · B</div>'),
 ('Before Any Price Goes Out, I Clarify the Demand and Read the Drawing', 'Supply Chain (1/2)'),
]

EXTRA_CSS = """
.pill{top:104px!important}
.rr2 .bands{position:absolute;left:44px;right:44px;top:146px;bottom:40px;display:grid;grid-template-rows:auto auto 1fr;gap:8px}
.band{display:flex;flex-direction:column;gap:7px;min-height:0}
.bh{display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--line);padding-bottom:3px}
.bh b{width:22px;height:22px;border-radius:6px;background:var(--or);color:#fff;display:grid;place-items:center;font-size:12px}
.bh span{font-size:15px;font-weight:600}
.rr2 .two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.rr2 .side{padding:7px 12px}.rr2 .side.o{border-top:2px solid var(--or)}.rr2 .side.s{border-top:2px solid var(--steel)}
.rr2 .sh{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}
.rr2 .sh b{font-size:13px;letter-spacing:.1em}.rr2 .side.o .sh b{color:var(--or)}.rr2 .side.s .sh b{color:var(--steel)}
.rr2 .sh span{font-size:9.5px;color:var(--mut)}
.rr2 .side ul.b{columns:2;font-size:11px}
.ex{width:100%;border-collapse:collapse;font-size:9.6px;line-height:1.3}
.ex th{text-align:left;font-size:8.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);padding:2px 6px 4px 0;font-weight:600}
.ex td{padding:3px 6px 3px 0;border-top:1px solid var(--line);vertical-align:top;color:var(--tx2)}
.ex td:first-child{color:var(--tx);width:54%}
.rr2 .side.s .ex td:first-child{color:var(--tx)}
.sip2{width:100%;border-collapse:collapse;font-size:9.8px;color:var(--tx2)}
.sip2 th{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx);text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}
.sip2 td{padding:4px 8px;border-bottom:1px solid var(--line);line-height:1.35}
.sip2 .pc{background:var(--or-dim);color:var(--tx);font-weight:600;border-left:1px solid var(--or);border-right:1px solid var(--or)}
.sip2 th.pc{color:var(--or)}
.sip2 .rl{font-size:10.5px;font-weight:700;letter-spacing:.08em;width:118px}.sip2 .rl.o{color:var(--or)}.sip2 .rl.s{color:var(--steel)}
.rr2 .three{flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;min-height:0}
.rr2 .box{padding:7px 12px}.rr2 .box h4{font-size:12px;margin-bottom:3px}
.rr2 .box ul.b{font-size:9.8px}.rr2 .box ul.b b{color:var(--tx)}
.sc2b{position:absolute;left:44px;right:44px;top:150px;bottom:42px;display:grid;grid-template-rows:1.25fr auto 1fr;gap:14px}
.sc2 .two{display:grid;grid-template-columns:1fr 1fr;gap:14px;min-height:0}
.sc2 .stp{padding:14px 16px;display:flex;flex-direction:column;gap:10px}
.sth{display:flex;align-items:center;gap:10px}.sth b{font-size:15px}
.sc2 .stp ul.b{font-size:12px;line-height:1.5}
.mon{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.mo{padding:10px 14px;border-left:3px solid var(--steel)!important;display:flex;flex-direction:column;gap:4px}
.mo b{font-size:12.5px}.mo span{font-size:11px;color:var(--tx2);line-height:1.35}
.bill{display:flex;flex-direction:column;gap:10px;min-height:0}
.crow{display:flex;gap:10px;align-items:stretch;flex:1;min-height:0}
.cl{width:100px;flex:none;border-radius:10px;display:grid;place-items:center;font-size:11px;font-weight:700;letter-spacing:.08em;color:#111}
.cl.s{background:var(--steel)}.cl.o{background:var(--or);color:#fff}
.cks{flex:1;display:flex;gap:6px}
.ck{flex:1;border:1px solid var(--line);border-radius:10px;background:rgba(255,255,255,.035);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font-size:11px;font-weight:600;text-align:center;padding:4px}
.ck i{font-style:normal;font-size:9px;color:var(--mut)}
.ck.hl{border-color:var(--or);color:var(--or);background:var(--or-dim)}
"""

# ---------- slide 09: product photos ----------
PROD = [("ft_fuel_truck.webp","Fuel Truck (FT)"),("wt_water_truck_clean.png","Water Truck (WT)"),("lt_lube_truck.webp","Lube Truck (LT)"),
        ("crane_truck_crop.png","Crane Truck"),("mixer_truck.webp","Mixer Truck"),("st_stemming_truck.webp","Stemming Truck")]
def tiles(items):
    return "".join(f'<div class="pp"><img src="{photo("assets/products/" + f, 700)}"><span>{n}</span></div>' for f, n in items)
pgrid = ('<div class="pgrid"><div class="pg pgl">' + tiles(PROD[:3]) + '</div><div class="pdiv"></div>'
         '<div class="pg pgr">' + tiles(PROD[3:]) + '</div></div>')
TITLES.append(('<div class="ev" style="flex:1;margin-top:14px">PRODUCT PHOTOS</div>', pgrid))
EXTRA_CSS += """
.pgrid{flex:1;margin-top:12px;display:grid;grid-template-columns:1fr 2px 1fr;gap:14px;min-height:0}
.pdiv{background:linear-gradient(180deg,transparent,var(--or),transparent)}
.pg{display:grid;gap:8px;min-height:0}.pg.pgl{grid-template-rows:repeat(3,minmax(0,1fr))}
.pg.pgr{grid-template-rows:repeat(3,minmax(0,1fr))}
.pp{position:relative;border-radius:10px;overflow:hidden;border:1px solid var(--line);min-height:0}
.pp{background:#050505}.pp img{width:100%;height:100%;object-fit:cover;object-position:50% 60%;display:block;position:absolute;inset:0}
.pp::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(0,0,0,.8))}
.pp span{position:absolute;left:8px;bottom:6px;z-index:1;font-size:10px;font-weight:600}
"""

# ---------- Job Description Execution (slides 12-15): content from the reviewed PPT ----------
PROD[PROD.index(("mixer_truck.webp", "Mixer Truck"))] = ("mixer_truck_v2.webp", "Mixer Truck")
pgrid = ('<div class="pgrid"><div class="pg pgl">' + tiles(PROD[:3]) + '</div><div class="pdiv"></div>'
         '<div class="pg pgr">' + tiles(PROD[3:]) + '</div></div>')
TITLES[-1] = (TITLES[-1][0], pgrid)
EXTRA_CSS += ".pgr .pp:first-child img{object-fit:contain}\n"

def steps(items, color_cls="", start=1):
    out = ""
    for k, (t, pts) in enumerate(items):
        out += (f'<div class="c jcard {color_cls}"><div class="sth"><span class="num">{start + k}</span><b>{t}</b></div>'
                + ul(pts, "s" if color_cls else "") + '<div class="ev2">EVIDENCE</div></div>')
    return out

def jde(num, kicker, title, pill, cards, cols, bottom, scls=""):
    kstyle = ' style="color:var(--steel)"' if scls else ""
    return f'''<section class="slide jde"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span></span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="kick"{kstyle}>{kicker}</div>
  <h1 class="t">{title}</h1>
  <div class="pill {scls}">{pill}</div>
  <div class="jb"><div class="jcards" style="grid-template-columns:repeat({cols},minmax(0,1fr))">{cards}</div>{bottom}</div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>{num}</b> / 15</span></div>
</div></section>'''

note = lambda t: f'<div class="jnote">{t}</div>'
KA = "Section 05 · Job Description Execution · A"
KB = "Section 05 · Job Description Execution · B"

slide12 = jde(12, KA, "Strategic (1/2)", "STEPS 1–4", steps([
  ("Define Market &amp; Objectives", ["Set the market objective for Small Suppeq and Truck Others", "Use it as the basis for growing market share"]),
  ("Design Market Study Plan", ["Define the scope of the study", "Decide the data collection method and the output expected"]),
  ("Collect Internal &amp; External Data", ["Internal: CRM, sales records, GP report", "External: industry data and competitor information"]),
  ("Analyse Market &amp; Competitors", ["Market size and share, segmentation, positioning and targeting", "Map competitor products and look for new product opportunities"]),
 ]), 4, note("Output of these four steps: a market study that management can act on."))

info = ('<div class="jinfo">' + "".join(f'<div><b>{h}</b><span>{v}</span></div>' for h, v in [
  ("Deliverables", "Market study report, competitor mapping, sales tools, GP and performance report"),
  ("Departments Involved", "Sales, Marketing Communication, Marketing Parts, UTPE, Finance"),
  ("Challenges", "Keeping market data current, validating competitor data, tight timelines"),
  ("Improvements", "Standard report template, automate market data updates, review competitor data regularly")]) + '</div>')
slide13 = jde(13, KA, "Strategic (2/2)", "STEPS 5–8", steps([
  ("Build Sales Tools &amp; Programs", ["Pamphlets, dealer incentive programs, campaigns", "Seasonal promotions and bundling", "Maintain the standard price list in CRM"]),
  ("Prepare Performance Reports", ["Gross Profit report and performance report", "PICA analysis as material for management review"]),
  ("Interpret Results &amp; Recommend", ["Translate research findings into clear conclusions", "Give recommendations that support strategic decisions"]),
  ("Innovation &amp; Development", ["Write the project charter for innovation projects", "Join related training such as Patria Mover", "Run site visits and report what was found"]),
 ], start=5), 4, info)

slide14 = jde(14, KB, "Supply Chain (1/2)", "MAIN PROCESS · STEPS 1–3", steps([
  ("Demand Check", ["Look at which demands are rising in PCR", "Clarify with the Business Consultant why the customer is buying — expansion, new business or replacement",
                    "Check where the project is located", "Check whether the customer wants it fast or cheap", "Check the expected price and when the PO is likely to come"]),
  ("Preliminary Drawing Review", ["Check what the unit does and how it works", "Check the main components and find which ones are critical on price or lead time",
                                  "Consult Application Engineering to understand the unit in more depth"]),
  ("Request Quote to UTE", ["Attach the preliminary drawing, expected price and lead time, end customer name and expected delivery so UTE has the full picture",
                            "Check the standard GP (13.6%, the price before negotiation)", "Check the SLA and escalate if it takes too long", "Enter the quote result into PCR"]),
 ], "sc"), 3, note("The clearer the demand at this stage, the fewer revisions later."), "s")

step4 = ul(["Check the PO, preliminary drawing and PJB in CRM", "Request QFD from UTE and collect special requests and painting style from the Business Consultant",
            "The RFD date from QFD becomes the due date of the PO Interco", "Close won route: Sales Manager → Marketing Associate → Marketing Manager → GM Marketing",
            "PO Interco approval: Marketing Manager → GM Marketing → Marketing Director"], "s")
step5 = ul(["Follow production regularly and update sales — visit the plant or request photos from Nandu", "Compare the QFD plan against actual production",
            "Escalate any production issue that puts the agreed RFD at risk", "Request and track painting style at least one month before RFD",
            "Join the customer FAT together with the Business Consultant"], "s")
MON = [("Pipeline–OSPO Dashboard", "Build it and update it every month."),
       ("Staging Pipeline in CRM", "No preliminary yet means the deal is still far off; once there is one, validate it and request a quote from UTPE."),
       ("Quote Price Dashboard", "Track the detail, average SLA and initial price of quotes from UTE."),
       ("Billing Progress", "Check whether it sits in production, UTE administration or Triatra administration, and escalate any blockage.")]
mon_html = "".join(f'<div class="c mo"><b>{k+1}. {h}</b><span>{d}</span></div>' for k, (h, d) in enumerate(MON))
slide15 = f'''<section class="slide sc2"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span></span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="kick" style="color:var(--steel)">{KB}</div>
  <h1 class="t">Supply Chain (2/2)</h1>
  <div class="pill s">MAIN PROCESS · STEPS 4–5</div>
  <div class="sc2b">
   <div class="two">
    <div class="c sc stp"><div class="sth"><span class="num">4</span><b>Close Won → CPO</b></div>{step4}</div>
    <div class="c sc stp"><div class="sth"><span class="num">5</span><b>Monitoring</b></div>{step5}</div>
   </div>
   <div><div class="lbl">INTERNAL MONITORING</div><div class="mon">{mon_html}</div></div>
   <div class="bill"><div class="lbl">BILLING PROCESS CHAIN</div>
    <div class="crow"><div class="cl s">AT UTE</div><div class="cks">{chain(ute)}</div></div>
    <div class="crow"><div class="cl o">AT TRIATRA</div><div class="cks">{chain(tri_chain, True)}</div></div>
   </div>
  </div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>15</b> / 15</span></div>
</div></section>'''

EXTRA_CSS += """
.jb{position:absolute;left:44px;right:44px;top:150px;bottom:42px;display:flex;flex-direction:column;gap:10px}
.jcards{flex:1;display:grid;gap:12px;min-height:0}
.jcard{padding:12px 14px;display:flex;flex-direction:column;gap:8px;min-height:0}
.jcard ul.b{font-size:11px;line-height:1.45}
.ev2{flex:1;min-height:60px;border:1.5px dashed var(--dash);border-radius:10px;display:grid;place-items:center;font-size:9.5px;letter-spacing:.2em;color:var(--mut)}
.jnote{font-size:12px;color:var(--tx2);border-left:3px solid var(--or);padding:6px 12px}
.jinfo{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.jinfo div{padding:9px 12px;border-right:1px solid var(--line);display:flex;flex-direction:column;gap:3px}.jinfo div:last-child{border-right:none}
.jinfo b{font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--or)}.jinfo span{font-size:10.5px;color:var(--tx2);line-height:1.35}
.sc2b{grid-template-rows:1.35fr auto 0.8fr!important}
.sc2 .stp ul.b{font-size:11px!important;line-height:1.45!important}
"""
