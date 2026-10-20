"""Appendix: crane photos. A1 = head to head leader vs our challenger; A2 = other leaders and F.lli Ferrari reference models."""
import sys
sys.path.insert(0, '.')
from cr_common import *
from PIL import Image
D = 'assets/cranes/'
deck = Deck()
def card(C, x, y, w, h, f, title, sub, color, tag=None, tagc=G):
    C.box(x, y, w, h, 'FFFFFF', 'D9D9D9', lw=.75)
    ph = h - 46; iw, ih = Image.open(D + f).size; k = min((w - 12) / iw, (ph - 8) / ih)
    C.s.shapes.add_picture(D + f, E(x + (w - iw * k) / 2), E(y + 6 + (ph - 8 - ih * k) / 2), E(iw * k), E(ih * k))
    C.tx(x + 6, y + ph + 2, w - 12, 18, [[(title, True, color, 10.5)]], al=PP_ALIGN.CENTER)
    C.tx(x + 6, y + ph + 20, w - 12, 16, [[(sub, False, '595959', 8.5)]], al=PP_ALIGN.CENTER)
    if tag:
        b = C.box(x + 6, y + 6, 70, 16, tagc); tf = b.text_frame
        for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'): setattr(tf, m, 0)
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = tag
        r.font.size = Pt(8); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = rgb('FFFFFF')
# ---------- A1: head to head ----------
C = deck.slide('Appendix: Crane Photos (1/2)/', 'What do the leader and', 'our challenger look like?',
               'Head to head: the class leader next to the crane we offer against it',
               [('Medium and Heavy tm classes where we have a challenger. ', False), ('Light and Small photos not yet available', True), (' (models not in the photo library).', False)])
pairs = [('Medium 25–30 tm', ('Amco_Veba_V825.jpg', 'Amco Veba V825', 'Leader · Rp 517 Jt'), ('F_lli_Ferrari_268_A4.jpg', 'F.lli Ferrari 258 A3', 'Rp 455 Jt · photo: 268 A4, same 8 Series')),
         ('Medium 30–35 tm', ('Hiab_X_CLX_388.jpg', 'HIAB X-CLX 388', 'Leader · Rp 762 Jt'), ('XCMG_SQZ325_4.jpg', 'XCMG SQZ325.4', 'Rp 484 Jt')),
         ('Medium 35–40 tm', ('Palfinger_PK_41002.jpg', 'Palfinger PK 41002', 'Leader · Rp 1.103 Jt'), ('XCMG_KSQZ365_4.jpg', 'XCMG KSQZ365.4', 'Rp 478 Jt')),
         ('Heavy 45–50 tm', ('Amco_Veba_V950.jpg', 'Amco Veba V950', 'Leader · Rp 1.575 Jt'), ('F_lli_Ferrari_FBR450R_A4.jpg', 'F.lli Ferrari FBR450 A4', 'Rp 1.251 Jt · photo: FBR450R A4')),
         ('Heavy 50–55 tm', ('Palfinger_PK_53002.jpg', 'Palfinger PK 53002', 'Leader · Rp 1.361 Jt'), ('F_lli_Ferrari_FBR450R_A4.jpg', 'F.lli Ferrari FBR450R A4', 'Rp 1.408 Jt'))]
PW = 1206 / len(pairs); CW = (PW - 18) / 2
for i, (lab, a, b) in enumerate(pairs):
    x = 36 + i * PW
    C.box(x + 2, 236, PW - 6, 24, DG); C.tx(x + 2, 240, PW - 6, 18, [[(lab, True, 'FFFFFF', 11)]], al=PP_ALIGN.CENTER)
    card(C, x + 2, 266, PW - 6, 192, a[0], a[1], a[2], '000000', 'LEADER', '7F7F7F')
    card(C, x + 2, 464, PW - 6, 192, b[0], b[1], b[2], DG, 'OUR CRANE', G)
C.tx(36, 664, 1206, 30, [[('Photos: brand brochures and websites, collected for the F.lli Ferrari market strategy deck. Prices per unit as on the class map slides '
                           '(competitors = average import price × Rp 17.803/USD; F.lli Ferrari = price list June 2026, K − I, less 13.6% TSP GP).', False, '7F7F7F', 7.5)]])
# ---------- A2: other models ----------
C = deck.slide('Appendix: Crane Photos (2/2)/', 'Which other cranes', 'did we look at?',
               'Other class leaders, and F.lli Ferrari models we checked but did not pick',
               [('Leaders of classes with no cheaper challenger yet, and F.lli Ferrari models that are ', False), ('more than 30% above the leader', True), (' in their class.', False)])
C.tx(36, 236, 600, 18, [[('Class leaders with no challenger yet', True, DG, 12)]])
lead = [('Sany_Palfinger_SPK42502.jpg', 'Sany Palfinger SPK42502', 'Medium 40–45 tm · Rp 693 Jt'), ('Sany_Palfinger_SPK61502.jpg', 'Sany Palfinger SPK61502', 'Heavy 60–65 tm · Rp 1.235 Jt'),
        ('Palfinger_PK_76002_EH_D.jpg', 'Palfinger PK 76002', 'Heavy 70–75 tm · Rp 1.918 Jt'), ('Palfinger_PK_88002_EH_C.jpg', 'Palfinger PK 88002', 'Heavy 80–85 tm · Rp 1.863 Jt'),
        ('XCMG_GSQZ880_6.jpg', 'XCMG GSQZ880.6', 'Heavy 85–90 tm · Rp 1.162 Jt')]
W5 = (1206 - 4 * 10) / 5
for i, (f, t, sb) in enumerate(lead): card(C, 36 + i * (W5 + 10), 258, W5, 190, f, t, sb, '000000')
C.tx(36, 456, 600, 18, [[('F.lli Ferrari models checked, not picked', True, DG, 12)]])
fer = [('F_lli_Ferrari_FBR350R_A4.jpg', 'FBR350R A4', 'Medium 30–35 · +49% vs X-CLX 388'), ('F_lli_Ferrari_746_A4.jpg', '746 A4', 'Medium 40–45 · +113% vs SPK42502'),
       ('F_lli_Ferrari_9601CR_A8.jpg', '9601CR A8', 'Heavy 50–55 · +140% vs PK 53002'), ('F_lli_Ferrari_FBR660R_A4.jpg', 'FBR660R A4', 'Heavy 55–60 · no import demand'),
       ('F_lli_Ferrari_990R.jpg', '990R', 'Heavy 70–75 · +121% vs PK 76002')]
for i, (f, t, sb) in enumerate(fer): card(C, 36 + i * (W5 + 10), 478, W5, 180, f, 'F.lli Ferrari ' + t, sb, DG)
C.tx(36, 666, 1206, 30, [[('Photos: brand brochures and websites. Prices per unit as on the class map slides. % = F.lli Ferrari price vs the class leader (price list June 2026, K − I, less 13.6% TSP GP; '
                           '9601CR A8 = UTPE quote; 990R = TSP price less deck & install, less 13.6%).', False, '7F7F7F', 7.5)]])
deck.save('v7/Appendix_Crane_Photos.pptx'); print('ok')
