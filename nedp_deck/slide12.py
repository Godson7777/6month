"""Slide 12 rebuilt in 'market review' style: annotated charts, database figures (764 units, USD)."""
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from lxml import etree
FONT = 'Neue Haas Grotesk Text Pro'; E = lambda v: Emu(round(v * 9525)); rgb = RGBColor.from_string
CLS = ['Light', 'Small', 'Medium', 'Heavy']; YRS = ['2023', '2024', '2025', '2026*']
NM = {'Light': 'Light (< 8 tm)', 'Small': 'Small (8–25 tm)', 'Medium': 'Medium (25–45 tm)', 'Heavy': 'Heavy (> 45 tm)'}
TXN = {'Light': [109, 52, 53, 34], 'Small': [68, 52, 75, 28], 'Medium': [74, 70, 60, 14], 'Heavy': [16, 17, 39, 3]}
VAL = {'Light': 3019087, 'Small': 5037297, 'Medium': 7304431, 'Heavy': 5712582}   # USD, 2023-2026*
COL = {'Light': 'C7EFD5', 'Small': '6FCF97', 'Medium': '1E9E57', 'Heavy': '0B4D2A'}
ACC = '1E9E57'; GREY = '6B6B6B'
U = {c: sum(TXN[c]) for c in CLS}; TU = sum(U.values()); TV = sum(VAL.values())
YT = [sum(TXN[c][k] for c in CLS) for k in range(4)]
su = {c: U[c] / TU for c in CLS}; sv = {c: VAL[c] / TV for c in CLS}
FX = 16000  # assumed IDR per USD - change here
usd = lambda v: f'Rp {v * FX / 1e9:,.1f} Bio'.replace(',', '#').replace('.', ',').replace('#', '.')
MH_U = U['Medium'] + U['Heavy']; MH_V = VAL['Medium'] + VAL['Heavy']

P = Presentation(); P.slide_width, P.slide_height = 12192000, 6858000
s = P.slides.add_slide(P.slide_layouts[6])

def tx(x, y, w, h, parts, sz=12, al=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """parts: str or list of paragraphs; each paragraph = list of (text, bold, color)."""
    b = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tf = b.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
    if isinstance(parts, str): parts = [[(parts, False, '000000')]]
    for i, para in enumerate(parts):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = al
        for t, bold, c in para:
            r = p.add_run(); r.text = t; r.font.size = Pt(sz); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = rgb(c)
    return b
def line(x1, y1, x2, y2, c='000000', w=1.0, dash=False):
    l = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
    l.line.color.rgb = rgb(c); l.line.width = Pt(w)
    if dash:
        from pptx.enum.dml import MSO_LINE
        l.line.dash_style = MSO_LINE.DASH
    return l
def box(x, y, w, h, fill):
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    r.fill.solid(); r.fill.fore_color.rgb = rgb(fill); r.line.fill.background(); return r
def legend(x, y):
    for c in CLS:
        box(x, y + 3, 10, 10, COL[c]); tx(x + 14, y, 130, 16, NM[c], 10); x += 140
def bracket(x, y1, y2, side='right', c='000000'):
    """vertical bracket with ticks; ticks point toward the chart."""
    d = -6 if side == 'right' else 6
    line(x, y1, x, y2, c, 0.75); line(x, y1, x + d, y1, c, 0.75); line(x, y2, x + d, y2, c, 0.75)
def chart(kind, x, y, w, h, cats, series, gap):
    cd = CategoryChartData(); cd.categories = cats
    for name, vals in series: cd.add_series(name, vals)
    ch = s.shapes.add_chart(kind, E(x), E(y), E(w), E(h), cd).chart
    ch.has_legend = False; ch.font.name = FONT; ch.font.size = Pt(12)
    pl = ch.plots[0]; pl.gap_width = gap; pl.overlap = 100
    ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False
    ca = ch.category_axis; ca.tick_labels.font.size = Pt(12); ca.tick_labels.font.name = FONT
    ca.format.line.color.rgb = rgb('000000'); ca.has_major_gridlines = False
    from pptx.enum.chart import XL_TICK_MARK
    ca.major_tick_mark = XL_TICK_MARK.NONE
    # plot area fills the frame except a strip for category labels -> known bar positions
    pa = ch._chartSpace.find('.//' + qn('c:plotArea'))
    lay = pa.find(qn('c:layout'))
    if lay is None:
        lay = etree.SubElement(pa, qn('c:layout')); pa.remove(lay); pa.insert(0, lay)
    lay.append(etree.fromstring('<c:manualLayout xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart">'
        '<c:layoutTarget val="inner"/><c:xMode val="edge"/><c:yMode val="edge"/>'
        '<c:x val="0"/><c:y val="0"/><c:w val="1"/><c:h val="0.92"/></c:manualLayout>'))
    bc = ch._chartSpace.find('.//' + qn('c:barChart'))
    sl = etree.fromstring('<c:serLines xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><c:spPr><a:ln w="6350">'
        '<a:solidFill><a:srgbClr val="7F7F7F"/></a:solidFill></a:ln></c:spPr></c:serLines>')
    bc.findall(qn('c:axId'))[0].addprevious(sl)
    return ch
def style_series(ch, labels, sz=11):
    for ser, c in zip(ch.series, CLS):
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(COL[c]); ser.format.line.color.rgb = rgb('FFFFFF')
        dl = ser.data_labels; dl.font.size = Pt(sz); dl.font.name = FONT; dl.show_value = False
        for k, t in enumerate(labels[c]):
            if not t: continue
            tf = ser.points[k].data_label.text_frame; tf.text = t
            for p in tf.paragraphs:
                for r in p.runs:
                    r.font.bold = True; r.font.color.rgb = rgb('000000' if c in ('Light', 'Small') else 'FFFFFF')
def bar_x(x, w, n, gap, k):
    cw = w / n; bw = cw / (1 + gap / 100); return x + cw * k + (cw - bw) / 2, bw

# ---------- header (deck template) ----------
tx(36, 22, 200, 16, '10/18/2026', 11); tx(440, 22, 400, 16, 'Shaping the future of our industry', 11, PP_ALIGN.CENTER)
tx(1144, 22, 100, 16, '12', 11, PP_ALIGN.RIGHT)
tx(36, 52, 900, 60, [[('Indonesian Import Folding Crane 23-26', True, '000000')]], 36, anchor=MSO_ANCHOR.MIDDLE)
tx(940, 54, 304, 56, [[('How big the market is?', True, '000000')], [("And who's lead the market?", True, '000000')]], 16, PP_ALIGN.RIGHT)
line(28, 116, 1252, 116, '000000', 3)
tx(36, 122, 1208, 28, [[('Triatra Need To Focus on Medium and Heavy class', True, '000000')]], 19, anchor=MSO_ANCHOR.MIDDLE)
line(28, 152, 1252, 152, '000000', 1)
tx(36, 157, 1208, 44, [[('Medium and Heavy class contribute ', False, '000000'),
    (f'{MH_V / TV:.0%} ({usd(MH_V)} out of {usd(TV)})', True, '000000'),
    (' of the total market size from 2023 to 2026, while their transactions are just ', False, '000000'),
    (f'{MH_U / TU:.0%} ({MH_U} units out of {TU} units)', True, '000000'),
    (' of the total imported quantity.', False, '000000')]], 14)
line(28, 204, 1252, 204, '000000', 1)

# ---------- LEFT: units per year (absolute) ----------
tx(36, 214, 560, 36, [[('Imported folding cranes by class per year, ', True, '000000'), ('2023 – 2026*', True, '000000'),
                        (', n of units', False, '000000')]], 12)
legend(36, 250)
LX, LY, LW, LH, LG, MAX = 60, 300, 520, 330, 70, 350
ch = chart(XL_CHART_TYPE.COLUMN_STACKED, LX, LY, LW, LH, YRS, [(NM[c], TXN[c]) for c in CLS], LG)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = MAX
style_series(ch, {c: [str(v) if v >= 8 else '' for v in TXN[c]] for c in CLS})
PH = LH * 0.92; ypx = lambda v: LY + PH - v / MAX * PH
for k, t in enumerate(YT):
    bx, bw = bar_x(LX, LW, 4, LG, k)
    tx(bx - 10, ypx(t) - 22, bw + 20, 18, [[(str(t), True, '000000')]], 13, PP_ALIGN.CENTER)
# 2026 Heavy (3 units) label beside bar
bx, bw = bar_x(LX, LW, 4, LG, 3); tx(bx + bw + 4, ypx(YT[3]) - 4, 60, 14, [[('3 Heavy', True, COL['Heavy'])]], 9)
# bracket: 2023 -> 2025 Light decline
b0, w0 = bar_x(LX, LW, 4, LG, 0)
tx(LX - 2, LY - 2, 250, 14, '', 1)
# insight box (white space above short bars)
b1, w1 = bar_x(LX, LW, 4, LG, 1)
tx(b1 - 6, LY - 2, 400, 50, [[('Light fell from ', False, '000000'), ('109 to 52–53 units', True, ACC),
    (' after 2023, while ', False, '000000'), ('Heavy more than doubled', True, ACC), (' to ', False, '000000'),
    ('39 units in 2025', True, ACC), (' (17% of that year).', False, '000000')]], 12)
# right-side bracket on Total share
tx(bx + bw + 4, ypx(YT[3]) + 12, 52, 30, [[('*Jan–Aug', False, GREY)], [('only', False, GREY)]], 9)

# ---------- divider with ">" ----------
line(640, 220, 640, 650, ACC, 2)
c = s.shapes.add_shape(MSO_SHAPE.OVAL, E(624), E(420), E(32), E(32)); c.fill.solid(); c.fill.fore_color.rgb = rgb(ACC); c.line.fill.background()
tf = c.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
r = tf.paragraphs[0].add_run(); r.text = '>'; r.font.bold = True; r.font.size = Pt(16); r.font.name = FONT; r.font.color.rgb = rgb('FFFFFF')
tf.paragraphs[0].alignment = PP_ALIGN.CENTER; tf.vertical_anchor = MSO_ANCHOR.MIDDLE

# ---------- RIGHT: units vs value (100%) ----------
tx(664, 214, 580, 36, [[('Share of units vs value by class, ', True, '000000'), ('2023 – 2026*', True, '000000'),
                         (', % of total', False, '000000')]], 12)
legend(664, 250)
RX, RY, RW, RH, RG = 750, 300, 280, 330, 35
ch2 = chart(XL_CHART_TYPE.COLUMN_STACKED_100, RX, RY, RW, RH, [f'Units\n(n = {TU})', f'Value\n(= {usd(TV)})'],
            [(NM[c], [U[c], VAL[c] * FX / 1e9]) for c in CLS], RG)
style_series(ch2, {c: [f'{U[c]}\n{su[c]:.0%}', f'{usd(VAL[c])}\n{sv[c]:.0%}'] for c in CLS})
PH2 = RH * 0.92; yp = lambda f: RY + PH2 * (1 - f)
cum = {}; a = 0
for c_ in CLS: cum[c_] = (a, a + sv[c_]); a += sv[c_]
cumu = {}; a = 0
for c_ in CLS: cumu[c_] = (a, a + su[c_]); a += su[c_]
vx, vw = bar_x(RX, RW, 2, RG, 1); ux, uw = bar_x(RX, RW, 2, RG, 0)
# per-class callouts right of the Value bar
X0 = vx + vw + 14
for c_ in CLS:
    lo, hi = cum[c_]; bracket(X0, yp(hi) + 2, yp(lo) - 2, 'right')
    big = c_ in ('Medium', 'Heavy'); col = ACC if big else '000000'
    tx(X0 + 8, (yp(hi) + yp(lo)) / 2 - 16, 126, 34,
       [[(f'~{sv[c_]:.0%} {c_}', True, col)], [(f'from {su[c_]:.0%} of units', False, GREY)]], 11, anchor=MSO_ANCHOR.MIDDLE)
# Medium+Heavy bracket left of the Units bar
lo, hi = cumu['Medium'][0], cumu['Heavy'][1]; xb = ux - 12
bracket(xb, yp(hi) + 2, yp(lo) - 2, 'left')
tx(664, (yp(hi) + yp(lo)) / 2 - 34, xb - 672, 68,
   [[(f'~{MH_U / TU:.0%}', True, ACC)], [('Medium +', False, '000000')], [('Heavy', False, '000000')], [(f'{MH_U} units', False, GREY)]], 11, PP_ALIGN.RIGHT)
xr = X0 + 138; lo, hi = cum['Medium'][0], cum['Heavy'][1]; bracket(xr, yp(hi) + 2, yp(lo) - 2, 'right', ACC)
tx(xr + 8, (yp(hi) + yp(lo)) / 2 - 30, 1244 - xr - 8, 60, [[(f'~{MH_V / TV:.0%}', True, ACC)], [('of value', False, '000000')], [(usd(MH_V), False, GREY)]], 11)

# ---------- footer ----------
tx(36, 662, 1208, 16, [[('Source: ', True, '000000'), ('Indonesia import records 2023 – Aug 2026, knuckle boom (folding) cranes; value converted from USD at assumed Rp 16.000/USD (Bio = billion).', False, '000000')]], 10)
tx(36, 680, 1208, 16, [[('Note: ', True, GREY), ('*2026 = Jan–Aug. Application Engineering makes ton meter class classification to make easier identification class. Share may not add to 100% due to rounding.', False, GREY)]], 10)
line(28, 700, 1252, 700, ACC, 1)
P.save('Slide12_Market_Review_Style.pptx'); print(TU, TV, MH_U, MH_V, f'{MH_V/TV:.4f}', f'{MH_U/TU:.4f}')
