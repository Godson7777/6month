"""Slides 13-15 after slide 12: who leads, where we can win, what we ask. Same style as slide12.py."""
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
FONT = 'Neue Haas Grotesk Text Pro'; E = lambda v: Emu(round(v * 9525)); rgb = RGBColor.from_string
ACC, GREY, LOSE = '1E9E57', '6B6B6B', 'C0392B'
G = ['0B4D2A', '1E9E57', '6FCF97', 'C7EFD5']; OTH = 'D9D9D9'
P = Presentation(); P.slide_width, P.slide_height = 12192000, 6858000
s = None
def tx(x, y, w, h, parts, sz=12, al=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    b = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
    if isinstance(parts, str): parts = [[(parts, False, '000000')]]
    for i, para in enumerate(parts):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = al
        for t, bold, c in para:
            r = p.add_run(); r.text = t; r.font.size = Pt(sz); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = rgb(c)
    return b
def line(x1, y1, x2, y2, c='000000', w=1.0):
    l = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2)); l.line.color.rgb = rgb(c); l.line.width = Pt(w)
def box(x, y, w, h, fill, line_c=None):
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h)); r.fill.solid(); r.fill.fore_color.rgb = rgb(fill)
    if line_c: r.line.color.rgb = rgb(line_c); r.line.width = Pt(1)
    else: r.line.fill.background()
    return r
def header(no, title, question, sub, msg):
    global s
    s = P.slides.add_slide(P.slide_layouts[6])
    tx(36, 22, 200, 16, '10/18/2026', 11); tx(440, 22, 400, 16, 'Shaping the future of our industry', 11, PP_ALIGN.CENTER)
    tx(1144, 22, 100, 16, str(no), 11, PP_ALIGN.RIGHT)
    tx(36, 52, 900, 60, [[(title, True, '000000')]], 36, anchor=MSO_ANCHOR.MIDDLE)
    tx(940, 54, 304, 56, [[(q, True, '000000')] for q in question], 16, PP_ALIGN.RIGHT)
    line(28, 116, 1252, 116, '000000', 3)
    tx(36, 122, 1208, 28, [[(sub, True, '000000')]], 19, anchor=MSO_ANCHOR.MIDDLE)
    line(28, 152, 1252, 152); tx(36, 157, 1208, 44, [msg], 14); line(28, 204, 1252, 204)
def footer(src, note):
    tx(36, 662, 1208, 16, [[('Source: ', True, '000000'), (src, False, '000000')]], 10)
    tx(36, 680, 1208, 16, [[('Note: ', True, GREY), (note, False, GREY)]], 10)
    line(28, 700, 1252, 700, ACC, 1)
def divider(x):
    line(x, 220, x, 650, ACC, 2)
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, E(x - 16), E(420), E(32), E(32)); c.fill.solid(); c.fill.fore_color.rgb = rgb(ACC); c.line.fill.background()
    tf = c.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    r = tf.paragraphs[0].add_run(); r.text = '>'; r.font.bold = True; r.font.size = Pt(16); r.font.name = FONT; r.font.color.rgb = rgb('FFFFFF')
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
def table(x, y, widths, rows, hdr_fill='000000', fills=None, sz=11, rh=26, left=(0,)):
    t = s.shapes.add_table(len(rows), len(widths), E(x), E(y), E(sum(widths)), E(rh * len(rows))).table
    for j, w in enumerate(widths): t.columns[j].width = E(w)
    for i, row in enumerate(rows):
        t.rows[i].height = E(rh)
        for j, v in enumerate(row):
            if isinstance(v, str): v = (v, False, '000000')
            cell = t.cell(i, j); cell.text = v[0]; cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for m in ('margin_left', 'margin_right'): setattr(cell, m, E(6))
            cell.margin_top = cell.margin_bottom = E(2)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT if j in left else PP_ALIGN.RIGHT
                for r in p.runs:
                    r.font.name = FONT; r.font.size = Pt(sz)
                    r.font.bold = i == 0 or v[1]; r.font.color.rgb = rgb('FFFFFF' if i == 0 else v[2])
            cell.fill.solid(); cell.fill.fore_color.rgb = rgb(hdr_fill if i == 0 else (fills[i] if fills and fills.get(i) else 'FFFFFF'))
    return t

# ================= SLIDE 13: who leads =================
MED = [('Sany Palfinger', 30, 47), ('XCMG', 14, 26), ('Palfinger', 5, 17)]; MED_T = 60
HEV = [('Palfinger', 22, 62), ('Amco Veba', 7, 23), ('XCMG', 4, 10)]; HEV_T = 39
header(13, 'Who Leads Medium and Heavy?', ["Who's lead the market?", 'And how strong are they?'],
       'Two brands lead: Sany Palfinger in Medium, Palfinger in Heavy',
       [('In 2025, ', False, '000000'), ('Sany Palfinger holds 47% of Medium value', True, '000000'), (' and ', False, '000000'),
        ('Palfinger holds 62% of Heavy value', True, '000000'),
        ('. The top 3 brands take 90% of Medium and 95% of Heavy value, so each class has one clear leader to win against.', False, '000000')])
def brand_panel(x0, cls, data, total_u):
    others_v = 100 - sum(d[2] for d in data); others_u = total_u - sum(d[1] for d in data)
    tx(x0, 214, 560, 36, [[(f'{cls} class (25–45 tm)' if cls == 'Medium' else f'{cls} class (> 45 tm)', True, '000000'),
                            (', share of import value by brand, 2025, %', False, '000000')]], 12)
    names = [d[0] for d in data] + ['Others']; vals = [d[2] for d in data] + [others_v]; units = [d[1] for d in data] + [others_u]
    cd = CategoryChartData(); cd.categories = ['Value']
    for n, v in zip(names[::-1], vals[::-1]): cd.add_series(n, [v])
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED_100, E(x0), E(262), E(560), E(70), cd).chart
    ch.has_legend = False; ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False
    ch.category_axis.visible = False; pl = ch.plots[0]; pl.gap_width = 10; pl.overlap = 100
    cols = [OTH] + G[:3][::-1]
    for ser, c, n, v in zip(ch.series, cols, names[::-1], vals[::-1]):
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(c); ser.format.line.color.rgb = rgb('FFFFFF')
        dl = ser.data_labels; dl.font.size = Pt(11); dl.font.name = FONT; dl.show_value = False
        tf = ser.points[0].data_label.text_frame; tf.text = f'{v}%'
        for r in tf.paragraphs[0].runs: r.font.bold = True; r.font.color.rgb = rgb('FFFFFF' if c in (G[0], G[1]) else '000000')
    # legend-like table of brands
    rows = [['#  Brand', 'Units 2025', 'Share of units', 'Share of value']]
    for i, (n, u, v) in enumerate(zip(names, units, vals)):
        lead = i == 0
        rows.append([(f'{i + 1}  {n}' if n != 'Others' else '    Others', lead, ACC if lead else '000000'),
                     (str(u), lead, '000000'), (f'{u / total_u:.0%}', lead, '000000'), (f'{v}%', lead, ACC if lead else '000000')])
    rows.append([('    Total', True, '000000'), (str(total_u), True, '000000'), ('100%', True, '000000'), ('100%', True, '000000')])
    table(x0, 352, [200, 120, 120, 120], rows, fills={1: 'E8F7EE'}, sz=12, rh=30)
    lead = data[0]
    tx(x0, 572, 560, 60, [[(f'{lead[0]} leads with {lead[1]} of {total_u} units ({lead[1] / total_u:.0%}) and {lead[2]}% of value', True, ACC)],
                           [('Top 3 brands = ' + f'{sum(d[2] for d in data)}% of value, {sum(d[1] for d in data)} of {total_u} units', False, '000000')]], 12)
brand_panel(36, 'Medium', MED, MED_T); divider(640); brand_panel(664, 'Heavy', HEV, HEV_T)
footer('Indonesia import records 2025, knuckle boom (folding) cranes; value in IDR before tax; brand split from earlier data cut (F.lli Ferrari Market Strategy).',
       'Total units 2025 from database (Medium 60, Heavy 39); "Others" = total minus top 3. Share may not add to 100% due to rounding.')

# ================= SLIDE 14: where we can win =================
header(14, 'Where Can F.lli Ferrari Win?', ['Where are we cheaper?', 'And where are we not?'],
       'F.lli Ferrari is cheaper head to head in 76 Medium and Heavy units',
       [('Against the leader in each tm class, ', False, '000000'), ('F.lli Ferrari is 14–32% cheaper in four matchups', True, '000000'),
        (' covering 76 units, but ', False, '000000'), ('48–107% more expensive against Sany Palfinger SPK and Palfinger PK 53002', True, '000000'),
        (', which together sold 127 units.', False, '000000')])
tx(36, 214, 1208, 20, [[('Head-to-head price by tm class, Medium and Heavy, 2023 – 2026*', True, '000000'), (', IDR per unit', False, '000000')]], 12)
W, L = ('Cheaper', True, ACC), ('More expensive', True, LOSE)
rows = [['tm class', 'Competitor model', 'Brand', 'Units sold', 'Price / unit', 'F.lli Ferrari model', 'Price / unit', 'Ferrari vs competitor', 'Result'],
        ['25 – 30 (Medium)', 'V825', 'Amco Veba', '31', 'Rp 650 Jt', '268 A4', 'Rp 500 Jt', ('−23%', True, ACC), W],
        ['30 – 35 (Medium)', 'SPK32080', 'Sany Palfinger', '33', 'Rp 530 Jt', 'FBR350R A4', 'Rp 1.090 Jt', ('+107%', True, LOSE), L],
        ['30 – 35 (Medium)', 'X-CLX 388 / 328', 'XCMG', '10', 'Rp 1.460 Jt', 'FBR350R A4', 'Rp 1.090 Jt', ('−25%', True, ACC), W],
        ['35 – 40 (Medium)', 'SPK36080', 'Sany Palfinger', '37', 'Rp 660 Jt', '7441C', 'Rp 1.240 Jt', ('+88%', True, LOSE), L],
        ['35 – 40 (Medium)', 'PK 41002', 'Palfinger', '21', 'Rp 1.440 Jt', '7441C', 'Rp 1.240 Jt', ('−14%', True, ACC), W],
        ['40 – 45 (Medium)', 'SPK42502', 'Sany Palfinger', '18', 'Rp 960 Jt', '746 A4', 'Rp 1.420 Jt', ('+48%', True, LOSE), L],
        ['45 – 50 (Heavy)', 'V950 + 2 others', 'Amco Veba', '14', 'Rp 1.990 Jt', 'FBR450R A4', 'Rp 1.350 Jt', ('−32%', True, ACC), W],
        ['50 – 55 (Heavy)', 'PK 53002', 'Palfinger', '39', 'Rp 1.760 Jt', '9601CR A8', 'Rp 3.260 Jt', ('+85%', True, LOSE), L],
        ['> 74 (Heavy)', 'PK 88002, GSQZ860/880', 'Palfinger / XCMG', '5', '—', 'No model', '—', '—', ('No offer', True, GREY)]]
fills = {i: 'E8F7EE' for i in (1, 3, 5, 7)}
table(36, 242, [140, 170, 130, 90, 110, 130, 110, 160, 168], rows, fills=fills, sz=11, rh=28, left=(0, 1, 2, 5))
tx(36, 568, 380, 70, [[('76 units', True, ACC)], [('where F.lli Ferrari is cheaper than the competitor model', False, '000000')]], 14)
tx(436, 568, 380, 70, [[('127 units', True, LOSE)], [('sold by SPK and PK 53002 at prices F.lli Ferrari cannot match today', False, '000000')]], 14)
tx(836, 568, 408, 70, [[('5 units', True, GREY)], [('above 74 tm, no F.lli Ferrari model (largest is 990R, 74 tm)', False, '000000')]], 14)
footer('Indonesia import records 2023 – Aug 2026 (earlier data cut, 638 units); F.lli Ferrari price list; competitor price = import value per unit, before tax.',
       '*2026 = Jan–Aug. 7441C price is an estimate. 45–50 tm includes V950 (12), X-HIPRO B58 (1), F485RA.2.23 (1). Jt = million rupiah.')

# ================= SLIDE 15: what we ask =================
header(15, 'Where Do We Attack First?', ['What do we focus on?', 'And what do we need?'],
       'Attack 25–30 tm and 45–50 tm first, then 35–40 tm',
       [('In 25–30 and 45–50 tm, ', False, '000000'), ('F.lli Ferrari matches Amco Veba feature by feature at 23–32% lower price', True, '000000'),
        ('. These two classes sold 66 units in 2023 – 2026*; Amco Veba sold 43 of them (V825 31, V950 12).', False, '000000')])
cards = [
    ('PRIORITY 1', '25 – 30 tm (Medium)', '268 A4 vs Amco Veba V825',
     [('49 units', 'class size'), ('31 units', 'V825 sold'), ('−23%', 'Ferrari price vs V825')],
     ['Red Power = Articulated Powerlink', 'PB = AVPS power boost', 'ECM = EBB electronic control', 'Magic Touch = Magic Touch auto fold']),
    ('PRIORITY 2', '45 – 50 tm (Heavy)', 'FBR450R A4 vs Amco Veba V950',
     [('17 units', 'class size'), ('12 units', 'V950 sold'), ('−32%', 'Ferrari price vs V950')],
     ['Red Power = Articulated Powerlink', 'PB = AVPS power boost', 'ECM = EBB electronic control', 'Magic Touch = Magic Touch auto fold']),
    ('PRIORITY 3', '35 – 40 tm (Medium)', '7441C vs Palfinger PK 41002',
     [('66 units', 'class size'), ('21 units', 'PK 41002 sold'), ('−14%', 'Ferrari price vs PK 41002 (est.)')],
     ['Confirm 7441C price with principal', 'Target PK 41002 users first', 'SPK36080 (37 units) is +88%:', 'not a target at today\'s price'])]
for k, (tag, cls, vs, kpis, feats) in enumerate(cards):
    x = 36 + k * 312; w = 296
    box(x, 214, w, 330, 'F2F2F2' if k else 'E8F7EE')
    tx(x + 14, 226, w - 28, 16, [[(tag, True, ACC)]], 10)
    tx(x + 14, 244, w - 28, 26, [[(cls, True, '000000')]], 17)
    tx(x + 14, 272, w - 28, 18, [[(vs, False, GREY)]], 12)
    for j, (big, small) in enumerate(kpis):
        tx(x + 14 + j * 92, 300, 90, 24, [[(big, True, ACC if j == 2 else '000000')]], 15)
        tx(x + 14 + j * 92, 326, 88, 40, [[(small, False, GREY)]], 9)
    line(x + 14, 372, x + w - 14, 372, 'BFBFBF', 0.75)
    tx(x + 14, 380, w - 28, 16, [[('Equal features' if k < 2 else 'Next steps', True, '000000')]], 11)
    tx(x + 14, 400, w - 28, 130, [[('• ' + f, False, '000000')] for f in feats], 11)
# ask box
box(980, 214, 264, 330, '0B4D2A')
tx(996, 226, 236, 16, [[('ASK TO BOD', True, 'C7EFD5')]], 10)
tx(996, 248, 236, 290, [[('1. ', True, 'FFFFFF'), ('Approve focus on 25–30, 45–50 and 35–40 tm', False, 'FFFFFF')], [('', False, 'FFFFFF')],
                        [('2. ', True, 'FFFFFF'), ('Support a price review with F.lli Ferrari for 30–35, 40–45 and 50–55 tm, where we are 48–107% above SPK and PK 53002', False, 'FFFFFF')],
                        [('', False, 'FFFFFF')],
                        [('3. ', True, 'FFFFFF'), ('Refresh brand and price data on the full 764-unit database before targets are set', False, 'FFFFFF')]], 12)
tx(36, 560, 1208, 60, [[('Not now: ', True, LOSE), ('30–35, 40–45 and 50–55 tm (SPK32080, SPK42502, PK 53002, 90 units) until price gap is closed; > 74 tm has no F.lli Ferrari model.', False, '000000')]], 12)
footer('Slide 14 head-to-head prices; Crane STP 4P Medium & Heavy (feature comparison); Indonesia import records 2023 – Aug 2026 (earlier data cut).',
       '*2026 = Jan–Aug. Unit counts per class from earlier data cut (638 units); refresh on 764-unit database before setting targets.')
P.save('Slides13_15_After_Slide12.pptx'); print('ok')
