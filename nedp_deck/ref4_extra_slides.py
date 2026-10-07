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

sides = ('<div class="two">'
  '<div class="c side o"><div class="sh"><b>A. STRATEGIC</b><span>Sets the direction · output used for management decisions</span></div>'
  + ul(["Pricing &amp; Market Analysis", "Market Study &amp; Program Development", "Market Program for Support Sales", "Performance Reporting (GP, PICA)", "Innovation &amp; Development"]) + '</div>'
  '<div class="c side s"><div class="sh"><b>B. SUPPLY CHAIN</b><span>Runs the transaction · output used for operations</span></div>'
  + ul(["Quotation &amp; Production Coordination", "Operational Reporting", "Internal &amp; External Coordination", "Routine Meetings &amp; Communication"], "s") + '</div></div>')
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
.rr2 .bands{position:absolute;left:44px;right:44px;top:150px;bottom:42px;display:grid;grid-template-rows:auto auto 1fr;gap:12px}
.band{display:flex;flex-direction:column;gap:7px;min-height:0}
.bh{display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--line);padding-bottom:5px}
.bh b{width:22px;height:22px;border-radius:6px;background:var(--or);color:#fff;display:grid;place-items:center;font-size:12px}
.bh span{font-size:15px;font-weight:600}
.rr2 .two{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.rr2 .side{padding:10px 14px}.rr2 .side.o{border-top:2px solid var(--or)}.rr2 .side.s{border-top:2px solid var(--steel)}
.rr2 .sh{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}
.rr2 .sh b{font-size:13px;letter-spacing:.1em}.rr2 .side.o .sh b{color:var(--or)}.rr2 .side.s .sh b{color:var(--steel)}
.rr2 .sh span{font-size:9.5px;color:var(--mut)}
.rr2 .side ul.b{columns:2;font-size:11px}
.sip2{width:100%;border-collapse:collapse;font-size:10.5px;color:var(--tx2)}
.sip2 th{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx);text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}
.sip2 td{padding:7px 8px;border-bottom:1px solid var(--line);line-height:1.35}
.sip2 .pc{background:var(--or-dim);color:var(--tx);font-weight:600;border-left:1px solid var(--or);border-right:1px solid var(--or)}
.sip2 th.pc{color:var(--or)}
.sip2 .rl{font-size:10.5px;font-weight:700;letter-spacing:.08em;width:118px}.sip2 .rl.o{color:var(--or)}.sip2 .rl.s{color:var(--steel)}
.rr2 .three{flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;min-height:0}
.rr2 .box{padding:10px 14px}.rr2 .box h4{font-size:12.5px;margin-bottom:6px}
.rr2 .box ul.b{font-size:10.8px}.rr2 .box ul.b b{color:var(--tx)}
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
