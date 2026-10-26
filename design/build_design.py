#!/usr/bin/env python3
"""Assemble the Outer Bounds Pro complete design into one self-contained HTML file.

  python3 build_design.py  ->  design/outer-bounds-pro-design.html

Sources: model.py (mechanical), drawings.py (sheets), netlist.py + schematic.py (electrical),
viewer.js (WebGL), ../bom/bom-data.json (purchased-item prices & vendors).
"""
import json, os, math
from html import escape
import model as M
import drawings as DW
from netlist import D

HERE = os.path.dirname(os.path.abspath(__file__))
BOM = json.load(open(os.path.join(HERE, "..", "bom", "bom-data.json")))
BL = {l["id"]: l for l in BOM["lines"]}
T = 2   # @1k column

# ---------------------------------------------------------------- PCBA roll-ups from the netlist
rows = D.bom_rows()
boards = {"CB": ("PCBA-CB", "Main carrier PCBA (10L HDI 160×92)", 1), "LB": ("PCBA-LB", "LED strobe PCBA (4L 40×30)", 3),
          "RH": ("PCBA-RH", "Radar head PCBA (4L 24×24)", 2), "BP": ("PCBA-BP", "Battery pack BMS (built by pack OEM)", 1)}
pcba_parts = {b: sum(r["qty"] * r["price"] for r in rows if r["board"] == b) for b in boards}
pcba_lines = {b: sum(1 for r in rows if r["board"] == b) for b in boards}
pcba_count = {b: sum(r["qty"] for r in rows if r["board"] == b) for b in boards}
fab = {"CB": (20 + 5 + 4.0), "LB": (0.70 + 0.9), "RH": (0.85 + 0.6), "BP": 0}   # bare board + assembly @1k

L1 = []   # level-1 (top assembly) BOM: (id, item, mfr, mpn, qty, unit@1k, source/vendor, url, status, note)
def l1(id_, item, mfr, mpn, qty, unit, vendor, url="", status="now", note=""):
    L1.append(dict(id=id_, item=item, mfr=mfr, mpn=mpn, qty=qty, unit=round(unit, 2), vendor=vendor, url=url, status=status, note=note))

for b, (pid, name, q) in boards.items():
    if b == "BP":
        continue
    l1(pid, name, "Outer Bounds (CM build)", f"OB-{b} rev A", q, pcba_parts[b] + fab[b], "Taiwan/Vietnam CM", "", "design",
       f"{pcba_lines[b]} BOM lines / {pcba_count[b]} placements per board (Level-2 BOM below) + bare board & assembly ${fab[b]:.2f}")
def frombom(id_, qty=None, override=None, note=""):
    l = BL[id_]
    l1(id_, l["item"], l["mfr"], l["mpn"], qty or l["qp"], override if override is not None else l["price"][T], l["vendor"], l["url"], l["status"], note or l["notes"][:140])
frombom("PWR-12", note="Smart pack built by OEM to schematic BP-01 (cells, BQ40Z50-R2, BQ771807, TE 787439-1). UN38.3 / IEC 62133-2.")
for i in ("CAM-01", "CAM-02", "CAM-03", "CAM-04", "CAM-05", "CAM-06"):
    frombom(i)
frombom("CPU-02")
frombom("UI-01"); frombom("UI-03"); frombom("THM-01"); frombom("THM-03"); frombom("THM-04")
for i in ("MEC-01", "MEC-02", "MEC-03", "MEC-04", "MEC-05", "MEC-06", "MEC-07", "MEC-08", "MEC-09", "MEC-10", "LED-11", "RAD-06"):
    frombom(i)
for x in L1:   # LED cable went to 10 positions (2 GND + Kelvin sense return) in rev A.1
    if x["id"] == "LED-11":
        x["item"], x["mpn"], x["unit"], x["note"] = "LED-board cable assembly, 10-pos (GHR-10V-S + SSHL crimps)", "GHR-10V-S", round(x["unit"] + 0.12, 2), "2 GND returns + Kelvin sense return per board"
l1("MEC-11", "Display/button silicone gasket + IP67 button caps (molded)", "Silicone molder", "OB-KEYPAD rev A", 1, 0.45, "RFQ", "", "design", "Seals SW1–SW3 and LED light-pipe")
l1("MEC-12", "Grip bar (PA6-GF30 core + TPE overmold) and crown fasteners", "Two-shot molder", "OB-GRIP rev A", 1, 1.85, "RFQ", "", "design", "Hidden top carry grip, flush with the crown")
for i in ("PWR-14", "BOX-01", "BOX-02", "BOX-03", "BOX-04", "BOX-05", "BOX-06", "LAB-01"):
    frombom(i)
l1_total = sum(x["qty"] * x["unit"] for x in L1)
landed = l1_total * 1.03 * 1.10 + 12

# ---------------------------------------------------------------- 3D gallery (static shaded renders)
P = M.build()
def render(view, k, w, h, explode=0.0, hide=()):
    prims = [p for p in P if p["g"] not in hide]
    body = DW.project(prims, view, w/2, h/2, k, explode=explode, style="shade")
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">{body}</svg>'
SHELL = set(M.SHELL_GROUPS)
SH = sorted(SHELL)
gallery = [
    ("Front", dict(az=-32, el=16, dist=620, target=[0, 20, 0])),
    ("Rear", dict(az=148, el=18, dist=620, target=[0, 20, 0])),
    ("Hidden grip, from above", dict(az=25, el=58, dist=560, target=[0, 40, 0])),
    ("Underside", dict(az=-30, el=-38, dist=620, target=[0, 20, 0])),
    ("Internals", dict(az=-35, el=20, dist=560, target=[0, 10, 0], hide=SH)),
    ("Exploded", dict(az=-38, el=22, dist=980, target=[0, 30, 0], explode=1.0)),
    ("In use, wide", dict(az=-135, el=28, dist=5600, target=[1100, 300, 500], setup=True)),
    ("Target end", dict(az=100, el=24, dist=620, target=[0, 20, 0])),
]

# ---------------------------------------------------------------- block diagram + power tree (SVG)
def blk(x, y, w, h, t, sub="", col="#e6f0fc", stroke="#2a78d6"):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{col}" stroke="{stroke}" stroke-width="1.4"/>'
    s += f'<text x="{x+w/2}" y="{y+(h/2 if not sub else h/2-6)+4}" text-anchor="middle" font-size="13" font-weight="700" fill="#0b0b0b">{escape(t)}</text>'
    if sub:
        s += f'<text x="{x+w/2}" y="{y+h/2+12}" text-anchor="middle" font-size="10.5" fill="#52514e">{escape(sub)}</text>'
    return s
def arr(x1, y1, x2, y2, lab="", col="#52514e", dash=False):
    d = ' stroke-dasharray="5 4"' if dash else ""
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1.6" marker-end="url(#ah)"{d}/>'
    if lab:
        s += f'<text x="{(x1+x2)/2+4}" y="{(y1+y2)/2-5}" font-size="10.5" fill="{col}" font-family="ui-monospace,Menlo,monospace">{escape(lab)}</text>'
    return s
DEF = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#52514e"/></marker></defs>'
def poly(pts, lab="", lx=0, ly=0, dash=False, col="#52514e"):
    d = ' stroke-dasharray="5 4"' if dash else ""
    s = f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="1.6" marker-end="url(#ah)"{d}/>'
    if lab:
        s += f'<text x="{lx}" y="{ly}" font-size="10.5" fill="{col}" font-family="ui-monospace,Menlo,monospace">{escape(lab)}</text>'
    return s
bd = [DEF]
bd += [blk(30, 40, 180, 60, "3× IMX900 cameras", "VK000601 · 940 nm filter", "#fff6dc", "#c9a227"),
       blk(30, 150, 180, 60, "3× LED strobe boards", "8× VSMA1094250 each", "#fff6dc", "#c9a227"),
       blk(30, 260, 180, 60, "2× radar heads", "SMR-333 24 GHz I/Q", "#fff6dc", "#c9a227"),
       blk(360, 40, 220, 70, "QCS6490 SoM (U10)", "8 GB · 128 GB UFS · Wi-Fi 6E · BT 5.2"),
       blk(360, 150, 220, 60, "STM32G474 timing master", "HRTIM 184 ps triggers + strobes"),
       blk(360, 260, 220, 60, "MSPM0G3507 + 2× ADS131M02", "radar capture (separate sensor)"),
       blk(360, 370, 220, 60, "Strobe bus 30–38 V", "TPS259470 eFuse → LM5155 → 940 µF"),
       blk(680, 40, 200, 50, "Wi-Fi 6E / BT", "app · GSPro · open API", "#eef7ef", "#1baf7a"),
       blk(680, 110, 200, 50, "2.4\" display + 3 buttons", "SPI · TPS61169 backlight", "#eef7ef", "#1baf7a"),
       blk(680, 180, 200, 50, "Sensors (I2C/SPI)", "SCL3300 · BMI323 · BMP585 · SHT45", "#eef7ef", "#1baf7a"),
       blk(680, 250, 200, 50, "Blower + buzzer + RGB", "Delta IP55 · PWM / tach", "#eef7ef", "#1baf7a"),
       blk(680, 370, 200, 60, "Power tree", "USB-C PD 65 W · 4S 81 Wh", "#fdeee7", "#eb6834")]
bd += [poly([(210, 70), (360, 70)], "CSI-2 ×3 (4-lane)", 222, 63),
       poly([(360, 160), (290, 160), (290, 90), (210, 90)], "trigger ×3", 296, 128),
       poly([(360, 185), (210, 185)], "gate cmd ×3", 222, 179),
       poly([(210, 200), (360, 200)], "I-sense → FLT", 222, 216),
       poly([(210, 290), (360, 290)], "I/Q ×2 (analog)", 222, 284),
       poly([(470, 150), (470, 110)], "SPI + UART", 476, 134),
       poly([(580, 290), (620, 290), (620, 95), (580, 95)], "UART", 626, 200),
       poly([(360, 400), (14, 400), (14, 180), (30, 180)], "STROBE_BUS", 140, 392),
       poly([(580, 60), (680, 60)]), poly([(580, 75), (640, 75), (640, 135), (680, 135)]), poly([(580, 85), (650, 85), (650, 205), (680, 205)]),
       poly([(580, 100), (660, 100), (660, 275), (680, 275)]), poly([(680, 400), (580, 400)], "VSYS", 612, 393)]
block_svg = f'<svg viewBox="0 0 900 445" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Helvetica,Arial" role="img" aria-label="System block diagram">{"".join(bd)}</svg>'

pt = [DEF]
pt += [blk(20, 30, 150, 54, "USB-C cord 65 W", "runs with or without pack", "#fdeee7", "#eb6834"), blk(20, 150, 150, 54, "81 Wh battery", "charges while running", "#fdeee7", "#eb6834"),
       blk(230, 85, 170, 64, "BQ25730 buck-boost", "NVDC charger, 400 kHz", "#fdeee7", "#eb6834"), blk(460, 85, 120, 64, "VSYS", "12.3–16.8 V", "#fff", "#0b0b0b")]
outs = [("3V8_SOM 6 A", "TPS56637 (U15)"), ("5V0 3 A", "TPS56637 (U11)"), ("3V3 2.5 A", "TPS62933 (U12)"), ("3V3_CAM 0.9 A", "TPS62933 (U13)"), ("STROBE_BUS 30–38 V", "eFuse U30 → LM5155 U31")]
for i, (a, b) in enumerate(outs):
    pt.append(blk(660, 10 + i*48, 220, 40, a, b, "#e6f0fc", "#2a78d6")); pt.append(arr(580, 117, 660, 30 + i*48))
pt += [arr(170, 57, 230, 105, "PPHV 65 W"), arr(170, 177, 230, 135), '<text x="176" y="200" font-size="10.5" fill="#52514e" font-family="ui-monospace,Menlo,monospace">BATFET Q5</text>', arr(400, 117, 460, 117)]
power_svg = f'<svg viewBox="0 0 900 250" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Helvetica,Arial" role="img" aria-label="Power tree">{"".join(pt)}</svg>'

# ---------------------------------------------------------------- setup plan view (dimensioned, top-down)
def plan_svg():
    bx, by, bz = M.BALL
    W_, H_ = 1200, 530
    k = 0.215
    ox, oz = 330, 70                      # svg origin for world x=0, z=0 (z grows downward on paper)
    X = lambda x: ox + x * k
    Z = lambda z: oz + z * k
    o = [DEF, '<defs><marker id="ad" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="#2a5db0"/></marker></defs>']
    o.append(f'<rect x="0" y="0" width="{W_}" height="{H_}" fill="#f4f5f1"/>')
    # mat
    o.append(f'<rect x="{X(bx-900)}" y="{Z(bz-300)}" width="{1800*k}" height="{1550*k}" fill="#cfe5d1" stroke="#7fb287"/>')
    o.append(f'<text x="{X(bx-890)}" y="{Z(bz+1235)}" font-size="11" fill="#3f6f47">hitting mat</text>')
    # target line
    o.append(f'<line x1="{X(-1500)}" y1="{Z(bz)}" x2="{X(M.SCREEN_X)}" y2="{Z(bz)}" stroke="#7a7974" stroke-width="1.4" stroke-dasharray="10 6"/>')
    o.append(f'<text x="{X(1500)}" y="{Z(bz)-6}" font-size="12" fill="#52514e" text-anchor="middle">target line →</text>')
    # alignment stick
    o.append(f'<line x1="{X(bx-450)}" y1="{Z(bz+260)}" x2="{X(bx+1050)}" y2="{Z(bz+260)}" stroke="#d8b10f" stroke-width="3"/>')
    o.append(f'<text x="{X(bx+1060)}" y="{Z(bz+264)}" font-size="11" fill="#8a6f00">alignment stick (in box)</text>')
    # camera fields of view (6.1 mm lens on IMX900, 41.6° HFOV), aimed per M.CAM_AIM
    for nm in ("CAM-T", "CAM-C"):
        cx = M.CAMS[nm][0]; yaw = math.radians(M.CAM_AIM[nm][0]); half = math.radians(41.6 / 2); R = 900
        p0 = (cx, M.Z1)
        pts = [p0] + [(cx + R * math.sin(yaw + a), M.Z1 + R * math.cos(yaw + a)) for a in (-half, half)]
        o.append('<polygon points="' + " ".join(f"{X(x):.1f},{Z(z):.1f}" for x, z in pts) + '" fill="#2a78d6" fill-opacity="0.10" stroke="#2a78d6" stroke-opacity="0.5"/>')
    o.append(f'<text x="{X(150)}" y="{Z(150)}" font-size="11" fill="#2a5db0">camera fields of view</text>')
    # radar beams (43° wide): rear head toward the backswing, down-range head toward the target
    for x0, aim, R, lab, lx, lz in ((M.X0 - M.BUMP, -77, 750, "rear radar: club approach / wake", -1420, -60),
                                     (M.X1 + M.BUMP, 77, 1500, "down-range radar: ball speed →", 700, -60)):
        a = math.radians(aim); h = math.radians(21.5)
        pts = [(x0, 0)] + [(x0 + R * math.sin(a + d), R * math.cos(a + d)) for d in (-h, h)]
        o.append('<polygon points="' + " ".join(f"{X(x):.1f},{Z(z):.1f}" for x, z in pts) + '" fill="#eb6834" fill-opacity="0.10" stroke="#eb6834" stroke-opacity="0.55"/>')
        o.append(f'<text x="{X(lx)}" y="{Z(lz)}" font-size="11" fill="#b4501e">{lab}</text>')
    # unit
    o.append(f'<rect x="{X(M.X0-M.BUMP)}" y="{Z(M.Z0)}" width="{(M.W+2*M.BUMP)*k}" height="{M.D*k}" rx="3" fill="#2b2d31"/>')
    o.append(f'<rect x="{X(M.WIN["x0"])}" y="{Z(M.Z1)-2}" width="{(M.WIN["x1"]-M.WIN["x0"])*k}" height="3" fill="#4a7fd0"/>')
    o.append(f'<text x="{X(0)}" y="{Z(M.Z0)-8}" font-size="13" font-weight="700" fill="#0b0b0b" text-anchor="middle">Outer Bounds Pro</text>')
    # capture zones + ball
    o.append(f'<rect x="{X(bx-152)}" y="{Z(bz-127)}" width="{304*k}" height="{254*k}" fill="#2a78d6" fill-opacity="0.18" stroke="#2a78d6" stroke-dasharray="4 3"/>')
    o.append(f'<rect x="{X(bx-101)}" y="{Z(bz-101)}" width="{202*k}" height="{202*k}" fill="none" stroke="#eb6834" stroke-dasharray="3 3"/>')
    o.append(f'<circle cx="{X(bx)}" cy="{Z(bz)}" r="{max(4, M.BALL_R*k)}" fill="#fff" stroke="#0b0b0b" stroke-width="1.5"/>')
    o.append(f'<text x="{X(bx)-14}" y="{Z(bz)+4}" font-size="12" font-weight="700" text-anchor="end">BALL</text>')
    # golfer feet (RH)
    for dx in (-230, 230):
        o.append(f'<rect x="{X(bx+dx-50)}" y="{Z(M.TOE_Z)}" width="{100*k}" height="{270*k}" rx="9" fill="#3a3f47"/>')
    o.append(f'<text x="{X(bx)}" y="{Z(M.TOE_Z+270)+16}" font-size="12" font-weight="700" text-anchor="middle">GOLFER (right-handed), facing the unit</text>')
    # screen / target
    o.append(f'<rect x="{X(M.SCREEN_X)}" y="{Z(bz-1500)}" width="5" height="{3000*k}" fill="#7a7974"/>')
    o.append(f'<text x="{X(M.SCREEN_X)-6}" y="{Z(bz-1500)-8}" font-size="12" font-weight="700" text-anchor="end">IMPACT SCREEN / TARGET</text>')
    o.append(f'<text x="{X(M.SCREEN_X)-6}" y="{Z(bz-1500)+8}" font-size="11" text-anchor="end" fill="#52514e">(outdoors: the range target, along the same line)</text>')
    # LH ghost (mirror across target line)
    mz0, mz1 = 2*bz - M.Z1, 2*bz - M.Z0
    o.append(f'<rect x="{X(M.X0-M.BUMP)}" y="{Z(mz0)}" width="{(M.W+2*M.BUMP)*k}" height="{(mz1-mz0)*k}" rx="3" fill="none" stroke="#7a7974" stroke-dasharray="5 4"/>')
    o.append(f'<text x="{X(bx+950)}" y="{Z((mz0+mz1)/2)+4}" font-size="11" fill="#7a7974">← left-handed: unit mirrors here (dashed), golfer stands where the unit is</text>')
    # dimensions
    def dimv(x, z0, z1, lab, side=1):
        return (f'<line x1="{X(x)}" y1="{Z(z0)}" x2="{X(x)}" y2="{Z(z1)}" stroke="#2a5db0" marker-start="url(#ad)" marker-end="url(#ad)"/>'
                f'<text x="{X(x)+6*side}" y="{(Z(z0)+Z(z1))/2+4}" font-size="11.5" fill="#2a5db0" text-anchor="{"start" if side>0 else "end"}" font-family="ui-monospace,Menlo,monospace">{lab}</text>')
    def dimh(z, x0, x1, lab, dy=-5):
        return (f'<line x1="{X(x0)}" y1="{Z(z)}" x2="{X(x1)}" y2="{Z(z)}" stroke="#2a5db0" marker-start="url(#ad)" marker-end="url(#ad)"/>'
                f'<text x="{(X(x0)+X(x1))/2}" y="{Z(z)+dy}" font-size="11.5" fill="#2a5db0" text-anchor="middle" font-family="ui-monospace,Menlo,monospace">{lab}</text>')
    o.append(dimv(bx - 40, M.Z1, bz, "450 mm (18 in) window → ball · OK 450–600", -1))
    o.append(dimh(M.Z1 + 70, bx, 0, f"{-bx:.0f} mm forward", -5))
    o.append(dimh(bz + 60, bx, M.SCREEN_X, "3.0 m (10 ft) ball → screen · min 2.4 m (8 ft)", 16))
    o.append(dimv(bx - 420, bz, M.TOE_Z, "≈0.5 m ball → toes", -1))
    o.append(f'<line x1="{X(0)}" y1="{Z(M.Z1)}" x2="{X(0)}" y2="{Z(M.Z1+110)}" stroke="#2a5db0" stroke-dasharray="2 2"/>')
    # north arrow / legend
    return f'<svg viewBox="0 0 {W_} {H_}" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Helvetica,Arial" role="img" aria-label="Setup plan view: unit, ball, golfer, target">{"".join(o)}</svg>'

# ---------------------------------------------------------------- assemble
sch = [(sid, title, desc, D.render_sheet(sid)) for sid, title, desc in D.sheets]
dwg = DW.all_sheets()
erc = D.erc()
model_json = json.dumps({"prims": P, "scene": M.scene(), "setupTarget": [1300, 300, 600], "shellGroups": M.SHELL_GROUPS}).replace("</", "<\\/")
viewer_js = open(os.path.join(HERE, "viewer.js")).read()
netlist_txt = D.netlist_text()
l2_json = json.dumps(rows)
l1_json = json.dumps(L1)

total_parts = sum(r["qty"] * boards[r["board"]][2] for r in rows if r["board"] != "BP")
open_items = [
    ("C6490P I/O voltage", "Carrier assumes 1.8 V SoM I/O and translates every digital signal (sheet CB-10). If the design guide shows on-module 3.3 V translation, U60–U68 become DNP and the _1V8 nets are bridged."),
    ("Thundercomm C6490P ball map", "U10 nets are final; ball numbers (incl. VREG_1P8 and the VBUS-detect GPIO) come from the C6490P HW design guide (NDA)."),
    ("Cord-only cold start", "Bench test: no pack, 5 V default USB contract only, SoM unprogrammed charger. BQ25730 must hold VSYS ≥ 10.5 V from its POR defaults until the SoM boots and PD reaches 20 V."),
    ("LED current loop", "Bench: OPA810 + CSD18543 loop rise time and overshoot on a real 8-LED string; firmware trims the strobe bus (30–38 V) to the lowest setting that keeps the sink in regulation."),
    ("Camera aim", "Stereo pair square and pitched 3° down, club camera toed in 7°. FOV sim: ball at address in frame for both hands, ≥ 240 mm of stereo flight at 5–20° launch, 155 mm at 45°. Confirm on a prototype."),
    ("SCL3300 inclinometer ($30)", "Cost-down candidate: drop it if the BMI323 holds ±0.2° levelling after factory calibration."),
    ("LED-board one-shot 8 µs cap value", "560 pF from datasheet curves; trim on the first LED board."),
    ("STM32G474 AF numbers", "Pin map from DS12288 Rev 1; re-check alternate-function numbers vs Rev 6 in CubeMX."),
    ("TE 5787441-1 ↔ 787439-1 keying", "Header is keyless and receptacle is right-hand key; confirm polarized mate with TE."),
    ("Small ICs flagged ⚠ on the sheets", "TPD4E05U06, TPD2E2U06, DAC80501Z, TPS61169, TPS7A4101, OPA810, Würth RGB, BQ40Z50 pin numbers: pull land patterns from vendor ECAD libraries (nets are final)."),
]

html = open(os.path.join(HERE, "page_template.html")).read()
def tab_svgs(items, cls):
    return "".join(f'<figure class="{cls}" id="{escape(i[0])}"><figcaption>{escape(i[0])} · {escape(i[1].split("·")[0].strip())}</figcaption><div class="svgwrap">{i[3]}</div></figure>' for i in items)
rep = {
    "__GALLERY__": "".join(f'<figure><img data-snap="{escape(json.dumps(v))}" alt="{escape(t)}"><figcaption>{escape(t)}</figcaption></figure>' for t, v in gallery),
    "__BLOCK__": block_svg, "__PLAN__": plan_svg(), "__POWER__": power_svg,
    "__SCH_TOC__": "".join(f'<a href="#{escape(s[0])}">{escape(s[0])} {escape(s[1].split("·")[0].split(":")[0])}</a>' for s in sch),
    "__SCHEMATICS__": tab_svgs(sch, "sheet"),
    "__DWG_TOC__": "".join(f'<a href="#dwg{i}">{escape(d.number)} {escape(d.title.split("·")[0])}</a>' for i, d in enumerate(dwg)),
    "__DRAWINGS__": "".join(f'<figure class="sheet" id="dwg{i}"><div class="svgwrap">{d.svg()}</div></figure>' for i, d in enumerate(dwg)),
    "__MODEL__": model_json, "__VIEWER__": viewer_js, "__NETLIST__": escape(netlist_txt), "__L1__": l1_json, "__L2__": l2_json,
    "__NPARTS__": str(len(D.parts)), "__NNETS__": str(len(D.nets())), "__NSHEETS__": str(len(sch)), "__NDWG__": str(len(dwg)),
    "__ERC__": "0 errors" if not erc else f"{len(erc)} issues",
    "__L1TOTAL__": f"${l1_total:,.0f}", "__LANDED__": f"${landed:,.0f}", "__PLACEMENTS__": f"{total_parts:,}",
    "__OPEN__": "".join(f"<tr><td style='width:32%'><b>{escape(a)}</b></td><td>{escape(b)}</td></tr>" for a, b in open_items),
    "__DIMS__": f"{M.W+2*M.BUMP:.0f} × {M.TOP-M.Y0:.0f} × {M.D:.0f} mm",
}
for k, v in rep.items():
    html = html.replace(k, v)
out = os.path.join(HERE, "outer-bounds-pro-design.html")
open(out, "w").write(html)
with open(os.path.join(HERE, "outer-bounds-pro-netlist.txt"), "w") as f:
    f.write(netlist_txt)
print("wrote", out, f"{os.path.getsize(out)/1e6:.1f} MB", "| L1 @1k", round(l1_total, 2), "landed", round(landed, 2), "| ERC", len(erc))
for b in boards:
    print(b, "parts", round(pcba_parts[b], 2), "lines", pcba_lines[b], "placements", pcba_count[b])
