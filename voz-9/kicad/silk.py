#!/usr/bin/env python3
"""Afasta a seda do cobre e engrossa o traço fino.

O JLCDFM marca seda a menos de 0,15 mm do pad ou do furo, e traço de
0,15 mm. A máscara desta placa abre rente ao pad (folga 0) e as vias
vão tampadas, então o recorte da máscara não tira a tinta de cima da
via. Este passo corta o contorno e empurra o texto até a tinta ficar
a pelo menos 0,20 mm do cobre. Não mexe em trilha, via ou pad.
"""

import math

import pcbnew

CLEAR = 0.20
MIN_THICK = 0.16
MIN_PIECE = 0.12
CELL = 8.0


def mm(value):
    return pcbnew.FromMM(value)


def to_mm(value):
    return pcbnew.ToMM(value)


def _dist_point_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    length2 = dx * dx + dy * dy
    if length2 < 1e-18:
        return math.hypot(px - ax, py - ay), 0.0
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy)), t


def _dist_aabb(px, py, cx, cy, hx, hy):
    dx = max(abs(px - cx) - hx, 0.0)
    dy = max(abs(py - cy) - hy, 0.0)
    return math.hypot(dx, dy)


def _circle_cut(ax, ay, bx, by, cx, cy, radius):
    """Trecho do segmento (t em 0..1) que entra no disco."""
    dx, dy = bx - ax, by - ay
    fx, fy = ax - cx, ay - cy
    a = dx * dx + dy * dy
    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - radius * radius
    if a < 1e-12:
        if c <= 0:
            return (0.0, 1.0)
        return None
    disc = b * b - 4.0 * a * c
    if disc < 0:
        return None
    root = math.sqrt(disc)
    t1 = (-b - root) / (2.0 * a)
    t2 = (-b + root) / (2.0 * a)
    lo, hi = max(0.0, min(t1, t2)), min(1.0, max(t1, t2))
    if hi - lo < 1e-6:
        return None
    return (lo, hi)


def _rect_cut(ax, ay, bx, by, cx, cy, hx, hy, margin):
    length = math.hypot(bx - ax, by - ay)
    steps = max(2, int(math.ceil(length / 0.04)))
    inside = []
    for i in range(steps + 1):
        t = i / steps
        px = ax + (bx - ax) * t
        py = ay + (by - ay) * t
        inside.append(_dist_aabb(px, py, cx, cy, hx, hy) < margin)
    if not any(inside):
        return []
    cuts = []
    start = None
    for i, flag in enumerate(inside):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            cuts.append((max(0.0, (start - 1) / steps), min(1.0, i / steps)))
            start = None
    if start is not None:
        cuts.append((max(0.0, (start - 1) / steps), 1.0))
    return [(lo, hi) for lo, hi in cuts if hi - lo > 1e-6]


def _subtract(cuts):
    pieces = [(0.0, 1.0)]
    for lo, hi in cuts:
        nxt = []
        for a, b in pieces:
            if hi <= a or lo >= b:
                nxt.append((a, b))
                continue
            if a < lo - 1e-9:
                nxt.append((a, min(b, lo)))
            if b > hi + 1e-9:
                nxt.append((max(a, hi), b))
        pieces = [(a, b) for a, b in nxt if b - a > 1e-6]
    return pieces


class Keepout:
    """Cobre de pad e de via, e furo sem cobre (M3)."""

    def __init__(self, board):
        self.circles = []
        self.rects = []
        self._grid = {}
        for fp in board.GetFootprints():
            for pad in fp.Pads():
                pos = pad.GetPosition()
                x, y = to_mm(pos.x), to_mm(pos.y)
                attr = int(pad.GetAttribute())
                shape = int(pad.GetShape())
                hx = to_mm(pad.GetSizeX()) / 2
                hy = to_mm(pad.GetSizeY()) / 2
                drill = max(to_mm(pad.GetDrillSizeX()), to_mm(pad.GetDrillSizeY())) / 2
                if attr == int(pcbnew.PAD_ATTRIB_NPTH):
                    if drill > 0:
                        self._add_circle(x, y, drill)
                    continue
                if shape == int(pcbnew.PAD_SHAPE_CIRCLE):
                    self._add_circle(x, y, max(hx, hy))
                else:
                    self._add_rect(x, y, hx, hy)
                if drill > max(hx, hy):
                    self._add_circle(x, y, drill)
        for item in board.GetTracks():
            if item.GetClass() != "PCB_VIA":
                continue
            pos = item.GetPosition()
            self._add_circle(
                to_mm(pos.x),
                to_mm(pos.y),
                to_mm(item.GetWidth(pcbnew.F_Cu)) / 2,
            )

    def _add_circle(self, x, y, radius):
        self.circles.append((x, y, radius))
        self._index(len(self.circles) - 1, "c", x, y, radius)

    def _add_rect(self, x, y, hx, hy):
        self.rects.append((x, y, hx, hy))
        self._index(len(self.rects) - 1, "r", x, y, math.hypot(hx, hy))

    def _index(self, idx, kind, x, y, radius):
        reach = int(math.ceil((radius + 2.0) / CELL)) + 1
        cx, cy = int(x // CELL), int(y // CELL)
        for ix in range(cx - reach, cx + reach + 1):
            for iy in range(cy - reach, cy + reach + 1):
                self._grid.setdefault((ix, iy), []).append((kind, idx))

    def near(self, ax, ay, bx, by):
        pad = 2.0
        found = []
        seen = set()
        x0, x1 = min(ax, bx) - pad, max(ax, bx) + pad
        y0, y1 = min(ay, by) - pad, max(ay, by) + pad
        for ix in range(int(x0 // CELL), int(x1 // CELL) + 1):
            for iy in range(int(y0 // CELL), int(y1 // CELL) + 1):
                for item in self._grid.get((ix, iy), ()):
                    if item not in seen:
                        seen.add(item)
                        found.append(item)
        return found

    def cuts(self, ax, ay, bx, by, width):
        margin = CLEAR + width / 2
        cuts = []
        for kind, idx in self.near(ax, ay, bx, by):
            if kind == "c":
                cx, cy, radius = self.circles[idx]
                hit = _circle_cut(ax, ay, bx, by, cx, cy, radius + margin)
                if hit:
                    cuts.append(hit)
            else:
                cx, cy, hx, hy = self.rects[idx]
                cuts.extend(_rect_cut(ax, ay, bx, by, cx, cy, hx, hy, margin))
        if cuts and self.gap_segment(ax, ay, bx, by, width) >= CLEAR - 0.005:
            return []
        return cuts

    def gap_segment(self, ax, ay, bx, by, width):
        worst = 99.0
        for kind, idx in self.near(ax, ay, bx, by):
            if kind == "c":
                cx, cy, radius = self.circles[idx]
                dist, _t = _dist_point_seg(cx, cy, ax, ay, bx, by)
                gap = dist - radius - width / 2
            else:
                cx, cy, hx, hy = self.rects[idx]
                length = math.hypot(bx - ax, by - ay)
                steps = max(2, int(math.ceil(length / 0.1)))
                gap = 99.0
                for i in range(steps + 1):
                    t = i / steps
                    px = ax + (bx - ax) * t
                    py = ay + (by - ay) * t
                    gap = min(gap, _dist_aabb(px, py, cx, cy, hx, hy) - width / 2)
            if gap < worst:
                worst = gap
        return worst


def _pieces(ax, ay, bx, by, width, keepout):
    length = math.hypot(bx - ax, by - ay)
    if length < 1e-6:
        return []
    spans = _subtract(keepout.cuts(ax, ay, bx, by, width))
    out = []
    for lo, hi in spans:
        if (hi - lo) * length < MIN_PIECE:
            continue
        out.append(
            (
                ax + (bx - ax) * lo,
                ay + (by - ay) * lo,
                ax + (bx - ax) * hi,
                ay + (by - ay) * hi,
            )
        )
    return out


def _point(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


def _xy(pt):
    # Copia na hora: o próximo GetStart/GetEnd reaproveita o objeto.
    return to_mm(pt.x), to_mm(pt.y)


def _ends(item):
    ax, ay = _xy(item.GetStart())
    bx, by = _xy(item.GetEnd())
    return ax, ay, bx, by


def _add_segment(parent, layer, width, piece):
    seg = pcbnew.PCB_SHAPE(parent)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetLayer(layer)
    seg.SetWidth(width)
    seg.SetStart(_point(piece[0], piece[1]))
    seg.SetEnd(_point(piece[2], piece[3]))
    parent.Add(seg)


def _write_pieces(item, pieces):
    parent = item.GetParent()
    layer = item.GetLayer()
    width = item.GetWidth()
    if not pieces:
        parent.Remove(item)
        return
    ax, ay, bx, by = pieces[0]
    item.SetShape(pcbnew.SHAPE_T_SEGMENT)
    item.SetStart(_point(ax, ay))
    item.SetEnd(_point(bx, by))
    for piece in pieces[1:]:
        _add_segment(parent, layer, width, piece)


def _poly_points(item):
    shape = int(item.GetShape())
    if shape == int(pcbnew.SHAPE_T_SEGMENT):
        ax, ay, bx, by = _ends(item)
        return [(ax, ay), (bx, by)]
    if shape == int(pcbnew.SHAPE_T_RECT):
        x1, y1, x2, y2 = _ends(item)
        return [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]
    if shape == int(pcbnew.SHAPE_T_CIRCLE):
        cx, cy = _xy(item.GetCenter())
        radius = to_mm(item.GetRadius())
        step = 0.45
        count = max(16, int(math.ceil(2 * math.pi * radius / step)))
        pts = []
        for i in range(count):
            ang = 2 * math.pi * i / count
            pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
        pts.append(pts[0])
        return pts
    if shape == int(pcbnew.SHAPE_T_ARC):
        cx, cy = _xy(item.GetCenter())
        sx, sy = _xy(item.GetStart())
        radius = math.hypot(sx - cx, sy - cy)
        a0 = math.atan2(sy - cy, sx - cx)
        sweep = item.GetArcAngle().AsRadians()
        length = abs(radius * sweep)
        count = max(2, int(math.ceil(length / 0.45)))
        pts = []
        for i in range(count + 1):
            ang = a0 + sweep * i / count
            pts.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))
        return pts
    return []


def _shape_needs_cut(item, keepout):
    pts = _poly_points(item)
    width = to_mm(item.GetWidth())
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        if keepout.cuts(ax, ay, bx, by, width):
            return True
    return False


def _clip_shapes(board, keepout):
    # Lê tudo antes de gravar. Remover um item invalida o GetStart dos outros.
    jobs = []
    for fp in board.GetFootprints():
        for item in fp.GraphicalItems():
            if item.GetClass() != "PCB_SHAPE":
                continue
            if item.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS):
                continue
            shape = int(item.GetShape())
            width = to_mm(item.GetWidth())
            if shape == int(pcbnew.SHAPE_T_SEGMENT):
                ax, ay, bx, by = _ends(item)
                if not keepout.cuts(ax, ay, bx, by, width):
                    continue
                jobs.append((item, _pieces(ax, ay, bx, by, width, keepout)))
                continue
            if shape not in (
                int(pcbnew.SHAPE_T_RECT),
                int(pcbnew.SHAPE_T_CIRCLE),
                int(pcbnew.SHAPE_T_ARC),
            ):
                continue
            pts = _poly_points(item)
            if not _shape_needs_cut(item, keepout):
                continue
            pieces = []
            for i in range(len(pts) - 1):
                pieces.extend(
                    _pieces(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], width, keepout)
                )
            jobs.append((item, pieces))
    for item, pieces in jobs:
        _write_pieces(item, pieces)
    return len(jobs)


def _thicken_text(item):
    if item.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS) or not item.IsVisible():
        return False
    height = to_mm(item.GetTextHeight())
    if height < 1.0:
        item.SetTextSize(pcbnew.VECTOR2I(mm(1.0), mm(1.0)))
        height = 1.0
    thick = max(height / 6.0, MIN_THICK)
    if to_mm(item.GetTextThickness()) < thick - 1e-4:
        item.SetTextThickness(mm(thick))
        return True
    return False


def _silk_texts(board):
    found = []
    for fp in board.GetFootprints():
        for item in (fp.Reference(), fp.Value()):
            if item.IsVisible() and item.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS):
                found.append((fp.GetReference(), item))
        for item in fp.GraphicalItems():
            if item.GetClass() == "PCB_TEXT":
                found.append((fp.GetReference(), item))
    for item in board.GetDrawings():
        if item.GetClass() == "PCB_TEXT":
            found.append(("placa", item))
    return found


def _stroke(sub):
    seg = pcbnew.Cast_to_SHAPE_SEGMENT(sub)
    ax, ay = _xy(seg.GetStart())
    bx, by = _xy(seg.GetEnd())
    return ax, ay, bx, by, to_mm(seg.GetWidth())


def _text_gap(item, keepout):
    """Folga da tinta até o cobre. None se o texto está longe de tudo."""
    box = item.GetBoundingBox()
    x1, y1 = to_mm(box.GetLeft()), to_mm(box.GetTop())
    x2, y2 = to_mm(box.GetRight()), to_mm(box.GetBottom())
    near = keepout.near(x1, y1, x2, y2)
    if not near:
        return None, None
    shape = item.GetEffectiveTextShape()
    subs = shape.GetSubshapes()
    strokes = [_stroke(subs[i]) for i in range(shape.Size())]
    worst = 99.0
    where = None
    for kind, idx in near:
        if kind == "c":
            cx, cy, radius = keepout.circles[idx]
            reach = radius
        else:
            cx, cy, hx, hy = keepout.rects[idx]
            reach = max(hx, hy)
        if cx < x1 - reach - CLEAR or cx > x2 + reach + CLEAR:
            continue
        if cy < y1 - reach - CLEAR or cy > y2 + reach + CLEAR:
            continue
        for ax, ay, bx, by, width in strokes:
            if kind == "c":
                dist, _t = _dist_point_seg(cx, cy, ax, ay, bx, by)
                gap = dist - radius - width / 2
            else:
                length = math.hypot(bx - ax, by - ay)
                steps = max(1, int(math.ceil(length / 0.05)))
                gap = 99.0
                for i in range(steps + 1):
                    t = i / steps
                    px = ax + (bx - ax) * t
                    py = ay + (by - ay) * t
                    gap = min(gap, _dist_aabb(px, py, cx, cy, hx, hy) - width / 2)
            if gap < worst:
                worst = gap
                where = (cx, cy)
            if worst <= 0:
                return worst, where
    return worst, where


def _move_texts(board, keepout):
    moved = []
    for name, item in _silk_texts(board):
        if item.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS) or not item.IsVisible():
            continue
        origin = item.GetPosition()
        ox, oy = to_mm(origin.x), to_mm(origin.y)
        shifted = False
        for _step in range(14):
            gap, where = _text_gap(item, keepout)
            if gap is None or gap >= CLEAR - 0.01:
                break
            pos = item.GetPosition()
            tx, ty = to_mm(pos.x), to_mm(pos.y)
            dx, dy = tx - where[0], ty - where[1]
            norm = math.hypot(dx, dy)
            if norm < 0.05:
                dx, dy, norm = 0.0, -1.0, 1.0
            step = min(1.2, max(0.2, CLEAR - gap + 0.1))
            if math.hypot(tx + dx / norm * step - ox, ty + dy / norm * step - oy) > 6.0:
                break
            item.SetPosition(
                _point(
                    min(298.0, max(2.0, tx + dx / norm * step)),
                    min(138.0, max(2.0, ty + dy / norm * step)),
                )
            )
            shifted = True
        if shifted:
            pos = item.GetPosition()
            moved.append(
                (
                    name,
                    item.GetText(),
                    round(to_mm(pos.x) - ox, 2),
                    round(to_mm(pos.y) - oy, 2),
                )
            )
    return moved


def _thicken_all(board):
    count = 0
    for _name, item in _silk_texts(board):
        if _thicken_text(item):
            count += 1
    return count


def prepare(board):
    """Engrossa o 'K' dos diodos e afasta a seda do cobre."""
    thick = _thicken_all(board)
    keepout = Keepout(board)
    moved = _move_texts(board, keepout)
    clipped = _clip_shapes(board, keepout)
    print(f"seda  traço={thick}  texto={len(moved)}  contorno={clipped}")
    for name, text, dx, dy in moved:
        print(f"  {name} {text!r}  dx={dx} dy={dy}")
    return thick, moved, clipped


def check(board):
    """Lista a seda que ainda ficaria no aviso do JLCDFM."""
    errors = []
    for name, item in _silk_texts(board):
        if item.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS) or not item.IsVisible():
            continue
        thick = to_mm(item.GetTextThickness())
        height = to_mm(item.GetTextHeight())
        if height < 1.0 - 1e-3 or thick < MIN_THICK - 1e-3:
            errors.append(f"seda {name} {item.GetText()!r} traço {thick:.3f} mm")
    keepout = Keepout(board)
    for name, item in _silk_texts(board):
        if item.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS) or not item.IsVisible():
            continue
        gap, _where = _text_gap(item, keepout)
        if gap is not None and gap < 0.15:
            errors.append(f"seda {name} {item.GetText()!r} a {gap:.3f} mm do cobre")
    close = 0
    for fp in board.GetFootprints():
        for item in fp.GraphicalItems():
            if item.GetClass() != "PCB_SHAPE":
                continue
            if item.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS):
                continue
            width = to_mm(item.GetWidth())
            if width < MIN_THICK - 1e-3:
                errors.append(f"seda {fp.GetReference()} traço {width:.3f} mm")
            pts = _poly_points(item)
            for i in range(len(pts) - 1):
                gap = keepout.gap_segment(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], width)
                if gap < 0.15:
                    close += 1
                    if close <= 8:
                        errors.append(
                            f"seda {fp.GetReference()} contorno a {gap:.3f} mm do cobre"
                        )
                    break
    if close > 8:
        errors.append(f"seda: mais {close - 8} contornos a menos de 0,15 mm do cobre")
    return errors
