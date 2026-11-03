"""Deck for F.lli Ferrari meeting: most popular crane models per tm range (imports 2023 - 2026). Simple tables."""
import sys
sys.path.insert(0, '.')
import crane_data as d, crane_map as cm
from cr_common import *
usd = lambda x: f"USD {x:,.0f}".replace(',', '.')
idr = lambda x: f"Rp {x * d.FX / 1e6:,.0f} Jt".replace(',', '.')
RANGE = {'Light': 'up to 8 tm', 'Small': '8 – 25 tm', 'Medium': '25 – 45 tm', 'Heavy': 'above 45 tm'}
def lab(tr): lo, hi = tr; return f'up to {hi} tm' if lo == 0 else f'{lo} – {hi} tm'
def pop(t, n): return sorted(t['models'], key=lambda x: (-x['q'], -x['usd']))[:n]
NOTE = ('Source: Indonesia import records 2023 – Aug 2026 (folding / knuckle boom cranes only; Hyva and Zoomlion not included). '
        'Units = units imported. Price per unit = average import price of the model (CIF value ÷ units), before Indonesian duty and tax; Rp at 17.803 per USD. '
        'Model variants merged (e.g. SPK8500 = SPK8500, A, B).')
deck = Deck()
def table(C, rows, widths, y0, rh, head, cls_col=True):
    s = C.s; X0 = 36
    tb = s.shapes.add_table(1 + len(rows), len(widths), E(X0), E(y0), E(sum(widths)), E(30 + rh * len(rows))).table
    for j, w in enumerate(widths): tb.columns[j].width = E(w)
    tb.rows[0].height = E(30)
    for i in range(1, 1 + len(rows)): tb.rows[i].height = E(rh)
    def cell(i, j, text, bold=False, fillc='FFFFFF', color='000000', sz=12, al=PP_ALIGN.LEFT):
        c = tb.cell(i, j); c.fill.solid(); c.fill.fore_color.rgb = rgb(fillc); c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.margin_left = c.margin_right = E(8); c.margin_top = c.margin_bottom = E(1)
        p = c.text_frame.paragraphs[0]; p.alignment = al; r = p.add_run(); r.text = text
        r.font.name = FONT; r.font.size = Pt(sz); r.font.bold = bold; r.font.color.rgb = rgb(color)
    for j, h in enumerate(head): cell(0, j, h, True, DG, 'FFFFFF', 12, PP_ALIGN.RIGHT if j >= len(head) - 3 else PP_ALIGN.LEFT)
    return tb, cell
# ---------- slide 1: overview, most popular model per tm range ----------
rows = []
for c in d.CLS:
    for t in cm.tiers(c):
        m = pop(t, 1)[0]; rows.append((c, t, m))
C = deck.slide('Most Popular Cranes in Indonesia/', 'Which crane sells most', 'in each tm range?',
               'Sany Palfinger, Palfinger and Amco Veba sell the most popular model in nearly every tm range',
               [('Folding cranes imported into Indonesia, ', False), ('2023 – 2026', True), ('. One row per tm range: the model with the most units sold.', False)])
widths = [110, 140, 200, 220, 130, 200, 206]
tb, cell = table(C, rows, widths, 236, 25.5, ['Class', 'tm range', 'Brand', 'Model', 'Units sold', 'Price / unit (USD)', 'Price / unit (Rp)'])
start = {}
for i, (c, t, m) in enumerate(rows, start=1):
    start.setdefault(c, [i, i])[1] = i
    fill = 'FFFFFF' if i % 2 else 'F7F7F7'
    cell(i, 1, lab(t['tier']), True, fill, '000000', 11)
    cell(i, 2, m['nice'], False, fill, '000000', 11)
    cell(i, 3, m['type'], True, fill, DG, 11)
    cell(i, 4, f"{m['q']}", False, fill, '000000', 11, PP_ALIGN.RIGHT)
    cell(i, 5, usd(m['usd'] / m['q']), False, fill, '000000', 11, PP_ALIGN.RIGHT)
    cell(i, 6, idr(m['usd'] / m['q']), False, fill, '595959', 11, PP_ALIGN.RIGHT)
for c, (a, b) in start.items():
    if b > a: tb.cell(a, 0).merge(tb.cell(b, 0))
    cell(a, 0, c, True, COL[c], 'FFFFFF' if c in DARK else '000000', 12)
C.tx(36, 680, 1206, 30, [[(NOTE, False, '7F7F7F', 7.5)]])
# ---------- slides 2-5: top 3 per tm range, per class ----------
for c in d.CLS:
    T = cm.tiers(c); rows = [(t, r, m) for t in T for r, m in enumerate(pop(t, 3), start=1)]
    tu = sum(t['units'] for t in T); top = max(T, key=lambda t: t['units']); tm_ = pop(top, 1)[0]
    C = deck.slide(f'{c} Class ({RANGE[c]})/', 'Top 3 models', 'in each tm range',
                   f"{c}: {tm_['nice']} {tm_['type']} is the best seller, {tm_['q']} units in {lab(top['tier'])}",
                   [(f'{c} class: ', False), (f'{tu} units imported in 2023 – 2026', True), ('. Up to three best-selling models per tm range.', False)])
    rh = min(34, (650 - 236 - 30) / len(rows))
    widths = [150, 70, 210, 250, 140, 190, 196]
    tb, cell = table(C, rows, widths, 236, rh, ['tm range', '#', 'Brand', 'Model', 'Units sold', 'Price / unit (USD)', 'Price / unit (Rp)'])
    span = {}
    for i, (t, r, m) in enumerate(rows, start=1):
        span.setdefault(t['tier'], [i, i, t])[1] = i
        fill = LG if r == 1 else 'FFFFFF'; sz = 12 if len(rows) <= 9 else 11
        cell(i, 1, str(r), r == 1, fill, G if r == 1 else '7F7F7F', sz)
        cell(i, 2, m['nice'], r == 1, fill, '000000', sz)
        cell(i, 3, m['type'], True, fill, DG if r == 1 else '000000', sz)
        cell(i, 4, f"{m['q']}", r == 1, fill, '000000', sz, PP_ALIGN.RIGHT)
        cell(i, 5, usd(m['usd'] / m['q']), False, fill, '000000', sz, PP_ALIGN.RIGHT)
        cell(i, 6, idr(m['usd'] / m['q']), False, fill, '595959', sz, PP_ALIGN.RIGHT)
    for tr, (a, b, t) in span.items():
        if b > a: tb.cell(a, 0).merge(tb.cell(b, 0))
        cc = tb.cell(a, 0); cc.fill.solid(); cc.fill.fore_color.rgb = rgb('F2F2F2'); cc.vertical_anchor = MSO_ANCHOR.MIDDLE
        cc.margin_left = E(8); tf = cc.text_frame; p = tf.paragraphs[0]
        for txt, bo, col, sz in [(lab(tr), True, G, 13)]:
            r = p.add_run(); r.text = txt; r.font.name = FONT; r.font.size = Pt(sz); r.font.bold = bo; r.font.color.rgb = rgb(col)
        p2 = tf.add_paragraph(); r = p2.add_run(); r.text = f"{t['units']} unit{'s' if t['units'] > 1 else ''} in total"; r.font.name = FONT; r.font.size = Pt(9.5); r.font.color.rgb = rgb('595959')
    C.tx(36, 680, 1206, 30, [[(NOTE, False, '7F7F7F', 7.5)]])
deck.save('v7/Ferrari_Meeting_Popular_Cranes.pptx'); print('ok')
