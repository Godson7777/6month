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
    set_runs(c.text_frame.paragraphs[0], 'After Sales/' if 'Medium' in c.text_frame.text else 'What happens after the unit is delivered?')
t2 = SH['Table 2'].table
set_runs(t2.cell(0, 0).text_frame.paragraphs[0], 'After delivery, I monitor unit performance and make sure problems do not repeat')
set_runs(t2.cell(1, 0).text_frame.paragraphs[0], 'Units under warranty are monitored, and every failure is followed up.')
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
STEPS = [
 ('Monitor Unit Performance', ['Monitor unit performance', 'Gather customer feedback'], 'as1_warranty.png'),
 ('Follow Up Problems', ['Follow up problems', 'Ensure the problem is not repeated in other orders'], 'as2_failure.png'),
]
for i, (head, bullets, f) in enumerate(STEPS):
    W = 600; x = 36 + i * (W + 6)
    hb = s.shapes.add_shape(MSO_SHAPE.CHEVRON if i else MSO_SHAPE.PENTAGON, E(x), E(222), E(W), E(30))
    hb.fill.solid(); hb.fill.fore_color.rgb = rgb('1E9E57'); hb.line.fill.background(); hb.shadow.inherit = False
    tf = hb.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER; r = tf.paragraphs[0].add_run()
    r.text = f'{i + 1}. {head}'; r.font.size = Pt(14); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = rgb('FFFFFF')
    tx(x + 4, 262, W - 8, 50, ['• ' + b for b in bullets], 10.5)
    pic(f, x, 310, W, 360)
tx(36, 678, 1206, 14, ['Photos: warranty unit population report and product failure analysis.'], 7, '6B6B6B')
P.save('v7/Slide_AfterSales.pptx'); print('ok', len(P.slides))
