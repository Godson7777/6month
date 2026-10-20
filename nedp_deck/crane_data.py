"""Single source for the all-class crane market deck (Noir v11, JISDOR Rp 17.803/USD)."""
import openpyxl, collections, re
DB = 'data/Crane_Market_GVW_Pairing_v11_Noir.xlsx'; PL = 'data/Price_List_Crane_Ferrari_Jun26_Rev1.xlsx'
FX = 17803
CLS = ['Light', 'Small', 'Medium', 'Heavy']
CN = {'SANY PALFINGER', 'XCMG', 'BOB-LIFT', 'ZOOMLION'}           # 0% duty (ACFTA); others 5%
def excluded(r):
    m = str(r[1])
    if r[0] in ('HYVA', 'ZOOMLION'): return 'brand out'
    if '19000XG' in m or '6000XG' in m: return 'grabber'
    if m.startswith('TADANO TM-Z'): return 'telescopic'
    if 'PK 36050' in m or 'PK 48002' in m: return 'invalid price'
    return None
RAW = [r for r in openpyxl.load_workbook(DB, data_only=True, read_only=True)['8. Pivot Source'].iter_rows(min_row=2, values_only=True) if r[0]]
R = [r for r in RAW if not excluded(r)]
# r: 0 brand, 1 model, 2 class, 4 year, 8 qty, 9 unit USD, 10 value USD, 11 importer, 12 tm, 13 tm rounded
def fam(b, m):
    out = []
    for t in m[len(b):].strip().split():
        if re.search(r'\d', t): out.append(re.sub(r'(\d)[A-Z]+$', r'\1', t)); break
        out.append(t)
    return ' '.join(out)
landed = lambda b, usd: usd * FX          # as-is import (Eximpedia) price, no duty / tax assumption
HI = {'Light': 8, 'Small': 25, 'Medium': 45, 'Heavy': 999}
def cls_of(tm):
    t = int(tm + .5); return 'Light' if t <= 8 else 'Small' if t <= 25 else 'Medium' if t <= 45 else 'Heavy'
def tier(cls, tm):
    tm = min(tm, HI[cls])
    if cls == 'Light': return (0, 5) if tm <= 5 else (5, 8)
    if cls == 'Small': return (8, 10) if tm <= 10 else next((lo, lo + 5) for lo in (10, 15, 20) if tm <= lo + 5)
    lo = int((tm - 1e-9) // 5 * 5); return (lo, lo + 5)
NICE = {'SANY PALFINGER': 'Sany Palfinger', 'PALFINGER': 'Palfinger', 'HIAB': 'HIAB', 'AMCO VEBA': 'Amco Veba', 'XCMG': 'XCMG',
        'BOB-LIFT': 'Bob-Lift', 'FASSI': 'Fassi', 'PM CRANES': 'PM Cranes', 'FERRARI': 'F.lli Ferrari', 'TADANO': 'Tadano'}
# year x class
def by_year():
    U = collections.defaultdict(int); V = collections.defaultdict(float)
    for r in R: U[(r[4], r[2])] += r[8]; V[(r[4], r[2])] += r[10] * FX
    return U, V
# F.lli Ferrari price list as-is, crane only: K - I, sheet 25.06; tm per flliferrari.it or model-name class
FTM = {'315 A2': 1.5, '350 A2': 3.45, '543 A2': 4.3, '563 A2': 6, '563R A2': 6, '563 A3': 6, '563 A4': 6, '563R A4': 6,
       '6108 A2': 9.6, '6108 A3': 9.6, '6148 A3': 13.9, '5148 A4': 13.9, '178 A3': 15.8, '178 A4': 15.8, '6238 A3': 19.3, '6238 A4': 19.3,
       '6248 A3': 23, '6248 A4': 23, '258 A3': 25, '258R A3': 25, '258 A4': 25, '268 A3': 25.4, '268 A4': 25.4,
       '934 A4': 33, '934R A4': 33, 'FBR350 A4': 32.8, 'FBR350R A4': 32.8, 'FBR450 A4': 45.5, 'FBR450R A4': 45.5, 'FBR450R A6': 45.5,
       '746 A4': 44, '749R A4': 49, 'FBR600R A4': 58, 'FBR660R A4': 58.8, 'FBR660R A6': 58.8}
def ferrari():
    ws = openpyxl.load_workbook(PL, data_only=True)['25.06']; out = {}
    for r in ws.iter_rows(min_row=3, values_only=True):
        if r[3] in FTM and r[10]:
            p = (r[10] - r[8]) * (1 - .136)       # price list, crane only (K - I), less 13.6% TSP GP
            if r[3] not in out or p < out[r[3]]['p']:
                out[r[3]] = dict(brand='F.lli Ferrari', type=r[3], tm=FTM[r[3]], p=p, lead=r[6], src=r[4])
    # Heavy models not in the June 2026 price list (sources as in the earlier F.lli Ferrari deck)
    for t, tm, p, src in [('9601CR A8', 50.7, 3260e6, 'UTPE quote 15 Sep 2026, crane only'),
                          ('9661C', 63.2, 160000 * 20830, 'EUR 160.000 ex-works x Rp 20.830/EUR'),
                          ('990R', 74, 4110e6 / .97, 'TSP price less Rp 168 Jt cargo deck & install, less 13.6% TSP GP')]:
        out[t] = dict(brand='F.lli Ferrari', type=t, tm=tm, p=p, lead=None, src=src, extra=True)
    return list(out.values())
