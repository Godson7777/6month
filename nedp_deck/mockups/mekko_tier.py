import openpyxl, collections, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
wb = openpyxl.load_workbook('../data/Crane_Market_GVW_Pairing_v11_Noir.xlsx', data_only=True, read_only=True)
R = list(wb['8. Pivot Source'].iter_rows(min_row=2, values_only=True))
tier = lambda tm: next(lo for lo in range(25, 100, 5) if lo < tm <= lo + 5)
T = collections.Counter(); M = collections.Counter(); MV = collections.Counter()
for r in R:
    if r[2] not in ('Medium', 'Heavy'): continue
    t = tier(r[13])
    if t > 45: continue  # Heavy >50 tm has 1-4 units per tier
    T[t] += r[8] or 0; M[(t, r[0], r[1])] += r[8] or 0
rows = []
for t in sorted(T):
    ms = sorted([(k, q) for k, q in M.items() if k[0] == t], key=lambda x: -x[1])
    (_, b, m), q = ms[0]; segs = [(m.replace(b + ' ', ''), q)]; cum = q
    for (t2, b2, m2), q2 in ms[1:]:
        if cum / T[t] >= .8: break
        if b2 == b: segs.append((m2.replace(b + ' ', ''), q2)); cum += q2
    rows.append((t, b.title().replace('Hiab', 'HIAB'), segs, T[t]))
TOT = sum(r[3] for r in rows)
fig, ax = plt.subplots(figsize=(15, 7.5), dpi=110); ax.set_xlim(0, 1); ax.set_ylim(-.12, 1.16); ax.axis('off')
fig.text(.02, .95, 'Top-1 model and its brand family per tm tier, 2023 – Aug 2026', fontsize=17, weight='bold')
fig.text(.02, .91, 'Column width = tier size (units). Dark = top-1 model, mid = other models of the same brand, grey = rest of tier. Dashed = 80% target.', fontsize=11, color='#555')
x = 0; DK, MD, LT = '#0B4D2A', '#6FCF97', '#D9D9D9'
for t, b, segs, n in rows:
    w = n / TOT; y = 0
    for i, (m, q) in enumerate(segs):
        h = q / n; ax.add_patch(Rectangle((x, y), w, h, color=DK if i == 0 else MD, ec='white', lw=1.5))
        ax.text(x + w / 2, y + h / 2, f'{m}\n{q}u', ha='center', va='center', fontsize=9, weight='bold', color='white' if i == 0 else 'k')
        y += h
    ax.add_patch(Rectangle((x, y), w, 1 - y, color=LT, ec='white', lw=1.5))
    ax.text(x + w / 2, y + (1 - y) / 2, f'Rest\n{n - round(y * n)}u', ha='center', va='center', fontsize=9, color='#555')
    # brace on the right side of the brand family
    ax.plot([x + w - .006] * 2, [0.005, y - .005], color='#1E9E57', lw=2)
    ax.text(x + w / 2, y + .015, f'{b} {y:.0%}', ha='center', va='bottom', fontsize=10, weight='bold', color='#1E9E57')
    ax.text(x + w / 2, 1.02, f'{t}–{t + 5} tm\n{n} units', ha='center', va='bottom', fontsize=11, weight='bold')
    ax.text(x + w / 2, -.05, 'Medium' if t < 45 else 'Heavy', ha='center', fontsize=9, color='#555')
    x += w
ax.axhline(.8, color='#C0392B', ls='--', lw=1.4); ax.text(1.002, .8, '80%', color='#C0392B', va='center', fontsize=11, weight='bold')
fig.text(.02, .02, 'Source: Crane Market GVW Pairing v11 (Noir), 8. Pivot Source. Variants (B/C/E) counted as separate types as in database. Heavy > 50 tm (13 units) not shown.', fontsize=9, color='#666')
fig.savefig('mekko_tier_top1.png', bbox_inches='tight')
