"""Schematic engine: netlist definition -> SVG sheets, ERC report, netlist export, ref-des BOM.

Components are declared with a symbol type and a pin list. Every pin carries a net name, and connectivity
is by net name (net-label schematic style, as used for SoM carrier boards). The renderer draws each IC as a
block with numbered pins and net labels, and each passive as a two-terminal symbol, grouped into
functional clusters on each sheet.
"""
from html import escape
from collections import defaultdict

INK = "#1b1c1e"; NETC = "#1d5fb4"; PWRC = "#b0281e"; GNDC = "#3b3b3b"; NCC = "#9aa0a6"


class Part:
    def __init__(self, ref, kind, value, mpn, mfr, fp, pins, sheet, cluster, note="", price=0.0, dnp=False):
        self.ref, self.kind, self.value, self.mpn, self.mfr, self.fp = ref, kind, value, mpn, mfr, fp
        self.pins = pins            # list of (pin_number, pin_name, net, side) side in {L,R}
        self.sheet, self.cluster, self.note, self.price, self.dnp = sheet, cluster, note, price, dnp


class Design:
    def __init__(self):
        self.parts = []
        self.sheets = []        # (id, title, description)
        self.blocks = {}        # sheet -> list of (cluster title, text)

    def sheet(self, sid, title, desc=""):
        self.sheets.append((sid, title, desc))

    def ic(self, ref, value, mpn, mfr, fp, sheet, cluster, left, right, note="", price=0.0):
        """left/right: list of (pin, name, net)."""
        pins = [(p, n, net, "L") for p, n, net in left] + [(p, n, net, "R") for p, n, net in right]
        self.parts.append(Part(ref, "ic", value, mpn, mfr, fp, pins, sheet, cluster, note, price))

    def two(self, kind, ref, value, n1, n2, sheet, cluster, mpn="", mfr="", fp="0402", price=0.0, note="", dnp=False):
        pins = [("1", "1", n1, "L"), ("2", "2", n2, "R")]
        if kind in ("D", "LED"):
            pins = [("1", "A", n1, "L"), ("2", "K", n2, "R")]
        self.parts.append(Part(ref, kind, value, mpn, mfr, fp, pins, sheet, cluster, note, price, dnp))

    def fet(self, ref, value, mpn, mfr, fp, d, g, s, sheet, cluster, price=0.0, ptype=False):
        pins = [("G", "G", g, "L"), ("D", "D", d, "R"), ("S", "S", s, "R")]
        self.parts.append(Part(ref, "PFET" if ptype else "NFET", value, mpn, mfr, fp, pins, sheet, cluster, "", price))

    # ------------------------------------------------------------ analysis
    BOARDS = {"CB": "Main carrier", "LB": "LED strobe board (x3)", "RH": "Radar head (x2)", "BP": "Battery pack BMS"}

    def nets(self, board=None):
        """Connectivity is per board: each PCBA has its own reference designators and nets.
        With board=None, keys are board-qualified ("CB/GND") so nets on different boards never merge."""
        n = defaultdict(list)
        for p in self.parts:
            b = p.sheet.split("-")[0]
            if board is not None and b != board:
                continue
            for pin, name, net, _ in p.pins:
                if net and net != "NC":
                    n[net if board else f"{b}/{net}"].append((p.ref, pin, name))
        return n

    def erc(self):
        issues = []
        drivers = {"3V3", "5V0", "3V8_SOM", "VSYS", "STROBE_BUS", "1V8_SOM"}
        for b in self.BOARDS:
            n = self.nets(b)
            for net, conns in sorted(n.items()):
                if len(conns) < 2 and not net.startswith("TP_") and not net.startswith("EXT_"):
                    issues.append((f"{b}: single-connection net", net, conns))
            for d in sorted(drivers):
                if d in n and len(n[d]) < 3:
                    issues.append((f"{b}: power net with < 3 loads", d, n[d]))
            seen = defaultdict(set)
            for p in self.parts:
                if p.sheet.split("-")[0] == b:
                    for pin, name, net, _ in p.pins:
                        if (p.ref, pin) in seen and net not in seen[(p.ref, pin)]:
                            issues.append((f"{b}: pin on two nets", f"{p.ref}.{pin}", sorted(seen[(p.ref, pin)] | {net})))
                        seen[(p.ref, pin)].add(net)
            refs = defaultdict(set)
            for p in self.parts:
                if p.sheet.split("-")[0] == b:
                    refs[p.ref].add(id(p))
            for r, ids in refs.items():
                if len(ids) > 1:
                    issues.append((f"{b}: duplicate reference", r, []))
        return issues

    def netlist_text(self, board=None):
        """One netlist per PCBA (refs are only unique within a board). board=None concatenates all four."""
        out = []
        for b, title in self.BOARDS.items():
            if board and b != board:
                continue
            out += [f"# ===== {b}: {title} · Outer Bounds Pro rev A", "# NET <name> : <ref>.<pin>(<pin name>) ..."]
            for net, conns in sorted(self.nets(b).items()):
                out.append(f"NET {net} : " + " ".join(f"{r}.{p}({nm})" for r, p, nm in conns))
            out.append("")
        return "\n".join(out)

    def bom_rows(self):
        """Group identical parts into BOM lines with reference designators."""
        g = defaultdict(list)
        seen = set()
        for p in self.parts:
            base = p.ref.split(".")[0]          # multi-unit symbols (U10.A, U10.B ...) are one physical part
            board = p.sheet.split("-")[0]
            if (board, base) in seen:
                continue
            seen.add((board, base))
            if "." in p.ref:
                p = next(q for q in self.parts if q.ref.split(".")[0] == base and q.sheet.split("-")[0] == board and q.price)
            pre = ''.join(c for c in base if c.isalpha())
            kind = p.kind if p.kind != "ic" else {"J": "Connector", "SW": "Switch", "BZ": "Buzzer", "Y": "Crystal", "B": "Cell", "F": "Fuse", "LED": "LED", "D": "Diode/TVS"}.get(pre, "IC")
            key = (board, kind, p.value, p.mpn, p.mfr, p.fp, p.dnp)
            g[key].append((base, p))
        rows = []
        for (board, kind, value, mpn, mfr, fp, dnp), pps in g.items():
            ps = [x[1] for x in pps]
            refs = sorted((x[0] for x in pps), key=lambda r: (''.join(c for c in r if c.isalpha()), int(''.join(c for c in r if c.isdigit()) or 0)))
            rows.append(dict(board=board, kind=kind, value=value, mpn=mpn, mfr=mfr, fp=fp, qty=len(ps), refs=refs, price=ps[0].price,
                             dnp=dnp, note=ps[0].note))
        return sorted(rows, key=lambda r: (r["board"], r["kind"] != "IC", r["refs"][0]))

    # ------------------------------------------------------------ rendering
    def render_sheet(self, sid, width=1600):
        parts = [p for p in self.parts if p.sheet == sid]
        title = next(t for s, t, _ in self.sheets if s == sid)
        clusters = []
        for p in parts:
            if p.cluster not in clusters:
                clusters.append(p.cluster)
        svgs, y = [], 70
        PINH = 18
        for cl in clusters:
            cps = [p for p in parts if p.cluster == cl]
            ics = [p for p in cps if p.kind == "ic"]
            twos = [p for p in cps if p.kind != "ic"]
            svgs.append(f'<text x="30" y="{y}" font-size="15" font-weight="700" font-family="-apple-system,Segoe UI,Helvetica,Arial" fill="{INK}">{escape(cl)}</text>')
            svgs.append(f'<line x1="30" y1="{y+6}" x2="{width-30}" y2="{y+6}" stroke="#d6d8db"/>')
            y += 44
            # ICs side by side
            x = 40; row_h = 0
            for ic in ics:
                L = [q for q in ic.pins if q[3] == "L"]; R = [q for q in ic.pins if q[3] == "R"]
                ml = max([len(q[1]) for q in L] + [0]); mr = max([len(q[1]) for q in R] + [0])
                bw = max(190, int(6.3*(ml + mr)) + 40); lab = 150
                if x + lab*2 + bw + 40 > width - 30:
                    x = 40; y += row_h + 30; row_h = 0
                n = max(len(L), len(R), 2); bh = n*PINH + 30
                bx = x + lab
                svgs.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" fill="#fffbea" stroke="{INK}" stroke-width="1.4"/>')
                svgs.append(_t(bx+bw/2, y-16, ic.ref, 13, 700, "middle"))
                svgs.append(_t(bx+bw/2, y-3, ic.value, 11, 400, "middle", "#444"))
                svgs.append(_t(bx+bw/2, y+bh+14, ic.mpn, 10, 400, "middle", "#666", mono=True))
                if ic.note:
                    ok = ic.note.startswith("✔")
                    svgs.append(_t(bx+bw/2, y+bh+27, ic.note, 9, 600, "middle", "#1e7a34" if ok else "#a15c00"))
                    bh += 12
                for i, (pin, name, net, _) in enumerate(L):
                    py = y + 22 + i*PINH
                    svgs.append(f'<line x1="{bx-26}" y1="{py}" x2="{bx}" y2="{py}" stroke="{INK}" stroke-width="1.1"/>')
                    svgs.append(_t(bx+5, py+4, name, 10.5, 400, "start"))
                    svgs.append(_t(bx-4, py-3, str(pin), 9, 400, "end", "#777", mono=True))
                    svgs.append(_net(bx-28, py, net, "end"))
                for i, (pin, name, net, _) in enumerate(R):
                    py = y + 22 + i*PINH
                    svgs.append(f'<line x1="{bx+bw}" y1="{py}" x2="{bx+bw+26}" y2="{py}" stroke="{INK}" stroke-width="1.1"/>')
                    svgs.append(_t(bx+bw-5, py+4, name, 10.5, 400, "end"))
                    svgs.append(_t(bx+bw+4, py-3, str(pin), 9, 400, "start", "#777", mono=True))
                    svgs.append(_net(bx+bw+28, py, net, "start"))
                x += lab*2 + bw + 30
                row_h = max(row_h, bh + 20)
            if ics:
                y += row_h + 26
            # passives grid
            if twos:
                colw = 300; cols = max(1, (width - 60)//colw); i = 0
                for p in twos:
                    cx = 40 + (i % cols)*colw; cy = y + (i//cols)*46
                    svgs.append(_two(cx, cy, p))
                    i += 1
                y += ((len(twos)-1)//cols + 1)*46 + 10
            y += 20
        height = y + 90
        head = (f'<svg class="sch" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(title)}">'
                f'<rect x="1" y="1" width="{width-2}" height="{height-2}" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
                f'<text x="30" y="38" font-size="19" font-weight="800" font-family="-apple-system,Segoe UI,Helvetica,Arial" fill="{INK}">{escape(sid)} · {escape(title)}</text>'
                f'<rect x="{width-600}" y="{height-58}" width="590" height="48" fill="#fff" stroke="{INK}"/>'
                f'<text x="{width-590}" y="{height-38}" font-size="11" font-family="ui-monospace,Menlo,monospace" font-weight="700">OUTER BOUNDS PRO · SCHEMATIC {escape(sid)}</text>'
                f'<text x="{width-590}" y="{height-20}" font-size="11" font-family="ui-monospace,Menlo,monospace">Rev A · 2026-10-07 · net-label connectivity · DNP = do not populate</text>')
        return head + "".join(svgs) + "</svg>"


def _t(x, y, s, fs, fw, anchor, col=INK, mono=False):
    fam = "ui-monospace,Menlo,monospace" if mono else "-apple-system,Segoe UI,Helvetica,Arial"
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="{fw}" text-anchor="{anchor}" font-family="{fam}" fill="{col}">{escape(str(s))}</text>'


def _netcol(net):
    if net in ("GND", "PGND", "AGND", "SGND"):
        return GNDC
    if net == "NC":
        return NCC
    if net.isupper() and any(net.startswith(p) for p in ("VSYS", "VBUS", "VBAT", "3V3", "5V0", "3V8", "1V8", "STROBE_BUS", "VBUS_", "PACK", "VREG", "REGN", "VDDA", "AVDD", "DVDD", "VIN_", "VPH")):
        return PWRC
    return NETC


def _net(x, y, net, anchor):
    if net == "NC":
        return (f'<g stroke="{NCC}" stroke-width="1.2"><line x1="{x-4 if anchor=="end" else x}" y1="{y-4}" x2="{x+4 if anchor=="start" else x+0}" y2="{y+4}"/>'
                f'<line x1="{x-4 if anchor=="end" else x}" y1="{y+4}" x2="{x+4 if anchor=="start" else x}" y2="{y-4}"/></g>')
    col = _netcol(net)
    w = 6.4*len(net) + 10
    x0 = x - w if anchor == "end" else x
    return (f'<g><rect x="{x0:.1f}" y="{y-7}" width="{w:.1f}" height="14" rx="3" fill="#fff" stroke="{col}" stroke-width="0.8"/>'
            f'<text x="{x0+w/2:.1f}" y="{y+3.6:.1f}" font-size="9.5" text-anchor="middle" font-family="ui-monospace,Menlo,monospace" fill="{col}">{escape(net)}</text></g>')


def _two(x, y, p):
    n1, n2 = p.pins[0][2], p.pins[1][2] if len(p.pins) > 1 else ""
    sym_x = x + 92; out = []
    out.append(_net(sym_x-6, y+12, n1, "end"))
    k = p.kind
    s = sym_x
    if k == "R":
        out.append(f'<line x1="{s-6}" y1="{y+12}" x2="{s+4}" y2="{y+12}" stroke="{INK}"/><rect x="{s+4}" y="{y+7}" width="28" height="10" fill="#fff" stroke="{INK}" stroke-width="1.2"/><line x1="{s+32}" y1="{y+12}" x2="{s+42}" y2="{y+12}" stroke="{INK}"/>')
    elif k == "C":
        out.append(f'<line x1="{s-6}" y1="{y+12}" x2="{s+15}" y2="{y+12}" stroke="{INK}"/><line x1="{s+15}" y1="{y+3}" x2="{s+15}" y2="{y+21}" stroke="{INK}" stroke-width="2"/>'
                   f'<line x1="{s+21}" y1="{y+3}" x2="{s+21}" y2="{y+21}" stroke="{INK}" stroke-width="2"/><line x1="{s+21}" y1="{y+12}" x2="{s+42}" y2="{y+12}" stroke="{INK}"/>')
    elif k == "L":
        arcs = "".join(f'<path d="M{s+4+i*8} {y+12} a4 4 0 0 1 8 0" fill="none" stroke="{INK}" stroke-width="1.3"/>' for i in range(4))
        out.append(f'<line x1="{s-6}" y1="{y+12}" x2="{s+4}" y2="{y+12}" stroke="{INK}"/>{arcs}<line x1="{s+36}" y1="{y+12}" x2="{s+42}" y2="{y+12}" stroke="{INK}"/>')
    elif k in ("D", "LED", "TVS"):
        out.append(f'<line x1="{s-6}" y1="{y+12}" x2="{s+10}" y2="{y+12}" stroke="{INK}"/><path d="M{s+10} {y+4} L{s+26} {y+12} L{s+10} {y+20} Z" fill="{"#fff" if k!="LED" else "#ffe9c2"}" stroke="{INK}"/>'
                   f'<line x1="{s+26}" y1="{y+4}" x2="{s+26}" y2="{y+20}" stroke="{INK}" stroke-width="1.6"/><line x1="{s+26}" y1="{y+12}" x2="{s+42}" y2="{y+12}" stroke="{INK}"/>')
        if k == "LED":
            out.append(f'<path d="M{s+18} {y+2} l6 -6 M{s+23} {y+4} l6 -6" stroke="#c0392b" stroke-width="1"/>')
    elif k in ("NFET", "PFET"):
        g, d, src = p.pins[0][2], p.pins[1][2], p.pins[2][2]
        out = [_net(s-6, y+20, g, "end"),
               f'<line x1="{s-6}" y1="{y+20}" x2="{s+10}" y2="{y+20}" stroke="{INK}"/><line x1="{s+10}" y1="{y+8}" x2="{s+10}" y2="{y+32}" stroke="{INK}" stroke-width="1.6"/>'
               f'<line x1="{s+15}" y1="{y+6}" x2="{s+15}" y2="{y+34}" stroke="{INK}" stroke-width="2"/><line x1="{s+15}" y1="{y+10}" x2="{s+34}" y2="{y+10}" stroke="{INK}"/>'
               f'<line x1="{s+15}" y1="{y+30}" x2="{s+34}" y2="{y+30}" stroke="{INK}"/><circle cx="{s+20}" cy="{y+20}" r="13" fill="none" stroke="{INK}" stroke-width="0.8"/>',
               _t(s+37, y+8, "D", 8, 400, "start", "#777"), _net(s+46, y+10, d, "start"), _t(s+37, y+38, "S", 8, 400, "start", "#777"), _net(s+46, y+30, src, "start")]
        out.append(_t(s+20, y+48, f"{p.ref} {p.value}", 10, 700, "middle"))
        return "".join(out)
    elif k == "Y":
        out.append(f'<line x1="{s-6}" y1="{y+12}" x2="{s+12}" y2="{y+12}" stroke="{INK}"/><line x1="{s+12}" y1="{y+4}" x2="{s+12}" y2="{y+20}" stroke="{INK}" stroke-width="1.6"/>'
                   f'<rect x="{s+16}" y="{y+5}" width="10" height="14" fill="#fff" stroke="{INK}"/><line x1="{s+30}" y1="{y+4}" x2="{s+30}" y2="{y+20}" stroke="{INK}" stroke-width="1.6"/><line x1="{s+30}" y1="{y+12}" x2="{s+42}" y2="{y+12}" stroke="{INK}"/>')
    elif k == "FB":
        out.append(f'<line x1="{s-6}" y1="{y+12}" x2="{s+6}" y2="{y+12}" stroke="{INK}"/><rect x="{s+6}" y="{y+6}" width="26" height="12" fill="#444" stroke="{INK}"/><line x1="{s+32}" y1="{y+12}" x2="{s+42}" y2="{y+12}" stroke="{INK}"/>')
    else:   # generic 2-pin (fuse, jumper, test point)
        out.append(f'<line x1="{s-6}" y1="{y+12}" x2="{s+42}" y2="{y+12}" stroke="{INK}"/><rect x="{s+6}" y="{y+7}" width="24" height="10" rx="5" fill="#fff" stroke="{INK}"/>')
    out.append(_net(s+48, y+12, n2, "start"))
    lab = f"{p.ref} {p.value}" + (" DNP" if p.dnp else "")
    out.append(_t(s+18, y+34, lab, 9.5, 700, "middle", "#c0392b" if p.dnp else INK))
    if p.fp:
        out.append(_t(s+18, y+43, p.fp, 8, 400, "middle", "#888", mono=True))
    return "".join(out)
