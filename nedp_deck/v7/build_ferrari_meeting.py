"""Deck for the F.lli Ferrari meeting: most popular crane types per tm class (by units imported, 2023-2026)."""
import sys
sys.path.insert(0, '.')
src = open('v7/build_cr_deck.py').read(); src = src[:src.index('\ns_market_all();')]
exec(src)                     # brings deck, s_market_all, helpers
import crane_map as cm
jt = lambda x: f"Rp {num(x / 1e6, 0)} Jt"
POP = {c: cm.tiers(c) for c in d.CLS}
def ferr(t):
    base = {}
    for f in t['fer']:
        k = f['type'].split()[0]
        if k not in base: base[k] = f
    out = ', '.join(sorted(base, key=lambda k: base[k]['tm']))
    if not out and t['tier'] == (35, 40): out = '7441C (not in price list; please quote)'
    return out or '–'

def s_popular(classes, title, head, body):
    C = deck.slide(title, 'Which crane types sell most', 'in each tm class?', head, body)
    s = C.s; rows = [(c, t) for c in classes for t in POP[c]]
    cols = ['Class', 'tm class', 'Units', '#1 most popular', '#2', '#3', 'F.lli Ferrari in this size']
    W = [70, 78, 52, 300, 230, 230, 246]; X0, Y0 = 36, 236
    tb = s.shapes.add_table(1 + len(rows), len(cols), E(X0), E(Y0), E(sum(W)), E(400)).table
    for j, w in enumerate(W): tb.columns[j].width = E(w)
    rh = (652 - Y0 - 30) / len(rows); tb.rows[0].height = E(30)
    for i in range(1, len(rows) + 1): tb.rows[i].height = E(rh)
    def cell(i, j, runs, fillc='FFFFFF', al=PP_ALIGN.LEFT):
        c = tb.cell(i, j); c.fill.solid(); c.fill.fore_color.rgb = rgb(fillc); c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.margin_left = c.margin_right = E(6); c.margin_top = c.margin_bottom = E(1)
        for k, para in enumerate(runs):
            p = c.text_frame.paragraphs[0] if k == 0 else c.text_frame.add_paragraph(); p.alignment = al
            for t, b, col, sz in para:
                r = p.add_run(); r.text = t; r.font.bold = b; r.font.size = Pt(sz); r.font.name = FONT; r.font.color.rgb = rgb(col)
    for j, h in enumerate(cols): cell(0, j, [[(h, True, 'FFFFFF', 10.5)]], G if j == 6 else (DG if j != 3 else '0B4D2A'), PP_ALIGN.CENTER if j in (1, 2) else PP_ALIGN.LEFT)
    start, end = {}, {}
    for i, (c, t) in enumerate(rows, start=1):
        start.setdefault(c, i); end[c] = i
        lo, hi = t['tier']; cell(i, 1, [[(f'≤ {hi} tm' if lo == 0 else f'{lo}–{hi} tm', True, '000000', 10)]], 'F2F2F2', PP_ALIGN.CENTER)
        cell(i, 2, [[(str(t['units']), True, '000000', 10)]], 'F2F2F2', PP_ALIGN.CENTER)
        ms = sorted(t['models'], key=lambda x: -x['q'])[:3]
        for k in range(3):
            if k < len(ms):
                m = ms[k]; sh = m['q'] / t['units']
                cell(i, 3 + k, [[(f"{m['nice']} {m['type']}", True, DG if k == 0 else '000000', 10 if k == 0 else 9.5),
                                 (f"  {m['q']} units ({sh:.0%}) · {jt(m['p'])}", False, '595959', 8.5)]], LG if k == 0 else 'FFFFFF')
            else: cell(i, 3 + k, [[('', False, '000000', 9)]])
        cell(i, 6, [[(ferr(t), True, DG, 9.5)]], 'FFFFFF')
    for c in classes:
        if end[c] > start[c]: tb.cell(start[c], 0).merge(tb.cell(end[c], 0))
        cell(start[c], 0, [[(c, True, 'FFFFFF' if c in DARK else '000000', 11)]], COL[c])
    C.tx(36, 662, 1206, 34, [[('Source: Indonesia import records (Crane Market GVW Pairing v11), 2023 – 2026 (2026 partial year); folding cranes only; Hyva, Zoomlion, grabbers and telescopic cranes excluded. '
        'Popularity = units imported. Price = average import price per unit (total value ÷ units) × Rp 17.803/USD, before import duty and tax. Model variants merged. '
        'F.lli Ferrari models placed by lifting moment (flliferrari.it / price list June 2026).', False, '7F7F7F', 7)]])

def s_focus():
    focus = [(c, t) for c in d.CLS for t in POP[c] if t['units'] >= 20]
    focus.sort(key=lambda ct: -ct[1]['units'])
    tot = sum(t['units'] for c in d.CLS for t in POP[c]); fu = sum(t['units'] for _, t in focus)
    C = deck.slide('Where to Focus with F.lli Ferrari/', 'Which models must we beat,', 'and at what price?',
                   f'{len(focus)} tm classes take {fu / tot:.0%} of all units; each has one clear model to beat',
                   [('Ranked by units imported in 2023 – 2026. ', False), ('Price to beat', True), (' = average import price of the #1 model, before duty and tax.', False)])
    s = C.s
    cols = ['#', 'Class', 'tm class', 'Units', 'Model to beat (#1)', 'Its share', 'Price to beat /unit', 'F.lli Ferrari model to offer']
    W = [36, 80, 86, 62, 290, 86, 170, 396]; X0, Y0 = 36, 236
    tb = s.shapes.add_table(1 + len(focus), len(cols), E(X0), E(Y0), E(sum(W)), E(300)).table
    for j, w in enumerate(W): tb.columns[j].width = E(w)
    rh = min(44, (640 - Y0 - 30) / len(focus)); tb.rows[0].height = E(30)
    for i in range(1, len(focus) + 1): tb.rows[i].height = E(rh)
    def cell(i, j, t, b=False, col='000000', fillc='FFFFFF', sz=10.5, al=PP_ALIGN.LEFT):
        c = tb.cell(i, j); c.fill.solid(); c.fill.fore_color.rgb = rgb(fillc); c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.margin_left = c.margin_right = E(6); p = c.text_frame.paragraphs[0]; p.alignment = al
        r = p.add_run(); r.text = t; r.font.bold = b; r.font.size = Pt(sz); r.font.name = FONT; r.font.color.rgb = rgb(col)
    for j, h in enumerate(cols): cell(0, j, h, True, 'FFFFFF', G if j == 7 else DG, 10.5, PP_ALIGN.CENTER if j in (0, 2, 3, 5) else PP_ALIGN.LEFT)
    for i, (c, t) in enumerate(focus, start=1):
        m = max(t['models'], key=lambda x: x['q']); lo, hi = t['tier']
        cell(i, 0, str(i), True, '000000', 'F2F2F2', 10.5, PP_ALIGN.CENTER)
        cell(i, 1, c, True, 'FFFFFF' if c in DARK else '000000', COL[c])
        cell(i, 2, f'{lo}–{hi} tm', True, '000000', 'F2F2F2', 10.5, PP_ALIGN.CENTER)
        cell(i, 3, str(t['units']), True, '000000', 'F2F2F2', 10.5, PP_ALIGN.CENTER)
        cell(i, 4, f"{m['nice']} {m['type']}", True, DG, LG)
        cell(i, 5, f"{m['q'] / t['units']:.0%}", False, '000000', 'FFFFFF', 10.5, PP_ALIGN.CENTER)
        cell(i, 6, jt(m['p']), True, '000000')
        f = ferr(t); cell(i, 7, f if f != '–' else 'No model in this size: please advise', f != '–', DG if f != '–' else 'C55A11', 'FFFFFF', 10.5)
    C.tx(36, 662, 1206, 30, [[('Source: Indonesia import records (Crane Market GVW Pairing v11), 2023 – 2026 (2026 partial year); folding cranes only. Price to beat = average import price per unit of the #1 model '
        '(total value ÷ units) × Rp 17.803/USD, before import duty, tax and distributor margin. tm classes with fewer than 20 units in 2023 – 2026 not shown.', False, '7F7F7F', 7.5)]])

s_market_all()
s_popular(['Light', 'Small'], 'Most Popular Cranes: Light & Small/', 'Light & Small: Sany Palfinger leads; SPK8500 and SPK23500 are the volume models',
          [('Light and Small: ', False), (f"{sum(t['units'] for c in ('Light', 'Small') for t in POP[c])} units", True), (' imported in 2023 – 2026. ', False),
           ('5–8 tm and 20–25 tm', True), (' are the two biggest tm classes.', False)])
s_popular(['Medium', 'Heavy'], 'Most Popular Cranes: Medium & Heavy/', 'Medium is split between Sany Palfinger, Amco Veba and HIAB; Heavy is Palfinger PK 53002',
          [('Medium and Heavy: ', False), (f"{sum(t['units'] for c in ('Medium', 'Heavy') for t in POP[c])} units", True), (' imported in 2023 – 2026. ', False),
           ('30–35 tm and 35–40 tm', True), (' are the biggest Medium classes; PK 53002 alone is 39 of 65 Heavy units.', False)])
s_focus()
deck.save('v7/Ferrari_Meeting_Popular_Cranes.pptx'); print('saved')
