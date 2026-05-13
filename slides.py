from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import mm
import math, random

# ── 16:9 slide dimensions (PowerPoint standard in points) ─────────────────────
SW = 720   # slide width  in points
SH = 405   # slide height in points

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = HexColor("#FFFFFF")
PANEL    = HexColor("#162236")
CARD     = HexColor("#1C2E44")
BORDER   = HexColor("#243650")
A1       = HexColor("#4FC3F7")   # sky blue
A2       = HexColor("#66BB6A")   # green
A3       = HexColor("#FFA726")   # amber
A4       = HexColor("#EF5350")   # red/coral
A5       = HexColor("#AB47BC")   # purple
WHITE    = HexColor("#FFFFFF")
LGRAY    = HexColor("#90A4AE")
DGRAY    = HexColor("#37474F")
YELLOW   = HexColor("#FFF176")
RSOFT    = HexColor("#EF9A9A")
GSOFT    = HexColor("#A5D6A7")
BSOFT    = HexColor("#90CAF9")
DARK     = HexColor("#0D1B2A")

# ── Layout constants ──────────────────────────────────────────────────────────
TOP_BAR  = 28     # header bar height
MARGIN_L = 28
MARGIN_R = 28
CONTENT_TOP = SH - TOP_BAR - 14   # y to start content below header
CONTENT_BOT = 16                   # bottom margin

def content_height():
    return CONTENT_TOP - CONTENT_BOT  # usable content height

# ── Canvas helpers ─────────────────────────────────────────────────────────────

def new_page(c, accent=A1):
    c.setFillColor(BG)
    c.rect(0, 0, SW, SH, fill=1, stroke=0)
    c.setFillColor(accent)
    c.rect(0, SH - TOP_BAR, SW, TOP_BAR, fill=1, stroke=0)

def header(c, title, subtitle=None, accent=A1):
    """Draw title inside the top bar."""
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN_L, SH - TOP_BAR + 9, title)
    if subtitle:
        c.setFont("Helvetica", 8)
        tw = c.stringWidth(title, "Helvetica-Bold", 13)
        c.setFillColor(HexColor("#1A3A5C"))
        c.drawString(MARGIN_L + tw + 10, SH - TOP_BAR + 10, subtitle)

def section_cover(c, num, title, subtitle, accent):
    new_page(c, accent)
    # left color stripe
    c.setFillColor(accent)
    c.rect(0, 0, 10, SH - TOP_BAR, fill=1, stroke=0)
    # big number ghost
    c.setFillColor(HexColor("#1A2E44"))
    c.setFont("Helvetica-Bold", 120)
    c.drawString(18, SH//2 - 60, num)
    # title
    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(18, SH//2 - 4)
    c.drawString(20, SH//2 - 4, title)
    # subtitle
    c.setFillColor(LGRAY)
    c.setFont("Helvetica", 12)
    c.drawString(20, SH//2 - 22, subtitle)

def rounded_rect(c, x, y, w, h, r=4, fill=CARD, stroke=BORDER, sw=0.8):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(sw)
    c.roundRect(x, y, w, h, r, fill=1, stroke=1)

def label_box(c, cx, cy, w, h, text, fill=CARD, border=A1, tcolor=WHITE, fsize=8, bold=False):
    rounded_rect(c, cx - w/2, cy - h/2, w, h, r=3, fill=fill, stroke=border, sw=1)
    c.setFillColor(tcolor)
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, fsize)
    tw = c.stringWidth(text, font, fsize)
    c.drawString(cx - tw/2, cy - fsize*0.35, text)

def arrow_h(c, x1, y1, x2, y2=None, col=A1, lw=1.2):
    """Draw a horizontal/near-horizontal arrow.

    Supports both call styles used in this file:
    - arrow_h(c, x1, y, x2, col)
    - arrow_h(c, x1, y1, x2, y2, col)
    """
    # Backward compatibility: 5-arg style where 5th positional arg is color.
    if isinstance(y2, Color):
        col = y2
        y2 = y1
    if y2 is None:
        y2 = y1

    c.setStrokeColor(col)
    c.setLineWidth(lw)

    angle = math.atan2(y2 - y1, x2 - x1)
    ex = x2 - 5 * math.cos(angle)
    ey = y2 - 5 * math.sin(angle)
    c.line(x1, y1, ex, ey)

    c.setFillColor(col)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - 7 * math.cos(angle - 0.4), y2 - 7 * math.sin(angle - 0.4))
    p.lineTo(x2 - 7 * math.cos(angle + 0.4), y2 - 7 * math.sin(angle + 0.4))
    p.close()
    c.drawPath(p, fill=1, stroke=0)

def arrow_v(c, x, y1, y2, col=A1, lw=1.2):
    """Arrow pointing downward from y1 to y2 (y2 < y1 in PDF coords)."""
    c.setStrokeColor(col); c.setLineWidth(lw)
    c.line(x, y1, x, y2 + 5)
    c.setFillColor(col)
    p = c.beginPath()
    p.moveTo(x, y2); p.lineTo(x-3, y2+6); p.lineTo(x+3, y2+6); p.close()
    c.drawPath(p, fill=1, stroke=0)

def arrow_diag(c, x1, y1, x2, y2, col=A1, lw=1.2):
    c.setStrokeColor(col); c.setLineWidth(lw)
    angle = math.atan2(y2 - y1, x2 - x1)
    ex = x2 - 5*math.cos(angle); ey = y2 - 5*math.sin(angle)
    c.line(x1, y1, ex, ey)
    c.setFillColor(col)
    p = c.beginPath(); p.moveTo(x2, y2)
    p.lineTo(x2 - 7*math.cos(angle - 0.4), y2 - 7*math.sin(angle - 0.4))
    p.lineTo(x2 - 7*math.cos(angle + 0.4), y2 - 7*math.sin(angle + 0.4))
    p.close(); c.drawPath(p, fill=1, stroke=0)

def math_pill(c, x, y, text, w=None, accent=YELLOW):
    fw = c.stringWidth(text, "Courier-Bold", 9)
    bw = w if w else fw + 16
    rounded_rect(c, x, y - 10, bw, 16, r=3, fill=HexColor("#1A3050"), stroke=accent, sw=1)
    c.setFillColor(accent)
    c.setFont("Courier-Bold", 9)
    c.drawString(x + 8, y - 4, text)

def bullet_list(c, x, y, items, size=9, lh=16, col=WHITE, dot=A1, max_w=None):
    mw = max_w if max_w else SW - x - MARGIN_R
    for item in items:
        c.setFillColor(dot)
        c.circle(x + 4, y + 2.5, 2.5, fill=1, stroke=0)
        c.setFillColor(col); c.setFont("Helvetica", size)
        # simple word-wrap
        words = item.split(); line = ""; first_line = True
        ix = x + 12
        for word in words:
            test = (line + " " + word).strip()
            if c.stringWidth(test, "Helvetica", size) <= mw - 12:
                line = test
            else:
                c.drawString(ix, y, line)
                y -= lh - 4; line = word; ix = x + 18
        if line:
            c.drawString(ix, y, line)
            y -= lh
    return y

def section_label(c, x, y, text, accent=A1):
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y, text.upper())
    c.setLineWidth(0.5); c.setStrokeColor(accent)
    tw = c.stringWidth(text.upper(), "Helvetica-Bold", 8)
    c.line(x + tw + 4, y + 3, SW - MARGIN_R, y + 3)

# ══════════════════════════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════════════════════════
random.seed(99)
c = canvas.Canvas("ensemble_slides.pdf", pagesize=(SW, SH))

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 01 – COVER
# ─────────────────────────────────────────────────────────────────────────────
new_page(c, A1)
# decorative circles (background)
for cx, cy, r, col in [(SW-80, 80, 70, HexColor("#0F2840")),
                        (SW-50, 40, 35, HexColor("#122840")),
                        (60,    50, 45, HexColor("#0F2840"))]:
    c.setFillColor(col); c.circle(cx, cy, r, fill=1, stroke=0)

c.setFillColor(DARK); c.setFont("Helvetica-Bold", 30)
tw = c.stringWidth("Ensemble Learning", "Helvetica-Bold", 30)
c.drawString((SW - tw)/2, SH//2 + 30, "Ensemble Learning")

c.setFillColor(A1); c.setFont("Helvetica-Bold", 13)
sub = "Bagging  ·  Boosting  ·  Random Forest  ·  XGBoost"
tw = c.stringWidth(sub, "Helvetica-Bold", 13)
c.drawString((SW - tw)/2, SH//2 + 8, sub)

c.setFillColor(LGRAY); c.setFont("Helvetica", 10)
sub2 = "From Fundamentals to Mathematics — with Step-by-Step Diagrams"
tw = c.stringWidth(sub2, "Helvetica", 10)
c.drawString((SW - tw)/2, SH//2 - 10, sub2)

# bottom tag line
c.setFillColor(DGRAY)
c.rect(0, 0, SW, 22, fill=1, stroke=0)
c.setFillColor(A1); c.setFont("Helvetica-Bold", 8)
tags = ["Decision Trees", "Information Gain", "Bias-Variance", "Bagging", "Boosting", "XGBoost"]
tx = MARGIN_L
for tag in tags:
    tw = c.stringWidth(tag, "Helvetica-Bold", 8)
    rounded_rect(c, tx, 4, tw + 10, 14, r=3, fill=CARD, stroke=A1, sw=0.5)
    c.setFillColor(A1); c.setFont("Helvetica-Bold", 8)
    c.drawString(tx + 5, 8, tag)
    tx += tw + 18
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# SLIDE 02 – TABLE OF CONTENTS
# ─────────────────────────────────────────────────────────────────────────────
new_page(c, A1)
header(c, "Table of Contents", accent=A1)
sections = [
    ("01", "Prerequisites",  "Entropy · Information Gain · Decision Trees · Bias · Variance · Overfitting", A1),
    ("02", "Bagging",        "Bootstrap Aggregation — how averaging kills variance step by step", A2),
    ("03", "Random Forest",  "Bagging + Feature Randomness = Decorrelated Trees", A3),
    ("04", "Boosting",       "Sequential Error Correction — AdaBoost & Gradient Boosting", A4),
    ("05", "XGBoost",        "Regularised Gradient Boosting — the Competition Champion", A5),
    ("06", "Comparison",     "Side-by-side summary · When to use which", LGRAY),
]
y = CONTENT_TOP - 8
row_h = (y - CONTENT_BOT) / len(sections) - 2
for num, title, sub, col in sections:
    rounded_rect(c, MARGIN_L, y - row_h, SW - MARGIN_L - MARGIN_R, row_h - 2, r=4, fill=CARD, stroke=col, sw=1)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 12); c.drawString(MARGIN_L + 8, y - row_h/2 + 3, num)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 9); c.drawString(MARGIN_L + 30, y - row_h/2 + 3, title)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7.5); c.drawString(MARGIN_L + 30, y - row_h/2 - 8, sub)
    y -= row_h + 2
c.showPage()

# ═══════════════════════════════════════════════════════
# SECTION 01 – PREREQUISITES
# ═══════════════════════════════════════════════════════

# ─── S03: Entropy ─────────────────────────────────────
new_page(c, A1)
header(c, "Prerequisites — Entropy: Measuring Disorder", accent=A1)
y = CONTENT_TOP

# LEFT: explanation
lx = MARGIN_L; rx = SW//2 + 10
col_w = SW//2 - MARGIN_L - 10

section_label(c, lx, y - 2, "Concept", A1)
y -= 18
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 10)
c.drawString(lx, y, "Entropy = How mixed / impure a set is")
y -= 14
bullet_list(c, lx, y, [
    "Pure set (all same class): Entropy = 0",
    "Perfectly mixed (50/50): Entropy = 1",
    "More classes, more mixed = higher entropy",
], size=9, lh=15, max_w=col_w, col=DARK)
y -= 50
math_pill(c, lx, y, "H(S) = - SUM  p_i * log2(p_i)", w=col_w - 10)
y -= 22
c.setFillColor(LGRAY); c.setFont("Helvetica", 8)
c.drawString(lx, y, "p_i = fraction of class i in set S")

# RIGHT: visual entropy bar
rx2 = rx; ry = CONTENT_TOP - 18
section_label(c, rx2, ry, "Visualised", A1)
ry -= 18
examples = [
    ([10, 0],  "All Cat",    "H = 0.00", A2),
    ([8, 2],   "8 Cat 2 Dog","H = 0.72", A3),
    ([5, 5],   "5 Cat 5 Dog","H = 1.00", A4),
    ([3, 7],   "3 Cat 7 Dog","H = 0.88", A3),
    ([0, 10],  "All Dog",    "H = 0.00", A2),
]
bar_w = (SW - rx2 - MARGIN_R) / len(examples) - 6
for i, (counts, lab, hval, col) in enumerate(examples):
    bx = rx2 + i * (bar_w + 6)
    total = sum(counts)
    # stacked bar
    bar_h = 80
    by_base = ry - bar_h - 30
    fracs = [c_/total for c_ in counts]
    colors_bar = [A1, A3]
    yy = by_base
    for frac, bc in zip(fracs, colors_bar):
        h_ = frac * bar_h
        c.setFillColor(bc)
        c.rect(bx, yy, bar_w, h_, fill=1, stroke=0)
        yy += h_
    # outline
    c.setStrokeColor(BORDER); c.setLineWidth(0.5)
    c.rect(bx, by_base, bar_w, bar_h, fill=0, stroke=1)
    # entropy label
    c.setFillColor(col); c.setFont("Helvetica-Bold", 8)
    tw = c.stringWidth(hval, "Helvetica-Bold", 8)
    c.drawString(bx + bar_w/2 - tw/2, by_base - 12, hval)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
    tw = c.stringWidth(lab, "Helvetica", 7)
    c.drawString(bx + bar_w/2 - tw/2, by_base - 22, lab)

c.showPage()

# ─── S04: Information Gain ────────────────────────────
new_page(c, A1)
header(c, "Prerequisites — Information Gain: Choosing the Best Split", accent=A1)
y = CONTENT_TOP

section_label(c, MARGIN_L, y - 2, "Core Idea", A1)
y -= 18
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 10)
c.drawString(MARGIN_L, y, "Information Gain = How much does a split REDUCE entropy?")
y -= 15
bullet_list(c, MARGIN_L, y, [
    "Before split: measure entropy of the whole set H(S)",
    "After split on feature A: measure weighted entropy of each child node",
    "IG = H(S) - weighted_avg( H(children) )",
    "Pick the split with the HIGHEST Information Gain at each node",
], size=9, lh=15, max_w=SW - MARGIN_L*2, col=DARK)
y -= 65
math_pill(c, MARGIN_L, y, "IG(S, A) = H(S)  -  SUM_v  (|S_v|/|S|) * H(S_v)", w=320)
y -= 22
c.setFillColor(LGRAY); c.setFont("Helvetica", 8)
c.drawString(MARGIN_L, y, "S_v = subset of S where feature A has value v")
y -= 22

# Diagram: example split
section_label(c, MARGIN_L, y - 2, "Worked Example — should we split on Weather or Wind?", A1)
y -= 18

# root node
root_cx = SW / 2; root_cy = y - 22; root_w = 190; root_h = 28
rounded_rect(c, root_cx - root_w/2, root_cy - root_h/2, root_w, root_h, r=4, fill=CARD, stroke=A1, sw=1.5)
c.setFillColor(A1); c.setFont("Helvetica-Bold", 8)
tw = c.stringWidth("All 14 samples  [9 Play, 5 No-Play]  H=0.94", "Helvetica-Bold", 8)
c.drawString(root_cx - tw/2, root_cy - 3, "All 14 samples  [9 Play, 5 No-Play]  H=0.94")

# Option A: Weather split
lx_a = MARGIN_L + 10; y_child = root_cy - 68
c.setFillColor(A3); c.setFont("Helvetica-Bold", 8)
c.drawString(lx_a, root_cy - 35, "Split on WEATHER")
children_a = [("Sunny\n[2P,3N]\nH=0.97", A4, lx_a + 30),
              ("Overcast\n[4P,0N]\nH=0.00", A2, lx_a + 100),
              ("Rain\n[3P,2N]\nH=0.97",   A4, lx_a + 170)]
for label, col, cx in children_a:
    arrow_diag(c, root_cx, root_cy - root_h/2, cx + 25, y_child + 20, A3)
    rounded_rect(c, cx, y_child, 56, 28, r=3, fill=CARD, stroke=col, sw=1)
    c.setFillColor(WHITE); c.setFont("Helvetica", 7.5)
    for li, line in enumerate(label.split("\n")):
        tw = c.stringWidth(line, "Helvetica", 7.5)
        c.drawString(cx + 28 - tw/2, y_child + 22 - li*9, line)
# IG A
math_pill(c, lx_a, y_child - 22, "IG(Weather) = 0.94 - (5/14)*0.97 - (4/14)*0 - (5/14)*0.97 = 0.247", w=270)

# Option B: Wind split
rx_b = SW//2 + 20
c.setFillColor(A5); c.setFont("Helvetica-Bold", 8)
c.drawString(rx_b, root_cy - 35, "Split on WIND")
children_b = [("Weak\n[6P,2N]\nH=0.81",  A2, rx_b + 20),
              ("Strong\n[3P,3N]\nH=1.00", A4, rx_b + 110)]
for label, col, cx in children_b:
    arrow_diag(c, root_cx, root_cy - root_h/2, cx + 30, y_child + 20, A5)
    rounded_rect(c, cx, y_child, 60, 28, r=3, fill=CARD, stroke=col, sw=1)
    c.setFillColor(WHITE); c.setFont("Helvetica", 7.5)
    for li, line in enumerate(label.split("\n")):
        tw = c.stringWidth(line, "Helvetica", 7.5)
        c.drawString(cx + 30 - tw/2, y_child + 22 - li*9, line)
math_pill(c, rx_b, y_child - 22, "IG(Wind) = 0.94 - (8/14)*0.81 - (6/14)*1.00 = 0.048", w=240)

# Decision
y2 = y_child - 42
rounded_rect(c, MARGIN_L, y2 - 12, SW - MARGIN_L*2, 16, r=3, fill=HexColor("#0A2A10"), stroke=A2, sw=1.5)
c.setFillColor(A2); c.setFont("Helvetica-Bold", 8.5)
msg = "CHOOSE Weather  (IG=0.247) over Wind (IG=0.048)  — higher gain = better split!"
tw = c.stringWidth(msg, "Helvetica-Bold", 8.5)
c.drawString((SW - tw)/2, y2 - 5, msg)

c.showPage()

# ─── S05: Decision Tree Structure ─────────────────────
new_page(c, A1)
header(c, "Prerequisites — Building a Decision Tree with Information Gain", accent=A1)

# Full tree diagram
def dtree_node(c, cx, cy, lines, w, h, fill=CARD, border=A1, fsize=8):
    rounded_rect(c, cx - w/2, cy - h/2, w, h, r=3, fill=fill, stroke=border, sw=1)
    for i, ln in enumerate(lines):
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold" if i==0 else "Helvetica", fsize)
        tw = c.stringWidth(ln, "Helvetica-Bold" if i==0 else "Helvetica", fsize)
        c.drawString(cx - tw/2, cy + (len(lines)/2 - i)*10 - 3, ln)

root_cx = SW/2; root_cy = SH - TOP_BAR - 45
dtree_node(c, root_cx, root_cy, ["Weather?", "H(S)=0.94"], 120, 28, fill=CARD, border=A1)

# Level 1 children
l1 = [(root_cx - 200, root_cy - 70, "Sunny", ["Humidity?", "H=0.97"], A3),
      (root_cx,        root_cy - 70, "Overcast", ["PLAY", "(pure leaf)"], A2),
      (root_cx + 200,  root_cy - 70, "Rain", ["Wind?", "H=0.97"], A5)]

for cx1, cy1, lab, node_lines, col in l1:
    arrow_diag(c, root_cx, root_cy - 14, cx1, cy1 + 14, col)
    c.setFillColor(col); c.setFont("Helvetica", 7)
    tw = c.stringWidth(lab, "Helvetica", 7)
    c.drawString((root_cx + cx1)/2 - tw/2 + 5, (root_cy + cy1)/2 + 2, lab)
    fill_ = HexColor("#0A2A10") if "PLAY" in node_lines[0] else CARD
    dtree_node(c, cx1, cy1, node_lines, 110, 26, fill=fill_, border=col)

# Level 2 – Humidity children
hum_cx = root_cx - 200; hum_cy = root_cy - 70
l2_sunny = [(hum_cx - 60, hum_cy - 65, "High", ["NO PLAY", "H=0.00"], A4),
            (hum_cx + 60, hum_cy - 65, "Normal", ["PLAY", "H=0.00"], A2)]
for cx2, cy2, lab2, nlines2, col2 in l2_sunny:
    arrow_diag(c, hum_cx, hum_cy - 13, cx2, cy2 + 13, col2)
    c.setFillColor(col2); c.setFont("Helvetica", 7)
    tw = c.stringWidth(lab2, "Helvetica", 7)
    c.drawString((hum_cx + cx2)/2 - tw/2 + 2, (hum_cy + cy2)/2, lab2)
    fill_ = HexColor("#2A0A0A") if "NO" in nlines2[0] else HexColor("#0A2A10")
    dtree_node(c, cx2, cy2, nlines2, 90, 26, fill=fill_, border=col2)

# Level 2 – Wind children
wind_cx = root_cx + 200; wind_cy = root_cy - 70
l2_rain = [(wind_cx - 60, wind_cy - 65, "Weak", ["PLAY", "H=0.00"], A2),
           (wind_cx + 60, wind_cy - 65, "Strong", ["NO PLAY", "H=0.00"], A4)]
for cx2, cy2, lab2, nlines2, col2 in l2_rain:
    arrow_diag(c, wind_cx, wind_cy - 13, cx2, cy2 + 13, col2)
    c.setFillColor(col2); c.setFont("Helvetica", 7)
    tw = c.stringWidth(lab2, "Helvetica", 7)
    c.drawString((wind_cx + cx2)/2 - tw/2 + 2, (wind_cy + cy2)/2, lab2)
    fill_ = HexColor("#0A2A10") if "NO" not in nlines2[0] else HexColor("#2A0A0A")
    dtree_node(c, cx2, cy2, nlines2, 90, 26, fill=fill_, border=col2)

# Algorithm note
by = CONTENT_BOT + 6
rounded_rect(c, MARGIN_L, by, SW - MARGIN_L*2, 22, r=3, fill=CARD, stroke=A1, sw=0.8)
c.setFillColor(A1); c.setFont("Helvetica-Bold", 8)
c.drawString(MARGIN_L + 6, by + 14, "Algorithm:")
c.setFillColor(WHITE); c.setFont("Helvetica", 8)
c.drawString(MARGIN_L + 60, by + 14, "At each node → compute IG for ALL features → pick highest IG → split → recurse until pure or max_depth reached")
c.setFillColor(LGRAY); c.setFont("Helvetica", 7.5)
c.drawString(MARGIN_L + 6, by + 4, "Other metrics exist: Gini Impurity = 1 - SUM(p_i^2),  Gain Ratio, Chi-Square.  Information Gain is the most interpretable.")

c.showPage()

# ─── S06: The Overfitting Problem ─────────────────────
new_page(c, A1)
header(c, "Prerequisites — The Problem: Decision Trees Overfit", accent=A1)

# Show a deep tree memorising noise vs shallow missing patterns
section_label(c, MARGIN_L, CONTENT_TOP - 2, "Problem Setup", A4)

y = CONTENT_TOP - 18
# Two panel layout
pw = (SW - MARGIN_L*2 - 16) / 2
p1x = MARGIN_L; p2x = MARGIN_L + pw + 16

# Panel 1: Deep tree = overfit
rounded_rect(c, p1x, CONTENT_BOT, pw, y - CONTENT_BOT, r=4, fill=CARD, stroke=A4, sw=1.5)
c.setFillColor(A4); c.setFont("Helvetica-Bold", 9)
tw = c.stringWidth("Deep Tree → OVERFITTING", "Helvetica-Bold", 9)
c.drawString(p1x + pw/2 - tw/2, y - 14, "Deep Tree → OVERFITTING")
# draw messy jagged boundary
cl_w = pw - 24; cl_h = 110; cl_x = p1x + 12; cl_y = y - 140
c.setFillColor(HexColor("#1A2A3A"))
c.rect(cl_x, cl_y, cl_w, cl_h, fill=1, stroke=0)
# noisy boundary line (wiggly)
c.setStrokeColor(A4); c.setLineWidth(1.5)
p = c.beginPath(); p.moveTo(cl_x, cl_y + cl_h/2)
for i in range(20):
    xi = cl_x + (i+1) * cl_w / 20
    yi = cl_y + cl_h/2 + random.uniform(-28, 28)
    p.lineTo(xi, yi)
c.drawPath(p, fill=0, stroke=1)
# dots
for _ in range(18):
    dx = cl_x + random.uniform(4, cl_w-4); dy = cl_y + random.uniform(4, cl_h-4)
    col_dot = A1 if random.random() > 0.5 else A3
    c.setFillColor(col_dot); c.circle(dx, dy, 3, fill=1, stroke=0)
c.setFillColor(RSOFT); c.setFont("Helvetica", 7.5)
c.drawString(cl_x, cl_y - 14, "Boundary memorises NOISE")
c.drawString(cl_x, cl_y - 24, "Fails on new data (HIGH VARIANCE)")
# stats
math_pill(c, p1x + 6, CONTENT_BOT + 28, "Train accuracy: ~100%    Test accuracy: ~65%", w=pw - 12, accent=A4)
math_pill(c, p1x + 6, CONTENT_BOT + 8, "Bias: LOW    Variance: HIGH", w=pw - 12, accent=A4)

# Panel 2: Shallow tree = underfit
rounded_rect(c, p2x, CONTENT_BOT, pw, y - CONTENT_BOT, r=4, fill=CARD, stroke=A3, sw=1.5)
c.setFillColor(A3); c.setFont("Helvetica-Bold", 9)
tw = c.stringWidth("Shallow Tree → UNDERFITTING", "Helvetica-Bold", 9)
c.drawString(p2x + pw/2 - tw/2, y - 14, "Shallow Tree → UNDERFITTING")
cl2_x = p2x + 12; cl2_y = cl_y
c.setFillColor(HexColor("#1A2A3A"))
c.rect(cl2_x, cl2_y, cl_w, cl_h, fill=1, stroke=0)
# straight boundary line
c.setStrokeColor(A3); c.setLineWidth(1.5)
c.line(cl2_x, cl2_y + cl_h/2, cl2_x + cl_w, cl2_y + cl_h/2)
for _ in range(18):
    dx = cl2_x + random.uniform(4, cl_w-4); dy = cl2_y + random.uniform(4, cl_h-4)
    col_dot = A1 if random.random() > 0.5 else A3
    c.setFillColor(col_dot); c.circle(dx, dy, 3, fill=1, stroke=0)
c.setFillColor(LGRAY); c.setFont("Helvetica", 7.5)
c.drawString(cl2_x, cl2_y - 14, "Boundary too simple — misses structure")
c.drawString(cl2_x, cl2_y - 24, "Poor on train AND test (HIGH BIAS)")
math_pill(c, p2x + 6, CONTENT_BOT + 28, "Train accuracy: ~72%    Test accuracy: ~70%", w=pw - 12, accent=A3)
math_pill(c, p2x + 6, CONTENT_BOT + 8, "Bias: HIGH    Variance: LOW", w=pw - 12, accent=A3)

c.showPage()

# ─── S07: Bias-Variance Tradeoff ──────────────────────
new_page(c, A1)
header(c, "Prerequisites — The Bias-Variance Tradeoff", accent=A1)
y = CONTENT_TOP

# Left column: formula & explanation
lw = SW//2 - MARGIN_L - 8
section_label(c, MARGIN_L, y - 2, "The Decomposition", A1)
y -= 18
math_pill(c, MARGIN_L, y, "Total Error = Bias^2  +  Variance  +  Irreducible Noise", w=lw)
y -= 22
bullet_list(c, MARGIN_L, y, [
    "Bias^2: error from wrong assumptions (too simple model)",
    "Variance: error from sensitivity to training data fluctuations",
    "Irreducible noise: cannot be eliminated — it's in the data",
    "Bias and Variance TRADE OFF — reducing one tends to increase the other",
    "Ensemble methods BREAK this tradeoff by attacking each separately",
], size=8.5, lh=14, max_w=lw, col=DARK)

# Right column: archer target diagram
rx = SW//2 + 10
section_label(c, rx, CONTENT_TOP - 2, "Target Analogy", A1)
targets = [
    (rx + 75,  CONTENT_TOP - 60, "High Bias\nLow Variance", A3, "shallow tree"),
    (rx + 195, CONTENT_TOP - 60, "Low Bias\nHigh Variance", A4, "deep tree"),
    (rx + 75,  CONTENT_TOP - 160, "Low Bias\nLow Variance\n(GOAL)", A2, "ensemble"),
    (rx + 195, CONTENT_TOP - 160, "High Bias\nHigh Variance\n(Worst)", A4, "bad model"),
]
shots_patterns = [
    [(0,-2),(1,-2),(0,-1),(1,-1),(0,-3)],      # clustered but offset (high bias)
    [(15,-12),(-10,8),(12,10),(-8,-14),(6,2)], # scattered (high variance)
    [(1,-1),(0,1),(-1,0),(1,1),(0,-1)],         # clustered at center
    [(14,8),(-12,-10),(10,-12),(-8,9),(-4,4)], # scattered and offset
]
for i, (tx, ty, label, col, note) in enumerate(targets):
    # rings
    for r_, rc in [(22, HexColor("#3A3A3A")), (15, HexColor("#555")),
                   (9,  HexColor("#777")),  (4,  HexColor("#CC4444"))]:
        c.setFillColor(rc); c.circle(tx, ty, r_, fill=1, stroke=0)
    # shots
    for (dx, dy) in shots_patterns[i]:
        c.setFillColor(YELLOW); c.circle(tx+dx, ty+dy, 2.5, fill=1, stroke=0)
    # label
    c.setFillColor(col); c.setFont("Helvetica-Bold", 7)
    for li, ln in enumerate(label.split("\n")):
        tw = c.stringWidth(ln, "Helvetica-Bold", 7)
        c.drawString(tx - tw/2, ty - 32 - li*9, ln)

c.showPage()

# ─── S08: Ensemble Idea ───────────────────────────────
new_page(c, A1)
header(c, "Prerequisites — The Big Idea: Combine Many Weak Models", accent=A1)

y = CONTENT_TOP - 8
rounded_rect(c, MARGIN_L, y - 28, SW - MARGIN_L*2, 30, r=4, fill=HexColor("#0A2A10"), stroke=A2, sw=1.5)
c.setFillColor(A2); c.setFont("Helvetica-Bold", 11)
msg = "Wisdom of Crowds:  Average of many imperfect predictions beats any single prediction"
tw = c.stringWidth(msg, "Helvetica-Bold", 11)
c.drawString((SW - tw)/2, y - 10, msg)
c.setFillColor(LGRAY); c.setFont("Helvetica", 8)
sub = "Each model has its own error — but errors are RANDOM and cancel each other out when averaged"
tw = c.stringWidth(sub, "Helvetica", 8)
c.drawString((SW - tw)/2, y - 22, sub)
y -= 40

# Visual: 5 models + aggregate
section_label(c, MARGIN_L, y - 2, "Illustration — 5 models each predict a value", A1)
y -= 16
true_val = 42
preds = [39, 45, 41, 44, 38]
errors = [p - true_val for p in preds]
avg_pred = sum(preds) / len(preds)

# Number line
nl_x = MARGIN_L + 20; nl_y = y - 50; nl_w = SW - MARGIN_L*2 - 40
nl_min = 34; nl_max = 50
def val_to_x(v): return nl_x + (v - nl_min) / (nl_max - nl_min) * nl_w

c.setStrokeColor(BORDER); c.setLineWidth(1)
c.line(nl_x, nl_y, nl_x + nl_w, nl_y)
# tick marks
for v in range(nl_min, nl_max+1, 2):
    vx = val_to_x(v)
    c.setStrokeColor(BORDER); c.line(vx, nl_y-3, vx, nl_y+3)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
    c.drawString(vx - 4, nl_y - 12, str(v))

# true value
tvx = val_to_x(true_val)
c.setStrokeColor(A2); c.setLineWidth(1.5)
c.line(tvx, nl_y - 20, tvx, nl_y + 30)
c.setFillColor(A2); c.setFont("Helvetica-Bold", 8)
c.drawString(tvx - 10, nl_y + 33, f"TRUE={true_val}")

# individual predictions
colors_p = [A4, A3, A4, A3, A4]
for i, (p, col) in enumerate(zip(preds, colors_p)):
    px_ = val_to_x(p)
    c.setFillColor(col); c.circle(px_, nl_y + i*6 - 2, 3.5, fill=1, stroke=0)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
    c.drawString(px_ + 5, nl_y + i*6 - 4, f"M{i+1}={p}")

# avg prediction
apx = val_to_x(avg_pred)
c.setFillColor(A1); c.setFont("Helvetica-Bold", 8)
c.drawString(apx - 18, nl_y - 35, f"AVG={avg_pred:.1f}")
c.setStrokeColor(A1); c.setLineWidth(2)
c.line(apx, nl_y - 28, apx, nl_y + 40)

y -= 100
# Key point
rounded_rect(c, MARGIN_L, y - 22, SW - MARGIN_L*2, 24, r=3, fill=CARD, stroke=A1, sw=1)
c.setFillColor(WHITE); c.setFont("Helvetica", 9)
lines_ = [
    "Each model's ERROR is different  (some too high, some too low).",
    "When we AVERAGE, the errors partially cancel → the average is CLOSER to the truth than any individual model.",
]
for i, ln in enumerate(lines_):
    tw = c.stringWidth(ln, "Helvetica", 9)
    c.drawString((SW-tw)/2, y - 8 - i*12, ln)

y -= 36
# Two types of ensembles
tw_box = (SW - MARGIN_L*2 - 12) / 2
for xi, (title, desc, col, fix) in enumerate([
    ("BAGGING", "Parallel training. Each model sees different data. Average/vote. Best for HIGH VARIANCE.", A2, "Fixes: Overfitting"),
    ("BOOSTING", "Sequential training. Each model corrects the previous one's mistakes. Best for HIGH BIAS.", A4, "Fixes: Underfitting"),
]):
    bx = MARGIN_L + xi*(tw_box + 12)
    rounded_rect(c, bx, y - 30, tw_box, 32, r=4, fill=CARD, stroke=col, sw=1.5)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 10); c.drawString(bx + 8, y - 8, title)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7.5)
    # wrap text
    words = desc.split(); line = ""; ly_ = y - 20
    for word in words:
        test = (line+" "+word).strip()
        if c.stringWidth(test,"Helvetica",7.5) < tw_box-16: line=test
        else:
            c.drawString(bx+8, ly_, line); ly_-=10; line=word
    if line: c.drawString(bx+8, ly_, line)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 8)
    c.drawString(bx + 8, y - 28, fix)

c.showPage()

# ═══════════════════════════════════════════════════════
# SECTION 02 – BAGGING
# ═══════════════════════════════════════════════════════

new_page(c, A2)
header(c, "Section 02 — Bagging: Bootstrap Aggregation", accent=A2)
# big section display
c.setFillColor(A2)
c.rect(0, 0, 10, SH - TOP_BAR, fill=1, stroke=0)
c.setFillColor(HexColor("#162A1A"))
c.setFont("Helvetica-Bold", 100)
c.drawString(20, SH//2 - 55, "02")
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 26)
c.drawString(20, SH//2 - 4, "Bagging")
c.setFillColor(LGRAY); c.setFont("Helvetica", 11)
c.drawString(20, SH//2 - 22, "Bootstrap Aggregation — Killing Variance One Tree at a Time")
c.showPage()

# ─── Bagging Diagram 1: The PROBLEM ───────────────────
new_page(c, A2)
header(c, "Bagging — Step 1: The Problem (One Deep Tree Overfits)", accent=A2)

y = CONTENT_TOP - 10
section_label(c, MARGIN_L, y, "PROBLEM DIAGRAM", A4)
y -= 18

# Show one training set → one deep tree → wrong on test
bw3 = (SW - MARGIN_L*2 - 30) / 3
# Box 1: Training data
b1x = MARGIN_L; b1y = y - 90
rounded_rect(c, b1x, b1y, bw3, 90, r=4, fill=CARD, stroke=A1, sw=1)
c.setFillColor(A1); c.setFont("Helvetica-Bold", 8)
tw = c.stringWidth("Training Data (N=10)", "Helvetica-Bold", 8)
c.drawString(b1x + bw3/2 - tw/2, b1y + 82, "Training Data (N=10)")
# draw 10 colored dots in a scatter
random.seed(11)
for i in range(10):
    dx = b1x + 15 + random.random()*(bw3-30)
    dy = b1y + 12 + random.random()*60
    col_d = A1 if i < 6 else A3
    c.setFillColor(col_d); c.circle(dx, dy, 4, fill=1, stroke=0)
# Label noise
c.setFillColor(A4); c.setFont("Helvetica", 7)
c.drawString(b1x + 4, b1y + 4, "Noise in data!")

arrow_h(c, b1x + bw3 + 2, b1y + 45, b1x + bw3 + 14, b1y + 45, A2)

# Box 2: One deep tree
b2x = b1x + bw3 + 16
rounded_rect(c, b2x, b1y, bw3, 90, r=4, fill=CARD, stroke=A4, sw=1.5)
c.setFillColor(A4); c.setFont("Helvetica-Bold", 8)
tw = c.stringWidth("One Deep Tree (max_depth=10)", "Helvetica-Bold", 8)
c.drawString(b2x + bw3/2 - tw/2, b1y + 82, "One Deep Tree (max_depth=10)")
# draw jagged over-fitted boundary in this box
area_x = b2x + 8; area_y = b1y + 10; area_w = bw3 - 16; area_h = 65
c.setFillColor(HexColor("#1A2030")); c.rect(area_x, area_y, area_w, area_h, fill=1, stroke=0)
c.setStrokeColor(A4); c.setLineWidth(1.5)
p = c.beginPath(); p.moveTo(area_x, area_y + area_h/2)
random.seed(22)
for i in range(12):
    xi = area_x + (i+1)*area_w/12
    yi = area_y + area_h/2 + random.uniform(-25, 25)
    p.lineTo(xi, yi)
c.drawPath(p, fill=0, stroke=1)
c.setFillColor(RSOFT); c.setFont("Helvetica-Bold", 7)
c.drawString(b2x + 4, b1y + 4, "Memorised noise!")

arrow_h(c, b2x + bw3 + 2, b1y + 45, b2x + bw3 + 14, b1y + 45, A2)

# Box 3: Test performance
b3x = b2x + bw3 + 16
rounded_rect(c, b3x, b1y, bw3, 90, r=4, fill=CARD, stroke=A4, sw=1.5)
c.setFillColor(A4); c.setFont("Helvetica-Bold", 8)
tw = c.stringWidth("Test Performance", "Helvetica-Bold", 8)
c.drawString(b3x + bw3/2 - tw/2, b1y + 82, "Test Performance")
math_pill(c, b3x + 6, b1y + 62, "Train Acc: 100%", w=bw3-12, accent=A2)
math_pill(c, b3x + 6, b1y + 42, "Test Acc:  62%", w=bw3-12, accent=A4)
math_pill(c, b3x + 6, b1y + 22, "Variance: HIGH", w=bw3-12, accent=A4)
c.setFillColor(A4); c.setFont("Helvetica-Bold", 8)
c.drawString(b3x + 6, b1y + 6, "BAD GENERALISATION!")

# Now show what happens if we train on different data
y = b1y - 28
rounded_rect(c, MARGIN_L, y - 22, SW - MARGIN_L*2, 24, r=3, fill=HexColor("#2A0A0A"), stroke=A4, sw=1)
c.setFillColor(WHITE); c.setFont("Helvetica", 9)
msg = "Key observation: train same deep tree on slightly different data → COMPLETELY different boundaries!  The model is highly unstable."
tw = c.stringWidth(msg, "Helvetica", 9)
c.drawString((SW-tw)/2, y - 14, msg)

# Mini illustration: 3 different training sets → 3 different boundaries
y -= 38
mini_w = (SW - MARGIN_L*2 - 20) / 3
mini_h = 55
for j in range(3):
    mx = MARGIN_L + j*(mini_w + 10)
    my = y - mini_h
    rounded_rect(c, mx, my, mini_w, mini_h, r=3, fill=CARD, stroke=A3, sw=0.8)
    c.setFillColor(A3); c.setFont("Helvetica-Bold", 7)
    tw = c.stringWidth(f"Training Set {j+1}", "Helvetica-Bold", 7)
    c.drawString(mx + mini_w/2 - tw/2, my + mini_h - 10, f"Training Set {j+1}")
    inner_x = mx + 6; inner_y = my + 8; inner_w = mini_w - 12; inner_h = mini_h - 22
    c.setFillColor(HexColor("#1A2030"))
    c.rect(inner_x, inner_y, inner_w, inner_h, fill=1, stroke=0)
    c.setStrokeColor(A4); c.setLineWidth(1.2)
    p = c.beginPath(); p.moveTo(inner_x, inner_y + inner_h/2)
    random.seed(j*5+3)
    for i in range(8):
        xi = inner_x + (i+1)*inner_w/8
        yi = inner_y + inner_h/2 + random.uniform(-inner_h*0.45, inner_h*0.45)
        p.lineTo(xi, yi)
    c.drawPath(p, fill=0, stroke=1)
    c.setFillColor(RSOFT); c.setFont("Helvetica", 6.5)
    c.drawString(mx + 4, my + 2, "Different boundary each time!")

c.showPage()

# ─── Bagging Diagram 2: Bootstrap Sampling ────────────
new_page(c, A2)
header(c, "Bagging — Step 2: Bootstrap Sampling (The Fix Begins)", accent=A2)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "SOLUTION STEP 2A — Create B different training sets from ONE dataset", A2)
y -= 18

# Original dataset row
rounded_rect(c, MARGIN_L, y - 26, SW - MARGIN_L*2, 26, r=4, fill=CARD, stroke=A1, sw=1.5)
c.setFillColor(A1); c.setFont("Helvetica-Bold", 9)
c.drawString(MARGIN_L + 8, y - 10, "Original Dataset (N = 8 samples)")
samples_orig = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
sx = MARGIN_L + 110
for si, s in enumerate(samples_orig):
    c.setFillColor(A1)
    c.roundRect(sx + si*38, y - 22, 32, 14, 2, fill=1, stroke=0)
    c.setFillColor(DARK); c.setFont("Helvetica-Bold", 8)
    tw = c.stringWidth(s, "Helvetica-Bold", 8)
    c.drawString(sx + si*38 + 16 - tw/2, y - 13, s)
y -= 38

# Three bootstrap arrows + sets
bootstrap_sets = [
    ["S1","S1","S3","S5","S5","S7","S7","S8"],
    ["S2","S2","S3","S4","S6","S6","S7","S8"],
    ["S1","S3","S3","S4","S4","S5","S7","S8"],
]
bw3 = (SW - MARGIN_L*2 - 20) / 3
for j, bset in enumerate(bootstrap_sets):
    bx = MARGIN_L + j*(bw3 + 10)
    # arrow from original down
    arrow_v(c, bx + bw3/2, y - 2, y - 30, A2)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
    c.drawString(bx + bw3/2 + 4, y - 18, "sample w/")
    c.drawString(bx + bw3/2 + 4, y - 26, "replacement")
    by = y - 72
    rounded_rect(c, bx, by, bw3, 40, r=3, fill=HexColor("#1A3A1A"), stroke=A2, sw=1)
    c.setFillColor(A2); c.setFont("Helvetica-Bold", 8)
    tw = c.stringWidth(f"Bootstrap {j+1}", "Helvetica-Bold", 8)
    c.drawString(bx + bw3/2 - tw/2, by + 32, f"Bootstrap {j+1}")
    for si2, s in enumerate(bset[:8]):
        is_dup = bset[:si2].count(s) > 0
        col_s = A3 if is_dup else A2
        sx2 = bx + 4 + si2*((bw3-8)/8)
        c.setFillColor(col_s)
        c.roundRect(sx2, by + 4, (bw3-8)/8 - 2, 20, 2, fill=1, stroke=0)
        c.setFillColor(DARK); c.setFont("Helvetica-Bold", 6.5)
        tw2 = c.stringWidth(s, "Helvetica-Bold", 6.5)
        c.drawString(sx2 + ((bw3-8)/8-2)/2 - tw2/2, by + 11, s)

y -= 84
# Legend
c.setFillColor(A3); c.roundRect(MARGIN_L + 4, y, 12, 9, 1, fill=1, stroke=0)
c.setFillColor(LGRAY); c.setFont("Helvetica", 7.5)
c.drawString(MARGIN_L + 20, y + 2, "= duplicate sample (appears more than once)")
c.setFillColor(A2); c.roundRect(MARGIN_L + 4 + 160, y, 12, 9, 1, fill=1, stroke=0)
c.drawString(MARGIN_L + 20 + 160, y + 2, "= unique sample")

y -= 18
math_pill(c, MARGIN_L, y, "Each bootstrap contains ~63% unique samples.  ~37% are left out (Out-Of-Bag = FREE validation!)", w=SW - MARGIN_L*2 - 10, accent=A2)
y -= 24

# Key insight box
rounded_rect(c, MARGIN_L, y - 26, SW - MARGIN_L*2, 28, r=3, fill=HexColor("#0A2A10"), stroke=A2, sw=1.5)
c.setFillColor(WHITE); c.setFont("Helvetica", 9)
msg1 = "Each bootstrap set is DIFFERENT  →  each tree trained on it sees slightly different data  →  each tree makes DIFFERENT errors"
msg2 = "→  when we average the predictions, those different errors will CANCEL OUT  →  much lower variance!"
for i, msg in enumerate([msg1, msg2]):
    tw = c.stringWidth(msg, "Helvetica", 9)
    c.drawString((SW-tw)/2, y - 10 - i*13, msg)

c.showPage()

# ─── Bagging Diagram 3: Train Trees + Aggregate ───────
new_page(c, A2)
header(c, "Bagging — Step 3 & 4: Train Trees + Aggregate Predictions", accent=A2)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "SOLUTION STEP 2B — Train one tree per bootstrap, then combine", A2)
y -= 16

# Row of bootstrap datasets
bw = (SW - MARGIN_L*2 - 30) / 4
data_y = y - 30
tree_y = y - 90
agg_y = y - 145
pred_y = y - 185

for j in range(4):
    bx = MARGIN_L + j*(bw + 10)
    cx = bx + bw/2

    # Dataset box
    rounded_rect(c, bx, data_y, bw, 28, r=3, fill=CARD, stroke=A1, sw=0.8)
    c.setFillColor(A1); c.setFont("Helvetica-Bold", 7.5)
    tw = c.stringWidth(f"Bootstrap D{j+1}", "Helvetica-Bold", 7.5)
    c.drawString(cx - tw/2, data_y + 19, f"Bootstrap D{j+1}")
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
    tw = c.stringWidth("(N samples w/ replacement)", "Helvetica", 7)
    c.drawString(cx - tw/2, data_y + 7, "(N samples w/ replacement)")

    # Arrow down to tree
    arrow_v(c, cx, data_y - 1, tree_y + 35, A2)

    # Tree box
    rounded_rect(c, bx, tree_y, bw, 33, r=3, fill=HexColor("#1A3A1A"), stroke=A2, sw=1)
    c.setFillColor(A2); c.setFont("Helvetica-Bold", 7.5)
    tw = c.stringWidth(f"Tree T{j+1}", "Helvetica-Bold", 7.5)
    c.drawString(cx - tw/2, tree_y + 24, f"Tree T{j+1}")
    # mini tree icon
    tc = cx; ty_ = tree_y + 14
    c.setStrokeColor(A2); c.setLineWidth(0.8)
    c.line(tc, ty_, tc - 14, ty_ - 10); c.line(tc, ty_, tc + 14, ty_ - 10)
    c.line(tc-14, ty_-10, tc-22, ty_-18); c.line(tc-14, ty_-10, tc-6, ty_-18)
    c.line(tc+14, ty_-10, tc+6, ty_-18); c.line(tc+14, ty_-10, tc+22, ty_-18)
    for lx2, ly2 in [(tc-22,ty_-18),(tc-6,ty_-18),(tc+6,ty_-18),(tc+22,ty_-18)]:
        c.setFillColor(A2); c.circle(lx2, ly2, 2.5, fill=1, stroke=0)

    # Arrow to aggregator
    arrow_v(c, cx, tree_y - 1, agg_y + 14, A2)

    # individual prediction
    pred_labels = [["Class A", A2], ["Class A", A2], ["Class B", A4], ["Class A", A2]]
    pl, pc = pred_labels[j]
    rounded_rect(c, bx, agg_y, bw, 14, r=2, fill=CARD, stroke=pc, sw=0.8)
    c.setFillColor(pc); c.setFont("Helvetica-Bold", 7)
    tw = c.stringWidth(f"Predicts: {pl}", "Helvetica-Bold", 7)
    c.drawString(cx - tw/2, agg_y + 4, f"Predicts: {pl}")

# Aggregator box
all_cx = SW/2
agg_box_y = agg_y - 30
rounded_rect(c, MARGIN_L + 40, agg_box_y, SW - MARGIN_L*2 - 80, 26, r=4, fill=HexColor("#1A2E3A"), stroke=A1, sw=1.5)
c.setFillColor(A1); c.setFont("Helvetica-Bold", 9)
tw = c.stringWidth("AGGREGATOR", "Helvetica-Bold", 9)
c.drawString(all_cx - tw/2, agg_box_y + 17, "AGGREGATOR")
c.setFillColor(LGRAY); c.setFont("Helvetica", 7.5)
tw = c.stringWidth("Classification: Majority Vote  |  Regression: Average", "Helvetica", 7.5)
c.drawString(all_cx - tw/2, agg_box_y + 5, "Classification: Majority Vote  |  Regression: Average")
for j in range(4):
    cx = MARGIN_L + j*(bw + 10) + bw/2
    arrow_diag(c, cx, agg_y - 1, all_cx, agg_box_y + 26, A1)

# Final prediction
fp_y = agg_box_y - 28
arrow_v(c, all_cx, agg_box_y, fp_y + 16, A2)
rounded_rect(c, all_cx - 120, fp_y, 240, 18, r=3, fill=HexColor("#0A2A10"), stroke=A2, sw=1.5)
c.setFillColor(A2); c.setFont("Helvetica-Bold", 9)
tw = c.stringWidth("Final Prediction: Class A  (3 out of 4 votes)", "Helvetica-Bold", 9)
c.drawString(all_cx - tw/2, fp_y + 6, "Final Prediction: Class A  (3 out of 4 votes)")

# Math
math_pill(c, MARGIN_L, CONTENT_BOT + 6, "f_bag(x) = majority_vote{T1(x), T2(x), ..., TB(x)}   or   (1/B)*SUM T_b(x) for regression", w=SW-MARGIN_L*2-10, accent=A2)

c.showPage()

# ─── Bagging Diagram 4: WHY variance drops ────────────
new_page(c, A2)
header(c, "Bagging — Why Variance DROPS: The Math Explained Visually", accent=A2)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "PROOF — Why does averaging reduce variance?", A2)
y -= 18

# Show error cancellation visually
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 9)
c.drawString(MARGIN_L, y, "Each tree's prediction = truth + its own random error:")
y -= 14
math_pill(c, MARGIN_L, y, "T_b(x) = f*(x) + epsilon_b     where epsilon_b is random error with mean=0", w=SW-MARGIN_L*2-10, accent=A3)
y -= 22
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 9)
c.drawString(MARGIN_L, y, "When we AVERAGE B trees:")
y -= 14
math_pill(c, MARGIN_L, y, "f_bag(x) = (1/B) * SUM T_b(x) = f*(x) + (1/B)*SUM epsilon_b", w=SW-MARGIN_L*2-10, accent=A2)
y -= 22

# Variance formula
math_pill(c, MARGIN_L, y, "Var( f_bag ) = (1/B^2) * SUM Var(epsilon_b)  =  sigma^2 / B   (if trees independent)", w=SW-MARGIN_L*2-10, accent=A2)
y -= 24
c.setFillColor(A2); c.setFont("Helvetica-Bold", 9)
c.drawString(MARGIN_L, y, "Conclusion:  More trees → Variance goes down by factor of B  →  LESS OVERFITTING!")
y -= 22

# Visual bar chart of variance vs B
section_label(c, MARGIN_L, y - 2, "Variance Reduction as B increases", A2)
y -= 18
chart_x = MARGIN_L + 20; chart_y = y - 90; chart_w = 280; chart_h = 85
c.setFillColor(CARD); c.rect(chart_x, chart_y, chart_w, chart_h, fill=1, stroke=0)
# axes
c.setStrokeColor(BORDER); c.setLineWidth(0.8)
c.line(chart_x, chart_y, chart_x, chart_y + chart_h)
c.line(chart_x, chart_y, chart_x + chart_w, chart_y)
# variance curve
B_vals = [1, 5, 10, 20, 50, 100]
var_vals = [1.0, 0.2, 0.10, 0.05, 0.02, 0.01]
pts = [(chart_x + (i/(len(B_vals)-1))*chart_w, chart_y + (1-v)*chart_h*0.9) for i, v in enumerate(var_vals)]
c.setStrokeColor(A2); c.setLineWidth(2)
p_ = c.beginPath(); p_.moveTo(*pts[0])
for pt in pts[1:]: p_.lineTo(*pt)
c.drawPath(p_, fill=0, stroke=1)
for pt in pts:
    c.setFillColor(A2); c.circle(pt[0], pt[1], 3, fill=1, stroke=0)
# labels
c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
for i, (B, pt) in enumerate(zip(B_vals, pts)):
    c.drawString(pt[0]-5, chart_y-10, str(B))
c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
c.drawString(chart_x + chart_w/2 - 10, chart_y - 18, "Number of Trees (B)")
# y-axis label
c.saveState(); c.translate(chart_x - 14, chart_y + chart_h/2); c.rotate(90)
c.drawString(-18, 0, "Variance"); c.restoreState()

# Right side: bias unchanged
rx = MARGIN_L + 330
rounded_rect(c, rx, y - 105, SW - rx - MARGIN_R, 110, r=4, fill=CARD, stroke=A3, sw=1)
c.setFillColor(A3); c.setFont("Helvetica-Bold", 9)
tw = c.stringWidth("What about BIAS?", "Helvetica-Bold", 9)
c.drawString(rx + (SW-rx-MARGIN_R)/2 - tw/2, y - 14, "What about BIAS?")
c.setFillColor(WHITE); c.setFont("Helvetica", 8.5)
lines_b = [
    "Bias stays the SAME.",
    "Averaging unbiased predictions",
    "gives an unbiased average.",
    "",
    "Bagging does NOT fix underfitting.",
    "Use Boosting for that!",
]
for li, ln in enumerate(lines_b):
    c.drawString(rx + 8, y - 30 - li*11, ln)

# Summary box
math_pill(c, MARGIN_L, CONTENT_BOT + 6, "Bagging  solves OVERFITTING  (High Variance).    It does NOT reduce Bias.", w=SW-MARGIN_L*2-10, accent=A2)
c.showPage()

# ═══════════════════════════════════════════════════════
# SECTION 03 – RANDOM FOREST
# ═══════════════════════════════════════════════════════

new_page(c, A3)
header(c, "Section 03 — Random Forest", accent=A3)
c.setFillColor(A3); c.rect(0, 0, 10, SH - TOP_BAR, fill=1, stroke=0)
c.setFillColor(HexColor("#2A1A0A")); c.setFont("Helvetica-Bold", 100)
c.drawString(20, SH//2 - 55, "03")
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 26)
c.drawString(20, SH//2 - 4, "Random Forest")
c.setFillColor(LGRAY); c.setFont("Helvetica", 11)
c.drawString(20, SH//2 - 22, "Bagging + Feature Randomness = Decorrelated Trees")
c.showPage()

# ─── RF Problem: Correlated Trees ─────────────────────
new_page(c, A3)
header(c, "Random Forest — The Problem with Plain Bagging: Correlated Trees", accent=A3)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "NEW PROBLEM — Bagging trees can be correlated!", A4)
y -= 18

c.setFillColor(DARK); c.setFont("Helvetica", 9)
c.drawString(MARGIN_L, y, "Even with bootstrap sampling, all trees see the same pool of features.")
y -= 12
c.drawString(MARGIN_L, y, "If one feature is very strong (e.g. 'Income'), ALL trees will split on it first → similar trees → correlated errors!")
y -= 12
c.setFillColor(A4); c.setFont("Helvetica-Bold", 8.5)
c.drawString(MARGIN_L, y, "Correlated errors do NOT cancel out when averaged.  Variance reduction is limited!")
y -= 22

# Visual: 3 identical-looking trees
section_label(c, MARGIN_L, y - 2, "Illustration — All trees choose the same dominant feature", A4)
y -= 16
tw_box = (SW - MARGIN_L*2 - 20) / 3
for j in range(3):
    bx = MARGIN_L + j*(tw_box + 10); by = y - 80
    rounded_rect(c, bx, by, tw_box, 80, r=3, fill=CARD, stroke=A4, sw=1)
    cx = bx + tw_box/2
    c.setFillColor(A4); c.setFont("Helvetica-Bold", 7.5)
    tw = c.stringWidth(f"Tree {j+1} (different bootstrap)", "Helvetica-Bold", 7.5)
    c.drawString(cx - tw/2, by + 72, f"Tree {j+1} (different bootstrap)")
    # root node always splits on Income
    label_box(c, cx, by + 54, tw_box-20, 14, "Income > 50k?", fill=HexColor("#3A1A1A"), border=A4, fsize=7)
    label_box(c, cx - 35, by + 34, 60, 12, "Income > 80k?", fill=HexColor("#3A1A1A"), border=A4, fsize=7)
    label_box(c, cx + 35, by + 34, 60, 12, "Income > 30k?", fill=HexColor("#3A1A1A"), border=A4, fsize=7)
    arrow_diag(c, cx-8, by+47, cx-35, by+40, A4, lw=0.8)
    arrow_diag(c, cx+8, by+47, cx+35, by+40, A4, lw=0.8)
    c.setFillColor(RSOFT); c.setFont("Helvetica", 7)
    tw = c.stringWidth("All start with Income!", "Helvetica", 7)
    c.drawString(cx - tw/2, by + 6, "All start with Income!")
    if j < 2:
        arrow_h(c, bx + tw_box + 2, by + 40, bx + tw_box + 10, by + 40, LGRAY)

# Correlation consequence
c.setFillColor(A4); c.setFont("Helvetica-Bold", 8.5)
msg_c = "Because trees are similar → their errors are correlated ρ → Var(average) = ρ*σ² + (1-ρ)*σ²/B  → floor is ρ*σ² even as B→∞"
y2 = y - 90
math_pill(c, MARGIN_L, y2, msg_c, w=SW-MARGIN_L*2-10, accent=A4)

y2 -= 24
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 9)
c.drawString(MARGIN_L, y2, "Solution: FORCE trees to be different by randomising which features they can use at each split!")
c.showPage()

# ─── RF Fix: Feature Randomness ───────────────────────
new_page(c, A3)
header(c, "Random Forest — The Fix: Random Feature Subsets at Every Split", accent=A3)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "SOLUTION — At each split, only consider m features chosen at random", A3)
y -= 16

math_pill(c, MARGIN_L, y, "m = sqrt(p) for classification    m = p/3 for regression     p = total number of features", w=SW-MARGIN_L*2-10, accent=A3)
y -= 22

# Show feature selection process
c.setFillColor(DARK); c.setFont("Helvetica", 8.5)
c.drawString(MARGIN_L, y, "Suppose we have 9 features total (p=9).  At each node, randomly pick m=3 features.  Build the split using only those 3.")
y -= 22

# Three trees, each with different feature subsets
tw_3 = (SW - MARGIN_L*2 - 20) / 3
all_feats = ["F1","F2","F3","F4","F5","F6","F7","F8","F9"]
feat_colors = [A1,A2,A3,A4,A5,A1,A2,A3,A4]
random.seed(42)
for j in range(3):
    bx = MARGIN_L + j*(tw_3 + 10)
    by = y - 130
    rounded_rect(c, bx, by, tw_3, 130, r=3, fill=CARD, stroke=A3, sw=1)
    cx = bx + tw_3/2
    c.setFillColor(A3); c.setFont("Helvetica-Bold", 7.5)
    tw = c.stringWidth(f"Tree {j+1}", "Helvetica-Bold", 7.5)
    c.drawString(cx - tw/2, by + 122, f"Tree {j+1}")

    # All features shown at each level
    for level in range(2):
        row_y = by + 95 - level*50
        c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
        label = "Node features available:" if level == 0 else "Child node features:"
        c.drawString(bx + 4, row_y + 8, label)

        chosen = random.sample(range(9), 3)
        for fi in range(9):
            fx = bx + 5 + fi * (tw_3-10)/9
            fy = row_y - 4
            col_f = feat_colors[fi] if fi in chosen else HexColor("#2A2A3A")
            c.setFillColor(col_f)
            c.roundRect(fx, fy, (tw_3-10)/9 - 2, 10, 1, fill=1, stroke=0)
            c.setFillColor(WHITE if fi in chosen else DGRAY)
            c.setFont("Helvetica-Bold", 5.5)
            tw2 = c.stringWidth(all_feats[fi], "Helvetica-Bold", 5.5)
            c.drawString(fx + (tw_3-10)/9/2 - tw2/2, fy + 2.5, all_feats[fi])

        # best split from chosen
        best_feat = all_feats[chosen[0]]
        c.setFillColor(A3); c.setFont("Helvetica-Bold", 7)
        c.drawString(bx + 4, row_y - 18, f"  → Best split: {best_feat}")

c.setFillColor(A3); c.setFont("Helvetica-Bold", 8.5)
y -= 145
c.drawString(MARGIN_L, y, "Each tree chooses from a DIFFERENT random subset → different root splits → DECORRELATED trees!")
y -= 14
c.setFillColor(LGRAY); c.setFont("Helvetica", 8)
c.drawString(MARGIN_L, y, "Even if Income is the globally best feature, Tree 2 might not even see it → forced to find the second-best split!")
y -= 22

# The correlation formula
math_pill(c, MARGIN_L, y, "Var(RF) = rho*sigma^2  +  (1-rho)*sigma^2/B     Lower rho = lower variance floor!", w=SW-MARGIN_L*2-10, accent=A3)
y -= 22
math_pill(c, MARGIN_L, y, "Random forests lower rho by forcing diverse splits → variance drops FURTHER than plain Bagging!", w=SW-MARGIN_L*2-10, accent=A2)
c.showPage()

# ─── RF Full Pipeline ──────────────────────────────────
new_page(c, A3)
header(c, "Random Forest — Complete Algorithm Diagram", accent=A3)

y = CONTENT_TOP - 6
# 4-step pipeline across the slide
steps_rf = [
    ("1. Bootstrap", "Sample N rows\nwith replacement", A1),
    ("2. Grow Tree", "At each split, pick\nrandom m features\nthen best IG split", A3),
    ("3. Full Depth", "No pruning —\ngrow until pure\n(max IG = 0)", A2),
    ("4. Vote/Avg", "Majority vote\n(class) or mean\n(regression)", A2),
]
step_w = (SW - MARGIN_L*2 - 30) / len(steps_rf)
sx = MARGIN_L
for i, (stitle, sdesc, col) in enumerate(steps_rf):
    rounded_rect(c, sx, y - 60, step_w, 60, r=4, fill=CARD, stroke=col, sw=1.5)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 8.5)
    tw = c.stringWidth(stitle, "Helvetica-Bold", 8.5)
    c.drawString(sx + step_w/2 - tw/2, y - 12, stitle)
    c.setFillColor(WHITE); c.setFont("Helvetica", 7.5)
    for li, ln in enumerate(sdesc.split("\n")):
        tw = c.stringWidth(ln, "Helvetica", 7.5)
        c.drawString(sx + step_w/2 - tw/2, y - 28 - li*10, ln)
    if i < len(steps_rf)-1:
        arrow_h(c, sx + step_w + 1, y - 30, sx + step_w + 9, y - 30, col)
    sx += step_w + 10

y -= 76

# Repeat B times label
c.setStrokeColor(LGRAY); c.setLineWidth(0.5); c.setDash([3,3])
c.rect(MARGIN_L, y, SW - MARGIN_L*2, 14, fill=0, stroke=1)
c.setDash()
c.setFillColor(LGRAY); c.setFont("Helvetica", 7.5)
tw = c.stringWidth("↑ Repeat for B trees (e.g. B=100) ↑", "Helvetica", 7.5)
c.drawString((SW-tw)/2, y + 4, "↑ Repeat for B trees (e.g. B=100) ↑")
y -= 26

# Show 3 trees side by side then aggregate
section_label(c, MARGIN_L, y - 2, "Full illustration with 3 trees", A3)
y -= 14
tree_bw = (SW - MARGIN_L*2 - 20) / 3
for j in range(3):
    bx = MARGIN_L + j*(tree_bw + 10)
    by = y - 70
    rounded_rect(c, bx, by, tree_bw, 70, r=3, fill=CARD, stroke=A3, sw=1)
    cx = bx + tree_bw/2
    c.setFillColor(A3); c.setFont("Helvetica-Bold", 7.5)
    tw = c.stringWidth(f"Tree {j+1}  [IG-based splits]", "Helvetica-Bold", 7.5)
    c.drawString(cx - tw/2, by + 62, f"Tree {j+1}  [IG-based splits]")
    # mini tree
    tc2 = cx; ty2 = by + 48
    c.setStrokeColor(A3); c.setLineWidth(0.8)
    c.line(tc2, ty2, tc2-18, ty2-14); c.line(tc2, ty2, tc2+18, ty2-14)
    c.line(tc2-18, ty2-14, tc2-26, ty2-24); c.line(tc2-18, ty2-14, tc2-10, ty2-24)
    c.line(tc2+18, ty2-14, tc2+10, ty2-24); c.line(tc2+18, ty2-14, tc2+26, ty2-24)
    for lx3, ly3 in [(tc2-26,ty2-24),(tc2-10,ty2-24),(tc2+10,ty2-24),(tc2+26,ty2-24)]:
        c.setFillColor(A2); c.circle(lx3, ly3, 3, fill=1, stroke=0)
    label_box(c, cx, by + 48, 50, 10, f"IG split #{j+1}", fill=HexColor("#1A3A1A"), border=A3, fsize=7)
    pred_vals = ["Class A", "Class A", "Class B"]
    p_col = A2 if "A" in pred_vals[j] else A4
    rounded_rect(c, bx + 8, by + 4, tree_bw - 16, 14, r=2, fill=CARD, stroke=p_col, sw=1)
    c.setFillColor(p_col); c.setFont("Helvetica-Bold", 7.5)
    tw = c.stringWidth(f"Pred: {pred_vals[j]}", "Helvetica-Bold", 7.5)
    c.drawString(cx - tw/2, by + 8, f"Pred: {pred_vals[j]}")

# Aggregate box
y -= 82
all_cx2 = SW/2
rounded_rect(c, MARGIN_L+60, y-18, SW-MARGIN_L*2-120, 20, r=3, fill=HexColor("#0A2A10"), stroke=A2, sw=1.5)
c.setFillColor(A2); c.setFont("Helvetica-Bold", 9)
tw = c.stringWidth("MAJORITY VOTE  →  Final: Class A  (2/3 trees agree)", "Helvetica-Bold", 9)
c.drawString((SW-tw)/2, y - 10, "MAJORITY VOTE  →  Final: Class A  (2/3 trees agree)")
for j in range(3):
    cx_t = MARGIN_L + j*(tree_bw+10) + tree_bw/2
    arrow_diag(c, cx_t, y+82-82, all_cx2, y-1, A2)

math_pill(c, MARGIN_L, CONTENT_BOT + 4, "OOB Score: each sample predicted by trees that did NOT train on it → free cross-validation accuracy!", w=SW-MARGIN_L*2-10, accent=A3)
c.showPage()

# ═══════════════════════════════════════════════════════
# SECTION 04 – BOOSTING
# ═══════════════════════════════════════════════════════
new_page(c, A4)
header(c, "Section 04 — Boosting", accent=A4)
c.setFillColor(A4); c.rect(0, 0, 10, SH - TOP_BAR, fill=1, stroke=0)
c.setFillColor(HexColor("#2A0A0A")); c.setFont("Helvetica-Bold", 100)
c.drawString(20, SH//2 - 55, "04")
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 26)
c.drawString(20, SH//2 - 4, "Boosting")
c.setFillColor(LGRAY); c.setFont("Helvetica", 11)
c.drawString(20, SH//2 - 22, "Sequential Error Correction — Fighting Bias, Round by Round")
c.showPage()

# ─── Boosting: The Problem ────────────────────────────
new_page(c, A4)
header(c, "Boosting — The Problem: Bagging Can't Fix High Bias", accent=A4)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "THE PROBLEM — Shallow trees (stumps) underfit. Averaging them doesn't help.", A4)
y -= 18

# Show 3 shallow stumps and their average still underfits
c.setFillColor(DARK); c.setFont("Helvetica", 8.5)
c.drawString(MARGIN_L, y, "A shallow 1-level tree (stump) can only learn one simple rule.  It misses most patterns (HIGH BIAS).")
y -= 12
c.drawString(MARGIN_L, y, "If we bag 100 shallow stumps... we just average 100 simple rules → still a simple rule.  BIAS IS NOT REDUCED.")
y -= 20

# Visual: 3 stumps on same data + their average
bw4 = (SW - MARGIN_L*2 - 20) / 3
data_pts_x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
data_pts_y = [0.2,0.7,0.3,0.8,0.2,0.9,0.15,0.75,0.35]

for j in range(3):
    bx = MARGIN_L + j*(bw4 + 10); by = y - 90
    rounded_rect(c, bx, by, bw4, 90, r=3, fill=CARD, stroke=A4, sw=1)
    area_x = bx+8; area_y = by+18; area_w = bw4-16; area_h = 62
    c.setFillColor(HexColor("#1A1A2A")); c.rect(area_x, area_y, area_w, area_h, fill=1, stroke=0)
    # data points
    for xi_, yi_ in zip(data_pts_x, data_pts_y):
        px_ = area_x + xi_ * area_w; py_ = area_y + yi_ * area_h
        c.setFillColor(A1 if yi_ > 0.5 else A3); c.circle(px_, py_, 3, fill=1, stroke=0)
    # stump: single horizontal cut
    cuts = [0.5, 0.5, 0.5]
    cut_y2 = area_y + cuts[j]*area_h
    c.setStrokeColor(A4); c.setLineWidth(1.5)
    c.line(area_x, cut_y2, area_x+area_w, cut_y2)
    c.setFillColor(A3); c.setFont("Helvetica-Bold", 7)
    tw = c.stringWidth(f"Stump {j+1}: y > 0.5?", "Helvetica-Bold", 7)
    c.drawString(bx + bw4/2 - tw/2, by + 12, f"Stump {j+1}: y > 0.5?")
    c.setFillColor(RSOFT); c.setFont("Helvetica", 7)
    c.drawString(bx+4, by+3, "Too simple — misses curve!")

c.setFillColor(A4); c.setFont("Helvetica-Bold", 8.5)
y -= 102
c.drawString(MARGIN_L, y, "Averaging all 3 stumps → still the same horizontal line → STILL HIGH BIAS!")
y -= 14
c.drawString(MARGIN_L, y, "We need a DIFFERENT approach: each new model must CORRECT the mistakes of the previous ones.")
y -= 22

rounded_rect(c, MARGIN_L, y - 22, SW-MARGIN_L*2, 24, r=3, fill=HexColor("#2A0A0A"), stroke=A4, sw=1.5)
c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 9)
msg = "Key insight for Boosting: instead of training models independently, train them SEQUENTIALLY where each one focuses on what the last one got WRONG."
tw = c.stringWidth(msg, "Helvetica-Bold", 9)
if tw > SW - MARGIN_L*2 - 20:
    c.setFont("Helvetica-Bold", 8)
    tw = c.stringWidth(msg, "Helvetica-Bold", 8)
c.drawString((SW-tw)/2, y - 10, msg)
c.showPage()

# ─── AdaBoost Step by Step ────────────────────────────
new_page(c, A4)
header(c, "Boosting — AdaBoost: Reweighting Mistakes Step by Step", accent=A4)

y = CONTENT_TOP - 6
# Sample row
samples = [("S1","●","correct"), ("S2","●","correct"), ("S3","○","correct"),
           ("S4","●","wrong"),   ("S5","○","wrong"),   ("S6","●","correct"),
           ("S7","○","correct"), ("S8","●","wrong")]
sample_w = (SW - MARGIN_L*2) / len(samples)

section_label(c, MARGIN_L, y - 2, "8 training samples — initial weights all equal (1/8)", A4)
y -= 14

# Round 1
rounds_data = [
    ("Round 1: Stump on Feature A", [0,1,2,3,4,5,6,7], [3,4,7], A4),
    ("Round 2: Focus on wrong ones → Stump B", [0,1,2,3,4,5,6,7], [0,1,5], A3),
    ("Round 3: Focus on remaining errors → Stump C", [0,1,2,3,4,5,6,7], [2,6], A5),
]
rh = (y - CONTENT_BOT - 30) / len(rounds_data) - 8
for ri, (rlabel, all_s, wrong_s, col) in enumerate(rounds_data):
    ry = y - ri*(rh + 10)
    rounded_rect(c, MARGIN_L, ry - rh, SW-MARGIN_L*2, rh, r=3, fill=CARD, stroke=col, sw=1)

    c.setFillColor(col); c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN_L + 6, ry - 12, rlabel)

    # samples with weight bars
    for si, (sname, sym, _) in enumerate(samples):
        sx3 = MARGIN_L + si*sample_w + sample_w*0.15
        is_wrong = si in wrong_s
        # weight bar
        weight_h = 30 if si in wrong_s and ri > 0 else (20 if si in wrong_s else 16)
        base_y = ry - rh + 4
        bar_col = A4 if is_wrong else A2
        c.setFillColor(bar_col)
        c.rect(sx3, base_y, sample_w*0.7, weight_h, fill=1, stroke=0)
        # sample label
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 7)
        tw = c.stringWidth(sname, "Helvetica-Bold", 7)
        c.drawString(sx3 + sample_w*0.35 - tw/2, base_y + weight_h + 3, sname)
        # wrong marker
        if is_wrong:
            c.setFillColor(RSOFT); c.setFont("Helvetica-Bold", 10)
            c.drawString(sx3 + sample_w*0.35 - 4, base_y + weight_h + 13, "✗")

    # alpha value
    alphas = ["α₁=0.42", "α₂=0.65", "α₃=0.92"]
    math_pill(c, SW - MARGIN_R - 100, ry - rh + 4, alphas[ri], w=90, accent=col)

# Final combination
y2 = CONTENT_BOT + 4
math_pill(c, MARGIN_L, y2, "F(x) = sign( alpha1*h1(x) + alpha2*h2(x) + alpha3*h3(x) )    Higher alpha = more trusted model", w=SW-MARGIN_L*2-10, accent=A4)
c.showPage()

# ─── AdaBoost Mathematics ─────────────────────────────
new_page(c, A4)
header(c, "AdaBoost — Full Mathematics", accent=A4)

y = CONTENT_TOP - 8
lw = (SW - MARGIN_L*2 - 16) / 2

# Left column
section_label(c, MARGIN_L, y - 2, "Initialisation & Algorithm", A4)
y -= 16
math_pill(c, MARGIN_L, y, "w_i = 1/N   for all i=1..N", w=lw)
y -= 20
steps_ada = [
    ("1. Train weak learner h_t", "on weighted samples"),
    ("2. Compute weighted error", "eps_t = SUM(w_i * I(h_t wrong)) / SUM(w_i)"),
    ("3. Compute model weight", "alpha_t = 0.5 * ln( (1-eps_t) / eps_t )"),
    ("4. Update weights", "w_i = w_i * exp(-alpha_t * y_i * h_t(x_i))"),
    ("5. Normalise weights", "SUM(w_i) = 1  (divide all by sum)"),
]
for slabel, smath in steps_ada:
    c.setFillColor(A4); c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN_L, y, slabel)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7.5)
    c.drawString(MARGIN_L, y - 10, smath)
    y -= 24

math_pill(c, MARGIN_L, y, "Final: F(x) = sign( SUM alpha_t * h_t(x) )", w=lw, accent=A4)

# Right column
rx = MARGIN_L + lw + 16
y = CONTENT_TOP - 16
section_label(c, rx, y + 6, "Alpha Insight", A3)
y -= 14

# Alpha curve
c_h = 90; c_w = lw - 10
c_x = rx; c_y = y - c_h
rounded_rect(c, c_x, c_y, c_w, c_h, r=3, fill=CARD, stroke=BORDER, sw=0.5)
c.setStrokeColor(BORDER); c.setLineWidth(0.5)
c.line(c_x, c_y + c_h/2, c_x + c_w, c_y + c_h/2)
c.line(c_x + c_w/2, c_y, c_x + c_w/2, c_y + c_h)
eps_range = [i/20 for i in range(1, 10)]
alpha_vals = [0.5*math.log((1-e)/e) for e in eps_range]
alpha_max = max(alpha_vals); alpha_min = min(alpha_vals)
def eps_to_xy(eps, alpha):
    px_ = c_x + eps/(0.5)*c_w*0.9 + c_w*0.05
    py_ = c_y + c_h/2 + alpha/(alpha_max*1.1)*c_h*0.45
    return px_, py_
pts_curve = [eps_to_xy(e, a) for e, a in zip(eps_range, alpha_vals)]
c.setStrokeColor(A4); c.setLineWidth(1.5)
p_ = c.beginPath(); p_.moveTo(*pts_curve[0])
for pt in pts_curve[1:]: p_.lineTo(*pt)
c.drawPath(p_, fill=0, stroke=1)
c.setFillColor(LGRAY); c.setFont("Helvetica", 6.5)
c.drawString(c_x + c_w*0.7, c_y + 4, "epsilon →")
c.drawString(c_x + 4, c_y + c_h*0.85, "alpha ↑")
c.drawString(c_x + 4, c_y + 4, "alpha ↓ (negative=flip)")
y -= c_h + 8

bullet_list(c, rx, y, [
    "eps < 0.5 → alpha > 0 → model helps",
    "eps = 0.5 → alpha = 0 → model ignored (random)",
    "eps → 0  → alpha → ∞ → near-perfect model gets huge weight",
    "eps > 0.5 → alpha < 0 → model's vote is FLIPPED",
], size=8, lh=14, max_w=lw, col=DARK)
c.showPage()

# ─── Gradient Boosting ────────────────────────────────
new_page(c, A4)
header(c, "Boosting — Gradient Boosting: Fitting Residuals Step by Step", accent=A4)

y = CONTENT_TOP - 6
section_label(c, MARGIN_L, y - 2, "KEY IDEA — Fit each new tree to the RESIDUALS (errors) of the current model", A4)
y -= 16

# Step pipeline
steps_gb = [
    ("F0: Predict mean", "F_0(x) = mean(y) for all", "Residuals: y - F_0(x)", A1),
    ("h1: Fit tree to r1", "IG splits on residual values", "Update: F_1 = F_0 + eta*h1", A3),
    ("h2: Fit tree to r2", "r2 = y - F_1(x)  smaller!", "Update: F_2 = F_1 + eta*h2", A3),
    ("hM: After M rounds", "Residuals near zero", "F_M(x) = F_0 + eta*SUM h_m", A2),
]
gb_w = (SW - MARGIN_L*2 - 30) / len(steps_gb)
sx4 = MARGIN_L
for i, (stitle, sdesc, supd, col) in enumerate(steps_gb):
    rounded_rect(c, sx4, y - 65, gb_w, 65, r=4, fill=CARD, stroke=col, sw=1.5)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 7.5)
    tw = c.stringWidth(stitle, "Helvetica-Bold", 7.5)
    c.drawString(sx4 + gb_w/2 - tw/2, y - 12, stitle)
    c.setFillColor(WHITE); c.setFont("Helvetica", 7)
    tw = c.stringWidth(sdesc, "Helvetica", 7)
    c.drawString(sx4 + gb_w/2 - tw/2, y - 28, sdesc)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7)
    tw = c.stringWidth(supd, "Helvetica", 7)
    c.drawString(sx4 + gb_w/2 - tw/2, y - 40, supd)
    # residual bar (decreasing)
    bar_heights = [50, 30, 18, 6]
    c.setFillColor(col)
    c.rect(sx4 + gb_w/2 - 8, y - 60, 16, bar_heights[i]*0.3 + 4, fill=1, stroke=0)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 6)
    tw = c.stringWidth("residual", "Helvetica", 6)
    c.drawString(sx4 + gb_w/2 - tw/2, y - 64, "residual")
    if i < len(steps_gb)-1:
        arrow_h(c, sx4 + gb_w + 1, y - 32, sx4 + gb_w + 9, y - 32, col)
    sx4 += gb_w + 10

y -= 80

# Numeric example
section_label(c, MARGIN_L, y - 2, "Numeric Example (3 samples, regression)", A4)
y -= 14

ex_data = [("x=1", 10, 8.0, 8.3, 9.8), ("x=2", 20, 8.0, 9.8, 19.6), ("x=3", 15, 8.0, 9.8, 14.8)]
col_heads = ["Sample", "True y", "F0 (mean)", "F0 residual", "F1 pred", "F1 residual"]
cw_cols = [50, 45, 60, 75, 55, 75]
hx = MARGIN_L
row_hy = y - 14
# header
for ch, cw in zip(col_heads, cw_cols):
    rounded_rect(c, hx, row_hy, cw, 14, r=1, fill=HexColor("#1A3050"), stroke=A1, sw=0.5)
    c.setFillColor(A1); c.setFont("Helvetica-Bold", 7)
    tw = c.stringWidth(ch, "Helvetica-Bold", 7)
    c.drawString(hx + cw/2 - tw/2, row_hy + 4, ch)
    hx += cw

for ri2, (sname, ty, f0, f0r, f1p) in enumerate(ex_data):
    hx = MARGIN_L; ry2 = row_hy - (ri2+1)*14
    f0_residual = ty - f0; f1_residual = ty - f1p
    row_data = [sname, str(ty), str(f0), f"{f0_residual:+.1f}", str(f1p), f"{f1_residual:+.1f}"]
    for ci2, (cell, cw) in enumerate(zip(row_data, cw_cols)):
        bg2 = CARD if ri2%2==0 else HexColor("#1A2A3A")
        bc2 = A4 if ci2 in [3,5] and abs(float(cell.replace("+","")) if cell[0] in "+-0123456789" else 0) > 0.5 else BORDER
        rounded_rect(c, hx, ry2, cw, 14, r=1, fill=bg2, stroke=bc2, sw=0.5)
        c.setFillColor(RSOFT if (ci2 in [3,5] and cell.startswith("+") and abs(float(cell)) > 0.5) else WHITE if ci2>0 else LGRAY)
        c.setFont("Helvetica", 7); tw = c.stringWidth(cell,"Helvetica",7)
        c.drawString(hx + cw/2 - tw/2, ry2 + 4, cell)
        hx += cw

y = row_hy - 4*14 - 10
math_pill(c, MARGIN_L, y, "F_m(x) = F_{m-1}(x) + eta * h_m(x)    Residuals shrink each round  → Bias reduces!", w=SW-MARGIN_L*2-10, accent=A4)
c.showPage()

# ─── Boosting vs Overfitting ──────────────────────────
new_page(c, A4)
header(c, "Boosting — Fixes Bias But Can Overfit: How to Control It", accent=A4)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "WHAT BOOSTING SOLVES & ITS RISKS", A4)
y -= 16

# Side by side
pw = (SW - MARGIN_L*2 - 12) / 2
# Fixes
rounded_rect(c, MARGIN_L, CONTENT_BOT, pw, y - CONTENT_BOT, r=4, fill=CARD, stroke=A2, sw=1.5)
c.setFillColor(A2); c.setFont("Helvetica-Bold", 9)
tw = c.stringWidth("FIXES: High Bias (Underfitting)", "Helvetica-Bold", 9)
c.drawString(MARGIN_L + pw/2 - tw/2, y - 14, "FIXES: High Bias (Underfitting)")
y2 = y - 28
bullet_list(c, MARGIN_L+6, y2, [
    "Sequential correction reduces bias each round",
    "Weak stumps combined → strong model",
    "Can model complex non-linear patterns",
    "More rounds (M) → lower training error",
], size=8.5, lh=15, max_w=pw-12, dot=A2)

# Risks
rx2 = MARGIN_L + pw + 12
rounded_rect(c, rx2, CONTENT_BOT, pw, y - CONTENT_BOT, r=4, fill=CARD, stroke=A4, sw=1.5)
c.setFillColor(A4); c.setFont("Helvetica-Bold", 9)
y3 = y
tw = c.stringWidth("RISK: Overfitting if not controlled", "Helvetica-Bold", 9)
c.drawString(rx2 + pw/2 - tw/2, y3 - 14, "RISK: Overfitting if not controlled")
y4 = y3 - 28
bullet_list(c, rx2+6, y4, [
    "Too many rounds M → memorises training data",
    "Learning rate too high → overly aggressive",
    "Deep trees → each step too complex",
], size=8.5, lh=15, max_w=pw-12, dot=A4)

# Controls
c.setFillColor(A3); c.setFont("Helvetica-Bold", 8.5)
c.drawString(rx2 + 6, y4 - 55, "How to prevent overfitting:")
controls = [("Shrinkage","Small learning rate eta (0.01–0.1)"),
            ("Early stopping","Stop when val error increases"),
            ("Subsampling","Use fraction of rows per round"),
            ("Shallow trees","max_depth = 3 or 4 only")]
for ci, (cname, cdesc) in enumerate(controls):
    cy = y4 - 72 - ci*18
    rounded_rect(c, rx2+6, cy, pw-14, 15, r=2, fill=CARD, stroke=A3, sw=0.8)
    c.setFillColor(A3); c.setFont("Helvetica-Bold", 7); c.drawString(rx2+10, cy+4, cname+":")
    c.setFillColor(WHITE); c.setFont("Helvetica", 7)
    tw5 = c.stringWidth(cname+":", "Helvetica-Bold", 7)
    c.drawString(rx2+12+tw5, cy+4, cdesc)

c.showPage()

# ═══════════════════════════════════════════════════════
# SECTION 05 – XGBoost
# ═══════════════════════════════════════════════════════
new_page(c, A5)
header(c, "Section 05 — XGBoost", accent=A5)
c.setFillColor(A5); c.rect(0, 0, 10, SH - TOP_BAR, fill=1, stroke=0)
c.setFillColor(HexColor("#1A0A2A")); c.setFont("Helvetica-Bold", 100)
c.drawString(20, SH//2 - 55, "05")
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 26)
c.drawString(20, SH//2 - 4, "XGBoost")
c.setFillColor(LGRAY); c.setFont("Helvetica", 11)
c.drawString(20, SH//2 - 22, "eXtreme Gradient Boosting — Regularised, Fast, and Dominant")
c.showPage()

# ─── XGBoost: Problem with Vanilla GB ─────────────────
new_page(c, A5)
header(c, "XGBoost — The Problem: Vanilla Gradient Boosting Overfits", accent=A5)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "THE PROBLEM — Standard GB has no regularisation and is slow", A4)
y -= 16

c.setFillColor(DARK); c.setFont("Helvetica", 8.5)
c.drawString(MARGIN_L, y, "Vanilla Gradient Boosting (Friedman 2001) works well, but has key weaknesses:")
y -= 18

weaknesses = [
    ("No regularisation", "Leaf weights can grow arbitrarily large → overfitting", A4),
    ("Greedy splits only", "Uses only first-order gradient → slow convergence", A3),
    ("No missing value handling", "Must pre-process missing data manually", A3),
    ("Sequential (slow)", "Cannot parallelise tree building", A4),
    ("Heuristic split finding", "Exact greedy is O(N*p) per split — slow on large data", A4),
]
for i, (wname, wdesc, col) in enumerate(weaknesses):
    by = y - i*22 - 16
    rounded_rect(c, MARGIN_L, by, SW-MARGIN_L*2, 18, r=3, fill=CARD, stroke=col, sw=0.8)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 8); c.drawString(MARGIN_L+6, by+5, wname+":")
    c.setFillColor(WHITE); c.setFont("Helvetica", 8)
    tw6 = c.stringWidth(wname+": ", "Helvetica-Bold", 8)
    c.drawString(MARGIN_L+6+tw6, by+5, wdesc)

y -= len(weaknesses)*22 + 26
rounded_rect(c, MARGIN_L, y - 22, SW-MARGIN_L*2, 24, r=3, fill=HexColor("#1A0A2A"), stroke=A5, sw=1.5)
c.setFillColor(A5); c.setFont("Helvetica-Bold", 9)
msg7 = "XGBoost (Chen & Guestrin, 2016) adds: L1+L2 regularisation + 2nd-order gradients + column subsampling + cache-aware computation"
tw7 = c.stringWidth(msg7, "Helvetica-Bold", 9)
if tw7 > SW - MARGIN_L*2 - 20:
    c.setFont("Helvetica-Bold", 8); tw7 = c.stringWidth(msg7, "Helvetica-Bold", 8)
c.drawString((SW-tw7)/2, y - 11, msg7)
c.showPage()

# ─── XGBoost: Objective Function ──────────────────────
new_page(c, A5)
header(c, "XGBoost — The Fix: Regularised Objective + 2nd Order Gradients", accent=A5)

y = CONTENT_TOP - 8
section_label(c, MARGIN_L, y, "THE SOLUTION — New Objective Function with Built-in Regularisation", A5)
y -= 16

# Objective breakdown
math_pill(c, MARGIN_L, y, "Obj = SUM_i  L(y_i, y_hat_i)   +   SUM_k  Omega(f_k)", w=SW-MARGIN_L*2-10, accent=A5)
y -= 18

# Two boxes: loss term + regularisation term
bw8 = (SW - MARGIN_L*2 - 12) / 2
rounded_rect(c, MARGIN_L, y - 60, bw8, 62, r=3, fill=CARD, stroke=A1, sw=1)
c.setFillColor(A1); c.setFont("Helvetica-Bold", 8.5)
tw = c.stringWidth("Loss Term: SUM L(y_i, y_hat_i)", "Helvetica-Bold", 8.5)
c.drawString(MARGIN_L + bw8/2 - tw/2, y - 12, "Loss Term: SUM L(y_i, y_hat_i)")
c.setFillColor(LGRAY); c.setFont("Helvetica", 8)
lines_l = ["How well does model fit?",
           "MSE: (y - y_hat)^2 / 2",
           "Log Loss for classification",
           "→ Want this to go DOWN"]
for li, ln in enumerate(lines_l): c.drawString(MARGIN_L+6, y-26-li*10, ln)

rx8 = MARGIN_L + bw8 + 12
rounded_rect(c, rx8, y - 60, bw8, 62, r=3, fill=CARD, stroke=A5, sw=1.5)
c.setFillColor(A5); c.setFont("Helvetica-Bold", 8.5)
tw = c.stringWidth("Regularisation: Omega(f)", "Helvetica-Bold", 8.5)
c.drawString(rx8 + bw8/2 - tw/2, y - 12, "Regularisation: Omega(f)")
c.setFillColor(LGRAY); c.setFont("Helvetica", 8)
lines_r = ["How complex is the tree?",
           "Omega(f) = gamma*T + (lambda/2)*SUM(w_j^2)",
           "T=leaves, w_j=leaf weights",
           "→ Penalises complexity → prevents overfit"]
for li, ln in enumerate(lines_r): c.drawString(rx8+6, y-26-li*10, ln)
y -= 72

# 2nd order gradients
section_label(c, MARGIN_L, y - 2, "2nd Order Taylor Approximation — Smarter Updates", A5)
y -= 14
math_pill(c, MARGIN_L, y, "Obj_approx = SUM_i [ g_i*f(x_i) + (1/2)*h_i*f(x_i)^2 ] + Omega(f)", w=SW-MARGIN_L*2-10, accent=A5)
y -= 18
math_pill(c, MARGIN_L, y, "g_i = dL/dy_hat   (1st deriv, direction)      h_i = d^2L/dy_hat^2   (2nd deriv, curvature)", w=SW-MARGIN_L*2-10, accent=LGRAY)
y -= 22

# Optimal values
rounded_rect(c, MARGIN_L, y - 32, SW-MARGIN_L*2, 34, r=3, fill=HexColor("#1A0A2A"), stroke=A5, sw=1.5)
c.setFillColor(A5); c.setFont("Helvetica-Bold", 8.5)
c.drawString(MARGIN_L+6, y-10, "Closed-form optimal leaf weight & split gain:")
math_pill(c, MARGIN_L+6, y-22, "w_j* = -(SUM_j g_i) / (SUM_j h_i + lambda)", w=220, accent=A5)
math_pill(c, MARGIN_L+6+230, y-22, "Gain = (1/2)*[G_L^2/(H_L+lam) + G_R^2/(H_R+lam) - (G_L+G_R)^2/(H_L+H_R+lam)] - gamma", w=270, accent=A3)
c.showPage()

# ─── XGBoost Full Step Diagram ────────────────────────
new_page(c, A5)
header(c, "XGBoost — Step-by-Step Pipeline (Numeric Example)", accent=A5)

y = CONTENT_TOP - 6
section_label(c, MARGIN_L, y, "Example: 4 samples, predict house price. eta=0.3, lambda=1, gamma=0", A5)
y -= 16

# Pipeline
xgb_steps = [
    ("Initialise", "F0(x) = 0.5\n(or log-odds\nfor classif.)", A1),
    ("Compute g,h", "g_i = F0-y_i\nh_i = 1 (MSE)\nper sample", A5),
    ("Build tree\n(max IG gain)", "Split: feature\nwith max Gain\nusing g,h,lam", A5),
    ("Optimal\nleaf weights", "w* = -SUM(g)/\n(SUM(h)+lam)\nper leaf", A3),
    ("Update", "F1=F0+eta*T1\nNew residuals\nfor round 2", A2),
]
sw5 = (SW - MARGIN_L*2 - 40) / len(xgb_steps)
sx5 = MARGIN_L
for i, (stitle, sdesc, col) in enumerate(xgb_steps):
    by = y - 80
    rounded_rect(c, sx5, by, sw5, 80, r=3, fill=CARD, stroke=col, sw=1.5)
    cx5 = sx5 + sw5/2
    c.setFillColor(col); c.setFont("Helvetica-Bold", 7.5)
    for li, ln in enumerate(stitle.split("\n")):
        tw = c.stringWidth(ln, "Helvetica-Bold", 7.5)
        c.drawString(cx5 - tw/2, by + 70 - li*10, ln)
    c.setFillColor(WHITE); c.setFont("Helvetica", 7)
    for li, ln in enumerate(sdesc.split("\n")):
        tw = c.stringWidth(ln, "Helvetica", 7)
        c.drawString(cx5 - tw/2, by + 42 - li*10, ln)
    if i < len(xgb_steps)-1:
        arrow_h(c, sx5 + sw5 + 1, by + 40, sx5 + sw5 + 9, by + 40, col)
    sx5 += sw5 + 10

y -= 92

# Numeric table
section_label(c, MARGIN_L, y - 2, "Numerical trace — 2 rounds", A5)
y -= 14
col_heads2 = ["x", "True y", "F0", "g = F0-y", "h=1", "Leaf w*", "F1=F0+0.3*w*", "New residual"]
cw9 = [26, 36, 26, 60, 30, 55, 80, 70]
rows9 = [(1, 10, 0.5, -9.5, 1, "-9.5/2=-4.75", "0.5+0.3*-4.75=-0.92", "10-(-0.92)=10.92"),
         (2, 15, 0.5, -14.5, 1, "-14.5/2=-7.25", "0.5+0.3*-7.25=-1.68", "15-(-1.68)=16.68"),
         (3, 8,  0.5, -7.5,  1, "-7.5/2=-3.75",  "0.5+0.3*-3.75=-0.63", "8-(-0.63)=8.63"),
         (4, 12, 0.5, -11.5, 1, "-11.5/2=-5.75", "0.5+0.3*-5.75=-1.22", "12-(-1.22)=13.22")]
hx9 = MARGIN_L
row_hy9 = y - 12
for ch9, cw9_ in zip(col_heads2, cw9):
    rounded_rect(c, hx9, row_hy9, cw9_, 12, r=1, fill=HexColor("#1A0A2A"), stroke=A5, sw=0.5)
    c.setFillColor(A5); c.setFont("Helvetica-Bold", 6.5)
    tw = c.stringWidth(ch9, "Helvetica-Bold", 6.5)
    c.drawString(hx9 + cw9_/2 - tw/2, row_hy9 + 3, ch9)
    hx9 += cw9_

for ri9, row9 in enumerate(rows9):
    hx9 = MARGIN_L; ry9 = row_hy9 - (ri9+1)*12
    for ci9, (cell9, cw9_) in enumerate(zip(row9, cw9)):
        bg9 = CARD if ri9%2==0 else HexColor("#1A1A2A")
        rounded_rect(c, hx9, ry9, cw9_, 12, r=1, fill=bg9, stroke=BORDER, sw=0.3)
        c.setFillColor(LGRAY if ci9==0 else WHITE); c.setFont("Helvetica", 6)
        s9 = str(cell9); tw = c.stringWidth(s9, "Helvetica", 6)
        c.drawString(hx9 + cw9_/2 - tw/2, ry9 + 3, s9)
        hx9 += cw9_

y = row_hy9 - 6*12 - 8
math_pill(c, MARGIN_L, y, "Note: w* uses SUM(g)/SUM(h)+lambda PER LEAF — here all 4 are in one leaf for simplicity.  gamma penalises adding more leaves.", w=SW-MARGIN_L*2-10, accent=A5)
c.showPage()

# ─── XGBoost Hyperparameters ──────────────────────────
new_page(c, A5)
header(c, "XGBoost — Hyperparameters & How They Fight Overfitting/Underfitting", accent=A5)

y = CONTENT_TOP - 8
params_xgb = [
    ("n_estimators", "M",     "Number of trees / boosting rounds",             "100",   A5,  "More = lower bias.  Too many = overfit."),
    ("learning_rate","eta",   "Step size — shrinks each tree's contribution",  "0.1",   A3,  "Smaller = better generalisation, needs more trees"),
    ("max_depth",    "d",     "Max depth of each tree",                        "6",     A4,  "Deeper = more bias reduction, more overfit risk"),
    ("gamma",        "γ",     "Min gain needed to make a split",               "0",     A5,  "Higher = fewer splits = simpler trees = less overfit"),
    ("reg_lambda",   "λ",     "L2 ridge on leaf weights",                      "1",     A5,  "Higher = smaller leaf weights = less overfit"),
    ("reg_alpha",    "α",     "L1 lasso on leaf weights",                      "0",     A5,  "Sparsifies weights — useful with many features"),
    ("subsample",    "ss",    "Fraction of rows sampled per tree (Stochastic GB)","1",  A2,  "< 1.0 adds randomness → reduces overfit"),
    ("colsample_bytree","cst","Fraction of features used per tree (like RF)","1",       A2,  "< 1.0 decorrelates trees → reduces overfit"),
    ("min_child_weight","mcw","Min hessian sum in leaf (complexity control)","1",       A3,  "Higher = simpler model = less overfit"),
    ("early_stopping","es",   "Stop if val metric doesn't improve for N rounds","10",   A2,  "Best practice: always use with a validation set"),
]
row_h10 = (y - CONTENT_BOT - 4) / len(params_xgb) - 2
for i, (pname, psym, pdesc, pdef, col, effect) in enumerate(params_xgb):
    by = y - (i+1)*(row_h10+2)
    rounded_rect(c, MARGIN_L, by, SW-MARGIN_L*2, row_h10, r=2, fill=CARD, stroke=col, sw=0.7)
    c.setFillColor(col); c.setFont("Courier-Bold", 8); c.drawString(MARGIN_L+4, by+row_h10/2-1, pname)
    c.setFillColor(YELLOW); c.setFont("Helvetica-Bold", 7); c.drawString(MARGIN_L+88, by+row_h10/2-1, psym)
    c.setFillColor(WHITE); c.setFont("Helvetica", 7.5); c.drawString(MARGIN_L+100, by+row_h10/2-1, pdesc)
    c.setFillColor(A2); c.setFont("Helvetica-Bold", 7); c.drawString(MARGIN_L+280, by+row_h10/2-1, f"≈{pdef}")
    c.setFillColor(LGRAY); c.setFont("Helvetica", 7); c.drawString(MARGIN_L+320, by+row_h10/2-1, effect)

c.showPage()

# ═══════════════════════════════════════════════════════
# SECTION 06 – COMPARISON
# ═══════════════════════════════════════════════════════
new_page(c, LGRAY)
header(c, "Section 06 — Summary & Comparison", accent=LGRAY)
c.setFillColor(LGRAY); c.rect(0, 0, 10, SH - TOP_BAR, fill=1, stroke=0)
c.setFillColor(HexColor("#1A2A3A")); c.setFont("Helvetica-Bold", 100)
c.drawString(20, SH//2 - 55, "06")
c.setFillColor(DARK); c.setFont("Helvetica-Bold", 26)
c.drawString(20, SH//2 - 4, "Comparison")
c.setFillColor(LGRAY); c.setFont("Helvetica", 11)
c.drawString(20, SH//2 - 22, "Side-by-side guide — know when to use what")
c.showPage()

# ─── Comparison Table ─────────────────────────────────
new_page(c, A1)
header(c, "Full Comparison — All Methods Side by Side", accent=A1)

y = CONTENT_TOP - 6
headers_t = ["Property", "Bagging", "Random Forest", "AdaBoost", "GradBoost", "XGBoost"]
col_ws_t = [78, 60, 72, 60, 65, 65]
col_acs = [LGRAY, A2, A3, A4, A4, A5]
rows_t = [
    ("Training",       "Parallel",     "Parallel",     "Sequential",  "Sequential",  "Sequential"),
    ("Base learner",   "Any",          "Dec. Trees",   "Stump/tree",  "Shallow tree","Shallow tree"),
    ("Fixes",          "Variance",     "Variance",     "Bias",        "Bias+Var",    "Bias+Var"),
    ("Aggregation",    "Vote/Mean",    "Vote/Mean",    "Wtd. vote",   "Additive",    "Additive"),
    ("Regularisation", "None",         "Via depth",    "Via alpha",   "Shrinkage",   "L1+L2+gamma"),
    ("Missing data",   "Manual",       "Manual",       "Manual",      "Manual",      "Built-in"),
    ("Feature import", "No",           "YES",          "Partial",     "YES",         "YES"),
    ("Overfit risk",   "Low",          "Very Low",     "Can overfit", "Medium",      "Controllable"),
    ("Speed",          "Fast",         "Fast",         "Medium",      "Slow",        "Very Fast"),
    ("Best for",       "High-var mdls","Tabular data", "Weak lrnrs",  "Complex data","Most tasks"),
]
row_ht = (y - CONTENT_BOT - 4) / (len(rows_t)+1) - 1

# header row
hx_t = MARGIN_L
for ch_t, cw_t, ca in zip(headers_t, col_ws_t, col_acs):
    rounded_rect(c, hx_t, y - row_ht, cw_t, row_ht - 1, r=1, fill=ca, stroke=ca, sw=0.3)
    c.setFillColor(DARK if ca != LGRAY else DARK); c.setFont("Helvetica-Bold", 7.5)
    tw_t = c.stringWidth(ch_t, "Helvetica-Bold", 7.5)
    c.drawString(hx_t + cw_t/2 - tw_t/2, y - row_ht + row_ht/2 - 3, ch_t)
    hx_t += cw_t

for ri_t, row_t in enumerate(rows_t):
    hx_t = MARGIN_L; ry_t = y - (ri_t+2)*(row_ht+1)
    for ci_t, (cell_t, cw_t, ca) in enumerate(zip(row_t, col_ws_t, col_acs)):
        bg_t = CARD if ri_t%2==0 else HexColor("#1A2A3A")
        brd = ca if ci_t > 0 else BORDER
        rounded_rect(c, hx_t, ry_t, cw_t, row_ht-1, r=1, fill=bg_t, stroke=brd, sw=0.3)
        c.setFillColor(ca if ci_t > 0 else LGRAY)
        c.setFont("Helvetica-Bold" if ci_t==0 else "Helvetica", 7)
        tw_t2 = c.stringWidth(cell_t, "Helvetica-Bold" if ci_t==0 else "Helvetica", 7)
        c.drawString(hx_t + cw_t/2 - tw_t2/2, ry_t + row_ht/2 - 3, cell_t)
        hx_t += cw_t

c.showPage()

# ─── Bias-Variance Map ────────────────────────────────
new_page(c, A1)
header(c, "Visual Summary — Where Each Method Sits on Bias-Variance Map", accent=A1)

y = CONTENT_TOP - 6
# Quadrant plot
ax_x = MARGIN_L + 40; ax_y = CONTENT_BOT + 20
ax_w = SW - ax_x - MARGIN_R - 20; ax_h = y - ax_y

# Background quadrants
c.setFillColor(HexColor("#1A0A0A")); c.rect(ax_x, ax_y + ax_h/2, ax_w/2, ax_h/2, fill=1, stroke=0)  # HB, HV
c.setFillColor(HexColor("#1A1A0A")); c.rect(ax_x + ax_w/2, ax_y + ax_h/2, ax_w/2, ax_h/2, fill=1, stroke=0)  # LB HV
c.setFillColor(HexColor("#1A0A1A")); c.rect(ax_x, ax_y, ax_w/2, ax_h/2, fill=1, stroke=0)  # HB LV
c.setFillColor(HexColor("#0A1A0A")); c.rect(ax_x + ax_w/2, ax_y, ax_w/2, ax_h/2, fill=1, stroke=0)  # LB LV (ideal)

# Axes
c.setStrokeColor(LGRAY); c.setLineWidth(1)
c.line(ax_x, ax_y, ax_x + ax_w, ax_y)
c.line(ax_x, ax_y, ax_x, ax_y + ax_h)
c.line(ax_x, ax_y + ax_h/2, ax_x + ax_w, ax_y + ax_h/2)
c.line(ax_x + ax_w/2, ax_y, ax_x + ax_w/2, ax_y + ax_h)

# Axis labels
c.setFillColor(LGRAY); c.setFont("Helvetica", 8)
c.drawString(ax_x + ax_w/2 - 20, ax_y - 14, "← LOW BIAS     HIGH BIAS →")
c.saveState(); c.translate(ax_x - 20, ax_y + ax_h/2)
c.rotate(90); c.drawString(-40, 0, "← LOW VAR     HIGH VAR →"); c.restoreState()

# Quadrant labels
quad_labels = [
    (ax_x + ax_w*0.25, ax_y + ax_h*0.85, "High Bias\nHigh Var", HexColor("#EF5350")),
    (ax_x + ax_w*0.75, ax_y + ax_h*0.85, "Low Bias\nHigh Var", A3),
    (ax_x + ax_w*0.25, ax_y + ax_h*0.15, "High Bias\nLow Var", A3),
    (ax_x + ax_w*0.75, ax_y + ax_h*0.15, "Low Bias\nLow Var\n(IDEAL)", A2),
]
for (qx, qy, qlabel, qcol) in quad_labels:
    c.setFillColor(qcol); c.setFont("Helvetica-Bold", 7.5)
    for li, ln in enumerate(qlabel.split("\n")):
        tw = c.stringWidth(ln, "Helvetica-Bold", 7.5); c.drawString(qx - tw/2, qy - li*10, ln)

# Method points
# bias_frac, var_frac → plot position (0=left/bottom, 1=right/top of that axis)
# NOTE: x-axis = bias (right = HIGH bias), y-axis = variance (top = HIGH variance)
methods_map = [
    ("Single Deep Tree", 0.15, 0.88, A4),
    ("Single Shallow Tree", 0.80, 0.15, A3),
    ("Bagging", 0.15, 0.45, A2),
    ("Random Forest", 0.15, 0.22, A3),
    ("AdaBoost", 0.25, 0.38, A4),
    ("Grad. Boosting", 0.18, 0.30, A4),
    ("XGBoost\n(well-tuned)", 0.12, 0.12, A5),
    ("XGBoost\n(overtrained)", 0.10, 0.80, RSOFT),
]
for mname, bias_f, var_f, col in methods_map:
    px_m = ax_x + bias_f * ax_w
    py_m = ax_y + var_f * ax_h
    c.setFillColor(col); c.circle(px_m, py_m, 5, fill=1, stroke=0)
    c.setFillColor(DARK); c.setFont("Helvetica", 7)
    for li, ln in enumerate(mname.split("\n")):
        c.drawString(px_m + 7, py_m + 3 - li*9, ln)

c.showPage()

# ─── When to Use Which ────────────────────────────────
new_page(c, A1)
header(c, "Decision Guide — When to Use Which Algorithm", accent=A1)

y = CONTENT_TOP - 6
scenarios = [
    ("Model is OVERFITTING (high variance)",          "→  Bagging / Random Forest",       A2),
    ("Model is UNDERFITTING (high bias)",             "→  Boosting (AdaBoost/XGBoost)",   A4),
    ("Fast training needed, good baseline",           "→  Random Forest",                 A3),
    ("Winning competitions on tabular data",          "→  XGBoost / LightGBM",            A5),
    ("Dataset has missing values, no preprocessing", "→  XGBoost (handles natively)",     A5),
    ("Need feature importance ranking",               "→  Random Forest or XGBoost",      A3),
    ("Very high dimensional sparse features",        "→  XGBoost with colsample < 1",     A5),
    ("Interpretability required",                    "→  Single Decision Tree (not ensemble)", LGRAY),
    ("Small dataset, noisy labels",                  "→  Random Forest (OOB validation)", A2),
    ("Need uncertainty estimates",                   "→  Bagging (prediction variance across trees)", A2),
]
row_hs = (y - CONTENT_BOT - 4) / len(scenarios) - 2
for i, (situation, action, col) in enumerate(scenarios):
    by = y - (i+1)*(row_hs+2)
    rounded_rect(c, MARGIN_L, by, SW-MARGIN_L*2, row_hs, r=2, fill=CARD, stroke=col, sw=0.8)
    c.setFillColor(LGRAY); c.setFont("Helvetica", 8); c.drawString(MARGIN_L+6, by+row_hs/2, situation)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 8.5)
    tw_a = c.stringWidth(action, "Helvetica-Bold", 8.5)
    c.drawString(SW - MARGIN_R - tw_a - 6, by+row_hs/2, action)

c.showPage()

# ─── Final Summary ────────────────────────────────────
new_page(c, A1)
header(c, "Key Takeaways — Everything in One Place", accent=A1)
c.setFillColor(A1); c.rect(0, 0, SW, 3, fill=1, stroke=0)

y = CONTENT_TOP - 8
takeaways_f = [
    (A1, "Information Gain", "H(S) - SUM(|Sv|/|S| * H(Sv))  is the primary split metric in decision trees. Other metrics (Gini, Chi-sq) also exist."),
    (A2, "Bagging", "PARALLEL.  Bootstrap + average.  Reduces VARIANCE (fixes overfitting).  Bias unchanged."),
    (A3, "Random Forest", "Bagging + random feature subsets at each split.  Decorrelates trees → lower variance floor."),
    (A4, "Boosting", "SEQUENTIAL.  Each model corrects previous errors.  Reduces BIAS (fixes underfitting).  Risk of overfit."),
    (A5, "XGBoost", "Regularised GB + 2nd order gradients + column sampling.  Controls both bias AND variance.  Fastest."),
    (LGRAY, "Rule of thumb", "Overfit? → Add trees to Bagging/RF or regularise.  Underfit? → Boost longer or deeper."),
]
row_htf = (y - CONTENT_BOT - 4) / len(takeaways_f) - 3
for i, (col, title, desc) in enumerate(takeaways_f):
    by = y - (i+1)*(row_htf+3)
    rounded_rect(c, MARGIN_L, by, SW-MARGIN_L*2, row_htf, r=3, fill=CARD, stroke=col, sw=1.5)
    c.setFillColor(col); c.setFont("Helvetica-Bold", 8.5); c.drawString(MARGIN_L+6, by+row_htf/2, title+":")
    c.setFillColor(WHITE); c.setFont("Helvetica", 8)
    tw_tf = c.stringWidth(title+": ", "Helvetica-Bold", 8.5)
    # wrap desc
    words_d = desc.split(); line_d = ""; dy_d = by+row_htf/2
    avail_w = SW - MARGIN_L*2 - tw_tf - 16
    for word_d in words_d:
        test_d = (line_d+" "+word_d).strip()
        if c.stringWidth(test_d,"Helvetica",8) <= avail_w:
            line_d = test_d
        else:
            c.drawString(MARGIN_L+6+tw_tf, dy_d, line_d); dy_d -= 9; line_d = word_d
    if line_d: c.drawString(MARGIN_L+6+tw_tf, dy_d, line_d)

c.showPage()
c.save()
print("PDF saved successfully!")