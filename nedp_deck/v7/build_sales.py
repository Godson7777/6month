"""One slide: Pre Sales (Demand Check, Preliminary Drawing Review, Request Quote to UTE) with photos, in the user's deck style."""
import copy, os
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
E = lambda v: Emu(round(v * 9525)); rgb = RGBColor.from_string; FONT = 'Neue Haas Grotesk Text Pro'
P = Presentation('v7/6M_V9.pptx'); L = P.slides._sldIdLst
for i, sid in reversed(list(enumerate(list(L)))):
    if i != 13: P.part.drop_rel(sid.rId); L.remove(sid)
src = P.slides[0]
s = P.slides.add_slide(src.slide_layout)
for ph in list(s.placeholders): ph._element.getparent().remove(ph._element)
for sh in src.shapes:
    if sh.name in ('Date Placeholder 3', 'Slide Number Placeholder 5', 'Title 10', 'Group 31', 'Straight Connector 34', 'Table 2'):
        s.shapes._spTree.append(copy.deepcopy(sh._element))
P.part.drop_rel(L[0].rId); L.remove(L[0])
def set_runs(par, text):
    rs = par.runs; rs[0].text = text
    for r in rs[1:]: r._r.getparent().remove(r._r)
SH = {sh.name: sh for sh in s.shapes}
for c in SH['Group 31'].shapes:
    set_runs(c.text_frame.paragraphs[0], 'Sales/' if 'Medium' in c.text_frame.text else 'What happens after the PO comes in?')
t2 = SH['Table 2'].table
set_runs(t2.cell(0, 0).text_frame.paragraphs[0], 'After the PO, I lock the order details, follow production and push billing to invoice')
set_runs(t2.cell(1, 0).text_frame.paragraphs[0], 'From Close Won to invoice, so the unit reaches the customer on the agreed RFD.')
def tx(x, y, w, h, paras, sz, color='000000', bold=False, al=PP_ALIGN.LEFT):
    b = s.shapes.add_textbox(E(x), E(y), E(w), E(h)); tf = b.text_frame; tf.word_wrap = True
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
    for i, t in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.alignment = al; p.space_after = Pt(3)
        r = p.add_run(); r.text = t; r.font.size = Pt(sz); r.font.name = FONT; r.font.bold = bold; r.font.color.rgb = rgb(color)
    return b
os.makedirs('/tmp/claude-0/ps', exist_ok=True)
def pic(f, x, y, w, h):
    path = 'assets/evidence/' + f
    if f.endswith('.webp'):
        out = '/tmp/claude-0/ps/' + f.replace('.webp', '.png'); Image.open(path).convert('RGB').save(out); path = out
    iw, ih = Image.open(path).size; k = min(w / iw, h / ih); pw, ph = iw * k, ih * k
    fr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
    fr.fill.solid(); fr.fill.fore_color.rgb = rgb('F2F2F2'); fr.line.fill.background(); fr.shadow.inherit = False
    p_ = s.shapes.add_picture(path, E(x + (w - pw) / 2), E(y + (h - ph) / 2), E(pw), E(ph))
    p_.line.color.rgb = rgb('D9D9D9'); p_.line.width = Pt(.5)
def chips(x, y, w, title, items, cols):
    tx(x, y, w, 14, [title], 9.5, '1E9E57', True)
    cw = (w - (cols - 1) * 4) / cols; ch_ = 22
    for k, it in enumerate(items):
        cx = x + (k % cols) * (cw + 4); cy = y + 18 + (k // cols) * (ch_ + 4)
        b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(cx), E(cy), E(cw), E(ch_))
        b.fill.solid(); b.fill.fore_color.rgb = rgb('F2F2F2'); b.line.fill.background(); b.shadow.inherit = False
        tf = b.text_frame; tf.margin_left = tf.margin_right = E(2); tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = it
        r.font.size = Pt(8.5); r.font.name = FONT; r.font.color.rgb = rgb('000000')
    return y + 18 + ((len(items) - 1) // cols + 1) * (ch_ + 4)
STEPS = [
 ('Close Won → CPO', ['PO, preliminary drawing and PJB checked in CRM',
                      'QFD requested from UTE; special requests and painting style collected from the Business Consultant',
                      'RFD date in the QFD becomes the due date of the PO Interco'], []),
 ('Production Monitoring', ['Production followed regularly: plant visits or photos from Nandu',
                      'QFD plan compared with actual production',
                      'Issues that put the RFD at risk escalated early',
                      'Painting style requested at least one month before RFD',
                      'Customer FAT joined with the Business Consultant'],
  [('sc5_72.webp', 0, 12, 194, 136), ('sc5_73.webp', 200, 12, 194, 136), ('sc5_74.webp', 0, 154, 194, 136), ('sc5_75.webp', 200, 154, 194, 136)]),
 ('Billing', ['Weekly billing tracker per unit, up to BAST and invoice',
              'Monthly report: target, carry over, additional, actual',
              'PICA on carry-over units: cause and corrective action',
              'Blockages escalated until the invoice goes out'],
  [('s4_a.webp', 0, 16, 394, 164), ('s4_b.webp', 0, 186, 394, 104)]),
]
for i, (head, bullets, pics) in enumerate(STEPS):
    x = 36 + i * 406; W = 394
    hb = s.shapes.add_shape(MSO_SHAPE.CHEVRON if i else MSO_SHAPE.PENTAGON, E(x), E(222), E(W), E(30))
    hb.fill.solid(); hb.fill.fore_color.rgb = rgb('1E9E57'); hb.line.fill.background(); hb.shadow.inherit = False
    tf = hb.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER; r = tf.paragraphs[0].add_run()
    r.text = f'{i + 1}. {head}'; r.font.size = Pt(14); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = rgb('FFFFFF')
    tx(x + 4, 262, W - 8, 112, ['• ' + b for b in bullets], 10.5)
    for f, dx, dy, w, h in pics: pic(f, x + dx, 380 + dy, w, h)
from pptx.enum.dml import MSO_LINE_DASH_STYLE
fx, fy, fw, fh = 36, 502, 394, 168
fb = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(fx), E(fy), E(fw), E(fh))
fb.fill.background(); fb.line.color.rgb = rgb('9E9E9E'); fb.line.width = Pt(1); fb.line.dash_style = MSO_LINE_DASH_STYLE.DASH; fb.shadow.inherit = False
tg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(fx + 10), E(fy - 9), E(46), E(18))
tg.fill.solid(); tg.fill.fore_color.rgb = rgb('6B6B6B'); tg.line.fill.background(); tg.shadow.inherit = False
r = tg.text_frame.paragraphs[0].add_run(); r.text = 'FYI'; r.font.size = Pt(9); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = rgb('FFFFFF')
tg.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER; tg.text_frame.margin_top = tg.text_frame.margin_bottom = 0
y = chips(fx + 12, fy + 18, fw - 24, 'CLOSE WON APPROVAL', ['Sales Manager', '→ Marketing Associate', '→ Marketing Manager', '→ GM Marketing'], 2)
chips(fx + 12, y + 12, fw - 24, 'PO INTERCO APPROVAL', ['Marketing Manager', '→ GM Marketing', '→ Marketing Director'], 3)
tx(36, 678, 1206, 14, ['Photos: unit production at the UTE plant; billing report with PICA, and weekly billing tracker.'], 7, '6B6B6B')
P.save('v7/Slide_Sales.pptx'); print('ok', len(P.slides))
