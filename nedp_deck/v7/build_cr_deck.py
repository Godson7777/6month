"""Crane market deck (all classes): S1 market 2023-2026, S2 market 2025, S3+ competitor maps per class."""
import sys, collections
sys.path.insert(0, '.')
import crane_data as d, crane_map as cm
from cr_common import *
from PIL import Image
deck = Deck()

# ======================= S1: market 2023 - 2026 =======================
def s_market_all():
    U, V = d.by_year(); YRS = [2023, 2024, 2025, 2026]
    TU = sum(U.values()); TV = sum(V.values())
    cu = {c: sum(U[(y, c)] for y in YRS) for c in d.CLS}; cv = {c: sum(V[(y, c)] for y in YRS) for c in d.CLS}
    avg_u = lambda cs: sum(U[(y, c)] for y in YRS[:3] for c in cs) / 3
    avg_v = lambda cs: sum(V[(y, c)] for y in YRS[:3] for c in cs) / 3 / 1e9
    LS, MH = ('Light', 'Small'), ('Medium', 'Heavy')
    ls_u = sum(cu[c] for c in LS) / TU; mh_v = sum(cv[c] for c in MH) / TV
    C = deck.slide('Indonesian Import Folding Crane 23–26/', 'How big is the market?', 'And how much sells each year?',
                   'Every class buys every year: Light & Small bring the volume, Medium & Heavy bring the value',
                   [('From 2023 to 2026, Indonesia imported ', False), (f'{TU} folding cranes (Rp {num(TV / 1e9)} Bio)', True), (', about ', False),
                    (f'{avg_u(d.CLS):.0f} units (Rp {num(avg_v(d.CLS))} Bio) a year', True), ('. Light & Small make up ', False), (f'{ls_u:.0%} of units', True),
                    (', while Medium & Heavy hold ', False), (f'{mh_v:.0%} of value', True), ('.', False)], title_w=880)
    # left: units per year
    C.tx(36, 252, 580, 18, [[('Imported folding cranes by class per year, 2023 – 2026', True, '000000', 12.5)]], al=PP_ALIGN.CENTER)
    h23, h25 = U[(2023, 'Heavy')], U[(2025, 'Heavy')]; l23, l25 = U[(2023, 'Light')], U[(2025, 'Light')]
    t25 = sum(U[(2025, c)] for c in d.CLS)
    C.tx(210, 274, 410, 40, [[('Heavy almost ', False, '000000', 11.5), (f'tripled from {h23} to {h25} units in 2025', True, G, 11.5),
                              (f' ({h25 / t25:.0%} of that year), while ', False, '000000', 11.5), (f'Light fell from {l23} to {l25}', True, G, 11.5), ('.', False, '000000', 11.5)]])
    CX, CY, CW, CH = 36, 312, 470, 322; PX, PY, PW, PH = .01, .03, .98, .88; VMAX = 205
    ch = C.chart(XL_CHART_TYPE.COLUMN_STACKED, CX, CY, CW, CH, ['2023', '2024', '2025', '2026*'], [(LEG[c], [U[(y, c)] for y in YRS]) for c in d.CLS], gap=75)
    ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = VMAX; C.manual(ch, PX, PY, PW, PH)
    for k, c in enumerate(d.CLS):
        se = ch.plots[0].series[k]; se.format.fill.solid(); se.format.fill.fore_color.rgb = rgb(COL[c])
        dl = se.data_labels; dl.show_value = True; dl.number_format = '0'; dl.number_format_is_linked = False
        dl.position = XL_LABEL_POSITION.CENTER; dl.font.size = Pt(12); dl.font.bold = True; dl.font.name = FONT
        dl.font.color.rgb = rgb('FFFFFF' if c in DARK else '000000')
        for j, y in enumerate(YRS):
            if U[(y, c)] < 4: C.hide_label(se, j)
    x0, y0, pw, ph = CX + CW * PX, CY + CH * PY, CW * PW, CH * PH; catW = pw / 4
    for j, y in enumerate(YRS):
        t = sum(U[(y, c)] for c in d.CLS); cx = x0 + catW * (j + .5)
        C.tx(cx - 40, y0 + ph * (1 - t / VMAX) - 17, 80, 15, [[(f'{t} units', True, '404040', 10)]], al=PP_ALIGN.CENTER)
    AX = 514
    for k, (lab, cs) in enumerate([('Light & Small', LS), ('Medium & Heavy', MH)]):
        yy = 330 + k * 80
        C.tx(AX, yy, 104, 30, [[('Avg sales / year', True, '000000', 9.5)], [(lab, True, '000000', 9.5)]], al=PP_ALIGN.CENTER)
        C.line(AX, yy + 32, AX + 104, yy + 32, '404040', .75)
        C.tx(AX, yy + 36, 104, 30, [[(f'{avg_u(cs):.0f} units', True, G, 11)], [(f'Rp {num(avg_v(cs))} Bio', True, G, 11)]], al=PP_ALIGN.CENTER)
    C.tx(AX, 490, 104, 30, [[('Average of the full years 2023 – 2025', False, '595959', 8)]], al=PP_ALIGN.CENTER)
    C.legend(40, 640, 145)
    C.box(36, 662, 580, 20, None, '000000', lw=.75)
    C.tx(44, 665, 566, 16, [[('Ton-meter classes follow the Application Engineering classification. *2026 is a partial year.', False, '000000', 9)]])
    C.divider(630, 250, 686)
    C.tx(650, 252, 592, 18, [[('Imported folding cranes by class, 2023 – 2026', True, '000000', 12.5)]], al=PP_ALIGN.CENTER)
    C.mix_panel(736, 276, 420, 358, cu, cv, 648, 1160)
    C.legend(660, 640, 145)
    C.box(736, 662, 420, 20, 'FFFFFF', 'BFBFBF', lw=.75)
    C.tx(736, 665, 420, 16, [[('Light & Small bring the volume, Medium & Heavy bring the value', True, G, 10)]], al=PP_ALIGN.CENTER)
    C.tx(36, 692, 1206, 22, [[(SOURCE_NOTE, False, '7F7F7F', 6.5)]])

# ======================= S2: market 2025 =======================
BRCOL = {'SANY PALFINGER': '0B4D2A', 'PALFINGER': '1E9E57', 'XCMG': '74CC95', 'AMCO VEBA': 'B7E4C7', 'HIAB': 'A6A6A6', 'FASSI': 'D0D0D0', 'BOB-LIFT': 'EDEDED'}
def s_market_2025():
    R = [r for r in d.R if r[4] == 2025]
    cu = collections.Counter(); cv = collections.Counter(); bv = collections.Counter(); bu = collections.Counter()
    for r in R: cu[r[2]] += r[8]; cv[r[2]] += r[10] * d.FX; bv[(r[2], r[0])] += r[10] * d.FX; bu[(r[2], r[0])] += r[8]
    cu = {c: cu[c] for c in d.CLS}; cv = {c: cv[c] for c in d.CLS}; TU = sum(cu.values()); TV = sum(cv.values())
    ls_u = (cu['Light'] + cu['Small']) / TU; mh_v = (cv['Medium'] + cv['Heavy']) / TV
    lead = {c: max([(b, v) for (cc, b), v in bv.items() if cc == c], key=lambda x: x[1]) for c in d.CLS}
    top3 = {c: sum(sorted([v for (cc, b), v in bv.items() if cc == c], reverse=True)[:3]) / cv[c] for c in d.CLS}
    C = deck.slide('Indonesian Import Folding Crane 2025/', 'How big was 2025?', 'And who led each class?',
                   f'2025: Sany Palfinger led Light, Small and Medium; Palfinger led Heavy with {lead["Heavy"][1] / cv["Heavy"]:.0%} of its value',
                   [('In 2025, Indonesia imported ', False), (f'{TU} folding cranes (Rp {num(TV / 1e9)} Bio)', True), ('. Light & Small made up ', False),
                    (f'{ls_u:.0%} of units', True), (', while Medium & Heavy held ', False), (f'{mh_v:.0%} of value', True),
                    ('. In every class, ', False), (f'the top three brands held {min(top3.values()):.0%} or more of the value', True), ('.', False)], title_w=880)
    C.tx(36, 252, 580, 18, [[('Imported folding cranes by class, 2025', True, '000000', 12.5)]], al=PP_ALIGN.CENTER)
    C.mix_panel(122, 276, 420, 358, cu, cv, 34, 546)
    C.legend(40, 640, 145)
    C.box(36, 662, 580, 20, None, '000000', lw=.75)
    C.tx(44, 665, 566, 16, [[('Ton-meter classes follow the Application Engineering classification.', False, '000000', 9)]])
    C.divider(630, 250, 686)
    # right: brand share of value per class
    C.tx(650, 252, 592, 18, [[('Who led each class in 2025,', True, '000000', 12.5), (' % of class value', False, '000000', 12.5)]], al=PP_ALIGN.CENTER)
    brands = [b for b in BRCOL if any(bv[(c, b)] for c in d.CLS)]
    cats = list(reversed(d.CLS))
    BX, BY, BW, BH = 740, 278, 400, 350; QX, QY, QW, QH = .0, .02, 1.0, .96
    ch = C.chart(XL_CHART_TYPE.BAR_STACKED_100, BX, BY, BW, BH, cats, [(d.NICE[b], [bv[(c, b)] / cv[c] for c in cats]) for b in brands], gap=45, serlines=False)
    ch.category_axis.visible = False; C.manual(ch, QX, QY, QW, QH)
    for k, b in enumerate(brands):
        se = ch.plots[0].series[k]; se.format.fill.solid(); se.format.fill.fore_color.rgb = rgb(BRCOL[b])
        fc = 'FFFFFF' if b in ('SANY PALFINGER', 'PALFINGER') else '000000'
        for j, c in enumerate(cats):
            sh = bv[(c, b)] / cv[c]
            if sh >= .3: C.point_fmt(se, j, f'"{d.NICE[b]} "0%', fc, 10)
            elif sh >= .05: C.point_fmt(se, j, '0%', fc, 9.5)
            else: C.hide_label(se, j)
    rowh = BH * QH / 4
    for j, c in enumerate(d.CLS):          # bar charts draw the first category at the bottom: Light (last) is the top row
        yc = BY + BH * QY + rowh * (j + .5)
        C.tx(650, yc - 16, 86, 32, [[(c, True, G if c in DARK else '000000', 11)], [(f'{cu[c]} units', False, '000000', 9)]], al=PP_ALIGN.RIGHT)
        C.tx(1146, yc - 16, 96, 32, [[(f'Rp {num(cv[c] / 1e9)} Bio', True, '000000', 10)], [(f'top 3: {top3[c]:.0%}', False, '595959', 8.5)]])
    lx = 652
    for b in brands:
        w = max(64, 22 + 7.2 * len(d.NICE[b])); C.legend(lx, 640, w, [(BRCOL[b], d.NICE[b])]); lx += w + 2
    C.box(736, 662, 420, 20, 'FFFFFF', 'BFBFBF', lw=.75)
    C.tx(736, 665, 420, 16, [[('Every class has one clear leader to beat', True, G, 10)]], al=PP_ALIGN.CENTER)
    C.tx(36, 692, 1206, 22, [[(SOURCE_NOTE.replace('2023 – 2026; 2026 is a partial year', '2025'), False, '7F7F7F', 6.5)]])

# ======================= S3+: competitor map per class =======================
LOGO = {'AMCO VEBA': 'amco_veba', 'FASSI': 'fassi', 'HIAB': 'hiab', 'PALFINGER': 'palfinger', 'SANY PALFINGER': 'sany_palfinger', 'XCMG': 'xcmg', 'FERRARI': 'ferrari'}
RANGE = {'Light': '≤ 8 tm', 'Small': '> 8 – 25 tm', 'Medium': '> 25 – 45 tm', 'Heavy': '> 45 tm'}
jt = lambda x: f"Rp {num(x / 1e6, 0)} Jt"
def s_map(CLS):
    T = cm.tiers(CLS); cu = collections.Counter()
    for t in T:
        for x in t['models']: cu[x['brand']] += x['q']
    BR = [b for b, _ in cu.most_common() if b != 'FERRARI']
    TU = sum(t['units'] for t in T); TA = sum(t['amt'] for t in T); main = max(T, key=lambda t: t['units'])
    mt, mc = main['top'], main['ch']
    head = (f"{CLS}: {mt['nice']} {mt['type']} leads; " + (f"{mc['nice']} {mc['type']} is {jt(mt['p'] - mc['p'])} cheaper per unit" if mc else 'no cheaper crane of the same size yet'))
    C = deck.slide(f'{CLS} Class Map 2023–26/', 'Who leads each tm class?', 'Which crane beats it on price?', head,
                   [(f'{CLS} class ({RANGE[CLS]}): ', False), (f'{TU} units worth Rp {num(TA / 1e9)} Bio', True), (' in 2023 – 2026. ', False),
                    (f'{main["tier"][0]}–{main["tier"][1]} tm takes {main["units"] / TU:.0%} of units', True),
                    ('. Each row compares the tier leader (by value) with the cheapest crane of about the same size.', False)])
    s = C.s
    cols = ['tm class', 'Our challenger', 'F.lli Ferrari'] + BR
    W0, W1, W2 = 92, 170, 150; WB = (1206 - W0 - W1 - W2) / len(BR); widths = [W0, W1, W2] + [WB] * len(BR)
    X0, Y0 = 36, 246
    tb = s.shapes.add_table(1 + len(T), len(cols), E(X0), E(Y0), E(sum(widths)), E(300)).table
    for j, w in enumerate(widths): tb.columns[j].width = E(w)
    tb.rows[0].height = E(48); RH = max(80, (648 - Y0 - 48) / len(T))
    for i in range(1, 1 + len(T)): tb.rows[i].height = E(RH)
    FS = 11 if len(T) <= 2 else 10 if len(T) <= 4 else 9
    def fill(c, color): c.fill.solid(); c.fill.fore_color.rgb = rgb(color)
    def write(c, paras, al=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
        tf = c.text_frame; c.vertical_anchor = anchor; c.margin_left = c.margin_right = E(6); c.margin_top = E(5); c.margin_bottom = E(3)
        for k, para in enumerate(paras):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph(); p.alignment = al
            for t, bold, color, sz in para:
                r = p.add_run(); r.text = t; r.font.size = Pt(sz); r.font.bold = bold; r.font.name = FONT; r.font.color.rgb = rgb(color)
    for j, name in enumerate(cols):
        c = tb.cell(0, j); fill(c, G if j == 1 else DG)
        if j == 0: write(c, [[('tm class', True, 'FFFFFF', 10.5)]], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        elif j == 1: write(c, [[('Our challenger', True, 'FFFFFF', 11)], [('cheapest of the same size', False, LG, 8.5)]], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
        else: write(c, [[('', False, 'FFFFFF', 8)], [('', False, 'FFFFFF', 8)], [('price list + imports' if j == 2 else f'{cu[name]} units', False, LG, 8.5)]], PP_ALIGN.CENTER, MSO_ANCHOR.BOTTOM)
    def model_lines(x, top=False):
        return ([[('TOP 1', True, G, FS - 1)]] if top else []) + [
            [(f"{x['type']}", True, '000000', FS + .5)],
            [(f"• {x['q']} unit{'s' if x['q'] > 1 else ''}", False, '000000', FS - .5)],
            [(f"• Rp {num(x['amt'] / 1e9, 1 if x['amt'] >= 1e9 else 2)} Bio total", False, '000000', FS - .5)],
            [(f"• {jt(x['p'])} /unit", False, '000000', FS - .5)], [('', False, '000000', 4)]]
    for i, t in enumerate(T, start=1):
        lo, hi = t['tier']; lab = f'≤ {hi} tm' if lo == 0 else f'> {lo} – {hi} tm'
        c = tb.cell(i, 0); fill(c, 'F2F2F2'); write(c, [[(lab, True, G, FS + 2)], [(f"{t['units']} units", False, '000000', FS)], [(f"Rp {num(t['amt'] / 1e9)} Bio", False, '000000', FS)]], PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
        ch = t['ch']; c = tb.cell(i, 1); fill(c, LG if ch else 'F2F2F2')
        if ch:
            srcl = 'F.lli Ferrari price list' if ch.get('src') else f"import data, {ch['q']} unit{'s' if ch['q'] > 1 else ''}"
            write(c, [[(f"{ch['nice']} {ch['type']}", True, DG, FS + 1)], [(f"• {jt(ch['p'])} /unit", False, '000000', FS)], [('', False, '000000', 4)],
                      [(f"{jt(t['top']['p'] - ch['p'])} cheaper", True, G, FS + 2)],
                      [(f"• vs {t['top']['nice']} {t['top']['type']}, {jt(t['top']['p'])} /unit", False, '595959', FS - 1.5)], [('', False, '000000', 4)],
                      [(srcl, False, '7F7F7F', FS - 2.5)]], PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
        else:
            write(c, [[('No cheaper crane of the same size', False, '595959', FS - 1)]], PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)
        c = tb.cell(i, 2); fill(c, 'FFFFFF'); paras = []
        for x in [m for m in t['models'] if m['brand'] == 'FERRARI']: paras += model_lines(x, x is t['top'])
        base = {}
        for f in t['fer']:
            k = f['type'].split()[0]
            if k not in base or f['p'] < base[k]['p']: base[k] = f
        for f in sorted(base.values(), key=lambda f: f['tm']):
            paras += [[(f"{f['type']}", True, '000000', FS + .5)], [(f"• {jt(f['p'])} /unit", False, '000000', FS - .5)], [('', False, '000000', 4)]]
        write(c, paras or [[('–', False, '7F7F7F', FS - 1)]])
        for j, b in enumerate(BR, start=3):
            c = tb.cell(i, j); ms = [m for m in t['models'] if m['brand'] == b]
            fill(c, 'FFF7D6' if any(m is t['top'] for m in ms) else 'FFFFFF'); paras = []
            for m in ms: paras += model_lines(m, m is t['top'])
            write(c, paras or [[('', False, '000000', 8)]])
    for j, name in enumerate(cols):
        if j < 2: continue
        key = 'FERRARI' if j == 2 else name; x = X0 + sum(widths[:j]); w = widths[j]
        plate = C.box(x + 8, Y0 + 5, w - 16, 24, 'FFFFFF', None, MSO_SHAPE.ROUNDED_RECTANGLE)
        if key in LOGO:
            f = f'assets/logos/brands/{LOGO[key]}.png'; iw, ih = Image.open(f).size; k = min((w - 28) / iw, 18 / ih)
            s.shapes.add_picture(f, E(x + w / 2 - iw * k / 2), E(Y0 + 17 - ih * k / 2), E(iw * k), E(ih * k))
        else:
            tf = plate.text_frame; tf.margin_top = tf.margin_bottom = 0; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
            r = p.add_run(); r.text = d.NICE.get(key, key.title()); r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = rgb(DG); r.font.name = FONT
    C.legend(36, 658, 470, [(LG, 'Our challenger: cheaper than the tier leader, at most 2 tm smaller'), ('FFF7D6', 'Tier leader (TOP 1 = highest import value in the tier)')])
    C.tx(36, 680, 1206, 34, [[('Source: Indonesia import records (Crane Market GVW Pairing v11, Noir), 2023 – 2026 (2026 partial year); F.lli Ferrari price list June 2026 (Rev1), sheet 25.06. '
        'Competitor price = average import unit price of the model (total value ÷ total units) × Rp 17.803/USD (JISDOR 23 Sep 2026) × (1 + import duty: 0% China/ACFTA, 5% others) × (1 + PPN 11% + PPh 22 2.5%); crane only, before distributor margin. '
        'F.lli Ferrari price = (column K − column I) × (1 − 13.6% TSP GP): crane only, no cargo deck, no install, no warranty; taxes included. '
        'Units and amount = import value before tax. Model variants merged (e.g. SPK8500 = SPK8500, A, B). tm class per Application Engineering (rounded max lifting moment). '
        'Folding cranes only; Hyva, Zoomlion, grabbers, telescopic cranes and invalid-price records excluded. Bob-Lift not used as challenger.', False, '7F7F7F', 6.5)]])

s_market_all(); s_market_2025(); s_map('Light')
deck.save('v7/CR_Deck.pptx'); print('saved')
