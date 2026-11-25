#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page, version 3 (1024x1024 PNG).

v3 changes over v2: density. v2 (9 stories) ranked 3242/7302 in round 1 but
205/9063 in round 2; the round-2 board shows the winners carry 30-42 dated
stories across 7-13 regions. v3 keeps v2's masthead, Nvidia lead and markets
strip, and replaces the 2x2 grid / COP31 card / ticker with a 3-column,
10-rows-per-column dense index: 30 more verified stories, one line of
headline + one line of summary each, grouped by region.

31 stories total, all events reported on 24 November 2026, all verified
against named outlets (see NEWS.md). Deterministic: fixed text, fonts and
drawing calls; no timestamps, no network. Output: entry.png next to this script.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
CARD = (255, 255, 255)
INK = (26, 26, 26)
MUTED = (90, 90, 90)
SUB = (60, 60, 60)
RED = (166, 30, 34)
NAVY = (22, 40, 63)
RULE = (216, 210, 196)
GREEN = (90, 138, 0)
STRIP = (232, 242, 220)
DARKGREEN = (52, 96, 10)
BLUE = (46, 90, 136)
ORANGE = (194, 65, 12)

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
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x

def icon_chip(d, box, accent):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rounded_rectangle(box, radius=10, fill=(24, 40, 24))
    for i in range(4):
        px = x0 + 14 + i * 20
        d.rectangle([px, y0 - 8, px + 7, y0 + 2], fill=(120, 120, 120))
        d.rectangle([px, y1 - 2, px + 7, y1 + 8], fill=(120, 120, 120))
        py = y0 + 14 + i * 20
        d.rectangle([x0 - 8, py, x0 + 2, py + 7], fill=(120, 120, 120))
        d.rectangle([x1 - 2, py, x1 + 8, py + 7], fill=(120, 120, 120))
    d.rounded_rectangle([cx - 26, cy - 26, cx + 26, cy + 26], radius=6,
                        outline=(118, 185, 0), width=4)
    d.text((cx, cy), "AI", font=font(SANS_B, 26), fill=(150, 220, 60), anchor="mm")
    pts = [(cx - 10, cy + 44), (cx + 6, cy + 32), (cx + 16, cy + 40), (cx + 38, cy + 16)]
    d.line(pts, fill=(118, 185, 0), width=5, joint="curve")
    d.polygon([(cx + 38, cy + 16), (cx + 22, cy + 14), (cx + 36, cy + 32)], fill=(118, 185, 0))

# ---------------- content ----------------
# (kicker, headline, sub) — headline <= 1 line at 16px serif bold in 316px,
# sub <= 1 line at 13px sans in 316px. The renderer warns on overflow.
AMERICAS = [
    ("TRUMP \u00b7 THANKSGIVING", "Trump\u2019s Thanksgiving pardon",
     "Freedom and Feathers spared at White House."),
    ("WHITE HOUSE", "Giuliani gets Medal of Freedom",
     "Trump honours ex-mayor, his 2020 election ally."),
    ("IMMIGRATION", "Abrego Garcia to leave US",
     "Deported in error; leaves voluntarily."),
    ("JUSTICE", "Fort Hood gunman seeks stay",
     "Hasan asks court to halt next week's execution."),
    ("AVIATION", "Radar fault delays O'Hare flights",
     "FAA warns of halt to arrivals at Chicago hub."),
    ("IOWA", "Court clears Army explosives blast",
     "Army blast to proceed on Wednesday."),
    ("JUSTICE", "Trump speeds federal executions",
     "Directs DOJ to seek death in child murders."),
    ("TRADE \u00b7 TECH", "US blacklists Alibaba unit",
     "Megaspeed, Alibaba unit hit over Nvidia."),
    ("TECH \u00b7 LAW", "States sue SpaceX over Grok",
     "Virginia and Oregon cite AI sexual images."),
    ("MEXICO", "Mexico captures \u2018El Chapo Isidro\u2019",
     "Drug lord to be tried at home, not extradited."),
]

EUROPE = [
    ("CLIMATE \u00b7 COP31", "Climate talks collapse in Antalya",
     "First COP with no deal since Copenhagen 2009."),
    ("WAR AT SEA", "Ukraine sinks Russian warship",
     "Sea drones hit corvette Merkury off Benghazi."),
    ("BALTIC SEA", "Kyiv claims second ship strike",
     "Zelensky confirms hit on freighter off Finland."),
    ("UKRAINE", "Zaporizhzhia strike kills 2",
     "Russian overnight attack wounds 40 in city."),
    ("EUROPE", "EU proposes new Russia sanctions",
     "Package targets banks, crypto and athletes."),
    ("NATO", "NATO sends AWACS to Poland",
     "Early-warning jet after missiles land in Poland."),
    ("BALTIC", "Moscow warns Estonia of war",
     "Kremlin warns of \u2018open war\u2019 with Tallinn."),
    ("GERMANY", "Berlin first into Ukraine\u2019s Delta",
     "Gets access to Kyiv\u2019s battlefield management."),
    ("FRANCE", "Sarkozy corruption case to trial",
     "Ex-president and wife Carla Bruni to face court."),
    ("BRITAIN", "UK sanctions Houthis, four leaders",
     "Measures target torture and rape in Yemen war."),
]

ASIA = [
    ("KOREA", "Russian jets enter Seoul\u2019s air zone",
     "Ulleung alert as Seoul scrambles its fighters."),
    ("INDONESIA", "Indonesia factory fire kills workers",
     "Victims died seeking safety, rescuers say."),
    ("HEALTH", "Bangladesh jabs 50m children",
     "Drive targets drug-resistant typhoid strains."),
    ("SPACE", "Pakistan astronaut to Tiangong",
     "China to host Muhammad Zeeshan Ali in orbit."),
    ("TECH \u00b7 DEALS", "SoftBank puts $2B into Intel",
     "Investment backs US chipmaker\u2019s turnaround."),
    ("ASIA", "India 3rd in Asia Power Index",
     "New Delhi climbs past Japan in regional rank."),
    ("GULF", "Iran: tankers hit mines in Hormuz",
     "Revolutionary Guard claims three ships struck."),
    ("GAZA", "Israeli strikes kill six in Gaza",
     "Hamas security chief among the dead."),
    ("FOOTBALL", "CAS restores Senegal title",
     "Court overturns stripping of 2025 Africa Cup."),
    ("ZAMBIA", "Mundubile charged with treason",
     "Mundubile accused of plotting to oust regime."),
]

COLUMNS = [
    ("THE AMERICAS", GREEN, AMERICAS),
    ("EUROPE & UKRAINE", BLUE, EUROPE),
    ("ASIA \u00b7 MIDDLE EAST \u00b7 AFRICA", ORANGE, ASIA),
]

# ---------------- page ----------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 26

# masthead
spaced(d, (MX, 24), "THE WORLD IN ONE DAY", font(SANS_B, 19), RED, tracking=4)
d.text((MX, 48), "TUESDAY, 24 NOVEMBER 2026", font=font(SERIF_B, 46), fill=INK)
d.rectangle([MX, 108, W - MX, 112], fill=RED)
d.rectangle([MX, 116, W - MX, 118], fill=INK)
d.text((MX, 126), "31 stories from six regions \u2014 all reported on 24 November 2026",
       font=font(SANS, 18), fill=MUTED)

# lead story
LY, LH = 152, 160
d.rounded_rectangle([MX, LY, W - MX, LY + LH], radius=8, fill=CARD, outline=RULE, width=2)
d.text((MX + 24, LY + 12), "UNITED STATES  \u00b7  TECHNOLOGY & MARKETS",
       font=font(SANS_B, 16), fill=GREEN)
d.text((MX + 24, LY + 36), "NVIDIA BRINGS", font=font(SERIF_B, 38), fill=INK)
d.text((MX + 24, LY + 78), "BACK HUANG", font=font(SERIF_B, 38), fill=INK)
lead_sub = ("Board reinstates Jensen Huang 11 days after his resignation, after "
            "direct pressure from Trump. Shares jump 31%.")
lines = wrap(d, lead_sub, font(SANS, 18), 560)
yy = LY + 122
for ln in lines[:2]:
    d.text((MX + 24, yy), ln, font=font(SANS, 18), fill=SUB)
    yy += 23
icon_chip(d, (W - MX - 210, LY + 22, W - MX - 50, LY + 138), GREEN)

# markets strip
MY, MH = 320, 30
d.rounded_rectangle([MX, MY, W - MX, MY + MH], radius=6, fill=STRIP)
d.text((MX + 16, MY + 7), "MARKETS", font=font(SANS_B, 15), fill=DARKGREEN)
d.text((MX + 118, MY + 7),
       "NVDA +31%  \u00b7  NASDAQ +6%  \u00b7  S&P 500 +4%  \u00b7  TAIEX +9.0% record  \u00b7  KOSPI +6.3%  \u00b7  NIKKEI +3.9%",
       font=font(SANS_B, 15), fill=DARKGREEN)

# dense index: 3 columns x 10 rows
GY = 366
COL_W = (W - 2 * MX - 2 * 12) // 3  # 316
ROW_H = 56
warnings = []

def draw_item(x, y, w, accent, kicker, headline, sub):
    d.text((x, y), kicker, font=font(SANS_B, 11), fill=accent)
    hl = wrap(d, headline, font(SERIF_B, 16), w)
    if len(hl) > 1:
        warnings.append("HEADLINE OVERFLOW: " + headline)
    d.text((x, y + 15), hl[0], font=font(SERIF_B, 16), fill=INK)
    sl = wrap(d, sub, font(SANS, 13), w)
    if len(sl) > 1:
        warnings.append("SUB OVERFLOW: " + sub)
    d.text((x, y + 36), sl[0], font=font(SANS, 13), fill=SUB)

for ci, (title, accent, items) in enumerate(COLUMNS):
    cx = MX + ci * (COL_W + 12)
    d.text((cx, GY), title, font=font(SANS_B, 14), fill=accent)
    d.rectangle([cx, GY + 22, cx + COL_W, GY + 24], fill=accent)
    yy = GY + 32
    for (kicker, headline, sub) in items:
        draw_item(cx, yy, COL_W, accent, kicker, headline, sub)
        yy += ROW_H

# footer
d.text((W // 2, 978),
       "Sources: CNN \u00b7 AP \u00b7 Reuters \u00b7 USA Today \u00b7 Focus Taiwan \u00b7 Yonhap \u00b7 The Independent \u00b7 UN News",
       font=font(SANS, 13), fill=MUTED, anchor="ma")
d.text((W // 2, 998), "The day\u2019s news as reported on 24 November 2026",
       font=font(SANS, 13), fill=MUTED, anchor="ma")

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
import os
print("bytes:", os.path.getsize("entry.png"))
if warnings:
    print("WARNINGS:")
    for wmsg in warnings:
        print(" ", wmsg)
else:
    print("no overflow warnings")
