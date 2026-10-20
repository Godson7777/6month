"""Competitor map per class/tier + challenger pick (uses crane_data)."""
import collections, crane_data as d
def models():
    M = collections.defaultdict(lambda: dict(q=0, v=0, tms=[]))
    for r in d.R:
        k = (r[2], r[0], d.fam(r[0], r[1])); m = M[k]; m['q'] += r[8]; m['v'] += r[10]; m['tms'].append(r[12])
    out = []
    for (cls, b, t), m in M.items():
        tm = max(m['tms'])
        out.append(dict(cls=cls, brand=b, nice=d.NICE.get(b, b.title()), type=t, tm=tm, tier=d.tier(cls, tm), q=m['q'],
                        usd=m['v'], amt=m['v'] * d.FX, p=d.landed(b, m['v'] / m['q'])))
    return out
MOD = models(); FER = d.ferrari()
def tiers(cls):
    res = []
    for tr in sorted({x['tier'] for x in MOD if x['cls'] == cls}):
        T = sorted([x for x in MOD if x['cls'] == cls and x['tier'] == tr], key=lambda x: -x['usd']); top = T[0]
        fer = [dict(f, nice='F.lli Ferrari') for f in FER if d.cls_of(f['tm']) == cls and d.tier(cls, f['tm']) == tr]
        cands = [x for x in T[1:] if x['brand'] != top['brand']] + fer
        ok = [c for c in cands if c['p'] < top['p'] and c['tm'] >= top['tm'] - 2]
        ch = min(ok, key=lambda c: c['p']) if ok else None
        res.append(dict(tier=tr, units=sum(x['q'] for x in T), amt=sum(x['amt'] for x in T), models=T, top=top, fer=fer, ch=ch))
    return res
if __name__ == '__main__':
    import sys
    for cls in sys.argv[1:] or d.CLS:
        for t in tiers(cls):
            print(f"== {cls} {t['tier']} units {t['units']} amt Rp {t['amt']/1e9:.1f} Bn")
            for x in t['models']: print(f"   {x['nice']:15s} {x['type']:14s} {x['tm']:5.1f}tm {x['q']:3d}u amt {x['amt']/1e9:6.2f}Bn  p {x['p']/1e6:7.0f}Jt")
            for f in t['fer']: print(f"   FER {f['type']:12s} {f['tm']:5.1f}tm p {f['p']/1e6:7.0f}Jt  {f['src']} {f['lead']}")
            c = t['ch']; print('   >> CH', (c['nice'], c['type'], round(c['tm'],1), round(c['p']/1e6)) if c else None, 'vs TOP', t['top']['nice'], t['top']['type'], round(t['top']['p']/1e6))
