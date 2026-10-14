"""Medium & Heavy STP + 4P table: fills template_excle_penyajian_data_v2 and renders HTML for JPG export."""
import json, copy, sys
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

pos = json.load(open('/tmp/claude-0/pos.json'))
def tier(k):
    v = pos[k]; tot = sum(u*p for *_, u, p in v); return sum(u for *_, u, _ in v), tot
MED = ['25-30', '30-35', '35-40', '40-45']; HEV = ['45-50', '50-55', '60-65', '70-75', '80-85', '85-90']
MTOT = sum(tier(k)[1] for k in MED); HTOT = sum(tier(k)[1] for k in HEV)

# feature sets (special features only; from brand material + earlier Palfinger/Amco/Ferrari comparison)
F = {
 'Palfinger': {'Linkage': 'Power Link Plus', 'Power boost': 'HPLS', 'Extension speed': 'High Speed Extension', 'Oscillation': 'AOS', 'Electronic control': 'PALTRONIC 150', 'Auto fold': 'P-Fold'},
 'Sany Palfinger': {'Power boost': 'HPLS (MH)', 'Extension speed': 'High speed ext. (ROU)', 'Electronic control': 'Paltronic 50'},
 'Amco Veba': {'Linkage': 'Articulated Powerlink', 'Power boost': 'AVPS', 'Electronic control': 'EBB', 'Auto fold': 'Magic Touch'},
 'Ferrari': {'Linkage': 'Red Power', 'Power boost': 'PB', 'Extension speed': 'RS', 'Oscillation': 'SDV', 'Electronic control': 'ECM', 'Auto fold': 'Magic Touch'},
 'XCMG': {'Electronic control': 'Load limiter*'},
}
def feats(top, ch):
    a, b = F.get(top, {}), F.get(ch, {}); eq, win, lose = [], [], []
    for f in ['Linkage', 'Power boost', 'Extension speed', 'Oscillation', 'Electronic control', 'Auto fold']:
        if f in a and f in b: eq.append(f"{f} ({b[f]} = {a[f]})")
        elif f in b: win.append(f"{f} ({b[f]})")
        elif f in a: lose.append(f"{f} ({a[f]}, Top 1 only)")
    if len(eq)==6: eq=['All 6 named features equal (linkage, power boost, extension speed, oscillation, electronic control, auto fold)']
    return eq, win, lose

PLACE = {
 'Sany Palfinger': 'China-made; Palfinger Asia Pacific rep. office Jakarta, dealer network',
 'Palfinger': 'Austria-made; dealer PT Sanggar Sarana Baja (ABM Group) for mining',
 'Amco Veba': 'Italy-made; importer/dealer under assessment',
 'XCMG': 'China-made; official distributor PT Gaya Makmur Tractors (18 branches)',
}
PROMO_C = {
 'Palfinger': 'PALFINGER APAC Owners Club events (Jakarta 2024)', 'Sany Palfinger': 'Under assessment',
 'Amco Veba': 'Under assessment', 'XCMG': 'Under assessment'}
PLACE_CH = {
 'Ferrari': 'Triatra + UTPE body & mounting; UT network: 5 site ops, 10 site reps; Italy-made',
 'XCMG': 'Triatra + UTPE mounting (partnership needed: GM Tractors holds XCMG); China-made'}
PROMO_CH = 'Bundle truck + crane + UTPE body + service package; trial-to-buy for key accounts'

def mk(k, top, tm, ch, cm, cp, cls, note=''):
    units, val = tier(k); rows = {n: (u, p) for _, n, _, u, p in pos[k]}
    tu, tp = rows[tm]; tshare = tu*tp/val
    gap = None if cp is None or tp is None else cp/tp - 1
    eq, win, lose = feats(top, ch) if ch else ([], [], [])
    return dict(tm=k.replace('-', ' – '), qty=units, share=val/(MTOT if cls == 'M' else HTOT), top=top, tmodel=tm,
                tqty=tu, tshare=tshare, tprice=tp, ch=ch, cm=cm, cp=cp, gap=gap, eq=eq, win=win+[f"− {x}" for x in lose],
                place_c=PLACE[top], place_ch=PLACE_CH.get(ch, '–'), promo=PROMO_CH if ch else '–', note=note)

MEDROWS = [
 mk('25-30', 'Amco Veba', 'V825', 'Ferrari', '268 A4', 500e6, 'M', 'Sany Palfinger absent; 2nd-largest brand shown'),
 mk('30-35', 'Sany Palfinger', 'SPK32080', 'XCMG', 'SQZ325.4', 550e6, 'M'),
 mk('35-40', 'Sany Palfinger', 'SPK36080', 'XCMG', 'SQZ365.4', 600e6, 'M'),
 mk('40-45', 'Sany Palfinger', 'SPK42502', 'Ferrari', '746 A4', 1420e6, 'M'),
]
HEVROWS = [
 mk('45-50', 'Amco Veba', 'V950', 'Ferrari', 'FBR450R A4', 1350e6, 'H', 'Palfinger absent; 2nd-largest brand shown'),
 mk('50-55', 'Palfinger', 'PK 53002', 'Ferrari', '9601CR A8', 3260e6, 'H'),
 mk('60-65', 'Sany Palfinger', 'SPK61502', 'Ferrari', '9661C', None, 'H', 'Palfinger absent; Ferrari price TBC'),
 mk('70-75', 'Palfinger', 'PK 76002 EH D', 'Ferrari', '990R', 4110e6, 'H'),
 mk('80-85', 'Palfinger', 'PK 88002 EH C', 'Ferrari', 'TBC (price list)', None, 'H', 'Ferrari model from price list'),
 mk('85-90', 'XCMG', 'GSQZ880.6', None, None, None, 'H', 'No challenger'),
]
json.dump({'M': MEDROWS, 'H': HEVROWS}, open('/home/user/6month/nedp_deck/stp4p/data.json', 'w'), indent=1)

# ---------------- Excel ----------------
wb = openpyxl.load_workbook(sys.argv[1]); ws = wb.active; ws.title = 'Medium & Heavy'
RED, YEL, GRN = PatternFill('solid', fgColor='FEEBEC'), PatternFill('solid', fgColor='FFF7C2'), PatternFill('solid', fgColor='E1F9EC')
def copy_header(src0, dst0):
    for r in range(4):
        for c in range(1, 18):
            s = ws.cell(src0+r, c); d = ws.cell(dst0+r, c)
            d.value = s.value; d._style = copy.copy(s._style)
        ws.row_dimensions[dst0+r].height = ws.row_dimensions[src0+r].height
    for m in list(ws.merged_cells.ranges):
        if m.min_row >= src0 and m.max_row <= src0+3:
            ws.merge_cells(start_row=m.min_row-src0+dst0, start_column=m.min_col, end_row=m.max_row-src0+dst0, end_column=m.max_col)
def fill(r0, rows):
    style = [copy.copy(ws.cell(5, c)._style) for c in range(1, 18)]
    for i, d in enumerate(rows):
        r = r0+i
        vals = [d['tm'], d['qty'], d['share'], d['top'], d['tmodel'], d['tqty'], d['tshare'], d['tprice'], d['ch'] or 'No challenger',
                d['cm'] or '–', d['cp'] if d['cp'] else 'TBC', '\n'.join(d['eq']) or '–', '\n'.join(d['win']) or '–',
                d['gap'] if d['gap'] is not None else 'TBC', d['place_c'], d['place_ch'], d['promo']]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v); cell._style = copy.copy(style[c-1])
            cell.alignment = Alignment(wrap_text=True, vertical='top')
        for c in (3, 7): ws.cell(r, c).number_format = '0%'
        for c in (8, 11): ws.cell(r, c).number_format = '#,##0'
        ws.cell(r, 14).number_format = '+0%;-0%;0%'
        g = d['gap']
        fillc = RED if g is not None and g > .3 else YEL if g is not None and g > 0 else GRN if g is not None else None
        if fillc:
            for c in range(9, 15): ws.cell(r, c).fill = fillc
        ws.row_dimensions[r].height = 120
for r in range(5, 12):
    for c in range(1, 18):
        if r > 8: ws.cell(r, c).value = None
fill(5, MEDROWS)
h0 = 5+len(MEDROWS)+2
copy_header(1, h0); ws.cell(h0, 1).value = 'Heavy Class Crane'
fill(h0+4, HEVROWS)
n = h0+4+len(HEVROWS)+1
for t in ['Notes:',
          'Period Jan 2023 – 14 Aug 2026. Market share = tier value / class value; value = units × highest import unit price per model (estimate, incl. duty & tax).',
          'Top 1 share = Top 1 model value / tier value. Price gap = challenger price vs Top 1 model price. Green = cheaper; yellow = up to +30%; red = > +30% (negotiate price with F.lli Ferrari).',
          'Special features compare named systems only; * XCMG feature names to be verified with the XCMG datasheet.',
          'Fassi is kept for Petrosea (key-account exception) and appears only in the conclusion.']:
    ws.cell(n, 1, t).font = Font(name='Arial', size=9, bold=t == 'Notes:'); n += 1
for c, w in zip(range(1, 18), [9, 7, 9, 15, 13, 7, 9, 15, 10, 14, 15, 38, 38, 10, 32, 32, 34]):
    ws.column_dimensions[get_column_letter(c)].width = w
wb.save('/home/user/6month/nedp_deck/stp4p/Crane_STP_4P_Medium_Heavy.xlsx')
print('ok', MTOT/1e9, HTOT/1e9)
