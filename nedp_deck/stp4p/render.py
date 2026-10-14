import json,html
D=json.load(open('data.json'))
def rp(v): return 'TBC' if not v else f"Rp {v/1e6:,.0f} jt".replace(',','.')
def pc(v): return f"{v*100:.0f}%"
def gap(g):
    if g is None: return '<span class="mu">TBC</span>'
    c='g' if g<=0 else 'y' if g<=.3 else 'r'
    return f'<b class="{c}">{g*100:+.0f}%</b>'.replace('-','−')
def ul(xs): return '<br>'.join(html.escape(x) for x in xs) or '–'
def rows(R):
    o=''
    for d in R:
        d['pc']={'Palfinger':'Owners Club events','Sany Palfinger':'Under assessment','Amco Veba':'Under assessment','XCMG':'Under assessment'}[d['top']]
        g=d['gap']; cls='' if g is None else ('red' if g>.3 else 'amb' if g>0 else '')
        o+=f'''<tr class="{cls}"><td class="b">{d['tm']}</td><td class="n">{d['qty']}</td><td class="n">{pc(d['share'])}</td>
<td><b>{d['top']}</b><br><span class="mu">{d['tmodel']}</span></td><td class="n">{d['tqty']}</td><td class="n">{pc(d['tshare'])}</td><td class="n">{rp(d['tprice'])}</td>
<td><b>{d['ch'] or '<span class="tag">NO CHALLENGER</span>'}</b><br><span class="mu">{d['cm'] or ''}</span></td><td class="n">{rp(d['cp']) if d['ch'] else '–'}</td>
<td class="sm">{ul(d['eq'])}</td><td class="sm">{ul(d['win'])}</td><td class="n">{gap(g) if d['ch'] else '–'}</td>
<td class="sm">{d['place_c']}<br><span class='mu'>Promo: {d.get('pc','')}</span></td><td class="sm">{d['place_ch']}</td><td class="sm">{d['promo']}</td></tr>'''
    return o
def slide(k,title,head,stp):
    return f'''<div class="s"><div class="k">{title} · Jan 2023 – 14 Aug 2026</div><h1>{head}</h1>
<table><tr><th class="g" colspan="3">Segmentation</th><th class="g" colspan="4">Top 1 competitor · Targeting</th><th class="g" colspan="2">Challenger · Positioning</th>
<th class="g p" colspan="2">Product</th><th class="g p">Price</th><th class="g p" colspan="2">Place</th><th class="g p">Promotion</th></tr>
<tr><th>tm</th><th>Qty</th><th>Value share</th><th>Brand · model</th><th>Qty</th><th>Share</th><th>Price/unit</th><th>Brand · model</th><th>Price/unit</th>
<th>Equal features</th><th>Winning features</th><th>vs Top 1</th><th>Competitor</th><th>Challenger</th><th>Challenger plan</th></tr>{rows(D[k])}</table>
<div class="stp">{''.join(f'<div class="c"><b>{a}</b><p>{b}</p></div>' for a,b in stp)}</div>
<div class="f">Value = units × highest import unit price per model (estimate, incl. duty &amp; tax). Share = tier value / class value; Top 1 share = model value / tier value. Green = cheaper than Top 1, yellow ≤ +30%, red &gt; +30% (negotiate with F.lli Ferrari). − = feature only the Top 1 has. *XCMG feature names to verify. Place sources: Palfinger, Kontan/Industry.co.id (SSB 2024), GM Tractors.</div></div>'''
css=open('style.css').read()
H=f'''<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
{slide('M','Medium class · 25–45 tm','XCMG and Ferrari answer Sany Palfinger in <i>three of four</i> tiers; 40–45 tm needs a Ferrari price cut',
 [('S','4 tm tiers; 30–40 tm holds <strong>69%</strong> of Medium value.'),('T','Win 25–30 (Ferrari −23%), 35–40 (XCMG −9%); 30–35 at near-par (XCMG +4%).'),('P · 4P','<em>"Same capacity, lower price, UT service on site"</em> — bundle truck + crane + body + service.')])}
{slide('H','Heavy class · &gt;45 tm','Ferrari wins 45–50 tm; the <i>63% prize</i> at 50–55 tm needs a Ferrari price cut',
 [('S','6 tm tiers; 50–55 tm alone is <strong>63%</strong> of Heavy value, 95% of it PK 53002.'),('T','Win 45–50 (Ferrari −32%) now; 50–55 and 70–75 after price negotiation.'),('P · 4P','<em>"European features equal to Palfinger, at a fairer price"</em> — same 6 named systems.')])}
</body></html>'''
open('stp4p_slides.html','w').write(H)
