"""NEDP 6-month review, native PowerPoint build (Bitwise design guidance).
Every table is a real PowerPoint table, charts are native charts, boxes are shapes; pictures are only photos and logos.
Usage: python3 v4/build_native.py v4/NEDP_6M_Review_v4.pptx"""
import json, sys
from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt
from lxml import etree

ROOT = '/home/user/6month/nedp_deck/'
IMG = '/tmp/claude-0/v4img/'
DR = '/tmp/claude-0/dv2/img/'
PROD = ROOT + 'assets/products/'
K = 12192000 / 1280
def E(v): return Emu(round(v * K))

# Bitwise tokens
INK, BODY, MUTED, SUB, LINE, LINE2, WASH = '11181C', '4D555C', '697177', '889096', 'E6E8EB', 'D7DBDF', 'F9FAFB'
GREEN, GREEN_D, GREEN_L, GREEN_T = '22C96A', '076932', 'E1F9EC', '83E7AE'
AMB_L, AMB = 'FFF7C2', 'AB6400'
RED_L, RED = 'FEEBEC', 'CE2C31'
DARK, DARK2 = '11181C', '23343C'
SERIF, SANS = 'Georgia', 'Arial'
TOTAL = 18
rgb = lambda h: RGBColor.from_string(h)

P = Presentation(); P.slide_width, P.slide_height = 12192000, 6858000
BL = P.slide_layouts[6]


# ---------- primitives ----------
def rect(s, x, y, w, h, fill=None, line=None, radius=None, lw=0.75, dash=False):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    if radius: shp.adjustments[0] = min(.5, radius / min(w, h))
    if fill: shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill)
    else: shp.fill.background()
    if line:
        shp.line.color.rgb = rgb(line); shp.line.width = Pt(lw)
        if dash: shp.line.dash_style = 4
    else: shp.line.fill.background()
    _nostyle(shp)
    shp.text_frame.text = ''
    return shp


def _nostyle(shp):
    st = shp._element.find(qn('p:style'))
    if st is not None: shp._element.remove(st)


def grad(shp, c1, c2):
    shp.fill.gradient(); shp.fill.gradient_angle = 45
    st = shp.fill.gradient_stops; st[0].color.rgb = rgb(c1); st[1].color.rgb = rgb(c2)


def hline(s, x, y, w, color=LINE, lw=0.75):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x), E(y), E(x + w), E(y))
    _nostyle(c); c.line.color.rgb = rgb(color); c.line.width = Pt(lw); return c


def arrow(s, x1, y1, x2, y2, color=GREEN, lw=1.5):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
    _nostyle(c); c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
    ln = c.line._get_or_add_ln(); t = etree.SubElement(ln, qn('a:tailEnd')); t.set('type', 'triangle'); t.set('w', 'med'); t.set('len', 'med')
    return c


def runs_of(text, emph=True):
    if not emph: return [(text, False)]
    """'plain *italic* plain' -> [(txt, italic)]"""
    out = []
    for i, part in enumerate(text.split('*')):
        if part: out.append((part, i % 2 == 1))
    return out


def tx(s, x, y, w, h, text, size=11, color=INK, bold=False, font=SANS, align='l', anchor='t', italic_color=GREEN_D,
       spacing=None, caps=False, lh=None, wrap=True, bullets=False, emph=True):
    tb = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tf = tb.text_frame; tf.word_wrap = wrap
    for a in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, a, 0)
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    paras = text if isinstance(text, list) else [text]
    for i, ptxt in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        if lh: p.line_spacing = lh
        if bullets:
            pPr = p._p.get_or_add_pPr(); pPr.set('marL', str(int(Pt(10)))); pPr.set('indent', str(-int(Pt(10))))
            bu = etree.SubElement(pPr, qn('a:buChar')); bu.set('char', '•')
            if i: p.space_before = Pt(2)
        for t, it in runs_of(ptxt.upper() if caps else ptxt, emph):
            r = p.add_run(); r.text = t; f = r.font
            f.size = Pt(size); f.bold = bold; f.name = font; f.italic = it
            f.color.rgb = rgb(italic_color if it else color)
            if spacing: r._r.get_or_add_rPr().set('spc', str(int(spacing * 100)))
    return tb


def kicker(s, x, y, text, color=MUTED, w=600):
    return tx(s, x, y, w, 14, text, 8.5, color, True, caps=True, spacing=1.5, emph=False)


def pic(s, path, x, y, w=None, h=None, cover=True):
    """Place a picture; with w and h and cover=True it is cropped to fill, else fitted inside the box."""
    iw, ih = Image.open(path).size
    if w and h:
        if cover:
            p = s.shapes.add_picture(path, E(x), E(y), E(w), E(h))
            r_box, r_img = w / h, iw / ih
            if r_img > r_box: c = (1 - r_box / r_img) / 2; p.crop_left = p.crop_right = c
            else: c = (1 - r_img / r_box) / 2; p.crop_top = p.crop_bottom = c
            return p
        sc = min(w / iw, h / ih); pw, ph = iw * sc, ih * sc
        return s.shapes.add_picture(path, E(x + (w - pw) / 2), E(y + (h - ph) / 2), E(pw), E(ph))
    if w: return s.shapes.add_picture(path, E(x), E(y), width=E(w))
    return s.shapes.add_picture(path, E(x), E(y), height=E(h))


def round_pic(p, r=0.06):
    sp = p._element.spPr; g = sp.find(qn('a:prstGeom')); g.set('prst', 'roundRect')
    av = g.find(qn('a:avLst'))
    if av is None: av = etree.SubElement(g, qn('a:avLst'))
    gd = etree.SubElement(av, qn('a:gd')); gd.set('name', 'adj'); gd.set('fmla', f'val {int(r * 100000)}')


# ---------- native table ----------
def _border(cell, side, color, w=0.75):
    tcPr = cell._tc.get_or_add_tcPr()
    tag = {'L': 'a:lnL', 'R': 'a:lnR', 'T': 'a:lnT', 'B': 'a:lnB'}[side]
    for old in tcPr.findall(qn(tag)): tcPr.remove(old)
    ln = etree.SubElement(tcPr, qn(tag)); ln.set('w', str(int(Pt(w))))
    if color:
        sf = etree.SubElement(ln, qn('a:solidFill')); c = etree.SubElement(sf, qn('a:srgbClr')); c.set('val', color)
    else: etree.SubElement(ln, qn('a:noFill'))


def table(s, x, y, w, rows, colw, rowh=22, head=1, size=9, hsize=7.5, fills=None, styles=None, aligns=None, merges=(), group_row=False,
          grid=None, upper=True, hfill=None, hcolor=MUTED, rowhs=None):
    """rows: list of lists of str ('*x*' = green italic serif-free emphasis not used; '**' ignored).
    styles[(r,c)] = dict(bold, color, size, font) ; fills[r] = hex for whole row ; aligns[c] = 'l'|'r'|'c'"""
    nr, nc = len(rows), len(rows[0])
    gs = s.shapes.add_table(nr, nc, E(x), E(y), E(w), E(rowh * nr))
    tbl = gs.table
    tblPr = tbl._tbl.tblPr
    for a in ('firstRow', 'bandRow'): tblPr.set(a, '0')
    sid = tblPr.find(qn('a:tableStyleId'))
    if sid is None: sid = etree.SubElement(tblPr, qn('a:tableStyleId'))
    sid.text = '{5940675A-B579-460E-94D1-54222C63F5DA}'  # "No Style, Table Grid" -> we override borders
    tot = sum(colw)
    for i, cw in enumerate(colw): tbl.columns[i].width = E(w * cw / tot)
    for r in range(nr): tbl.rows[r].height = E(rowhs[r] if rowhs else rowh)
    for (r0, c0, r1, c1) in merges: tbl.cell(r0, c0).merge(tbl.cell(r1, c1))
    for r in range(nr):
        for c in range(nc):
            cell = tbl.cell(r, c)
            if cell.is_spanned:
                if grid:
                    for side in 'LRTB': _border(cell, side, grid if r >= head else LINE2)
                continue
            val = rows[r][c]; ishead = r < head
            cell.margin_left = cell.margin_right = Pt(4); cell.margin_top = cell.margin_bottom = Pt(2)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            st = (styles or {}).get((r, c), {})
            fill = st.get('fill') or (fills or {}).get(r) or (hfill if ishead else None)
            if st.get('anchor'): cell.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE}[st['anchor']]
            if fill: cell.fill.solid(); cell.fill.fore_color.rgb = rgb(fill)
            else: cell.fill.background()
            tf = cell.text_frame; tf.word_wrap = True
            lines = str(val).split('\n')
            for li, line in enumerate(lines):
                p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
                al = st.get('align') or (aligns or {}).get(c, 'l')
                p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[al]
                p.font.size = Pt(st.get('size', hsize if ishead else size))
                if not line: continue
                rr = p.add_run(); f = rr.font
                if ishead:
                    rr.text = line.upper() if upper else line; f.size = Pt(st.get('size', hsize)); f.bold = True; f.name = SANS
                    f.color.rgb = rgb(st.get('color', hcolor))
                    if upper: rr._r.get_or_add_rPr().set('spc', '50')
                else:
                    rr.text = line; f.name = st.get('font', SANS)
                    sub = li > 0 and st.get('sub', False)
                    f.size = Pt(st.get('size', size) - (1 if sub else 0)); f.bold = st.get('bold', False) and not sub
                    f.color.rgb = rgb(MUTED if sub else st.get('color', INK))
            if grid:
                for side in 'LRTB': _border(cell, side, LINE2 if ishead else grid)
            else:
                for side in 'LRT': _border(cell, side, None)
                _border(cell, 'B', INK if r == head - 1 else (LINE2 if ishead else LINE), 1.25 if r == head - 1 else 0.75)
            tcPr = cell._tc.get_or_add_tcPr()
            for fe in [e for e in tcPr if e.tag in (qn('a:solidFill'), qn('a:noFill'))]: tcPr.remove(fe); tcPr.append(fe)
            for p in tf.paragraphs:
                ep = etree.SubElement(p._p, qn('a:endParaRPr')); ep.set('sz', str(int(st.get('size', hsize if ishead else size) * 100)))
    return gs


# ---------- page chrome ----------
LOGO = ROOT + 'assets/cutout/triatra_logo.png'


def new(kick, head, lede=None):
    s = P.slides.add_slide(BL); n = len(P.slides)
    s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb('FFFFFF')
    pic(s, LOGO, 56, 24, h=22)
    tx(s, 640, 29, 584, 14, f'NEDP 6-MONTH REVIEW  ·  {kick.upper()}', 7.5, MUTED, align='r', spacing=1)
    hline(s, 56, 56, 1168)
    kicker(s, 56, 74, kick)
    tx(s, 56, 90, 1168, 40, head, 21, INK, font=SERIF)
    if lede: tx(s, 56, 132, 1168, 18, lede, 10.5, BODY)
    hline(s, 56, 692, 1168)
    tx(s, 56, 698, 600, 12, 'NEDP MID YEAR REVIEW 2026  ·  TIBERIAS K. SIMU', 7, SUB, True, spacing=1)
    tx(s, 1024, 698, 200, 12, f'{n:02d} / {TOTAL}', 7, SUB, True, align='r', spacing=1)
    return s


def divider(kick, head, sub):
    s = P.slides.add_slide(BL); n = len(P.slides)
    bg = rect(s, 0, 0, 1280, 720, DARK); grad(bg, DARK, DARK2)
    pic(s, LOGO, 64, 40, h=26)
    kicker(s, 64, 250, kick, GREEN_T)
    tx(s, 64, 272, 1150, 140, head, 40, 'FFFFFF', font=SERIF, italic_color=GREEN_T, lh=1.05)
    tx(s, 64, 420, 1000, 20, sub, 13, 'C1C8CD')
    hline(s, 64, 684, 1152, '30393E')
    tx(s, 64, 692, 600, 12, 'NEDP MID YEAR REVIEW 2026', 7, '7D868C', True, spacing=1)
    tx(s, 1016, 692, 200, 12, f'{n:02d} / {TOTAL}', 7, '7D868C', True, align='r', spacing=1)
    return s


def card(s, x, y, w, h, label=None, fill=WASH, line=None, dash=False, lcolor=MUTED):
    rect(s, x, y, w, h, fill, line, radius=10, dash=dash)
    if label: kicker(s, x + 14, y + 11, label, lcolor, w - 28)


# =====================================================================
# 01 divider
divider('Part 01 · Personal', 'Who I am and *what I bring* to Triatra.', 'About me  ·  Onboarding  ·  Company  ·  Role  ·  Project')

# 02 about me
s = new('Personal information', 'A management graduate now running *Small Suppeq and Truck Others*')
card(s, 56, 160, 300, 520, 'Profile', lcolor=GREEN_D)
tx(s, 70, 190, 280, 24, 'Tiberias Krisgaharu Simu', 14, INK, font=SERIF)
tx(s, 70, 216, 270, 16, 'PT Triatra Sinergia Pratama', 10, GREEN_D, True)
y = 256
for k, v in [('Position', 'Marketing Strategic 2 Associate'), ('Division', 'Marketing Unit & Strategic'), ('Products', 'Small Suppeq · Truck Others'),
             ('Place, date of birth', 'Kupang, 22 April 2001'), ('Phone', '0822 7222 2463')]:
    kicker(s, 70, y, k, SUB); tx(s, 70, y + 15, 270, 16, v, 10.5, INK); hline(s, 70, y + 40, 272); y += 54
card(s, 372, 160, 500, 96, 'Education')
pic(s, IMG + 'f2_1.png', 388, 190, 46, 46, cover=False)
tx(s, 446, 196, 410, 16, 'Universitas Sanata Dharma, Yogyakarta', 11, INK, True)
tx(s, 446, 214, 410, 14, 'Bachelor (S1) · Management · Faculty of Economics', 9, MUTED)
card(s, 372, 268, 500, 252, 'Work experience')
for i, (lg, a, b, yr, now) in enumerate([('f2_2.png', 'PT Triatra Sinergia Pratama', 'Marketing Strategic 2 Associate', '2026 – now', True),
                                         ('f2_3.png', 'Outlier', 'Team Lead Data Annotator', '2023 – 2025', False),
                                         ('f2_4.png', 'Krishma International', 'Marketing Coordinator', '2021 – 2023', False)]):
    yy = 298 + i * 72
    pic(s, IMG + lg, 388, yy, 56, 40, cover=False)
    tx(s, 456, yy + 4, 300, 16, a, 11, INK, True); tx(s, 456, yy + 21, 300, 14, b, 9, MUTED)
    rect(s, 770, yy + 8, 88, 22, GREEN if now else 'FFFFFF', None if now else GREEN, radius=11)
    tx(s, 770, yy + 8, 88, 22, yr, 8.5, 'FFFFFF' if now else GREEN_D, True, align='c', anchor='m')
    if i < 2: hline(s, 388, yy + 58, 470)
card(s, 372, 532, 500, 148, 'Organization')
pic(s, IMG + 'f2_5.png', 388, 568, 46, 46, cover=False)
tx(s, 446, 574, 300, 16, 'HMJM Universitas Sanata Dharma', 11, INK, True); tx(s, 446, 592, 300, 14, 'President', 9, MUTED)
rect(s, 770, 578, 88, 22, 'FFFFFF', GREEN, radius=11); tx(s, 770, 578, 88, 22, '2021 – 2022', 8.5, GREEN_D, True, align='c', anchor='m')
p = pic(s, IMG + 'f2_6.png', 888, 160, 336, 520); round_pic(p, .04)

# 03 onboarding
s = new('Onboarding journey', 'Two programs built my base; *AHEMCE* comes next')
cols = [('Basic Technical Course', 'DONE', ['s3_4.jpg', 's3_5.jpg'], ['Engine basics', 'Electrical system', 'Axle, wheel and suspension', 'Final drive and undercarriage']),
        ('B-One · Orientation', 'DONE', ['s3_7.jpg', 's3_6.jpg'], ['8 Astra competencies', 'AI at work', 'Teamwork', 'Corporate bootcamp']),
        ('AHEMCE', 'NEXT', None, ['Heavy equipment', 'Mining', 'Contracting', 'Energy'])]
cw = (1168 - 2 * 24) / 3
hline(s, 56 + 22, 176, 1168 - 44, LINE2, 1.25)
for i, (t, st, ph, L) in enumerate(cols):
    x = 56 + i * (cw + 24); nxt = st == 'NEXT'
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, E(x + 14), E(170), E(12), E(12))
    dot.fill.solid(); dot.fill.fore_color.rgb = rgb('FFFFFF' if nxt else GREEN); dot.line.color.rgb = rgb(GREEN); dot.line.width = Pt(1.5)
    card(s, x, 196, cw, 484, None, 'FFFFFF' if nxt else WASH, LINE2 if nxt else None, dash=nxt)
    tx(s, x + 16, 210, cw - 80, 22, t, 15, INK, font=SERIF)
    tx(s, x + cw - 66, 214, 50, 14, st, 7.5, GREEN_D, True, align='r', spacing=1)
    if ph:
        pw = (cw - 32 - 8) / 2
        for j, f in enumerate(ph):
            p = pic(s, DR + f, x + 16 + j * (pw + 8), 244, pw, 300); round_pic(p, .04)
    else:
        tx(s, x + 16, 330, cw - 32, 90, 'Astra Heavy Equipment, Mining, Construction and Energy', 20, BODY, font=SERIF, lh=1.15)
    kicker(s, x + 16, 560, 'What I learned' if not nxt else 'What I will learn', SUB)
    tx(s, x + 16, 578, cw - 32, 96, L, 10.5, BODY, bullets=True)

# 04 company
s = new('Company profile', 'Triatra sells *PATRIA and ULTRA* to four industries for the UTPE group')
kicker(s, 56, 158, 'Corporate entity structure')
chain = [('f5_1.png', 'Astra International', 'Heavy Equipment, Mining, Construction and Energy'),
         ('f5_2.png', 'United Tractors', 'Construction machinery'), ('f5_3.png', 'UTPE', 'Engineering solution and marine')]
for i, (lg, a, b) in enumerate(chain):
    yy = 178 + i * 70
    rect(s, 56, yy, 540, 52, 'FFFFFF', LINE, radius=8)
    pic(s, IMG + lg, 68, yy + 8, 110, 36, cover=False)
    tx(s, 196, yy + 10, 380, 16, a, 11, INK, True); tx(s, 196, yy + 27, 380, 14, b, 9, MUTED)
    arrow(s, 326, yy + 52, 326, yy + 70, LINE2, 1)
kids = [('f5_4.png', 'Distribution and trading', True), ('f5_5.png', 'Ship owner and operator', False), ('f5_6.png', 'Ship building and repair', False)]
hline(s, 56 + 90, 400, 360, LINE2)
for i, (lg, b, me) in enumerate(kids):
    x = 56 + i * 184
    rect(s, x, 410, 172, 96, GREEN_L if me else WASH, GREEN if me else None, radius=8, lw=1.25)
    if me:
        rect(s, x + 46, 402, 80, 16, GREEN_D, radius=8); tx(s, x + 46, 402, 80, 16, 'MY COMPANY', 7, 'FFFFFF', True, align='c', anchor='m', spacing=1)
    pic(s, IMG + lg, x + 36, 426, 100, 42, cover=False)
    tx(s, x + 6, 478, 160, 14, b, 8.5, GREEN_D if me else MUTED, me, align='c')
card(s, 56, 520, 540, 160, 'What Triatra does')
tx(s, 70, 544, 512, 40, 'Distributor of PATRIA and ULTRA products for mining, construction, agriculture, forestry and maritime. Sells units and full after-sales support.', 10.5, BODY, lh=1.2)
for i, (lg, a, b) in enumerate([('f5_7.png', 'Unit', 'Trader of UTPE units, local and export'), ('f5_8.png', 'Parts, components and services', 'Maintenance and remanufacturing')]):
    x = 70 + i * 256
    rect(s, x, 600, 244, 66, 'FFFFFF', LINE, radius=8)
    pic(s, IMG + lg, x + 10, 614, 80, 38, cover=False)
    tx(s, x + 98, 612, 140, 14, a, 9.5, INK, True); tx(s, x + 98, 630, 140, 28, b, 8.5, MUTED)
kicker(s, 624, 158, 'Industry coverage')
for i, (f, t, new_) in enumerate([('f5_9.png', 'Coal and mineral mining', False), ('f5_10.png', 'Construction', False),
                                  ('f5_11.png', 'Forestry and agro-industry', False), ('f5_12.png', 'Maritime', True)]):
    x = 624 + (i % 2) * 306; yy = 178 + (i // 2) * 254
    p = pic(s, IMG + f, x, yy, 294, 240); round_pic(p, .04)
    rect(s, x, yy + 196, 294, 44, '11181C')
    tx(s, x + 12, yy + 196, 270, 44, f'0{i + 1}   {t}', 11, 'FFFFFF', True, anchor='m')
    if new_:
        rect(s, x + 204, yy + 12, 78, 18, GREEN, radius=9); tx(s, x + 204, yy + 12, 78, 18, 'NEW · 2025', 7.5, 'FFFFFF', True, align='c', anchor='m')

# 05 site map
s = new('Site operation', 'Triatra serves customers from *16 points* across Indonesia',
        'Head Office in Jakarta, 6 Site Operations and 9 Site Representatives.')
mp = Image.open(IMG + 'f7_1.png').convert('RGBA'); a = mp.getchannel('A')
grey = Image.new('RGBA', mp.size, (193, 200, 205, 255)); grey.putalpha(a); grey.save('/tmp/claude-0/v4img/map_grey.png')
MX, MY, MW, MH = 150, 160, 980, 358
pic(s, '/tmp/claude-0/v4img/map_grey.png', MX, MY, MW, MH, cover=False)
PINS = [('H', 26.40, 73.14), ('O', 24.59, 69.01), ('R', 18.78, 57.11), ('R', 13.65, 31.90), ('R', 42.34, 54.55), ('R', 44.25, 56.98), ('O', 44.16, 47.64),
        ('R', 45.52, 45.58), ('R', 42.99, 40.54), ('O', 47.22, 42.23), ('R', 45.04, 36.28), ('R', 45.48, 31.65), ('R', 48.67, 22.19), ('O', 48.79, 31.94),
        ('R', 54.60, 88.43), ('O', 90.95, 62.81)]
iw, ih = mp.size; sc = min(MW / iw, MH / ih); ox, oy = MX + (MW - iw * sc) / 2, MY + (MH - ih * sc) / 2
CL = {'H': (GREEN_D, 'FFFFFF'), 'O': (GREEN, 'FFFFFF'), 'R': ('FFFFFF', INK)}
for i, (t, px, py) in enumerate(PINS):
    cx, cy = ox + iw * sc * px / 100, oy + ih * sc * py / 100; d = 18
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, E(cx - d / 2), E(cy - d / 2), E(d), E(d))
    o.fill.solid(); o.fill.fore_color.rgb = rgb(CL[t][0]); o.line.color.rgb = rgb(INK if t == 'R' else CL[t][0]); o.line.width = Pt(.75)
    o.shadow.inherit = False
    tf = o.text_frame; [setattr(tf, m, 0) for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom')]
    r = tf.paragraphs[0].add_run(); r.text = str(i + 1); r.font.size = Pt(7); r.font.bold = True; r.font.color.rgb = rgb(CL[t][1]); r.font.name = SANS
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
for i, (t, lbl) in enumerate([('H', 'Head Office'), ('O', 'Site Operation'), ('R', 'Site Representative')]):
    x = 900 + i * 110
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, E(x), E(140), E(10), E(10)); o.fill.solid(); o.fill.fore_color.rgb = rgb(CL[t][0]); o.line.color.rgb = rgb(INK if t == 'R' else CL[t][0]); o.line.width = Pt(.75)
    tx(s, x + 14, 138, 96, 14, lbl, 8, MUTED)
SITES = [('Head Office', 'Jl. Raya Bekasi KM 22, Cakung, Jakarta Timur'), ('Jakarta', 'Jl. Raya Bekasi KM 22, Cakung, Jakarta Timur'),
         ('Tanjung Enim', 'Jl. Lingga Raya 10, Muara Enim, Sumatera Selatan'), ('Pekanbaru', 'Jl. Soekarno Hatta KM 3,5 No. 151, Riau'),
         ('Banjarmasin', 'Jl. Ahmad Yani KM 13,5 Gambut, Kalimantan Selatan'), ('Sungai Danau', 'Ds. Karang Indah, Angsana, Tanah Bumbu, Kalsel'),
         ('Tanjung Tabalong', 'Jl. A. Yani KM 7,5 Maburai, Tabalong, Kalsel'), ('Batu Kajang', 'Jl. Negara KM 140, Batu Sopang, Paser, Kaltim'),
         ('Muara Teweh', 'Jl. Ahmad Yani No. 85, Barito Utara, Kalteng'), ('Balikpapan', 'Jl. Jend. Sudirman No. 844, Balikpapan, Kaltim'),
         ('Melak', 'Hauling Road Trubaindo, Kutai Barat, Kaltim'), ('Tabang', 'Workshop Buma Km 6, Hauling Road, Kaltim'),
         ('Tanjung Redeb', 'Jl. Gunung Panjang No. 101B, Berau, Kaltim'), ('Sangatta', 'Jl. HDRS Tango Delta KPC, Kutai Timur, Kaltim'),
         ('Sumbawa', 'Memco Area Tongo, Sekongkang, Sumbawa Barat, NTB'), ('Timika', 'Jl. Kuala Tembaga E-4, Kuala Kencana, Papua')]
TY = {0: 'H', 1: 'O', 6: 'O', 9: 'O', 13: 'O', 15: 'O'}
for half in range(2):
    rows = [['#', 'Site', 'Type', 'Address']]
    for i in range(half * 8, half * 8 + 8):
        rows.append([str(i + 1), SITES[i][0], {'H': 'Head office', 'O': 'Operation', 'R': 'Rep.'}[TY.get(i, 'R')], SITES[i][1]])
    st = {(r, 1): {'bold': True} for r in range(1, 9)}
    st.update({(r, 0): {'bold': True, 'color': GREEN_D} for r in range(1, 9)})
    table(s, 56 + half * 592, 528, 576, rows, [20, 100, 66, 300], rowh=17.5, size=8, hsize=7, styles=st)

# 06 org
s = new('Organization', 'I work in Marketing Strategic 2, under *Ignatius Indrawan S.*')
def node(x, y, w, name, role, hl=False, h=40, me=False):
    rect(s, x, y, w, h, GREEN_L if me else ('FFFFFF' if not hl else WASH), GREEN if me else LINE2, radius=6, lw=1.25 if me else .75)
    tx(s, x + 6, y + 6, w - 12, 14, name, 9.5, INK, True, align='c')
    tx(s, x + 6, y + 21, w - 12, 14, role, 7.5, GREEN_D if (me or hl) else MUTED, me or hl, align='c')
node(530, 150, 220, 'Ceisar Centiaga', 'DIRECTOR IN CHARGE', True)
arrow(s, 640, 190, 640, 202, LINE2, 1)
node(530, 202, 220, 'Ricardo Tanada', 'MKT UNIT & STRATEGIC DIV HEAD', True)
hline(s, 152, 262, 976, LINE2, 1); arrow(s, 640, 242, 640, 262, LINE2, 1)
COLS = [('Kresnanto A.W.', 'MKT STRATEGIC 1 HEAD', [('Satrio F.R.', 'Big Suppeq, Big Vessel, Bucket'), ('M. Fawwaz J.', 'Cabin, Forestry, Agro, Forklift, Towerlamp, Pump')]),
        ('Ricardo Tanada (c)', 'MKT STRATEGIC 2 HEAD', [('Ignatius Indrawan S.', 'DEPUTY HEAD'), ('Ervin Bahar P.', 'Medium Vessel, Man Hauler, Bus Scania'),
                                                       ('Tiberias K.S.  ◄ ME', 'Small Suppeq, Truck Others'), ('Eurico', 'Mining / Non-mining Trailer, Overseas Zone'),
                                                       ('Nandu Narpati', 'Admin')]),
        ('Ugik Praseno', 'MKT STRATEGIC 3 HEAD', [('Baihaqi', 'Mineral Processing, EPC'), ('Yuda Prana', 'Maritime, Renewable Energy'), ('Celine', 'Ultra Product Support'), ('Hanifa', 'Automation, EV')]),
        ('Marketing Communication', 'MARCOMM', [('Karina Audina E.', 'Marcomm'), ('Adinda Siti K.', 'Marcomm'), ('Rahma', 'Graphic Designer')])]
for i, (h, r, ppl) in enumerate(COLS):
    x = 56 + i * 296; w = 280
    arrow(s, x + w / 2, 262, x + w / 2, 278, LINE2, 1)
    if i == 1: rect(s, x - 8, 272, w + 16, 412, None, GREEN, radius=8, lw=1.25)
    node(x, 280, w, h, r, True)
    for j, (n_, d) in enumerate(ppl):
        node(x, 332 + j * 66, w, n_, d, hl=(d == 'DEPUTY HEAD'), h=54 if True else 40, me='ME' in n_)

# 07 roles flow: full detail from Draft_v2, translated to English
s = new('Roles & responsibility · Supply chain', 'I take every order from *inquiry to delivery* for two product lines',
        'Five steps from customer inquiry to factory acceptance test (FAT), for Small Suppeq and Truck Others.')
STEPS = [('Inquiry & opportunity', ['Business Consultant', 'Application Engineering', 'Marketing Unit'],
          ['Check spec and buying reason', 'Check project location', 'Check target price and lead time', 'Check urgency and PO date', 'Lead / opportunity in CRM']),
         ('Preliminary', ['Business Consultant', 'Application Engineering', 'Marketing Unit Triatra'],
          ['Repeat order or new drawing?', 'Request drawing in iServe; MKU Head assigns AE (same day)',
           'AE drawing: repeat 1 day, minor 3 days, major 5 days', 'Check unit function and critical parts', 'Handle customer revisions']),
         ('Pricing / Quotation', ['Marketing Unit Triatra', 'Marketing Unit UTPE'],
          ['Request quote to UTPE: drawing, target price, lead time, customer info', 'UTPE quote: price/COGS, lead time, validity',
           'Input standard price; check standard GP', 'Submit PCR for approval', 'Watch SLA; escalate if late']),
         ('Negotiation & CPO', ['Business Consultant', 'Marketing Unit Triatra', 'Marketing Unit UTPE'],
          ['Revise lead time and spec if asked', 'Check PO / PJB vs drawing', 'Validate order; fill SAP condition type',
           'DP request or confirm order → SO', 'Extend PN, master data, sharing profit', 'PO interco: MKU Manager → GM → Director']),
         ('Production & Delivery', ['Business Consultant', 'Marketing Unit Triatra', 'Marketing Unit UTPE', 'Warehouse'],
          ['Build follows QFD', 'Weekly progress to BC', 'Escalate major problems', 'FAT and QC at warehouse',
           'Delivery plan; BAST and SPB signed'])]
cw, gap = (1168 - 4 * 14) / 5, 14
for i, (t, pic_, L) in enumerate(STEPS):
    x = 56 + i * (cw + gap)
    ch_ = s.shapes.add_shape(MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON, E(x), E(158), E(cw + (gap + 6 if i < 4 else 0)), E(40))
    _nostyle(ch_); ch_.fill.solid(); ch_.fill.fore_color.rgb = rgb(GREEN_D if i % 2 == 0 else '0A7F3F'); ch_.line.fill.background()
    if i: ch_.adjustments[0] = 0.28
    else: ch_.adjustments[0] = 0.28
    tx(s, x + (22 if i else 12), 158, cw - 26, 40, [f'{i + 1:02d}  {t}'], 10.5, 'FFFFFF', True, anchor='m', emph=False)
    card(s, x, 206, cw, 74, 'PIC')
    tx(s, x + 14, 231, cw - 22, 48, pic_, 8, INK, True, lh=1.0)
    card(s, x, 288, cw, 206, 'Detail')
    tx(s, x + 14, 310, cw - 24, 182, L, 8.5, BODY, bullets=True, lh=1.05, emph=False)
for g, (lbl, items) in enumerate([('Small Suppeq', [('ft_fuel_truck.webp', 'Fuel truck'), ('wt_water_truck_clean.png', 'Water truck'), ('lt_lube_truck.webp', 'Lube truck')]),
                                  ('Truck Others', [('crane_truck_crop.png', 'Crane truck'), ('mixer_truck.webp', 'Mixer truck'), ('st_stemming_truck.webp', 'Stemming truck')])]):
    gx = 56 + g * 592; pw = (576 - 16) / 3
    kicker(s, gx, 504, f'Units I handle · {lbl}', GREEN_D); hline(s, gx, 520, 576)
    for j, (f, n_) in enumerate(items):
        src = PROD + f
        if f.endswith('.webp'):
            src = f'/tmp/claude-0/v4img/{f}.png'; Image.open(PROD + f).convert('RGB').save(src)
        x = gx + j * (pw + 8)
        pic(s, src, x, 528, pw, 150)
        rect(s, x, 654, pw, 24, INK); tx(s, x + 8, 654, pw - 16, 24, n_, 9.5, 'FFFFFF', True, anchor='m')

D = json.load(open(ROOT + 'stp4p/data.json'))
# 08 strategic: 4C -> STP -> 4P exactly as agreed in discussion
s = new('Strategic · 4C → STP → 4P', 'Partner *F.lli Ferrari* for quality buyers and *XCMG* for price buyers')
rows = [['Step', 'Item', 'Key point', 'Supporting data']]
G = [('4C', [('Change', 'HYVA has left; value sits in Medium + Heavy', 'Triatra has no crane brand since HYVA stopped. Medium + Heavy = 41% of units, 64% of value (2023 – 2026). Heavy units 12 → 17 → 35 (2023 – 2025).'),
             ('Competitor', 'Two leaders, one per class', 'Medium: Sany Palfinger, 38% of value. Heavy: Palfinger, 66% of value; PK 53002 alone sold 39 of 65 units (2023 – 2026).'),
             ('Customer', 'Medium buys on price, Heavy buys on quality', 'China brands take 73% of Medium value; European brands take 85% of Heavy value. 88% go on trucks ≥ 24 t GVW (mining, construction).'),
             ('Company', 'Partner two brands to serve both buyers', 'XCMG for price-oriented buyers. F.lli Ferrari for quality-oriented buyers.')]),
     ('STP', [('Segmentation', 'Two classes, ten 5-tm tiers', 'Medium 25 – 45 tm: 196 units, Rp 156 M. Heavy > 45 tm: 65 units, Rp 115 M.'),
              ('Targeting', 'Take share from the Top 1 model in each tier', 'Medium: Sany Palfinger SPK32080, SPK36080, SPK42502. Heavy: Palfinger PK 53002, PK 76002, PK 88002.'),
              ('Positioning', 'Two clear promises', 'XCMG: same capacity, lower price (SQZ365.4 −9% vs SPK36080). Ferrari: European features, cheaper where it wins (−23% at 25 – 30 tm, −32% at 45 – 50 tm) and faster delivery from China stock (~14 weeks).')]),
     ('4P', [('Product', 'Offer Ferrari models that beat the Top 1 on features', 'Red Power (more working range), SDV (less boom flex), Magic Touch (auto open/stow): Sany Palfinger has none. PB, RS, ECM: equal to Palfinger.'),
             ('Price', 'Negotiate a better price with Ferrari and XCMG', 'Ferrari: lower price on 746 A4 (+48%), 9601CR A8 (+85%), 990R (+79%). XCMG: Triatra special price on SQZ325.4 and SQZ365.4.'),
             ('Place', 'Negotiate stock to cut lead time', 'Ferrari stocks 268 A4 and FBR450R A4 in China (14-week lead time) and main components in Malaysia. XCMG via GM Tractors.'),
             ('Promotion', 'Sell a ready-to-work package', 'Crane + flatdeck + installation (+2-year warranty on Ferrari). Exhibitions and customer visits with a Marcom sales kit.')])]
merges = []; st = {}
for name, items in G:
    r0 = len(rows)
    for it, k, d in items: rows.append([name, it, k, d])
    r1 = len(rows) - 1; merges.append((r0, 0, r1, 0))
    st[(r0, 0)] = {'bold': True, 'color': GREEN_D, 'size': 12, 'anchor': 'm', 'align': 'c'}
    for r in range(r0, r1 + 1):
        st[(r, 1)] = {'bold': True, 'size': 10}; st[(r, 2)] = {'bold': True, 'size': 10}; st[(r, 3)] = {'size': 9.5}
        if rows[r][1] == 'Company':
            for c in (1, 2, 3): st[(r, c)]['fill'] = GREEN_L
table(s, 56, 158, 1168, rows, [80, 140, 330, 618], rowh=46, size=9.5, hsize=9.5, styles=st, merges=merges,
      grid=LINE, upper=False, hfill='F0F2F4', hcolor=INK, rowhs=[26] + [44.5] * 11)

# 09 charter: old layout with section divider bars
s = new('Project charter', 'Sell the first *Ferrari and XCMG* challenger cranes by March 2027')
def bar(x, y, w, t, sub=None, h=24):
    rect(s, x, y, w, h, GREEN_D)
    tx(s, x + 10, y, w - 20, h, t, 10.5, 'FFFFFF', True, anchor='m', caps=True, spacing=0.5, emph=False)
def body(x, y, w, h, text, size=9.5, bullets=False, num=False):
    rect(s, x, y, w, h, WASH)
    if num: text = [f'{i + 1}. {t}' for i, t in enumerate(text)]
    tx(s, x + 10, y + 5, w - 20, h - 8, text, size, INK, lh=1.08, bullets=bullets, emph=False)
L, LW, R0, RW = 56, 566, 638, 586
y = 150
bar(L, y, LW, 'Project name'); body(L, y + 24, LW, 26, 'Multi-brand Crane Challenger: F.lli Ferrari and XCMG', 10.5); y += 58
bar(L, y, LW, 'Background'); body(L, y + 24, LW, 86, 'HYVA stopped making cranes, so Triatra has no crane brand. From Jan 2023 to Aug 2026 Indonesia imported 638 knuckle boom cranes; Medium and Heavy (> 25 tm) are 41% of units but 64% of value, led by Sany Palfinger (Medium) and Palfinger (Heavy). This project puts a challenger brand against the Top 1 of each tm tier.'); y += 116
bar(L, y, LW, 'Objectives'); body(L, y + 24, LW, 60, ['Map Medium and Heavy cranes by tm tier, brand and model (4C)', 'Pick one challenger per tier: XCMG for price buyers, Ferrari for quality buyers (STP)', 'Set Product, Price, Place and Promotion per tier and sell the first unit (4P)'], num=True); y += 90
bar(L, y, LW, 'Project scope · Medium and Heavy class (> 25 tm)'); body(L, y + 24, LW, 38, ['1. Market size and brand leaders   2. Top 1 vs challenger per tier   3. Feature and price comparison', '4. Brand negotiation (Ferrari, XCMG)   5. Sales kit, exhibition and first sale'], 9); y += 74
bar(L, y, 410, 'KPI / metric'); bar(L + 416, y, LW - 416, 'Target')
body(L, y + 24, 410, 92, ['4C, STP, 4P approved (Aug 2026)', 'Ferrari and XCMG terms signed (Dec 2026)', 'Sales kit ready (Dec 2026)', 'Quotations sent (Feb 2027)', 'First unit sold (Mar 2027)'], 9.5, num=True)
body(L + 416, y + 24, LW - 416, 92, ['First Ferrari or XCMG challenger crane sold by March 2027'], 11); y += 122
bar(L, y, LW, 'Support required'); body(L, y + 24, LW, 26, 'Marcom (sales kit, exhibition) · F.lli Ferrari (stock, parts, price) · XCMG (special price) · UTPE', 9)
y = 150
bar(R0, y, RW, 'Project timeframe')
G = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
ACT = [('Market study (4C)', 0, 3), ('STP and challenger choice', 3, 5), ('Negotiate with Ferrari and XCMG', 4, 7), ('Sales kit with Marcom', 5, 7),
       ('Exhibition and customer visits', 7, 9), ('Quotation → PO → first unit sold', 8, 10)]
rows = [['Activity', '2026'] + [''] * 6 + ['2027', '', ''], [''] + G] + [[a] + [''] * 10 for a, _, _ in ACT]
st = {(r + 2, k + 1): {'fill': GREEN} for r, (_, a, b) in enumerate(ACT) for k in range(a, b)}
table(s, R0, y + 24, RW, rows, [190] + [39.6] * 10, rowh=20, head=2, size=8.5, hsize=8.5, styles=st, aligns={k: 'c' for k in range(1, 11)},
      merges=[(0, 0, 1, 0), (0, 1, 0, 7), (0, 8, 0, 10)], grid=LINE, upper=False, hfill=WASH, hcolor=INK)
y += 24 + 160 + 8
bar(R0, y, RW, 'Benefit of project'); body(R0, y + 24, RW, 40, 'Triatra gets a crane brand for every Medium and Heavy tier again: XCMG for price buyers, Ferrari for quality buyers, with a clear 4P to win units from the Top 1.'); y += 72
bar(R0, y, RW, 'Project team')
rows = [['Executive sponsor', ': Ricardo Tanada'], ['Advisor', ': Ricardo Tanada / Ignatius Indrawan'], ['Coordinator', ': Ignatius Indrawan'],
        ['Project lead', ': Tiberias Krisgaharu Simu'], ['Team members', ': Marketing Unit · Application Engineering · UTPE · Business Consultant']]
rect(s, R0, y + 24, RW, 92, WASH)
for i, (a, b_) in enumerate(rows):
    tx(s, R0 + 10, y + 28 + i * 17, 140, 16, a, 9.5, INK); tx(s, R0 + 150, y + 28 + i * 17, RW - 160, 16, b_, 9.5, INK, emph=False)
y += 122
bar(R0, y, RW, 'Project approval')
aw = (RW - 18) / 4
for i, (role, nm) in enumerate([('Lead', 'Tiberias Krisgaharu Simu'), ('Coordinator', 'Ignatius Indrawan'), ('Advisor', 'Ricardo Tanada'), ('Executive Sponsor', 'Ricardo Tanada')]):
    x = R0 + i * (aw + 6)
    tx(s, x + 4, y + 28, aw, 14, role, 9, INK, True); tx(s, x + 4, y + 42, aw, 12, 'Date:', 8.5, MUTED)
    rect(s, x, y + 58, aw, 50, 'FFFFFF', LINE2); rect(s, x, y + 108, aw, 22, WASH, LINE2)
    tx(s, x + 6, y + 108, aw - 8, 22, nm, 8.5, INK, anchor='m')

# 10 market size (native chart + table)
s = new('Study · Market size', 'Focus on Medium and Heavy: *64% of value* from 41% of units')
kicker(s, 56, 158, 'Units imported per year by class · 2023 – 2026*')
cd = CategoryChartData(); cd.categories = ['2023', '2024', '2025', '2026*']
SER = [('Light (≤ 8 tm)', [54, 49, 49, 55]), ('Small (8–25 tm)', [58, 51, 66, 43]), ('Medium (25–45 tm)', [71, 58, 54, 19]), ('Heavy (> 45 tm)', [12, 17, 35, 2])]
for n_, v in SER: cd.add_series(n_, v)
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, E(56), E(174), E(640), E(300), cd).chart
ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False; ch.legend.font.size = Pt(8); ch.legend.font.color.rgb = rgb(MUTED)
for sr, c in zip(ch.series, ['C1C8CD', '889096', GREEN, GREEN_D]):
    sr.format.fill.solid(); sr.format.fill.fore_color.rgb = rgb(c)
pl = ch.plots[0]; pl.gap_width = 60; pl.overlap = -10; pl.has_data_labels = True
pl.data_labels.font.size = Pt(7.5); pl.data_labels.font.color.rgb = rgb(BODY); pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
va = ch.value_axis; va.visible = False; va.has_major_gridlines = False
ca = ch.category_axis; ca.tick_labels.font.size = Pt(9); ca.tick_labels.font.color.rgb = rgb(BODY); ca.format.line.color.rgb = rgb(LINE2)
kicker(s, 56, 486, 'Total units and import value · 2023 – 14 Aug 2026')
rows = [['Class', 'Lifting moment', 'Units', 'Import value (IDR)', 'Share'], ['Light', '≤ 8 tm', '177', 'Rp 40.118.000.000', '12%'],
        ['Small', '8 – 25 tm', '200', 'Rp 77.241.000.000', '24%'], ['Medium', '25 – 45 tm', '196', 'Rp 118.328.000.000', '36%'],
        ['Heavy', '> 45 tm', '65', 'Rp 91.154.000.000', '28%'], ['Total', '', '638', 'Rp 326.841.000.000', '100%']]
st = {(r, c): {'bold': True, 'color': GREEN_D, 'fill': GREEN_L} for r in (3, 4) for c in range(5)}
st.update({(5, c): {'bold': True} for c in range(5)})
table(s, 56, 504, 640, rows, [90, 110, 70, 170, 70], rowh=29, size=9.5, styles=st, aligns={2: 'r', 3: 'r', 4: 'r'})
for i, (v, l, hl) in enumerate([('67', 'Medium + Heavy units / year · target', True), ('104', 'Light + Small units / year · not target', False)]):
    x = 728 + i * 252
    card(s, x, 160, 240, 104, None, GREEN_L if hl else WASH)
    tx(s, x + 16, 172, 200, 50, v, 34, GREEN_D if hl else INK, font=SERIF); tx(s, x + 16, 230, 210, 28, l, 8.5, MUTED, True)
card(s, 728, 280, 496, 300, 'Key points')
tx(s, 744, 308, 466, 260, ['Medium + Heavy: 41% of units, 64% of import value', 'Value per unit: Rp 803 jt vs Rp 311 jt for Light + Small',
                          '88% of Medium and Heavy cranes go on trucks GVW ≥ 24 t: mining, construction, heavy logistics',
                          '2026 is partial: only 12 Medium and 1 Heavy unit to 14 Aug'], 11, INK, bullets=True, lh=1.2)
tx(s, 728, 596, 496, 80, '*2026 annualised (Jan – 14 Aug × 1.61). Source: Indonesia import records HS 84269100 + 84264900; truck-mounted knuckle boom cranes; Zoomlion and Hyva excluded; USD 1 = Rp 17.803.',
   8, SUB, lh=1.1, emph=False)

# 11 brand leaders 2025: top 3 brands, tables first then qty charts
s = new('Study · Brand leaders 2025 only', 'Two leaders to beat: *Sany Palfinger* in Medium, *Palfinger* in Heavy')
rect(s, 56, 150, 1168, 50, GREEN_L, radius=8)
tx(s, 72, 150, 1136, 50, ['Why only the top 3 brands: in 2025 they hold 90% of Medium value (49 of 54 units, 91%) and 95% of Heavy value (33 of 35 units, 94%).'],
   12, GREEN_D, True, anchor='m', align='c', emph=False)
for i, (lbl, cats, vals, rows, top3) in enumerate([
        ('Medium · 25 – 45 tm', ['Amco Veba', 'Palfinger', 'XCMG', 'Sany Palfinger'], [5, 5, 14, 30],
         [['#', 'Brand', 'Units', 'Import value (IDR)', 'Share'], ['1', 'Sany Palfinger', '30', 'Rp 13.226.000.000', '47%'], ['2', 'XCMG', '14', 'Rp 7.197.000.000', '26%'],
          ['3', 'Palfinger', '5', 'Rp 4.869.000.000', '17%'], ['', 'Top 3 brands', '49 of 54', 'Rp 25.292.000.000', '90%'], ['', 'Total Medium 2025', '54', 'Rp 28.000.000.000', '100%']], None),
        ('Heavy · > 45 tm', ['XCMG', 'Amco Veba', 'Palfinger'], [4, 7, 22],
         [['#', 'Brand', 'Units', 'Import value (IDR)', 'Share'], ['1', 'Palfinger', '22', 'Rp 29.738.000.000', '62%'], ['2', 'Amco Veba', '7', 'Rp 11.065.000.000', '23%'],
          ['3', 'XCMG', '4', 'Rp 4.647.000.000', '10%'], ['', 'Top 3 brands', '33 of 35', 'Rp 45.450.000.000', '95%'], ['', 'Total Heavy 2025', '35', 'Rp 48.000.000.000', '100%']], None)]):
    x = 56 + i * 596
    kicker(s, x, 214, lbl, GREEN_D)
    st = {(1, c): {'bold': True, 'color': GREEN_D, 'fill': GREEN_L} for c in range(5)}
    st.update({(4, c): {'bold': True, 'color': GREEN_D} for c in range(5)})
    st.update({(5, c): {'bold': True, 'fill': 'F0F2F4'} for c in range(5)})
    table(s, x, 232, 572, rows, [24, 170, 70, 200, 60], rowh=26, size=10, styles=st, aligns={2: 'r', 3: 'r', 4: 'r'})
    kicker(s, x, 402, 'Units sold by brand · 2025')
    cd = CategoryChartData(); cd.categories = cats; cd.add_series('Units', vals)
    ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, E(x), E(418), E(572), E(196), cd).chart
    ch.has_legend = False; ch.has_title = False; pl = ch.plots[0]; pl.gap_width = 60; pl.has_data_labels = True
    pl.data_labels.font.size = Pt(9); pl.data_labels.font.bold = True; pl.data_labels.number_format = '0" units"'; pl.data_labels.number_format_is_linked = False
    for j in range(len(cats)):
        pt = ch.series[0].points[j]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(GREEN_D if j == len(cats) - 1 else 'C1C8CD')
    ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False
    ch.category_axis.tick_labels.font.size = Pt(9.5); ch.category_axis.tick_labels.font.color.rgb = rgb(INK); ch.category_axis.format.line.color.rgb = rgb(LINE2)
card(s, 56, 624, 1168, 58)
tx(s, 72, 632, 1136, 44, ['Leaders are far ahead: Sany Palfinger sold 2.1× XCMG in Medium (30 vs 14 units); Palfinger sold 3.1× Amco Veba in Heavy (22 vs 7 units).',
                          'Share = share of import value. Scope is 2025 only, so figures are smaller than the 2023 – 2026 totals.'], 10, INK, bullets=True, emph=False)

# 12–16 STP + 4P tables: header follows template_excle_penyajian_data_v2 exactly; split over slides where it does not fit
import math
rpf = lambda v: 'TBC' if not v else f"Rp {v:,.0f}".replace(',', '.')
pct = lambda v: f"{v * 100:.0f}%"
def gapfill(g): return None if g is None else (RED_L if g > .3 else AMB_L if g > 0 else GREEN_L)
def gapcol(g): return MUTED if g is None else (RED if g > .3 else AMB if g > 0 else GREEN_D)
TITLE = {'M': 'Medium Class Crane', 'H': 'Heavy Class Crane'}
CW = 5.5  # px per char at 8 pt Arial (estimate)
def est_lines(txt, w, cw=CW):
    return sum(max(1, math.ceil(len(l) * cw / max(w - 12, 20))) for l in str(txt).split('\n'))

def legend_notes(s, y, note):
    for i, (c, l) in enumerate([(GREEN_L, 'Green = challenger cheaper than Top 1'), (AMB_L, 'Yellow = up to +30%'), (RED_L, 'Red = over +30%: negotiate price with F.lli Ferrari')]):
        x = 56 + [0, 230, 400][i]; rect(s, x, y + 2, 11, 11, c, LINE2, radius=2); tx(s, x + 17, y, 300, 14, l, 8.5, BODY)
    tx(s, 56, y + 18, 1168, 30, note, 8, MUTED, emph=False, lh=1.05)

def stp_slide(key, kick, head, stp):
    s = new(kick, head)
    R = D[key]
    rows = [[TITLE[key]] + [''] * 10,
            ['TM Class', 'Market Size', '', 'Top 1 Competitor', '', '', '', '', 'Challenger', '', ''],
            ['', 'Qty', 'Market Share', 'Brand', 'Type', 'Qty', 'Share', 'Price/unit', 'Brand', 'Type', 'Price/Unit']]
    st = {(0, 0): {'color': 'FFFFFF', 'fill': INK, 'size': 10.5, 'align': 'c'}}
    for c in range(11):
        for r in (1, 2): st.setdefault((r, c), {'align': 'c'})
    for d in R:
        r = len(rows); g = d['gap']
        top = d['top'] + ('*' if 'absent' in d.get('note', '') else '')
        rows.append([d['tm'], str(d['qty']), pct(d['share']), top, d['tmodel'], str(d['tqty']), pct(d['tshare']), rpf(d['tprice']),
                     d['ch'] or 'No challenger', d['cm'] or '–', rpf(d['cp']) if d['ch'] else '–'])
        for c in range(11): st[(r, c)] = {'size': 10.5, 'align': 'c' if c in (0, 1, 2, 5, 6) else ('r' if c in (7, 10) else 'l')}
        st[(r, 0)]['bold'] = True; st[(r, 3)]['bold'] = True; st[(r, 8)]['bold'] = True
        for c in (8, 9, 10): st[(r, c)]['fill'] = gapfill(g)
        if not d['ch']: st[(r, 8)].update(color=MUTED)
    n = len(R); hh = [26, 24, 32]; body = (510 - 160 - sum(hh)) / n
    table(s, 56, 160, 1168, rows, [62, 48, 72, 118, 118, 48, 62, 128, 98, 120, 128], head=3, size=10.5, hsize=9,
          styles=st, merges=[(0, 0, 0, 10), (1, 0, 2, 0), (1, 1, 1, 2), (1, 3, 1, 7), (1, 8, 1, 10)],
          grid=LINE, upper=False, hfill='F0F2F4', hcolor=INK, rowhs=hh + [body] * n)
    cw = (1168 - 32) / 3
    for i, (k_, v) in enumerate(stp):
        x = 56 + i * (cw + 16)
        card(s, x, 528, cw, 116, k_, GREEN_L if k_ == 'Positioning' else WASH, lcolor=GREEN_D)
        tx(s, x + 14, 552, cw - 28, 88, v, 11.5, INK, lh=1.12, emph=False)
    tx(s, 56, 652, 1168, 34, 'Period Jan 2023 – 14 Aug 2026. Market share = tier value / class value; value = units × highest import unit price per model (estimate, incl. duty & tax). '
       'Top 1 share = Top 1 model value / tier value. * Top 1 brand has no model in this tier: next-largest brand shown. Fill: green = challenger cheaper, yellow = up to +30%, red = over +30%.',
       8, MUTED, emph=False, lh=1.05)

def mix_slide(key, kick, head, R, summary=None):
    s = new(kick, head)
    colw = [60, 74, 66, 98, 254, 232, 72, 78, 116, 118]
    rows = [[TITLE[key]] + [''] * 9,
            ['TM Class', 'Challenger', '', '', 'Product', '', 'Price', 'Place', '', 'Promotion'],
            ['', 'Brand', 'Type', 'Price/Unit', 'Special features', '', '', '', '', ''],
            ['', '', '', '', 'Equal features', 'Winning features', '', 'Competitor', 'Challenger', '']]
    st = {(0, 0): {'color': 'FFFFFF', 'fill': INK, 'size': 10.5, 'align': 'c'}}
    for c in range(10):
        for r in (1, 2, 3): st.setdefault((r, c), {'align': 'c'})
    est = []
    for d in R:
        r = len(rows); g = d['gap']
        if d['ch']:
            gs = 'TBC' if g is None else f"{g * 100:+.0f}%".replace('-', '−') + '\nvs Top 1'
            vals = [d['tm'], d['ch'], d['cm'], rpf(d['cp']), '\n'.join(d['eq']) or '–', '\n'.join(d['win']) or '–', gs, d['place_c'], d['place_ch'], d['promo']]
        else:
            vals = [d['tm'], 'No challenger', '–', '–', '–', '–', '–', d['place_c'], '–', '–']
        rows.append(vals)
        for c in range(10): st[(r, c)] = {'size': 8, 'anchor': 't' if c in (4, 5, 8, 9) else 'm', 'align': 'c' if c in (0, 6) else ('r' if c == 3 else 'l')}
        st[(r, 0)].update(bold=True, size=10); st[(r, 1)]['bold'] = True; st[(r, 5)].update(bold=True, color=GREEN_D)
        st[(r, 6)].update(bold=True, color=gapcol(g), size=10)
        for c in range(1, 7): st[(r, c)]['fill'] = gapfill(g)
        if not d['ch']: st[(r, 1)].update(color=MUTED)
        est.append(max(est_lines(v, colw[c] * 1168 / sum(colw), CW * (1.08 if c == 5 else 1)) for c, v in enumerate(vals)) * 12.8 + 10)
    hh = [24, 22, 22, 22]; top = 160
    if summary and top + sum(hh) + sum(est) > 520: summary = None
    bottom = 600 if summary is None else 520
    avail = bottom - top - sum(hh); k = max(1, avail / sum(est))
    table(s, 56, top, 1168, rows, colw, head=4, size=8, hsize=9, styles=st,
          merges=[(0, 0, 0, 9), (1, 0, 3, 0), (1, 1, 1, 3), (1, 4, 1, 5), (1, 6, 3, 6), (1, 7, 2, 8), (1, 9, 3, 9),
                  (2, 1, 3, 1), (2, 2, 3, 2), (2, 3, 3, 3), (2, 4, 2, 5)],
          grid=LINE, upper=False, hfill='F0F2F4', hcolor=INK, rowhs=hh + [e * k for e in est])
    if summary:
        cw = (1168 - 48) / 4
        for i, (k_, v) in enumerate(summary):
            x = 56 + i * (cw + 16); card(s, x, 532, cw, 104, k_, WASH, lcolor=GREEN_D)
            tx(s, x + 14, 554, cw - 28, 80, v, 9.5, INK, lh=1.1, emph=False)
    legend_notes(s, 648, 'Price = challenger price vs Top 1 model price. Equal features = both brands have the system (challenger name = Top 1 name). '
                 'Winning features = only the challenger has it. * XCMG feature names to be verified with the XCMG datasheet.')

H_ = D['H']
stp_slide('M', 'STP · Medium class 25–45 tm · 1 / 2', 'Medium: target *Sany Palfinger* with XCMG at 30–40 tm and Ferrari at 25–30 tm',
          [('Segmentation', 'Medium class split into 4 tm tiers. 30–40 tm holds 65% of Medium units (128 of 196) and 69% of value.'),
           ('Targeting', 'Top 1 model of each tier: Sany Palfinger at 30–45 tm. At 25–30 tm Sany Palfinger has no model, so Amco Veba V825 is the target.'),
           ('Positioning', 'XCMG: same capacity as Sany Palfinger at a lower price. Ferrari 268 A4: European features, 23% cheaper than Amco Veba V825.')])
mix_slide('M', '4P · Medium class 25–45 tm · 2 / 2', 'Medium: XCMG wins on price; *renegotiate Ferrari* before selling 40–45 tm', D['M'])
stp_slide('H', 'STP · Heavy class > 45 tm · 1 / 3', 'Heavy: Ferrari is the only challenger and is *cheaper only at 45–50 tm*',
          [('Segmentation', 'Heavy class split into 6 tm tiers. 50–55 tm holds 62% of Heavy units (40 of 65), almost all Palfinger PK 53002.'),
           ('Targeting', 'Top 1 model of each tier: Palfinger at 50–55, 70–75 and 80–85 tm. Amco Veba (45–50) and Sany Palfinger (60–65) where Palfinger has no model.'),
           ('Positioning', 'Ferrari: the same European features as Palfinger, delivered faster from stock in China (~14 weeks) against Europe-built leaders.')])
mix_slide('H', '4P · Heavy class 45–65 tm · 2 / 3', 'Heavy 45–65 tm: Ferrari *matches or beats* the leader on features', H_[:3])
mix_slide('H', '4P · Heavy class 70–90 tm · 3 / 3', 'Heavy 70–90 tm: same features as Palfinger, so win on *delivery time*', H_[3:],
          summary=[('Product', 'Ferrari only. Extra features at 45–50 tm (RS, SDV) and 60–65 tm (Red Power, SDV, Magic Touch); equal to Palfinger at 50–85 tm.'),
                   ('Price', 'Cheaper only at 45–50 tm (−32%). +79% to +85% at 50–55 and 70–75 tm: negotiate price with F.lli Ferrari.'),
                   ('Place', 'Ferrari stocks units in China (~14 weeks) and parts in Malaysia, against Palfinger built in Europe.'),
                   ('Promotion', 'Crane + flatdeck + installation + 2-year warranty. Exhibitions with Marcom sales kit.')])

# conclusion
s = new('Conclusion', 'Partner with *F.lli Ferrari and XCMG*; keep Fassi for Petrosea')
def brand_card(x, w, name, sub, rows, notes, hl=False):
    card(s, x, 156, w, 340, None, GREEN_L if hl else WASH)
    tx(s, x + 16, 168, w - 32, 32, name, 22, INK, font=SERIF)
    kicker(s, x + 16, 204, sub, GREEN_D)
    yy = 224
    if rows:
        st = {}
        for r in range(1, len(rows)):
            g = rows[r][3]
            st[(r, 2)] = {'bold': True, 'color': gapcol(g) if isinstance(g, float) else MUTED}
        body = [[a, b_, (f"{g * 100:+.0f}%".replace('-', '−') if isinstance(g, float) else g)] for a, b_, _, g in [(*r_[:2], None, r_[3]) for r_ in rows[1:]]]
        table(s, x + 16, yy, w - 32, [rows[0][:3]] + body, [60, 150, 70], rowh=19, size=9, hsize=7.5, styles=st, aligns={2: 'r'})
        yy += 19 * len(rows) + 10
    tx(s, x + 16, yy, w - 32, 490 - yy, notes, 10, INK, bullets=True, lh=1.1, emph=False)
DM = {d['tm']: d for d in D['M'] + D['H']}
xr = [['tm', 'Model', 'vs Top 1', None]] + [[d['tm'], f"{d['cm']} vs {d['tmodel']}", None, d['gap']] for d in D['M'] if d['ch'] == 'XCMG']
fr = [['tm', 'Model', 'vs Top 1', None]] + [[d['tm'], f"{d['cm']} vs {d['tmodel']}", None, d['gap'] if d['gap'] is not None else 'TBC'] for d in D['M'] + D['H'] if d['ch'] == 'Ferrari']
brand_card(56, 360, 'XCMG', 'Medium · price buyers', xr,
           ['30–40 tm is 65% of Medium units and 69% of value', 'Ask XCMG for a special price at both tiers', 'Partnership terms needed: GM Tractors is XCMG\'s official distributor in Indonesia',
            'Bundle crane + flatdeck + installation; exhibitions with Marcom sales kit'])
brand_card(432, 520, 'F.lli Ferrari', 'Heavy · quality buyers · plus 25–30 and 40–45 tm', fr,
           ['Negotiate price at the red tiers: 40–45, 50–55 and 70–75 tm', 'Stock units in China (~14 weeks) and parts in Malaysia',
            'Bundle + 2-year warranty; exhibitions with Marcom sales kit'], hl=True)
brand_card(968, 256, 'Fassi', 'Key account', None,
           ['Petrosea buys Fassi only', 'Keep Fassi supply for this account', 'Outside the Ferrari + XCMG challenger plan'])
bx = rect(s, 56, 510, 1168, 170, DARK, radius=10); grad(bx, DARK, DARK2)
kicker(s, 80, 530, 'Decisions needed', GREEN_T)
for i, t in enumerate(['Approve partnership talks with F.lli Ferrari and XCMG', 'Mandate Ferrari price and stock negotiation', 'Budget for exhibitions and Marcom sales kit']):
    x = 80 + i * 380
    tx(s, x, 560, 80, 40, f'0{i + 1}', 26, GREEN_T, font=SERIF)
    tx(s, x, 606, 340, 60, t, 14, 'FFFFFF', font=SERIF, lh=1.1)

# 15 thanks
divider('Thank you', 'Questions and *feedback* are welcome.', 'Tiberias Krisgaharu Simu  ·  Marketing Strategic 2 Associate  ·  PT Triatra Sinergia Pratama')

assert len(P.slides) == TOTAL, len(P.slides)
P.save(sys.argv[1]); print('saved', len(P.slides))
