#!/usr/bin/env python3
"""Quebra os furos J1–J9 da v3 em um grupo por controle.

Não cria trilha. Cada controle vira um footprint próprio, com o mesmo
número de pino de pcb.md, para poder ser arrastado sozinho. O pino NC
sai. O primeiro furo de cada grupo fica quadrado.
"""

import math
import sys

import pcbnew

BOARD = "/workspace/voz-9/kicad-v3/voz-9.kicad_pcb"
PITCH = 3.96
EXTRA = 0.85
PAD = 2.5
DRILL = 1.6

# Rótulo e pinos, na ordem de pcb.md.
GROUPS = {
    "J1": [
        ("OSC A", "1 2"),
        ("OSC B", "3 4"),
        ("AMOUNT", "5 6 7"),
        ("SHAPE", "8 9 10"),
        ("CUTOFF", "11 12 13"),
        ("SW A", "14 15"),
        ("SW B", "16 17"),
        ("DRONE", "18 19"),
    ],
    "J3": [
        ("TIME", "1 2 3"),
        ("H1", "4 5"),
        ("H2", "6 7"),
        ("H3", "8 9"),
        ("F-BACK", "10 11 12"),
        ("WET", "13 14 15"),
        ("STACK", "16 17"),
        ("VOLUME", "18 19 20"),
    ],
    "J4": [
        ("A", "1 2 3"),
        ("B", "4 5 6"),
        ("IN", "7 8 9"),
        ("FILT", "10 11 12"),
        ("FCV", "13 14 15"),
        ("VCV", "16 17 18"),
    ],
    "J5": [
        ("LFO", "1 2 3"),
        ("ECV", "4 5 6"),
        ("CLK", "7 8 9"),
        ("SEND", "10 11 12"),
        ("RCV", "13 14 15"),
    ],
    "J2": [
        ("RATE", "1 2 3"),
        ("DEPTH", "4 5 6"),
        ("TREM", "7 8 9"),
        ("MODE", "10 11 12"),
    ],
    "J6": [
        ("LED", "1 2"),
        ("P4", "3 4"),
        ("GATE", "5 6"),
    ],
    "J7": [
        ("XLR IN", "1 2 3 4 5"),
        ("PRE", "6 7 8"),
        ("OSC IN", "9 10 11"),
    ],
    "J8": [
        ("XLR OUT", "1 2 3 4 5"),
    ],
    "J9": [
        ("LOW", "1 2 3"),
        ("MID F", "4 5 6"),
        ("MID G", "7 8 9"),
        ("HIGH", "10 11 12"),
    ],
}

HORIZONTAL = {"J1", "J3", "J4", "J5"}


def mm(value):
    return pcbnew.FromMM(value)


def to_mm(value):
    return pcbnew.ToMM(value)


def iu(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


def pins_of(spec):
    return spec.split()


def place(origin, along_x, groups):
    cursor = 0.0
    ox, oy = origin
    out = []
    for index, (label, spec) in enumerate(groups):
        numbers = pins_of(spec)
        pts = []
        for number in numbers:
            if along_x:
                pts.append((number, ox + cursor, oy))
            else:
                pts.append((number, ox, oy + cursor))
            cursor += PITCH
        if index != len(groups) - 1:
            cursor += EXTRA
        out.append((label, pts))
    return out


def end_of(groups):
    return groups[-1][1][-1]


def pth_layers():
    layers = pcbnew.LSET.AllCuMask()
    layers.AddLayer(pcbnew.F_Mask)
    layers.AddLayer(pcbnew.B_Mask)
    return layers


def add_group(board, ref, label, pts, nets):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(label)
    fp.SetAttributes(pcbnew.FP_THROUGH_HOLE)
    fp.SetExcludedFromBOM(True)
    fp.SetExcludedFromPosFiles(True)
    first = pts[0]
    fp.SetPosition(iu(first[1], first[2]))
    board.Add(fp)
    layers = pth_layers()
    for index, (number, x, y) in enumerate(pts):
        pad = pcbnew.PAD(fp)
        pad.SetNumber(number)
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetShape(pcbnew.PAD_SHAPE_RECT if index == 0 else pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetSize(iu(PAD, PAD))
        pad.SetDrillSize(iu(DRILL, DRILL))
        pad.SetLayerSet(layers)
        pad.SetPosition(iu(x, y))
        net = nets[number]
        if net is not None and net.GetNetCode() != 0:
            pad.SetNet(net)
        fp.Add(pad)
    xs = [x for _, x, y in pts]
    ys = [y for _, x, y in pts]
    value = fp.Value()
    value.SetVisible(True)
    value.SetLayer(pcbnew.F_SilkS)
    value.SetTextSize(iu(1.0, 1.0))
    value.SetTextThickness(mm(0.16))
    value.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
    value.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
    if ref in HORIZONTAL:
        # J1/J3 na borda: nome para fora. J4/J5: para o circuito.
        outward = ys[0] > 86
        value.SetPosition(iu(sum(xs) / len(xs), ys[0] + (2.45 if outward else -2.45)))
        value.SetTextAngle(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
    else:
        value.SetPosition(iu(xs[0] - 2.6, sum(ys) / len(ys)))
        value.SetTextAngle(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
    ref_text = fp.Reference()
    ref_text.SetVisible(False)
    return fp


def drop_old_names(board):
    for item in list(board.GetDrawings()):
        if item.GetClass() != "PCB_TEXT":
            continue
        if item.GetText() in GROUPS:
            board.Delete(item)


def layout(origins):
    placed = {}
    placed["J1"] = place(origins["J1"], True, GROUPS["J1"])
    j1_end = end_of(placed["J1"])[1]
    j3_x = origins["J3"][0]
    if j1_end + PAD + 0.4 > j3_x:
        j3_x = j1_end + 4.0
    placed["J3"] = place((j3_x, origins["J3"][1]), True, GROUPS["J3"])
    placed["J4"] = place(origins["J4"], True, GROUPS["J4"])
    j4_end = end_of(placed["J4"])[1]
    j5_x = origins["J5"][0]
    if j4_end + PAD + 0.4 > j5_x:
        j5_x = j4_end + 4.0
    placed["J5"] = place((j5_x, origins["J5"][1]), True, GROUPS["J5"])
    placed["J2"] = place(origins["J2"], False, GROUPS["J2"])
    placed["J7"] = place(origins["J7"], False, GROUPS["J7"])
    placed["J9"] = place(origins["J9"], False, GROUPS["J9"])
    j2_end = end_of(placed["J2"])[2]
    j6_y = origins["J6"][1]
    if j2_end + PAD + 0.4 > j6_y:
        j6_y = j2_end + 2.7
    placed["J6"] = place((origins["J6"][0], j6_y), False, GROUPS["J6"])
    placed["J8"] = place(origins["J8"], False, GROUPS["J8"])
    return placed


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else BOARD
    board = pcbnew.LoadBoard(path)
    by_ref = {}
    origins = {}
    nets = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref not in GROUPS:
            continue
        by_ref[ref] = fp
        pos = fp.GetPosition()
        origins[ref] = (to_mm(pos.x), to_mm(pos.y))
        nets[ref] = {pad.GetNumber(): pad.GetNet() for pad in fp.Pads()}
    missing = [ref for ref in GROUPS if ref not in by_ref]
    if missing:
        raise SystemExit(f"faltam conectores: {missing}")

    placed = layout(origins)
    points = [(ref, number, x, y) for ref, groups in placed.items() for _, pts in groups for number, x, y in pts]
    for ref, number, x, y in points:
        if not (5.5 <= x <= 194.5 and 5.5 <= y <= 96.5):
            raise SystemExit(f"{ref}.{number} fora da placa: {x:.2f},{y:.2f}")
    for i, a in enumerate(points):
        for b in points[i + 1 :]:
            if math.hypot(a[2] - b[2], a[3] - b[3]) < PAD + 0.2:
                raise SystemExit(f"furos perto demais: {a[0]}.{a[1]} e {b[0]}.{b[1]}")

    for ref, groups in placed.items():
        for label, pts in groups:
            add_group(board, ref, label, pts, nets[ref])
        board.Delete(by_ref[ref])
        count = sum(len(pts) for _, pts in groups)
        print(f"{ref} grupos={len(groups)} furos={count}")
    drop_old_names(board)
    block = board.GetTitleBlock()
    block.SetComment(1, "Furos agrupados por controle. Sem trilhas, para reposicionar.")
    board.Save(path)
    print("salvo", path)


if __name__ == "__main__":
    main()
