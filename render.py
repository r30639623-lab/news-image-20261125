"""Front page renderer: The World Today, Wednesday 25 November 2026.

Draws a 1024x1024 newspaper front page with 35 stories across 7 regions:
masthead, six stat boxes, three feature panels, ten medium cards, a world
map with 22 numbered pins, a two-column story list, a date-check strip and
a footer. Pure Pillow, no network, no external assets.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 28
RIGHT = 996

CREAM = (247, 243, 232)
WHITE = (255, 255, 255)
INK = (17, 17, 17)
RED = (176, 30, 36)
GRAY_BODY = (150, 140, 125)
GRAY_DARK = (107, 98, 87)
PILL_BG = (238, 231, 214)
STRIP_BG = (226, 231, 235)
CHESS_LIGHT = (240, 217, 181)
CHESS_DARK = (181, 136, 99)
LAND = (214, 203, 175)
LAND_EDGE = (180, 168, 140)
GREEN_A = (34, 110, 60)
GREEN_B = (42, 125, 68)
NAVY_TOP = (12, 18, 38)
NAVY_BOT = (35, 44, 69)
MOON = (235, 230, 205)
FLAME = (255, 170, 40)
BORDER = (205, 200, 188)
RULE = (17, 17, 17)

DEJAVU = "/usr/share/fonts/truetype/dejavu/"
LIBER = "/usr/share/fonts/truetype/liberation/"


def F(path, size):
    return ImageFont.truetype(path, size)


FONTS = {
    "title": F(DEJAVU + "DejaVuSerif-Bold.ttf", 62),
    "subtitle": F(DEJAVU + "DejaVuSans-Bold.ttf", 20),
    "redline": F(LIBER + "LiberationSans-Bold.ttf", 15),
    "ticker": F(DEJAVU + "DejaVuSerif.ttf", 14),
    "region": F(DEJAVU + "DejaVuSans-Bold.ttf", 14),
    "stat_num": F(DEJAVU + "DejaVuSans-Bold.ttf", 21),
    "stat_cap": F(DEJAVU + "DejaVuSans.ttf", 8),
    "panel_head": F(DEJAVU + "DejaVuSerif-Bold.ttf", 17),
    "card_head": F(DEJAVU + "DejaVuSerif-Bold.ttf", 12),
    "panel_body": F(DEJAVU + "DejaVuSans.ttf", 7),
    "card_body": F(DEJAVU + "DejaVuSans.ttf", 7),
    "bar": F(DEJAVU + "DejaVuSans-Bold.ttf", 11),
    "card_bar": F(DEJAVU + "DejaVuSans-Bold.ttf", 10),
    "loc": F(DEJAVU + "DejaVuSans-Bold.ttf", 9),
    "pill": F(DEJAVU + "DejaVuSans-Bold.ttf", 9),
    "source": F(DEJAVU + "DejaVuSans.ttf", 10),
    "list": F(DEJAVU + "DejaVuSerif.ttf", 8),
    "list_b": F(DEJAVU + "DejaVuSerif-Bold.ttf", 8),
    "datecheck": F(DEJAVU + "DejaVuSans.ttf", 7),
    "footer": F(DEJAVU + "DejaVuSans.ttf", 10),
    "pin": F(DEJAVU + "DejaVuSans-Bold.ttf", 7),
    "chess": F(DEJAVU + "DejaVuSans.ttf", 26),
    "matchday": F(DEJAVU + "DejaVuSans-Bold.ttf", 13),
    "map_head": F(DEJAVU + "DejaVuSerif-Bold.ttf", 16),
}


def wrap(draw, text, font, max_w):
    """Greedy word wrap, returns a list of lines fitting max_w pixels."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_center(draw, cx, top, text, font, fill):
    draw.text((cx, top), text, font=font, fill=fill, anchor="ma")


def text_left(draw, x, top, text, font, fill):
    draw.text((x, top), text, font=font, fill=fill, anchor="la")


def text_right(draw, x, top, text, font, fill):
    draw.text((x, top), text, font=font, fill=fill, anchor="ra")


TITLE = "THE WORLD TODAY"
SUBTITLE = "WEDNESDAY, 25 NOVEMBER 2026"
REDLINE = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
TICKER = ("Shenzhou 24 carries Pakistan's first astronaut \u00b7 "
          "Gukesh takes White in Game 2 \u00b7 "
          "Nine Champions League ties tonight")
REGION_BAR = ("AMERICAS 2 \u00b7 EUROPE 5 \u00b7 MIDDLE EAST 1 \u00b7 ASIA 4 \u00b7 "
              "AFRICA 5 \u00b7 OCEANIA 16 \u00b7 GLOBAL 2")

STATS = [
    ("3", "crew aboard", "Shenzhou 24"),
    ("14", "games in the", "chess title match"),
    ("9", "Champions League", "ties tonight"),
    ("63", "measles cases", "in Sydney in 2026"),
    ("$5.9m", "lost to NZ cyber", "breaches"),
    ("\u00a5300bn", "Japan bond sale", "due today"),
]

PANELS = [
    {
        "num": "1", "cat": "SPACE", "loc": "JIUQUAN",
        "headline": "Shenzhou 24 lifts off with Pakistan's first astronaut",
        "body": ("China's Long March 2F launched from Jiuquan at 00:18 UTC. "
                 "Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali \u2014 the first "
                 "Pakistani in orbit \u2014 dock with Tiangong."),
        "pill": "3 crew \u00b7 first Pakistani in orbit",
        "source": "CMSA, Reuters",
        "kind": "rocket",
    },
    {
        "num": "2", "cat": "CHESS", "loc": "GENEVA",
        "headline": "", "body": "", "pill": "", "source": "",
        "kind": "chess",
    },
    {
        "num": "3", "cat": "FOOTBALL", "loc": "EUROPE",
        "headline": "Nine Champions League ties light up Wednesday",
        "body": ("Matchday 5: PSG host Roma, Sporting CP face Manchester "
                 "United, Lille meet Bayern and Club Brugge take on "
                 "Liverpool, plus five more ties."),
        "pill": "9 ties \u00b7 Matchday 5",
        "source": "UEFA",
        "kind": "pitch",
    },
]

CARDS = [
    ("4", "POLITICS", "BRUSSELS \u00b7 EU",
     "EU hosts Western Balkans summit",
     "Costa and von der Leyen host six Balkan leaders; enlargement and security on the table.",
     "arrow"),
    ("5", "ECONOMY", "WASHINGTON \u00b7 BEA, Fed",
     "US data day: PCE, GDP and Beige Book due",
     "PCE inflation, Q3 GDP, jobless claims and the Beige Book land before Thanksgiving.",
     "chart"),
    ("6", "SCIENCE", "BERLIN \u00b7 ESA",
     "Hera shows first Dimorphos images",
     "ESA presents the first detailed images of the asteroid after the DART impact, in Berlin today.",
     "globe"),
    ("7", "POLITICS", "RIYADH \u00b7 reports",
     "Lebanon and Qatar condemn Houthi strike",
     "Beirut and Doha condemn Tuesday's drone strike on the PIF tower, which wounded 11 people.",
     "arrow"),
    ("8", "POLITICS", "CANBERRA \u00b7 ABC",
     "Chalmers flags public service cuts",
     "The Treasurer says the government will save more than it spends in its mid-year budget update.",
     "check"),
    ("9", "MARKETS", "SYDNEY \u00b7 ABC",
     "ASX set to slip as Wall Street retreats",
     "All stocks were dumped again on Wall Street; the ASX is set to fall ahead of inflation data.",
     "chart"),
    ("10", "SPORT", "MELBOURNE \u00b7 ABC",
     "Sinner set to miss Australian Open",
     "The world No. 1 is set to miss the year's first Grand Slam, leaving the men's draw wide open.",
     "ball"),
    ("11", "SPORT", "BHOPAL \u00b7 Hockey India",
     "Unbeaten India meet unbeaten Japan tonight",
     "India and Japan, both on 12 points, meet in the final round-robin game at 19:00 IST.",
     "ball"),
    ("12", "ECONOMY", "TOKYO \u00b7 reports",
     "Tokyo steadies after 5% rout; bond sale due",
     "The Nikkei is back after the holiday, and a \u00a5300bn 40-year bond auction is set for today.",
     "chart"),
    ("13", "CULTURE", "LONDON \u00b7 ABC",
     "Charles and Elton John hail Molly Meldrum",
     "Tributes pour in for the Australian music icon, who has died aged 83.",
     "bird"),
]

ITEMS = [
    (14, "MELBOURNE", "Firefighter in induced coma after tanker blaze", "ABC"),
    (15, "ROBE", "Golf course plan risks Aboriginal heritage", "ABC"),
    (16, "BRISBANE", "100+ clubs threaten Football Qld breakaway", "ABC"),
    (17, "BRISBANE", "Queensland $2-a-litre petrol as biofuel bill fails", "ABC"),
    (18, "PERTH", "Teen on trial over nurse's death in park", "ABC"),
    (19, "SYDNEY", "Measles alert as cases reach 63 this year", "ABC"),
    (20, "CANBERRA", "Housing downturn brings no relief to buyers", "ABC"),
    (21, "WELLINGTON", "Flavell slams ACT's Maori seats referendum idea", "RNZ"),
    (22, "WELLINGTON", "AI blamed as cyber breaches surge", "RNZ"),
    (23, "WELLINGTON", "Kainga Ora homes pitched to land bankers", "RNZ"),
    (24, "WELLINGTON", "No student barred from exam re-sit, NZQA told", "RNZ"),
    (25, "CHRISTCHURCH", "Fonterra pressed for more on milk-dump plan", "RNZ"),
    (26, "JAYAPURA", "Probe call after West Papuan student leader dies", "RNZ"),
    (27, "WELLINGTON", "COP31 format needs re-think, envoys say", "RNZ"),
    (28, "DAKAR", "CAF to comply with CAS ruling restoring Senegal", "reports"),
    (29, "DAKAR", "MPs meet today on budget decree", "reports"),
    (30, "JOHANNESBURG", "Madlanga: Witness T's secrets", "Daily Maverick"),
    (31, "CAPE TOWN", "CPUT students pay R76k for roaches", "Daily Maverick"),
    (32, "JOHANNESBURG", "ANC decline 'a referendum on us'", "Daily Maverick"),
    (33, "BERLIN", "R\u00f6ttgen attacks AfD on Miosga", "ARD"),
    (34, "BRUSSELS", "Belgian state bonds on sale from today", "reports"),
    (35, "LOS ANGELES", "Blade Runner 2099 premieres on Prime", "ABC"),
]

# lon/lat per story number, for the map pins.
PIN_LONLAT = {
    14: (144.96, -37.81), 15: (139.76, -37.16), 16: (153.03, -27.47),
    17: (152.45, -27.95), 18: (115.86, -32.07), 19: (151.21, -33.87),
    20: (149.13, -35.28), 21: (174.78, -41.29), 22: (174.30, -41.55),
    23: (175.10, -41.05), 24: (174.55, -41.45), 25: (172.64, -43.53),
    26: (140.72, -2.53), 27: (174.95, -41.10), 28: (-17.47, 14.69),
    29: (-17.05, 14.45), 30: (28.05, -26.20), 31: (18.42, -33.92),
    32: (28.45, -26.45), 33: (13.40, 52.52), 34: (4.35, 50.85),
    35: (-118.24, 34.05),
}

# Simplified continent outlines, in page pixels.
CONTINENTS = [
    # North America
    [(42, 778), (70, 770), (110, 768), (140, 775), (152, 788),
     (140, 805), (128, 825), (115, 840), (100, 832), (88, 812),
     (60, 800), (40, 788)],
    # Greenland
    [(188, 762), (205, 756), (216, 766), (208, 779), (192, 776)],
    # South America
    [(108, 845), (130, 840), (142, 858), (135, 885), (122, 905),
     (110, 898), (103, 872), (100, 855)],
    # Europe
    [(196, 776), (214, 770), (230, 778), (226, 793), (210, 796), (198, 786)],
    # Africa
    [(192, 812), (220, 805), (242, 818), (240, 850), (230, 885),
     (215, 900), (200, 878), (188, 845), (186, 822)],
    # Asia
    [(235, 770), (290, 762), (340, 768), (356, 782), (350, 805),
     (335, 822), (312, 828), (290, 818), (268, 802), (245, 790), (233, 780)],
    # Australia
    [(298, 920), (330, 912), (352, 922), (352, 942), (335, 952),
     (308, 950), (296, 935)],
    # New Zealand
    [(350, 938), (357, 936), (360, 946), (353, 951)],
]

DATE_CHECK = ("DATE CHECK \u2014 Left out as earlier news: the Houthi strike on "
              "the Riyadh tower itself, the Hamas security chief killed in Gaza "
              "and Katz's Iran warning (Tue 24 Nov); the BJP-Akali Dal reunion "
              "and the Landmine Monitor report (Tue); the Russian war-dead leak "
              "(Mon 23 Nov); the ICJ's Myanmar ruling (Thu 19 Nov); the Ariane 6 "
              "launch (Tue). Every story here happened, or was first reported, "
              "on Wed 25 Nov 2026.")

FOOTER = ("Compiled from major wire reports \u00b7 25 November 2026 "
          "\u00b7 PAGE 1 OF 1")


PANEL_X = [28, 354, 680]
PANEL_W = 314
PANEL_TOP = 260
PANEL_BOT = 492
CARD_X = [28, 222, 416, 610, 804]
CARD_W = 188
CARD_ROWS = [502, 622]
CARD_H = 112


def draw_header(draw):
    text_center(draw, 512, 16, TITLE, FONTS["title"], INK)
    text_center(draw, 512, 88, SUBTITLE, FONTS["subtitle"], INK)
    text_center(draw, 512, 115, REDLINE, FONTS["redline"], RED)
    text_center(draw, 512, 136, TICKER, FONTS["ticker"], GRAY_DARK)
    draw.rectangle([MARGIN, 158, RIGHT, 159], fill=RULE)


def draw_stats(draw):
    xs = [28, 190, 352, 514, 676, 838]
    for i, (num, cap1, cap2) in enumerate(STATS):
        x0 = xs[i]
        x1 = x0 + 156
        draw.rectangle([x0, 168, x1, 220], fill=WHITE, outline=BORDER)
        text_center(draw, (x0 + x1) // 2, 177, num, FONTS["stat_num"], RED)
        text_center(draw, (x0 + x1) // 2, 203, cap1, FONTS["stat_cap"], GRAY_DARK)
        text_center(draw, (x0 + x1) // 2, 211, cap2, FONTS["stat_cap"], GRAY_DARK)
    text_center(draw, 512, 229, REGION_BAR, FONTS["region"], INK)
    draw.rectangle([MARGIN, 250, RIGHT, 251], fill=RULE)


def draw_bar(draw, x0, x1, top, num, cat, loc):
    draw.rectangle([x0, top, x1, top + 22], fill=RED)
    text_left(draw, x0 + 8, top + 6, num + " " + cat, FONTS["bar"], WHITE)
    text_right(draw, x1 - 8, top + 6, loc, FONTS["bar"], WHITE)


def draw_pill(draw, x, y, text, source=None, right=None):
    tw = draw.textlength(text, font=FONTS["pill"])
    w = int(tw) + 18
    draw.rounded_rectangle([x, y, x + w, y + 17], radius=8, fill=PILL_BG)
    text_center(draw, x + w // 2, y + 4, text, FONTS["pill"], INK)
    if source and right:
        text_right(draw, right, y + 3, source, FONTS["source"], GRAY_DARK)
    return w


def draw_sky(draw):
    x0, y0, w, h = 36, 390, 298, 95
    for yy in range(h):
        t = yy / max(h - 1, 1)
        r = int(NAVY_TOP[0] + (NAVY_BOT[0] - NAVY_TOP[0]) * t)
        g = int(NAVY_TOP[1] + (NAVY_BOT[1] - NAVY_TOP[1]) * t)
        b = int(NAVY_TOP[2] + (NAVY_BOT[2] - NAVY_TOP[2]) * t)
        draw.line([(x0, y0 + yy), (x0 + w, y0 + yy)], fill=(r, g, b))
    # stars
    for sx, sy in [(60, 400), (95, 415), (130, 398), (160, 420), (230, 405),
                   (255, 425), (285, 400), (320, 430), (75, 440), (270, 445)]:
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=WHITE)
    # moon
    draw.ellipse([301, 401, 323, 423], fill=MOON)
    # rocket: nose, body, window, fins, flame
    draw.polygon([(185, 400), (172, 432), (198, 432)], fill=RED)
    draw.rectangle([174, 432, 196, 462], fill=(240, 240, 240))
    draw.ellipse([179, 439, 191, 451], fill=(120, 170, 210))
    draw.polygon([(174, 452), (160, 472), (174, 468)], fill=RED)
    draw.polygon([(196, 452), (210, 472), (196, 468)], fill=RED)
    draw.polygon([(178, 462), (192, 462), (185, 480)], fill=FLAME)
    # low clouds
    for cx0, cy0, cx1, cy1 in [(55, 472, 115, 483), (135, 474, 190, 484),
                               (235, 470, 300, 482)]:
        draw.ellipse([cx0, cy0, cx1, cy1], fill=(200, 200, 200))
    draw.line([(x0, 483), (x0 + w, 483)], fill=(90, 90, 90), width=2)


def draw_chess(draw):
    x0, y0, w, h = 364, 292, 294, 199
    cw = w / 8.0
    ch = h / 8.0
    for row in range(8):
        for col in range(8):
            fill = CHESS_LIGHT if (row + col) % 2 == 0 else CHESS_DARK
            draw.rectangle([x0 + col * cw, y0 + row * ch,
                            x0 + (col + 1) * cw, y0 + (row + 1) * ch],
                           fill=fill)
    pieces = [("\u265c", 0, 0, INK), ("\u2654", 0, 4, INK),
              ("\u265f", 5, 4, INK), ("\u2659", 6, 3, CHESS_LIGHT),
              ("\u2658", 7, 7, CHESS_LIGHT)]
    for glyph, row, col, color in pieces:
        cx = x0 + (col + 0.5) * cw
        cy = y0 + (row + 0.5) * ch
        draw.text((cx, cy), glyph, font=FONTS["chess"], fill=color, anchor="mm")


def draw_pitch(draw):
    x0, y0, w, h = 688, 390, 298, 96
    band = w / 6.0
    for i in range(6):
        fill = GREEN_A if i % 2 == 0 else GREEN_B
        draw.rectangle([x0 + i * band, y0, x0 + (i + 1) * band, y0 + h], fill=fill)
    # white markings
    draw.rectangle([692, 394, 982, 482], outline=WHITE, width=2)
    draw.line([(837, 394), (837, 482)], fill=WHITE, width=2)
    draw.ellipse([811, 412, 863, 464], outline=WHITE, width=2)
    # pale ball, top left
    draw.ellipse([706, 401, 724, 419], fill=MOON, outline=(150, 140, 125))
    # soccer ball, right of centre
    draw.ellipse([865, 423, 895, 453], fill=WHITE, outline=INK, width=2)
    draw.polygon([(880, 432), (888, 438), (885, 447), (875, 447), (872, 438)],
                 fill=INK)
    text_left(draw, 700, 466, "MATCHDAY 5", FONTS["matchday"], WHITE)


def draw_panel(draw, idx, panel):
    x0 = PANEL_X[idx]
    x1 = x0 + PANEL_W
    draw.rectangle([x0, PANEL_TOP, x1, PANEL_BOT], fill=WHITE, outline=BORDER)
    draw_bar(draw, x0, x1, PANEL_TOP, panel["num"], panel["cat"], panel["loc"])
    kind = panel["kind"]
    if kind == "chess":
        draw_chess(draw)
        return
    lines = wrap(draw, panel["headline"], FONTS["panel_head"], 298)
    y = 290
    for line in lines:
        text_left(draw, x0 + 8, y, line, FONTS["panel_head"], INK)
        y += 25
    body = wrap(draw, panel["body"], FONTS["panel_body"], 298)
    y = 344
    for line in body:
        text_left(draw, x0 + 8, y, line, FONTS["panel_body"], (40, 40, 40))
        y += 10
    draw_pill(draw, x0 + 8, 366, panel["pill"], panel["source"], x1 - 8)
    if kind == "rocket":
        draw_sky(draw)
    elif kind == "pitch":
        draw_pitch(draw)


def draw_strip_icon(draw, x0, y0, w, kind):
    """Small graphic inside a card's bottom strip."""
    h = 22
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=STRIP_BG, outline=(150, 140, 125))
    cy = y0 + h // 2
    if kind == "arrow":
        draw.polygon([(x0 + 10, cy - 7), (x0 + 10, cy + 7), (x0 + 28, cy)],
                     fill=RED)
    elif kind == "chart":
        draw.line([(x0 + 6, cy), (x0 + w - 6, cy)], fill=INK, width=1)
        pts = [(x0 + 12, cy + 2), (x0 + 45, cy - 2), (x0 + 70, cy + 6),
               (x0 + 95, cy - 4), (x0 + 120, cy + 1), (x0 + 145, cy - 3)]
        draw.line(pts, fill=RED, width=2)
        for px, py in pts:
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
    elif kind == "globe":
        cx, cy2 = x0 + w - 26, cy
        draw.ellipse([cx - 11, cy2 - 11, cx + 11, cy2 + 11],
                     fill=(140, 180, 210), outline=(40, 80, 130))
        draw.ellipse([cx - 4, cy2 - 11, cx + 4, cy2 + 11],
                     outline=(40, 80, 130))
        draw.line([(cx - 11, cy2), (cx + 11, cy2)], fill=(40, 80, 130))
    elif kind == "check":
        cx = x0 + w - 26
        draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11],
                     outline=INK, width=2)
        draw.line([(cx - 6, cy), (cx - 1, cy + 5), (cx + 7, cy - 6)],
                  fill=RED, width=3)
    elif kind == "ball":
        cx = x0 + w - 26
        draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11],
                     fill=WHITE, outline=INK, width=2)
        draw.polygon([(cx, cy - 5), (cx + 5, cy - 1), (cx + 3, cy + 5),
                      (cx - 3, cy + 5), (cx - 5, cy - 1)], fill=INK)
    elif kind == "bird":
        cx, cy2 = x0 + w - 30, cy
        draw.ellipse([cx - 12, cy2 - 5, cx + 8, cy2 + 6], fill=WHITE,
                     outline=INK)
        draw.ellipse([cx + 6, cy2 - 9, cx + 14, cy2 - 1], fill=WHITE,
                     outline=INK)
        draw.polygon([(cx + 13, cy2 - 6), (cx + 20, cy2 - 4), (cx + 13, cy2 - 2)],
                     fill=FLAME)


def draw_card(draw, idx, card):
    num, cat, loc, headline, body, icon = card
    row = idx // 5
    col = idx % 5
    x0 = CARD_X[col]
    x1 = x0 + CARD_W
    y0 = CARD_ROWS[row]
    y1 = y0 + CARD_H
    draw.rectangle([x0, y0, x1, y1], fill=WHITE, outline=BORDER)
    draw.rectangle([x0, y0, x1, y0 + 16], fill=RED)
    text_left(draw, x0 + 6, y0 + 4, num + " " + cat, FONTS["card_bar"], WHITE)
    text_left(draw, x0 + 6, y0 + 21, loc, FONTS["loc"], GRAY_DARK)
    lines = wrap(draw, headline, FONTS["card_head"], 180)
    y = y0 + 30
    for line in lines:
        text_left(draw, x0 + 5, y, line, FONTS["card_head"], INK)
        y += 17
    body_lines = wrap(draw, body, FONTS["card_body"], 176)
    y = y0 + 66
    for line in body_lines:
        text_left(draw, x0 + 5, y, line, FONTS["card_body"], (40, 40, 40))
        y += 10
    draw_strip_icon(draw, x0 + 6, y0 + 89, CARD_W - 12, icon)


def draw_map(draw):
    draw.rectangle([29, 775, 357, 967], fill=(226, 232, 235))
    text_left(draw, MARGIN, 742, "WHERE IT HAPPENED", FONTS["map_head"], INK)
    draw.rectangle([MARGIN, 766, RIGHT, 767], fill=RULE)
    for poly in CONTINENTS:
        draw.polygon(poly, fill=LAND, outline=LAND_EDGE)
    for num, (lon, lat) in PIN_LONLAT.items():
        x = 195 + 0.95 * lon
        y = 883 - 1.50 * lat
        draw.ellipse([x - 6, y - 6, x + 6, y + 6], fill=RED, outline=WHITE)
        draw.text((x, y), str(num), font=FONTS["pin"], fill=WHITE, anchor="mm")


def draw_list(draw):
    cols = [(373, 0), (690, 11)]
    for x0, start in cols:
        y = 774
        for num, city, text, source in ITEMS[start:start + 11]:
            head = "%d. %s \u2014 " % (num, city)
            rest = "%s (%s)" % (text, source)
            text_left(draw, x0, y, head, FONTS["list_b"], INK)
            w = draw.textlength(head, font=FONTS["list_b"])
            text_left(draw, x0 + w, y, rest, FONTS["list"], INK)
            y += 18


def draw_bottom(draw):
    draw.rectangle([MARGIN, 968, RIGHT, 1002], fill=(255, 245, 244),
                   outline=RED, width=2)
    lines = wrap(draw, DATE_CHECK, FONTS["datecheck"], 952)
    y = 972
    for line in lines:
        text_left(draw, MARGIN + 8, y, line, FONTS["datecheck"], (90, 20, 20))
        y += 11
    text_center(draw, 512, 1007, FOOTER, FONTS["footer"], GRAY_DARK)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_stats(draw)
    for i, panel in enumerate(PANELS):
        draw_panel(draw, i, panel)
    for i, card in enumerate(CARDS):
        draw_card(draw, i, card)
    draw_map(draw)
    draw_list(draw)
    draw_bottom(draw)
    return img


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "news.png")
    build().save(out)
    print("wrote", out)
