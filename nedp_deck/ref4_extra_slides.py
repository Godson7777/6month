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

# ---------- slide 12: Strategic rebuilt on the 5 Position Description areas ----------
def area_cards(items):
    return "".join(
        f'<div class="c jcard"><div class="sth"><span class="num">{k+1}</span><b>{t}</b></div>'
        f'<div class="pdref">PD {ref}</div>' + ul(pts) +
        f'<div class="endr"><b>END RESULT</b>{er}</div><div class="ev2">EVIDENCE</div></div>'
        for k, (t, ref, pts, er) in enumerate(items))
slide12 = jde(12, KA, "Strategic", "5 AREAS · POSITION DESCRIPTION", area_cards([
  ("Pricing &amp; Market Analysis", "1e", ["Price &amp; market analysis simulation"], "Basis for the pricing strategy"),
  ("Market Study &amp; Program Development", "2a–d", ["Collect market data", "Map competitor products", "Analyse new product development", "Write the market study summary"],
   "Market size / share, segmentation, positioning &amp; targeting"),
  ("Market Program for Support Sales", "3a–f", ["Sales tools: pamphlet, dealer &amp; sales incentive", "Campaign, portfolio &amp; project showcase",
   "Seasonal promo / bundling", "Standard price list in CRM", "Event support (mining expo)"], "Programs ready for the sales team"),
  ("Performance Reporting", "4a", ["Gross Profit (GP) Report", "Performance Report", "PICA analysis"], "Input for performance evaluation &amp; management decisions"),
  ("Innovation &amp; Development", "7a–c", ["Project Charter for innovation projects", "Patria Mover training", "Site visit &amp; visit report"],
   "Innovation framework; field conditions documented"),
 ]), 5, note("Every area is taken from the official Position Description — Marketing Strategic 2 Associate."))
EXTRA_CSS += """
.pdref{font-size:9px;letter-spacing:.12em;color:var(--mut);margin-top:-4px}
.endr{font-size:10.5px;color:var(--tx);border-left:2px solid var(--or);padding:3px 8px;background:var(--or-dim);border-radius:4px;line-height:1.35}
.endr b{display:block;font-size:8.5px;letter-spacing:.14em;color:var(--or)}
.jde .jcards .jcard .sth b{font-size:13px;line-height:1.2}
"""

# ---------- slide 12: no PD refs/note; evidence images for areas 1-2 ----------
EVID = {0: ["s1_a.png", "s1_b.webp", "s1_c.png"], 1: ["s2_a.png", "s2_b.webp"]}
def area_cards(items):
    out = ""
    for k, (t, ref, pts, er) in enumerate(items):
        ev = ('<div class="evimg">' + "".join(f'<img src="{photo("assets/evidence/" + f, 1100)}">' for f in EVID[k]) + '</div>'
              if k in EVID else '<div class="ev2">EVIDENCE</div>')
        out += (f'<div class="c jcard"><div class="sth"><span class="num">{k+1}</span><b>{t}</b></div>' + ul(pts) +
                f'<div class="endr"><b>END RESULT</b>{er}</div>{ev}</div>')
    return out
slide12 = jde(12, KA, "Strategic", "STEPS 1–5", area_cards([
  ("Pricing &amp; Market Analysis", "", ["Price &amp; market analysis simulation"], "Basis for the pricing strategy"),
  ("Market Study &amp; Program Development", "", ["Collect market data", "Map competitor products", "Analyse new product development", "Write the market study summary"],
   "Market size / share, segmentation, positioning &amp; targeting"),
  ("Market Program for Support Sales", "", ["Sales tools: pamphlet, dealer &amp; sales incentive", "Campaign, portfolio &amp; project showcase",
   "Seasonal promo / bundling", "Standard price list in CRM", "Event support (mining expo)"], "Programs ready for the sales team"),
  ("Performance Reporting", "", ["Gross Profit (GP) Report", "Performance Report", "PICA analysis"], "Input for performance evaluation &amp; management decisions"),
  ("Innovation &amp; Development", "", ["Project Charter for innovation projects", "Patria Mover training", "Site visit &amp; visit report"],
   "Innovation framework; field conditions documented"),
 ]), 5, "")
EXTRA_CSS += """
.evimg{flex:1;min-height:0;display:flex;flex-direction:column;gap:5px}
.evimg img{flex:1;min-height:0;width:100%;object-fit:contain;background:#050505;border:1px solid var(--line);border-radius:6px}
"""

# ---------- final Strategic: single slide 12 (slide 13 removed) ----------
EVID = {0: ["s1_a.png", "s1_b.webp", "s1_c.png"], 1: ["s2_a.png", "s2_b.webp"],
        2: ["s3_a.webp", "s3_b.png", "s3_c.webp", "s3_d.png"], 3: ["s4_a.webp", "s4_b.webp"],
        4: ["s5_a.webp", "s5_b.webp", "s5_c.webp"]}
slide12 = jde(12, KA, "Strategic", "STEPS 1–5", area_cards([
  ("Pricing &amp; Market Analysis", "", ["Price &amp; market analysis simulation"], "Basis for the pricing strategy"),
  ("Market Study &amp; Program Development", "", ["Collect market data", "Map competitor products", "Analyse new product development", "Write the market study summary"],
   "Market size / share, segmentation, positioning &amp; targeting"),
  ("Market Program for Support Sales", "", ["Sales tools (pamphlet)", "Campaign, portfolio &amp; project showcase", "Event support (mining expo)"], "Programs ready for the sales team"),
  ("Performance Reporting", "", ["PICA analysis", "Billing report"], "Input for performance evaluation &amp; management decisions"),
  ("Innovation &amp; Development", "", ["Innovation project &amp; development"], "Innovation framework; field conditions documented"),
 ]), 5, info)
DROP_SLIDES = ["13"]
EXTRA_CSS += ".jde .jcard{gap:6px}.jde .jcard ul.b{font-size:10.5px}\n"

# ---------- Supply Chain (1/2) evidence ----------
SC_EV = {"Demand Check": ["sc1_a.png", "sc1_b.webp", "sc1_c.png"], "Preliminary Drawing Review": ["sc2_a.png", "sc2_b.png"],
         "Request Quote to UTE": ["sc3_a.png", "sc3_b.png"]}
def steps(items, color_cls="", start=1):
    out = ""
    for k, (t, pts) in enumerate(items):
        key = t.replace("&amp;", "&")
        ev = ('<div class="evimg evrow">' + "".join(f'<img src="{photo("assets/evidence/" + f, 1100)}">' for f in SC_EV[key]) + '</div>'
              if key in SC_EV else '<div class="ev2">EVIDENCE</div>')
        out += (f'<div class="c jcard {color_cls}"><div class="sth"><span class="num">{start + k}</span><b>{t}</b></div>'
                + ul(pts, "s" if color_cls else "") + ev + '</div>')
    return out
slide14 = jde(14, KB, "Supply Chain (1/2)", "MAIN PROCESS · STEPS 1–3", steps([
  ("Demand Check", ["Look at which demands are rising in PCR", "Clarify with the Business Consultant why the customer is buying — expansion, new business or replacement",
                    "Check where the project is located", "Check whether the customer wants it fast or cheap", "Check the expected price and when the PO is likely to come"]),
  ("Preliminary Drawing Review", ["Check what the unit does and how it works", "Check the main components and find which ones are critical on price or lead time",
                                  "Consult Application Engineering to understand the unit in more depth"]),
  ("Request Quote to UTE", ["Attach the preliminary drawing, expected price and lead time, end customer name and expected delivery so UTE has the full picture",
                            "Check the standard GP (13.6%, the price before negotiation)", "Check the SLA and escalate if it takes too long", "Enter the quote result into PCR"]),
 ], "sc"), 3, "", "s")
EXTRA_CSS += ".evrow{flex-direction:row;flex-wrap:wrap}.evrow img{flex:1 1 45%;min-width:0;height:calc(50% - 3px)}\n"

# ---------- Section 06: Project — F.lli Ferrari crane strategy ----------
TITLES.append(('<span style="font-size:19px;font-weight:700">Job Description Execution</span></div>',
  '<span style="font-size:19px;font-weight:700">Job Description Execution</span></div><div class="c plain" style="display:flex;align-items:center;gap:22px;padding:14px 20px"><span style="font:700 30px var(--mono);color:var(--or)">06</span><span style="font-size:19px;font-weight:700">Project — F.lli Ferrari Crane Strategy</span></div>'))
EXTRA_CSS += ".agenda-fix{}\n"
KP = "Section 06 · Project · F.lli Ferrari Crane Strategy"
def pslide(title, body, extra_cls=""):
    return f'''<section class="slide prj {extra_cls}"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span></span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="kick">{KP}</div><h1 class="t">{title}</h1><div class="pb">{body}</div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>00</b> / 15</span></div></div></section>'''
def kpi(n, l, hl=False): return f'<div class="c kpi{" me" if hl else ""}"><b>{n}</b><span>{l}</span></div>'
p_div = f'''<section class="slide div"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span></span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="big">06</div><div class="sec">SECTION 06</div><h2>Project</h2>
  <div class="subs" style="top:410px"><div class="a">F.lli Ferrari Crane Strategy</div><div>Truck-mounted knuckle boom crane · Indonesia</div></div><div class="haz"></div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>00</b> / 15</span></div></div></section>'''
p1 = pslide("Background &amp; Market Size", f'''
 <div class="pg2"><div>
  <div class="lbl">PROJECT BACKGROUND</div>
  <div class="c pbox"><ul class="b">
   <li><b>Goal:</b> find where F.lli Ferrari truck-mounted cranes can win in Indonesia, and which models to stock</li>
   <li><b>Data:</b> Indonesia import records (HS 84269100 + 84264900), Jan 2023 – 14 Aug 2026; Zoomlion &amp; Hyva excluded</li>
   <li><b>Method:</b> size the market by lifting class (Light / Small / Medium / Heavy), find brand &amp; model leaders, then compare price head to head per 5-tm class</li>
   <li><b>Price basis:</b> competitor import price + duty + PPN + PPh 22 vs F.lli Ferrari TSP price list, before distributor margin</li></ul></div>
  <div class="lbl" style="margin-top:12px">WHY MEDIUM &amp; HEAVY (&gt; 25 tm)</div>
  <div class="kpis">{kpi("41%","of units")}{kpi("64%","of import value", True)}{kpi("Rp 803 Jt","avg value / unit vs Rp 311 Jt Light+Small")}{kpi("67 / yr","Medium + Heavy units")}</div>
 </div><div>
  <div class="lbl">EVIDENCE · MARKET SIZE BY CLASS</div>
  <div class="evbig"><img src="{photo("assets/evidence/s1_a.png", 1400)}"></div>
  <div class="lbl" style="margin-top:12px">TOTAL 2023 – 14 AUG 2026</div>
  <div class="kpis">{kpi("638","units imported")}{kpi("Rp 326,8 M","import value (IDR)")}</div>
 </div></div>''')
p2 = pslide("Competitor Landscape &amp; Price Comparison", f'''
 <div class="pg2"><div>
  <div class="lbl">BRAND LEADERS · 2025</div>
  <div class="c pbox"><ul class="b">
   <li><b>Medium (25–45 tm):</b> Sany Palfinger leads with 47% of value (30 units), then XCMG and Palfinger</li>
   <li><b>Heavy (&gt; 45 tm):</b> Palfinger leads with 62% of value; PK 53002 alone is 63% of Heavy units</li>
   <li>Each leader relies on one main model, so one well-priced alternative can take share</li></ul></div>
  <div class="lbl" style="margin-top:12px">HEAD-TO-HEAD: WHERE F.LLI FERRARI IS CHEAPER</div>
  <table class="ptab"><tr><th>Class</th><th>Cheaper head to head on</th><th>Units</th></tr>
   <tr><td>Medium 25–35 tm</td><td>Amco Veba V825, Hiab X-CLX 388 / 328</td><td>41 of 111</td></tr>
   <tr><td>Medium 35–45 tm</td><td>Palfinger PK 41002</td><td>21 of 85</td></tr>
   <tr><td>Heavy 45–90 tm</td><td>Amco Veba V950, Hiab X-HIPRO B58, Fassi F485RA</td><td>14 of 65</td></tr></table>
 </div><div>
  <div class="lbl">EVIDENCE · PRICE COMPARISON (HEAVY)</div>
  <div class="evbig"><img src="{photo("assets/evidence/s1_c.png", 1400)}"></div>
 </div></div>''')
CR = [("268 A4","25.4 tm","31","Amco Veba V825","−23%"),("7441C*","37.7 tm","21","Palfinger PK 41002","−14%"),
      ("FBR450R A4","45.5 tm","13","Amco Veba V950 / Fassi F485RA","−32% / −16%"),("FBR350R A4","32.8 tm","10","Hiab X-CLX 388 / 328","−25% / −2%"),
      ("9601CR A8","50.7 tm","1","Hiab X-HIPRO B58","−3%")]
cards = "".join(f'<div class="c crc"><div class="crh"><b>{m}</b><span>{t}</span></div><div class="crn">{u}<small>units won</small></div><div class="crl">CHEAPER THAN</div><div class="crv">{c} <i>{d}</i></div></div>' for m,t,u,c,d in CR)
p3 = pslide("Recommendation &amp; Next Steps", f'''
 <div class="lbl">STOCK THE FIVE F.LLI FERRARI CRANES THAT WIN ON PRICE · SAME SIZE OR BIGGER, LOWER PRICE</div>
 <div class="crs">{cards}</div>
 <div class="pg3">
  <div class="c pbox"><h4>Opportunity</h4><ul class="b"><li>76 competitor units (2023 – Aug 2026) were in classes where a cheaper, same-size F.lli Ferrari exists</li><li>Focus on Medium &amp; Heavy: fewer units, most of the value</li></ul></div>
  <div class="c pbox"><h4>Next Steps</h4><ul class="b"><li>Confirm price for 7441C (estimate) and 9661C (not yet known)</li><li>Set stock plan &amp; lead time with UTPE / TSP</li><li>Build sales tools and target customers of V825, PK 41002 and V950</li></ul></div>
  <div class="c pbox"><h4>Notes</h4><ul class="b"><li>No F.lli Ferrari model above 74 tm (80–90 tm class)</li><li>2026 data is partial (Jan – 14 Aug)</li><li>Prices rounded to Rp 10.000.000</li></ul></div>
 </div>''')
PROJECT = [p_div, p1, p2, p3]
EXTRA_CSS += """
.pb{position:absolute;left:44px;right:44px;top:150px;bottom:42px;display:flex;flex-direction:column;gap:10px}
.pg2{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:20px;min-height:0}.pg2>div{display:flex;flex-direction:column;min-height:0}
.pbox{padding:10px 14px}.pbox ul.b{font-size:11px;line-height:1.45}.pbox ul.b b{color:var(--tx)}.pbox h4{font-size:12.5px;margin-bottom:5px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(0,1fr));gap:8px}
.kpi{padding:10px 12px;display:flex;flex-direction:column;gap:3px}.kpi b{font-size:22px;color:var(--or)}.kpi span{font-size:10px;color:var(--tx2);line-height:1.3}
.evbig{flex:1;min-height:0;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#050505}.evbig img{width:100%;height:100%;object-fit:contain;display:block}
.ptab{width:100%;border-collapse:collapse;font-size:11px}.ptab th{text-align:left;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);padding:5px 8px;border-bottom:1px solid var(--line)}
.ptab td{padding:7px 8px;border-bottom:1px solid var(--line);color:var(--tx2)}.ptab td:last-child{color:var(--or);font-weight:600;white-space:nowrap}
.crs{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}
.crc{padding:12px 14px;border-top:3px solid var(--or)}.crh{display:flex;justify-content:space-between;align-items:baseline}.crh b{font-size:14px}.crh span{font-size:11px;color:var(--tx2)}
.crn{font-size:40px;font-weight:700;color:var(--or);line-height:1.1;margin-top:6px}.crn small{font-size:11px;color:var(--tx2);font-weight:400;margin-left:6px}
.crl{font-size:9px;letter-spacing:.14em;color:var(--mut);margin-top:8px;border-top:1px solid var(--line);padding-top:6px}
.crv{font-size:11px;margin-top:4px}.crv i{font-style:normal;color:#5bd17a;font-weight:600;float:right}
.pg3{flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:10px;min-height:0}
"""

# ---------- Section 06 Project: all slides of the F.lli Ferrari study, re-framed ----------
def islide(title, img):
    return pslide(title, f'<div class="evbig full"><img src="{photo("assets/project/" + img, 1800)}"></div>')
PROJ_SLIDES = [
 ("Market Size by Class", "p02.png"), ("Brand Leaders · 2025", "p04.png"), ("Models of the Brand Leaders · 2025", "p05.png"),
 ("Price Comparison · Medium 25–35 tm", "p07.png"), ("Price Comparison · Medium 35–45 tm", "p08.png"),
 ("Price Comparison · Heavy 45–90 tm", "p09.png"), ("F.lli Ferrari Crane Advantage", "p10.png"),
 ("Appendix · Model Photos · Medium", "p11.png"), ("Appendix · Model Photos · Heavy &amp; F.lli Ferrari", "p12.png")]
p_close = pslide("Project Summary &amp; Next Steps", '''
 <div class="pg3" style="grid-template-columns:repeat(4,1fr)">
  <div class="c pbox"><h4>Background</h4><ul class="b"><li><b>Goal:</b> find where F.lli Ferrari truck-mounted cranes can win in Indonesia and which models to stock</li><li><b>Data:</b> import records HS 84269100 + 84264900, Jan 2023 – 14 Aug 2026; Zoomlion &amp; Hyva excluded</li><li><b>Method:</b> market size by class → brand &amp; model leaders → head-to-head price per 5-tm class</li></ul></div>
  <div class="c pbox"><h4>Key Findings</h4><ul class="b"><li>Medium &amp; Heavy = 41% of units, 64% of value</li><li>Leaders depend on one main model (Sany Palfinger, Palfinger PK 53002)</li><li>Five F.lli Ferrari cranes are same size or bigger and cheaper: 268 A4, 7441C, FBR450R A4, FBR350R A4, 9601CR A8</li></ul></div>
  <div class="c pbox"><h4>Next Steps</h4><ul class="b"><li>Confirm price for 7441C (estimate) and 9661C (not yet known)</li><li>Set stock plan &amp; lead time with UTPE / TSP</li><li>Build sales tools and target customers of V825, PK 41002 and V950</li></ul></div>
  <div class="c pbox"><h4>Notes</h4><ul class="b"><li>No F.lli Ferrari model above 74 tm</li><li>2026 data is partial (Jan – 14 Aug)</li><li>Prices before distributor margin, rounded to Rp 10.000.000</li></ul></div>
 </div>''')
PROJECT = [p_div] + [islide(t, f) for t, f in PROJ_SLIDES] + [p_close]
EXTRA_CSS += ".evbig.full{flex:1;background:#0d1117}\n"

EXTRA_CSS += ".prj .pg3{flex:none;align-items:start}.prj .pbox ul.b{font-size:12px}\n"

SC_EV["Request Quote to UTE"].append("sc3_c.png")
SC_EV["Preliminary Drawing Review"] += ["sc2_c.webp", "sc2_d.png"]
slide14 = jde(14, KB, "Supply Chain (1/2)", "MAIN PROCESS · STEPS 1–3", steps([
  ("Demand Check", ["Look at which demands are rising in PCR", "Clarify with the Business Consultant why the customer is buying — expansion, new business or replacement",
                    "Check where the project is located", "Check whether the customer wants it fast or cheap", "Check the expected price and when the PO is likely to come"]),
  ("Preliminary Drawing Review", ["Check what the unit does and how it works", "Check the main components and find which ones are critical on price or lead time",
                                  "Consult Application Engineering to understand the unit in more depth"]),
  ("Request Quote to UTE", ["Attach the preliminary drawing, expected price and lead time, end customer name and expected delivery so UTE has the full picture",
                            "Check the standard GP (13.6%, the price before negotiation)", "Check the SLA and escalate if it takes too long", "Enter the quote result into PCR"]),
 ], "sc"), 3, "", "s")
PROJECT = PROJECT[:-1]  # summary slide removed

# ===================== Section 06 Project: native redesign (tables/bars = editable in PPT) =====================
def bars(series, cats, colors, maxv):
    out = '<div class="vbars">'
    for ci, c in enumerate(cats):
        out += '<div class="vgrp"><div class="vcols">' + "".join(
            f'<div class="vcol" style="height:{v/maxv*100:.0f}%;background:{colors[si]}"><span>{v:.0f}</span></div>'
            for si, (_, vals) in enumerate(series) for v in [vals[ci]]) + f'</div><div class="vlab">{c}</div></div>'
    return out + '</div>'
def legend(names, colors):
    return '<div class="leg">' + "".join(f'<span><i style="background:{c}"></i>{n}</span>' for n, c in zip(names, colors)) + '</div>'
def table(head, rows, hl=None, cls="dt"):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join(f'<tr class="{(hl or {}).get(r[0], "")}">' + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><tr>{h}</tr>{b}</table>'

CLS_C = ["#5b6470", "#9aa3ad", "#FF8A3D", "#4da3ff"]
CLS_N = ["Light (≤ 8 tm)", "Small (8–25 tm)", "Medium (25–45 tm)", "Heavy (> 45 tm)"]
units = [("Light", [54, 49, 40, 55]), ("Small", [56, 51, 66, 43]), ("Medium", [71, 59, 54, 19]), ("Heavy", [12, 17, 35, 2])]
q1 = pslide("Market Size by Class", f'''
 <div class="pg2" style="grid-template-columns:1.25fr 1fr"><div>
  <div class="lbl">UNITS IMPORTED PER YEAR BY CLASS · 2023 – 2026*</div>{legend(CLS_N, CLS_C)}
  {bars(units, ["2023", "2024", "2025", "2026*"], CLS_C, 75)}
  <div class="lbl" style="margin-top:10px">TOTAL UNITS &amp; IMPORT VALUE · 2023 – 14 AUG 2026</div>
  {table(["Class", "Lifting moment", "Units", "Import value (IDR)", "Share"], [
    ["Light", "≤ 8 tm", "177", "Rp 40.118.000.000", "12%"], ["Small", "8 – 25 tm", "200", "Rp 77.241.000.000", "24%"],
    ["Medium", "25 – 45 tm", "196", "Rp 118.328.000.000", "36%"], ["Heavy", "> 45 tm", "65", "Rp 91.154.000.000", "28%"],
    ["Total", "", "638", "Rp 326.841.000.000", "100%"]], {"Medium": "or", "Heavy": "bl", "Total": "tot"})}
 </div><div>
  <div class="lbl">AVERAGE UNITS PER YEAR</div>
  <div class="kpis">{kpi("67", "Medium + Heavy · target classes", True)}{kpi("104", "Light + Small · non-target")}</div>
  <div class="lbl" style="margin-top:12px">KEY POINTS</div>
  <div class="c pbox"><ul class="b">
   <li><b>Medium + Heavy:</b> 41% of units, 64% of import value</li>
   <li><b>Value per unit:</b> Rp 803 Jt vs Rp 311 Jt for Light + Small</li>
   <li><b>Use:</b> 88% of Medium &amp; Heavy cranes need a truck GVW ≥ 24 t — mining, construction, heavy logistics</li>
   <li><b>2026 is partial:</b> only 12 Medium and 1 Heavy unit to 14 Aug; import records may be incomplete</li></ul></div>
  <div class="src">*2026 annualised (Jan – 14 Aug × 1.61). Source: Indonesia import records HS 84269100 + 84264900; truck-mounted knuckle boom cranes; Zoomlion &amp; Hyva excluded; USD 1 = Rp 17.803.</div>
 </div></div>''')

def hbars(rows, color, maxv):
    return '<div class="hb">' + "".join(f'<div class="hbr"><span class="hn">{n}</span><div class="hbt"><div style="width:{u/maxv*100:.0f}%;background:{color if k==len(rows)-1 else "#4a4a4a"}"></div></div><span class="hv">{u} · {v}</span></div>'
                                      for k, (n, u, v) in enumerate(rows)) + '</div>'
q2 = pslide("Brand Leaders · 2025", f'''
 <div class="pg2"><div>
  <div class="ctag or">MEDIUM · 25 – 45 tm</div>
  <div class="lbl">UNITS &amp; IMPORT VALUE BY BRAND · 2025</div>
  {hbars([("Amco Veba", 5, "Rp 2,7 M"), ("Palfinger", 5, "Rp 4,9 M"), ("XCMG", 14, "Rp 7,2 M"), ("Sany Palfinger", 30, "Rp 13,2 M")], "#FF8A3D", 30)}
  {table(["#", "Brand", "Units", "Import value (IDR)", "Share"], [["1", "Sany Palfinger", "30", "Rp 13.226.000.000", "47%"], ["2", "XCMG", "14", "Rp 7.197.000.000", "26%"], ["3", "Palfinger", "5", "Rp 4.869.000.000", "17%"]], {"1": "or"})}
  <div class="note2">Total Medium 2025: 54 units · Rp 28,0 M</div>
 </div><div>
  <div class="ctag bl">HEAVY · &gt; 45 tm</div>
  <div class="lbl">UNITS &amp; IMPORT VALUE BY BRAND · 2025</div>
  {hbars([("XCMG", 4, "Rp 4,6 M"), ("Amco Veba", 7, "Rp 11,1 M"), ("Palfinger", 22, "Rp 29,7 M")], "#4da3ff", 30)}
  {table(["#", "Brand", "Units", "Import value (IDR)", "Share"], [["1", "Palfinger", "22", "Rp 29.738.000.000", "62%"], ["2", "Amco Veba", "7", "Rp 11.065.000.000", "23%"], ["3", "XCMG", "4", "Rp 4.647.000.000", "10%"]], {"1": "bl"})}
  <div class="note2">Total Heavy 2025: 35 units · Rp 48,0 M. Sany Palfinger = Sany–Palfinger JV, made in China.</div><div class="c pbox" style="margin-top:12px"><ul class="b"><li>Both leaders are well ahead of the next brand in value</li><li>Scope: 2025 only, so figures are smaller than the 2023 – 2026 totals</li></ul></div>
 </div></div>''')

MODELS = [("Sany Palfinger", "or", [("SPK36080 · 36 tm", 14), ("SPK42502 · 42.5 tm", 6), ("SPK32080 · 30.4 tm", 6)]),
          ("XCMG", "or", [("GSQZ330.4 · 33 tm", 4), ("SQZ325.4 · 32.5 tm", 3), ("KSQZ300.3 · 30 tm", 3)]),
          ("Palfinger", "or", [("PK 32080 C · 30.4 tm", 4), ("PK 41002 EH C · 38.4 tm", 1)]),
          ("Palfinger", "bl", [("PK 53002 SH B · 50.1 tm", 22)]), ("Amco Veba", "bl", [("V950 · 45.9 tm", 7)]),
          ("XCMG", "bl", [("GSQZ880.6 · 88 tm", 2), ("GSQZ860.6 · 86 tm", 2)])]
def mcard(b, c, rows):
    mx = max(u for _, u in rows); col = "#FF8A3D" if c == "or" else "#4da3ff"
    return (f'<div class="c mcard"><b>{b}</b>' + "".join(f'<div class="hbr"><span class="hn">{n}</span><div class="hbt"><div style="width:{u/mx*100:.0f}%;background:{col if k==0 else "#4a4a4a"}"></div></div><span class="hv">{u}</span></div>' for k, (n, u) in enumerate(rows)) + '</div>')
q3 = pslide("Models of the Brand Leaders · 2025", f'''
 <div class="ctag or">MEDIUM · 25 – 45 tm · units sold by model</div><div class="mrow">{"".join(mcard(*m) for m in MODELS[:3])}</div>
 <div class="ctag bl">HEAVY · &gt; 45 tm · units sold by model</div><div class="mrow">{"".join(mcard(*m) for m in MODELS[3:])}</div>
 <div class="c pbox"><ul class="b"><li>Each leader relies on one main model; <b>PK 53002 alone is 63% of Heavy units</b> in 2025</li></ul></div>''')

def pcell(x):
    if not x: return '<td></td>'
    m, d, spec, price = x
    k = "g" if d.startswith("−") else ("r" if d.startswith("+") else "nn")
    return f'<td class="{k}"><b>{m}</b> <em>{d}</em><br><span>{spec}</span><br><span>{price}</span></td>'
def ptable(brands, rows):
    h = '<tr><th>tm class</th><th class="ff">F.lli Ferrari</th>' + "".join(f"<th>{b}<br><span>{u}</span></th>" for b, u in brands) + '</tr>'
    body = ""
    for cls, ff, cells in rows:
        body += f'<tr><td class="tc">{cls}</td><td class="ffc">{ff}</td>' + "".join(pcell(c) for c in cells) + "</tr>"
    return f'<table class="pt">{h}{body}</table>'
PLEG = '<div class="leg"><span><i style="background:#1f5f35"></i>F.lli Ferrari cheaper</span><span><i style="background:#6b2222"></i>F.lli Ferrari more expensive</span><span><i style="background:#3a3a3a"></i>About the same (±0%)</span></div>'
PSRC = '<div class="src">Competitor: highest import unit price 2023 – 14 Aug 2026 × Rp 17.803/USD + import duty + PPN 11% + PPh 22 2.5%, before distributor margin. F.lli Ferrari: TSP price list Rev1 (Jun 2026) less 13.6% margin and 3% warranty. Rounded to Rp 10 Jt.</div>'
ML = lambda *a: "<br>".join(a)
q4 = pslide("Price Comparison · Medium 25 – 35 tm", PLEG + ptable(
  [("Sany Palfinger", "88 units"), ("Amco Veba", "36 units"), ("XCMG", "33 units"), ("Palfinger", "29 units"), ("Hiab", "10 units")], [
  (ML("&gt;25–30 tm", "49 units"), ML("<b>268 A4</b>", "25.4 tm", "Rp 500 Jt"), [None, ("V825", "−23%", "25.6 tm · 31 units", "Rp 650 Jt"),
     ("KSQZ300.3", "−3%", "30 tm · 15 units · smaller crane", "Rp 510 Jt"), None, None]),
  ("", "", [None, None, ("SQ12ZK3Q", "±0%", "30 tm · 2 units", "Rp 500 Jt"), None, None]),
  ("", "", [None, None, ("KSQZ300.4", "−12%", "30 tm · 1 unit · smaller crane", "Rp 570 Jt"), None, None]),
  (ML("&gt;30–35 tm", "62 units"), ML("<b>FBR350R A4</b>", "32.8 tm", "Rp 1.090 Jt"), [("SPK32080", "+107%", "30.4 tm · 33 units", "Rp 530 Jt"),
     ("V933", "+30%", "31.9 tm · 4 units", "Rp 840 Jt"), ("GSQZ330.4", "+40%", "33 tm · 4 units", "Rp 780 Jt"),
     ("PK 32080 C", "±0%", "30.4 tm · 8 units", "Rp 1.090 Jt"), ("X-CLX 388", "−25%", "34.3 tm · 9 units", "Rp 1.460 Jt")]),
  ("", "", [None, None, ("SQZ325.4", "+98%", "32.5 tm · 3 units", "Rp 550 Jt"), None, ("X-CLX 328", "−2%", "30.3 tm · 1 unit", "Rp 1.120 Jt")]),
 ]) + PSRC)
q5 = pslide("Price Comparison · Medium 35 – 45 tm", PLEG + ptable(
  [("Sany Palfinger", "88 units"), ("Amco Veba", "36 units"), ("XCMG", "33 units"), ("Palfinger", "29 units")], [
  (ML("&gt;35–40 tm", "66 units"), ML("<b>7441C</b>", "37.7 tm · estimate", "Rp 1.240 Jt"), [("SPK36080", "+88%", "36 tm · 37 units", "Rp 660 Jt"), None,
     ("KSQZ400.4", "+66%", "40 tm · 2 units", "Rp 750 Jt"), ("PK 41002", "−14%", "38.4 tm · 21 units", "Rp 1.440 Jt")]),
  ("", "", [None, None, ("GSQZ400.4", "+76%", "40 tm · 2 units", "Rp 700 Jt"), None]),
  ("", "", [None, None, ("SQZ365.4", "+107%", "36.5 tm · 2 units", "Rp 600 Jt"), None]),
  ("", "", [None, None, ("SQZ400", "+109%", "40 tm · 1 unit", "Rp 600 Jt"), None]),
  ("", "", [None, None, ("KSQZ365.4", "+129%", "36.5 tm · 1 unit", "Rp 540 Jt"), None]),
  (ML("&gt;40–45 tm", "19 units"), ML("<b>746 A4</b>", "43.4 tm", "Rp 1.420 Jt"), [("SPK42502", "+48%", "42.5 tm · 18 units", "Rp 960 Jt"),
     ("V946B", "+12%", "44.2 tm · 1 unit", "Rp 1.270 Jt"), None, None]),
 ]) + PSRC)
q6 = pslide("Price Comparison · Heavy 45 – 90 tm", PLEG + ptable(
  [("Palfinger", "42 units"), ("Amco Veba", "12 units"), ("XCMG", "7 units"), ("Hiab", "2 units"), ("Fassi", "1 unit"), ("Sany Palfinger", "1 unit")], [
  (ML("&gt;45–50 tm", "17 units"), ML("<b>FBR450R A4</b>", "45.5 tm", "Rp 1.350 Jt"), [None, ("V950", "−32%", "45.9 tm · 12 units", "Rp 1.990 Jt"),
     ("GSQZ460.4", "+66%", "46 tm · 3 units", "Rp 810 Jt"), ("EFFER 525H", "−10%", "50 tm · 1 unit · smaller crane", "Rp 1.510 Jt"), ("F485RA.2.23", "−16%", "47 tm · 1 unit", "Rp 1.610 Jt"), None]),
  (ML("&gt;50–55 tm", "40 units"), ML("<b>9601CR A8</b>", "50.7 tm", "Rp 3.260 Jt"), [("PK 53002", "+85%", "50.1 tm · 39 units", "Rp 1.760 Jt"), None, None,
     ("X-HIPRO B58", "−3%", "50.93 tm · 1 unit", "Rp 3.370 Jt"), None, None]),
  (ML("&gt;55–60 tm", "0 units"), ML("<b>FBR660R A4</b>", "58.8 tm", "Rp 2.030 Jt"), [None] * 6),
  (ML("&gt;60–65 tm", "1 unit"), ML("<b>9661C</b>", "63.2 tm", "Price not yet known"), [None] * 5 + [("SPK61502", "no price", "61.5 tm · 1 unit", "Rp 1.400 Jt")]),
  (ML("&gt;70–75 tm", "2 units"), ML("<b>990R</b>", "74 tm", "Rp 4.110 Jt"), [("PK 76002 EH D", "+80%", "71.6 tm · 2 units", "Rp 2.290 Jt")] + [None] * 5),
  (ML("&gt;80–85 tm", "1 unit"), "No F.lli Ferrari model", [("PK 88002 EH C", "+85%", "81.6 tm · 1 unit", "Rp 2.220 Jt")] + [None] * 5),
  (ML("&gt;85–90 tm", "4 units"), "No F.lli Ferrari model", [None, None, ("GSQZ880.6 / 860.6", "+211%", "86–88 tm · 4 units", "Rp 1.320 Jt")] + [None] * 3),
 ]) + PSRC)
CR2 = [("268 A4", "25.4 tm", "31", [("Amco Veba V825 · 31", "−23%")]), ("7441C*", "37.7 tm", "21", [("Palfinger PK 41002 · 21", "−14%")]),
       ("FBR450R A4", "45.5 tm", "13", [("Amco Veba V950 · 12", "−32%"), ("Fassi F485RA.2.23 · 1", "−16%")]),
       ("FBR350R A4", "32.8 tm", "10", [("Hiab X-CLX 388 · 9", "−25%"), ("Hiab X-CLX 328 · 1", "−2%")]), ("9601CR A8", "50.7 tm", "1", [("Hiab X-HIPRO B58 · 1", "−3%")])]
cc = "".join(f'<div class="c crc"><img src="{photo(f"assets/project/crane{k}.png", 500)}"><div class="crh"><b>{m}</b><span>{t}</span></div><div class="crn">{u}<small>units won</small></div><div class="crl">CHEAPER THAN</div>'
             + "".join(f'<div class="crv">{c} <i>{d}</i></div>' for c, d in vs) + '</div>' for k, (m, t, u, vs) in enumerate(CR2))
q7 = pslide("F.lli Ferrari Crane Advantage", f'''
 <div class="lbl">FIVE F.LLI FERRARI CRANES · SAME SIZE OR BIGGER AND LOWER PRICE THAN THESE COMPETITORS · JAN 2023 – 14 AUG 2026</div>
 <div class="crs crs2">{cc}</div>
 <div class="src">Units won = imports of the rival model. Head to head = F.lli Ferrari cheaper and not more than 2 tm smaller. *7441C price is an estimate.</div>''')
qa1 = islide("Appendix · Model Photos · Medium", "p11.png")
qa2 = islide("Appendix · Model Photos · Heavy &amp; F.lli Ferrari", "p12.png")
q6 = q6.replace('class="pt"', 'class="pt tight"')
PROJECT = [p_div, q1, q2, q3, q4, q5, q6, q7, qa1, qa2]
EXTRA_CSS += """
.leg{display:flex;gap:14px;font-size:10px;color:var(--tx2);margin:2px 0 6px}.leg i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.vbars{display:flex;gap:18px;height:170px;align-items:flex-end;border-bottom:1px solid var(--line);padding:0 6px}
.vgrp{flex:1;display:flex;flex-direction:column;height:100%}.vcols{flex:1;display:flex;align-items:flex-end;gap:3px}
.vcol{flex:1;position:relative;border-radius:3px 3px 0 0}.vcol span{position:absolute;top:-14px;left:0;right:0;text-align:center;font-size:9px;color:var(--tx2)}
.vlab{text-align:center;font-size:10px;color:var(--tx2);padding-top:4px}
.dt{width:100%;border-collapse:collapse;font-size:10.5px}.dt th{text-align:left;font-size:9px;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);padding:5px 8px;border-bottom:1px solid var(--line)}
.dt td{padding:5px 8px;border-bottom:1px solid var(--line);color:var(--tx2)}.dt tr.or td{color:#FF8A3D;font-weight:600}.dt tr.bl td{color:#4da3ff;font-weight:600}.dt tr.tot td{color:var(--tx);font-weight:700}
.src{font-size:8.5px;color:var(--mut);line-height:1.35;margin-top:6px}
.ctag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.1em;padding:3px 10px;border-radius:999px;margin-bottom:6px;color:#111}.ctag.or{background:#FF8A3D}.ctag.bl{background:#4da3ff}
.hb{display:flex;flex-direction:column;gap:6px;margin:4px 0 10px}.hbr{display:grid;grid-template-columns:150px 1fr 90px;gap:8px;align-items:center;font-size:10.5px}
.hn{color:var(--tx)}.hv{color:var(--tx2);font-size:10px}.hbt{height:12px;background:rgba(255,255,255,.05);border-radius:3px;overflow:hidden}.hbt div{height:100%}
.note2{font-size:10px;color:var(--tx2);margin-top:6px}
.mrow{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:8px}.mcard{padding:10px 12px;display:flex;flex-direction:column;gap:5px}.mcard>b{font-size:12px;margin-bottom:2px}
.mcard .hbr{grid-template-columns:130px 1fr 24px}
.pt{width:100%;border-collapse:collapse;font-size:9.6px;table-layout:fixed}.pt th{background:#1a1a1a;color:var(--tx);font-size:10px;padding:5px;border:1px solid #2a2a2a}.pt th span{color:var(--mut);font-weight:400;font-size:9px}
.pt th.ff{background:#b3261e}.pt td{border:1px solid #2a2a2a;padding:4px 6px;vertical-align:top;line-height:1.3;color:var(--tx2)}
.pt td b{color:var(--tx)}.pt td em{font-style:normal;font-weight:700}.pt td.g{background:#1f3d2a}.pt td.g em{color:#5bd17a}.pt td.r{background:#3d1f1f}.pt td.r em{color:#ff8a8a}.pt td.nn{background:#2a2a2a}.pt td.nn em{color:#ddd}
.pt td.tc{color:#4da3ff;font-weight:600;text-align:center}.pt td.ffc{background:#3a1512;color:var(--tx)}
.crs2 .crc img{width:100%;height:120px;object-fit:cover;border-radius:8px;margin-bottom:8px}.crs2{flex:1}.crs2 .crv{margin-top:6px}
"""

EXTRA_CSS += """
.prj .pb{gap:12px}
.pt{font-size:11.5px}.pt th{font-size:11.5px;padding:8px 6px}.pt td{padding:8px 8px;line-height:1.4}
.vbars{height:250px}.vcol span{font-size:11px}.vlab{font-size:12px}
.dt{font-size:12px}.dt td{padding:7px 8px}.dt th{font-size:10px}
.hb{gap:10px}.hbr{font-size:12.5px;grid-template-columns:160px 1fr 110px}.hbt{height:18px}.hv{font-size:11.5px}
.mrow{gap:14px;margin-bottom:14px}.mcard{padding:16px 18px;gap:10px}.mcard>b{font-size:15px}.mcard .hbr{grid-template-columns:170px 1fr 28px}
.prj .pbox ul.b{font-size:13px}.kpi b{font-size:30px}.kpi span{font-size:11.5px}
.crs2 .crc{display:flex;flex-direction:column}.crs2 .crc img{height:200px}.crs2 .crn{font-size:52px}.crs2 .crv{font-size:12.5px}.crs2 .crh b{font-size:16px}
.ctag{font-size:11.5px;padding:4px 12px}.note2{font-size:11.5px}.src{font-size:9.5px}
"""
EXTRA_CSS += ".pt.tight td{padding:4px 7px;line-height:1.3}.pt.tight{font-size:10.8px}\n"

# ---------- slide 10 aligned with slides 12-14; new work challenges ----------
STRAT = [
 ("Pricing &amp; Market Analysis: price &amp; market analysis simulation", "Basis for the pricing strategy"),
 ("Market Study &amp; Program Development: market data, competitor mapping, new product analysis, summary", "Market size / share, segmentation, positioning &amp; targeting"),
 ("Market Program for Support Sales: sales tools (pamphlet), campaign &amp; project showcase, event support", "Programs ready for the sales team"),
 ("Performance Reporting: PICA analysis, billing report", "Input for performance evaluation &amp; management decisions"),
 ("Innovation &amp; Development: innovation project &amp; development", "Innovation framework; field conditions documented"),
]
SUPPLY = [
 ("Demand Check: rising demand in PCR, buying reason, location, priority, expected price", "Clear demand before quoting"),
 ("Preliminary Drawing Review: unit function, critical components, Application Engineering", "Critical price / lead-time items identified"),
 ("Request Quote to UTE: full data, standard GP 13.6%, SLA, result into PCR", "Quote ready for the sales team"),
 ("Close Won → CPO: PO / PJB in CRM, QFD, RFD = PO Interco due date, approval route", "PO Interco issued"),
 ("Monitoring: production follow-up, QFD vs actual, painting style, FAT", "Unit delivered on RFD; billing documents complete"),
]
sides = ('<div class="two">' + ex_table("A. STRATEGIC", "Sets the direction · for management decisions", "o", STRAT)
         + ex_table("B. SUPPLY CHAIN", "Runs the transaction · for operations", "s", SUPPLY) + '</div>')
boxes = ('<div class="three">'
  '<div class="c box"><h4>Dimensions</h4>' + ul(["<b>Financial:</b> non-Patria procurement budget, COGS per unit, target margin per PO", "<b>Non-financial:</b> vendors &amp; customers, documents verified, report frequency, meetings &amp; site visits"]) + '</div>'
  '<div class="c box"><h4>Working Relationships</h4>' + ul(["<b>Internal:</b> Sales &amp; Marketing, Warehouse, Finance &amp; Accounting, Legal, Procurement", "<b>External:</b> customers, Patria &amp; non-Patria vendors, forwarders, UTPE"]) + '</div>'
  '<div class="c box"><h4>Work Challenges</h4>' + ul(["Push UTPE marketing to send unit price quotes quickly", "Push UTPE marketing and escalate to superiors when production problems threaten the timeline",
   "Sudden customer quote requests that need a price in a very short time"]) + '</div></div>')
slide10 = f'''<section class="slide rr2"><div class="in">
  <div class="top"><span class="tag">[ INTERNAL USE ONLY ]</span><span></span><img class="tri" src="{tri}" alt="Triatra"></div>
  <div class="kick">Section 04 · Roles &amp; Responsibility · B</div>
  <h1 class="t">Strategic vs Supply Chain</h1>
  <div class="bands">{band(1, "Strategic vs Supply Chain", sides)}{band(2, "SIPOC", sip)}{band(3, "Dimensions, Working Relationships &amp; Work Challenges", boxes)}</div>
  <div class="foot"><span>NEDP Mid Year Review 2026</span><span><b>10</b> / 15</span></div>
</div></section>'''

# ---------- Monitoring evidence (Supply Chain 2/2) ----------
ev5 = '<div class="evimg evrow">' + "".join(f'<img src="{photo(f"assets/evidence/sc5_{i}.webp", 700)}">' for i in (72, 73, 74, 75)) + '</div>'
slide15 = slide15.replace('<b>Monitoring</b></div>' + step5 + '</div>', '<b>Monitoring</b></div>' + step5 + ev5 + '</div>')
EXTRA_CSS += ".sc2 .stp .evimg{min-height:0}.sc2 .stp .evrow img{flex:1 1 22%;height:100%;object-fit:cover}\n"
EXTRA_CSS += ".sc2b{grid-template-rows:minmax(0,1.6fr) auto minmax(0,.75fr)!important;gap:10px}.sc2 .two{min-height:0;overflow:hidden}.sc2 .stp{min-height:0;overflow:hidden;gap:6px;padding:10px 14px}.sc2 .stp ul.b{font-size:10.5px!important;line-height:1.35!important}.sc2 .stp .evimg{flex:1}.mo{padding:7px 12px}.mo span{font-size:10px}\n"
