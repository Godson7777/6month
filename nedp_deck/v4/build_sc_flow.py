"""One slide: supply chain flow Pre-Sales -> Sales -> After-Sales (from Flow Transaksi UNIT Tobe)."""
src = open('/home/user/6month/nedp_deck/v4/build_native.py').read()
exec(src[:src.index('# =====')])
TOTAL = 1
s = new('Supply chain · Unit transaction flow', 'Supply chain runs the order from *drawing to delivery*')
ST = [('PRE-SALES', 'Inquiry → quotation sent', 'Steps 1 – 63'), ('SALES', 'Negotiation → production done', 'Steps 64 – 133'),
      ('AFTER-SALES', 'Delivery → payment', 'Steps 134 – 154')]
w = 368; gap = 32
for i, (t, sub, rng) in enumerate(ST):
    x = 56 + i * (w + gap)
    ch_ = s.shapes.add_shape(MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON, E(x), E(156), E(w + (gap if i < 2 else 0)), E(58))
    _nostyle(ch_); ch_.fill.solid(); ch_.fill.fore_color.rgb = rgb([GREEN_D, '0A7F3F', '0DA54F'][i]); ch_.line.fill.background(); ch_.adjustments[0] = 0.25
    tx(s, x + (30 if i else 16), 160, w - 50, 24, t, 14, 'FFFFFF', True, emph=False)
    tx(s, x + (30 if i else 16), 186, w - 50, 20, f'{sub}  ·  {rng}', 9.5, 'E1F9EC', emph=False)
COLS = [
 ('Pre-sales activities', [
   'Request preliminary drawing in iServe; MKU Head assigns to AE (same day)',
   'AE drafts drawing; with DE PATRIA if detail needed (repeat 1 day · minor 3 days · major 5 days)',
   'Handle drawing revisions from customer',
   'Request quotation to PATRIA: price/COGS, lead time, validity',
   'Input standard price; submit PCR in DiKantor for approval'],
  'Example: customer asks for a 30 KL water truck → AE sends drawing in 3 days → PATRIA quotes price and 12-week lead time → PCR approved.'),
 ('Sales activities', [
   'Revise lead time and spec during negotiation',
   'Validate order and fill SAP condition type; approval MKU Manager → GM',
   'DP request or confirm order → sales order (close won)',
   'Extend PN, maintain master data, calculate sharing profit',
   'Release PO Interco: MKU Manager → GM → Director',
   'Pass PATRIA production progress to BC weekly'],
  'Example: PO for 2 lube trucks → new PN created → PO Interco released to PATRIA → weekly progress to BC.'),
 ('After-sales activities', [
   'Warehouse receives unit; QC; PATRIA repairs if needed',
   'Issue BAST and SPB/BAPB',
   'MKU creates delivery plan',
   'Deliver unit with BC; customer signs SPB and BAST',
   'Documents to Finance for invoice and payment'],
  'Example: crane truck passes QC → delivery plan to Sangatta site → BAST signed → invoice issued.')]
for i, (h, L, ex) in enumerate(COLS):
    x = 56 + i * (w + gap)
    card(s, x, 230, w, 318, h, lcolor=GREEN_D)
    tx(s, x + 14, 256, w - 28, 290, L, 11.5, INK, bullets=True, lh=1.08, emph=False)
    rect(s, x, 560, w, 106, GREEN_L, radius=10)
    tx(s, x + 14, 572, w - 28, 90, ex, 11, GREEN_D, True, lh=1.08, emph=False)
tx(s, 56, 674, 1168, 14, 'Source: Flow Transaksi UNIT Tobe (154 steps); supply chain = Marketing Unit, Application Engineering, PATRIA, Warehouse.', 8, MUTED, emph=False)
P.save('/home/user/6month/nedp_deck/v4/Slide_SupplyChain_Flow.pptx'); print('ok')
