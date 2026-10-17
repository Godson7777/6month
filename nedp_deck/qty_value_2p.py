"""2 slides from user's table (Txn & Value USD, 2023–2026): slide 1 = QTY view, slide 2 = VALUE view. Template font."""
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
FONT = 'Neue Haas Grotesk Text Pro'; E = lambda v: Emu(round(v * 9525)); rgb = RGBColor.from_string
CLS = ['Light', 'Small', 'Medium', 'Heavy']; YRS = ['2023', '2024', '2025', '2026*']
TXN = {'Light': [109, 52, 53, 34], 'Small': [68, 52, 75, 28], 'Medium': [74, 70, 60, 14], 'Heavy': [16, 17, 39, 3]}
VAL = {'Light': [1318389, 839029, 551005, 310665], 'Small': [1535331, 1127848, 1777124, 596994],
       'Medium': [2452614, 2703601, 1759387, 388829], 'Heavy': [1095383, 1437894, 2951742, 227563]}
COL = {'Light': 'C7EFD5', 'Small': '6FCF97', 'Medium': '1E9E57', 'Heavy': '0B4D2A'}
P = Presentation(); P.slide_width, P.slide_height = 12192000, 6858000
def tx(s, x, y, w, h, t, sz, bold=False, color='000000', al=PP_ALIGN.LEFT):
    b = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tf = b.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = al; r = p.add_run(); r.text = t
    r.font.size = Pt(sz); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = rgb(color); return b
def slide(data, title, sub, unit, fmt, takeaways):
    s = P.slides.add_slide(P.slide_layouts[6])
    tx(s, 36, 34, 1208, 56, title, 30, True)
    tx(s, 36, 92, 1208, 24, sub, 13, color='6B6B6B')
    tot = {c: sum(data[c]) for c in CLS}; T = sum(tot.values())
    # 100% stacked chart (McKinsey style)
    if unit == 'Txn':   # units per year + total
        cats = YRS + ['Total']; vals = {c: data[c] + [tot[c]] for c in CLS}
        lab = lambda c, k: f"{vals[c][k]} ({vals[c][k] / sum(vals[x][k] for x in CLS):.0%})"
    else:               # units vs value
        cats = ['Units', 'Value']; vals = {c: [sum(TXN[c]), tot[c]] for c in CLS}
        lab = lambda c, k: f"{vals[c][k] / sum(vals[x][k] for x in CLS):.0%}"
    cd = CategoryChartData(); cd.categories = cats
    for c in CLS: cd.add_series(c, vals[c])
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED_100, E(36), E(130), E(560), E(530), cd).chart
    ch.has_legend = True; from pptx.enum.chart import XL_LEGEND_POSITION
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False; ch.legend.font.size = Pt(11); ch.legend.font.name = FONT
    pl = ch.plots[0]; pl.gap_width = 50 if unit == 'Txn' else 90; pl.overlap = 100
    ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False
    ch.category_axis.tick_labels.font.size = Pt(13); ch.category_axis.tick_labels.font.bold = True; ch.category_axis.tick_labels.font.name = FONT
    for ser, c in zip(ch.series, CLS):
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(COL[c]); ser.format.line.color.rgb = rgb('FFFFFF')
        for k in range(len(cats)):
            tf = ser.points[k].data_label.text_frame; tf.text = lab(c, k); r = tf.paragraphs[0].runs[0]
            r.font.size = Pt(11 if unit == 'Txn' else 14); r.font.bold = True; r.font.name = FONT
            r.font.color.rgb = rgb('000000' if c in ('Light', 'Small') else 'FFFFFF')
    # table: per year + total + share
    rows = 6; cols = 7
    tb = s.shapes.add_table(rows, cols, E(620), E(150), E(624), E(260)).table
    hdr = ['Class'] + YRS + ['Total', 'Share']
    widths = [96, 80, 80, 80, 80, 116, 92]
    for j, w in enumerate(widths): tb.columns[j].width = E(w)
    body = [[c] + [fmt(v) for v in data[c]] + [fmt(tot[c]), f'{tot[c] / T:.0%}'] for c in CLS]
    yt = [sum(data[c][k] for c in CLS) for k in range(4)]
    body.append(['Total'] + [fmt(v) for v in yt] + [fmt(T), '100%'])
    for i, row in enumerate([hdr] + body):
        for j, v in enumerate(row):
            cell = tb.cell(i, j); cell.text = v
            p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.RIGHT
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            r = p.runs[0]; r.font.name = FONT; r.font.size = Pt(12)
            hd = i == 0; last = i == 5; heavy = row[0] in ('Medium', 'Heavy') and not hd
            r.font.bold = hd or last or j >= 5
            r.font.color.rgb = rgb('FFFFFF' if hd else '000000')
            cell.fill.solid(); cell.fill.fore_color.rgb = rgb('000000' if hd else ('F2F2F2' if heavy else 'FFFFFF'))
    # takeaways
    for k, (big, small) in enumerate(takeaways):
        x = 620 + k * 316
        tx(s, x, 440, 300, 50, big, 30, True); tx(s, x, 492, 300, 70, small, 12, color='404040')
    tx(s, 36, 676, 1208, 20, '*2026 = partial year (to Aug). Source: Indonesia import records, knuckle boom cranes; Txn = import transactions; value in USD.', 9, color='6B6B6B')
    return s
fq = lambda v: f'{v:,}'.replace(',', '.')
fv = lambda v: f'${v / 1e6:,.2f} M'.replace('.', ',')
tq = {c: sum(TXN[c]) for c in CLS}; tv = {c: sum(VAL[c]) for c in CLS}; TQ = sum(tq.values()); TV = sum(tv.values())
s1 = slide(TXN, 'Heavy is only 75 of 764 units sold (10%)',
           f'Crane import transactions by class, 2023 – 2026* (100% = {TQ} units)', 'Txn', fq,
           [(f'{tq["Medium"] + tq["Heavy"]} units', f'Medium + Heavy = {(tq["Medium"] + tq["Heavy"]) / TQ:.0%} of {TQ} units'),
            (f'{tq["Heavy"]} units', f'Heavy = {tq["Heavy"] / TQ:.0%} of units; peak 39 units in 2025')])
s2 = slide(VAL, 'Heavy is 10% of units but 27% of value',
           f'Crane import value by class, 2023 – 2026* (100% = {fv(TV)})', 'USD', fv,
           [(f'{(tv["Medium"] + tv["Heavy"]) / TV:.0%} of value', f'Medium + Heavy = {fv(tv["Medium"] + tv["Heavy"])} from {(tq["Medium"] + tq["Heavy"]) / TQ:.0%} of units'),
            (f'{(tv["Heavy"] / tq["Heavy"]) / (tv["Light"] / tq["Light"]):.1f}x'.replace('.', ','), 'Heavy value per unit vs Light')])
P.save('QTY_vs_Value_2slides.pptx'); print(TQ, TV)
