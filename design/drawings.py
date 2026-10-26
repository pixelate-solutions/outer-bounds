"""Engineering drawings (SVG) generated from model.P.

Exterior, internal and detail views are produced from the same primitive list as the 3D viewer,
so the drawings and the 3D model cannot disagree.
"""
import math
from html import escape
import model as M

INK = "#1b1c1e"; DIM = "#2a5db0"; HID = "#9aa0a6"; CL = "#c0392b"


# ------------------------------------------------------------------ geometry
def rot_y(p, c, deg):
    if not deg:
        return p
    r = math.radians(deg); x, y, z = p[0]-c[0], p[1], p[2]-c[2]
    return (c[0] + x*math.cos(r) + z*math.sin(r), y, c[2] - x*math.sin(r) + z*math.cos(r))


def faces(p, explode=0.0):
    """List of (polygon3d, normal) for a primitive, in world coords."""
    cx, cy, cz = [p["c"][i] + explode*p["ex"][i] for i in range(3)]
    out = []
    if p["t"] == "mesh":
        V = [(v[0]+explode*p["ex"][0], v[1]+explode*p["ex"][1], v[2]+explode*p["ex"][2]) for v in p["v"]]
        return [([V[i] for i in f], tuple(n)) for f, n in zip(p["f"], p["fn"])]
    if p["t"] == "box":
        hx, hy, hz = [v/2 for v in p["s"]]
        V = [(cx+sx*hx, cy+sy*hy, cz+sz*hz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
        idx = lambda sx, sy, sz: ((sx+1)//2)*4 + ((sy+1)//2)*2 + (sz+1)//2
        F = [((1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1), (1, 0, 0)),
             ((-1, -1, -1), (-1, -1, 1), (-1, 1, 1), (-1, 1, -1), (-1, 0, 0)),
             ((-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1), (0, 1, 0)),
             ((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1), (0, -1, 0)),
             ((-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1), (0, 0, 1)),
             ((-1, -1, -1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), (0, 0, -1))]
        for f in F:
            poly = [rot_y(V[idx(*v)], (cx, cy, cz), p["ry"]) for v in f[:4]]
            n = rot_y(f[4], (0, 0, 0), p["ry"])
            out.append((poly, n))
    else:
        n, r, h = p["seg"], p["r"], p["h"]
        ring = []
        for k in range(n):
            a = 2*math.pi*k/n; u, v = r*math.cos(a), r*math.sin(a)
            ring.append({"x": ((-h/2, u, v), (h/2, u, v)), "y": ((u, -h/2, v), (u, h/2, v)), "z": ((u, v, -h/2), (u, v, h/2))}[p["ax"]])
        A = [rot_y((cx+a[0][0], cy+a[0][1], cz+a[0][2]), (cx, cy, cz), p["ry"]) for a in ring]
        B = [rot_y((cx+a[1][0], cy+a[1][1], cz+a[1][2]), (cx, cy, cz), p["ry"]) for a in ring]
        axn = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[p["ax"]]
        axn = rot_y(axn, (0, 0, 0), p["ry"])
        out.append((B, axn)); out.append((list(reversed(A)), tuple(-v for v in axn)))
        for k in range(n):
            k2 = (k+1) % n
            mid = [(A[k][i]+A[k2][i]+B[k][i]+B[k2][i])/4 - (cx, cy, cz)[i] for i in range(3)]
            m = math.sqrt(sum(v*v for v in mid)) or 1
            out.append(([A[k], A[k2], B[k2], B[k]], tuple(v/m for v in mid)))
    return out


VIEWS = {  # name: (right vector, up vector, toward-viewer vector)
    "front": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    "rear": ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
    "top": ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    "bottom": ((1, 0, 0), (0, 0, 1), (0, -1, 0)),
    "right": ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
    "left": ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),
}


def iso_view(az=-35, el=28):
    a, e = math.radians(az), math.radians(el)
    t = (math.sin(a)*math.cos(e), math.sin(e), math.cos(a)*math.cos(e))     # toward viewer
    r = (math.cos(a), 0, -math.sin(a))
    u = (t[1]*r[2]-t[2]*r[1], t[2]*r[0]-t[0]*r[2], t[0]*r[1]-t[1]*r[0])
    return (r, u, t)


dot = lambda a, b: a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


def hexmix(col, k, base=(255, 255, 255)):
    col = col.lstrip("#"); c = [int(col[i:i+2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(int(c[i]*k + base[i]*(1-k)) for i in range(3))


def shade(col, f):
    col = col.lstrip("#"); c = [int(col[i:i+2], 16) for i in (0, 2, 4)]
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(v*f))) for v in c)


class Sheet:
    def __init__(self, w, h, title, number, scale_note=""):
        self.w, self.h, self.title, self.number, self.scale_note = w, h, title, number, scale_note
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def svg(self):
        tb = (f'<g font-family="ui-monospace,Menlo,monospace" font-size="11" fill="{INK}">'
              f'<rect x="{self.w-620}" y="{self.h-70}" width="610" height="60" fill="#fff" stroke="{INK}"/>'
              f'<line x1="{self.w-620}" y1="{self.h-45}" x2="{self.w-10}" y2="{self.h-45}" stroke="{INK}"/>'
              f'<line x1="{self.w-130}" y1="{self.h-70}" x2="{self.w-130}" y2="{self.h-10}" stroke="{INK}"/>'
              f'<text x="{self.w-612}" y="{self.h-52}" font-weight="700">OUTER BOUNDS PRO · {escape(self.title)}</text>'
              f'<text x="{self.w-612}" y="{self.h-30}">Units mm · third-angle projection · {escape(self.scale_note)}</text>'
              f'<text x="{self.w-612}" y="{self.h-16}">Rev A · 2026-10-07 · general tolerance ±0.2 unless noted</text>'
              f'<text x="{self.w-122}" y="{self.h-52}">SHEET</text><text x="{self.w-122}" y="{self.h-22}" font-size="20" font-weight="700">{self.number}</text></g>')
        return (f'<svg class="dwg" viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(self.title)}">'
                f'<rect x="1" y="1" width="{self.w-2}" height="{self.h-2}" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
                + "".join(self.parts) + tb + "</svg>")


def project(prims, view, ox, oy, k, explode=0.0, style="ext", hide_groups=(), only_groups=None, ghost_groups=()):
    """Painter-sorted projection. style: 'ext' = engineering white fill + ink edges, 'shade' = tinted solids."""
    r, u, t = view if isinstance(view, tuple) else VIEWS[view]
    polys = []
    for p in prims:
        if p["g"] in hide_groups:
            continue
        if only_groups is not None and p["g"] not in only_groups and p["g"] not in ghost_groups:
            continue
        ghost = p["g"] in ghost_groups
        for poly, n in faces(p, explode):
            if dot(n, t) <= 1e-6:
                continue
            depth = sum(dot(v, t) for v in poly)/len(poly)
            pts = [(ox + dot(v, r)*k, oy - dot(v, u)*k) for v in poly]
            polys.append((depth, pts, p, n, ghost))
    polys.sort(key=lambda a: a[0])
    out = []
    light = (0.35, 0.75, 0.55)
    for depth, pts, p, n, ghost in polys:
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        if ghost:
            out.append(f'<polygon points="{d}" fill="none" stroke="{HID}" stroke-width="0.6" stroke-dasharray="4 3"/>')
        elif style == "ext":
            fill = "#ffffff" if p["col"] not in (M.C["glass"], M.C["grill"], "#000000", "#050505") else "#e9ecf2"
            out.append(f'<polygon points="{d}" fill="{fill}" stroke="{INK}" stroke-width="0.8" stroke-linejoin="round"/>')
        else:
            lam = 0.55 + 0.45*max(0, dot(n, light)/math.sqrt(dot(light, light)))
            fill = shade(p["col"], lam*1.25)
            op = p.get("a", 1.0)
            out.append(f'<polygon points="{d}" fill="{fill}" fill-opacity="{op}" stroke="#111" stroke-opacity="0.35" stroke-width="0.4" stroke-linejoin="round"/>')
    return "".join(out)


def to2d(view, ox, oy, k):
    r, u, t = view if isinstance(view, tuple) else VIEWS[view]
    return lambda P3: (ox + dot(P3, r)*k, oy - dot(P3, u)*k)


def dim(x0, y0, x1, y1, off, label, horiz=True, col=DIM, fs=12):
    """Dimension line between two 2D points, offset perpendicular by `off` px."""
    if horiz:
        y = (y0 if off < 0 else y1) + off
        y = min(y0, y1) + off if off < 0 else max(y0, y1) + off
        return (f'<g stroke="{col}" fill="{col}" font-size="{fs}" font-family="ui-monospace,Menlo,monospace">'
                f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y+(4 if off>0 else -4)}" stroke-width="0.6"/>'
                f'<line x1="{x1}" y1="{y1}" x2="{x1}" y2="{y+(4 if off>0 else -4)}" stroke-width="0.6"/>'
                f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke-width="0.8" marker-start="url(#ar)" marker-end="url(#ar)"/>'
                f'<text x="{(x0+x1)/2}" y="{y-4}" text-anchor="middle" stroke="none">{escape(label)}</text></g>')
    x = min(x0, x1) + off if off < 0 else max(x0, x1) + off
    return (f'<g stroke="{col}" fill="{col}" font-size="{fs}" font-family="ui-monospace,Menlo,monospace">'
            f'<line x1="{x0}" y1="{y0}" x2="{x+(4 if off>0 else -4)}" y2="{y0}" stroke-width="0.6"/>'
            f'<line x1="{x1}" y1="{y1}" x2="{x+(4 if off>0 else -4)}" y2="{y1}" stroke-width="0.6"/>'
            f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke-width="0.8" marker-start="url(#ar)" marker-end="url(#ar)"/>'
            f'<text x="{x-5}" y="{(y0+y1)/2}" text-anchor="middle" stroke="none" transform="rotate(-90 {x-5} {(y0+y1)/2})">{escape(label)}</text></g>')


MARK = ('<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,1 L10,5 L0,9 z" fill="{DIM}"/></marker></defs>')


def label(x, y, text, fs=13, bold=True, col=INK, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{fs}" font-family="-apple-system,Segoe UI,Helvetica,Arial" '
            f'font-weight="{700 if bold else 400}" fill="{col}" text-anchor="{anchor}">{escape(text)}</text>')


def leader(x0, y0, x1, y1, text, fs=11, anchor="start"):
    return (f'<g font-family="-apple-system,Segoe UI,Helvetica,Arial" font-size="{fs}" fill="{INK}">'
            f'<circle cx="{x0}" cy="{y0}" r="2" fill="{INK}"/><line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{INK}" stroke-width="0.6"/>'
            f'<text x="{x1 + (3 if anchor=="start" else -3)}" y="{y1+4}" text-anchor="{anchor}">{escape(text)}</text></g>')


def centermark(x, y, s=8):
    return (f'<g stroke="{CL}" stroke-width="0.5" stroke-dasharray="6 2 1 2"><line x1="{x-s}" y1="{y}" x2="{x+s}" y2="{y}"/>'
            f'<line x1="{x}" y1="{y-s}" x2="{x}" y2="{y+s}"/></g>')


# ------------------------------------------------------------------ sheets
def sheet_general_arrangement(P):
    k = 1.55
    sh = Sheet(1500, 1060, "GENERAL ARRANGEMENT · EXTERIOR", "M-01", "scale 1:1.55 on screen")
    sh.add(MARK)
    ext = [p for p in P if p["ext"]]
    # front view
    fx, fy = 360, 470
    sh.add(label(fx-200, fy-215, "FRONT VIEW (faces the ball)"))
    sh.add(project(ext, "front", fx, fy, k))
    f2 = to2d("front", fx, fy, k)
    a, b = f2((M.X0-M.BUMP, M.Y0, 0)), f2((M.X1+M.BUMP, M.Y0, 0)); sh.add(dim(a[0], a[1], b[0], b[1], 34, f"{M.W+2*M.BUMP:.0f} overall (incl. bumpers)"))
    a, b = f2((M.X0, M.Y0, 0)), f2((M.X1, M.Y0, 0)); sh.add(dim(a[0], a[1], b[0], b[1], 16, f"{M.W:.0f} shell"))
    a, b = f2((M.X1+M.BUMP, M.TOP, 0)), f2((M.X1+M.BUMP, M.Y0, 0)); sh.add(dim(a[0], a[1], b[0], b[1], 22, f"{M.TOP-M.Y0:.0f} overall", horiz=False))
    a, b = f2((M.X0-M.BUMP, M.TOP, 0)), f2((M.X0-M.BUMP, M.Y1, 0)); sh.add(dim(a[0], a[1], b[0], b[1], -40, f"{M.TOP-M.Y1:.0f} crown", horiz=False))
    a, b = f2((M.WIN["x0"], M.WIN["y1"], 0)), f2((M.WIN["x1"], M.WIN["y1"], 0)); sh.add(dim(a[0], a[1], b[0], b[1], -14, f"IR window {M.WIN['x1']-M.WIN['x0']:.0f}"))
    a, b = f2((M.X0-M.BUMP, M.WIN["y1"], 0)), f2((M.X0-M.BUMP, M.WIN["y0"], 0)); sh.add(dim(a[0], a[1], b[0], b[1], -22, f"{M.WIN['y1']-M.WIN['y0']:.0f}", horiz=False))
    # camera axes behind the window
    for nm, (x, y) in M.CAMS.items():
        q = f2((x, y, 0)); sh.add(centermark(*q, 10)); sh.add(label(q[0]+12, q[1]-8, nm, 10, False, CL))
    t = f2((M.CAMS["CAM-T"][0], M.CAMS["CAM-T"][1], 0)); bq = f2((M.CAMS["CAM-B"][0], M.CAMS["CAM-B"][1], 0))
    sh.add(dim(t[0], t[1], bq[0], bq[1], -50, "80 stereo baseline", horiz=False, col=CL))
    c = f2((M.CAMS["CAM-C"][0], M.CAMS["CAM-C"][1], 0)); mid = f2((M.CAMS["CAM-B"][0], M.CAMS["CAM-C"][1], 0))
    sh.add(dim(mid[0], mid[1], c[0], c[1], 0, "85 club cam offset", horiz=True, col=CL))
    # top view (above front view)
    tx, ty = fx, 140
    sh.add(label(tx-200, 50, "TOP VIEW"))
    sh.add(project(ext, "top", tx, ty, k))
    t2 = to2d("top", tx, ty, k)
    a, b = t2((M.X1+M.BUMP, 0, M.Z0)), t2((M.X1+M.BUMP, 0, M.Z1)); sh.add(dim(a[0], a[1], b[0], b[1], 22, f"{M.D:.0f}", horiz=False))
    for x, z, txt, dx, dy in ((72, 20, "2.4\" sunlight-readable display", 150, -40), (-72, 16, "POWER · MODE · L/R (IP67)", -40, -95),
                              (0, 19, "hidden grip: 90 mm bar, flush with top, 19 mm finger gaps", 60, -95)):
        p0 = t2((x, M.TOP, z)); sh.add(leader(p0[0], p0[1], p0[0]+dx, p0[1]+dy, txt, 10, "start" if dx > 0 else "end"))
    # right view
    rx, ry = 800, fy
    sh.add(label(rx-70, fy-220, "RIGHT END (target side)"))
    sh.add(project(ext, "right", rx, ry, k))
    r2 = to2d("right", rx, ry, k)
    p0 = r2((M.X1+M.BUMP, 20, -14)); sh.add(leader(p0[0], p0[1], p0[0]+80, p0[1]-90, "radome: down-range radar head", 10))
    # rear view
    bx, by = 1190, fy
    sh.add(label(bx-200, fy-220, "REAR VIEW"))
    sh.add(project(ext, "rear", bx, by, k))
    b2 = to2d("rear", bx, by, k)
    for (x, y, txt, dx, dy) in ((M.USBC[0], M.USBC[1], "USB-C 65 W PD, IP67", -60, 110), (M.VENT[0], M.VENT[1], "ePTFE pressure vent", -40, 160),
                                 (-92, 50, "blower intake", 40, -150), (-45, 64, "exhaust", -60, -110), (-5, -50, "rating label", 60, 110)):
        p0 = b2((x, y, M.Z0)); sh.add(leader(p0[0], p0[1], p0[0]+dx, p0[1]+dy, txt, 10, "start" if dx > 0 else "end"))
    # bottom view
    ux, uy = fx, 850
    sh.add(label(ux-200, 765, "BOTTOM VIEW"))
    sh.add(project(ext, "bottom", ux, uy, k))
    u2 = to2d("bottom", ux, uy, k)
    p0 = u2((M.TRIPOD[0], M.Y0, 21)); sh.add(centermark(*p0, 10)); sh.add(leader(p0[0], p0[1], p0[0]-50, p0[1]+70, "1/4\"-20 tripod thread in bench foot", 10, "end"))
    p0 = u2((44, M.Y0, 0)); sh.add(leader(p0[0], p0[1], p0[0]+120, p0[1]+80, "battery door, 96 x 74 opening, tool-less latch", 10))
    a, b = u2((M.TRIPOD[0], M.Y0, M.Z1)), u2((M.X0, M.Y0, M.Z1)); sh.add(dim(b[0], b[1], a[0], a[1], 30, f"{M.TRIPOD[0]-M.X0:.0f} to tripod axis"))
    # notes
    notes = ["NOTES", "1. Shell PC/ABS UL94 V-0, faceted (no blends > R1), texture MT-11010; body graphite, crown black.",
             "2. TPE end caps 65A, faceted, stretch-on; radomes PC 3.6 mm (λ/2 at 24.2 GHz), no metallic paint.",
             "3. IR window: 2.0 mm chemically strengthened glass, IR-pass ink (T>90 % @ 940 nm), AR both sides,",
             "   IR-opaque isolation bands between LED and camera zones (prevents strobe cross-talk).",
             "4. Sealing IP54: silicone die-cut gaskets at window, halves, battery door; ePTFE vent.",
             "5. Mass target 1.75 kg incl. pack (bench 0.42, pack 0.30, shell+crown 0.55, electronics 0.25, caps 0.12).",
             "6. Optics symmetric about the centre line: stereo pair square, pitched 3° down; club camera toed in 7°.",
             "7. Grip bar: glass-filled PA6 core, TPE overmold underside, rated 10x unit mass (175 N) static.",
             "8. Runs on the pack or on USB-C; with the cord in it runs and charges together (NVDC power path)."]
    for i, n in enumerate(notes):
        sh.add(label(720, 740 + i*20, n, 12, i == 0))
    return sh


def sheet_internal(P):
    k = 1.55
    sh = Sheet(1500, 1060, "INTERNAL ARRANGEMENT (shell, window, end caps removed)", "M-02", "scale 1:1.55 on screen")
    sh.add(MARK)
    shell_groups = set(M.SHELL_GROUPS)
    inner = [p for p in P if p["g"] not in shell_groups]
    ghost = [p for p in P if p["g"] in ("Front shell (PC/ABS)", "Rear shell (PC/ABS)")]
    fx, fy = 340, 330
    sh.add(label(fx-190, 120, "FRONT VIEW, window removed"))
    sh.add(project(ghost, "front", fx, fy, k, only_groups=set(), ghost_groups={"Front shell (PC/ABS)", "Rear shell (PC/ABS)"}))
    sh.add(project(inner, "front", fx, fy, k, style="shade"))
    f2 = to2d("front", fx, fy, k)
    for x, y, txt in ((0, 50, "CAM-T IMX900"), (0, -30, "CAM-B IMX900"), (56, 50, "CAM-C club IMX900"), (-84, 10, "LED-A (8x)"),
                      (86, 10, "LED-B (8x)"), (56, -26, "LED-C (8x)"), (-60, -60, "bench foot · tripod thread"), (60, -63, "4S1P pack (bay)")):
        p0 = f2((x, y, 40)); sh.add(leader(p0[0], p0[1], p0[0] + (30 if x >= 0 else -30), p0[1]-28, txt, 10, "start" if x >= 0 else "end"))
    tx, ty = 1050, 330
    sh.add(label(tx-190, 120, "SECTION A-A: TOP VIEW, top wall removed"))
    sh.add(project(ghost, "top", tx, ty, k, only_groups=set(), ghost_groups={"Front shell (PC/ABS)", "Rear shell (PC/ABS)"}))
    sh.add(project([p for p in inner if p["g"] != "Display & buttons"], "top", tx, ty, k, style="shade"))
    t2 = to2d("top", tx, ty, k)
    for i, (x, z, txt) in enumerate(((-110, -14, "rear radar head"), (-92, -18, "IP55 blower"), (-45, -24, "fin stack"),
                                     (-20, 1, "QCS6490 SoM + Cu spreader"), (0, 21, "optical bench 6061-T651, 10 mm"))):
        p0 = t2((x, 60, z)); sh.add(leader(p0[0], p0[1], 830, 190 + i*34, txt, 10, "end"))
    for i, (x, z, txt) in enumerate(((40, 7, "carrier PCB (front: FPC, MCU, charger)"), (44, -30, "battery pack below"), (110, -14, "down-range radar"))):
        p0 = t2((x, 60, z)); sh.add(leader(p0[0], p0[1], 1270, 210 + i*44, txt, 10))
    sx, sy = 340, 830
    sh.add(label(sx-190, 580, "SECTION B-B: RIGHT SIDE, end cap removed"))
    sh.add(project(ghost, "right", sx, sy, k, only_groups=set(), ghost_groups={"Front shell (PC/ABS)", "Rear shell (PC/ABS)"}))
    sh.add(project(inner, "right", sx, sy, k, style="shade"))
    r2 = to2d("right", sx, sy, k)
    a, b = r2((0, 0, M.BENCH["z0"])), r2((0, 0, M.CARRIER["z0"])); sh.add(dim(a[0], a[1], b[0], b[1], -160, f"{M.BENCH['z0']-M.CARRIER['z0']:.0f} bench→carrier"))
    for y, z, txt in ((-63, 0, "4S1P pack, 4x LG M58T"), (68, -24, "heat pipe → fin stack → blower"), (10, 21, "bench"), (-20, 7, "carrier"), (40, 32, "lens / filter")):
        p0 = r2((120, y, z)); sh.add(leader(p0[0], p0[1], p0[0]+90, p0[1]+(30 if y < 0 else -20), txt, 10))
    notes = ["THERMAL & STRUCTURE",
             "• SoM bay is sealed (IP54). Heat leaves through a 6 mm Cu heat pipe to an Al fin stack in a separate",
             "  ducted bay; the IP55 blower pulls rear air across the fins and out the top grille.",
             "• Optical bench is a 3-point kinematic mount (1 fixed, 1 slotted, 1 floating) to the front shell,",
             "  so shell flex cannot move the stereo pair (requirement: < 0.01° drift).",
             "• Tripod thread is tapped in the bench foot, so tripod load goes into the bench, not the plastic.",
             "• Battery bay is shaded from the fin-stack exhaust (charge stops > 45 °C).",
             "• Strobe bulk caps (2x 470 µF/50 V) sit on the carrier back side, 17 mm envelope."]
    for i, n in enumerate(notes):
        sh.add(label(760, 700 + i*20, n, 12, i == 0))
    return sh


def sheet_bench():
    """Optical bench detail drawing (front view with bores, LED pads, mount points)."""
    k = 3.0
    sh = Sheet(1500, 1000, "OPTICAL BENCH DETAIL · 6061-T651", "M-03", "scale 3:1 on screen")
    sh.add(MARK)
    B = M.BENCH; ox, oy = 750, 420
    X = lambda x: ox + x*k; Y = lambda y: oy - y*k
    sh.add(label(70, 70, "FRONT VIEW (lens side)"))
    sh.add(f'<rect x="{X(B["x0"])}" y="{Y(B["y1"])}" width="{(B["x1"]-B["x0"])*k}" height="{(B["y1"]-B["y0"])*k}" fill="#f4f6f8" stroke="{INK}" stroke-width="1.2"/>')
    sh.add(f'<rect x="{X(-110)}" y="{Y(B["y0"])}" width="{220*k}" height="{34*k}" fill="#eef1f4" stroke="{INK}" stroke-width="1"/>')
    holes = []
    for nm, (x, y) in M.CAMS.items():
        sh.add(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{10.5*k}" fill="#fff" stroke="{INK}"/>')   # Ø21 H7 holder bore
        sh.add(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{7.0*k}" fill="none" stroke="{HID}" stroke-dasharray="4 3"/>')
        sh.add(centermark(X(x), Y(y), 34))
        for dx, dy in ((-10.0, 0.0), (10.0, 0.0)):
            sh.add(f'<circle cx="{X(x+dx)}" cy="{Y(y+dy)}" r="{1.1*k}" fill="#fff" stroke="{INK}"/>')
        sh.add(label(X(x)+30*k/3, Y(y)-11*k, f"{nm}: Ø21 H7 bore, 2x M2 on 20.0 pitch, seat yaw {M.CAM_AIM[nm][0]:.0f}° / pitch {M.CAM_AIM[nm][1]:.0f}°", 11, False, CL))
        holes.append((nm, x, y))
    for nm, (x, y, yaw) in M.LEDB.items():
        sh.add(f'<rect x="{X(x-20)}" y="{Y(y+15)}" width="{40*k}" height="{30*k}" fill="none" stroke="{INK}" stroke-dasharray="7 3"/>')
        sh.add(label(X(x-19), Y(y+15)-6, f"{nm} pad, {abs(yaw):.0f}° wedge, 2x M2", 11, False))
    for (x, y, t) in ((-100, -66, "Ø4 fixed datum (A)"), (100, -66, "Ø4 x 6 slot (B)"), (0, 68, "M3 floating (C)")):
        sh.add(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{2.2*k}" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
        sh.add(label(X(x)+8, Y(y)+(-8 if y > 0 else 22), t, 11, False))
    sh.add(f'<circle cx="{X(M.TRIPOD[0])}" cy="{Y(B["y0"]-34)+3}" r="5" fill="{CL}"/>')
    sh.add(label(X(M.TRIPOD[0])+10, Y(B["y0"]-34)-4, "1/4\"-20 UNC x 10 deep from below", 11, False, CL))
    a = (X(B["x0"]), Y(B["y1"])); b = (X(B["x1"]), Y(B["y1"])); sh.add(dim(a[0], a[1], b[0], b[1], -30, "220"))
    a = (X(B["x1"]), Y(B["y1"])); b = (X(B["x1"]), Y(B["y0"]-34)); sh.add(dim(a[0], a[1], b[0], b[1], 30, "152", horiz=False))
    t, bo = M.CAMS["CAM-T"], M.CAMS["CAM-B"]
    sh.add(dim(X(t[0]), Y(t[1]), X(bo[0]), Y(bo[1]), -60, "80.00 ±0.01", horiz=False, col=CL))
    rows = [("Bore", "X", "Y", "Spec")] + [(n, f"{x:+.2f}", f"{y:+.2f}", "Ø21.000 H7, ⟂ 0.01 to seat") for n, x, y in holes]
    tbx, tby = 70, 820
    sh.add(label(tbx, tby-14, "HOLE TABLE (datum A = fixed mount, origin = enclosure centre)", 12))
    for i, r in enumerate(rows):
        for j, cell in enumerate(r):
            sh.add(label(tbx + [0, 130, 230, 330][j], tby + 10 + i*18, cell, 11, i == 0))
    notes = ["NOTES", "1. Material 6061-T651, stress-relieved, flatness 0.02 over bench face.",
             "2. Camera bores reamed in one setup; seat faces at 3.00° pitch (CAM-C also 7.00° yaw) ±0.05°.",
             "3. Black hard anodize Type III 25 µm (low IR reflectance inside the optical cavity).",
             "4. Volume path ≥10k: extrusion + 5-axis datum faces (die-cast not stable enough).",
             "5. Bench 10 mm; camera stack board-back→lens-front 26.5 mm (VC + CIL361), 4.5 mm air to window."]
    for i, n in enumerate(notes):
        sh.add(label(780, 780 + i*20, n, 12, i == 0))
    return sh


def sheet_pcbs():
    sh = Sheet(1500, 1060, "PCB ASSEMBLY DRAWINGS · CARRIER / LED / RADAR", "M-04", "carrier 4:1, small boards 6:1")
    sh.add(MARK)
    k = 4.0; ox, oy = 360, 300
    cr = M.CARRIER
    X = lambda x: ox + x*k; Y = lambda y: oy - (y - (cr["y0"]+cr["y1"])/2)*k
    sh.add(label(60, 70, "CARRIER PCB · FRONT (component side A) · 160 x 92 mm · 10-layer 1+8+1 HDI"))
    sh.add(f'<rect x="{X(cr["x0"])}" y="{Y(cr["y1"])}" width="{(cr["x1"]-cr["x0"])*k}" height="{(cr["y1"]-cr["y0"])*k}" rx="8" fill="#e8f3ec" stroke="{INK}" stroke-width="1.4"/>')
    parts = [("J10 CAM-T", -63, 38, -47, 44), ("J11 CAM-B", -43, 38, -27, 44), ("J12 CAM-C", 12, 38, 28, 44),
             ("U20 STM32G474", -12, -10, 2, 4), ("U40 MSPM0G3507", 10, -30, 20, -22), ("U2 BQ25730", 40, 18, 52, 30),
             ("U1 TPS25751", 56, 18, 62, 24), ("Q3", 40.5, 2.5, 47.5, 9.5), ("Q4", 54.5, 2.5, 61.5, 9.5), ("Q5", 40.5, -11.5, 47.5, -4.5),
             ("Q6", 54.5, -11.5, 61.5, -4.5), ("L2 2.2µH", 66, -2, 78, 10), ("L10 3.8V", -71, 15, -61, 25), ("L11 5V", -71, -3, -61, 7),
             ("U5 SCL3300", -48, 26, -40, 34), ("J3 BATT", 70, 30, 78, 46), ("L30 boost", -60, -34, -50, -24),
             ("U30 LM5155", -46, -34, -40, -28), ("J20-22 LED", -30, 22, -12, 30), ("J30/31 RADAR", 22, -40, 38, -34),
             ("J40 DISPLAY", 0, 42, 10, 48), ("U12 TPS62933", -46, 4, -40, 10), ("U6/7 BMP585/SHT45", -20, 34, -8, 40), ("J2 USB-C", 56, -40, 66, -32)]
    for (n, x0, y0, x1, y1) in parts:
        sh.add(f'<rect x="{X(x0)}" y="{Y(y1)}" width="{(x1-x0)*k}" height="{(y1-y0)*k}" fill="#fff" stroke="{INK}" stroke-width="0.8"/>')
        sh.add(f'<text x="{X((x0+x1)/2)}" y="{Y((y0+y1)/2)+3}" font-size="9.5" text-anchor="middle" font-family="ui-monospace,Menlo,monospace" fill="{INK}">{escape(n)}</text>')
    for (x, y) in ((-75, -37), (75, -37), (-75, 45), (75, 45)):
        sh.add(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{1.6*k}" fill="#fff" stroke="{INK}"/>')
    a = (X(cr["x0"]), Y(cr["y0"])); b = (X(cr["x1"]), Y(cr["y0"])); sh.add(dim(a[0], a[1], b[0], b[1], 26, "160"))
    a = (X(cr["x1"]), Y(cr["y1"])); b = (X(cr["x1"]), Y(cr["y0"])); sh.add(dim(a[0], a[1], b[0], b[1], 26, "92", horiz=False))
    sh.add(label(X(-40), Y(-44)+56, "Back side B: U10 QCS6490 SoM (39x33x2.75 LGA + shield) at X -39.5..-0.5, Y 2..35 · C31/C32 470µF · Cu spreader", 11, False))
    # layer stack
    sx, sy = 60, 560
    sh.add(label(sx, sy, "CARRIER STACK-UP (1.6 mm, 10L, 1+8+1 HDI, ENIG)"))
    stack = [("L1", "Signal / components A (laser µvia to L2)"), ("L2", "GND"), ("L3", "MIPI CSI 100 Ω diff, USB 90 Ω"), ("L4", "GND"),
             ("L5", "Power: VSYS / 3V8_SOM"), ("L6", "Power: 5V0 / 3V3 / STROBE_BUS (isolated pour)"), ("L7", "GND"),
             ("L8", "Low-speed signals / SPI / I2C"), ("L9", "GND"), ("L10", "Signal / components B (SoM)")]
    for i, (l, d) in enumerate(stack):
        col = "#c47a3a" if "GND" not in d else "#9a6a40"
        sh.add(f'<rect x="{sx}" y="{sy+12+i*22}" width="60" height="14" fill="{col}"/>')
        sh.add(label(sx+70, sy+24+i*22, f"{l}  {d}", 11, False))
    # LED board
    k2 = 6.0; lx, ly = 920, 160
    sh.add(label(lx-40, 70, "LED STROBE BOARD (x3) · 40 x 30 mm · 4L FR-4 2 oz · thermal vias"))
    sh.add(f'<rect x="{lx}" y="{ly}" width="{40*k2}" height="{30*k2}" rx="6" fill="#e6f0f7" stroke="{INK}" stroke-width="1.3"/>')
    for i in range(4):
        for j in range(2):
            cx, cy = lx + (8 + i*8)*k2, ly + (10 + j*10)*k2
            sh.add(f'<rect x="{cx-1.93*k2}" y="{cy-1.93*k2}" width="{3.85*k2}" height="{3.85*k2}" fill="#fff" stroke="{INK}"/>')
            sh.add(f'<circle cx="{cx}" cy="{cy}" r="{1.3*k2}" fill="none" stroke="{HID}"/>')
            sh.add(f'<text x="{cx}" y="{cy+3}" font-size="9" text-anchor="middle" font-family="ui-monospace,Menlo,monospace">D{1+i+j*4}</text>')
    for (n, x0, y0, w, h) in (("Q1 CSD18543", 2, 1, 5, 4), ("U1 OPA810", 9, 1, 6, 4), ("U2/U3 '123", 17, 1, 8, 4), ("U4 TLV3201", 27, 1, 5, 4),
                              ("RS 0R1", 33, 1, 5, 4), ("C1-4 2.2µ", 2, 25, 14, 4), ("C5 100µF", 18, 25, 8, 4), ("J1 GH-10", 28, 25, 10, 4)):
        sh.add(f'<rect x="{lx+x0*k2}" y="{ly+y0*k2}" width="{w*k2}" height="{h*k2}" fill="#fff" stroke="{INK}" stroke-width="0.7"/>')
        sh.add(f'<text x="{lx+(x0+w/2)*k2}" y="{ly+(y0+h/2)*k2+3}" font-size="8.5" text-anchor="middle" font-family="ui-monospace,Menlo,monospace">{escape(n)}</text>')
    sh.add(dim(lx, ly+30*k2, lx+40*k2, ly+30*k2, 22, "40"))
    sh.add(dim(lx+40*k2, ly, lx+40*k2, ly+30*k2, 22, "30", horiz=False))
    sh.add(label(lx, ly+30*k2+60, "8 LEDs in series, 23–34 V at 5 A (VF 2.9–4.2 V each). Linear sink holds 5.0 A; loop (bus cap → LEDs → FET → RS)", 11, False))
    sh.add(label(lx, ly+30*k2+78, "kept < 15 mm²; 2x M2 to bench wedge pad; NTC under LED row.", 11, False))
    # radar head
    rx, ry = 920, 600
    sh.add(label(rx-40, 560, "RADAR HEAD BOARD (x2) · 24 x 24 mm · 4L FR-4"))
    sh.add(f'<rect x="{rx}" y="{ry}" width="{24*k2}" height="{24*k2}" rx="5" fill="#e8f3ec" stroke="{INK}" stroke-width="1.3"/>')
    sh.add(f'<rect x="{rx+1.5*k2}" y="{ry+4.5*k2}" width="{21*k2}" height="{15*k2}" fill="#fff6dc" stroke="{INK}"/>')
    sh.add(f'<text x="{rx+12*k2}" y="{ry+12*k2+3}" font-size="10" text-anchor="middle" font-family="ui-monospace,Menlo,monospace">SMR-333 (21 x 15)</text>')
    sh.add(f'<rect x="{rx+9*k2}" y="{ry+20.5*k2}" width="{6*k2}" height="{3*k2}" fill="#fff" stroke="{INK}"/>')
    sh.add(f'<text x="{rx+12*k2}" y="{ry+22*k2+3}" font-size="8.5" text-anchor="middle" font-family="ui-monospace,Menlo,monospace">J1 SH-6</text>')
    sh.add(dim(rx, ry+24*k2, rx+24*k2, ry+24*k2, 22, "24"))
    sh.add(label(rx, ry+24*k2+60, "Module + LDO + IF op-amp on head; ADC/MCU on carrier. Heads mirror-symmetric:", 11, False))
    sh.add(label(rx, ry+24*k2+78, "±58° yaw / 12° up; the L/R setting swaps rear and down-range roles.", 11, False))
    return sh


def sheet_exploded(P):
    sh = Sheet(1500, 1060, "EXPLODED ISOMETRIC · ASSEMBLY ORDER", "M-05", "not to scale")
    view = iso_view(-38, 24)
    sh.add(project(P, view, 760, 520, 1.45, explode=1.0, style="shade"))
    f = to2d(view, 760, 520, 1.45)
    callouts = [("1", "IR window", (0, 30, M.Z1), "IR window (glass + IR ink)"),
                ("2", "Front shell (PC/ABS)", (-100, 78, M.Z1), "Front shell"),
                ("3", "LED strobe boards (3x8 VSMA1094250)", (88, 10, 34), "LED strobe boards x3"),
                ("4", "Cameras (3x IMX900)", (0, 50, 40), "Cameras x3 + lenses + filters"),
                ("5", "Optical bench (6061-T651)", (100, -60, 27), "Optical bench"),
                ("6", "Main carrier PCB", (60, 40, 7), "Main carrier PCB"),
                ("7", "SoM + heat pipe + blower", (-20, 20, 0), "SoM, heat pipe, fins, blower"),
                ("8", "Battery pack (4S1P 81 Wh)", (40, -64, 0), "4S1P 81 Wh pack"),
                ("9", "Battery door", (40, M.Y0, 30), "Battery door"),
                ("10", "Rear shell (PC/ABS)", (60, 60, M.Z0), "Rear shell"),
                ("11", "TPE end caps", (M.X1+M.BUMP, 40, 20), "TPE end caps + radomes"),
                ("12", "Radar heads (2x SMR-333)", (109, 20, 22), "Radar heads x2"),
                ("13", "Display & buttons", (72, M.TOP, 0), "Display + buttons"),
                ("14", "Top crown + hidden grip", (-80, M.TOP, 0), "Top crown + hidden grip bar")]
    ex = {p["g"]: p["ex"] for p in P}
    for i, (num, g, pt, txt) in enumerate(callouts):
        e = ex.get(g, [0, 0, 0]); q = f((pt[0]+e[0], pt[1]+e[1], pt[2]+e[2]))
        tx_, ty_ = (1260 if q[0] > 760 else 250), 100 + i*62
        sh.add(f'<line x1="{q[0]:.1f}" y1="{q[1]:.1f}" x2="{tx_ + (0 if tx_ < 760 else 0)}" y2="{ty_}" stroke="{INK}" stroke-width="0.6"/>')
        sh.add(f'<circle cx="{tx_}" cy="{ty_}" r="13" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
        sh.add(f'<text x="{tx_}" y="{ty_+4}" font-size="12" font-weight="700" text-anchor="middle" font-family="-apple-system,Helvetica,Arial">{num}</text>')
        sh.add(label(tx_ + (18 if tx_ > 760 else -18), ty_+4, txt, 12, False, INK, "start" if tx_ > 760 else "end"))
    sh.add(label(90, 1000, "Assembly order: 5 → 4/3 (bench sub-assembly, calibrate) → 6+7 → 12 → 2 (bench 3-pt mount) → 1 → 10 → 14 → 13 → 11 → 8/9.", 12, False))
    return sh


def sheet_battery():
    sh = Sheet(1500, 760, "BATTERY PACK OB-BAT-4S81 · 4S1P 21700", "M-06", "scale 3:1 on screen")
    sh.add(MARK)
    b = M.BATT; k = 3.0; ox, oy = 120, 140
    w, d = (b["x1"]-b["x0"]), (b["z1"]-b["z0"])
    sh.add(label(ox, 110, "TOP VIEW (door removed)"))
    sh.add(f'<rect x="{ox}" y="{oy}" width="{w*k}" height="{d*k}" rx="10" fill="#eef2f8" stroke="{INK}" stroke-width="1.3"/>')
    for i in range(4):
        x = ox + (4 + i*21.2)*k
        sh.add(f'<rect x="{x}" y="{oy+4*k}" width="{21.1*k}" height="{70.2*k}" rx="{10*k}" fill="#dbe7f8" stroke="{INK}"/>')
        sh.add(f'<text x="{x+10.5*k}" y="{oy+40*k}" font-size="12" text-anchor="middle" font-family="ui-monospace,Menlo,monospace">B{i+1} M58T</text>')
    sh.add(f'<rect x="{ox+(w-1)*k}" y="{oy+(20-b["z0"]-0)*k/1.0 - 20*k}" width="{3*k}" height="{14*k}" fill="#fff" stroke="{INK}"/>')
    sh.add(dim(ox, oy+d*k, ox+w*k, oy+d*k, 24, f"{w:.0f}"))
    sh.add(dim(ox+w*k, oy, ox+w*k, oy+d*k, 30, f"{d:.0f}", horiz=False))
    sh.add(label(ox, oy+d*k+70, f"Pack height {b['y1']-b['y0']:.0f} mm · mass ≈ 300 g · 14.4 V nom / 16.8 V max · 5.65 Ah · 81 Wh (< 100 Wh carry-on)", 12, False))
    ex = 560
    lines = ["PACK ELECTRONICS (inside pack, own PCB 80 x 18 mm)", "• TI BQ40Z50-R2 fuel gauge + protector (CHG/DSG FETs, 2 mΩ sense)",
             "• TI BQ771807 independent 2nd-level OVP → chemical fuse", "• 2x NTC on cells, 1x on FETs", "• TE 787439-1 5-pos plug: PACK+, PACK−, SMBC, SMBD, PRES",
             "• SMBus to host charger/SoC; pack reports SoC %, health, temp", "", "CERTIFICATION", "• UN 38.3 (T1–T8), IEC 62133-2, ship at 30 % SoC (IATA 2026)",
             "• EU 2023/1542 Art. 11: user-removable without tools — met by the bottom door", "", "SECOND SOURCES", "• Molicel INR21700-P50B or Samsung 50S (72 Wh), same housing"]
    for i, t in enumerate(lines):
        sh.add(label(ex, 140 + i*22, t, 12, t.isupper() or t.startswith("PACK ELEC")))
    return sh


def all_sheets():
    P = M.build()
    return [sheet_general_arrangement(P), sheet_internal(P), sheet_bench(), sheet_pcbs(), sheet_exploded(P), sheet_battery()]


if __name__ == "__main__":
    s = all_sheets()
    open("/tmp/dwg_test.html", "w").write("<html><body style='background:#ddd'>" + "".join(x.svg() for x in s) + "</body></html>")
    print("ok", len(s))
