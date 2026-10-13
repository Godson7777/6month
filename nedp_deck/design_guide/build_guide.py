"""Design Guidance deck for the 6-month review, built on Template_PPT_2026_V3.pptx.
Every element is a native, editable PowerPoint shape (Arial only).
Run from nedp_deck/:  python3 design_guide/build_guide.py"""
import copy, io
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.dml import MSO_LINE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

SRC = "design_guide/Template_PPT_2026_V3.pptx"
OUT = "design_guide/NEDP_6M_Design_Guidance.pptx"
A = "assets/"

# ---- palette (from the template style guide) ----
BROWN, ORANGE, SAND, PEACH = "80350E", "E55200", "A35F35", "F0A878"
GREY, MUTED, INK, WASH = "B8BEC4", "6E7B84", "26262A", "F7F8FA"
BORDER, RULE, TINT, WHITE = "C9D0D7", "E4E8EB", "FDEEE4", "FFFFFF"
X0, X1, Y0, Y1 = 45, 915, 75, 505          # body zone in pt

p = Presentation(SRC)
S = list(p.slides)
COVER, PALETTE, TIMEFRAME, BLANK, APPX, THANKS = S
LAYOUT = BLANK.slide_layout                    # 8_Custom Layout: number box, logo, footer
HDR = [copy.deepcopy(sh._element) for sh in BLANK.shapes]          # number, title, subtitle boxes
SRC_BOX = copy.deepcopy(next(sh._element for sh in PALETTE.shapes if sh.has_text_frame and sh.text_frame.text.startswith("Source")))


def rgb(h): return RGBColor.from_string(h)


def set_text(el_shape, text):
    """Replace the text of a copied text box but keep its first run's formatting."""
    tf = el_shape.text_frame
    p0 = tf.paragraphs[0]
    for extra in tf.paragraphs[1:]:
        extra._p.getparent().remove(extra._p)
    runs = p0.runs
    runs[0].text = text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def new_slide(num, title, sub, source="Source: Triatra Template PPT 2026 V3; design references collected for this guide"):
    s = p.slides.add_slide(LAYOUT)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    for el in HDR:
        s.shapes._spTree.append(copy.deepcopy(el))
    num_box, t_box, s_box = [sh for sh in s.shapes if sh.has_text_frame][:3]
    by_y = sorted([num_box, t_box, s_box], key=lambda x: (x.left, x.top))
    nb = min([num_box, t_box, s_box], key=lambda x: x.left)
    rest = sorted([x for x in (num_box, t_box, s_box) if x is not nb], key=lambda x: x.top)
    set_text(nb, num); set_text(rest[0], title); set_text(rest[1], sub)
    if len(num) > 3:
        for r in nb.text_frame.paragraphs[0].runs: r.font.size = Pt(13)
    s.shapes._spTree.append(copy.deepcopy(SRC_BOX))
    set_text([sh for sh in s.shapes if sh.has_text_frame][-1], source)
    return s


def T(s, x, y, w, h, text, size=10, bold=False, color=INK, align="l", anchor="t", spc=0, line=None, wrap=True):
    """Text box. `text` may be a string or a list of paragraphs; each paragraph a string or list of
    (text, {size,bold,color}) runs."""
    tb = s.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    paras = text if isinstance(text, list) else [text]
    for i, para in enumerate(paras):
        pp = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        pp.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        if line: pp.line_spacing = line
        runs = para if isinstance(para, list) else [(para, {})]
        for t, o in runs:
            r = pp.add_run(); r.text = t; f = r.font
            f.name = "Arial"; f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold)
            f.color.rgb = rgb(o.get("color", color))
            sp = o.get("spc", spc)
            if sp: r._r.get_or_add_rPr().set("spc", str(int(sp * 100)))
    return tb


def R(s, x, y, w, h, fill=None, line=None, lw=0.75, shape="rect", radius=0.10, dash=False):
    kind = {"rect": MSO_SHAPE.RECTANGLE, "round": MSO_SHAPE.ROUNDED_RECTANGLE, "oval": MSO_SHAPE.OVAL,
            "chevron": MSO_SHAPE.CHEVRON, "pent": MSO_SHAPE.PENTAGON, "pie": MSO_SHAPE.PIE}[shape]
    sh = s.shapes.add_shape(kind, Pt(x), Pt(y), Pt(w), Pt(h))
    if shape == "round": sh.adjustments[0] = radius
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    else: sh.fill.background()
    if line:
        sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
        if dash: sh.line.dash_style = MSO_LINE.DASH
    else: sh.line.fill.background()
    sh.shadow.inherit = False
    sh.text_frame.margin_left = sh.text_frame.margin_right = Pt(4)
    return sh


def L(s, x1, y1, x2, y2, color=RULE, w=0.75):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(x1), Pt(y1), Pt(x2), Pt(y2))
    c.line.color.rgb = rgb(color); c.line.width = Pt(w)
    return c


def label(s, x, y, w, text):
    """Template section label: brown 8.5 pt caps + hairline."""
    T(s, x, y, w, 14, text, 8.5, True, BROWN)
    R(s, x, y + 17, w, 1, RULE)


def tag(s, x, y, n, fill=BROWN, size=18):
    o = R(s, x, y, size, size, fill, shape="oval")
    T(s, x, y, size, size, str(n), 8.5, True, WHITE, "c", "m")
    return o


def picture(s, path, x, y, w, h, crop=True):
    """Insert a picture cropped (centre) to fill w × h without distortion."""
    im = Image.open(path)
    if im.mode not in ("RGB", "RGBA"): im = im.convert("RGBA")
    b = io.BytesIO(); im.save(b, "PNG" if im.mode == "RGBA" else "JPEG", quality=92); b.seek(0)
    pic = s.shapes.add_picture(b, Pt(x), Pt(y), Pt(w), Pt(h))
    iw, ih = im.size; target = w / h
    if crop:
        if iw / ih > target:
            e = (1 - target * ih / iw) / 2; pic.crop_left = pic.crop_right = e
        else:
            e = (1 - (iw / target) / ih) / 2; pic.crop_top = pic.crop_bottom = e
    return pic


def fit(path, x, y, w, h):
    """Return a box that fits the image inside w × h (contain), centred."""
    iw, ih = Image.open(path).size; sc = min(w / iw, h / ih)
    return x + (w - iw * sc) / 2, y + (h - ih * sc) / 2, iw * sc, ih * sc


slides = []

# ======================================================================= 0.1 principles
s = new_slide("0.1", "DESIGN GUIDANCE — PRINCIPLES", "Every slide in the 6-month review should be clear at first glance",
              "Source: layout ideas adapted from the Bitwise Asset Management website (editorial headline, stat row, whitespace)")
T(s, X0, 92, X1 - X0, 14, "WHY THIS GUIDE", 8.5, True, MUTED, "c", spc=2)
T(s, X0, 108, X1 - X0, 30, [[("One deck, one look, one ", {}), ("clear", {"color": ORANGE}), (" story.", {})]], 22, True, INK, "c")
T(s, 170, 140, 620, 30, "A shared standard for colour, type, layout and evidence, so reviewers spend their time on the content and not on decoding the slide.",
  10, False, MUTED, "c")
L(s, X0 - 25, 222, X1 + 25, 222, RULE, 1)
cols = [("One message per slide", "The subtitle states the conclusion and the body only proves it. If a slide needs two messages, split it into two slides."),
        ("Evidence over adjectives", "Show the number, the photo, the screenshot or the document. Replace words such as 'significant' with the figure and its source."),
        ("Whitespace is structure", "Group items with space, not with extra boxes. Align everything to the grid so the eye reads left to right, top to bottom.")]
for i, (h, b) in enumerate(cols):
    x = X0 + i * 300
    T(s, x, 192, 270, 16, h, 11, True, INK)
    R(s, x, 218.5, 7, 7, ORANGE, shape="oval")
    T(s, x, 236, 265, 60, b, 9.5, False, MUTED, line=1.15)
R(s, X0, 318, X1 - X0, 170, WASH)
T(s, X0 + 24, 334, 400, 14, "THE STANDARD IN FOUR NUMBERS", 8.5, True, MUTED, spc=2)
stats = [("1", "message per slide, written as the subtitle"), ("≤ 6", "bullets per box, one line each where possible"),
         ("3", "colours on one slide, plus the neutrals"), ("8.5 pt", "smallest text size, including sources")]
for i, (n, t) in enumerate(stats):
    x = X0 + 24 + i * 210
    if i: L(s, x - 14, 368, x - 14, 462, BORDER)
    T(s, x, 362, 190, 44, n, 32, True, ORANGE)
    T(s, x, 412, 180, 40, t, 9.5, True, INK, line=1.1)
slides.append(s)

# ======================================================================= 0.2 anatomy
s = new_slide("0.2", "DESIGN GUIDANCE — SLIDE ANATOMY", "Six fixed zones: the header carries the message, the body proves it")
fx, fy, fw, fh = X0, 86, 470, 264.4                  # mini slide (scale 0.49)
k = fw / 960
R(s, fx, fy, fw, fh, WHITE, BORDER, 1)
R(s, fx + 19 * k, fy + 21 * k, 42 * k, 19 * k, ORANGE)
T(s, fx + 19 * k, fy + 21 * k, 42 * k, 19 * k, "1", 7, True, WHITE, "c", "m")
T(s, fx + 71 * k, fy + 13 * k, 300, 9, "MAJOR SLIDE TITLE", 6, True, ORANGE)
T(s, fx + 71 * k, fy + 30 * k, 360, 10, "Subtitle written as the message of the slide", 7, True, INK)
R(s, fx + fw - 50, fy + 7, 38, 15, TINT); T(s, fx + fw - 50, fy + 7, 38, 15, "LOGO", 5.5, True, ORANGE, "c", "m")
R(s, fx, fy + 62 * k, fw, 0.8, RULE)
R(s, fx + X0 * k, fy + Y0 * k, (X1 - X0) * k, (Y1 - Y0) * k, TINT, PEACH, 0.75, dash=True)
T(s, fx + X0 * k, fy + Y0 * k, (X1 - X0) * k, (Y1 - Y0) * k, ["BODY ZONE", "870 × 430 pt"], 8, True, SAND, "c", "m")
T(s, fx + 20 * k, fy + 521 * k, 200, 7, "Source: Internal resources", 4.5, False, MUTED)
T(s, fx + fw - 205, fy + 521 * k, 200, 7, "© 2026 PT Triatra Sinergia Pratama …   Page 4", 4.5, False, MUTED, "r")
for n, (cx, cy) in enumerate([(19, 21), (71 + 150, 10), (71 + 300, 32), (X0 + 22, Y0 + 30), (20 + 110, 521), (900, 521)], 1):
    tag(s, fx + cx * k - 7, fy + cy * k - 16 if n in (1, 2, 3) else fy + cy * k - 7, n, BROWN, 14)
specs = [("Number box", "Section.slide number. White 16 pt bold on Orange. Already in the layout."),
         ("Major title", "Topic in CAPS. Arial 12 pt bold, Orange E55200. One line only."),
         ("Subtitle = message", "A full sentence with the takeaway. Arial 14 pt bold, Ink 26262A. Max two lines."),
         ("Body zone", "x 45–915 pt, y 75–505 pt. Nothing outside it except the logo and the footer."),
         ("Source line", "Arial 9 pt, Muted 6E7B84, at y 521 pt. Start with 'Source:'."),
         ("Footer & page", "Copyright and page number come from the master. Never retype them.")]
for i, (h, b) in enumerate(specs):
    y = 88 + i * 44
    tag(s, 540, y, i + 1)
    T(s, 566, y + 1, 350, 14, h, 10, True, BROWN)
    T(s, 566, y + 16, 350, 26, b, 8.5, False, MUTED, line=1.1)
    if i < 5: R(s, 540, y + 40, 375, 0.75, RULE)
R(s, X0, 372, 470, 58, TINT)
T(s, X0 + 12, 380, 446, 12, "NOTE", 8.5, True, ORANGE)
T(s, X0 + 12, 395, 446, 30, "Start every content slide from layout '8_Custom Layout' (Home › Layout). The number box, logo, rule and footer then stay in exactly the same place on every page.",
  9, False, INK, line=1.1)
R(s, X0, 442, 470, 58, BROWN)
T(s, X0 + 12, 450, 446, 12, "KEY TAKEAWAY", 8.5, True, PEACH)
T(s, X0 + 12, 465, 446, 30, "Read only the subtitles from first to last slide: they should tell the whole 6-month story on their own.", 10, True, WHITE, line=1.1)
R(s, 540, 362, 375, 138, WASH)
T(s, 554, 372, 350, 12, "HEADER COPY TEST", 8.5, True, MUTED, spc=1)
T(s, 554, 390, 350, 105, [[("Weak  ", {"bold": True, "color": ORANGE}), ("Supply Chain", {})],
                          [("Better  ", {"bold": True, "color": BROWN}), ("Supply chain: from demand check to monitoring", {})],
                          [("Best  ", {"bold": True, "color": INK}), ("Five-step supply chain keeps every PO on its agreed RFD date", {})]],
  9.5, False, INK, line=1.6)
slides.append(s)

# ======================================================================= 0.3 grid
s = new_slide("0.3", "DESIGN GUIDANCE — GRID & SPACING", "A 12-column grid with 12 pt gutters keeps every slide aligned")
label(s, X0, 84, X1 - X0, "1 · 12-COLUMN GRID  (column 61.5 pt · gutter 12 pt · margins 45 pt)")
cw = (X1 - X0 - 11 * 12) / 12
for i in range(12):
    x = X0 + i * (cw + 12)
    R(s, x, 110, cw, 60, TINT)
    T(s, x, 110, cw, 60, str(i + 1), 11, True, PEACH, "c", "m")
label(s, X0, 184, X1 - X0, "2 · COMMON SPLITS")
splits = [([12], "Full width · chart, table, timeline"), ([6, 6], "Halves · before / after, two products"),
          ([4, 8], "One third + two thirds · photo + explanation"), ([4, 4, 4], "Thirds · three pillars, three steps"),
          ([3, 3, 3, 3], "Quarters · KPI row, four cards")]
for r, (parts, txt) in enumerate(splits):
    y = 210 + r * 30; x = X0
    for n in parts:
        w = n * cw + (n - 1) * 12
        R(s, x, y, w * 0.70, 22, WASH, BORDER, 0.75)
        T(s, x, y, w * 0.70, 22, f"{n} col", 8.5, True, MUTED, "c", "m")
        x += w * 0.70 + 12 * 0.7
    T(s, X0 + 870 * 0.70 + 20, y + 4, 240, 16, txt, 9, False, INK)
label(s, X0, 368, X1 - X0, "3 · SPACING SCALE  (use only these steps)")
steps = [(4, "Icon → label"), (8, "Inside a card"), (12, "Card → card (gutter)"), (16, "Card padding"), (24, "Group → group"), (36, "Section → section")]
for i, (v, t) in enumerate(steps):
    x = X0 + i * 145
    R(s, x, 396 + (36 - v), v, v, ORANGE)
    T(s, x + 44, 402, 100, 14, f"{v} pt", 12, True, INK)
    T(s, x + 44, 418, 100, 14, t, 8.5, False, MUTED)
R(s, X0, 452, X1 - X0, 48, TINT)
T(s, X0 + 12, 460, 850, 34, [[("Rule of thumb  ", {"bold": True, "color": ORANGE}),
                              ("Space between groups must be at least twice the space inside a group. If two boxes look related, bring them closer; if not, push them apart.", {})]],
  9.5, False, INK, line=1.15)
slides.append(s)

# ======================================================================= 0.4 typography
s = new_slide("0.4", "DESIGN GUIDANCE — TYPOGRAPHY", "Arial only, nine sizes, emphasis with colour and weight")
label(s, X0, 82, X1 - X0, "1 · TYPE SCALE — ARIAL")
T(s, X0, 104, 140, 12, "ROLE", 8, True, MUTED, spc=1); T(s, 200, 104, 400, 12, "SAMPLE", 8, True, MUTED, spc=1)
T(s, 640, 104, 275, 12, "SPEC", 8, True, MUTED, spc=1)
rows = [("Cover title", "Design Guidance", 28, True, ORANGE, "28–32 pt · Bold · Orange"),
        ("Major slide title", "MAJOR SLIDE TITLE", 12, True, ORANGE, "12 pt · Bold · CAPS · Orange"),
        ("Subtitle / message", "Five F.lli Ferrari cranes win on price", 14, True, INK, "14 pt · Bold · Ink"),
        ("Key number", "31 units", 22, True, ORANGE, "20–28 pt · Bold · Orange"),
        ("Section label", "1 · COLOUR PALETTE", 8.5, True, BROWN, "8.5 pt · Bold · CAPS · Brown"),
        ("Card title", "Card title", 10, True, BROWN, "10 pt · Bold · Brown"),
        ("Body", "Body text explains, in two to four lines.", 10, False, INK, "10 pt · Regular · Ink · spacing 1.1"),
        ("Detail / label", "Supporting detail, two lines max", 8.5, False, MUTED, "8.5 pt · Regular · Muted"),
        ("Source", "Source: Internal resources", 9, False, MUTED, "9 pt · Regular · Muted · y 521 pt")]
y = 120
for role, sample, sz, b, c, spec in rows:
    h = max(22, sz * 1.35)
    T(s, X0, y + (h - 12) / 2, 150, 12, role, 9, True, INK)
    T(s, 200, y, 430, h, sample, sz, b, c, anchor="m", spc=1 if sample.isupper() and sz < 10 else 0)
    T(s, 640, y + (h - 12) / 2, 275, 12, spec, 8.5, False, MUTED)
    R(s, X0, y + h + 3, X1 - X0, 0.75, RULE)
    y += h + 7
notes = [("EMPHASIS", "Orange or Bold only. Never underline, italic, shadow or WordArt."),
         ("HIERARCHY", "Max two sizes inside one box. Bigger means more important, not more text."),
         ("ALIGNMENT", "Left-align text. Centre only key numbers and single-line labels.")]
for i, (h, b) in enumerate(notes):
    x = X0 + i * 294
    R(s, x, 454, 282, 48, TINT)
    T(s, x + 10, 461, 262, 12, h, 8.5, True, ORANGE)
    T(s, x + 10, 475, 262, 26, b, 9, False, INK, line=1.1)
slides.append(s)

# ======================================================================= 0.6 colour usage
s = new_slide("0.6", "DESIGN GUIDANCE — COLOUR IN USE", "Mostly white and ink, orange only where the eye must land")
label(s, X0, 84, X1 - X0, "1 · PROPORTION ON A CONTENT SLIDE")
x = X0
for pct, fill, name, tc in [(60, WASH, "60% White / Wash — background, cards", MUTED), (25, INK, "25% Ink / Muted — text", WHITE),
                            (10, ORANGE, "10% Orange", WHITE), (5, BROWN, "5%", WHITE)]:
    w = (X1 - X0) * pct / 100
    R(s, x, 110, w, 30, fill, BORDER if fill == WASH else None)
    T(s, x + 8, 110, w - 10, 30, name, 8.5, True, tc, anchor="m")
    x += w
T(s, X0, 146, 870, 14, "Brown, Sand and Peach are accents for takeaways, phases and chart series. Orange full-bleed is reserved for the cover, dividers, appendix and closing.",
  8.5, False, MUTED)
label(s, X0, 174, X1 - X0, "2 · CHART SERIES ORDER")
for i, (c, n) in enumerate([(ORANGE, "1 · Focus / Triatra"), (BROWN, "2 · Second series"), (SAND, "3 · Third"), (PEACH, "4 · Fourth"),
                            (GREY, "5 · Others / benchmark"), (MUTED, "6 · Total / reference")]):
    x = X0 + i * 147
    R(s, x, 200, 26, 18, c); T(s, x + 32, 202, 112, 14, n, 8.5, True, INK)
T(s, X0, 224, 870, 14, "Competitors and 'others' always in Grey so the focus series stays readable, even when printed in black and white.", 8.5, False, MUTED)
label(s, X0, 252, X1 - X0, "3 · DO AND DON'T")
pairs = [((WHITE, ORANGE, "Rp 1.240 jt", BORDER), "Orange number on white", (PEACH, ORANGE, "Rp 1.240 jt", None), "Orange on peach — too low contrast"),
         ((BROWN, WHITE, "Key takeaway", None), "White text on Brown or Orange", (ORANGE, GREY, "Key takeaway", None), "Grey text on Orange"),
         ((WASH, INK, "Neutral card", BORDER), "Neutral card, one accent", (ORANGE, WHITE, "Orange card", None), "Every card in Orange — nothing stands out")]
for i, (do, dt, dont, nt) in enumerate(pairs):
    x = X0 + i * 294
    for j, ((f, tc, txt, ln), cap, mark, mc) in enumerate([(do, dt, "DO", BROWN), (dont, nt, "DON'T", ORANGE)]):
        yy = 280 + j * 110
        T(s, x, yy, 60, 12, mark, 8.5, True, mc, spc=1)
        R(s, x, yy + 16, 282, 52, f, ln)
        T(s, x, yy + 16, 282, 52, txt, 16, True, tc, "c", "m")
        T(s, x, yy + 72, 282, 24, cap, 8.5, False, INK if j == 0 else MUTED)
slides.append(s)

# ======================================================================= 0.7 components
s = new_slide("0.7", "DESIGN GUIDANCE — COMPONENTS", "Eight reusable blocks beyond the basic boxes — copy them from here")
cards = [(X0 + i * 220, 84 + j * 212) for j in range(2) for i in range(4)]
CW, CH = 208, 200
names = ["SECTION INTRO", "STAT ROW", "WHY COLUMNS", "NUMBERED LIST", "STATUS CHIPS", "CALL-TO-ACTION TAGS", "ICON LIST", "LOGO STRIP"]
for (x, y), n in zip(cards, names):
    R(s, x, y, CW, CH, WHITE, BORDER, 0.75)
    T(s, x + 12, y + 10, CW - 24, 12, n, 8, True, MUTED, spc=1)
    R(s, x + 12, y + 26, CW - 24, 0.75, RULE)
(x, y) = cards[0]
T(s, x + 12, y + 46, CW - 24, 12, "SUPPLY CHAIN", 8, True, MUTED, "c", spc=2)
T(s, x + 12, y + 62, CW - 24, 44, [[("From demand to ", {}), ("delivery", {"color": ORANGE}), (".", {})]], 14, True, INK, "c")
T(s, x + 12, y + 118, CW - 24, 40, "Kicker + headline open a section or a dense slide. One orange word only.", 8.5, False, MUTED, "c", line=1.1)
(x, y) = cards[1]
for i, (n, t) in enumerate([("67", "units / yr"), ("41%", "of units"), ("64%", "of value")]):
    xx = x + 14 + i * 64
    if i: L(s, xx - 6, y + 52, xx - 6, y + 104, BORDER)
    T(s, xx, y + 52, 58, 30, n, 20, True, ORANGE); T(s, xx, y + 84, 58, 20, t, 8.5, True, INK)
T(s, x + 12, y + 126, CW - 24, 60, "Three to four numbers, label under each, hairline dividers. Numbers come from the source line.", 8.5, False, MUTED, line=1.1)
(x, y) = cards[2]
L(s, x + 8, y + 76, x + CW - 8, y + 76, RULE, 1)
for i, t in enumerate(["Plan", "Execute", "Monitor"]):
    xx = x + 14 + i * 64
    T(s, xx, y + 50, 60, 14, t, 9, True, INK); R(s, xx, y + 73, 6, 6, ORANGE, shape="oval")
    T(s, xx, y + 86, 56, 34, "Short line of proof", 8, False, MUTED, line=1.1)
T(s, x + 12, y + 132, CW - 24, 56, "Title above, dot on one thin line, text below. Use for 3 pillars or a simple process.", 8.5, False, MUTED, line=1.1)
(x, y) = cards[3]
for i, (c, t, d) in enumerate([("A1", "Market size", "Units and value by class"), ("A2", "Price check", "Head to head by tm class"), ("A3", "Advantage", "Five cranes that win")]):
    yy = y + 36 + i * 34
    T(s, x + 12, yy, 30, 16, c, 12, True, ORANGE); T(s, x + 44, yy, 150, 14, t, 9.5, True, INK)
    T(s, x + 44, yy + 14, 150, 12, d, 8, False, MUTED); R(s, x + 12, yy + 29, CW - 24, 0.75, RULE)
T(s, x + 12, y + 142, CW - 24, 50, "Agenda, appendix list, step list. Code in Orange, title Ink, detail Muted.", 8.5, False, MUTED, line=1.1)
(x, y) = cards[4]
for i, (t, f, tc, ln) in enumerate([("Done", BROWN, WHITE, None), ("On going", SAND, WHITE, None), ("Not started", WHITE, MUTED, BORDER), ("At risk", ORANGE, WHITE, None)]):
    xx = x + 12 + (i % 2) * 94; yy = y + 42 + (i // 2) * 30
    R(s, xx, yy, 86, 20, f, ln, shape="round", radius=0.5); T(s, xx, yy, 86, 20, t, 8.5, True, tc, "c", "m")
T(s, x + 12, y + 112, CW - 24, 70, "Pill chips for status in tables and timelines. Same four words and colours everywhere in the deck.", 8.5, False, MUTED, line=1.1)
(x, y) = cards[5]
R(s, x + 12, y + 44, 86, 24, None, ORANGE, 1); T(s, x + 12, y + 44, 86, 24, "SEE APPENDIX", 8, True, ORANGE, "c", "m", spc=1)
R(s, x + 108, y + 44, 86, 24, ORANGE); T(s, x + 108, y + 44, 86, 24, "DECISION", 8, True, WHITE, "c", "m", spc=1)
T(s, x + 12, y + 82, CW - 24, 100, "Outline tag points to more detail; filled tag marks the one thing you ask the reviewer to decide. Max one filled tag per slide.",
  8.5, False, MUTED, line=1.1)
(x, y) = cards[6]
for i, t in enumerate(["Weekly market update", "Price simulation tool", "Site visit photos"]):
    yy = y + 40 + i * 26
    R(s, x + 12, yy, 18, 18, WASH, BORDER, 0.5, shape="oval"); T(s, x + 12, yy, 18, 18, "›", 10, True, ORANGE, "c", "m")
    T(s, x + 38, yy + 3, 150, 14, t, 9, False, INK)
T(s, x + 12, y + 124, CW - 24, 60, "Replaces plain bullets when each line is a deliverable or a resource.", 8.5, False, MUTED, line=1.1)
(x, y) = cards[7]
for i in range(6):
    xx = x + 12 + (i % 3) * 62; yy = y + 40 + (i // 3) * 34
    R(s, xx, yy, 56, 26, WASH); T(s, xx, yy, 56, 26, "LOGO", 7, True, GREY, "c", "m")
T(s, x + 12, y + 118, CW - 24, 70, "Partners, brands or competitors. Same box size, logos in original colours, aligned on one baseline.", 8.5, False, MUTED, line=1.1)
slides.append(s)

# ======================================================================= 0.8 data viz
s = new_slide("0.8", "DESIGN GUIDANCE — CHARTS & TABLES", "Highlight one series, label directly, cite the source",
              "Source: chart values are the example Medium-class units (2023–2026) from the F.lli Ferrari market study")
label(s, X0, 84, 480, "1 · CHART — NATIVE, EDITABLE")
cd = CategoryChartData(); cd.categories = ["2023", "2024", "2025", "2026*"]
cd.add_series("Medium", (71, 59, 54, 19)); cd.add_series("Others", (122, 91, 107, 59))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Pt(X0), Pt(108), Pt(480), Pt(220), cd)
ch = gf.chart; ch.has_legend = True; ch.legend.include_in_layout = False; ch.legend.position = XL_LEGEND_POSITION.TOP
ch.legend.font.size = Pt(8.5); ch.legend.font.color.rgb = rgb(MUTED)
for ser, c in zip(ch.plots[0].series, [ORANGE, GREY]):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(c)
pl = ch.plots[0]; pl.gap_width = 60; pl.overlap = -10; pl.has_data_labels = True
dl = pl.data_labels; dl.font.size = Pt(8.5); dl.font.bold = True; dl.font.color.rgb = rgb(INK); dl.position = XL_LABEL_POSITION.OUTSIDE_END
va = ch.value_axis; va.visible = False; va.has_major_gridlines = False
ca = ch.category_axis; ca.tick_labels.font.size = Pt(9); ca.tick_labels.font.color.rgb = rgb(MUTED); ca.format.line.color.rgb = rgb(BORDER)
for el in gf._element.iter():
    pass
T(s, X0, 330, 480, 12, "Units per year. *2026 = Jan–14 Aug.", 8.5, False, MUTED)
label(s, X0, 352, 480, "2 · TABLE")
tb = s.shapes.add_table(5, 4, Pt(X0), Pt(376), Pt(480), Pt(120)).table
data = [["Class", "Units", "Import value", "Share"], ["Light", "177", "Rp 40.118 jt", "12%"], ["Small", "200", "Rp 77.241 jt", "24%"],
        ["Medium", "196", "Rp 118.328 jt", "36%"], ["Total", "638", "Rp 326.841 jt", "100%"]]
tbl_el = tb._tbl
tbl_el.tblPr.set("firstRow", "0"); tbl_el.tblPr.set("bandRow", "0")
for ri, row in enumerate(data):
    for ci, v in enumerate(row):
        c = tb.cell(ri, ci); c.fill.background(); c.margin_left = c.margin_right = Pt(6); c.margin_top = c.margin_bottom = Pt(3)
        c.text = v; para = c.text_frame.paragraphs[0]; para.alignment = PP_ALIGN.RIGHT if ci else PP_ALIGN.LEFT
        r = para.runs[0]; r.font.name = "Arial"; r.font.size = Pt(8.5 if ri == 0 else 9.5)
        r.font.bold = ri in (0, 4) or (ri == 3); r.font.color.rgb = rgb(MUTED if ri == 0 else (ORANGE if ri == 3 else INK))
        tcPr = c._tc.get_or_add_tcPr()
        for side in ("lnL", "lnR", "lnT", "lnB"):
            ln = etree.SubElement(tcPr, qn("a:" + side), w=str(int(Pt(1.2 if (side == "lnB" and ri in (0, 3)) else 0.75))))
            if side in ("lnL", "lnR") or (side == "lnT"):
                etree.SubElement(ln, qn("a:noFill"))
            else:
                sf = etree.SubElement(ln, qn("a:solidFill")); etree.SubElement(sf, qn("a:srgbClr"), val=INK if ri in (0, 3) else RULE)
        # tcPr children must precede the fill already set; move fill last for schema order
        for f in tcPr.findall(qn("a:noFill")) + tcPr.findall(qn("a:solidFill")):
            tcPr.remove(f); tcPr.append(f)
rules = [("Title = insight", "The subtitle says what the chart shows. Units and period go in a small note under the chart."),
         ("One highlight", "Focus series in Orange, every other series Grey. Never a rainbow of categories."),
         ("Label directly", "Data labels on bars, no gridlines, hide the value axis when labels are shown."),
         ("Start at zero", "Bar axes always start at 0. No 3D, no shadows, no pie with more than 4 slices."),
         ("Tables", "Ink rule under header and before total, hairlines between rows, numbers right-aligned, totals bold."),
         ("Native only", "Insert charts and tables from PowerPoint/Excel, never as screenshots, so they stay editable.")]
for i, (h, b) in enumerate(rules):
    y = 88 + i * 68
    tag(s, 556, y, i + 1)
    T(s, 584, y + 1, 330, 14, h, 10, True, BROWN)
    T(s, 584, y + 17, 330, 40, b, 9, False, INK, line=1.12)
    if i < 5: R(s, 556, y + 60, 359, 0.75, RULE)
slides.append(s)

# ======================================================================= 0.10 imagery
s = new_slide("0.10", "DESIGN GUIDANCE — IMAGERY & EVIDENCE", "Photos prove the work: crop with purpose, caption, cite",
              "Source: product cutout, site photo and CRM screenshot from this review deck")
items = [("PRODUCT CUTOUT", A + "cutout/u2.png", "Background removed, placed on Wash, same baseline and height for all units in a row.", "contain"),
         ("FIELD PHOTO", A + "evidence/sc5_73.webp", "Crop to the action (people, unit, plant). Caption bar: what, where, when.", "cover"),
         ("EVIDENCE SCREENSHOT", A + "evidence/sc1_a.png", "Crop to the part that proves the point, 0.75 pt Border frame, source under it.", "cover")]
for i, (h, path, txt, mode) in enumerate(items):
    x = X0 + i * 294; w = 282
    label(s, x, 84, w, f"{i + 1} · {h}")
    if mode == "contain":
        R(s, x, 110, w, 190, WASH)
        bx, by, bw, bh = fit(path, x + 14, 124, w - 28, 162); picture(s, path, bx, by, bw, bh, crop=False)
    else:
        pic = picture(s, path, x, 110, w, 190)
        if i == 2: pic.line.color.rgb = rgb(BORDER); pic.line.width = Pt(0.75)
    if i == 1:
        R(s, x, 276, w, 24, INK); T(s, x + 10, 276, w - 20, 24, "Monitoring · plant visit · 2026", 8.5, True, WHITE, anchor="m")
    if i == 2:
        T(s, x, 304, w, 12, "Source: CRM, Triatra", 8, False, MUTED)
    T(s, x, 322, w, 40, txt, 9, False, INK, line=1.12)
label(s, X0, 372, X1 - X0, "4 · AVOID")
for i, (h, b) in enumerate([("Stretched images", "Lock the aspect ratio; crop instead of squeezing."),
                            ("Low resolution", "Use originals. Below ~150 dpi at the printed size looks blurry."),
                            ("Mixed styles", "One corner style per slide: all square or all rounded."),
                            ("Decoration only", "Every photo must show the unit, the place or the result.")]):
    x = X0 + i * 220
    R(s, x, 398, 208, 100, TINT)
    T(s, x + 12, 408, 184, 14, h, 10, True, ORANGE)
    T(s, x + 12, 426, 184, 64, b, 9, False, INK, line=1.12)
slides.append(s)

# ======================================================================= 0.11 page types
s = new_slide("0.11", "DESIGN GUIDANCE — PAGE TYPES", "Eight page types cover the whole 6-month review")
TW, TH = 200, 112.5
types = [("Cover", "Template title slide; title, prepared for, date"), ("Agenda", "Numbered list, one line per section"),
         ("Section divider", "Orange panel left, section number + list"), ("Content · 2 columns", "Message left, evidence right (4 + 8)"),
         ("KPI dashboard", "Stat row on top, chart or table below"), ("Process / timeline", "Steps or timeframe table, status chips"),
         ("Evidence gallery", "3–4 photos or screenshots with captions"), ("Appendix · Thank you", "List of appendices, closing slide")]


def thumb(s, x, y, kind):
    R(s, x, y, TW, TH, WHITE, BORDER, 0.75)
    if kind in (0, 2, 7):
        R(s, x if kind != 0 else x + TW * 0.47, y, TW * (0.32 if kind != 0 else 0.53), TH, ORANGE)
    if kind == 0:
        R(s, x + 10, y + 40, 60, 8, ORANGE); R(s, x + 10, y + 54, 40, 3, ORANGE); R(s, x + 10, y + 84, 70, 4, GREY)
        return
    if kind not in (2, 7):
        R(s, x + 5, y + 6, 12, 7, ORANGE); R(s, x + 22, y + 5, 60, 3.5, ORANGE); R(s, x + 22, y + 11, 100, 4, INK); R(s, x, y + 19, TW, 0.6, RULE)
    if kind == 1:
        for i in range(6):
            R(s, x + 20, y + 28 + i * 13, 8, 6, ORANGE); R(s, x + 34, y + 29 + i * 13, 90, 4, INK); R(s, x + 20, y + 37 + i * 13, 160, 0.5, RULE)
    elif kind == 2:
        R(s, x + 10, y + 50, 40, 9, WHITE); R(s, x + 82, y + 30, 50, 4, BROWN)
        for i in range(4): R(s, x + 82, y + 42 + i * 12, 100, 4, INK)
    elif kind == 3:
        for i in range(5): R(s, x + 10, y + 30 + i * 10, 55, 4, INK if i == 0 else GREY)
        R(s, x + 76, y + 28, 114, 72, WASH, BORDER, 0.5)
    elif kind == 4:
        for i in range(4):
            R(s, x + 10 + i * 46, y + 27, 40, 24, WASH); R(s, x + 14 + i * 46, y + 31, 18, 8, ORANGE)
        for i, hh in enumerate([30, 22, 38, 16, 26]): R(s, x + 20 + i * 34, y + 102 - hh, 18, hh, ORANGE if i == 2 else GREY)
    elif kind == 5:
        for i in range(5):
            R(s, x + 10, y + 30 + i * 15, 40, 4, INK); R(s, x + 58 + i * 25, y + 28 + i * 15, 45, 8, [BROWN, SAND, PEACH, ORANGE, GREY][i])
    elif kind == 6:
        for i in range(4):
            R(s, x + 10 + i * 46, y + 28, 40, 58, GREY); R(s, x + 10 + i * 46, y + 90, 34, 4, INK)
    elif kind == 7:
        for i in range(3): R(s, x + 76, y + 30 + i * 22, 12, 7, ORANGE); R(s, x + 94, y + 31 + i * 22, 90, 4, INK); R(s, x + 76, y + 43 + i * 22, 110, 0.5, RULE)


for i, (n, d) in enumerate(types):
    x = X0 + (i % 4) * 223.3; y = 86 + (i // 4) * 210
    thumb(s, x, y, i)
    T(s, x, y + TH + 8, TW, 14, f"{i + 1:02d}  {n}", 10, True, INK)
    T(s, x, y + TH + 24, TW, 40, d, 8.5, False, MUTED, line=1.1)
slides.append(s)

# ======================================================================= 0.12 storyline
s = new_slide("0.12", "DESIGN GUIDANCE — STORYLINE", "Recommended flow for the 6-month review: who I am, where I work, what I did, what is next")
secs = [("00", "Personal", "About me, onboarding", "2"), ("01", "Company", "Group, business lines, industries", "2"),
        ("02", "Site", "Operations map", "1"), ("03", "Organization", "Structure, my position", "1"),
        ("04", "Roles", "Products, strategic vs supply chain", "2"), ("05", "Execution", "Strategic + supply chain with evidence", "3–4"),
        ("06", "Project", "Problem, analysis, result", "6–8"), ("07", "Next 6 months", "Learnings, plan, support needed", "2")]
cw = (X1 - X0) / 8
for i, (n, t, d, k_) in enumerate(secs):
    x = X0 + i * cw
    R(s, x, 92, cw + 6, 30, ORANGE if i == 6 else (BROWN if i < 6 else SAND), shape="chevron" if i else "pent")
    T(s, x + (8 if i == 0 else 18), 92, cw - 18, 30, f"{n}  {t}", 8.5, True, WHITE, anchor="m")
    T(s, x + 4, 132, cw - 8, 40, d, 8.5, False, INK, line=1.1)
    T(s, x + 4, 176, cw - 8, 26, k_, 20, True, ORANGE)
    T(s, x + 4, 202, cw - 8, 12, "slides", 8, False, MUTED)
R(s, X0, 222, X1 - X0, 0.75, RULE)
label(s, X0, 236, 420, "WHAT EACH PART MUST ANSWER")
qs = [("Personal & Company", "Do I understand the company I joined and where my products fit?"),
      ("Roles & Execution", "What did I do every month, and what is the evidence?"),
      ("Project", "What problem did I solve, with which data, and what changed?"),
      ("Next 6 months", "What will I deliver next, and what support do I need?")]
for i, (h, q) in enumerate(qs):
    y = 262 + i * 58
    T(s, X0, y, 16, 16, str(i + 1), 13, True, ORANGE)
    T(s, X0 + 24, y, 390, 14, h, 10, True, BROWN)
    T(s, X0 + 24, y + 16, 390, 30, q, 9.5, False, INK, line=1.1)
R(s, 490, 236, 425, 128, BROWN)
T(s, 506, 248, 395, 12, "KEY TAKEAWAY", 8.5, True, PEACH)
T(s, 506, 266, 395, 90, "Spend most slides on Execution and Project: that is where reviewers judge the six months. Company and organization slides only set the context.",
  12, True, WHITE, line=1.15)
R(s, 490, 376, 205, 124, TINT)
T(s, 502, 386, 180, 12, "NOTE", 8.5, True, ORANGE)
T(s, 502, 402, 182, 92, "Target 25–30 main slides for a 30-minute slot, about one minute per slide. Move detail to the appendix.", 9, False, INK, line=1.12)
R(s, 710, 376, 205, 124, ORANGE)
T(s, 722, 386, 180, 12, "ASK", 8.5, True, WHITE)
T(s, 722, 402, 182, 92, "End with one clear request: the decision, approval or support you need from the reviewers.", 9, False, WHITE, line=1.12)
slides.append(s)

# ======================================================================= 0.13 writing
s = new_slide("0.13", "DESIGN GUIDANCE — WRITING & NUMBERS", "Short sentences, real numbers, one format for every figure")
label(s, X0, 84, 470, "1 · HEADLINES: TOPIC → MESSAGE")
T(s, X0, 108, 150, 12, "AVOID", 8.5, True, ORANGE, spc=1); T(s, 205, 108, 310, 12, "USE", 8.5, True, BROWN, spc=1)
ex = [("Market Overview", "Medium and Heavy cranes are 41% of units but 64% of import value"),
      ("Price Comparison", "F.lli Ferrari is cheaper head to head in five tm classes"),
      ("Monitoring", "Regular plant follow-up keeps each PO on its agreed RFD date"),
      ("Work Challenges", "Last-minute quote requests are the main risk to lead time")]
for i, (a, b) in enumerate(ex):
    y = 126 + i * 44
    R(s, X0, y, 150, 36, TINT); T(s, X0 + 8, y, 136, 36, a, 9.5, True, MUTED, anchor="m")
    T(s, 165, y, 30, 36, "→", 14, True, ORANGE, "c", "m")
    R(s, 205, y, 310, 36, WASH, BORDER, 0.5); T(s, 213, y, 296, 36, b, 9.5, True, INK, anchor="m", line=1.05)
label(s, X0, 312, 470, "2 · TEXT RULES")
for i, t in enumerate(["Max 6 bullets per box, ideally one line each; no full stops on fragments.",
                       "Max ~40 words per box. If more is needed, it belongs in the appendix.",
                       "Define an abbreviation once: Request for Delivery (RFD).",
                       "One language per deck (English); keep product and form names as in the system.",
                       "Names: full name + role on first mention, short name after."]):
    y = 338 + i * 32
    R(s, X0, y + 4, 6, 6, ORANGE, shape="oval")
    T(s, X0 + 16, y, 455, 28, t, 9.5, False, INK, line=1.1)
label(s, 545, 84, 370, "3 · NUMBER FORMATS")
fm = [("Currency, table", "Rp 1.240.000.000"), ("Currency, text", "Rp 1,24 M · Rp 650 jt"), ("Unit / capacity", "25–35 tm · 30,4 tm"),
      ("Count", "31 units · 1 unit"), ("Percent", "41% · +23% · −14%"), ("Date", "14 Aug 2026"), ("Period", "Jan 2023 – Aug 2026"),
      ("Quarter / month", "Q3 2026 · Oct 2026"), ("Estimate", "7441C* — *estimate, note it")]
for i, (k_, v) in enumerate(fm):
    y = 110 + i * 33
    T(s, 545, y + 6, 150, 14, k_, 9, True, MUTED)
    T(s, 700, y + 4, 215, 18, v, 11, True, INK)
    R(s, 545, y + 28, 370, 0.75, RULE)
R(s, 545, 412, 370, 88, TINT)
T(s, 557, 422, 346, 12, "NOTE", 8.5, True, ORANGE)
T(s, 557, 438, 346, 58, "Use the en dash (–) for ranges and the minus sign (−) for drops. Round only in text; tables keep the full figure so totals add up.",
  9, False, INK, line=1.12)
slides.append(s)

# ======================================================================= 0.14 checklist
s = new_slide("0.14", "DESIGN GUIDANCE — PRE-SEND CHECKLIST", "Fifteen checks before the deck goes to the reviewers")
groups = [("STORY", ["Subtitles alone tell the 6-month story", "One message per slide", "Agenda matches the section dividers", "Last slide states the ask / next step", "Appendix holds the detail, not the main deck"]),
          ("DESIGN", ["Every content slide uses '8_Custom Layout'", "Arial only; sizes from the type scale", "Colours only from the palette", "Body stays inside x 45–915, y 75–505 pt", "Photos sharp, cropped, not stretched"]),
          ("DATA", ["Every chart and table has a source line", "Numbers match between slides and appendix", "Formats follow the number rules", "Charts and tables are native, not pictures", "Spelling and names checked"])]
for gi, (g, its) in enumerate(groups):
    x = X0 + gi * 294
    label(s, x, 84, 282, f"{gi + 1} · {g}")
    for i, t in enumerate(its):
        y = 112 + i * 40
        R(s, x, y + 2, 13, 13, WHITE, BROWN, 1)
        T(s, x + 22, y, 255, 32, t, 9.5, False, INK, line=1.1)
        R(s, x, y + 34, 282, 0.75, RULE)
label(s, X0, 330, X1 - X0, "4 · FILE NAMING & VERSIONS")
R(s, X0, 356, X1 - X0, 44, WASH, BORDER, 0.5)
T(s, X0 + 14, 356, 840, 44, [[("NEDP_6M_Review_", {"color": INK}), ("TiberiasSimu", {"color": ORANGE}), ("_v03", {"color": BROWN}), ("_2026-10-13", {"color": SAND}), (".pptx", {"color": MUTED})]],
  15, True, INK, anchor="m")
for i, (h, b) in enumerate([("Program + topic", "Same prefix for every file of the review"), ("Owner", "Who presents the deck"),
                            ("Version", "v01, v02 … raise it on every sent copy"), ("Date", "ISO date, so files sort by time")]):
    x = X0 + i * 220
    T(s, x, 410, 208, 14, h, 9.5, True, BROWN); T(s, x, 426, 208, 28, b, 8.5, False, MUTED, line=1.1)
R(s, X0, 460, X1 - X0, 40, BROWN)
T(s, X0 + 14, 460, 840, 40, [[("KEY TAKEAWAY  ", {"color": PEACH, "size": 8.5}), ("Send a PDF to read and the PPTX to edit; keep the PPTX file version on the cover up to date.", {})]],
  11, True, WHITE, anchor="m")
slides.append(s)

# ======================================================================= reuse template slides
for sh in PALETTE.shapes:
    if sh.has_text_frame:
        t = sh.text_frame.text
        if t == "0.1": set_text(sh, "0.5")
        elif t.startswith("STYLE GUIDE"): set_text(sh, "DESIGN GUIDANCE — COLOUR PALETTE & BOXES")
        elif t.startswith("Colour palette and shapes"): set_text(sh, "Eleven colours and six box types — copy from here when building new slides")
for sh in TIMEFRAME.shapes:
    if sh.has_text_frame:
        t = sh.text_frame.text
        if t == "0.2": set_text(sh, "0.9")
        elif t.startswith("STYLE GUIDE"): set_text(sh, "DESIGN GUIDANCE — TIMEFRAME TEMPLATE")
        elif t.startswith("General timeframe"): set_text(sh, "Plans and milestones in one native table — copy, then rename periods, rows and bars")
for sl in (PALETTE, TIMEFRAME):
    sl._element.attrib.pop("show", None)

# cover + closing text
for sh in COVER.shapes:
    if not sh.has_text_frame: continue
    t = sh.text_frame.text
    if t == "[TITLE]": set_text(sh, "DESIGN GUIDANCE")
    elif t.startswith("Prepared for"):
        tf = sh.text_frame; tf.paragraphs[1].runs[0].text = "NEDP 6-Month Review 2026 — slide standard"
        for r in tf.paragraphs[1].runs[1:]: r.text = ""
    elif t.startswith("[date]"):
        tf = sh.text_frame; tf.paragraphs[0].runs[0].text = "13 October 2026"
        for r in tf.paragraphs[0].runs[1:]: r.text = ""
        para = tf.paragraphs[1]; para.runs[0].text = "File version: 13.10.2026"
        for r in para.runs[1:]: r.text = ""
for sh in THANKS.slide_layout.shapes:
    if sh.has_text_frame and "Prepared by" in sh.text_frame.text:
        lines = ["Prepared by:", "Tiberias K. Simu – Marketing Strategic 2 Associate", "Department of Strategic Marketing 2",
                 "Marketing Unit & Strategic Division"]
        paras = [pp for pp in sh.text_frame.paragraphs if pp.runs]
        for i, para in enumerate(paras[:4]):
            para.runs[0].text = lines[i]
            for r in para.runs[1:]: r.text = ""
# footer page number box: wide enough for two digits
for lay in p.slide_layouts:
    for sh in lay.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith("Page") and sh.width < Pt(70):
            sh.left = sh.left - Pt(20); sh.width = sh.width + Pt(20); sh.text_frame.word_wrap = False

# ======================================================================= order + cleanup
lst = p.slides._sldIdLst
new = [COVER] + slides[:4] + [PALETTE] + slides[4:7] + [TIMEFRAME] + slides[7:] + [THANKS]
sid = {id(sl): sl.slide_id for sl in list(p.slides)}
els = {int(e.get("id")): e for e in lst}
for sl in (BLANK, APPX):
    el = els[sid[id(sl)]]
    p.part.drop_rel(el.get(qn("r:id"))); lst.remove(el)
for e in list(lst): lst.remove(e)
for sl in new: lst.append(els[sid[id(sl)]])
p.save(OUT)
print("saved", OUT, len(new), "slides")
