"""Bright orange deck: 3-5 most popular crane models per tm class, with photos (imports 2023-2026)."""
import sys, os
sys.path.insert(0, '.')
import crane_data as d, crane_map as cm
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
E = lambda v: Emu(round(v * 9525)); rgb = RGBColor.from_string; F = 'Arial'
OR, OR2, ORL, ORXL, DK, GR = 'F26522', 'FF8A3D', 'FFE3D1', 'FFF5EE', '2B2B2B', '6B6B6B'
num = lambda x, n=1: f'{x:,.{n}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
jt = lambda x: f"Rp {num(x / 1e6, 0)} Jt"
W_, H_ = 1280, 720
P = Presentation(); P.slide_width, P.slide_height = E(W_), E(H_)
BL = P.slide_layouts[6]
WEB, OLD, LOGO = 'assets/cranes_web/', 'assets/cranes/', 'assets/logos/brands/'
PHOTO = {'SPK8500': WEB + 'SPK8500.jpg', 'SPK6500': WEB + 'SPK6500_t.jpg', 'SPK15500': WEB + 'SPK15500.jpg', 'SPK18500': WEB + 'SPK18500.jpg',
         'SPK23500': WEB + 'SPK23500.jpg', 'SPK32080': WEB + 'SPK32080_t.jpg', 'SPK42502': WEB + 'SPK42502_t.jpg', 'V806': WEB + 'V806.jpg', 'X-CLX 288': WEB + 'XCLX288.jpg',
         'V825': OLD + 'Amco_Veba_V825.jpg', 'X-CLX 388': OLD + 'Hiab_X_CLX_388.jpg', 'PK 32080': OLD + 'Palfinger_PK_32080_C.jpg', 'V933': OLD + 'Amco_Veba_V933.jpg',
         'GSQZ330.4': OLD + 'XCMG_GSQZ330_4.jpg', 'SPK36080': OLD + 'Sany_Palfinger_SPK36080.jpg', 'PK 41002': OLD + 'Palfinger_PK_41002.jpg',
         'KSQZ400.4': OLD + 'XCMG_KSQZ400_4.jpg', 'GSQZ400.4': OLD + 'XCMG_GSQZ400_4.jpg', 'V946': OLD + 'Amco_Veba_V946B.jpg', 'V950': OLD + 'Amco_Veba_V950.jpg',
         'GSQZ460.4': OLD + 'XCMG_GSQZ460_4.jpg', 'F485RA.2.23': OLD + 'Fassi_F485RA_2_23.jpg', 'EFFER 525': OLD + 'Hiab_EFFER_525H.jpg', 'PK 53002': OLD + 'Palfinger_PK_53002.jpg',
         'X-HIPRO B58': OLD + 'Hiab_X_HIPRO_B58.jpg', 'SPK61502': OLD + 'Sany_Palfinger_SPK61502.jpg', 'PK 76002': OLD + 'Palfinger_PK_76002_EH_D.jpg',
         'PK 88002': OLD + 'Palfinger_PK_88002_EH_C.jpg', 'GSQZ880.6': OLD + 'XCMG_GSQZ880_6.jpg', 'GSQZ860.6': OLD + 'XCMG_GSQZ860_6.jpg',
         'KSQZ300.3': OLD + 'XCMG_KSQZ300_3.jpg', 'SQ12ZK3': OLD + 'XCMG_SQ12ZK3Q.jpg', 'KSQZ300.4': OLD + 'XCMG_KSQZ300_4.jpg', 'SPK38080': None}
LG = {'AMCO VEBA': 'amco_veba', 'FASSI': 'fassi', 'HIAB': 'hiab', 'PALFINGER': 'palfinger', 'SANY PALFINGER': 'sany_palfinger', 'XCMG': 'xcmg', 'FERRARI': 'ferrari'}

def tx(s, x, y, w, h, paras, al=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    b = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
    for k, para in enumerate(paras):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph(); p.alignment = al
        for t, b_, c, sz in para:
            r = p.add_run(); r.text = t; r.font.bold = b_; r.font.size = Pt(sz); r.font.name = F; r.font.color.rgb = rgb(c)
    return b
def box(s, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, line=None):
    b = s.shapes.add_shape(shape, E(x), E(y), E(w), E(h)); b.shadow.inherit = False
    if fill: b.fill.solid(); b.fill.fore_color.rgb = rgb(fill)
    else: b.fill.background()
    if line: b.line.color.rgb = rgb(line); b.line.width = Pt(.75)
    else: b.line.fill.background()
    return b
def pic(s, f, x, y, w, h, cover=False):
    iw, ih = Image.open(f).size
    if cover:   # crop to fill
        k = max(w / iw, h / ih); p = s.shapes.add_picture(f, E(x), E(y), E(w), E(h))
        cw, chh = w / k / iw, h / k / ih; p.crop_left = p.crop_right = (1 - cw) / 2; p.crop_top = p.crop_bottom = (1 - chh) / 2
    else:
        k = min(w / iw, h / ih); s.shapes.add_picture(f, E(x + (w - iw * k) / 2), E(y + (h - ih * k) / 2), E(iw * k), E(ih * k))
def frame(title, sub, page):
    s = P.slides.add_slide(BL)
    box(s, 0, 0, W_, H_, 'FFFFFF')
    box(s, 0, 0, W_, 92, OR); box(s, 0, 92, W_, 6, OR2)
    tx(s, 40, 16, 1000, 40, [[(title, True, 'FFFFFF', 26)]])
    tx(s, 40, 56, 1100, 26, [[(sub, False, 'FFF1E6', 13)]])
    tx(s, 1180, 30, 60, 30, [[(str(page), True, 'FFFFFF', 14)]], PP_ALIGN.RIGHT)
    box(s, 0, H_ - 26, W_, 26, ORXL)
    tx(s, 40, H_ - 20, 1200, 16, [[('Source: Indonesia import records (Crane Market GVW Pairing v11), 2023 – 2026 (2026 partial year). Folding cranes only. Units = units imported; '
                                   'price = average import price per unit × Rp 17.803/USD, before duty and tax. Photos: manufacturer websites and brochures.', False, GR, 7.5)]])
    return s
def card(s, x, y, w, h, m, rank, tier_units):
    box(s, x, y, w, h, 'FFFFFF', MSO_SHAPE.ROUNDED_RECTANGLE, 'F3C7A8').adjustments[0] = .05
    ph = h * .58; f = PHOTO.get(m['type'])
    if f and os.path.exists(f): pic(s, f, x + 6, y + 6, w - 12, ph - 6, cover=True)
    else:
        box(s, x + 6, y + 6, w - 12, ph - 6, ORXL)
        lg = LG.get(m['brand'])
        if lg:
            lf = LOGO + lg + '.png'; iw, ih = Image.open(lf).size; k = min((w - 50) / iw, 30 / ih)
            s.shapes.add_picture(lf, E(x + w / 2 - iw * k / 2), E(y + ph / 2 - ih * k / 2 - 6), E(iw * k), E(ih * k))
        else: tx(s, x, y + ph / 2 - 16, w, 20, [[(m['nice'], True, OR, 13)]], PP_ALIGN.CENTER)
        tx(s, x, y + ph / 2 + 16, w, 14, [[('photo to follow', False, GR, 8)]], PP_ALIGN.CENTER)
    b = box(s, x + 10, y + 12, 30, 30, OR if rank == 1 else OR2, MSO_SHAPE.OVAL); tf = b.text_frame
    for mm in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, mm, 0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = f'#{rank}'; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = rgb('FFFFFF'); r.font.name = F
    ty = y + ph + 6
    tx(s, x + 10, ty, w - 20, 16, [[(m['nice'], False, GR, 9)]])
    tx(s, x + 10, ty + 14, w - 20, 22, [[(m['type'], True, DK, 14)]])
    tx(s, x + 10, ty + 36, w - 20, 16, [[(f"{m['q']} units", True, OR, 12), (f"  ·  {m['q'] / tier_units:.0%} of class", False, GR, 9)]])
    tx(s, x + 10, ty + 54, w - 20, 16, [[(f"{jt(m['p'])} /unit", False, DK, 10)]])
def ferr(t):
    base = []
    for f in sorted(t['fer'], key=lambda f: f['tm']):
        k = f['type'].split()[0]
        if k not in base: base.append(k)
    return ', '.join(base)
def tier_row(s, y, h, cls, t, label=None, models=None):
    lo, hi = t['tier'] if t else (0, 0)
    ms = models or sorted(t['models'], key=lambda x: -x['q'])[:5 if t['units'] >= 20 else 3]
    units = sum(x['q'] for x in ms) if models else t['units']
    box(s, 40, y, 150, h, ORL, MSO_SHAPE.ROUNDED_RECTANGLE).adjustments[0] = .06
    tx(s, 52, y + 14, 130, 20, [[(cls.upper(), True, OR, 11)]])
    tx(s, 52, y + 32, 130, 34, [[(label or (f'≤ {hi} tm' if lo == 0 else f'{lo}–{hi} tm'), True, DK, 22)]])
    tx(s, 52, y + 70, 130, 20, [[(f"{t['units'] if t else units} units", True, DK, 13)]])
    tx(s, 52, y + 88, 130, 16, [[('imported 2023 – 26', False, GR, 8.5)]])
    if t and ferr(t): tx(s, 52, y + h - 46, 132, 40, [[('F.lli Ferrari size:', True, OR, 8.5)], [(ferr(t), False, DK, 8.5)]])
    cw = (1240 - 200 - 4 * 10) / 5
    for i, m in enumerate(ms): card(s, 200 + i * (cw + 10), y, cw, h, m, i + 1, t['units'] if t else units)

T = {c: cm.tiers(c) for c in d.CLS}; tiers = {(c, t['tier']): t for c in d.CLS for t in T[c]}
U, V = d.by_year(); TU = sum(U.values()); TV = sum(V.values()) / 1e9
# ---------- cover ----------
s = P.slides.add_slide(BL); box(s, 0, 0, W_, H_, OR)
box(s, 760, 0, 520, H_, OR2)
pic(s, WEB + 'SPK23500.jpg', 760, 0, 520, H_, cover=True)
box(s, 0, 0, 760, H_, OR)
tx(s, 60, 190, 680, 40, [[('MARKET BRIEF FOR F.LLI FERRARI', True, 'FFE3D1', 14)]])
tx(s, 60, 236, 680, 170, [[('The most popular', True, 'FFFFFF', 40)], [('folding cranes in', True, 'FFFFFF', 40)], [('Indonesia', True, 'FFFFFF', 40)]])
tx(s, 60, 420, 680, 30, [[('Top 3 – 5 models in every tm class, 2023 – 2026', False, 'FFFFFF', 18)]])
box(s, 60, 466, 120, 4, 'FFFFFF')
tx(s, 60, 486, 680, 60, [[(f'{TU} cranes imported  ·  Rp {num(TV)} Bio  ·  ~188 units a year', True, 'FFFFFF', 15)], [('PT Triatra Sinergia Pratama · Marketing Strategic', False, 'FFE3D1', 12)]])
# ---------- overview ----------
s = frame('Every class has a clear #1 model', 'Most popular model in each tm class, by units imported 2023 – 2026', 2)
rows = [(c, t) for c in d.CLS for t in T[c] if t['units'] >= 3]
cw, chh = (1200 - 3 * 12) / 4, 0
cols = {c: [t for cc, t in rows if cc == c] for c in d.CLS}
for j, c in enumerate(d.CLS):
    x = 40 + j * (cw + 12)
    box(s, x, 116, cw, 40, OR if j % 2 == 0 else OR2, MSO_SHAPE.ROUNDED_RECTANGLE).adjustments[0] = .2
    cu = sum(t['units'] for t in T[c])
    tx(s, x, 124, cw, 26, [[(f'{c}  ·  {cu} units', True, 'FFFFFF', 15)]], PP_ALIGN.CENTER)
    for i, t in enumerate(cols[c]):
        m = max(t['models'], key=lambda x: x['q']); yy = 168 + i * 124; lo, hi = t['tier']
        box(s, x, yy, cw, 114, ORXL, MSO_SHAPE.ROUNDED_RECTANGLE, 'F3C7A8').adjustments[0] = .08
        f = PHOTO.get(m['type'])
        if f and os.path.exists(f): pic(s, f, x + 8, yy + 8, 110, 98, cover=True)
        else:
            box(s, x + 8, yy + 8, 110, 98, ORL); lg = LG.get(m['brand'])
            if lg:
                lf = LOGO + lg + '.png'; iw, ih = Image.open(lf).size; k = min(96 / iw, 26 / ih)
                s.shapes.add_picture(lf, E(x + 63 - iw * k / 2), E(yy + 57 - ih * k / 2), E(iw * k), E(ih * k))
        tx(s, x + 128, yy + 10, cw - 136, 16, [[(f'≤ {hi} tm' if lo == 0 else f'{lo}–{hi} tm', True, OR, 11), (f'  {t["units"]} units', False, GR, 9)]])
        tx(s, x + 128, yy + 30, cw - 136, 16, [[(m['nice'], False, GR, 9)]])
        tx(s, x + 128, yy + 44, cw - 136, 24, [[(m['type'], True, DK, 16)]])
        tx(s, x + 128, yy + 70, cw - 136, 16, [[(f"{m['q']} units · {m['q'] / t['units']:.0%}", True, OR, 10)]])
        tx(s, x + 128, yy + 87, cw - 136, 16, [[(f"{jt(m['p'])} /unit", False, DK, 9)]])
# ---------- detail slides ----------
pg = 3
spec = [('Light', [(0, 5), (5, 8)], 'Light (≤ 8 tm): Sany Palfinger SPK8500 is the volume model'),
        ('Small', [(8, 10), (10, 15)], 'Small (8 – 15 tm): SPK15500 leads 10–15 tm'),
        ('Small', [(15, 20), (20, 25)], 'Small (15 – 25 tm): SPK23500 is 70 of 87 units at 20–25 tm'),
        ('Medium', [(25, 30), (30, 35)], 'Medium (25 – 35 tm): Amco Veba V825 and Sany Palfinger SPK32080 lead'),
        ('Medium', [(35, 40), (40, 45)], 'Medium (35 – 45 tm): Sany Palfinger SPK36080 and SPK42502 lead'),
        ('Heavy', [(45, 50), (50, 55)], 'Heavy (45 – 55 tm): Amco Veba V950 and Palfinger PK 53002 lead')]
for cls, trs, title in spec:
    s = frame(title, f'Top models by units imported, 2023 – 2026 · {cls} class', pg); pg += 1
    for k, tr in enumerate(trs): tier_row(s, 116 + k * 290, 278, cls, tiers[(cls, tr)])
# heavy > 55
big = [t for t in T['Heavy'] if t['tier'][0] >= 55]
ms = sorted([m for t in big for m in t['models']], key=lambda x: -x['q'])[:5]
s = frame('Heavy (> 55 tm): small volumes, Palfinger and XCMG', 'All models above 55 tm, 2023 – 2026 · Heavy class', pg); pg += 1
fake = dict(units=sum(t['units'] for t in big), fer=[f for t in big for f in t['fer']], tier=(55, 90), models=ms)
tier_row(s, 116, 278, 'Heavy', fake, label='> 55 tm', models=ms)
box(s, 200, 420, 1040, 120, ORXL, MSO_SHAPE.ROUNDED_RECTANGLE, 'F3C7A8').adjustments[0] = .08
tx(s, 230, 440, 980, 90, [[('Only ', False, DK, 15), (f"{fake['units']} units", True, OR, 15), (' above 55 tm in four years: ', False, DK, 15),
                           ('one or two units per model.', True, DK, 15)], [('These are project sales, quoted one by one.', False, GR, 13)]])
P.save('v7/Popular_Cranes_by_tm_Class.pptx'); print('saved', pg - 1, 'slides')
