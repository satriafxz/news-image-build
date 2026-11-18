#!/usr/bin/env python3
"""Render the original news-image-20261118 front page (1024x1024 PNG).

All artwork is drawn programmatically with Pillow: flat shapes, flags,
maps and silhouettes. No photograph or third-party artwork is used.
Text is set in DejaVu / Liberation fonts, sized to stay legible at 300px.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

NAVY = (15, 42, 68)
NAVY2 = (31, 68, 104)
RED = (180, 35, 24)
BLUE = (43, 108, 163)
LIGHT = (234, 240, 247)
LIGHT2 = (245, 247, 250)
GREY = (90, 98, 110)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
TAN = (232, 222, 200)
SEA = (198, 222, 238)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading=None, align="left"):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        if align == "center":
            w = draw.textlength(ln, font=fnt)
            draw.text((x - w / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def flag(draw, x, y, w, h, kind):
    # simple flat flag on a pole
    draw.line([(x, y), (x, y + 150)], fill=NAVY, width=4)
    if kind == "china":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        for sx, sy in [(x + 12, y + 10), (x + 30, y + 8), (x + 36, y + 18),
                       (x + 30, y + 28), (x + 14, y + 26)]:
            draw.text((sx, sy), "*", font=font(SANS_B, 16), fill=(255, 222, 0))
    elif kind == "usa":
        for i in range(7):
            col = (178, 34, 52) if i % 2 == 0 else WHITE
            draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7], fill=col)
        draw.rectangle([x, y, x + w * 0.45, y + h * 0.55], fill=NAVY)
    elif kind == "russia":
        for i, col in enumerate([WHITE, (0, 57, 166), (213, 0, 50)]):
            draw.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=col)


def figure(draw, cx, base, h, color):
    # stylised person silhouette: no face, no likeness of a real person
    head_r = 13
    draw.ellipse([cx - head_r, base - h, cx + head_r, base - h + 2 * head_r],
                 fill=color)
    draw.polygon([(cx - 22, base), (cx - 14, base - h + 30),
                  (cx + 14, base - h + 30), (cx + 22, base)], fill=color)


def spiral(draw, cx, cy, rmax, color):
    for r in range(12, rmax, 12):
        a0 = r * 0.35
        a1 = a0 + 4.2
        pts = []
        for k in range(40):
            a = a0 + (a1 - a0) * k / 39
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.85))
        draw.line(pts, fill=color, width=5)


img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# outer border
d.rectangle([8, 8, W - 9, H - 9], outline=BLACK, width=4)

# ---- masthead ----
draw_lines(d, ["THE WORLD IN ONE IMAGE"], 512, 26,
           font(SANS_B, 26), GREY, align="center")
draw_lines(d, ["THE WORLD TODAY"], 512, 58,
           font(SERIF_B, 76), NAVY, align="center")
d.line([(40, 152), (984, 152)], fill=BLACK, width=3)
draw_lines(d, ["Wednesday, 18 November 2026"], 512, 162,
           font(SERIF_B, 42), RED, align="center")
d.line([(40, 222), (984, 222)], fill=BLACK, width=3)

# ---- hero panel: Shenzhen ----
d.rectangle([24, 236, 1000, 522], fill=LIGHT, outline=BLACK, width=2)
draw_lines(d, ["XI WELCOMES", "TRUMP IN", "SHENZHEN"], 48, 250,
           font(SERIF_B, 48), NAVY, leading=56)
draw_lines(d, ["Putin joins APEC leaders ahead of",
               "Thursday's trilateral meeting."], 48, 430,
           font(SANS, 28), BLACK, leading=34)

# skyline + flags + figures, right side of hero
for bx, bw, bh in [(660, 46, 62), (712, 34, 96), (752, 52, 48),
                   (810, 38, 118), (854, 48, 70), (908, 36, 92),
                   (950, 30, 56)]:
    d.rectangle([bx, 502 - bh, bx + bw, 502], fill=NAVY2)
d.rectangle([660, 502, 984, 522], fill=NAVY)
flag(d, 688, 300, 72, 44, "china")
flag(d, 806, 300, 72, 44, "usa")
flag(d, 904, 300, 64, 44, "russia")
figure(d, 720, 502, 96, (30, 30, 30))
figure(d, 840, 502, 96, (90, 98, 110))
figure(d, 936, 502, 96, (120, 40, 32))

# ---- middle row ----
# Gulf panel (left)
d.rectangle([24, 536, 500, 758], fill=WHITE, outline=BLACK, width=2)
d.rectangle([44, 550, 168, 576], fill=RED)
draw_lines(d, ["REPORTED"], 106, 552, font(SANS_B, 20), WHITE, align="center")
draw_lines(d, ["US–IRAN STRIKES", "REPORTED IN THE GULF"], 44, 584,
           font(SERIF_B, 30), NAVY, leading=36)
draw_lines(d, ["US jets reported to hit Qeshm;", "Iran says it hit US bases",
               "in Kuwait and Bahrain."], 44, 668,
           font(SANS, 23), BLACK, leading=28)

# Alaska panel (right)
d.rectangle([524, 536, 1000, 758], fill=WHITE, outline=BLACK, width=2)
draw_lines(d, ["PELTOLA WINS", "ALASKA SENATE SEAT"], 544, 550,
           font(SERIF_B, 33), NAVY, leading=40)
draw_lines(d, ["56–44"], 544, 636, font(SERIF_B, 48), RED)
draw_lines(d, ["Democrats projected", "Senate majority."], 736, 646,
           font(SANS, 22), BLACK, leading=27)
draw_lines(d, ["Announced 17 Nov Alaska time;", "reported 18 Nov UTC."], 544, 706,
           font(SANS, 20), GREY, leading=24)

# ---- bottom panel: Cyclone Akvan ----
d.rectangle([24, 772, 1000, 1000], fill=LIGHT2, outline=BLACK, width=2)
draw_lines(d, ["CYCLONE AKVAN", "HEADS FOR INDIA"], 48, 790,
           font(SERIF_B, 44), NAVY, leading=50)
draw_lines(d, ["Sustained 90–100 km/h • Gusts to 110 km/h",
               "Landfall forecast around noon 20 Nov,",
               "between Narsapur and Puri."], 48, 900,
           font(SANS, 27), BLACK, leading=33)
# Bay of Bengal map + spiral
d.rectangle([640, 792, 976, 980], fill=SEA)
d.polygon([(640, 792), (760, 792), (800, 860), (760, 980), (640, 980)],
          fill=TAN)
d.polygon([(700, 792), (760, 792), (800, 860), (780, 980), (700, 980)],
          fill=(210, 198, 172))
spiral(d, 880, 890, 72, BLUE)
d.ellipse([862, 872, 898, 908], fill=NAVY)
# arrow to coast
d.line([(830, 930), (770, 962)], fill=RED, width=5)
d.polygon([(770, 962), (786, 950), (786, 970)], fill=RED)
draw_lines(d, ["NARSAPUR–PURI"], 652, 800, font(SANS_B, 20), NAVY)

img.save(OUT, format="PNG", optimize=True)
print("saved", OUT)
