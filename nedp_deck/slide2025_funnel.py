"""2025 funnel slide: market by class (Light/Small excluded) -> Medium brands treemap -> Heavy brands treemap."""
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from lxml import etree
FONT = 'Neue Haas Grotesk Text Pro'; E = lambda v: Emu(round(v * 9525)); rgb = RGBColor.from_string
ACC, GREY, LG = '1E9E57', '6B6B6B', 'BFBFBF'
FX = 16000  # assumed IDR per USD
CLS = ['Light', 'Small', 'Medium', 'Heavy']
import openpyxl as _ox, collections as _co
DB = 'data/Crane_Market_GVW_Pairing_v11_Noir.xlsx'   # single source of truth
_rows = [r for r in _ox.load_workbook(DB, data_only=True, read_only=True)['8. Pivot Source'].iter_rows(min_row=2, values_only=True) if r[4] == 2025]
ROWS25 = [(r[0], r[2], r[8] or 0, r[10] or 0) for r in _rows]          # brand, class, qty, value USD
U = {c: sum(q for b_, c_, q, v in ROWS25 if c_ == c) for c in CLS}
V = {c: sum(v for b_, c_, q, v in ROWS25 if c_ == c) for c in CLS}
COL = {'Light': 'E3E3E3', 'Small': 'C9C9C9', 'Medium': '1E9E57', 'Heavy': '0B4D2A'}
rp = lambda usd: f'Rp {usd * FX / 1e9:,.1f} Bio'.replace(',', '#').replace('.', ',').replace('#', '.')
TU = sum(U.values()); TV = sum(V.values()); MHU = U['Medium'] + U['Heavy']; MHV = V['Medium'] + V['Heavy']
def pareto(cls):
    """brands sorted by units (tie -> value); take brands until cumulative units >= 80%."""
    bu, bv = _co.Counter(), _co.Counter()
    for b_, c_, q, v in ROWS25:
        if c_ == cls: bu[b_] += q; bv[b_] += v
    order = sorted(bu, key=lambda k: (-bu[k], -bv[k])); top, cum = [], 0
    for k in order:
        top.append(k); cum += bu[k]
        if cum / U[cls] >= 0.8: break
    rest = [k for k in order if k not in top]
    return [(k, bu[k], bv[k]) for k in top], [(k, bu[k], bv[k]) for k in rest]
MTOP, MREST = pareto('Medium'); HTOP, HREST = pareto('Heavy')
NICE = lambda b_: b_.title().replace('Xcmg', 'XCMG').replace('Hiab', 'HIAB')
MED = [(NICE(k), u) for k, u, v in MTOP]; MED.append(('Others', U['Medium'] - sum(u for _, u in MED)))
HEV = [(NICE(k), u) for k, u, v in HTOP]; HEV.append(('Others', U['Heavy'] - sum(u for _, u in HEV)))
SHADE = ['0B4D2A', '1E9E57', '6FCF97', 'C7EFD5']


import io, openpyxl
def wb_live(chart, kind):
    """Embedded workbook: sheet 'Data2025' = 2025 rows from the database; chart cells = SUMIFS formulas on it."""
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Sheet1'
    d = wb.create_sheet('Data2025'); d.append(['Brand', 'Class', 'Qty', 'Value (USD)'])
    for r in ROWS25: d.append(list(r))
    n = len(ROWS25) + 1
    rngB, rngC, rngQ, rngV = f'Data2025!$A$2:$A${n}', f'Data2025!$B$2:$B${n}', f'Data2025!$C$2:$C${n}', f'Data2025!$D$2:$D${n}'
    if kind == 'chart1':
        for j, c in enumerate(CLS): ws.cell(1, 2 + j, c)
        ws['A2'] = cd_cats[0]; ws['A3'] = cd_cats[1]; ws['A9'] = 'FX (Rp per USD)'; ws['B9'] = FX
        for j, c in enumerate(CLS):
            col = openpyxl.utils.get_column_letter(2 + j)
            ws[f'{col}2'] = f'=SUMIFS({rngQ},{rngC},"{c}")'
            ws[f'{col}3'] = f'=ROUND(SUMIFS({rngV},{rngC},"{c}")*$B$9/1000000000,1)'
        ws['F1'] = 'Total'; ws['F2'] = '=SUM(B2:E2)'; ws['F3'] = '=SUM(B3:E3)'
        ws['G1'] = 'Medium+Heavy %'; ws['G2'] = '=(D2+E2)/F2'; ws['G3'] = '=(D3+E3)/F3'
    else:
        for j, nm in enumerate(BRANDS): ws.cell(1, 2 + j, nm)
        ws['A2'] = 'Medium'; ws['A3'] = 'Heavy'; ws['H1'] = 'Class total'; ws['I1'] = 'Top brands %'
        dmap = {'Medium': dict(MED), 'Heavy': dict(HEV)}
        for i, cls in ((2, 'Medium'), (3, 'Heavy')):
            for j, nm in enumerate(BRANDS[:-1]):
                col = openpyxl.utils.get_column_letter(2 + j)
                ws[f'{col}{i}'] = f'=SUMIFS({rngQ},{rngB},"{nm.upper()}",{rngC},"{cls}")' if dmap[cls].get(nm, 0) else 0
            ws[f'H{i}'] = f'=SUMIFS({rngQ},{rngC},"{cls}")'
            ws[f'F{i}'] = f'=H{i}-SUM(B{i}:E{i})'
            ws[f'I{i}'] = f'=SUM(B{i}:E{i})/H{i}'
        ws['A5'] = 'Brands shown = Pareto (cumulative units >= 80%). Others = class total minus brands shown.'
    bio = io.BytesIO(); wb.save(bio)
    chart.part.chart_workbook.update_from_xlsx_blob(bio.getvalue())

P = Presentation(); P.slide_width, P.slide_height = 12192000, 6858000
s = P.slides.add_slide(P.slide_layouts[6])
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
    l = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2)); l.line.color.rgb = rgb(c); l.line.width = Pt(w); return l
def rect(x, y, w, h, fill, line_c='FFFFFF', lw=1.5):
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    if fill: r.fill.solid(); r.fill.fore_color.rgb = rgb(fill)
    else: r.fill.background()
    r.line.color.rgb = rgb(line_c); r.line.width = Pt(lw); return r
def tile(x, y, w, h, fill, top, bottom, dark):
    r = rect(x, y, w, h, fill); tf = r.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = E(6); tf.margin_top = tf.margin_bottom = E(5); tf.vertical_anchor = MSO_ANCHOR.TOP
    c = 'FFFFFF' if dark else '000000'
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; rr = p.add_run(); rr.text = top
    rr.font.size = Pt(13); rr.font.bold = True; rr.font.name = FONT; rr.font.color.rgb = rgb(c)
    # bottom label as separate textbox anchored at bottom-left
    tx(x + 5, y + h - 40, w - 10, 36, [[(bottom, True, c)]], 10.5 if w > 70 else 8.5, anchor=MSO_ANCHOR.BOTTOM)
def treemap(x, y, w, h, brands):
    T = sum(b[1] for b in brands); sh = [b[1] / T for b in brands]
    w0 = w * sh[0]; tile(x, y, w0, h, SHADE[0], f'~{sh[0]:.0%}', f'{brands[0][0]}, {brands[0][1]}', True)
    rest = sum(sh[1:]); rw = w - w0
    h1 = h * sh[1] / rest; tile(x + w0, y, rw, h1, SHADE[1], f'~{sh[1]:.0%}', f'{brands[1][0]}, {brands[1][1]}', True)
    w2 = rw * sh[2] / (sh[2] + sh[3])
    tile(x + w0, y + h1, w2, h - h1, SHADE[2], f'~{sh[2]:.0%}', f'{brands[2][0]}, {brands[2][1]}', False)
    tile(x + w0 + w2, y + h1, rw - w2, h - h1, SHADE[3], f'~{sh[3]:.0%}', f'{brands[3][0]}, {brands[3][1]}', False)
def banner(x, w, text, fill):
    b = rect(x, 214, w, 26, fill, fill, 1); tf = b.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = text
    r.font.size = Pt(12); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = rgb('FFFFFF')

# ---------- header ----------
tx(36, 22, 200, 16, '10/18/2026', 11); tx(440, 22, 400, 16, 'Shaping the future of our industry', 11, PP_ALIGN.CENTER); tx(1144, 22, 100, 16, '13', 11, PP_ALIGN.RIGHT)
tx(36, 52, 900, 60, [[('Indonesian Import Folding Crane 2025', True, '000000')]], 34, anchor=MSO_ANCHOR.MIDDLE)
tx(940, 54, 304, 56, [[('Where is the value?', True, '000000')], [('And who holds it?', True, '000000')]], 16, PP_ALIGN.RIGHT)
line(28, 116, 1252, 116, '000000', 3)
tx(36, 122, 1208, 28, [[(f'Medium and Heavy are {MHU / TU:.0%} of units but {MHV / TV:.0%} of value; 3 brands hold 80%+ of each class', True, '000000')]], 19, anchor=MSO_ANCHOR.MIDDLE)
line(28, 152, 1252, 152)
tx(36, 157, 1208, 44, [[('In 2025, Medium and Heavy imports reached ', False, '000000'), (f'{MHU} units ({rp(MHV)})', True, '000000'),
    (f' out of {TU} units ({rp(TV)}). ', False, '000000'), (f'Three brands cover {sum(u for _, u, _ in MTOP) / U["Medium"]:.0%} of Medium and {sum(u for _, u, _ in HTOP) / U["Heavy"]:.0%} of Heavy units.', True, '000000')]], 14)
line(28, 204, 1252, 204)

# ---------- panel 1: market by class ----------
P1X, P1W = 36, 380
banner(P1X, P1W, 'Market 2025: focus on Medium & Heavy', '595959'); rect(P1X, 240, P1W, 412, None, '595959', 1.5)
tx(P1X + 12, 248, P1W - 24, 34, [[('Market size by class, 2025, ', True, '000000'), ('units vs value', False, '000000')]], 12)
cd_cats = [f'Units ({TU})', 'Value (Rp Bio)']
cd = CategoryChartData(); cd.categories = cd_cats
for c in CLS: cd.add_series(c, [U[c], round(V[c] * FX / 1e9, 1)])
CX, CY, CW, CH = P1X + 82, 286, 200, 330
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED_100, E(CX), E(CY), E(CW), E(CH), cd).chart
ch.has_legend = False; ch.font.name = FONT; ch.font.size = Pt(9)
pl = ch.plots[0]; pl.gap_width = 55; pl.overlap = 100
ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False
ca = ch.category_axis; ca.major_tick_mark = XL_TICK_MARK.NONE; ca.format.line.color.rgb = rgb('000000')
ca.tick_labels.font.size = Pt(10); ca.tick_labels.font.bold = True; ca.tick_labels.font.name = FONT
pa = ch._chartSpace.find('.//' + qn('c:plotArea')); lay = pa.find(qn('c:layout'))
if lay is None:
    lay = etree.Element(qn('c:layout')); pa.insert(0, lay)
lay.append(etree.fromstring('<c:manualLayout xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:layoutTarget val="inner"/>'
    '<c:xMode val="edge"/><c:yMode val="edge"/><c:x val="0"/><c:y val="0"/><c:w val="1"/><c:h val="0.9"/></c:manualLayout>'))
bc = ch._chartSpace.find('.//' + qn('c:barChart'))
bc.findall(qn('c:axId'))[0].addprevious(etree.fromstring('<c:serLines xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><c:spPr><a:ln w="6350"><a:solidFill><a:srgbClr val="7F7F7F"/></a:solidFill></a:ln></c:spPr></c:serLines>'))
for ser, c in zip(ch.series, CLS):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(COL[c]); ser.format.line.color.rgb = rgb('FFFFFF')
    dl = ser.data_labels; dl.font.size = Pt(9); dl.font.name = FONT; dl.font.bold = True
    dl.show_value = True; dl.show_series_name = True; dl.number_format = 'General'; dl.number_format_is_linked = False
    dl.font.color.rgb = rgb('FFFFFF' if c in ('Medium', 'Heavy') else '404040')
wb_live(ch, 'chart1')
PH = CH * 0.9; fy = lambda f: CY + PH * (1 - f)
ls = (U['Light'] + U['Small']) / TU; lsv = (V['Light'] + V['Small']) / TV
# left bracket: Light+Small excluded
bx = CX - 8
line(bx, fy(ls) + 2, bx, fy(0) - 2, GREY, 0.75); line(bx, fy(ls) + 2, bx + 5, fy(ls) + 2, GREY, 0.75); line(bx, fy(0) - 2, bx + 5, fy(0) - 2, GREY, 0.75)
tx(P1X + 8, (fy(ls) + fy(0)) / 2 - 26, bx - P1X - 14, 52, [[('Light +', False, GREY)], [('Small', False, GREY)], [('excluded', True, GREY)]], 9, PP_ALIGN.RIGHT)
line(bx, fy(1) + 2, bx, fy(ls) - 2, ACC, 1); line(bx, fy(1) + 2, bx + 5, fy(1) + 2, ACC, 1); line(bx, fy(ls) - 2, bx + 5, fy(ls) - 2, ACC, 1)
tx(P1X + 8, (fy(1) + fy(ls)) / 2 - 20, bx - P1X - 14, 40, [[(f'{MHU / TU:.0%}', True, ACC)], [(f'{MHU} units', False, '000000')]], 10, PP_ALIGN.RIGHT)
rx = CX + CW + 6
line(rx, fy(1) + 2, rx, fy(lsv) - 2, ACC, 1); line(rx, fy(1) + 2, rx - 5, fy(1) + 2, ACC, 1); line(rx, fy(lsv) - 2, rx - 5, fy(lsv) - 2, ACC, 1)
tx(rx + 6, (fy(1) + fy(lsv)) / 2 - 20, P1X + P1W - rx - 10, 40, [[(f'{MHV / TV:.0%}', True, ACC)], [(rp(MHV), False, '000000')]], 10)

# ---------- arrow (funnel) ----------
def arrow(x):
    a = s.shapes.add_shape(MSO_SHAPE.CHEVRON, E(x), E(420), E(18), E(36)); a.fill.solid(); a.fill.fore_color.rgb = rgb(ACC); a.line.fill.background()
arrow(421)

# ---------- panel 2: brand share bars (Medium top, Heavy bottom) ----------
PX, PW = 452, 792
banner(PX, PW, 'Medium & Heavy 2025: who holds the market', ACC); rect(PX, 240, PW, 412, None, ACC, 1.5)
BRANDS = ['Sany Palfinger', 'Palfinger', 'Amco Veba', 'XCMG', 'Others']
assert all(n in BRANDS for n, _ in MED + HEV), (MED, HEV)
BCOL = {'Sany Palfinger': '0B4D2A', 'Palfinger': '1E9E57', 'Amco Veba': '6FCF97', 'XCMG': '9ADBB5', 'Others': 'D9D9D9'}
dm, dh = dict(MED), dict(HEV)
tx(PX + 14, 250, 520, 20, [[('Brand share of units, Medium vs Heavy, 2025, ', True, '000000'), ('% of class units', False, '000000')]], 12)
tx(PX + 14, 270, 520, 18, [[(f"Medium = {U['Medium']} units ({rp(V['Medium'])})  ·  Heavy = {U['Heavy']} units ({rp(V['Heavy'])})", True, GREY)]], 10)
cd2 = CategoryChartData(); cd2.categories = ['Medium', 'Heavy']
for n in BRANDS: cd2.add_series(n, [dm.get(n, 0), dh.get(n, 0)])
ch2 = s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED_100, E(PX + 8), E(292), E(530), E(330), cd2).chart
ch2.font.name = FONT; ch2.font.size = Pt(10)
ch2.has_legend = False
from pptx.enum.chart import XL_LEGEND_POSITION
pl2 = ch2.plots[0]; pl2.gap_width = 45; pl2.overlap = 100
ch2.value_axis.visible = False; ch2.value_axis.has_major_gridlines = False
ca2 = ch2.category_axis; ca2.major_tick_mark = XL_TICK_MARK.NONE; ca2.reverse_order = True
ca2.tick_labels.font.size = Pt(12); ca2.tick_labels.font.bold = True; ca2.format.line.color.rgb = rgb('000000')
bc2 = ch2._chartSpace.find('.//' + qn('c:barChart'))
bc2.findall(qn('c:axId'))[0].addprevious(etree.fromstring('<c:serLines xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><c:spPr><a:ln w="6350"><a:solidFill><a:srgbClr val="7F7F7F"/></a:solidFill></a:ln></c:spPr></c:serLines>'))
for ser, n in zip(ch2.series, BRANDS):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(BCOL[n]); ser.format.line.color.rgb = rgb('FFFFFF')
    dl = ser.data_labels; dl.font.size = Pt(10); dl.font.name = FONT; dl.font.bold = True
    dl.show_value = True; dl.show_series_name = True; dl.number_format = '0" units";;;'; dl.number_format_is_linked = False
    dl.font.color.rgb = rgb('FFFFFF' if BCOL[n] in ('0B4D2A', '1E9E57') else '000000'); dl.font.size = Pt(9)
    dls = dl._element
    sep = dls.find(qn('c:separator'))
    if sep is None:
        sep = etree.SubElement(dls, qn('c:separator'))
        dls.find(qn('c:showLeaderLines')) is not None and dls.find(qn('c:showLeaderLines')).addnext(sep)
    sep.text = '\n'
    # hide label where the brand has 0 units in that class
    for k, v in enumerate([dm.get(n, 0), dh.get(n, 0)]):
        if v == 0:
            d = etree.fromstring(f'<c:dLbl xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:idx val="{k}"/><c:delete val="1"/></c:dLbl>')
            dls.insert(0, d)
wb_live(ch2, 'chart2')
# explanation boxes, aligned to the two bars
def vshare(top, cls): return sum(v for _, _, v in top) / V[cls]
def names(top): return ', '.join(NICE(k) for k, _, _ in top[:-1]) + ' and ' + NICE(top[-1][0])
MR = ', '.join(f'{NICE(k)} {u}' for k, u, v in MREST); HR = ', '.join(f'{NICE(k)} {u}' for k, u, v in HREST)
NOTES = {
 'Medium': [[(f'{len(MTOP)} brands = {sum(u for _, u, _ in MTOP) / U["Medium"]:.0%} of units', True, ACC), (f' ({sum(u for _, u, _ in MTOP)} of {U["Medium"]}) and {vshare(MTOP, "Medium"):.0%} of value: {names(MTOP)}.', False, '000000')],
            [('Sany Palfinger', True, '000000'), (f' alone holds {dict(MED)["Sany Palfinger"]} units ({dict(MED)["Sany Palfinger"] / U["Medium"]:.0%}).', False, '000000')],
            [('Others: ', True, GREY), (MR + '.', False, GREY)]],
 'Heavy':  [[(f'{len(HTOP)} brands = {sum(u for _, u, _ in HTOP) / U["Heavy"]:.0%} of units', True, ACC), (f' ({sum(u for _, u, _ in HTOP)} of {U["Heavy"]}) and {vshare(HTOP, "Heavy"):.0%} of value: {names(HTOP)}.', False, '000000')],
            [('Palfinger', True, '000000'), (f' alone holds {dict(HEV)["Palfinger"]} units ({dict(HEV)["Palfinger"] / U["Heavy"]:.0%}).', False, '000000')],
            [('Others: ', True, GREY), (HR + '.', False, GREY)]]}
LOGO = {k: f'assets/logos/brands/{v}.png' for k, v in {'SANY PALFINGER': 'sany_palfinger', 'PALFINGER': 'palfinger', 'XCMG': 'xcmg', 'AMCO VEBA': 'amco_veba', 'HIAB': 'hiab', 'FASSI': 'fassi'}.items()}
ex = PX + 548
for k, cls in enumerate(['Medium', 'Heavy']):
    y = 300 + k * 148
    rect(ex, y, PW - 562, 142, 'F2F2F2', 'F2F2F2', 0.5)
    tx(ex + 10, y + 5, 60, 14, [[(cls, True, '000000')]], 9.5)
    # Pareto brand logos (from earlier F.lli Ferrari deck), in rank order
    from PIL import Image as _Im
    fs = [LOGO[k_] for k_, _, _ in (MTOP if cls == 'Medium' else HTOP) if k_ in LOGO]
    ws_ = [_Im.open(f).size for f in fs]; avail = PW - 582 - 6 * (len(fs) - 1)
    h_ = min(18, avail / sum(w / h for w, h in ws_)); lx = ex + 10
    for f, (w, h) in zip(fs, ws_):
        s.shapes.add_picture(f, E(lx), E(y + 22 + (18 - h_) / 2), height=E(h_)); lx += h_ * w / h + 6
    tx(ex + 10, y + 46, PW - 582, 94, NOTES[cls], 9)

# ---------- footer ----------
tx(36, 662, 1208, 16, [[('Source: ', True, '000000'), ('Crane Market GVW Pairing v11 (Noir), sheet 8. Pivot Source, 2025 rows; value converted from USD at assumed Rp 16.000/USD (Bio = billion).', False, '000000')]], 10)
tx(36, 680, 1208, 16, [[('Note: ', True, GREY), ('Chart data = SUMIFS on 2025 database rows (Edit Data). Brands shown until 80% of class units (Pareto); Others = rest. Light (< 8 tm) and Small (8–25 tm) excluded from focus.', False, GREY)]], 10)
line(28, 700, 1252, 700, ACC, 1)
P.save('Slide_2025_Medium_Heavy_Funnel.pptx'); print(TU, rp(TV), MHU, rp(MHV), MED, HEV)
