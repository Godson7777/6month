"""Design Guidance in the style of the Bitwise Asset Management website, for the NEDP 6-month review deck.
Tokens taken from the Bitwise page source (fonts, slate + brand scales, spacing, radii, shadows).
Everything is a native, editable PowerPoint object.  Run from nedp_deck/:  python3 design_guide/build_bitwise_guide.py"""
import io
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt

OUT = "design_guide/NEDP_6M_Design_Guidance_Bitwise.pptx"
A = "assets/"
SERIF, SANS = "Georgia", "Arial"          # stand-ins for Bitwise "Items" (serif) and "Neue Montreal" (sans)

# ---- Bitwise tokens (hsl values from the site converted to hex) ----
SL = {1: "FCFCFD", 2: "F9FAFB", 3: "F0F2F4", 4: "EBEDEF", 5: "E6E8EB", 6: "E0E3E6", 7: "D7DBDF", 8: "C1C8CD",
      9: "889096", 10: "7D868C", 11: "697177", 12: "4D555C", 13: "252D31", 14: "1C262C", 15: "11181C", 16: "020304"}
BR = {100: "E5FFF1", 200: "E1F9EC", 300: "83E7AE", 400: "39DB7F", 500: "22C96A", 600: "0DA54F", 800: "076932"}
ACC = {"amber": "FFC53D", "red": "E5484D", "blue": "0090FF", "purple": "8E4EC6", "orange": "E55200"}
INK, BODY, MUTE, LINE, WASH, WHITE = SL[15], SL[12], SL[11], SL[6], SL[2], "FFFFFF"
GREEN, GREEN_D = BR[500], BR[800]
W, H = 960, 540
X0, X1 = 48, 912

p = Presentation(); p.slide_width = Pt(W); p.slide_height = Pt(H)
BL = p.slide_layouts[6]
TOTAL = [0]


def rgb(h): return RGBColor.from_string(h)


def T(s, x, y, w, h, text, size=11, font=SANS, bold=False, color=BODY, align="l", anchor="t", spc=0, line=None, italic=False, wrap=True):
    """Text box. text = str | list of paragraphs; paragraph = str | list of (text, opts) runs.
    opts: size, font, bold, color, i (italic), spc (tracking pt)."""
    tb = s.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    for i, para in enumerate(text if isinstance(text, list) else [text]):
        pp = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        pp.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        if line: pp.line_spacing = line
        for t, o in (para if isinstance(para, list) else [(para, {})]):
            r = pp.add_run(); r.text = t; f = r.font
            f.name = o.get("font", font); f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold)
            f.italic = o.get("i", italic); f.color.rgb = rgb(o.get("color", color))
            sp = o.get("spc", spc)
            if sp: r._r.get_or_add_rPr().set("spc", str(int(sp * 100)))
    return tb


def shadow(sh, blur=16, dist=6, alpha=7):
    spPr = sh._element.spPr
    eff = etree.SubElement(spPr, qn("a:effectLst"))
    o = etree.SubElement(eff, qn("a:outerShdw"), blurRad=str(int(Pt(blur))), dist=str(int(Pt(dist))), dir="5400000", algn="t", rotWithShape="0")
    c = etree.SubElement(o, qn("a:srgbClr"), val=SL[15]); etree.SubElement(c, qn("a:alpha"), val=str(alpha * 1000))


def R(s, x, y, w, h, fill=None, line=None, lw=0.75, shape="rect", radius=None, dash=False, shd=False, grad=None):
    if isinstance(lw, str):                      # R(.., fill, line, "round", r) shorthand
        shape, radius, lw = lw, (shape if not isinstance(shape, str) else radius), 0.75
    kind = {"rect": MSO_SHAPE.RECTANGLE, "round": MSO_SHAPE.ROUNDED_RECTANGLE, "oval": MSO_SHAPE.OVAL,
            "chev": MSO_SHAPE.CHEVRON, "pent": MSO_SHAPE.PENTAGON}[shape]
    sh = s.shapes.add_shape(kind, Pt(x), Pt(y), Pt(w), Pt(h))
    if shape == "round": sh.adjustments[0] = (radius or 8) / min(w, h)
    if grad:
        sh.fill.gradient(); sh.fill.gradient_angle = grad[2]
        st = sh.fill.gradient_stops; st[0].color.rgb = rgb(grad[0]); st[0].position = 0; st[1].color.rgb = rgb(grad[1]); st[1].position = 1
    elif fill: sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    else: sh.fill.background()
    if line:
        sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
        if dash: sh.line.dash_style = MSO_LINE.DASH
    else: sh.line.fill.background()
    if shd: shadow(sh)
    else: sh.shadow.inherit = False
    return sh


def L(s, x1, y1, x2, y2, color=LINE, w=0.75):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Pt(x1), Pt(y1), Pt(x2), Pt(y2))
    c.line.color.rgb = rgb(color); c.line.width = Pt(w); return c


def kicker(s, x, y, w, text, color=MUTE, align="l", size=8.5):
    T(s, x, y, w, 12, text.upper(), size, SANS, True, color, align, spc=1.5)


def button(s, x, y, text, kind="primary", w=None, h=24):
    w = w or (len(text) * 6.2 + 30)
    fill, line, tc = {"primary": (GREEN, None, WHITE), "dark": (SL[14], None, SL[1]), "outline": (None, GREEN, GREEN),
                      "ghost": (None, SL[7], SL[15]), "white": (WHITE, None, SL[15])}[kind]
    R(s, x, y, w, h, fill, line, 1, "round", 3)
    T(s, x, y, w, h, text.upper(), 7.5, SANS, True, tc, "c", "m", spc=0.6)
    return w


def link(s, x, y, text, color=GREEN):
    T(s, x, y, 200, 12, [[(text.upper() + "  →", {})]], 7.5, SANS, True, color, spc=0.6)


def logo(s, x, y, h=20, white=False):
    path = A + "cutout/triatra_logo.png"
    im = Image.open(path).convert("RGBA")
    if white:
        a = im.getchannel("A"); im = Image.new("RGBA", im.size, (255, 255, 255, 255)); im.putalpha(a)
    b = io.BytesIO(); im.save(b, "PNG"); b.seek(0)
    s.shapes.add_picture(b, Pt(x), Pt(y), height=Pt(h))


def picture(s, path, x, y, w, h):
    im = Image.open(path)
    if im.mode not in ("RGB", "RGBA"): im = im.convert("RGBA")
    b = io.BytesIO(); im.save(b, "PNG" if im.mode == "RGBA" else "JPEG", quality=92); b.seek(0)
    pic = s.shapes.add_picture(b, Pt(x), Pt(y), Pt(w), Pt(h))
    iw, ih = im.size; t = w / h
    if iw / ih > t: e = (1 - t * ih / iw) / 2; pic.crop_left = pic.crop_right = e
    else: e = (1 - (iw / t) / ih) / 2; pic.crop_top = pic.crop_bottom = e
    return pic


def round_pic(pic, r=8):
    """Give a picture rounded corners (roundRect geometry)."""
    sp = pic._element.spPr; g = sp.find(qn("a:prstGeom")); g.set("prst", "roundRect")
    av = g.find(qn("a:avLst")); av.clear()
    etree.SubElement(av, qn("a:gd"), name="adj", fmla=f"val {int(r / min(pic.width / 12700, pic.height / 12700) * 100000)}")


def page(kick, head, lede=None, dark=False, section="Design Guidance"):
    """Light content page in the Bitwise style: utility bar, kicker, serif headline with italic emphasis, lede, footer."""
    s = p.slides.add_slide(BL); TOTAL[0] += 1; n = TOTAL[0]
    bg = SL[15] if dark else WHITE
    R(s, 0, 0, W, H, bg)
    logo(s, X0, 22, 18, white=False)
    T(s, 560, 26, X1 - 560, 12, [[("NEDP 6-MONTH REVIEW", {"color": SL[1] if dark else INK}), ("     ·     ", {"color": MUTE}),
                                   (section.upper(), {"color": MUTE})]], 7, SANS, True, INK, "r", spc=0.6)
    L(s, X0, 50, X1, 50, SL[13] if dark else SL[5], 0.75)
    if head is None:
        footer(s, n, dark); return s
    kicker(s, X0, 68, 600, kick, MUTE)
    T(s, X0, 84, X1 - X0, 40, head if isinstance(head, list) else [[(head, {})]], 24, SERIF, False, WHITE if dark else INK)
    if lede: T(s, X0, 122, 640, 30, lede, 10.5, SANS, False, SL[8] if dark else BODY, line=1.3)
    footer(s, n, dark)
    return s


def footer(s, n, dark=False):
    L(s, X0, 512, X1, 512, SL[13] if dark else SL[5], 0.75)
    T(s, X0, 518, 400, 10, "NEDP MID YEAR REVIEW 2026  ·  DESIGN GUIDANCE", 6.5, SANS, True, MUTE, spc=0.8)
    T(s, X1 - 60, 518, 60, 10, f"{n:02d}", 6.5, SANS, True, INK if not dark else SL[1], "r", spc=0.8)


def em(*parts):
    """Headline helper: plain strings and ('word', True) for the italic emphasis Bitwise uses."""
    return [[(t, {"i": True}) if isinstance(t, tuple) else (t, {}) for t in [x[0] if isinstance(x, tuple) else x for x in parts]]] \
        if False else [[((x[0]), {"i": True}) if isinstance(x, tuple) else (x, {}) for x in parts]]


# ============================================================ 01 cover (dark hero)
s = p.slides.add_slide(BL); TOTAL[0] += 1
R(s, 0, 0, W, H, grad=(SL[15], "23343C", 45))
logo(s, X0, 30, 22)
T(s, 560, 36, X1 - 560, 12, [[("DESIGN GUIDANCE", {"color": SL[1]}), ("     ·     ", {"color": SL[11]}), ("V1 · 13 OCT 2026", {"color": SL[9]})]], 7, SANS, True, SL[1], "r", spc=0.6)
kicker(s, X0, 170, 500, "NEDP 6-month review · slide standard", BR[300])
T(s, X0, 190, 640, 110, [[("A calm, ", {}), ("clear", {"i": True}), (" standard for the six-month review.", {})]], 38, SERIF, False, WHITE, line=1.05)
T(s, X0, 300, 470, 40, "A design guidance that brings the calm, editorial style of the Bitwise website to every slide of the review deck: serif headlines, quiet neutrals, one confident green.",
  10.5, SANS, False, SL[8], line=1.4)
bx = button(s, X0, 360, "Start here", "primary", 110)
button(s, X0 + bx + 10, 360, "See components", "outline", 130)
c = R(s, 640, 430, 272, 56, WHITE, None, shape="round", radius=6, shd=True)
T(s, 656, 440, 230, 10, "NOW IN USE", 6.5, SANS, True, BODY, spc=0.8)
T(s, 656, 455, 230, 18, [[("NEDP6M", {"bold": True, "color": INK}), ("   Tiberias K. Simu · Review deck", {"color": INK})]], 9.5, SANS)
T(s, 880, 450, 20, 18, "→", 12, SANS, False, INK)
T(s, X0, 500, 400, 10, "PT TRIATRA SINERGIA PRATAMA  ·  MARKETING UNIT & STRATEGIC DIVISION", 6.5, SANS, True, SL[9], spc=0.8)

# ============================================================ 02 contents
s = page("Contents", em("Everything you need, ", ("in one place", True), "."), "Four parts, read top to bottom the first time; afterwards jump straight to the page you need.")
cols = [("Foundations", ["Design DNA", "Typefaces", "Type scale", "Type details", "Neutral colours", "Brand & accent colours", "Colour in use", "Space, radius, elevation", "Grid"]),
        ("Components", ["Slide anatomy", "Buttons, links, tags", "Cards", "Section patterns", "Charts", "Tables", "Imagery"]),
        ("Layouts", ["Page types", "Dark sections", "Applied example"]),
        ("Application", ["Writing & voice", "Numbers & formats", "Draft → final workflow", "Pre-send checklist"])]
n = 3
for ci, (h, items) in enumerate(cols):
    x = X0 + ci * 216
    kicker(s, x, 176, 200, h)
    L(s, x, 192, x + 200, 192, SL[5])
    for j, it in enumerate(items):
        T(s, x, 202 + j * 31, 30, 14, f"{n:02d}", 9, SANS, True, GREEN)
        T(s, x + 28, 201 + j * 31, 170, 16, it, 11, SERIF, False, INK)
        L(s, x, 223 + j * 31, x + 200, 223 + j * 31, SL[4]); n += 1

# ============================================================ 03 design DNA (why columns)
s = page("Why this style", em("Professional slides, ", ("managed", True), " like a fund."),
         "Bitwise explains a complicated market to cautious investors. A 6-month review has the same job: explain a lot of work to busy reviewers, clearly.")
L(s, X0 - 20, 248, X1 + 20, 238, SL[5], 1)
dna = [("Editorial serif headlines", "Headlines are set in a light serif with one phrase in italic. It reads like a research note, not a sales pitch."),
       ("Quiet neutrals, one green", "Almost everything is slate grey on white. Green is used only for actions, highlights and the focus series in a chart."),
       ("Space does the work", "Large margins, one idea per block and centred section intros. Nothing is boxed unless it must be grouped.")]
for i, (h, b) in enumerate(dna):
    x = X0 + i * 300
    T(s, x, 210, 270, 18, h, 13, SERIF, False, INK)
    y = 247 - i * 4.6
    R(s, x, y - 3, 6, 6, GREEN, shape="oval")
    T(s, x, 266, 260, 70, b, 10, SANS, False, BODY, line=1.45)
R(s, X0, 360, X1 - X0, 132, WASH, shape="round", radius=12)
kicker(s, X0, 380, X1 - X0, "The style in three words", MUTE, "c")
T(s, X0, 398, X1 - X0, 40, [[("Calm. ", {}), ("Clear.", {"i": True}), (" Credible.", {})]], 26, SERIF, False, INK, "c")
button(s, W / 2 - 60, 448, "Read the rules", "primary", 120)

# ============================================================ 04 typefaces
s = page("Foundations · Typefaces", em("Two families: a ", ("serif", True), " to speak, a sans to explain."),
         "Bitwise pairs the serif 'Items' with the grotesk 'Neue Montreal'. Both are licensed web fonts, so the deck uses the closest fonts every Office computer already has.")
for i, (fam, sub, role, src, sample_font, weights, it) in enumerate([
        ("Georgia", "Headlines, card titles, big numbers", "Replaces Bitwise 'Items' (serif, weight 350–500)", "Regular + Italic only. Never bold.", SERIF, "Regular 400 · Italic 400", True),
        ("Arial", "Kickers, body, labels, buttons, tables", "Replaces Bitwise 'Neue Montreal' (sans, 400 / 550 / 650)", "Regular for text, Bold for kickers, labels, buttons.", SANS, "Regular 400 · Bold 700", False)]):
    x = X0 + i * 438
    R(s, x, 168, 426, 300, WHITE, SL[5], 0.75, "round", 10)
    T(s, x + 24, 186, 200, 90, "Aa", 66, sample_font, False, INK)
    T(s, x + 200, 196, 210, 22, fam, 18, sample_font, False, INK)
    T(s, x + 200, 222, 210, 30, sub, 9.5, SANS, False, BODY, line=1.3)
    kicker(s, x + 24, 290, 380, "Role")
    T(s, x + 24, 306, 380, 14, role, 10, SANS, False, INK)
    kicker(s, x + 24, 332, 380, "Weights")
    T(s, x + 24, 348, 380, 14, weights, 10, SANS, False, INK)
    kicker(s, x + 24, 374, 380, "Rule")
    T(s, x + 24, 390, 380, 14, src, 10, SANS, False, INK)
    T(s, x + 24, 420, 380, 40, "ABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz 0123456789 Rp % –", 9, sample_font, False, MUTE, italic=it)
T(s, X0, 478, X1 - X0, 28, [[("If fonts may be installed:  ", {"bold": True, "color": INK}),
                              ("'Newsreader Light' or 'Fraunces' come closest to Items, and 'Inter' or 'Manrope' to Neue Montreal (all free, Google Fonts). Embed them when saving (File › Options › Save › Embed fonts).", {})]],
  8.5, SANS, False, BODY, line=1.3)

# ============================================================ 05 type scale
s = page("Foundations · Type scale", em("Nine sizes, ", ("no more", True), "."), "Sizes are set for a 13.33 × 7.5 in slide. Web values from Bitwise are shown for reference (16 px ≈ 11 pt on a slide).")
hdr = ["STYLE", "SAMPLE", "FONT · SIZE · WEIGHT", "TRACKING · LEADING", "WEB REF"]
xs = [X0, 170, 520, 690, 820]
for x, t in zip(xs, hdr): T(s, x, 170, 160, 10, t, 7, SANS, True, MUTE, spc=1)
L(s, X0, 184, X1, 184, SL[13], 1)
rows = [("Display", [("Clear by ", {}), ("design", {"i": True})], SERIF, 36, False, INK, "Georgia 36 Regular", "-0.5 · 1.0", "48–64 px"),
        ("H1 · slide title", [("Professional funds", {})], SERIF, 24, False, INK, "Georgia 24 Regular", "0 · 1.1", "32 px"),
        ("H2 · section", [("Why the price ", {}), ("wins", {"i": True})], SERIF, 18, False, INK, "Georgia 18 Regular", "0 · 1.2", "24 px"),
        ("H3 · card title", [("Crypto Market Review", {})], SERIF, 13, False, INK, "Georgia 13 Regular", "0.2 · 1.25", "16 px Items"),
        ("Kicker", [("WHY BITWISE", {"spc": 1.5})], SANS, 8.5, True, MUTE, "Arial 8.5 Bold CAPS", "+1.5 · 1.0", "16 px 550 +2"),
        ("Lede", [("One sentence that frames the slide.", {})], SANS, 10.5, False, BODY, "Arial 10.5 Regular", "0 · 1.3", "18 px"),
        ("Body", [("Short paragraphs, slate 12.", {})], SANS, 10, False, BODY, "Arial 10 Regular", "0 · 1.45", "16 px 400"),
        ("Meta · label", [("Research  •  Oct 8, 2026", {})], SANS, 8.5, True, BODY, "Arial 8.5 Bold", "0 · 1.2", "14 px 550"),
        ("Button · source", [("VIEW ALL", {"spc": 0.6})], SANS, 7.5, True, GREEN, "Arial 7.5 Bold CAPS", "+0.6 · 1.0", "12 px 550 +0.8")]
y = 192
for name, sample, f, sz, b, c, spec, trk, web in rows:
    h = max(26, sz * 1.25)
    T(s, xs[0], y + (h - 12) / 2, 120, 12, name, 9, SANS, True, INK)
    T(s, xs[1], y, 340, h, [sample], sz, f, b, c, anchor="m")
    T(s, xs[2], y + (h - 12) / 2, 165, 12, spec, 8.5, SANS, False, BODY)
    T(s, xs[3], y + (h - 12) / 2, 125, 12, trk, 8.5, SANS, False, BODY)
    T(s, xs[4], y + (h - 12) / 2, 92, 12, web, 8.5, SANS, False, MUTE)
    L(s, X0, y + h + 3, X1, y + h + 3, SL[4])
    y += h + 6

# ============================================================ 06 type details
s = page("Foundations · Type details", em("Small rules that make it ", ("feel", True), " like Bitwise."))
rules = [("Italic, not bold, for emphasis", [("Crypto is ", {}), ("complicated", {"i": True}), (". We make it ", {}), ("clear", {"i": True}), (".", {})],
          "In serif headlines, put the one idea that matters in italic. Never bold a serif."),
         ("Sentence case headlines", [("Professional funds managed by experts", {})], "Capitalise only the first word and names. CAPS are only for kickers, labels and buttons."),
         ("Tracked caps for kickers", [("INVESTMENTS", {"font": SANS, "size": 10, "bold": True, "spc": 1.5, "color": MUTE})],
          "Kickers sit 12–16 pt above the headline, slate 11, tracking +1.5 pt."),
         ("Short lines", [("Max ~70 characters per line", {})], "Body text never spans the full slide. Cap paragraphs at 2/3 of the width."),
         ("Leading", [("1.0 · 1.25 · 1.45", {})], "Headlines 1.0–1.1, card titles 1.25, body 1.45 (Bitwise: 1, 1.25, 1.5)."),
         ("Numbers in serif", [("67", {"size": 26}), ("  units / year", {"font": SANS, "size": 9, "color": BODY})], "Key figures use Georgia, ink colour; the unit follows in small sans.")]
for i, (h, sample, b) in enumerate(rules):
    x = X0 + (i % 3) * 292; y = 150 + (i // 3) * 176
    R(s, x, y, 280, 164, WASH, shape="round", radius=10)
    kicker(s, x + 18, y + 16, 250, h, INK)
    T(s, x + 18, y + 40, 250, 56, [sample], 17, SERIF, False, INK, anchor="m")
    L(s, x + 18, y + 102, x + 262, y + 102, SL[6])
    T(s, x + 18, y + 110, 248, 50, b, 9, SANS, False, BODY, line=1.35)

# ============================================================ 07 neutrals
s = page("Foundations · Neutral colours", em("Sixteen greys carry ", ("almost everything", True), "."),
         "The Bitwise 'slate' scale: a cool, slightly blue grey. Light steps for surfaces and lines, dark steps for text and dark sections.")
roles = {1: "Page alt", 2: "Wash / section", 3: "Card hover", 4: "Hairline", 5: "Divider", 6: "Border", 7: "Border strong", 8: "Disabled",
         9: "Placeholder", 10: "Icon", 11: "Kicker · muted", 12: "Body text", 13: "Ink soft", 14: "Dark button", 15: "Ink · dark section", 16: "Black"}
sw = (X1 - X0 - 7 * 8) / 8
for i in range(16):
    k = i + 1; x = X0 + (i % 8) * (sw + 8); y = 172 + (i // 8) * 150
    R(s, x, y, sw, 70, SL[k], SL[6] if k < 5 else None, 0.5, "round", 6)
    T(s, x, y + 78, sw, 12, f"Slate {k}", 9, SANS, True, INK)
    T(s, x, y + 92, sw, 12, f"#{SL[k]}", 8.5, SANS, False, BODY)
    T(s, x, y + 106, sw, 24, roles[k], 8.5, SANS, False, MUTE, line=1.1)

# ============================================================ 08 brand + accents
s = page("Foundations · Brand & accent colours", em("One ", ("confident", True), " green, used sparingly."),
         "Bitwise green (hue 146°) marks actions and the focus of a chart. Accents come from the same Radix-style scales and are reserved for status and extra chart series.")
kicker(s, X0, 166, 400, "Brand green scale")
bw_ = (X1 - X0 - 6 * 8) / 7
for i, (k, v) in enumerate(BR.items()):
    x = X0 + i * (bw_ + 8)
    R(s, x, 184, bw_, 58, v, None, shape="round", radius=6)
    T(s, x, 248, bw_, 12, f"Green {k}", 9, SANS, True, INK)
    T(s, x, 261, bw_, 12, f"#{v}", 8.5, SANS, False, BODY)
T(s, X0, 280, X1 - X0, 14, [[("Green 500 ", {"bold": True, "color": INK}), ("primary button, highlight, focus series   ·   ", {}),
                              ("Green 800 ", {"bold": True, "color": INK}), ("hover, green text on white   ·   ", {}),
                              ("Green 100–200 ", {"bold": True, "color": INK}), ("tinted note background", {})]], 8.5, SANS, False, BODY)
kicker(s, X0, 316, 400, "Accents · status & chart series")
acc = [("amber", "Warning · on going"), ("red", "Risk · price higher"), ("blue", "Second series · info"), ("purple", "Third series"), ("orange", "Triatra logo only")]
for i, (k, t) in enumerate(acc):
    x = X0 + i * 176
    R(s, x, 334, 30, 30, ACC[k], shape="oval")
    T(s, x + 40, 336, 130, 12, f"{k.capitalize()}  #{ACC[k]}", 9, SANS, True, INK)
    T(s, x + 40, 350, 130, 12, t, 8.5, SANS, False, BODY)
R(s, X0, 392, X1 - X0, 100, BR[100], None, shape="round", radius=10)
kicker(s, X0 + 20, 408, 400, "Brand bridge · Triatra", GREEN_D)
T(s, X0 + 20, 426, 820, 60, "The Triatra logo stays in its own orange and is never recoloured. Orange is not used anywhere else in the deck, so the logo and the green never compete. If the reviewers require Triatra orange as the accent, swap Green 500 → #E55200 and Green 800 → #80350E everywhere; every other rule stays the same.",
  9.5, SANS, False, SL[13], line=1.4)

# ============================================================ 09 colour in use
s = page("Foundations · Colour in use", em("Mostly white, slate text, ", ("a touch", True), " of green."))
kicker(s, X0, 150, 400, "Proportion on a light slide")
x = X0
for pct, f, txt, tc in [(70, WHITE, "70%  White / Slate 1–2", BODY), (22, SL[12], "22%  Slate 11–15 text", WHITE), (6, SL[6], "6%", BODY), (2, GREEN, "", WHITE)]:
    w = (X1 - X0) * pct / 100
    R(s, x, 168, w, 30, f, SL[6] if f == WHITE else None, 0.75); T(s, x + 8, 168, w - 8, 30, txt, 8.5, SANS, True, tc, anchor="m"); x += w
T(s, X0, 204, X1 - X0, 12, "Lines and borders 6%  ·  green 2%: one button, one highlight or one focus series per slide.", 8.5, SANS, False, MUTE)
kicker(s, X0, 236, 400, "Light and dark sections")
R(s, X0, 254, 420, 110, WHITE, SL[6], 0.75, "round", 10)
kicker(s, X0 + 20, 270, 300, "Light · default"); T(s, X0 + 20, 286, 380, 26, [[("Most slides are ", {}), ("light", {"i": True}), (".", {})]], 17, SERIF, False, INK)
T(s, X0 + 20, 314, 380, 20, "White background, Slate 15 headline, Slate 12 body.", 9, SANS, False, BODY); button(s, X0 + 20, 334, "Primary", "primary", 70)
R(s, 492, 254, 420, 110, grad=(SL[15], "23343C", 45), shape="round", radius=10)
kicker(s, 512, 270, 300, "Dark · cover, dividers, closing", SL[9]); T(s, 512, 286, 380, 26, [[("Use dark ", {}), ("rarely", {"i": True}), (".", {})]], 17, SERIF, False, WHITE)
T(s, 512, 314, 380, 20, "Slate 15 → #23343C gradient, white headline, Slate 8 body.", 9, SANS, False, SL[8]); button(s, 512, 334, "Outline", "outline", 70)
kicker(s, X0, 384, 400, "Do and don't")
dd = [(True, "Green only on the action or the focus"), (False, "Green headlines, green boxes, green everything"),
      (True, "Accents only to mean something (risk, warning)"), (False, "Rainbow categories in one chart")]
for i, (ok, t) in enumerate(dd):
    x = X0 + i * 216
    R(s, x, 402, 204, 90, BR[100] if ok else "FFF7F7", None, shape="round", radius=8)
    T(s, x + 14, 414, 180, 12, "DO" if ok else "DON'T", 8, SANS, True, GREEN_D if ok else ACC["red"], spc=1)
    T(s, x + 14, 432, 176, 54, t, 10.5, SERIF, False, INK, line=1.2)

# ============================================================ 10 space radius elevation
s = page("Foundations · Space, radius, elevation", em("A ", ("4-point", True), " system, soft corners, barely-there shadows."))
kicker(s, X0, 150, 400, "Spacing scale (Bitwise space-1 … space-15, in pt)")
for i, v in enumerate([4, 8, 12, 16, 24, 32, 48, 64, 80]):
    x = X0 + i * 96
    R(s, x, 168 + (80 - v) * 0.6, v * 0.6 + 2, v * 0.6 + 2, GREEN if v in (16, 48) else SL[8], shape="rect")
    T(s, x, 222, 90, 12, f"{v} pt", 10, SERIF, False, INK)
    T(s, x, 236, 90, 24, ["inside chip", "icon ↔ text", "gutter", "card padding", "block gap", "title ↔ body", "section gap", "slide margin top", "hero padding"][i], 8, SANS, False, MUTE, line=1.1)
kicker(s, X0, 280, 400, "Corner radius")
for i, (r, t) in enumerate([(0, "0 · tables, photos in grids"), (3, "3 pt · buttons, chips"), (6, "6 pt · inputs, small cards"), (10, "10 pt · cards, panels"), (20, "20 pt · large hero panels")]):
    x = X0 + i * 174
    R(s, x, 298, 120, 64, WASH, SL[6], 0.75, "round" if r else "rect", max(r, 0.1))
    T(s, x, 368, 160, 24, t, 8.5, SANS, False, BODY)
kicker(s, X0, 404, 400, "Elevation")
for i, (t, d) in enumerate([("Flat + hairline", "Default card: white, Slate 6 border 0.75 pt"), ("Card shadow", "Floating callout on photos or dark hero"), ("Wash panel", "Slate 2 fill, no border, groups a section")]):
    x = X0 + i * 290
    sh = R(s, x, 422, 270, 66, WHITE if i < 2 else WASH, SL[6] if i == 0 else None, 0.75, "round", 10, shd=(i == 1))
    T(s, x + 16, 434, 240, 14, t, 12, SERIF, False, INK); T(s, x + 16, 454, 240, 24, d, 8.5, SANS, False, BODY)

# ============================================================ 11 grid
s = page("Foundations · Grid", em("Twelve columns, ", ("wide", True), " margins."),
         "Margins 48 pt left and right, 16 pt gutters. Section intros are centred; content is left-aligned on the grid.")
cw = (X1 - X0 - 11 * 16) / 12
for i in range(12):
    x = X0 + i * (cw + 16); R(s, x, 166, cw, 90, BR[100]); T(s, x, 166, cw, 90, str(i + 1), 12, SERIF, False, GREEN_D, "c", "m")
splits = [([12], "Hero, full chart, table"), ([6, 6], "Text + image"), ([4, 4, 4], "Why columns, three cards"),
          ([3, 3, 3, 3], "Stat row, four cards"), ([5, 7], "Lede + evidence"), ([8, 4], "Chart + takeaway")]
for r, (parts, t) in enumerate(splits):
    y = 272 + r * 36; x = X0
    for k in parts:
        w = (k * cw + (k - 1) * 16) * 0.74
        R(s, x, y, w, 26, WASH, SL[6], 0.5, "round", 4); T(s, x, y, w, 26, f"{k}", 9, SANS, True, MUTE, "c", "m")
        x += w + 16 * 0.74
    T(s, X0 + (X1 - X0) * 0.74 + 24, y + 7, 200, 14, t, 9.5, SANS, False, INK)

# ============================================================ 12 anatomy
s = page("Components · Slide anatomy", em("Every content slide, ", ("same frame", True), "."))
fx, fy, fw = X0, 148, 480; k = fw / 960; fh = 540 * k
R(s, fx, fy, fw, fh, WHITE, SL[7], 1)
s.shapes  # mini frame
R(s, fx + 48 * k, fy + 22 * k, 50 * k, 18 * k, "E55200")
T(s, fx + 560 * k, fy + 26 * k, 352 * k, 8, "NEDP 6-MONTH REVIEW · SECTION", 4, SANS, True, INK, "r")
L(s, fx + 48 * k, fy + 50 * k, fx + 912 * k, fy + 50 * k, SL[5], 0.5)
T(s, fx + 48 * k, fy + 66 * k, 300, 8, "KICKER", 4.5, SANS, True, MUTE, spc=0.6)
T(s, fx + 48 * k, fy + 80 * k, 400, 16, [[("Headline with one ", {}), ("italic", {"i": True}), (" idea", {})]], 11, SERIF, False, INK)
T(s, fx + 48 * k, fy + 120 * k, 300, 8, "Lede sentence in slate 12, max two lines.", 5, SANS, False, BODY)
R(s, fx + 48 * k, fy + 150 * k, 864 * k, 350 * k, BR[100], BR[300], 0.75, dash=True)
T(s, fx + 48 * k, fy + 150 * k, 864 * k, 350 * k, ["BODY", "864 × 350 pt"], 8, SANS, True, GREEN_D, "c", "m")
L(s, fx + 48 * k, fy + 512 * k, fx + 912 * k, fy + 512 * k, SL[5], 0.5)
T(s, fx + 48 * k, fy + 516 * k, 200, 6, "FOOTER · DECK NAME", 3.5, SANS, True, MUTE)
marks = [(48 + 75, 31), (912 - 380, 30), (14, 70), (14, 94), (14, 122), (480, 190), (48 + 160, 516)]
for i, (cx, cy) in enumerate(marks, 1):
    R(s, fx + cx * k - 7, fy + cy * k - 7, 14, 14, SL[15], shape="oval"); T(s, fx + cx * k - 7, fy + cy * k - 7, 14, 14, str(i), 7, SANS, True, WHITE, "c", "m")
spec = [("Logo", "Triatra logo, 18 pt high, top-left at 48 / 22 pt."), ("Utility bar", "Deck · section in 7 pt bold caps, right-aligned; hairline at 50 pt."),
        ("Kicker", "Section name, 8.5 pt bold caps, Slate 11, at 68 pt."), ("Headline", "Georgia 24, one italic phrase, sentence case, at 84 pt."),
        ("Lede", "Optional. Arial 10.5, Slate 12, at 122 pt, ≤ 2 lines."), ("Body", "From 150 to 500 pt. Everything sits on the 12-column grid."),
        ("Footer", "Hairline at 512 pt, deck name left, page number right.")]
for i, (h, b) in enumerate(spec):
    y = 150 + i * 49
    R(s, 552, y, 16, 16, SL[15], shape="oval"); T(s, 552, y, 16, 16, str(i + 1), 7.5, SANS, True, WHITE, "c", "m")
    T(s, 578, y, 330, 16, h, 12, SERIF, False, INK); T(s, 578, y + 18, 330, 24, b, 8.5, SANS, False, BODY, line=1.3)
    L(s, 552, y + 42, X1, y + 42, SL[4])

# ============================================================ 13 buttons, links, tags
s = page("Components · Buttons, links, tags", em("Small, ", ("tracked", True), ", and always meaningful."),
         "In a deck, buttons are labels for the next step or the decision you ask for. Keep the Bitwise shapes: 3 pt radius, 7.5 pt bold caps, +0.6 tracking.")
kicker(s, X0, 172, 300, "Buttons")
x = X0
for t, kd, d in [("Invest now", "primary", "Primary · the one action"), ("Create account", "dark", "Dark · neutral action"),
                 ("Learn more", "outline", "Outline · secondary"), ("Log in", "ghost", "Ghost · tertiary")]:
    w = button(s, x, 192, t, kd, 120); T(s, x, 224, 140, 12, d, 8.5, SANS, False, MUTE); x += 160
R(s, x, 184, 180, 50, SL[15], None, "round", 8); button(s, x + 30, 197, "Start investing", "primary", 120)
T(s, x, 240, 180, 12, "On dark: primary or outline", 8.5, SANS, False, MUTE)
kicker(s, X0, 272, 300, "Links")
link(s, X0, 292, "View all"); link(s, X0 + 140, 292, "Read more", INK); T(s, X0 + 280, 290, 300, 14, [[("Inline link in a sentence uses ", {}), ("Green 800", {"color": GREEN_D, "bold": True}), (".", {})]], 9.5, SANS, False, BODY)
kicker(s, X0, 326, 300, "Meta line")
T(s, X0, 344, 400, 14, [[("Research", {"bold": True}), ("  •  Oct 8, 2026", {})]], 9, SANS, False, BODY)
T(s, X0 + 220, 344, 400, 14, [[("Supply chain", {"bold": True}), ("  •  Step 4 of 5  •  Jun 2026", {})]], 9, SANS, False, BODY)
kicker(s, X0, 378, 300, "Status tags")
for i, (t, f, tc) in enumerate([("Done", BR[200], GREEN_D), ("On going", "FFF7C2", "AB6400"), ("At risk", "FEEBEC", "CE2C31"), ("Not started", SL[3], SL[11]), ("New", SL[15], WHITE)]):
    x = X0 + i * 104; R(s, x, 396, 92, 20, f, None, "round", 10); T(s, x, 396, 92, 20, t.upper(), 7, SANS, True, tc, "c", "m", spc=0.6)
R(s, X0, 436, X1 - X0, 56, WASH, None, "round", 10)
T(s, X0 + 20, 436, 820, 56, [[("Rule  ", {"bold": True, "color": INK}), ("Max one primary (green) button per slide. Status tags always use the same four words and colours through the whole deck.", {})]],
  10, SANS, False, BODY, anchor="m")

# ============================================================ 14 cards
s = page("Components · Cards", em("Cards that read like ", ("research notes", True), "."))
imgs = [A + "evidence/sc5_73.webp", A + "project/crane1.png", A + "evidence/s1_a.png"]
for i, (meta, ttl, d, im) in enumerate([("Monitoring  •  Jun 2026", "Plant visit keeps the RFD on track", "Weekly follow-up with UTE production and photo updates to sales.", imgs[0]),
                                        ("Project  •  Aug 2026", "F.lli Ferrari wins on price", "Five cranes beat competitors head to head in their tm class.", imgs[1]),
                                        ("Strategic  •  May 2026", "Pricing & market analysis", "Price simulation and competitor mapping for the sales team.", imgs[2])]):
    x = X0 + i * 220
    pic = picture(s, im, x, 152, 204, 116); round_pic(pic, 8)
    T(s, x, 278, 204, 12, [[(meta.split("  •  ")[0], {"bold": True}), ("  •  " + meta.split("  •  ")[1], {})]], 8.5, SANS, False, BODY)
    T(s, x, 294, 204, 34, ttl, 13, SERIF, False, INK, line=1.15)
    T(s, x, 330, 204, 36, d, 9, SANS, False, BODY, line=1.35)
    link(s, x, 372, "Read more", INK)
T(s, X0, 396, 650, 12, "INSIGHT CARD  ·  image 8 pt radius  ·  meta  ·  serif title  ·  one-line description  ·  link", 7, SANS, True, MUTE, spc=0.6)
x = 712
c = R(s, x, 152, 200, 62, WHITE, SL[5], 0.75, "round", 8, shd=True)
T(s, x + 14, 162, 170, 10, "Recommended to stock", 8, SANS, False, BODY)
T(s, x + 14, 178, 170, 18, [[("7441C", {"bold": True}), ("  F.lli Ferrari · 37.7 tm", {})]], 9, SANS, False, INK)
T(s, x + 178, 176, 14, 18, "→", 11, SANS, False, INK)
T(s, x, 220, 200, 12, "CALLOUT CARD · floats on photos", 7, SANS, True, MUTE, spc=0.6)
for j, (tk, nm, v) in enumerate([("268 A4", "25.4 tm · 31 units", "−23%"), ("7441C", "37.7 tm · 21 units", "−14%"), ("FBR450R", "45.5 tm · 13 units", "−32%")]):
    y = 246 + j * 34
    T(s, x, y, 70, 14, tk, 10, SANS, True, INK); T(s, x + 72, y + 1, 90, 14, nm, 8.5, SANS, False, BODY); T(s, x + 160, y, 40, 14, v, 10, SANS, True, GREEN_D, "r")
    L(s, x, y + 24, x + 200, y + 24, SL[5])
T(s, x, 352, 200, 12, "LIST ROW · ticker style", 7, SANS, True, MUTE, spc=0.6)
for i, (n_, t) in enumerate([("67", "units / year, Medium + Heavy"), ("64%", "of import value"), ("5", "classes where F.lli Ferrari wins")]):
    x = X0 + i * 290
    R(s, x, 420, 278, 72, WASH, None, "round", 10)
    T(s, x + 18, 430, 90, 40, n_, 28, SERIF, False, INK); T(s, x + 110, 440, 160, 30, t, 9.5, SANS, False, BODY, line=1.3)

# ============================================================ 15 section patterns
s = page("Components · Section patterns", em("Four patterns lifted ", ("straight", True), " from Bitwise."))
# A section intro
R(s, X0, 148, 420, 166, WASH, None, "round", 10)
kicker(s, X0, 166, 420, "Investments", MUTE, "c")
T(s, X0 + 20, 184, 380, 56, [[("Managed exposure to a growing world of ", {}), ("crane opportunities", {"i": True}), (".", {})]], 15, SERIF, False, INK, "c", line=1.15)
T(s, X0 + 40, 246, 340, 30, "Centred kicker + serif headline open a section. Optional one-line lede.", 8.5, SANS, False, BODY, "c")
T(s, X0 + 14, 296, 300, 10, "A · SECTION INTRO", 7, SANS, True, MUTE, spc=0.6)
# B why columns
R(s, 492, 148, 420, 166, WHITE, SL[5], 0.75, "round", 10)
L(s, 500, 214, 904, 208, SL[6], 1)
for i, t in enumerate(["Track record", "Broad suite", "Strong team"]):
    x = 512 + i * 134
    T(s, x, 180, 120, 14, t, 11, SERIF, False, INK); R(s, x, 208 - i * 2 - 3, 6, 6, GREEN, shape="oval")
    T(s, x, 226, 118, 50, "Two or three lines of proof under each dot.", 8.5, SANS, False, BODY, line=1.35)
T(s, 506, 296, 300, 10, "B · WHY COLUMNS (title · dot on line · text)", 7, SANS, True, MUTE, spc=0.6)
# C logo strip
R(s, X0, 330, 420, 166, WHITE, SL[5], 0.75, "round", 10)
kicker(s, X0, 350, 420, "Backed by leading institutions", MUTE, "c")
for i in range(6):
    x = X0 + 22 + i * 64; R(s, x, 376, 56, 26, SL[3], None, "round", 4); T(s, x, 376, 56, 26, "LOGO", 6.5, SANS, True, SL[9], "c", "m")
T(s, X0 + 30, 414, 360, 30, "Logos in one row, same height, greyscale or original colours — never mixed.", 8.5, SANS, False, BODY, "c")
L(s, X0 + 20, 454, X0 + 400, 454, SL[5])
T(s, X0 + 14, 478, 300, 10, "C · LOGO STRIP", 7, SANS, True, MUTE, spc=0.6)
# D CTA band
R(s, 492, 330, 420, 166, grad=(SL[15], "23343C", 45), shape="round", radius=10)
T(s, 512, 352, 380, 50, [[("Let us take the ", {}), ("next step", {"i": True}), (" together.", {})]], 17, SERIF, False, WHITE, line=1.15)
T(s, 512, 404, 360, 24, "Closing band: the one decision or support you ask the reviewers for.", 8.5, SANS, False, SL[8])
button(s, 512, 440, "Approve plan", "primary", 110); button(s, 632, 440, "See appendix", "outline", 110)
T(s, 506, 478, 300, 10, "D · CTA BAND (dark)", 7, SANS, True, SL[9], spc=0.6)

# ============================================================ 16 charts
s = page("Components · Charts", em("One ", ("green", True), " series, everything else slate."),
         "Native PowerPoint charts only. The focus series is Green 500; comparison series use Slate 8 and Slate 12.")
cd = CategoryChartData(); cd.categories = ["2023", "2024", "2025", "2026*"]
cd.add_series("Medium + Heavy", (90, 77, 89, 21)); cd.add_series("Light + Small", (103, 73, 72, 57))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Pt(X0), Pt(172), Pt(520), Pt(300), cd); ch = gf.chart
ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
ch.legend.font.size = Pt(8.5); ch.legend.font.color.rgb = rgb(BODY); ch.legend.font.name = SANS
for ser, c in zip(ch.plots[0].series, [GREEN, SL[8]]): ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(c)
pl = ch.plots[0]; pl.gap_width = 70; pl.overlap = -8; pl.has_data_labels = True
dl = pl.data_labels; dl.font.size = Pt(9); dl.font.name = SERIF; dl.font.color.rgb = rgb(INK); dl.position = XL_LABEL_POSITION.OUTSIDE_END
ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False
ca = ch.category_axis; ca.tick_labels.font.size = Pt(9); ca.tick_labels.font.name = SANS; ca.tick_labels.font.color.rgb = rgb(MUTE); ca.format.line.color.rgb = rgb(SL[6])
T(s, X0, 476, 520, 24, "Units imported per year. *2026 = Jan–14 Aug. Source: Indonesia import records (example from the F.lli Ferrari study).", 8, SANS, False, MUTE, line=1.3)
kicker(s, 600, 172, 300, "Series order")
for i, (c, t) in enumerate([(GREEN, "Focus / Triatra"), (SL[12], "Main comparison"), (SL[8], "Others"), (ACC["blue"], "Extra series 1"), (ACC["purple"], "Extra series 2"), (ACC["red"], "Negative / risk only")]):
    y = 192 + i * 24; R(s, 600, y, 22, 14, c, None, "round", 3); T(s, 630, y + 1, 200, 14, f"{i + 1}  {t}", 9, SANS, False, INK)
kicker(s, 600, 348, 300, "Rules")
for i, t in enumerate(["Headline states the insight", "Labels on bars; no gridlines, no axis", "Axis starts at zero; no 3D, no shadow",
                       "Numbers in Georgia, labels in Arial", "Source line under every chart"]):
    y = 366 + i * 24; R(s, 600, y + 4, 5, 5, GREEN, shape="oval"); T(s, 614, y, 300, 16, t, 9.5, SANS, False, INK)

# ============================================================ 17 tables
s = page("Components · Tables", em("Tables like a ", ("fund list", True), ": light, ruled, right-aligned."))
data = [["Ticker", "Product", "Class", "Units", "Price", "vs competitor"],
        ["268 A4", "F.lli Ferrari knuckle boom", "25–30 tm", "31", "Rp 500 jt", "−23%"],
        ["7441C", "F.lli Ferrari knuckle boom", "35–40 tm", "21", "Rp 1.240 jt", "−14%"],
        ["FBR450R A4", "F.lli Ferrari knuckle boom", "45–50 tm", "13", "Rp 1.350 jt", "−32%"],
        ["FBR350R A4", "F.lli Ferrari knuckle boom", "30–35 tm", "10", "Rp 1.090 jt", "−25%"],
        ["9601CR A8", "F.lli Ferrari knuckle boom", "50–55 tm", "1", "Rp 3.260 jt", "−3%"]]
cws = [110, 250, 110, 90, 140, 164]
tb = s.shapes.add_table(len(data), len(cws), Pt(X0), Pt(156), Pt(sum(cws)), Pt(26 * len(data))).table
tb._tbl.tblPr.set("firstRow", "0"); tb._tbl.tblPr.set("bandRow", "0")
for ci, w in enumerate(cws): tb.columns[ci].width = Pt(w)
for ri, row in enumerate(data):
    tb.rows[ri].height = Pt(26)
    for ci, v in enumerate(row):
        c = tb.cell(ri, ci); c.fill.background(); c.margin_left = c.margin_right = Pt(8); c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.text = v.upper() if ri == 0 else v
        pp = c.text_frame.paragraphs[0]; pp.alignment = PP_ALIGN.RIGHT if ci >= 3 else PP_ALIGN.LEFT
        r = pp.runs[0]; f = r.font; f.name = SANS; f.size = Pt(7.5 if ri == 0 else 9.5)
        f.bold = ri == 0 or ci == 0 or ci == 5; f.color.rgb = rgb(MUTE if ri == 0 else (GREEN_D if ci == 5 else (INK if ci == 0 else BODY)))
        if ri == 0: r._r.get_or_add_rPr().set("spc", "60")
        tcPr = c._tc.get_or_add_tcPr()
        for side in ("lnL", "lnR", "lnT", "lnB"):
            ln = etree.SubElement(tcPr, qn("a:" + side), w=str(int(Pt(1 if (side == "lnB" and ri == 0) else 0.75))))
            if side == "lnB":
                sf = etree.SubElement(ln, qn("a:solidFill")); etree.SubElement(sf, qn("a:srgbClr"), val=SL[15] if ri == 0 else SL[5])
            else: etree.SubElement(ln, qn("a:noFill"))
        for f_ in tcPr.findall(qn("a:noFill")) + tcPr.findall(qn("a:solidFill")):
            if f_.getparent() is tcPr: tcPr.remove(f_); tcPr.append(f_)
T(s, X0, 320, 864, 12, "Example rows from the F.lli Ferrari price comparison. Source: TSP price list, import records.", 8, SANS, False, MUTE)
for i, (h, b) in enumerate([("Header", "7.5 pt bold caps, Slate 11, tracking +0.6, 1 pt Slate 15 rule under it."),
                            ("Rows", "Hairline Slate 5, no fills, no vertical lines. 26 pt row height."),
                            ("Alignment", "Text left, numbers right. First column bold ink as the 'ticker'."),
                            ("Highlight", "Only the decision column in Green 800; risks in Red 9.")]):
    x = X0 + i * 216
    R(s, x, 350, 204, 140, WASH, None, "round", 10)
    T(s, x + 16, 366, 180, 16, h, 13, SERIF, False, INK); T(s, x + 16, 390, 176, 90, b, 9, SANS, False, BODY, line=1.4)

# ============================================================ 18 imagery
s = page("Components · Imagery", em("Photos with ", ("purpose", True), ", treated the same way."))
pic = picture(s, A + "project/crane3.png", X0, 150, 420, 236); round_pic(pic, 10)
R(s, X0, 150, 420, 236, grad=("11181C", "11181C", 90), shape="round", radius=10).fill.gradient()
ov = s.shapes[-1]; st = ov.fill.gradient_stops
for stp, a_ in zip(st, (85, 0)):
    stp.color.rgb = rgb(SL[15]); e = stp._gs.find(qn("a:srgbClr")); etree.SubElement(e, qn("a:alpha"), val=str(a_ * 1000))
ov.fill.gradient_angle = 0
kicker(s, X0 + 20, 300, 300, "Hero photo", SL[8])
T(s, X0 + 20, 316, 380, 40, [[("Dark gradient keeps the ", {}), ("headline", {"i": True}), (" readable.", {})]], 15, SERIF, False, WHITE, line=1.15)
c = R(s, X0 + 236, 342, 170, 34, WHITE, None, "round", 6, shd=True)
T(s, X0 + 248, 349, 150, 20, [[("F.lli Ferrari", {"bold": True}), ("  7441C  →", {})]], 8.5, SANS, False, INK, anchor="m")
for i, im in enumerate([A + "evidence/sc5_72.webp", A + "evidence/sc5_74.webp", A + "evidence/sc5_75.webp"]):
    x = 492 + i * 142; pic = picture(s, im, x, 150, 132, 100); round_pic(pic, 8)
    T(s, x, 256, 132, 12, ["Plant visit", "Painting check", "Customer FAT"][i], 9, SERIF, False, INK)
    T(s, x, 270, 132, 12, "Jun 2026 · UTE plant", 8, SANS, False, MUTE)
pc = s.shapes.add_picture(A + "cutout/u3.png", Pt(512), Pt(298), height=Pt(70))
R(s, 492, 292, 420, 94, WASH, None, "round", 10); s.shapes._spTree.remove(pc._element); s.shapes._spTree.append(pc._element)
T(s, 700, 316, 200, 50, "Product cutouts sit on Slate 2, same baseline and height across a row.", 9, SANS, False, BODY, line=1.35)
for i, (h, b) in enumerate([("Radius", "8–10 pt on single photos; 0 inside dense grids."), ("Overlay", "Slate 15 gradient, 85% → 0%, only under text."),
                            ("Caption", "Serif title + sans meta line under the photo."), ("Quality", "Originals only, never stretched, ≥ 150 dpi.")]):
    x = X0 + i * 216
    T(s, x, 406, 200, 16, h, 12, SERIF, False, INK); T(s, x, 426, 200, 40, b, 9, SANS, False, BODY, line=1.35)
    L(s, x, 400, x + 200, 400, SL[5])

# ============================================================ 19 page types
s = page("Layouts · Page types", em("Eight page types ", ("cover", True), " the whole review."))
TW, TH = 200, 112.5


def mini(s, x, y, t):
    dark = t in (0, 2, 7)
    R(s, x, y, TW, TH, None, SL[6], 0.75, grad=(SL[15], "23343C", 45) if dark else None) if dark else R(s, x, y, TW, TH, WHITE, SL[6], 0.75)
    hc = SL[1] if dark else SL[15]
    R(s, x + 8, y + 7, 16, 5, "E55200"); L(s, x + 8, y + 15, x + TW - 8, y + 15, SL[13] if dark else SL[5], 0.4)
    if t == 0:
        R(s, x + 10, y + 42, 80, 7, hc); R(s, x + 10, y + 52, 60, 7, hc); R(s, x + 10, y + 66, 70, 3, SL[9]); R(s, x + 10, y + 78, 26, 8, GREEN, None, "round", 2)
        R(s, x + 130, y + 88, 60, 14, WHITE, None, "round", 2)
    elif t == 1:
        R(s, x + 10, y + 22, 30, 3, SL[9]); R(s, x + 10, y + 28, 90, 7, hc)
        for i in range(4):
            xx = x + 10 + i * 46; R(s, xx, y + 44, 40, 3, SL[9])
            for j in range(4): R(s, xx, y + 52 + j * 12, 38, 3.5, SL[12])
    elif t == 2:
        R(s, x + 10, y + 46, 30, 3, BR[300]); R(s, x + 10, y + 54, 110, 9, hc); R(s, x + 10, y + 68, 80, 3, SL[9])
        R(s, x + 140, y + 24, 50, 80, SL[13])
    elif t == 3:
        R(s, x + 60, y + 24, 80, 3, SL[9]); R(s, x + 35, y + 31, 130, 7, hc)
        L(s, x + 8, y + 62, x + TW - 8, y + 60, SL[6], 0.5)
        for i in range(3):
            xx = x + 14 + i * 62; R(s, xx, y + 50, 40, 4, hc); R(s, xx, y + 59, 4, 4, GREEN, shape="oval")
            for j in range(3): R(s, xx, y + 72 + j * 8, 48, 3, SL[9])
    elif t == 4:
        R(s, x + 10, y + 22, 90, 6, hc)
        for i in range(3):
            xx = x + 10 + i * 62; R(s, xx, y + 36, 56, 30, SL[8], None, "round", 3); R(s, xx, y + 70, 30, 3, SL[12]); R(s, xx, y + 76, 50, 4, hc)
    elif t == 5:
        R(s, x + 10, y + 22, 90, 6, hc)
        for i, hh in enumerate([30, 22, 40, 14]): R(s, x + 14 + i * 22, y + 100 - hh, 14, hh, GREEN if i == 2 else SL[8])
        for j in range(4): R(s, x + 112, y + 40 + j * 14, 78, 3, SL[12]); L(s, x + 112, y + 47 + j * 14, x + 190, y + 47 + j * 14, SL[5], 0.4)
    elif t == 6:
        R(s, x + 10, y + 22, 90, 6, hc)
        for j in range(5):
            yy = y + 36 + j * 13; R(s, x + 10, yy, 30, 4, hc); R(s, x + 50, yy, 70, 4, SL[9]); R(s, x + 166, yy, 24, 4, GREEN_D); L(s, x + 10, yy + 8, x + 190, yy + 8, SL[5], 0.4)
    elif t == 7:
        R(s, x + 40, y + 40, 120, 8, hc); R(s, x + 60, y + 52, 80, 3, SL[9]); R(s, x + 62, y + 66, 36, 9, GREEN, None, "round", 2); R(s, x + 102, y + 66, 36, 9, None, GREEN, 0.5, "round", 2)


types = [("Cover · dark hero", "Kicker, serif title, lede, two buttons, callout card"), ("Agenda · link columns", "Sections as footer-style link columns"),
         ("Section divider · dark", "Kicker, serif title, photo panel right"), ("Section intro · why", "Centred kicker + headline, why columns"),
         ("Insights · cards", "Three cards: photo, meta, serif title"), ("Data · chart + table", "Chart left, ticker-style rows right"),
         ("Product list", "Ticker rows: code, name, class, value"), ("Closing · CTA", "Dark band, the one decision, buttons")]
for i, (n_, d) in enumerate(types):
    x = X0 + (i % 4) * 221.3; y = 150 + (i // 4) * 178
    mini(s, x, y, i)
    T(s, x, y + TH + 8, TW, 16, n_, 11, SERIF, False, INK); T(s, x, y + TH + 26, TW, 26, d, 8.5, SANS, False, BODY, line=1.3)

# ============================================================ 20 dark divider example
s = page("", None, dark=True, section="Layouts · Dark section divider")
R(s, 0, 52, W, 458, grad=(SL[15], "23343C", 45))
kicker(s, X0, 150, 400, "Section 06 · F.lli Ferrari crane strategy", BR[300])
T(s, X0, 172, 440, 120, [[("Where the price ", {}), ("wins", {"i": True}), (", and where it does not.", {})]], 32, SERIF, False, WHITE, line=1.05)
T(s, X0, 300, 400, 50, "Market overview, price comparison by tm class, the F.lli Ferrari advantage and the appendix.", 10.5, SANS, False, SL[8], line=1.4)
for i, t in enumerate(["A  Market overview", "B  Price comparison", "C  F.lli Ferrari advantage", "D  Appendix"]):
    y = 366 + i * 26; T(s, X0, y, 300, 14, t, 10, SANS, False, SL[3] if i else WHITE); L(s, X0, y + 20, X0 + 300, y + 20, SL[13], 0.75)
pic = picture(s, A + "project/crane2.png", 560, 140, 352, 340); round_pic(pic, 12)
c = R(s, 590, 420, 200, 40, WHITE, None, "round", 6, shd=True)
T(s, 604, 426, 180, 28, [[("5 cranes", {"bold": True}), ("  cheaper head to head  →", {})]], 8.5, SANS, False, INK, anchor="m")

# ============================================================ 21 applied example
s = page("Layouts · Applied example", [[("Five F.lli Ferrari cranes ", {}), ("win", {"i": True}), (" on price.", {})]],
         "Same size or bigger, lower price than the market leaders in their tm class (Jan 2023 – 14 Aug 2026).", section="Section 06 · Project")
for i, (n_, t) in enumerate([("5", "cranes cheaper head to head"), ("−3% to −32%", "price gap vs the leader"), ("76", "units won by these five models")]):
    x = X0 + i * 290
    if i: L(s, x - 14, 166, x - 14, 214, SL[5])
    T(s, x, 162, 270, 34, n_, 26, SERIF, False, INK); T(s, x, 198, 260, 14, t, 9, SANS, False, BODY)
for i, (tk, cl, u, v, im) in enumerate([("268 A4", "25–30 tm", "31 units won", "−23% vs Amco Veba V825", A + "project/crane0.png"),
                                        ("7441C", "35–40 tm", "21 units won", "−14% vs Palfinger PK 41002", A + "project/crane1.png"),
                                        ("FBR450R A4", "45–50 tm", "13 units won", "−32% vs Amco Veba V950", A + "project/crane2.png"),
                                        ("FBR350R A4", "30–35 tm", "10 units won", "−25% vs Hiab X-CLX 388", A + "project/crane3.png")]):
    x = X0 + i * 220
    R(s, x, 236, 204, 256, WHITE, SL[5], 0.75, "round", 10)
    pic = picture(s, im, x + 10, 246, 184, 110); round_pic(pic, 6)
    T(s, x + 14, 364, 180, 12, [[("F.lli Ferrari", {"bold": True}), ("  •  " + cl, {})]], 8.5, SANS, False, BODY)
    T(s, x + 14, 380, 180, 20, tk, 15, SERIF, False, INK)
    T(s, x + 14, 404, 180, 14, u, 9.5, SANS, False, BODY)
    R(s, x + 14, 428, 176, 0.75, SL[5])
    T(s, x + 14, 436, 180, 24, v, 9, SANS, True, GREEN_D, line=1.2)
    link(s, x + 14, 468, "See comparison", INK)

# ============================================================ 22 writing & voice
s = page("Application · Writing & voice", em("Complicated work, ", ("explained", True), " simply."),
         "Bitwise voice: confident, plain English, no hype. Headlines carry the message; the body only proves it.")
kicker(s, X0, 166, 400, "Topic → message")
for i, (a, b) in enumerate([("Market Overview", [("Medium and Heavy cranes are 41% of units but ", {}), ("64% of value", {"i": True})]),
                            ("Price Comparison", [("F.lli Ferrari is cheaper in ", {}), ("five", {"i": True}), (" tm classes", {})]),
                            ("Monitoring", [("Plant follow-up keeps every PO on its ", {}), ("agreed", {"i": True}), (" RFD date", {})]),
                            ("Work Challenges", [("Last-minute quotes are the ", {}), ("main risk", {"i": True}), (" to lead time", {})])]):
    y = 184 + i * 46
    T(s, X0, y + 8, 150, 16, a, 10, SANS, False, MUTE); T(s, X0 + 150, y + 6, 30, 16, "→", 12, SANS, True, GREEN)
    T(s, X0 + 180, y + 2, 380, 30, [b], 13, SERIF, False, INK, line=1.1); L(s, X0, y + 38, X0 + 560, y + 38, SL[4])
kicker(s, 640, 166, 300, "Voice rules")
for i, t in enumerate(["Short sentences, active voice", "One idea per headline", "Numbers instead of adjectives", "Define an abbreviation once: Request for Delivery (RFD)",
                       "English throughout; system names as they appear", "No hype words: 'very', 'huge', 'amazing'"]):
    y = 184 + i * 30; R(s, 640, y + 5, 5, 5, GREEN, shape="oval"); T(s, 654, y, 258, 26, t, 9.5, SANS, False, INK, line=1.25)
R(s, X0, 384, X1 - X0, 108, WASH, None, "round", 10)
kicker(s, X0, 402, X1 - X0, "The headline test", MUTE, "c")
T(s, X0 + 40, 420, X1 - X0 - 80, 60, [[("Read only the headlines from first to last slide. If they tell the whole 6-month story, the deck ", {}), ("works", {"i": True}), (".", {})]],
  16, SERIF, False, INK, "c", line=1.2)

# ============================================================ 23 numbers & formats
s = page("Application · Numbers & formats", em("One format for ", ("every", True), " figure."))
fm = [("Currency · table", "Rp 1.240.000.000"), ("Currency · text", "Rp 1,24 M  ·  Rp 650 jt"), ("Capacity", "25–35 tm  ·  30,4 tm"),
      ("Count", "31 units  ·  1 unit"), ("Percent / change", "41%  ·  +23%  ·  −14%"), ("Date", "14 Aug 2026"),
      ("Period", "Jan 2023 – Aug 2026"), ("Quarter / month", "Q3 2026  ·  Oct 2026"), ("Estimate", "7441C*  (*estimate, noted)")]
for i, (k_, v) in enumerate(fm):
    col = i // 5; row = i % 5; x = X0 + col * 440; y = 150 + row * 52
    T(s, x, y + 8, 160, 14, k_.upper(), 7.5, SANS, True, MUTE, spc=1); T(s, x + 160, y + 2, 260, 26, v, 16, SERIF, False, INK)
    L(s, x, y + 38, x + 420, y + 38, SL[5])
R(s, 488, 410, 424, 82, BR[100], None, "round", 10)
kicker(s, 506, 424, 300, "Note", GREEN_D)
T(s, 506, 440, 390, 48, "En dash (–) for ranges, minus sign (−) for drops. Round only in running text; tables keep the full figure so totals add up.", 9.5, SANS, False, SL[13], line=1.35)

# ============================================================ 24 workflow
s = page("Application · Draft → final", em("How your draft ", ("becomes", True), " the final deck."),
         "You keep the content and order; the design pass applies this guide. Five steps, in this order.")
steps = [("Map", "Tag each draft slide with one page type (p. 19)."), ("Message", "Rewrite the title as a message headline + kicker."),
         ("Rebuild", "Move content onto the grid using the components."), ("Evidence", "Swap screenshots for native charts/tables; add sources."),
         ("Check", "Run the checklist; export PDF + PPTX.")]
L(s, X0 + 10, 214, X1 - 10, 214, SL[6], 1)
for i, (h, b) in enumerate(steps):
    x = X0 + i * 176
    T(s, x, 172, 160, 14, f"0{i + 1}", 9, SANS, True, GREEN)
    T(s, x, 188, 160, 18, h, 15, SERIF, False, INK)
    R(s, x, 211, 6, 6, GREEN if i < 5 else SL[8], shape="oval")
    T(s, x, 230, 160, 60, b, 9.5, SANS, False, BODY, line=1.4)
R(s, X0, 316, 420, 176, WASH, None, "round", 10)
kicker(s, X0 + 20, 334, 380, "What stays yours")
for i, t in enumerate(["Order of sections and slides", "Facts, numbers and wording of results", "Photos and evidence you chose"]):
    T(s, X0 + 20, 356 + i * 26, 380, 16, [[("✓  ", {"color": GREEN, "bold": True}), (t, {})]], 10.5, SANS, False, INK)
R(s, 492, 316, 420, 176, WHITE, SL[5], 0.75, "round", 10)
kicker(s, 512, 334, 380, "What the design pass changes")
for i, t in enumerate(["Fonts, sizes, colours, spacing", "Position and size of every element", "Headlines rewritten as messages (you approve)", "Charts and tables rebuilt natively"]):
    T(s, 512, 356 + i * 26, 380, 16, [[("→  ", {"color": GREEN, "bold": True}), (t, {})]], 10.5, SANS, False, INK)

# ============================================================ 25 checklist
s = page("Application · Pre-send checklist", em("Sixteen checks ", ("before", True), " it goes out."))
groups = [("Story", ["Headlines alone tell the story", "One message per slide", "Agenda matches dividers", "Closing states the decision"]),
          ("Type", ["Georgia + Arial only", "Italic emphasis, never bold serif", "Kickers in tracked caps", "Body ≥ 9 pt, sources ≥ 8 pt"]),
          ("Colour & layout", ["Slate + one green only", "Max one primary button", "Everything on the 12-col grid", "Footer and page number present"]),
          ("Data", ["Native charts and tables", "Source under every figure", "Formats follow p. 23", "Numbers match the appendix"])]
for gi, (g, its) in enumerate(groups):
    x = X0 + gi * 216
    kicker(s, x, 152, 200, g); L(s, x, 168, x + 204, 168, SL[15], 1)
    for i, t in enumerate(its):
        y = 180 + i * 44
        R(s, x, y + 2, 13, 13, WHITE, SL[8], 1, "round", 3)
        T(s, x + 22, y, 180, 34, t, 10.5, SERIF, False, INK, line=1.15)
        L(s, x, y + 36, x + 204, y + 36, SL[4])
R(s, X0, 372, X1 - X0, 120, grad=(SL[15], "23343C", 45), shape="round", radius=12)
kicker(s, X0 + 28, 392, 400, "File naming", SL[9])
T(s, X0 + 28, 410, 800, 30, [[("NEDP_6M_Review_", {"color": WHITE}), ("TiberiasSimu", {"color": BR[300]}), ("_v03_2026-10-13", {"color": SL[8]}), (".pptx", {"color": SL[9]})]], 18, SERIF)
T(s, X0 + 28, 446, 600, 30, "Send the PDF to read and the PPTX to edit. Raise the version on every copy you send.", 9.5, SANS, False, SL[8])
button(s, X1 - 150, 448, "Ready to send", "primary", 120)

# ============================================================ 26 closing
s = p.slides.add_slide(BL); TOTAL[0] += 1
R(s, 0, 0, W, H, grad=(SL[15], "23343C", 45))
logo(s, X0, 30, 22)
kicker(s, 0, 190, W, "Next step", BR[300], "c")
T(s, 120, 212, 720, 90, [[("Send the draft. ", {}), ("We make it clear.", {"i": True})]], 38, SERIF, False, WHITE, "c")
T(s, 240, 290, 480, 40, "Share the draft PPT with its content and order. Each slide will be rebuilt with this guidance: type, colour, grid, components.",
  10.5, SANS, False, SL[8], "c", line=1.4)
button(s, W / 2 - 125, 350, "Share draft", "primary", 120); button(s, W / 2 + 5, 350, "Ask a question", "outline", 120)
T(s, X0, 500, 600, 12, "PREPARED BY TIBERIAS K. SIMU  ·  MARKETING STRATEGIC 2 ASSOCIATE  ·  PT TRIATRA SINERGIA PRATAMA", 6.5, SANS, True, SL[9], spc=0.8)
T(s, X0, 514, 860, 12, "Style reference: Bitwise Asset Management website (typography, colour tokens, components). Fonts substituted with Georgia and Arial.", 6.5, SANS, False, SL[11])

# strip theme styles (default shadows / outlines) from every shape and connector
for sl in p.slides:
    for el in sl.shapes._spTree.iter(qn("p:style")):
        pass
    for st in list(sl.shapes._spTree.iter(qn("p:style"))):
        st.getparent().remove(st)
p.save(OUT)
print("saved", OUT, TOTAL[0], "slides")
