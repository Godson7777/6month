"""Stock recommendation deck: 5 cranes (2 F.lli Ferrari + 3 XCMG), Minto order, native McKinsey-style charts."""
import sys
sys.path.insert(0, '.')
import crane_data as d, crane_map as cm
from cr_common import *
jt = lambda x: f"Rp {x/1e6:,.0f} Jt".replace(',', '.')
T = {(c, t['tier']): t for c in d.CLS for t in cm.tiers(c)}
F = {f['type']: f for f in d.ferrari()}
REC = [('F.lli Ferrari', 'FBR450 A4', [('Heavy', (45, 50)), ('Heavy', (50, 55))], 'Amco Veba V950', ('Heavy', (45, 50)), F['FBR450 A4']['p']),
       ('F.lli Ferrari', '258 A3', [('Medium', (25, 30))], 'Amco Veba V825', ('Medium', (25, 30)), F['258 A3']['p']),
       ('XCMG', 'SQ3.2ZK2', [('Light', (5, 8))], 'Sany Palfinger SPK8500', ('Light', (5, 8)), None),
       ('XCMG', 'SQZ325.4', [('Medium', (30, 35))], 'HIAB X-CLX 388', ('Medium', (30, 35)), None),
       ('XCMG', 'KSQZ365.4', [('Medium', (35, 40))], 'Palfinger PK 41002', ('Medium', (35, 40)), None)]
rows = []
for b, m, tiers, lead, lt, p in REC:
    t = T[lt]
    if p is None: p = next(x['p'] for x in t['models'] if x['type'] == m)
    units = sum(T[k]['units'] for k in tiers)
    lab = f"{tiers[0][0]} {tiers[0][1][0]}–{tiers[-1][1][1]} tm"
    rows.append(dict(brand=b, model=m, units=units, lab=lab, lead=lead, lp=t['top']['p'], p=p))
tot = sum(r['units'] for r in rows); allu = sum(t['units'] for t in T.values())
deck = Deck()
SRC = ('Source: Indonesia import records 2023 – Aug 2026 (folding cranes; Hyva, Zoomlion, grabbers, telescopic excluded). Prices per unit: competitors = average import price × Rp 17.803/USD; '
       'F.lli Ferrari = price list June 2026 (K − I) less 13.6% TSP GP; XCMG = average import price.')
# ---- 1: answer ----
C = deck.slide('Stock Recommendation/', 'Which cranes should we stock', 'to cut lead time?',
               'Stock 5 cranes: 2 F.lli Ferrari and 3 XCMG, in the tm ranges that buy the most',
               [('Without stock, buyers wait ', False), ('14 – 27 weeks', True), (' for a factory order. These 5 cranes cover ', False),
                (f'{tot} of {allu} units imported ({tot/allu:.0%})', True), (' and each is cheaper than the best-seller in its range.', False)])
tb = C.s.shapes.add_table(6, 5, E(36), E(240), E(1206), E(380)).table
for j, w in enumerate([60, 300, 220, 140, 486]): tb.columns[j].width = E(w)
why = ['Biggest Heavy demand; 27 weeks from Brazil, so stock matters most',
       'European crane vs Amco Veba, same size, lower price',
       'Largest tm range of all; fastest stock turnover',
       'Low-cost answer to HIAB buyers paying European prices',
       'Biggest price gap of all ranges']
hd = ['#', 'Crane', 'tm range', 'Units 2023–26', 'Why']
for i in range(6):
    tb.rows[i].height = E(34 if i == 0 else 69)
    for j in range(5):
        c = tb.cell(i, j); c.fill.solid(); c.vertical_anchor = MSO_ANCHOR.MIDDLE; c.margin_left = E(10)
        if i == 0: txt, bo, col, fc, sz = hd[j], True, 'FFFFFF', DG, 12
        else:
            r = rows[i-1]; fc = LG if r['brand'].startswith('F') else 'FFFFFF'
            txt, bo, col, sz = [str(i), f"{r['brand']} {r['model']}", r['lab'], str(r['units']), why[i-1]][j], j in (0, 1), DG if j == 1 else '000000', 13 if j < 4 else 12
        c.fill.fore_color.rgb = rgb(fc); p = c.text_frame.paragraphs[0]; run = p.add_run(); run.text = txt
        run.font.size = Pt(sz); run.font.bold = bo; run.font.name = FONT; run.font.color.rgb = rgb(col)
C.box(36, 628, 1206, 42, 'F2F2F2')
C.tx(46, 632, 1186, 36, [[('How to read: ', True, '000000', 10), ('tm = ton-meter (lifting moment). Light ≤ 8 tm · Small 8–25 tm · Medium 25–45 tm · Heavy > 45 tm. Units = cranes imported into Indonesia, Jan 2023 – Aug 2026. '
    'Green rows = F.lli Ferrari models. Lead time without stock: China 14 weeks, Italy 25 weeks, Brazil 27 weeks (F.lli Ferrari price list).', False, '000000', 10)]])
C.tx(36, 680, 1206, 30, [[(SRC, False, '7F7F7F', 7.5)]])
# ---- 2: demand chart ----
C = deck.slide('Where the Demand Is/', 'Do these tm ranges', 'really sell?',
               f'The 5 recommended ranges take {tot/allu:.0%} of all imported folding cranes',
               [('Units imported per tm range, 2023 – 2026. ', False), ('Green = range we stock.', True)])
keys = [k for k in T if T[k]['units'] >= 3]
sel = {k for _, _, tiers, *_ in REC for k in tiers}
cats = [f"{k[0]}\n{k[1][0]}–{k[1][1]} tm" for k in keys]
ch = C.chart(XL_CHART_TYPE.COLUMN_CLUSTERED, 36, 236, 1206, 390, cats, [('Units', [T[k]['units'] for k in keys])], gap=40, serlines=False)
se = ch.plots[0].series[0]; dl = se.data_labels; dl.show_value = True; dl.position = XL_LABEL_POSITION.OUTSIDE_END; dl.font.size = Pt(12); dl.font.bold = True; dl.font.name = FONT
for i, k in enumerate(keys):
    pt = se.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(G if k in sel else 'BFBFBF')
ch.category_axis.tick_labels.font.size = Pt(10)
C.box(36, 632, 1206, 40, 'F2F2F2')
C.tx(46, 636, 1186, 34, [[('How to read: ', True, '000000', 10), ('tm = ton-meter (lifting moment = load × reach). Classes: Light ≤ 8 tm · Small 8–25 tm · Medium 25–45 tm · Heavy > 45 tm, each split into 5-tm ranges. '
    'Bars = cranes imported into Indonesia in each range, Jan 2023 – Aug 2026. Green = range where we recommend stock.', False, '000000', 10)]])
C.tx(36, 680, 1206, 30, [[(SRC, False, '7F7F7F', 7.5)]])
# ---- 3: price chart ----
C = deck.slide('Price vs Best-Seller/', 'Can we win', 'on price?',
               'In every recommended range our crane costs less than the best-seller',
               [('Price per unit, Rp Jt. ', False), ('Grey = best-seller, green = our crane.', True)])
cats = [f"{r['lab']}: {r['model']} vs {r['lead']}" for r in rows]
ch = C.chart(XL_CHART_TYPE.BAR_CLUSTERED, 36, 236, 900, 380, cats, [('Best-seller', [round(r['lp']/1e6) for r in rows]), ('Our crane', [round(r['p']/1e6) for r in rows])], gap=50, serlines=False)
ch.plots[0].overlap = -10
for k, col in enumerate(['BFBFBF', G]):
    se = ch.plots[0].series[k]; se.format.fill.solid(); se.format.fill.fore_color.rgb = rgb(col)
    dl = se.data_labels; dl.show_value = True; dl.position = XL_LABEL_POSITION.OUTSIDE_END; dl.font.size = Pt(11); dl.font.name = FONT; dl.number_format = '#,##0'; dl.number_format_is_linked = False
ch.category_axis.reverse_order = True; ch.category_axis.tick_labels.font.size = Pt(11)
C.legend(40, 618, 160, [('BFBFBF', 'Best-seller'), (G, 'Our crane')])
C.box(36, 636, 1206, 40, 'F2F2F2')
C.tx(46, 640, 1186, 34, [[('How to read: ', True, '000000', 10), ('Best-seller = model with the highest import value in that tm range. Price = cost per unit, crane only, before Triatra margin: competitors at average import price, '
    'F.lli Ferrari at price list less TSP GP, XCMG at average import price. Rp Jt = million rupiah.', False, '000000', 10)]])
for i, r in enumerate(rows):
    C.tx(960, 246 + i * 72, 280, 50, [[(f"−{jt(r['lp'] - r['p'])}", True, G, 16)], [('cheaper per unit', False, '595959', 10)]])
C.tx(36, 680, 1206, 30, [[(SRC, False, '7F7F7F', 7.5)]])
deck.save('v7/Stock_Recommendation_5.pptx'); print('ok', tot, allu)
