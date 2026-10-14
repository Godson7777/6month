"""Draft v3: NEDP 6-month review in the Bitwise design guidance.
Reuses data-rich sections of the Ref5 deck and adds new slides. Output: v3/Deck_v3.html"""
import base64, io, json, re
from PIL import Image

ROOT = '/home/user/6month/nedp_deck/'
A = ROOT + 'assets/'
DR = '/tmp/claude-0/dv2/img/'
H = open(ROOT + 'NEDP_Deck_Ref5_Bright.html').read()
HEAD = H[:H.find('<body')]
FR = re.findall(r'<svg class="frame".*?</svg>', H, re.S)


def b64(path, w=1400, fmt=None):
    im = Image.open(path)
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    if im.mode == 'RGBA': im.save(b, 'PNG'); m = 'png'
    else: im.save(b, 'JPEG', quality=90); m = 'jpeg'
    return f'data:image/{m};base64,' + base64.b64encode(b.getvalue()).decode()


LOGO = b64(A + 'cutout/triatra_logo.png', 300)
N = [0]; TOTAL = 15


def frame(inner, cls=''):
    N[0] += 1
    return (f'<svg class="frame" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg"><foreignObject width="1280" height="720">'
            f'<section xmlns="http://www.w3.org/1999/xhtml" class="slide bw {cls}">{inner}</section></foreignObject></svg>')


def chrome(kick, head, body, lede='', dark=False):
    n = N[0] + 1
    return (f'<div class="bwtop"><img class="bwlogo" src="{LOGO}"><span class="bwutil"><b>NEDP 6-MONTH REVIEW</b> · {kick.upper()}</span></div>'
            f'<div class="bwk">{kick}</div><h1 class="bwh">{head}</h1>' + (f'<div class="bwl">{lede}</div>' if lede else '') +
            f'<div class="bwb">{body}</div><div class="bwf"><span>NEDP MID YEAR REVIEW 2026 · TIBERIAS K. SIMU</span><span>{n:02d} / {TOTAL}</span></div>')


def reuse(i, kick, head, n_new):
    s = FR[i]
    s = re.sub(r'<div class="kick"[^>]*>.*?</div>(\s*)<h1 class="t">.*?</h1>',
               f'<div class="kick">{kick}</div>\\1<h1 class="t">{head}</h1>', s, count=1, flags=re.S)
    s = re.sub(r'<span><b>\d+</b> / \d+</span>', f'<span><b>{n_new:02d}</b> / {TOTAL}</span>', s)
    s = s.replace('class="slide', 'class="slide bwr', 1)
    N[0] += 1
    return s


S = []
# 01 divider
S.append(frame(f'''<div class="dv"><img class="bwlogo" src="{LOGO}"><div class="dvk">PART 01 · PERSONAL</div>
<h1>Who I am and <i>what I bring</i> to Triatra.</h1><div class="dvl">About me · Onboarding journey</div>
<div class="dvf"><span>NEDP MID YEAR REVIEW 2026</span><span>01 / {TOTAL}</span></div></div>''', 'dark'))
# 02 about me
S.append(reuse(2, 'Personal information', 'A management graduate now running <i>Small Suppeq and Truck Others</i>', 2))
# 03 onboarding
ph = lambda f, w=900: b64(DR + f, w)
S.append(frame(chrome('Onboarding journey', 'Two programs built my base; <i>AHEMCE</i> comes next', f'''
<div class="ob">
 <div class="obc"><div class="obh"><span class="dot done"></span><b>Basic Technical Course</b><em>Done</em></div>
  <div class="obp qtwo"><img src="{ph('s3_4.jpg')}"><img src="{ph('s3_5.jpg')}"></div>
  <ul><li>Engine basics</li><li>Electrical system</li><li>Axle, wheel and suspension</li><li>Final drive and undercarriage</li></ul></div>
 <div class="obc"><div class="obh"><span class="dot done"></span><b>B-One · Orientation</b><em>Done</em></div>
  <div class="obp qtwo"><img src="{ph('s3_7.jpg')}"><img src="{ph('s3_6.jpg')}"></div>
  <ul><li>8 Astra competencies</li><li>AI at work</li><li>Teamwork</li><li>Corporate bootcamp</li></ul></div>
 <div class="obc next"><div class="obh"><span class="dot"></span><b>AHEMCE</b><em>Next</em></div>
  <div class="obbig">Astra Heavy Equipment, Mining, Construction and Energy</div>
  <ul><li>Heavy equipment</li><li>Mining</li><li>Contracting</li><li>Energy</li></ul></div>
</div><div class="obline"></div>''')))
# 04 company
S.append(reuse(5, 'Company profile', 'Triatra sells <i>PATRIA and ULTRA</i> to four industries for the UTPE group', 4))
# 05 site
S.append(reuse(7, 'Site operation', 'Triatra serves customers from <i>16 points</i> across Indonesia', 5))
# 06 org
S.append(reuse(9, 'Organization', 'I work in Marketing Strategic 2, under <i>Ignatius Indrawan S.</i>', 6))
# 07 roles
pr = lambda f: b64(A + 'products/' + f, 700)
STEPS = [('Inquiry', 'BC · AE · MKT', ['Spec, buying reason, site', 'Target price and lead time', 'Expected PO date']),
         ('Preliminary', 'BC · AE · MKT', ['Repeat or new drawing', 'Unit function', 'Critical parts: price, lead time']),
         ('Quotation', 'MKT Triatra · MKT UTPE', ['Quote request to UTE', 'Check standard GP', 'Track SLA; log PCR in CRM']),
         ('Negotiation & CPO', 'BC · MKT Triatra · MKT UTPE', ['PO / PJB vs drawing', 'PN, QFD, painting style', 'CPO and PO Interco approval']),
         ('Production', 'BC · MKT Triatra · MKT UTPE', ['Build vs QFD', 'Weekly update to BC', 'Escalate issues; run FAT'])]
flow = ''.join(f'<div class="st"><div class="stn">{i+1:02d}</div><b>{t}</b><span class="pic">{p}</span><ul>' + ''.join(f'<li>{x}</li>' for x in L) + '</ul></div>' + ('<div class="arr">→</div>' if i < 4 else '') for i, (t, p, L) in enumerate(STEPS))
units = lambda items: ''.join(f'<div class="un"><img src="{pr(f)}"><span>{n}</span></div>' for f, n in items)
S.append(frame(chrome('Roles & responsibility · Supply chain', 'I take every order from <i>inquiry to delivery</i> for two product lines', f'''
<div class="flow">{flow}</div>
<div class="prod"><div class="pg"><div class="pgh">SMALL SUPPEQ</div><div class="ug">{units([('ft_fuel_truck.webp','Fuel truck'),('wt_water_truck_clean.png','Water truck'),('lt_lube_truck.webp','Lube truck')])}</div></div>
<div class="pg"><div class="pgh">TRUCK OTHERS</div><div class="ug">{units([('crane_truck_crop.png','Crane truck'),('mixer_truck.webp','Mixer truck'),('st_stemming_truck.webp','Stemming truck')])}</div></div></div>''',
 'BC = Business Consultant · AE = Application Engineering · MKT = Marketing Unit')))
# 08 strategic 4C -> STP -> 4P
D = json.load(open(ROOT + 'stp4p/data.json'))
def short(d):
    g = d['gap']; gs = '–' if not d['ch'] else ('TBC' if g is None else f"{g*100:+.0f}%".replace('-', '−'))
    c = '' if g is None else ('r' if g > .3 else 'y' if g > 0 else 'g')
    return f"<tr><td>{d['tm']}</td><td>{d['top']} {d['tmodel']}</td><td>{(d['ch'] or 'No challenger') + ' ' + (d['cm'] or '')}</td><td class='n {c}'>{gs}</td></tr>"
mini = lambda R: ''.join(short(d) for d in R)
S.append(frame(chrome('Strategic · 4C → STP → 4P', 'Sell two challenger brands to take share from <i>Sany Palfinger and Palfinger</i>', f'''
<div class="s8">
 <div class="c4">
  <div class="cc"><span>CHANGE</span><p>HYVA stopped making cranes. Medium &amp; Heavy hold <b>64% of value</b> on 41% of units.</p></div>
  <div class="cc"><span>COMPETITOR</span><p>2025 leaders: <b>Sany Palfinger</b> 47% of Medium, <b>Palfinger</b> 62% of Heavy.</p></div>
  <div class="cc"><span>CUSTOMER</span><p>Medium buyers pick on price (China 73%). Heavy buyers pick on quality (Europe 85%).</p></div>
  <div class="cc me"><span>COMPANY</span><p>Partner <b>F.lli Ferrari</b> and <b>XCMG</b> to serve both buyer types.</p></div>
 </div>
 <div class="ar2">→</div>
 <div class="mid"><div class="cc"><span>STP</span><p><b>S</b> 2 classes, 10 tm tiers<br><b>T</b> Top 1 of each tier<br><b>P</b> XCMG: same capacity, lower price · Ferrari: European features, faster delivery</p></div>
  <table class="mt"><tr><th>tm</th><th>Top 1</th><th>Challenger</th><th>vs Top 1</th></tr>{mini(D['M'])}{mini([d for d in D['H'] if d['ch']])}</table></div>
 <div class="ar2">→</div>
 <div class="p4">
  <div class="cc"><span>PRODUCT</span><p>One challenger model per tier; show features the leader lacks.</p></div>
  <div class="cc"><span>PRICE</span><p>XCMG: get a special price. Ferrari: cut price where gap &gt; 30%.</p></div>
  <div class="cc"><span>PLACE</span><p>Ferrari stocks units in China (~14 weeks) and parts in Malaysia.</p></div>
  <div class="cc"><span>PROMOTION</span><p>Crane + flatdeck + install bundle (+2-yr warranty on Ferrari). Exhibitions with Marcom sales kit.</p></div>
 </div>
</div>''')))
# 09 project charter
G = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
ACT = [('Market study (4C)', 0, 3), ('STP and challenger choice', 3, 5), ('Negotiate with Ferrari and XCMG', 4, 7), ('Sales kit with Marcom', 5, 7),
       ('Exhibition and customer visits', 7, 9), ('Quotation → PO → first unit sold', 8, 10)]
gantt = '<tr><th>Activity</th>' + ''.join(f'<th>{m}</th>' for m in G) + '</tr>' + ''.join(
    f'<tr><td>{a}</td>' + ''.join(f'<td class="{"on" if s <= k < e else ""}"></td>' for k in range(10)) + '</tr>' for a, s, e in ACT)
S.append(frame(chrome('Project charter', 'Sell the first <i>Ferrari and XCMG</i> challenger cranes by March 2027', f'''
<div class="qpc">
 <div class="qpcl">
  <div class="qpb"><span>BACKGROUND</span><p>HYVA no longer makes cranes, so Triatra has no crane brand. Medium and Heavy cranes are 64% of import value, led by Sany Palfinger and Palfinger.</p></div>
  <div class="qpb"><span>GOAL</span><p>Put a cheaper or faster challenger against the Top 1 in each tm tier, and close the first sale.</p></div>
  <div class="qpb"><span>SCOPE</span><p>Medium and Heavy (&gt; 25 tm) · 4C → STP → 4P · F.lli Ferrari, XCMG (Fassi for Petrosea only)</p></div>
  <div class="qpb qtwo"><div><span>KPI</span><ol><li>4C, STP, 4P approved</li><li>Ferrari and XCMG terms signed</li><li>Sales kit ready</li><li>Quotations sent</li><li>First unit sold</li></ol></div>
   <div><span>TARGET</span><p class="qbig">First unit sold<br><b>Mar 2027</b></p></div></div>
 </div>
 <div class="qpcr">
  <div class="qpb"><span>TIMELINE · 2026 – 2027</span><table class="qgt">{gantt}</table></div>
  <div class="qpb"><span>TEAM</span><table class="qtm"><tr><td>Executive sponsor</td><td>Ricardo Tanada</td></tr><tr><td>Advisor</td><td>Ricardo Tanada · Ignatius Indrawan</td></tr>
   <tr><td>Coordinator</td><td>Ignatius Indrawan</td></tr><tr><td>Project lead</td><td>Tiberias Krisgaharu Simu</td></tr>
   <tr><td>Team members</td><td>Marketing Unit · Application Engineering · UTPE · Business Consultant</td></tr></table></div>
  <div class="qpb"><span>SUPPORT NEEDED</span><p>Marcom (sales kit) · F.lli Ferrari and XCMG (price and stock terms)</p></div>
 </div>
</div>''')))
# 10a / 10b
S.append(reuse(19, 'Study · Market size', 'Focus on Medium and Heavy: <i>64% of value</i> from 41% of units', 10))
S.append(reuse(20, 'Study · Brand leaders 2025', 'Two leaders to beat: <i>Sany Palfinger</i> in Medium, <i>Palfinger</i> in Heavy', 11))
# 11a / 11b tables
F = {'Palfinger': {'Linkage': 'Power Link Plus', 'Power boost': 'HPLS', 'Ext. speed': 'High Speed Ext.', 'Oscillation': 'AOS', 'Control': 'PALTRONIC 150', 'Auto fold': 'P-Fold'},
     'Sany Palfinger': {'Power boost': 'HPLS', 'Ext. speed': 'High speed ext.', 'Control': 'Paltronic 50'},
     'Amco Veba': {'Linkage': 'Articulated Powerlink', 'Power boost': 'AVPS', 'Control': 'EBB', 'Auto fold': 'Magic Touch'},
     'Ferrari': {'Linkage': 'Red Power', 'Power boost': 'PB', 'Ext. speed': 'RS', 'Oscillation': 'SDV', 'Control': 'ECM', 'Auto fold': 'Magic Touch'},
     'XCMG': {'Control': 'Load limiter'}}
def feat(top, ch):
    a, b = F.get(top, {}), F.get(ch, {})
    eq = [k for k in b if k in a]; win = [f'{b[k]}' for k in b if k not in a]
    return (', '.join(eq) or '–'), (', '.join(win) or 'Parity · wins on price/delivery')
def rows(R):
    o = ''
    for d in R:
        g = d['gap']; cls = '' if g is None else ('red' if g > .3 else 'amb' if g > 0 else '')
        rp = lambda v: 'TBC' if not v else f"Rp {v/1e6:,.0f} jt".replace(',', '.')
        if d['ch']:
            eq, win = feat(d['top'], d['ch'])
            gs = 'TBC' if g is None else f"<b class='{'g' if g <= 0 else 'y' if g <= .3 else 'r'}'>{g*100:+.0f}%</b>".replace('-', '−')
            if d['ch'] == 'Ferrari':
                place = 'Ferrari stocks units in China (~14 wks), parts in Malaysia'
                promo = 'Crane + flatdeck + install + 2-yr warranty; exhibition with sales kit'
                if g is not None and g > .3: place = 'Negotiate price with Ferrari. ' + place
            else:
                place = 'Negotiate special price with XCMG'; promo = 'Crane + flatdeck + install; exhibition with sales kit'
            ch = f"<b>{d['ch']}</b><br><span class='mu'>{d['cm']}</span>"; cp = rp(d['cp'])
        else:
            eq = win = place = promo = gs = cp = '–'; ch = '<span class="tag">NO CHALLENGER</span>'
        o += (f"<tr class='{cls}'><td class='b'>{d['tm']}</td><td class='n'>{d['qty']}</td><td class='n'>{d['share']*100:.0f}%</td>"
              f"<td><b>{d['top']}</b><br><span class='mu'>{d['tmodel']}</span></td><td class='n'>{d['tqty']}</td><td class='n'>{d['tshare']*100:.0f}%</td><td class='n'>{rp(d['tprice'])}</td>"
              f"<td>{ch}</td><td class='n'>{cp}</td><td class='n'>{gs}</td><td class='sm'>{eq}</td><td class='sm w'>{win}</td><td class='sm'>{place}</td><td class='sm'>{promo}</td></tr>")
    return o
TH = ('<tr><th class="g" colspan="3">Segmentation</th><th class="g" colspan="4">Targeting · Top 1</th><th class="g" colspan="3">Positioning · Challenger</th>'
      '<th class="g p" colspan="2">Product</th><th class="g p">Place</th><th class="g p">Promotion</th></tr>'
      '<tr><th>tm</th><th>Qty</th><th>Value</th><th>Brand · model</th><th>Qty</th><th>Share</th><th>Price</th><th>Brand · model</th><th>Price</th><th>vs Top 1</th>'
      '<th>Equal</th><th>Only challenger</th><th></th><th></th></tr>')
LEG = '<div class="leg"><i class="lg g"></i>Cheaper than Top 1 <i class="lg y"></i>Up to +30% <i class="lg r"></i>Over +30%: negotiate with Ferrari · Value = units × highest import price per model (estimate). * Top 1 absent in tier: next-largest brand shown.</div>'
for k, kick, head in [('M', 'STP + 4P · Medium class 25–45 tm', 'Use XCMG at 30–40 tm and Ferrari at 25–30 tm; <i>renegotiate Ferrari</i> for 40–45 tm'),
                      ('H', 'STP + 4P · Heavy class &gt; 45 tm', 'Win Heavy on <i>delivery time</i>; cut Ferrari\'s price to compete at 50–55 tm')]:
    R = D[k]
    for d in R:
        if 'absent' in d.get('note', ''): d['top'] += '*'
    S.append(frame(chrome(kick, head, f'<table class="xt">{TH}{rows(R)}</table>{LEG}')))
# 12 conclusion
S.append(frame(chrome('Conclusion', 'Partner with <i>F.lli Ferrari and XCMG</i>; keep Fassi for Petrosea', f'''
<div class="qcl">
 <div class="qbr"><div class="qbrh">XCMG</div><div class="qbrs">Medium · price buyers</div><ul><li>Challenger at 30–35 and 35–40 tm</li><li>SQZ365.4: −9% vs SPK36080</li><li>Ask XCMG for a special price</li><li>Bundle crane + flatdeck + install</li></ul></div>
 <div class="qbr f"><div class="qbrh">F.lli Ferrari</div><div class="qbrs">Heavy · quality buyers</div><ul><li>Wins 25–30 (−23%) and 45–50 tm (−32%)</li><li>Stock units in China (~14 weeks), parts in Malaysia</li><li>Cut price at 40–45, 50–55, 70–75 tm</li><li>Bundle + 2-year warranty</li></ul></div>
 <div class="qbr"><div class="qbrh">Fassi</div><div class="qbrs">Key account</div><ul><li>Petrosea buys Fassi only</li><li>Keep supply for this account</li></ul></div>
</div>
<div class="qask"><span>DECISIONS NEEDED</span><ol><li>Approve partnership talks with F.lli Ferrari and XCMG</li><li>Mandate Ferrari price and stock negotiation</li><li>Budget for exhibitions and Marcom sales kit</li></ol></div>''')))
# 13 thanks
S.append(frame(f'''<div class="dv"><img class="bwlogo" src="{LOGO}"><div class="dvk">THANK YOU</div><h1>Questions and <i>feedback</i> are welcome.</h1>
<div class="dvl">Tiberias Krisgaharu Simu · Marketing Strategic 2 Associate · PT Triatra Sinergia Pratama</div>
<div class="dvf"><span>NEDP MID YEAR REVIEW 2026</span><span>{TOTAL} / {TOTAL}</span></div></div>''', 'dark'))
assert len(S) == TOTAL, len(S)

CSS = open(ROOT + 'v3/bw.css').read()
html = HEAD.replace('</head>', f'<style>{CSS}</style></head>') + '<body><main id="deck">\n' + '\n'.join(S) + '\n</main></body></html>'
open(ROOT + 'v3/Deck_v3.html', 'w').write(html)
print('ok', len(S))
