"""Crane deck slide 1, in the user's 'Indonesian Import Folding Crane 23-26' style: units per year by class + units/value/share columns with braces."""
import copy, sys
sys.path.insert(0, '.')
import crane_data as d
from lxml import etree
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.chart.data import CategoryChartData
from pptx.oxml.ns import qn
E = lambda v: Emu(round(v * 9525)); rgb = RGBColor.from_string; FONT = 'Neue Haas Grotesk Text Pro'
num = lambda x, n=1: f'{x:,.{n}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
COL = {'Light': 'CDEFD9', 'Small': '74CC95', 'Medium': '1E9E57', 'Heavy': '0B4D2A'}
DARK = {'Medium', 'Heavy'}; G = '1E9E57'
LEG = {'Light': 'Light (≤ 8 tm)', 'Small': 'Small (8–25 tm)', 'Medium': 'Medium (25–45 tm)', 'Heavy': 'Heavy (> 45 tm)'}

U, V = d.by_year(); YRS = [2023, 2024, 2025, 2026]
TU = sum(U.values()); TV = sum(V.values()) / 1e9
cu = {c: sum(U[(y, c)] for y in YRS) for c in d.CLS}; cv = {c: sum(V[(y, c)] for y in YRS) / 1e9 for c in d.CLS}
avg_u = lambda cs: sum(U[(y, c)] for y in YRS[:3] for c in cs) / 3
avg_v = lambda cs: sum(V[(y, c)] for y in YRS[:3] for c in cs) / 3 / 1e9
LS, MH = ('Light', 'Small'), ('Medium', 'Heavy')
ls_u = sum(cu[c] for c in LS) / TU; mh_v = sum(cv[c] for c in MH) / TV

P = Presentation('v7/6M_V9.pptx'); L = P.slides._sldIdLst
for i, sid in reversed(list(enumerate(list(L)))):
    if i != 13: P.part.drop_rel(sid.rId); L.remove(sid)
src = P.slides[0]; s = P.slides.add_slide(src.slide_layout)
for ph in list(s.placeholders): ph._element.getparent().remove(ph._element)
for sh in src.shapes:
    if sh.name in ('Date Placeholder 3', 'Slide Number Placeholder 5', 'Title 10', 'Group 31', 'Straight Connector 34', 'Table 2'):
        s.shapes._spTree.append(copy.deepcopy(sh._element))
P.part.drop_rel(L[0].rId); L.remove(L[0])
def set_runs(par, text):
    rs = par.runs; rs[0].text = text
    for r in rs[1:]: r._r.getparent().remove(r._r)
SH = {sh.name: sh for sh in s.shapes}
# title + question (question moved right, group widened to the slide edge)
grp = SH['Group 31']; xf = grp._element.find('.//' + qn('a:xfrm'))
for tag in ('a:ext', 'a:chExt'): xf.find(qn(tag)).set('cx', str(E(1242 - 36.45)))
for c in grp.shapes:
    if 'Medium' in c.text_frame.text: set_runs(c.text_frame.paragraphs[0], 'Indonesian Import Folding Crane 23-26/'); c.width = E(930)
    else:
        tf = c.text_frame; ps = tf.paragraphs
        set_runs(ps[0], 'How big is the market?'); r0_ = ps[0].runs[0]._r
        br = etree.SubElement(ps[0]._p, qn('a:br')); ps[0]._p.remove(br); r0_.addnext(br)
        if r0_.find(qn('a:rPr')) is not None: br.append(copy.deepcopy(r0_.find(qn('a:rPr'))))
        r1_ = copy.deepcopy(r0_); br.addnext(r1_); r1_.find(qn('a:t')).text = 'And how much sells each year?'
        c.left = E(900); c.width = E(342)
t2 = SH['Table 2'].table
set_runs(t2.cell(0, 0).text_frame.paragraphs[0], 'Every class buys every year: Light & Small bring the volume, Medium & Heavy bring the value')
p1 = t2.cell(1, 0).text_frame.paragraphs[0]; r0 = p1.runs[0]
for r in p1.runs[1:]: r._r.getparent().remove(r._r)
parts = [('From 2023 to 2026, Indonesia imported ', False), (f'{TU} folding cranes (Rp {num(TV)} Bio)', True), (', about ', False),
         (f'{avg_u(d.CLS):.0f} units (Rp {num(avg_v(d.CLS))} Bio) a year', True), ('. Light & Small make up ', False), (f'{ls_u:.0%} of units', True),
         (', while Medium & Heavy hold ', False), (f'{mh_v:.0%} of value', True), ('.', False)]
r0.text = parts[0][0]; r0.font.bold = False; prev = r0._r
for t, b in parts[1:]:
    nr = copy.deepcopy(r0._r); prev.addnext(nr); prev = nr
for r, (t, b) in zip(p1.runs, parts): r.text = t; r.font.bold = b

def tx(x, y, w, h, paras, sz=11, al=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    b = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
    for k, para in enumerate(paras):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph(); p.alignment = al
        for t, bold, c, *z in para:
            r = p.add_run(); r.text = t; r.font.size = Pt(z[0] if z else sz); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = rgb(c)
    return b
def box(x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, lw=1):
    b = s.shapes.add_shape(shape, E(x), E(y), E(w), E(h)); b.shadow.inherit = False
    if fill: b.fill.solid(); b.fill.fore_color.rgb = rgb(fill)
    else: b.fill.background()
    if line: b.line.color.rgb = rgb(line); b.line.width = Pt(lw)
    else: b.line.fill.background()
    return b
def line(x1, y1, x2, y2, color='7F7F7F', w=1):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2)); c.line.color.rgb = rgb(color); c.line.width = Pt(w); return c
def manual(ch, PX, PY, PW, PH):
    pa = ch._chartSpace.find('.//' + qn('c:plotArea')); lay = pa.find(qn('c:layout'))
    if lay is None: lay = etree.SubElement(pa, qn('c:layout')); pa.remove(lay); pa.insert(0, lay)
    lay.append(etree.fromstring(f'<c:manualLayout xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:layoutTarget val="inner"/><c:xMode val="edge"/><c:yMode val="edge"/>'
                                f'<c:x val="{PX}"/><c:y val="{PY}"/><c:w val="{PW}"/><c:h val="{PH}"/></c:manualLayout>'))
def ser_lines(ch):
    bc = ch._chartSpace.find('.//' + qn('c:barChart'))
    sl = etree.SubElement(bc, qn('c:serLines')); bc.remove(sl); bc.find(qn('c:overlap')).addnext(sl)
    ln = etree.SubElement(etree.SubElement(sl, qn('c:spPr')), qn('a:ln'), w='6350'); etree.SubElement(etree.SubElement(ln, qn('a:solidFill')), qn('a:srgbClr'), val='808080')
def base_chart(x, y, w, h, cats, data, ctype, gap):
    cd = CategoryChartData(); cd.categories = cats
    for c in d.CLS: cd.add_series(LEG[c], data[c], number_format='0')
    ch = s.shapes.add_chart(ctype, E(x), E(y), E(w), E(h), cd).chart
    ch.has_legend = False; ch.has_title = False; ch.plots[0].gap_width = gap; ch.plots[0].overlap = 100; ser_lines(ch)
    va = ch.value_axis; va.visible = False; va.has_major_gridlines = False
    ca = ch.category_axis; ca.tick_labels.font.size = Pt(10.5); ca.tick_labels.font.name = FONT; ca.format.line.color.rgb = rgb('404040')
    for k, c in enumerate(d.CLS):
        se = ch.plots[0].series[k]; se.format.fill.solid(); se.format.fill.fore_color.rgb = rgb(COL[c])
    return ch
def legend(x, y, step):
    for i, c in enumerate(d.CLS):
        box(x + i * step, y + 2, 10, 10, COL[c]); tx(x + i * step + 14, y, step - 14, 14, [[(LEG[c], False, '000000', 10.5)]])

# ================= left panel =================
tx(36, 252, 580, 18, [[('Imported folding cranes by class per year, 2023 – 2026', True, '000000', 12.5)]], al=PP_ALIGN.CENTER)
h23, h25 = U[(2023, 'Heavy')], U[(2025, 'Heavy')]; l23, l25 = U[(2023, 'Light')], U[(2025, 'Light')]
tot25 = sum(U[(2025, c)] for c in d.CLS)
tx(210, 274, 410, 40, [[('Heavy almost ', False, '000000', 11.5), (f'tripled from {h23} to {h25} units in 2025', True, G, 11.5),
                         (f' ({h25 / tot25:.0%} of that year), while ', False, '000000', 11.5), (f'Light fell from {l23} to {l25}', True, G, 11.5), ('.', False, '000000', 11.5)]])
CX, CY, CW, CH = 36, 312, 470, 322; PX, PY, PW, PH = .01, .03, .98, .88; VMAX = 205
ch = base_chart(CX, CY, CW, CH, ['2023', '2024', '2025', '2026*'], {c: [U[(y, c)] for y in YRS] for c in d.CLS}, XL_CHART_TYPE.COLUMN_STACKED, 75)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = VMAX; manual(ch, PX, PY, PW, PH)
for k, c in enumerate(d.CLS):
    dl = ch.plots[0].series[k].data_labels; dl.show_value = True; dl.number_format = '0'; dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.CENTER; dl.font.size = Pt(12); dl.font.bold = True; dl.font.name = FONT
    dl.font.color.rgb = rgb('FFFFFF' if c in DARK else '000000')
    for j, y in enumerate(YRS):
        if U[(y, c)] < 4:
            ch.plots[0].series[k]._element.find(qn('c:dLbls')).insert(0, etree.fromstring(
                f'<c:dLbl xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:idx val="{j}"/><c:delete val="1"/></c:dLbl>'))
x0, y0, pw, ph = CX + CW * PX, CY + CH * PY, CW * PW, CH * PH; catW = pw / 4
for j, y in enumerate(YRS):
    t = sum(U[(y, c)] for c in d.CLS); cx = x0 + catW * (j + .5)
    tx(cx - 40, y0 + ph * (1 - t / VMAX) - 17, 80, 15, [[(f'{t} units', True, '404040', 10)]], al=PP_ALIGN.CENTER)
# average box (right of the bars)
AX = 514
tx(AX, 330, 104, 30, [[('Avg sales / year', True, '000000', 9.5)], [('Light & Small', True, '000000', 9.5)]], al=PP_ALIGN.CENTER)
line(AX, 362, AX + 104, 362, '404040', .75)
tx(AX, 366, 104, 30, [[(f'{avg_u(LS):.0f} units', True, G, 11)], [(f'Rp {num(avg_v(LS))} Bio', True, G, 11)]], al=PP_ALIGN.CENTER)
tx(AX, 410, 104, 30, [[('Avg sales / year', True, '000000', 9.5)], [('Medium & Heavy', True, '000000', 9.5)]], al=PP_ALIGN.CENTER)
line(AX, 442, AX + 104, 442, '404040', .75)
tx(AX, 446, 104, 30, [[(f'{avg_u(MH):.0f} units', True, G, 11)], [(f'Rp {num(avg_v(MH))} Bio', True, G, 11)]], al=PP_ALIGN.CENTER)
tx(AX, 486, 104, 30, [[('Average of full years 2023 – 2025', False, '595959', 8)]], al=PP_ALIGN.CENTER)
legend(40, 640, 145)
nb = box(36, 662, 580, 20, None, '000000', lw=.75)
tx(44, 665, 566, 16, [[('Ton-meter classes follow the Application Engineering classification. *2026 = Jan – 14 Aug only.', False, '000000', 9)]])

# ================= divider =================
line(630, 250, 630, 686, G, 2.25)
o = box(616, 452, 28, 28, G, None, MSO_SHAPE.OVAL); tf = o.text_frame
for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = '>'; r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = rgb('FFFFFF'); r.font.name = FONT

# ================= right panel =================
tx(650, 252, 592, 18, [[('Imported folding cranes by class, Jan 2023 – 14 Aug 2026', True, '000000', 12.5)]], al=PP_ALIGN.CENTER)
MX, MY, MW, MHh = 736, 276, 420, 358; QX, QY, QW, QH = .02, .02, .96, .89
shr = {c: [cu[c] / TU, cv[c] / TV, cv[c] / TV] for c in d.CLS}
ch = base_chart(MX, MY, MW, MHh, ['Units (qty)', 'Value (IDR)', 'Units → value'], shr, XL_CHART_TYPE.COLUMN_STACKED_100, 40)
manual(ch, QX, QY, QW, QH)
for k, c in enumerate(d.CLS):
    se = ch.plots[0].series[k]
    labels = [f'{cu[c]} units\n{cu[c] / TU:.0%}', f'Rp {num(cv[c])} Bio\n{cv[c] / TV:.0%}', f'{cu[c] / TU:.0%} → {cv[c] / TV:.0%}']
    for j, t in enumerate(labels):
        dl = se.points[j].data_label; dl.position = XL_LABEL_POSITION.CENTER; tf = dl.text_frame
        for li, part in enumerate(t.split('\n')):
            p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
            rr = p.add_run(); rr.text = part; rr.font.size = Pt(10.5); rr.font.bold = True; rr.font.name = FONT
            rr.font.color.rgb = rgb('FFFFFF' if c in DARK else '000000')
qx0, qy0, qw, qh = MX + MW * QX, MY + MHh * QY, MW * QW, MHh * QH; qcat = qw / 3; bw = qcat / 1.4
ub_l = qx0 + qcat * .5 - bw / 2; sb_r = qx0 + qcat * 2.5 + bw / 2
mh_u = 1 - ls_u; y_u = qy0 + qh * mh_u; y_v = qy0 + qh * mh_v; ybot = qy0 + qh
box(ub_l - 18, qy0, 12, y_u - qy0 - 3, None, G, MSO_SHAPE.LEFT_BRACE, 1.5)
box(ub_l - 18, y_u + 3, 12, ybot - y_u - 3, None, '000000', MSO_SHAPE.LEFT_BRACE, 1.5)
box(sb_r + 6, qy0, 12, y_v - qy0 - 3, None, G, MSO_SHAPE.RIGHT_BRACE, 1.5)
box(sb_r + 6, y_v + 3, 12, ybot - y_v - 3, None, '000000', MSO_SHAPE.RIGHT_BRACE, 1.5)
def callout(x, yc, w, big, rest, color):
    h = 28 + 13.5 * len(rest); b = box(x, yc - h / 2, w, h, 'FFFFFF', 'BFBFBF', lw=.75)
    tx(x + 3, yc - h / 2 + 4, w - 6, h - 6, [[(big, True, color, 12)]] + [[(t, False, '000000', 8.5)] for t in rest], al=PP_ALIGN.CENTER)
vmh = sum(cv[c] for c in MH); vls = sum(cv[c] for c in LS)
callout(648, (qy0 + y_u) / 2, 82, f'{mh_u:.0%}', ['of total units', 'from Medium', '& Heavy'], G)
callout(648, (y_u + ybot) / 2, 82, f'{ls_u:.0%}', ['of total units', 'from Light', '& Small'], '000000')
callout(1160, (qy0 + y_v) / 2, 82, f'{mh_v:.0%}', ['of total value', f'(Rp {num(vmh)} Bio)', 'from Medium', '& Heavy'], G)
callout(1160, (y_v + ybot) / 2, 82, f'{1 - mh_v:.0%}', ['of total value', f'(Rp {num(vls)} Bio)', 'from Light', '& Small'], '000000')
legend(660, 640, 145)
bn = box(736, 662, 420, 20, 'FFFFFF', 'BFBFBF', lw=.75)
tx(736, 665, 420, 16, [[('Light & Small bring the volume, Medium & Heavy bring the value', True, G, 10)]], al=PP_ALIGN.CENTER)
tx(36, 692, 1206, 22, [[('Source: Indonesia import records (Crane Market GVW Pairing v11, Noir), Jan 2023 – 14 Aug 2026. Folding cranes only; excludes the Noir "Excluded Rows", Hyva, Zoomlion, '
    'HIAB XG grabbers, Tadano TM-Z telescopic and 2 invalid-price records. Value before tax × Rp 17.803/USD (JISDOR 23 Sep 2026).', False, '7F7F7F', 6.5)]])
P.save('v7/CR1_Market_Size.pptx'); print('ok', TU, round(TV, 1), round(avg_u(LS)), round(avg_v(LS), 1), round(avg_u(MH)), round(avg_v(MH), 1), f'{ls_u:.3f} {mh_v:.3f}')
