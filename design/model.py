"""Outer Bounds Pro - mechanical model (single source of truth for 3D views and drawings).

Coordinate system (mm), origin at the centre of the enclosure envelope:
  +X  along the target line, toward the target
  +Y  up
  +Z  out of the front face, toward the ball/hitting area
The unit sits beside and slightly forward of the ball; the ball is at roughly (-150, -80, +500).
"""
import math

# ------------------------------------------------------------------ envelope & key dims
W, H, D = 240.0, 164.0, 96.0          # lower body (shell, excluding TPE end caps and the top crown)
BUMP = 12.0                           # TPE end-cap projection at each X end
WALL = 2.5
X0, X1 = -W/2, W/2
Y0, Y1 = -80.0, 84.0                  # Y1 = top of the lower body / base of the crown
TOP = 120.0                           # top of the crown (flush with the grip bar)
Z0, Z1 = -D/2, D/2

WIN = dict(x0=-112, x1=112, y0=-46, y1=76, t=2.0)          # IR window (strengthened glass + IR ink)
BENCH = dict(x0=-108, x1=108, y0=-44, y1=74, z0=10, z1=20)   # 10 mm plate; camera stack 26.5 mm (R-mechanical-dims)  # 6061-T651 optical bench plate
CAMS = {  # name: (x, y) of optical axis on the bench
    "CAM-T": (0.0, 50.0),      # stereo top, on the centre line
    "CAM-B": (0.0, -30.0),     # stereo bottom   -> 80 mm vertical baseline
    "CAM-C": (56.0, 50.0),     # club camera, 56 mm horizontal offset
}
# Optics are symmetric about x = 0, so the same placement works for right- and left-handed golfers
# (the unit is turned around for a left-hander and the ball sits 100 mm behind its centre either way).
CAM_AIM = {"CAM-T": (0.0, -3.0), "CAM-B": (0.0, -3.0), "CAM-C": (-7.0, -3.0)}   # (yaw, pitch) deg; pitch < 0 looks down
LEDB = {  # LED board centre (x, y), yaw (deg)
    "LED-A": (-84.0, 10.0, 10.0),
    "LED-B": (88.0, 10.0, -10.0),
    "LED-C": (56.0, -26.0, -7.0),
}
CARRIER = dict(x0=-80, x1=80, y0=-42, y1=50, z0=0.0, t=1.6)  # main carrier PCB 160 x 92
BATT = dict(x0=-4, x1=88, y0=-77, y1=-50, z0=-39, z1=39)     # 4S1P 21700 pack housing (92 x 27 x 78)
DISP = dict(x0=49.0, x1=96.3, z0=-31.0, z1=31.0)            # VIEWE 2.4" glass 62.06 x 47.32 x 3.41, portrait, under the right crown lobe
BTN_X = 72.5                                                # button column (left crown lobe), mirrors the display
# Faceted profiles: (y, half-width) seen from the front, (y, half-depth) seen from the side
BODY_A = [(-80, 108), (-68, 120), (72, 120), (84, 108)]
BODY_B = [(-80, 40), (-68, 48), (76, 48), (84, 38)]
CROWN = dict(a0=108, a1=92, b0=38, b1=34)                  # crown half-width/half-depth at its base (Y1) and top (TOP)
GRIP = dict(x=45.0, z=29.0, bar_z=10.0, bar_y=104.0)        # trench 90 x 58, bar 20 wide, 20 mm finger clearance under the bar
DOOR = dict(x0=-6.0, x1=90.0, z=37.0)
FAN = dict(x0=-112, x1=-72, y0=62, y1=74, z0=-38, z1=2)      # Delta BFB0405 40x40x10 blower (lying flat)
FINS = dict(x0=-70, x1=-20, y0=58, y1=76, z0=-38, z1=-10)
TRIPOD = (-60.0, 0.0)          # 1/4"-20 insert in bench foot, (x, z) on bottom face
USBC = (60.0, -22.0)           # (x, y) on rear face
VENT = (84.0, -22.0)

C = dict(  # colours
    crown="#2a2c31", shell="#4d525a", shell2="#33363b", bumper="#1c1d20", glass="#141820", bench="#8f969e", pcb="#1f6b46",
    pcbb="#2a6a8a", cam="#3a3d42", lens="#0e0f12", led="#d9d4c7", som="#5a5f66", alu="#b7bcc2", cu="#c47a3a",
    batt="#3d4a5c", cell="#4f8bd6", disp="#0b0c10", btn="#4a4d52", radar="#c9a227", fan="#26282c", rubber="#111214",
    accent="#eb6834", cap="#2f3d52", ind="#3b3b3b", chip="#222326", conn="#e6e1d6", grill="#0b0b0d", label="#c8c8c8",
)

SHELL_GROUPS = ["Front shell (PC/ABS)", "Rear shell (PC/ABS)", "Top crown + hidden grip", "IR window", "TPE end caps", "Battery door", "Feet"]
P = []   # primitives


def box(name, grp, c, s, col, ry=0, rx=0, ex=(0, 0, 0), ext=False, alpha=1.0, hidden_dash=True):
    P.append(dict(t="box", n=name, g=grp, c=list(c), s=list(s), col=col, ry=ry, rx=rx, ex=list(ex), ext=ext, a=alpha))


def cyl(name, grp, c, r, h, axis, col, n=20, ry=0, ex=(0, 0, 0), ext=False, alpha=1.0):
    P.append(dict(t="cyl", n=name, g=grp, c=list(c), r=r, h=h, ax=axis, col=col, seg=n, ry=ry, ex=list(ex), ext=ext, a=alpha))


def span(x0, x1, y0, y1, z0, z1):
    return [(x0+x1)/2, (y0+y1)/2, (z0+z1)/2], [x1-x0, y1-y0, z1-z0]


def prof(tab, y):
    """Piecewise-linear profile lookup."""
    for (y0, v0), (y1, v1) in zip(tab, tab[1:]):
        if y0 <= y <= y1:
            return v0 + (v1-v0)*(y-y0)/(y1-y0)
    raise ValueError(y)


def _hull(pts, eps=1e-6):
    """Convex hull of a small point set -> (vertices, faces as CCW index loops seen from outside, outward normals)."""
    V = sorted({tuple(round(c, 4) for c in p) for p in pts})
    sub = lambda a, b: (a[0]-b[0], a[1]-b[1], a[2]-b[2])
    cross = lambda a, b: (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
    dot3 = lambda a, b: a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
    planes = {}
    n_ = len(V)
    for i in range(n_):
        for j in range(i+1, n_):
            for k in range(j+1, n_):
                n = cross(sub(V[j], V[i]), sub(V[k], V[i]))
                m = math.sqrt(dot3(n, n))
                if m < 1e-9:
                    continue
                n = tuple(c/m for c in n); d = dot3(n, V[i])
                s = [dot3(n, p)-d for p in V]
                if all(v <= eps for v in s):
                    pass
                elif all(v >= -eps for v in s):
                    n, d = tuple(-c for c in n), -d
                else:
                    continue
                key = tuple(round(c, 5) for c in n) + (round(d, 3),)
                planes.setdefault(key, (n, d))
    F, N = [], []
    for n, d in planes.values():
        idx = [i for i, p in enumerate(V) if abs(dot3(n, p)-d) < 1e-4]
        cen = [sum(V[i][a] for i in idx)/len(idx) for a in range(3)]
        u = sub(V[idx[0]], cen); m = math.sqrt(dot3(u, u)); u = tuple(c/m for c in u)
        v = cross(n, u)
        idx.sort(key=lambda i: math.atan2(dot3(sub(V[i], cen), v), dot3(sub(V[i], cen), u)))
        F.append(idx); N.append([round(c, 6) for c in n])
    return [list(p) for p in V], F, N


def hull(name, grp, pts, col, ex=(0, 0, 0), ext=False, alpha=1.0):
    V, F, N = _hull(pts)
    c = [sum(p[i] for p in V)/len(V) for i in range(3)]
    P.append(dict(t="mesh", n=name, g=grp, c=c, v=V, f=F, fn=N, col=col, ry=0, rx=0, ex=list(ex), ext=ext, a=alpha))


def aimed_cyl(name, grp, pivot, z0, z1, r, yaw, pitch, col, ex=(0, 0, 0), n=16):
    """Cylinder along an optical axis that starts at `pivot`, yawed about Y then pitched (deg)."""
    a, b = math.radians(yaw), math.radians(pitch)
    d = (math.sin(a)*math.cos(b), math.sin(b), math.cos(a)*math.cos(b))
    u = (math.cos(a), 0.0, -math.sin(a))
    v = (-math.sin(a)*math.sin(b), math.cos(b), -math.cos(a)*math.sin(b))
    pts = [tuple(pivot[i] + r*math.cos(t)*u[i] + r*math.sin(t)*v[i] + z*d[i] for i in range(3))
           for z in (z0, z1) for t in (2*math.pi*k/n for k in range(n))]
    hull(name, grp, pts, col, ex=ex)


def build():
    P.clear()
    EXF, EXR = (0, 0, 130), (0, 0, -120)
    # ---------------------------------------------------------------- faceted shell: lower body, split front/rear at z = 0
    # The body is the intersection of a front-view profile (half-width a(y)) and a side-view profile (half-depth b(y)),
    # so each half is convex and is built as a hull of rectangle corners at every profile break.
    lv = sorted({y for y, _ in BODY_A} | {y for y, _ in BODY_B})
    for nm, g, zs, ex in (("front body half", "Front shell (PC/ABS)", 1, EXF), ("rear body half", "Rear shell (PC/ABS)", -1, EXR)):
        pts = [(sx*prof(BODY_A, y), y, z) for y in lv for sx in (-1, 1) for z in (0.0, zs*prof(BODY_B, y))]
        hull(nm, g, pts, C["shell"], ex=ex, ext=True)
    # IR window: chamfered-corner glass, proud of the front face by 1.5 mm
    wz0, wz1 = Z1-0.2, Z1+WIN["t"]-0.5
    wp = [(WIN["x0"], WIN["y0"]+16), (WIN["x0"]+16, WIN["y0"]), (WIN["x1"]-16, WIN["y0"]), (WIN["x1"], WIN["y0"]+16), (WIN["x1"], WIN["y1"]), (WIN["x0"], WIN["y1"])]
    hull("IR window (glass, IR-pass ink, AR)", "IR window", [(x, y, z) for x, y in wp for z in (wz0, wz1)], C["glass"], ex=(0, 0, 190), ext=True, alpha=0.6)
    for x0, x1, y0, y1 in ((-63.5, -60.5, WIN["y0"]+2, WIN["y1"]), (65.5, 68.5, WIN["y0"]+2, WIN["y1"]),
                           (28.5, 31.5, WIN["y0"]+2, 0.0), (28.5, 65.5, -1.5, 1.5)):   # IR-opaque isolation bands (printed on the window)
        c_, s_ = span(x0, x1, y0, y1, wz1, wz1+0.3)
        box("IR isolation band", "IR window", c_, s_, "#000000", ex=(0, 0, 190), ext=True)
    # front status light-bar (RGB light-pipe) centred under the window
    hull("status light-bar (RGB light-pipe)", "Display & buttons", [(x, y, z) for x, y in ((-22, -58), (-18, -62), (18, -62), (22, -58)) for z in (Z1-0.5, Z1+0.6)],
         C["accent"], ex=(0, 0, 130), ext=True)

    # ---------------------------------------------------------------- top crown with the hidden grip
    # Two end lobes (display right, buttons left), front and rear lips, and a grip bar flush with the top.
    # From the front and sides the crown reads as solid; the bar's 19 mm finger gaps only show from above.
    g = "Top crown + hidden grip"
    TX, TZ = GRIP["x"], GRIP["z"]
    for sx in (-1, 1):
        pts = [(sx*x, y, z) for y, a in ((Y1, CROWN["a0"]), (TOP, CROWN["a1"])) for x in (TX, a)
               for z in ((-CROWN["b0"], CROWN["b0"]) if y == Y1 else (-CROWN["b1"], CROWN["b1"]))]
        hull("crown lobe " + ("R (display)" if sx > 0 else "L (buttons)"), g, pts, C["crown"], ex=(0, 90, 0), ext=True)
    for sz in (-1, 1):   # lips, bevelled into the trench at the top edge
        pts = [(x, y, sz*z) for x in (-TX, TX) for y, z in ((Y1, TZ), (Y1, CROWN["b0"]), (TOP, CROWN["b1"]), (TOP, TZ+3), (TOP-4, TZ))]
        hull("crown lip " + ("front" if sz > 0 else "rear"), g, pts, C["crown"], ex=(0, 90, 0), ext=True)
    bz_, by_ = GRIP["bar_z"], GRIP["bar_y"]
    pts = [(x, y, s*z) for x in (-TX, TX) for s in (-1, 1) for y, z in ((by_, bz_-4), (by_+4, bz_), (TOP-2, bz_), (TOP, bz_-2))]
    hull("grip bar (flush with top)", g, pts, C["crown"], ex=(0, 120, 0), ext=True)
    c_, s_ = span(-TX+2, TX-2, by_-0.6, by_, -bz_+5, bz_-5); box("grip bar TPE overmold (underside)", g, c_, s_, C["rubber"], ex=(0, 120, 0), ext=True)
    c_, s_ = span(-TX, TX, Y1, Y1+0.6, -TZ, TZ); box("grip trench floor", g, c_, s_, C["grill"], ex=(0, 90, 0), ext=True)

    # ---------------------------------------------------------------- rear-face details
    g = "Rear shell (PC/ABS)"
    for k in range(5):   # exhaust grille over the fin stack
        y = 58+k*3.6
        c_, s_ = span(FINS["x0"]+2, FINS["x1"]-2, y, y+2.0, Z0-0.35, Z0-0.05)
        box("exhaust slot", g, c_, s_, C["grill"], ex=EXR, ext=True)
    for k in range(6):   # intake grille (blower)
        y = FAN["y0"]-18+k*5.0
        c_, s_ = span(FAN["x0"]+2, FAN["x1"]-2, y, y+2.6, Z0-0.35, Z0-0.05)
        box("intake slot", g, c_, s_, C["grill"], ex=EXR, ext=True)
    c_, s_ = span(USBC[0]-5, USBC[0]+5, USBC[1]-2, USBC[1]+2, Z0-0.4, Z0+0.6); box("USB-C IP67 (GCT USB4720)", g, c_, s_, "#050505", ex=EXR, ext=True)
    cyl("pressure vent (Amphenol LTW)", g, [VENT[0], VENT[1], Z0-0.5], 4.0, 1.5, "z", "#5a5d62", ex=EXR, ext=True)
    c_, s_ = span(-40, 30, -60, -40, Z0-0.3, Z0-0.05); box("rating / regulatory label", g, c_, s_, "#3c3f44", ex=EXR, ext=True)

    # ---------------------------------------------------------------- display + buttons on the crown lobes
    g = "Display & buttons"
    c_, s_ = span(DISP["x0"]-1.5, DISP["x1"]+1.5, TOP-0.2, TOP+0.6, DISP["z0"]-2, DISP["z1"]+2)
    box("display cover glass (AR, bonded)", g, c_, s_, C["disp"], ex=(0, 140, 0), ext=True)
    for i, z in enumerate((-16.0, 0.0, 16.0)):
        cyl(f"button {['POWER','MODE','L/R'][i]}", g, [-BTN_X, TOP+0.8, z], 5.0, 2.2, "y", C["btn"], ex=(0, 140, 0), ext=True)
    c_, s_ = span(-BTN_X-9, -BTN_X+9, TOP, TOP+0.3, 26, 28); box("button legend strip", g, c_, s_, C["accent"], ex=(0, 140, 0), ext=True)

    # ---------------------------------------------------------------- TPE end caps with radar radomes
    # Faceted wedges: full profile at the shell joint, a pointed chevron mid-way, a smaller bevelled outer face.
    for side, sx in (("L", -1), ("R", 1)):
        inner = [(-42, -83), (42, -83), (50, -66), (50, 74), (40, 90), (-40, 90), (-50, 74), (-50, -66)]
        mid = [(-52, -4), (52, -4)]
        outer = [(-34, -72), (34, -72), (42, -56), (42, 62), (32, 78), (-32, 78), (-42, 62), (-42, -56)]
        pts = ([(sx*(X1-6), y, z) for z, y in inner] + [(sx*(X1+BUMP-6), y, z) for z, y in mid] + [(sx*(X1+BUMP), y, z) for z, y in outer])
        hull(f"TPE end cap {side}", "TPE end caps", pts, C["bumper"], ex=(sx*150, 0, 0), ext=True)
        xr = sx*(X1+BUMP+0.15)
        c_, s_ = span(xr-0.2, xr+0.2, 5, 35, -28, 0)
        box(f"radome window {side} (PC 3.6 mm, λ/2)", "TPE end caps", c_, s_, "#3b3f45", ex=(sx*150, 0, 0), ext=True)
        c_, s_ = span(xr-0.25, xr+0.25, -50, -47, -30, 30)
        box(f"end-cap accent {side}", "TPE end caps", c_, s_, C["accent"], ex=(sx*150, 0, 0), ext=True)

    # ---------------------------------------------------------------- optical bench + cameras + LED boards
    g = "Optical bench (6061-T651)"
    c_, s_ = span(BENCH["x0"], BENCH["x1"], BENCH["y0"], BENCH["y1"], BENCH["z0"], BENCH["z1"])
    box("optical bench plate", g, c_, s_, C["bench"], ex=(0, 0, 45))
    c_, s_ = span(-106, -12, BENCH["y0"]-33, BENCH["y0"], BENCH["z0"], BENCH["z1"])
    box("bench foot L (tripod boss, datum A)", g, c_, s_, C["bench"], ex=(0, 0, 45))
    c_, s_ = span(92, 106, BENCH["y0"]-33, BENCH["y0"], BENCH["z0"], BENCH["z1"])
    box("bench foot R (slot B)", g, c_, s_, C["bench"], ex=(0, 0, 45))
    cyl("1/4-20 tripod thread (in bench foot)", g, [TRIPOD[0], Y0+1, 21], 4.0, 2.0, "y", "#b08d3c", ex=(0, 0, 45), ext=True)
    g = "Cameras (3x IMX900)"
    for nm, (x, y) in CAMS.items():
        zb = BENCH["z0"]                         # camera board front face sits on the bench back face
        c_, s_ = span(x-11.75, x+11.75, y-11, y+11, zb-1.54, zb)
        box(f"{nm} VC MIPI IMX900 PCB 23.5x22", g, c_, s_, C["cam"], ex=(0, 0, 45), ry=0)
        c_, s_ = span(x-8, x+8, y+6, y+10.5, zb-1.54-3.9, zb-1.54)
        box(f"{nm} 22-pin FPC connector (rear)", g, c_, s_, C["conn"], ex=(0, 0, 45))
        yaw, pitch = CAM_AIM[nm]
        aimed_cyl(f"{nm} VK000057 S-mount holder", g, (x, y, zb), 0, 12, 10.5, yaw, pitch, "#202226", ex=(0, 0, 45))
        aimed_cyl(f"{nm} CIL361 6.1mm f/1.8 + 940/40 filter", g, (x, y, zb), 12, 25, 7.0, yaw, pitch, C["lens"], ex=(0, 0, 45))
        aimed_cyl(f"{nm} front element", g, (x, y, zb), 25, 25.6, 4.2, yaw, pitch, "#283b6e", ex=(0, 0, 45))
    g = "LED strobe boards (3x8 VSMA1094250)"
    for nm, (x, y, yaw) in LEDB.items():
        zc = BENCH["z1"] + 3.0          # board seated in a machined wedge pocket in the bench face
        c_, s_ = span(x-20, x+20, y-15, y+15, zc-0.8, zc+0.8)
        box(f"{nm} board (4L FR-4)", g, c_, s_, C["pcbb"], ry=yaw, ex=(0, 0, 80))
        r = math.radians(yaw)
        for i in range(4):
            for j in range(2):
                lx, ly = -12+i*8, -5+j*10
                cx, cz = x + lx*math.cos(r), zc+0.8+1.45 - lx*math.sin(r)
                c_, s_ = span(cx-1.9, cx+1.9, y+ly-1.9, y+ly+1.9, cz-1.2, cz+1.2)
                box(f"{nm} LED", g, c_, s_, C["led"], ry=yaw, ex=(0, 0, 80))

    # ---------------------------------------------------------------- radar heads (behind radomes)
    g = "Radar heads (2x SMR-333)"
    for nm, x, yaw in (("rear head (club/wake)", -110.0, -122.0), ("down-range head (ball)", 110.0, 122.0)):
        c_, s_ = span(x-1.6, x, 8, 32, -26, -2); box(nm + " PCB", g, c_, s_, C["pcb"], ex=(-50 if x < 0 else 50, 0, 0))
        xs = x+0.0 if x < 0 else x-1.6
        c_, s_ = span(xs-3.1 if x > 0 else xs, xs if x > 0 else xs+3.1, 12.5, 27.5, -24.7, -3.3); box(nm + " SMR-333", g, c_, s_, C["radar"], ex=(-50 if x < 0 else 50, 0, 0))

    # ---------------------------------------------------------------- carrier PCB + SoM + key parts
    g = "Main carrier PCB"
    cr = CARRIER
    c_, s_ = span(cr["x0"], cr["x1"], cr["y0"], cr["y1"], cr["z0"], cr["z0"]+cr["t"]); box("carrier PCB 10L HDI 160x92", g, c_, s_, C["pcb"])
    zf, zb = cr["z0"]+cr["t"], cr["z0"]
    for i, x in enumerate((-55, -35, 30)):
        c_, s_ = span(x-8, x+8, 38, 44, zf, zf+2.0); box(f"FPC conn J{10+i} (FH12-22S)", g, c_, s_, C["conn"])
    c_, s_ = span(-12, 2, -10, 4, zf, zf+1.6); box("U20 STM32G474 (timing master)", g, c_, s_, C["chip"])
    c_, s_ = span(10, 20, -30, -22, zf, zf+1.0); box("U40 MSPM0G3507 (radar)", g, c_, s_, C["chip"])
    c_, s_ = span(40, 52, 18, 30, zf, zf+1.0); box("U2 BQ25730 (charger)", g, c_, s_, C["chip"])
    c_, s_ = span(56, 62, 18, 24, zf, zf+1.0); box("U1 TPS25751 (USB-C PD)", g, c_, s_, C["chip"])
    for i, (x, y) in enumerate(((44, 6), (58, 6), (44, -8), (58, -8))):
        c_, s_ = span(x-3.5, x+3.5, y-3.5, y+3.5, zf, zf+1.0); box(f"Q{i+3} CSD17578Q3A", g, c_, s_, C["chip"])
    c_, s_ = span(66, 78, -2, 10, zf, zf+5.0); box("L2 charger inductor 2.2 uH", g, c_, s_, C["ind"])
    for i, (x, y) in enumerate(((-66, 20), (-66, 2))):
        c_, s_ = span(x-5, x+5, y-5, y+5, zf, zf+4.0); box(f"L{10+i} buck inductor", g, c_, s_, C["ind"])
    c_, s_ = span(-60, -50, -34, -24, zf, zf+3.0); box("L30 strobe boost 10 uH SRP7028A", g, c_, s_, C["ind"])
    for i, x in enumerate((-36, -20)):
        cyl(f"C3{x} 470uF/50V strobe bulk (16x16.5)", g, [x, -24, zb-8.25], 8.0, 16.5, "z", C["cap"])
    c_, s_ = span(-48, -40, 26, 34, zf, zf+1.0); box("U5 SCL3300 inclinometer", g, c_, s_, C["chip"])
    c_, s_ = span(70, 78, 30, 46, zf, zf+3.0); box("J3 battery header (TE 5787441)", g, c_, s_, C["conn"])
    g = "SoM + heat pipe + blower"
    c_, s_ = span(-39.5, -0.5, 2, 35, zb-2.75, zb); box("U10 Thundercomm C6490P QCS6490 SoM 39x33", g, c_, s_, C["som"], ex=(0, 0, -30))
    c_, s_ = span(-38.5, -1.5, 3, 34, zb-6.0, zb-2.75); box("Cu spreader + 6.2 W/mK pad", g, c_, s_, C["cu"], ex=(0, 0, -30))
    cyl("heat pipe (6 mm, vertical run)", g, [-30, 34, zb-8], 3.0, 64, "y", C["cu"], ex=(0, 0, -30))
    cyl("heat pipe (into fin stack)", g, [-30, 66, (zb-8+FINS["z0"])/2], 3.0, abs(zb-8-FINS["z0"]), "z", C["cu"], ex=(0, 0, -30))
    for k in range(10):
        x = FINS["x0"]+2+k*5
        c_, s_ = span(x, x+0.6, FINS["y0"], FINS["y1"], FINS["z0"], FINS["z1"]); box("Al fin", g, c_, s_, C["alu"], ex=(0, 30, -30))
    c_, s_ = span(FAN["x0"], FAN["x1"], FAN["y0"], FAN["y1"], FAN["z0"], FAN["z1"]); box("Delta BFB0405HHA IP55 blower", g, c_, s_, C["fan"], ex=(-30, 30, -30))
    cyl("blower inlet", g, [(FAN["x0"]+FAN["x1"])/2, FAN["y1"]+0.1, (FAN["z0"]+FAN["z1"])/2], 12, 0.3, "y", "#3a3d42", ex=(-30, 30, -30))

    # ---------------------------------------------------------------- display module under the crown glass
    c_, s_ = span(DISP["x0"], DISP["x1"], TOP-3.6, TOP-0.2, DISP["z0"], DISP["z1"])
    box("VIEWE 2.4in transflective TFT", "Display & buttons", c_, s_, "#30343a", ex=(0, 140, 0))

    # ---------------------------------------------------------------- battery pack + door
    g = "Battery pack (4S1P 81 Wh)"
    b = BATT
    c_, s_ = span(b["x0"], b["x1"], b["y0"], b["y1"], b["z0"], b["z1"]); box("pack housing (PC, V-0)", g, c_, s_, C["batt"], ex=(0, -80, 0), alpha=0.45)
    for i in range(4):
        x = b["x0"]+4+10.55+i*21.2
        cyl(f"LG M58T cell {i+1}", g, [x, (b["y0"]+b["y1"])/2, 0], 10.55, 70.2, "z", C["cell"], ex=(0, -80, 0))
    c_, s_ = span(b["x1"]-1, b["x1"]+2, b["y0"]+6, b["y1"]-6, 20, 34); box("pack plug TE 787439-1", g, c_, s_, C["conn"], ex=(0, -80, 0))
    c_, s_ = span(DOOR["x0"], DOOR["x1"], Y0-0.6, Y0, -DOOR["z"], DOOR["z"]); box("battery door (latching)", "Battery door", c_, s_, C["shell2"], ex=(0, -120, 0), ext=True)
    c_, s_ = span(b["x0"]+30, b["x0"]+60, Y0-1.0, Y0-0.6, -6, 6); box("door latch", "Battery door", c_, s_, C["accent"], ex=(0, -120, 0), ext=True)
    for (x, z) in ((-100, -30), (-100, 30), (100, -30), (100, 30)):
        cyl("3M SJ5302 foot", "Feet", [x, Y0-1.75, z], 6.35, 3.5, "y", C["rubber"], ext=True, ex=(0, -130, 0))
    return P


def bbox(p):
    """Axis-aligned extents ignoring rotation (fine for drawings of unrotated parts)."""
    if p["t"] == "mesh":
        return [min(v[i] for v in p["v"]) for i in range(3)], [max(v[i] for v in p["v"]) for i in range(3)]
    if p["t"] == "box":
        return [p["c"][i]-p["s"][i]/2 for i in range(3)], [p["c"][i]+p["s"][i]/2 for i in range(3)]
    r, h = p["r"], p["h"]
    ext = {"x": (h/2, r, r), "y": (r, h/2, r), "z": (r, r, h/2)}[p["ax"]]
    return [p["c"][i]-ext[i] for i in range(3)], [p["c"][i]+ext[i] for i in range(3)]


if __name__ == "__main__":
    build()
    print(len(P), "primitives")
    groups = sorted({p["g"] for p in P})
    print(groups)


# ------------------------------------------------------------------ setup scene (ball, golfer, target)
# Placement used everywhere (3D setup view, plan drawing): right-handed golfer, unit beside and forward of the ball.
FLOOR_Y = Y0 - 3.5                     # underside of the rubber feet
BALL_R = 21.35
BALL = (-100.0, FLOOR_Y + BALL_R, Z1 + 450.0)   # 450 mm from the IR window, 100 mm behind the unit centre (both hands)
SCREEN_X = BALL[0] + 3048.0           # 10 ft ball-to-screen (8 ft minimum)
TOE_Z = BALL[2] + 500.0               # golfer toe line, ~0.5 m from the ball
LAUNCH_DEG = 14.0


def scene():
    S = []
    bx, by, bz = BALL

    def sbox(n, g, x0, x1, y0, y1, z0, z1, col, a=1.0):
        S.append(dict(t="box", n=n, g=g, c=[(x0+x1)/2, (y0+y1)/2, (z0+z1)/2], s=[x1-x0, y1-y0, z1-z0], col=col, ry=0, rx=0, ex=[0, 0, 0], ext=False, a=a))

    def scyl(n, g, c, r, h, ax, col, a=1.0):
        S.append(dict(t="cyl", n=n, g=g, c=list(c), r=r, h=h, ax=ax, col=col, seg=24, ry=0, ex=[0, 0, 0], ext=False, a=a))

    def ssph(n, g, c, r, col, a=1.0):
        S.append(dict(t="sph", n=n, g=g, c=list(c), r=r, col=col, ry=0, ex=[0, 0, 0], ext=False, a=a))

    g = "Setup: floor, mat, target line"
    sbox("floor", g, -2600, SCREEN_X + 400, FLOOR_Y - 2, FLOOR_Y - 0.5, -900, bz + 2000, "#cfd3cc")
    sbox("hitting mat (turf)", g, bx - 900, bx + 900, FLOOR_Y - 0.5, FLOOR_Y, bz - 300, bz + 1250, "#3f8f4a")
    sbox("target line (to the target)", g, -2400, SCREEN_X, FLOOR_Y, FLOOR_Y + 0.6, bz - 4, bz + 4, "#ffffff")
    scyl("alignment stick (in the box), parallel to target line", g, (bx + 300, FLOOR_Y + 5, bz + 260), 5, 1500, "x", "#e8c21c")
    g = "Setup: ball & capture zones"
    ssph("golf ball (at address)", g, BALL, BALL_R, "#f4f4f2")
    sbox("ball-data capture zone ≥ 305 × 254 mm (12 × 10 in)", g, bx - 152, bx + 152, FLOOR_Y + 0.1, FLOOR_Y + 0.7, bz - 127, bz + 127, "#2a78d6", 0.35)
    sbox("club-data zone ≥ 203 × 203 mm (8 × 8 in)", g, bx - 101, bx + 101, FLOOR_Y + 0.8, FLOOR_Y + 1.3, bz - 101, bz + 101, "#eb6834", 0.4)
    t = math.tan(math.radians(LAUNCH_DEG))
    for k in range(1, 13):
        dx = k * 240.0
        if bx + dx > SCREEN_X - 40:
            break
        ssph("ball-flight path (14° launch)", g, (bx + dx, by + dx * t, bz), 10, "#f4f4f2", 0.55)
    g = "Setup: golfer (right-handed)"
    for side, dx in (("trail", -230), ("lead", 230)):
        sbox(f"{side} foot", g, bx + dx - 50, bx + dx + 50, FLOOR_Y, FLOOR_Y + 70, TOE_Z, TOE_Z + 270, "#3a3f47")
        scyl(f"{side} leg", g, (bx + dx * 0.8, FLOOR_Y + 470, TOE_Z + 150), 65, 800, "y", "#8a94a6", 0.3)
    sbox("torso (bent toward the ball)", g, bx - 200, bx + 200, FLOOR_Y + 870, FLOOR_Y + 1420, TOE_Z - 40, TOE_Z + 200, "#8a94a6", 0.3)
    ssph("head (eyes over the ball line)", g, (bx, FLOOR_Y + 1540, TOE_Z - 60), 110, "#8a94a6", 0.3)
    g = "Setup: impact screen / target"
    sbox("impact screen / net (indoor target)", g, SCREEN_X, SCREEN_X + 25, FLOOR_Y, FLOOR_Y + 2700, bz - 1500, bz + 1500, "#f2f2ee", 0.85)
    sbox("aim point on screen", g, SCREEN_X - 2, SCREEN_X, by + 3048 * t - 150, by + 3048 * t + 150, bz - 150, bz + 150, "#eb6834", 0.9)
    return S
