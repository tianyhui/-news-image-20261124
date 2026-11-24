#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page, version 2 (1024x1024 PNG).

v2 changes over v1: markets data strip under the lead story (NVDA +31%,
NASDAQ +6%, S&P 500 +4%); a full-width COP31 card (climate talks collapse,
first no-deal since 2009); NATO AWACS / Poland missiles join the ticker;
Ukraine headline shortened so it is no longer cut off at two lines.

Deterministic: fixed text, fonts and drawing calls; no timestamps, no network.
Output: entry.png next to this script.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
CARD = (255, 255, 255)
INK = (26, 26, 26)
MUTED = (90, 90, 90)
RED = (166, 30, 34)
NAVY = (22, 40, 63)
RULE = (216, 210, 196)
GREEN = (90, 138, 0)
STRIP = (232, 242, 220)
DARKGREEN = (52, 96, 10)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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

def spaced(draw, xy, text, fnt, fill, tracking=3):
    """Draw uppercase text with letter tracking."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x

# ---------------- icons (simple geometric pictograms) ----------------
def icon_chip(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rounded_rectangle(box, radius=10, fill=(24, 40, 24))
    for i in range(4):  # pins
        px = x0 + 14 + i * 20
        d.rectangle([px, y0 - 8, px + 7, y0 + 2], fill=(120, 120, 120))
        d.rectangle([px, y1 - 2, px + 7, y1 + 8], fill=(120, 120, 120))
        py = y0 + 14 + i * 20
        d.rectangle([x0 - 8, py, x0 + 2, py + 7], fill=(120, 120, 120))
        d.rectangle([x1 - 2, py, x1 + 8, py + 7], fill=(120, 120, 120))
    d.rounded_rectangle([cx - 26, cy - 26, cx + 26, cy + 26], radius=6,
                        outline=(118, 185, 0), width=4)
    d.text((cx, cy), "AI", font=font(SANS_B, 26), fill=(150, 220, 60), anchor="mm")
    # rising arrow, bottom-right of the AI box so it never crosses the text
    pts = [(cx - 10, cy + 44), (cx + 6, cy + 32), (cx + 16, cy + 40), (cx + 38, cy + 16)]
    d.line(pts, fill=(118, 185, 0), width=5, joint="curve")
    d.polygon([(cx + 38, cy + 16), (cx + 22, cy + 14), (cx + 36, cy + 32)], fill=(118, 185, 0))

def icon_ship(d, box, accent):
    x0, y0, x1, y1 = box
    d.polygon([(x0 + 8, y0 + 52), (x1 - 8, y0 + 52), (x1 - 22, y0 + 74), (x0 + 22, y0 + 74)],
              fill=accent)
    d.rectangle([x0 + 30, y0 + 34, x0 + 62, y0 + 52], fill=accent)
    d.rectangle([x0 + 44, y0 + 14, x0 + 48, y0 + 34], fill=accent)
    d.line([(x0 + 46, y0 + 14), (x0 + 62, y0 + 22)], fill=accent, width=3)
    for i, yy in enumerate((y0 + 82, y0 + 90)):
        d.arc([x0 + 6 + i * 8, yy, x1 - 6 - i * 8, yy + 10], 0, 180, fill=(90, 140, 180), width=3)

def icon_jet(d, box, accent):
    x0, y0, x1, y1 = box
    # swept-wing jet, nose top-right
    d.polygon([(x1 - 8, y0 + 18), (x0 + 18, y0 + 56), (x0 + 8, y0 + 68),
               (x1 - 40, y0 + 56), (x1 - 52, y0 + 74), (x1 - 30, y0 + 44)],
              fill=accent)
    d.polygon([(x0 + 34, y0 + 52), (x0 + 46, y0 + 30), (x0 + 56, y0 + 52)],
              fill=(120, 120, 120))
    d.ellipse([x0 + 68, y0 + 12, x0 + 84, y0 + 22], fill=(200, 210, 220))
    d.ellipse([x0 + 8, y0 + 78, x0 + 24, y0 + 86], fill=(200, 210, 220))

def icon_flame(d, box, accent):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    # teardrop flame leaning right
    d.polygon([(cx + 6, y0 + 6), (cx + 28, y0 + 40), (cx + 20, y0 + 58),
               (cx + 26, y0 + 78), (cx + 10, y0 + 88), (cx - 12, y0 + 88),
               (cx - 26, y0 + 76), (cx - 18, y0 + 52), (cx - 24, y0 + 34),
               (cx - 6, y0 + 26)], fill=accent)
    d.polygon([(cx + 2, y0 + 44), (cx + 14, y0 + 60), (cx + 8, y0 + 78),
               (cx - 8, y0 + 78), (cx - 14, y0 + 62), (cx - 4, y0 + 50)],
              fill=(255, 200, 60))

def icon_cuffs(d, box, accent):
    x0, y0, x1, y1 = box
    d.ellipse([x0 + 8, y0 + 30, x0 + 44, y0 + 66], outline=accent, width=8)
    d.ellipse([x0 + 52, y0 + 30, x0 + 88, y0 + 66], outline=accent, width=8)
    d.line([(x0 + 44, y0 + 48), (x0 + 52, y0 + 48)], fill=accent, width=6)
    d.rectangle([x0 + 40, y0 + 20, x0 + 56, y0 + 30], fill=accent)

def icon_globe(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent, width=5)
    d.ellipse([cx - 11, cy - r, cx + 11, cy + r], outline=accent, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=accent, width=3)
    d.arc([cx - r, cy - 14, cx + r, cy + 14], 200, 340, fill=accent, width=3)

# ---------------- page ----------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 26  # margin

# masthead
spaced(d, (MX, 30), "THE WORLD IN ONE DAY", font(SANS_B, 20), RED, tracking=4)
d.text((MX, 56), "TUESDAY, 24 NOVEMBER 2026", font=font(SERIF_B, 52), fill=INK)
d.rectangle([MX, 128, W - MX, 133], fill=RED)
d.rectangle([MX, 137, W - MX, 139], fill=INK)
d.text((MX, 146), "The day's biggest stories \u2014 from Washington to Antalya",
       font=font(SANS, 19), fill=MUTED)

def panel(x, y, w, h, kicker, accent, headline, sub, icon=None):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD, outline=RULE, width=2)
    tx = x + 16
    if icon is not None:
        icon(d, (x + 16, y + 52, x + 112, y + 148), accent)
        tx = x + 128
    tw = x + w - 16 - tx
    d.text((tx, y + 12), kicker, font=font(SANS_B, 16), fill=accent)
    lines = wrap(d, headline, font(SERIF_B, 27), tw)
    yy = y + 36
    for ln in lines[:2]:
        d.text((tx, yy), ln, font=font(SERIF_B, 27), fill=INK)
        yy += 33
    lines = wrap(d, sub, font(SANS, 19), tw)
    for ln in lines[:3]:
        d.text((tx, yy + 4), ln, font=font(SANS, 19), fill=(60, 60, 60))
        yy += 24

# lead story
LY, LH = 176, 272
d.rounded_rectangle([MX, LY, W - MX, LY + LH], radius=8, fill=CARD, outline=RULE, width=2)
d.text((MX + 24, LY + 14), "UNITED STATES  \u00b7  TECHNOLOGY & MARKETS",
       font=font(SANS_B, 17), fill=GREEN)
d.text((MX + 24, LY + 42), "NVIDIA BRINGS", font=font(SERIF_B, 44), fill=INK)
d.text((MX + 24, LY + 92), "BACK HUANG", font=font(SERIF_B, 44), fill=INK)
lead_sub = ("Board votes unanimously to reinstate Jensen Huang, 11 days after "
            "his resignation \u2014 after direct pressure from President Trump. "
            "Shares jump 31%.")
lines = wrap(d, lead_sub, font(SANS, 21), 560)
yy = LY + 152
for ln in lines:
    d.text((MX + 24, yy), ln, font=font(SANS, 21), fill=(60, 60, 60))
    yy += 28
icon_chip(d, (W - MX - 236, LY + 40, W - MX - 56, LY + 220), GREEN)
# markets strip inside the lead card
d.rounded_rectangle([MX + 16, LY + LH - 40, W - MX - 16, LY + LH - 8],
                    radius=6, fill=STRIP)
d.text((MX + 32, LY + LH - 33), "MARKETS", font=font(SANS_B, 16), fill=DARKGREEN)
d.text((MX + 140, LY + LH - 33), "NVDA +31%    \u00b7    NASDAQ +6%    \u00b7    S&P 500 +4%",
       font=font(SANS_B, 17), fill=DARKGREEN)

# 2x2 grid
GY, GH, GAP = 462, 186, 14
GW = (W - 2 * MX - GAP) // 2
panel(MX, GY, GW, GH, "UKRAINE \u00b7 WAR AT SEA", (46, 90, 136),
      "Ukraine sinks Russian warship",
      "Sea drones sank the corvette Merkury off Benghazi; Moscow vows retaliation.",
      icon_ship)
panel(MX + GW + GAP, GY, GW, GH, "KOREA \u00b7 AIR DEFENCE", (15, 118, 110),
      "Russian jets enter Seoul's air zone",
      "Ulleung Island alert as Russian planes cross in; Seoul scrambles fighters.",
      icon_jet)
panel(MX, GY + GH + GAP, GW, GH, "MIDDLE EAST \u00b7 GULF STANDOFF", (194, 65, 12),
      "Iran\u2013US tensions rise in the Gulf",
      "Strikes step up under a US blockade; Trump warns of a \u201cvery traumatic\u201d outcome.",
      icon_flame)
panel(MX + GW + GAP, GY + GH + GAP, GW, GH, "MEXICO \u00b7 ORGANISED CRIME", (22, 101, 52),
      "Mexico captures \u2018El Chapo Isidro\u2019",
      "Alleged drug lord held; Mexico says it will try him at home, not extradite.",
      icon_cuffs)

# COP31 full-width card
CY, CH = 862, 66
d.rounded_rectangle([MX, CY, W - MX, CY + CH], radius=8, fill=CARD, outline=RULE, width=2)
icon_globe(d, (MX + 14, CY + 8, MX + 70, CY + 58), (15, 118, 110))
d.text((MX + 84, CY + 9), "CLIMATE  \u00b7  COP31, ANTALYA", font=font(SANS_B, 15), fill=(15, 118, 110))
d.text((W - MX - 16, CY + 10), "EU walks out as fossil-fuel wording is blocked.",
       font=font(SANS, 15), fill=(60, 60, 60), anchor="ra")
d.text((MX + 84, CY + 30), "Climate talks collapse \u2014 first no-deal since 2009",
       font=font(SERIF_B, 23), fill=INK)

# ticker (one line)
TY = 942
d.rounded_rectangle([MX, TY, W - MX, TY + 36], radius=8, fill=NAVY)
d.text((MX + 16, TY + 8), "ALSO TODAY", font=font(SANS_B, 16), fill=(255, 200, 60))
d.text((MX + 148, TY + 9),
       "NATO sends AWACS to Poland  \u2022  EU 22nd sanctions on Russia  \u2022  Bangladesh typhoid jabs for 50m children",
       font=font(SANS, 14), fill=(235, 235, 235))

# footer
d.text((W // 2, 990), "The day's news as reported on 24 November 2026  \u00b7  Sources: CNN \u00b7 AP \u00b7 Reuters \u00b7 USA Today \u00b7 The Independent",
       font=font(SANS, 14), fill=MUTED, anchor="ma")

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
