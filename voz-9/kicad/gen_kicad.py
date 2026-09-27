#!/usr/bin/env python3
"""Gera o projeto KiCad da BASE VOZ-9 (placa 300×140 mm).

Cada bloco fica junto do conector que o alimenta de fio, na ordem do sinal.
A fonte, o pré e o mix ocupam a faixa de cima. O miolo (MOD, NAB, fita)
fica no meio. J1–J9 são pinos macho 1×N na borda de baixo.
O esquema agrupa os mesmos blocos, ainda sem fios.
As trilhas não nascem aqui: `route.py` grava as nets e o cobre.
Rodar este gerador de novo apaga o roteamento.
"""

import json
import math
import os
import re
import uuid

import pcbnew

ROOT = os.path.dirname(os.path.abspath(__file__))
SYM = "/usr/share/kicad/symbols"
FP = "/usr/share/kicad/footprints"
DEMO_PRO = "/usr/share/kicad/demos/pic_programmer/pic_programmer.kicad_pro"

W, H = 300.0, 140.0
# A folha cobre os 300 mm de largura e deixa o carimbo fora do cobre.
PAGE_W, PAGE_H = 420.0, 200.0

FP_R = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal"
FP_C = "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm"
FP_CE = "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm"
FP_D = "Diode_THT:D_DO-41_SOD81_P7.62mm_Horizontal"
FP_DIP8 = "Package_DIP:DIP-8_W7.62mm_Socket"
FP_DIP16 = "Package_DIP:DIP-16_W7.62mm_Socket"
FP_TO92 = "Package_TO_SOT_THT:TO-92"
FP_TO220 = "Package_TO_SOT_THT:TO-220-3_Vertical"
FP_TRIM = "Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical"
FP_HOLE = "MountingHole:MountingHole_3.2mm_M3"

SYM_OP = "Amplifier_Operational:LM2904"
SYM_REG = "Regulator_Linear:LM7805_TO220"
SYM_7660 = "Regulator_SwitchedCapacitor:MAX1044"
SYM_PT = "Audio:PT2399"
SYM_JFET = "Device:Q_NJFET_DGS"

SHEET_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, "voz-9-sheet"))

parts = []
notes = []
block = ""


def uid(*bits):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "voz-9:" + ":".join(bits)))


def add(ref, val, sym, fp, x, y, bom=True, rot=0):
    parts.append(
        {
            "ref": ref,
            "val": val,
            "sym": sym,
            "fp": fp,
            "x": x,
            "y": y,
            "rot": rot,
            "block": block,
            "bom": bom,
        }
    )


def R(ref, val, x, y):
    add(ref, val, "Device:R", FP_R, 0, 0)


def C(ref, val, x, y):
    add(ref, val, "Device:C", FP_C, 0, 0)


def CE(ref, val, x, y):
    add(ref, val, "Device:C_Polarized", FP_CE, 0, 0)


def D(ref, val, x, y):
    add(ref, val, "Device:D", FP_D, 0, 0)


def Q(ref, val, x, y):
    add(ref, val, SYM_JFET, FP_TO92, 0, 0)


def DIP8(ref, val, sym, x, y):
    add(ref, val, sym, FP_DIP8, 0, 0)


def DIP16(ref, val, sym, x, y):
    add(ref, val, sym, FP_DIP16, 0, 0)


def HDR(ref, cols, x, y, name):
    n = cols * 2
    add(
        ref,
        name,
        f"Connector_Generic:Conn_01x{n:02d}",
        f"Connector_PinHeader_2.54mm:PinHeader_1x{n:02d}_P2.54mm_Vertical",
        0,
        0,
        rot=90,
    )


def rline(x0, y, items, dx=10.2):
    for i, (ref, val) in enumerate(items):
        R(ref, val, x0 + i * dx, y)


def cline(x0, y, items, dx=8.3):
    for i, (ref, val) in enumerate(items):
        C(ref, val, x0 + i * dx, y)


def eline(x0, y, items, dx=9.4):
    for i, (ref, val) in enumerate(items):
        CE(ref, val, x0 + i * dx, y)


def build_parts():
    global block
    block = "CHICOTES"
    HDR("J1", 10, 12, 16, "OSC")
    HDR("J2", 6, 12, 38, "LFO")
    HDR("J3", 10, 12, 58, "DELAY")
    HDR("J4", 10, 12, 80, "PATCH A")
    HDR("J5", 8, 12, 102, "PATCH B")
    HDR("J6", 3, 10, 126, "CTRL")
    HDR("J7", 6, 22, 126, "IN+PRE")
    HDR("J8", 3, 42, 126, "OUT")
    HDR("J9", 6, 12, 142, "EQ424")

    block = "FONTE"
    D("D1", "1N5817", 64, 21)
    DIP8("U4", "MAX1044", SYM_7660, 80, 22)
    add("U5", "78M05", SYM_REG, FP_TO220, 0, 0)
    CE("C56", "10µ", 114, 20)
    CE("C57", "10µ", 114, 29)
    CE("C58", "10µ", 114, 38)
    rline(64, 35, [("R14", "4k7"), ("R17", "4k7"), ("R19", "10k"), ("R20", "10k")], dx=11.2)
    R("R18", "5k6", 64, 41.5)
    R("R55", "22k", 75.2, 41.5)
    C("C22", "100n", 90, 41.5)
    eline(64, 51, [("C64", "47µ"), ("C65", "47µ"), ("C66", "47µ"), ("C67", "47µ")], dx=12)

    block = "U1"
    DIP8("U1", "NE5532", SYM_OP, 130, 22)
    rline(144, 16, [("R12", "2k2"), ("R13", "2k2"), ("R57", "22k")])
    rline(144, 22.4, [("R58", "22k"), ("R6", "1k"), ("R42", "10k")])
    rline(144, 28.8, [("R1", "220"), ("R2", "220"), ("R44", "10k")])
    cline(128, 36, [("C1", "100p"), ("C2", "100p"), ("C23", "100n"), ("C24", "100n"), ("C25", "100n")])
    eline(128, 45, [("C59", "10µ"), ("C60", "10µ"), ("C61", "10µ"), ("C62", "10µ"), ("C63", "10µ")])
    DIP8("U9", "TL072", SYM_OP, 156, 45)

    block = "U2"
    DIP8("U2", "TL072", SYM_OP, 186, 21)
    R("R21", "10k", 200, 16)
    R("R22", "10k", 200, 22.4)
    R("R62", "100k", 200, 28.8)
    R("R63", "100k", 200, 35.2)
    R("R72", "220k", 186, 35.2)
    C("C21", "100n", 186, 42)
    C("C6", "10n", 200, 42)
    C("C19", "100n", 186, 47.2)

    block = "MIX"
    Q("Q1", "J201", 64, 65)
    Q("Q2", "J201", 76, 65)
    Q("Q3", "J201", 88, 65)
    Q("Q6", "J201", 100, 65)
    D("D6", "MP20", 112, 65)
    rline(64, 73, [("R23", "10k"), ("R24", "10k"), ("R25", "10k"), ("R3", "1k"), ("R64", "100k"), ("R80", "1M")])
    rline(64, 79, [("R26", "10k"), ("R29", "10k"), ("R27", "10k"), ("R28", "10k"), ("R4", "1k"), ("R65", "100k")])
    rline(64, 85, [("R66", "100k"), ("R73", "220k")])
    cline(90, 85, [("C26", "100n"), ("C51", "1µ"), ("C52", "1µ")])

    block = "VCF"
    Q("Q4", "J201", 128, 60)
    Q("Q5", "J201", 140, 60)
    Q("Q7", "2N5457", 152, 60)
    D("D2", "1N4148", 164, 60)
    rline(128, 68, [("R30", "10k"), ("R67", "100k"), ("R61", "68k"), ("R31", "10k"), ("R69", "100k")])
    rline(128, 74.4, [("R74", "220k"), ("R68", "100k"), ("R5", "1k"), ("R32", "10k"), ("R33", "10k")])
    rline(128, 80.8, [("R34", "10k"), ("R15", "4k7"), ("R81", "1M")])
    cline(128, 86.8, [("C43", "220n"), ("C44", "220n"), ("C45", "220n"), ("C46", "220n"), ("C47", "220n")])

    block = "CLK"
    D("D3", "1N4148", 184, 60)
    D("D4", "1N4148", 196, 60)
    R("R59", "47k", 208, 60)
    rline(184, 68, [("R43", "10k"), ("R70", "100k"), ("R79", "220k")])
    rline(184, 74.4, [("R11", "2k"), ("R7", "1k"), ("R8", "1k")])
    rline(184, 80.8, [("R56", "22k"), ("R9", "1k"), ("R10", "1k")])
    CE("C55", "4µ7", 186, 87)
    R("R60", "68k", 202, 87)

    block = "NAB"
    DIP8("U3", "TL072", SYM_OP, 66, 104)
    rline(80, 98, [("R51", "15k"), ("R52", "15k"), ("R53", "15k"), ("R54", "15k"), ("R16", "4k7")])
    rline(80, 104.4, [("R45", "10k"), ("R46", "10k")])
    cline(80, 111, [("C4", "3n3"), ("C5", "3n3"), ("C48", "220n"), ("C49", "220n"), ("C20", "100n"), ("C29", "100n")])
    C("C30", "100n", 80, 116.5)
    C("C50", "220n", 90, 116.5)

    block = "ENV"
    cline(128, 98, [("C27", "100n"), ("C28", "100n")])
    eline(128, 108, [("C68", "47µ"), ("C53", "2µ2"), ("C54", "2µ2"), ("C71", "47µ")])
    add("RV1", "100k", "Device:R_Potentiometer_Trim", FP_TRIM, 0, 0)

    block = "TRIM"
    add("RV2", "100k", "Device:R_Potentiometer_Trim", FP_TRIM, 0, 0)
    D("D7", "MP20", 202, 104)

    block = "FITA"
    DIP16("U6", "PT2399", SYM_PT, 68, 136)
    DIP16("U7", "PT2399", SYM_PT, 88, 136)
    DIP16("U8", "PT2399", SYM_PT, 108, 136)
    rline(
        124,
        126,
        [
            ("R35", "10k"),
            ("R36", "10k"),
            ("R37", "10k"),
            ("R38", "10k"),
            ("R39", "10k"),
            ("R40", "10k"),
            ("R41", "10k"),
            ("R47", "10k"),
        ],
    )
    rline(
        124,
        132.4,
        [
            ("R48", "10k"),
            ("R49", "10k"),
            ("R50", "10k"),
            ("R71", "100k"),
            ("R75", "220k"),
            ("R76", "220k"),
            ("R77", "220k"),
            ("R78", "220k"),
        ],
    )
    cline(
        124,
        139,
        [
            ("C3", "2n2"),
            ("C7", "10n"),
            ("C8", "10n"),
            ("C9", "10n"),
            ("C10", "10n"),
            ("C11", "10n"),
            ("C12", "10n"),
            ("C13", "10n"),
            ("C14", "10n"),
        ],
    )
    cline(
        124,
        145.4,
        [
            ("C15", "10n"),
            ("C16", "10n"),
            ("C17", "10n"),
            ("C18", "22n"),
            ("C31", "100n"),
            ("C32", "100n"),
            ("C33", "100n"),
            ("C34", "100n"),
            ("C35", "100n"),
        ],
    )
    cline(
        124,
        151.8,
        [
            ("C36", "100n"),
            ("C37", "100n"),
            ("C38", "100n"),
            ("C39", "100n"),
            ("C40", "100n"),
            ("C41", "100n"),
            ("C42", "100n"),
        ],
    )
    CE("C69", "47µ", 190, 151.8)
    CE("C70", "47µ", 202, 151.8)

    block = "FUROS"
    inset = 6.0
    for i, (x, y) in enumerate(
        ((inset, inset), (W - inset, inset), (inset, H - inset), (W - inset, H - inset)),
        start=1,
    ):
        add(f"H{i}", "M3", "Mechanical:MountingHole", FP_HOLE, x, y, bom=False)


# Caixa do footprint em relação à origem (pino 1), com folga para o corpo.
# TO-220 ganha espaço extra acima dos pinos para a aba.
BOX = {
    FP_R: (-1.2, -2.0, 9.2, 2.0),
    FP_C: (-1.5, -2.0, 6.8, 2.0),
    FP_CE: (-2.0, -3.2, 4.4, 3.2),
    FP_D: (-1.5, -2.0, 9.4, 2.0),
    FP_DIP8: (-1.8, -2.2, 9.6, 10.0),
    FP_DIP16: (-1.8, -2.2, 9.6, 20.2),
    FP_TO92: (-1.8, -3.2, 4.4, 2.4),
    FP_TO220: (-3.2, -16.0, 8.4, 2.2),
    FP_TRIM: (-8.2, -3.2, 3.0, 3.2),
}


def rank(part):
    """CI primeiro, depois o desacoplamento, resistores por último."""
    fp = part["fp"]
    if "DIP-16" in fp:
        return 0
    if "DIP-8" in fp:
        return 1
    if "TO-220" in fp:
        return 2
    if "TO-92" in fp:
        return 3
    if "Potentiometer" in fp:
        return 4
    if "Diode" in fp:
        return 5
    if "CP_Radial" in fp:
        return 6
    if "C_Rect" in fp:
        return 7
    if "R_Axial" in fp:
        return 8
    return 9


def pack(items, x0, y0, x1, gap=3.4):
    cursor_x = x0
    cursor_y = y0
    row_h = 0.0
    for part in items:
        left, top, right, bottom = BOX[part["fp"]]
        width = right - left
        height = bottom - top
        if cursor_x > x0 and cursor_x + width > x1:
            cursor_x = x0
            cursor_y += row_h + gap
            row_h = 0.0
        part["x"] = cursor_x - left
        part["y"] = cursor_y - top
        part["rot"] = 0
        cursor_x += width + gap
        row_h = max(row_h, height)
    return cursor_y + row_h


def place_pins():
    """Duas fileiras de pinos na borda de baixo. Pino 1 à esquerda."""
    by_ref = {part["ref"]: part for part in parts}
    rows = (
        (["J1", "J3", "J4", "J5"], 132.0),
        (["J2", "J7", "J9", "J6", "J8"], 121.6),
    )
    x_left, x_right = 16.0, 284.0
    # A fileira de baixo encosta na borda. A de cima fica 10 mm acima,
    # ainda abaixo dos blocos.
    for refs, y in rows:
        groups = []
        for ref in refs:
            part = by_ref[ref]
            count = int(part["fp"].split("1x")[1][:2])
            groups.append((part, count))
        span = sum((count - 1) * 2.54 for _, count in groups)
        gap = (x_right - x_left - span) / (len(groups) - 1)
        x = x_left
        for part, count in groups:
            part["x"] = x
            part["y"] = y
            part["rot"] = 90
            notes.append((f"{part['ref']} {part['val']}", x + (count - 1) * 1.27, y - 3.5))
            x += (count - 1) * 2.54 + gap


# Peças reagrupadas pelo fio que elas puxam, não pelo tamanho.
# O nome do bloco é o mesmo no esquema e na seda da placa.
FLOW = {
    "FONTE": "D1 U4 U5 C56 C57 C58 R14 R17 R19 R20 R18 R55 C22 C64 C65 C66 C67".split(),
    "OSC": "U2 Q1 Q2 R21 R22 R62 R63 R72 C21 C6 C19 C51 C52".split(),
    "MIX": "Q3 Q6 D6 R23 R24 R25 R26 R27 R28 R29 R3 R4 R64 R65 R66 R80 R73 C26".split(),
    "PRE": "U1 R12 R13 R57 R58 R6 R42 R44 C1 C2 C23 C24 C25 C59 C60 C61 C62 C63".split(),
    "EQ": ["U9"],
    "MOD": (
        "Q4 Q5 Q7 D2 RV2 R30 R31 R32 R33 R34 R67 R68 R69 R61 R5 R15 R74 R81 "
        "C43 C44 C45 C46 C47 C27 C28 C68 C71 C53 C54"
    ).split(),
    "NAB": "U3 R51 R52 R53 R54 R16 R45 R46 C4 C5 C48 C49 C50 C20 C29 C30".split(),
    "FITA": (
        "U6 U7 U8 RV1 D7 R35 R36 R37 R38 R39 R40 R41 R47 R48 R49 R50 R71 "
        "R75 R76 R77 R78 C3 C7 C8 C9 C10 C11 C12 C13 C14 C15 C16 C17 C18 "
        "C31 C32 C33 C34 C35 C36 C37 C38 C39 C40 C41 C42 C69 C70"
    ).split(),
    "CLK": "D3 D4 R59 R43 R70 R79 R11 R7 R8 R9 R10 R56 R60 C55".split(),
    "OUT": ["R1", "R2"],
}

HEADER_BLOCK = {
    "J1": "OSC",
    "J2": "MOD",
    "J3": "FITA",
    "J4": "MOD",
    "J5": "CLK",
    "J6": "FONTE",
    "J7": "PRE",
    "J8": "OUT",
    "J9": "EQ",
}

# (x0, y0, x1, limite_y). Os pinos de cima estão em y=121,6.
# A faixa de baixo para antes deles.
ISLANDS = (
    ("PRE", 14, 14, 122, 36),
    ("EQ", 126, 14, 162, 40),
    ("FONTE", 166, 14, 290, 46),
    ("MOD", 14, 40, 104, 68),
    ("FITA", 108, 46, 248, 90),
    ("OSC", 14, 88, 84, 114),
    ("NAB", 108, 89, 198, 114),
    ("CLK", 202, 93, 272, 114),
    ("MIX", 252, 42, 290, 92),
    ("OUT", 262, 96, 290, 114),
)

# U9 fica neste retângulo. A rede Baxandall ainda não tem peça.
EQ_BAY = (126, 14, 162, 40)


def assign_flow():
    owner = {}
    for name, refs in FLOW.items():
        for ref in refs:
            if ref in owner:
                raise SystemExit(f"{ref} em dois blocos")
            owner[ref] = name
    for part in parts:
        ref = part["ref"]
        if ref in owner:
            part["block"] = owner[ref]
        elif ref in HEADER_BLOCK:
            part["block"] = HEADER_BLOCK[ref]
        elif ref[0] == "H":
            part["block"] = "FUROS"
        else:
            raise SystemExit(f"{ref} sem bloco de roteamento")
    missing = [ref for ref in owner if ref not in {p["ref"] for p in parts}]
    if missing:
        raise SystemExit(f"bloco cita ref ausente: {missing}")


def place_blocks():
    groups = {}
    for part in parts:
        if part["ref"][0] in "JH":
            continue
        groups.setdefault(part["block"], []).append(part)
    for items in groups.values():
        items.sort(key=rank)

    # O nome fica acima do bloco quando cabe. NAB e MIX encostam
    # no bloco de cima, então o texto desce para o vão de 2 mm.
    label_at = {
        "NAB": (116, 88.0),
        "MIX": (258, 40.4),
    }
    bottom = 0.0
    for name, x0, y0, x1, limit in ISLANDS:
        if name in label_at:
            notes.append((name, label_at[name][0], label_at[name][1]))
        else:
            notes.append((name, x0, y0 - 3.2))
        items = groups.pop(name)
        island_bottom = y0
        if items:
            island_bottom = pack(items, x0, y0, x1, gap=2.2)
        print(f"  {name:6} y {y0:.0f}→{island_bottom:.1f}  limite {limit:.0f}  x {x0:.0f}–{x1:.0f}")
        if island_bottom > limit:
            raise SystemExit(f"{name} desceu até {island_bottom:.1f}, limite {limit}")
        bottom = max(bottom, island_bottom)
    if groups:
        raise SystemExit(f"blocos sem lugar: {sorted(groups)}")
    # Vão entre o MOD e o OSC, longe da fita.
    notes.append(("V9  GND  VEE  V5  4V5  1V8", 48, 76))
    return bottom


def part_box(part):
    if part["ref"].startswith("J"):
        count = int(part["fp"].split("1x")[1][:2])
        left, top, right, bottom = -1.7, -1.7, 1.7, (count - 1) * 2.54 + 1.7
    elif part["ref"].startswith("H"):
        left, top, right, bottom = -3.2, -3.2, 3.2, 3.2
    else:
        left, top, right, bottom = BOX[part["fp"]]
    rot = part.get("rot") or 0
    rad = math.radians(rot)
    cos_r, sin_r = math.cos(rad), math.sin(rad)
    corners = []
    for x, y in ((left, top), (right, top), (right, bottom), (left, bottom)):
        corners.append(
            (part["x"] + x * cos_r + y * sin_r, part["y"] - x * sin_r + y * cos_r)
        )
    xs = [point[0] for point in corners]
    ys = [point[1] for point in corners]
    return min(xs), min(ys), max(xs), max(ys)


def check_placement():
    boxes = [(part["ref"],) + part_box(part) for part in parts]
    for i, (ref_a, ax0, ay0, ax1, ay1) in enumerate(boxes):
        if ax0 < 1 or ay0 < 1 or ax1 > W - 1 or ay1 > H - 1:
            raise SystemExit(f"{ref_a} fora da placa ({ax0:.1f},{ay0:.1f})-({ax1:.1f},{ay1:.1f})")
        for ref_b, bx0, by0, bx1, by1 in boxes[i + 1 :]:
            overlap_x = min(ax1, bx1) - max(ax0, bx0)
            overlap_y = min(ay1, by1) - max(ay0, by0)
            if overlap_x > 0.4 and overlap_y > 0.4:
                raise SystemExit(f"sobreposição {ref_a} × {ref_b}")
    bay_x0, bay_y0, bay_x1, bay_y1 = EQ_BAY
    for ref, x0, y0, x1, y1 in boxes:
        if ref == "U9":
            continue
        overlap_x = min(x1, bay_x1) - max(x0, bay_x0)
        overlap_y = min(y1, bay_y1) - max(y0, bay_y0)
        if overlap_x > 0.4 and overlap_y > 0.4:
            raise SystemExit(f"{ref} invadiu a baía do EQ")


def check_parts():
    refs = [p["ref"] for p in parts]
    dup = {r for r in refs if refs.count(r) > 1}
    if dup:
        raise SystemExit(f"refs duplicadas: {sorted(dup)}")
    missing_r = [f"R{i}" for i in range(1, 82) if f"R{i}" not in refs]
    missing_c = [f"C{i}" for i in range(1, 72) if f"C{i}" not in refs]
    if missing_r or missing_c:
        raise SystemExit(f"faltando R={missing_r} C={missing_c}")


def balanced(text, idx):
    depth = 0
    for i, ch in enumerate(text[idx:], idx):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[idx : i + 1]
    raise RuntimeError("sexpr sem fecho")


def find_symbol(text, name):
    key = f'(symbol "{name}"'
    start = 0
    while True:
        idx = text.find(key, start)
        if idx < 0:
            raise KeyError(name)
        nxt = text[idx + len(key) : idx + len(key) + 1]
        if nxt in "\r\n\t ":
            return balanced(text, idx)
        start = idx + 1


def rename_lib_symbol(body, lib_id):
    prefix = '(symbol "'
    if not body.startswith(prefix):
        raise RuntimeError(body[:40])
    return prefix + lib_id + body[len(prefix) + body[len(prefix) :].find('"') :]


def pins_by_unit(body, short):
    units = {}
    token = f'(symbol "{short}_'
    start = 0
    while True:
        idx = body.find(token, start)
        if idx < 0:
            break
        m = re.match(rf'\(symbol "{re.escape(short)}_(\d+)_\d+"', body[idx:])
        if not m:
            start = idx + 1
            continue
        sub = balanced(body, idx)
        nums = re.findall(r'\(number "([^"]+)"', sub)
        seen = units.setdefault(int(m.group(1)), [])
        for n in nums:
            if n not in seen:
                seen.append(n)
        start = idx + len(sub)
    return units


LIB_FILES = {
    "Device": "Device.kicad_sym",
    "Amplifier_Operational": "Amplifier_Operational.kicad_sym",
    "Regulator_Linear": "Regulator_Linear.kicad_sym",
    "Regulator_SwitchedCapacitor": "Regulator_SwitchedCapacitor.kicad_sym",
    "Audio": "Audio.kicad_sym",
    "Mechanical": "Mechanical.kicad_sym",
    "Connector_Generic": "Connector_Generic.kicad_sym",
}


def load_symbols(used):
    cache = {}
    embedded = []
    meta = {}
    for lib_id in sorted(used):
        lib, name = lib_id.split(":", 1)
        path = os.path.join(SYM, LIB_FILES[lib])
        if path not in cache:
            cache[path] = open(path, encoding="utf-8").read()
        body = find_symbol(cache[path], name)
        embedded.append(rename_lib_symbol(body, lib_id))
        units = pins_by_unit(body, name)
        place = [u for u in sorted(units) if u != 0 and units[u]]
        if not place:
            place = [1]
            units = {1: []}
        meta[lib_id] = {"units": place, "pins": units}
    return embedded, meta


def sch_escape(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')


def sch_cell(part, pins):
    """Largura e altura para o símbolo não encostar no vizinho."""
    ref = part["ref"]
    if ref.startswith("J"):
        count = max(len(pins), 2)
        return 24.0, 10.0 + 2.54 * count
    if ref.startswith("H"):
        return 12.0, 12.0
    fp = part["fp"]
    if "DIP-16" in fp:
        return 46.0, 52.0
    if "TO-220" in fp:
        return 24.0, 30.0
    if "DIP-8" in fp or part["sym"].endswith("LM2904") or "MAX1044" in part["sym"]:
        return 28.0, 22.0
    if "TO-92" in fp:
        return 18.0, 20.0
    if "Potentiometer" in fp:
        return 18.0, 20.0
    return 14.0, 16.0


def write_schematic(path, embedded, meta):
    cells = []
    order = ["FONTE", "OSC", "MIX", "PRE", "EQ", "MOD", "NAB", "FITA", "CLK", "OUT", "FUROS"]
    by_block = {name: [p for p in parts if p["block"] == name] for name in order}

    row_top = 292.0
    floor = 24.0
    x = 30.0
    texts = [
        (
            20,
            row_top + 16,
            "VOZ-9 BASE. Blocos na ordem do sinal, o mesmo agrupamento da placa. "
            "J1–J9 à esquerda de cada bloco: pino 1×N na borda de baixo da PCB. "
            "Ainda sem fios. D1 ânodo para J6. D6/D7 = MP20. "
            "Q7 2N5457: conferir a pinagem do lote. U9: baía livre para a rede do EQ.",
        )
    ]
    for name in order:
        items = by_block.get(name, [])
        items.sort(key=lambda part: (0 if part["ref"].startswith("J") else 1, part["ref"]))
        expanded = []
        for p in items:
            info = meta[p["sym"]]
            for unit in info["units"]:
                expanded.append((p, unit, info["pins"].get(unit, [])))
        if not expanded:
            continue
        texts.append((x, row_top + 6, name))
        cursor_x = x
        cursor_y = row_top
        col_w = 0.0
        block_right = x
        for p, unit, pins in expanded:
            width, height = sch_cell(p, pins)
            if cursor_y - height < floor:
                cursor_x += col_w + 10.0
                cursor_y = row_top
                col_w = 0.0
            cells.append((p, unit, pins, cursor_x, cursor_y))
            cursor_y -= height + 6.0
            col_w = max(col_w, width)
            block_right = max(block_right, cursor_x + width)
        x = block_right + 22.0

    page_w = max(420.0, x + 16.0)
    page_h = row_top + 36.0

    lines = [
        "(kicad_sch",
        "\t(version 20260101)",
        '\t(generator "voz9_gen_kicad")',
        '\t(generator_version "10.0")',
        f'\t(uuid "{SHEET_UUID}")',
        f'\t(paper "User" {page_w:.0f} {page_h:.0f})',
        "\t(title_block",
        '\t\t(title "VOZ-9 BASE")',
        '\t\t(date "2026-09-27")',
        '\t\t(rev "A")',
        '\t\t(comment 1 "Placa 300 x 140 mm. Blocos na ordem do sinal, ainda sem fios.")',
        "\t)",
        "\t(lib_symbols",
    ]
    for body in embedded:
        for line in body.splitlines():
            lines.append("\t\t" + line)
    lines.append("\t)")

    for p, unit, pins, sx, sy in cells:
        bom = "yes" if p["bom"] else "no"
        lines += [
            "\t(symbol",
            f'\t\t(lib_id "{p["sym"]}")',
            f"\t\t(at {sx:.2f} {sy:.2f} 0)",
            f"\t\t(unit {unit})",
            "\t\t(body_style 1)",
            "\t\t(exclude_from_sim no)",
            f"\t\t(in_bom {bom})",
            "\t\t(on_board yes)",
            "\t\t(in_pos_files yes)",
            "\t\t(dnp no)",
            f'\t\t(uuid "{uid(p["ref"], str(unit), "sym")}")',
            "\t\t(property \"Reference\" \"" + p["ref"] + "\"",
            f"\t\t\t(at {sx:.2f} {sy + 5.5:.2f} 0)",
            "\t\t\t(show_name no)",
            "\t\t\t(do_not_autoplace no)",
            "\t\t\t(effects (font (size 1.27 1.27)) (justify left))",
            "\t\t)",
            "\t\t(property \"Value\" \"" + sch_escape(p["val"]) + "\"",
            f"\t\t\t(at {sx:.2f} {sy - 5.5:.2f} 0)",
            "\t\t\t(show_name no)",
            "\t\t\t(do_not_autoplace no)",
            "\t\t\t(effects (font (size 1.27 1.27)) (justify left))",
            "\t\t)",
            "\t\t(property \"Footprint\" \"" + p["fp"] + "\"",
            f"\t\t\t(at {sx:.2f} {sy:.2f} 0)",
            "\t\t\t(hide yes)",
            "\t\t\t(show_name no)",
            "\t\t\t(do_not_autoplace no)",
            "\t\t\t(effects (font (size 1.27 1.27)))",
            "\t\t)",
            "\t\t(property \"Datasheet\" \"\"",
            f"\t\t\t(at {sx:.2f} {sy:.2f} 0)",
            "\t\t\t(hide yes)",
            "\t\t\t(show_name no)",
            "\t\t\t(do_not_autoplace no)",
            "\t\t\t(effects (font (size 1.27 1.27)))",
            "\t\t)",
            "\t\t(property \"Description\" \"" + sch_escape(p["block"]) + "\"",
            f"\t\t\t(at {sx:.2f} {sy:.2f} 0)",
            "\t\t\t(hide yes)",
            "\t\t\t(show_name no)",
            "\t\t\t(do_not_autoplace no)",
            "\t\t\t(effects (font (size 1.27 1.27)))",
            "\t\t)",
        ]
        for num in pins:
            lines += [
                f'\t\t(pin "{num}"',
                f'\t\t\t(uuid "{uid(p["ref"], str(unit), "pin", num)}")',
                "\t\t)",
            ]
        lines += [
            "\t\t(instances",
            '\t\t\t(project "voz-9"',
            f'\t\t\t\t(path "/{SHEET_UUID}"',
            f'\t\t\t\t\t(reference "{p["ref"]}")',
            "\t\t\t\t\t(unit " + str(unit) + ")",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t)",
            "\t)",
        ]

    for tx, ty, text in texts:
        lines += [
            "\t(text \"" + sch_escape(text) + "\"",
            f"\t\t(at {tx:.2f} {ty:.2f} 0)",
            "\t\t(effects (font (size 2.0 2.0)))",
            f'\t\t(uuid "{uid("text", text[:24], f"{tx:.0f}")}")',
            "\t)",
        ]
    lines += [
        "\t(sheet_instances",
        '\t\t(path "/"',
        '\t\t\t(page "1")',
        "\t\t)",
        "\t)",
        "\t(embedded_fonts no)",
        ")",
        "",
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def mm(v):
    return pcbnew.FromMM(v)


def xy(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


def add_seg(board, x1, y1, x2, y2, layer, width=0.15):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetStart(xy(x1, y1))
    seg.SetEnd(xy(x2, y2))
    seg.SetLayer(layer)
    seg.SetWidth(mm(width))
    board.Add(seg)


def add_text(board, text, x, y, layer, size=1.6):
    item = pcbnew.PCB_TEXT(board)
    item.SetText(text)
    item.SetPosition(xy(x, y))
    item.SetLayer(layer)
    item.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    item.SetTextThickness(mm(size * 0.15))
    board.Add(item)


def load_fp(fp_id):
    nick, name = fp_id.split(":", 1)
    directory = os.path.join(FP, nick + ".pretty")
    fp = pcbnew.FootprintLoad(directory, name)
    if fp is None:
        raise SystemExit(f"footprint ausente: {fp_id}")
    fp.SetFPID(pcbnew.LIB_ID(nick, name))
    return fp


def write_board(path):
    board = pcbnew.BOARD()
    settings = board.GetDesignSettings()
    settings.SetCopperLayerCount(2)
    settings.m_TrackMinWidth = mm(0.25)
    settings.m_MinClearance = mm(0.2)
    tb = board.GetTitleBlock()
    tb.SetTitle("VOZ-9 BASE")
    tb.SetDate("2026-09-27")
    tb.SetRevision("A")
    tb.SetComment(0, "300 x 140 mm")
    tb.SetComment(1, "Blocos junto do conector. Duas placas cabem numa chapa de 300 x 300.")

    add_seg(board, 0, 0, W, 0, pcbnew.Edge_Cuts)
    add_seg(board, W, 0, W, H, pcbnew.Edge_Cuts)
    add_seg(board, W, H, 0, H, pcbnew.Edge_Cuts)
    add_seg(board, 0, H, 0, 0, pcbnew.Edge_Cuts)

    add_text(board, "VOZ-9 BASE  300 x 140 mm", 150, 5.2, pcbnew.F_SilkS, 1.8)
    bay_x0, bay_y0, bay_x1, bay_y1 = EQ_BAY
    for x1, y1, x2, y2 in (
        (bay_x0, bay_y0, bay_x1, bay_y0),
        (bay_x1, bay_y0, bay_x1, bay_y1),
        (bay_x1, bay_y1, bay_x0, bay_y1),
        (bay_x0, bay_y1, bay_x0, bay_y0),
    ):
        add_seg(board, x1, y1, x2, y2, pcbnew.F_SilkS, 0.12)
    add_text(board, "EQ 424", bay_x0 + 28, (bay_y0 + bay_y1) / 2, pcbnew.F_SilkS, 1.4)
    for text, x, y in notes:
        add_text(board, text, x, y, pcbnew.F_SilkS, 1.15)

    for p in parts:
        fp = load_fp(p["fp"])
        fp.SetPosition(xy(p["x"], p["y"]))
        if p.get("rot"):
            fp.SetOrientation(pcbnew.EDA_ANGLE(p["rot"], pcbnew.DEGREES_T))
        fp.SetReference(p["ref"])
        fp.SetValue(p["val"])
        if p["ref"].startswith("J"):
            fp.Reference().SetVisible(False)
            fp.Value().SetVisible(False)
        else:
            fp.Reference().SetVisible(True)
        if "TO-92" in p["fp"]:
            for pad in fp.Pads():
                if pad.GetNumber() == "1":
                    pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        if not p["bom"]:
            fp.SetExcludedFromBOM(True)
        board.Add(fp)

    pcbnew.SaveBoard(path, board)
    # O pcbnew grava A4. Troca pela folha que cabe a placa.
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    old = '(paper "A4")'
    new = f'(paper "User" {PAGE_W:.0f} {PAGE_H:.0f})'
    if old not in text:
        raise SystemExit("folha A4 não encontrada para substituir")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new, 1))


def write_project(path):
    pro = json.load(open(DEMO_PRO, encoding="utf-8"))
    pro["meta"]["filename"] = "voz-9.kicad_pro"
    pro["sheets"] = [[SHEET_UUID, "voz-9"]]
    pro["schematic"]["top_level_sheets"] = [
        {"filename": "voz-9.kicad_sch", "name": "voz-9", "uuid": SHEET_UUID}
    ]
    pro["schematic"]["legacy_lib_list"] = []
    paths = pro["pcbnew"]["last_paths"]
    paths["netlist"] = "voz-9.net"
    paths["step"] = "voz-9.step"
    default = pro["net_settings"]["classes"][0]
    default["track_width"] = 0.6
    default["clearance"] = 0.35
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(pro, fh, indent=2)
        fh.write("\n")


def main():
    build_parts()
    assign_flow()
    check_parts()
    place_pins()
    bottom = place_blocks()
    check_placement()
    used = {p["sym"] for p in parts}
    embedded, meta = load_symbols(used)
    write_board(os.path.join(ROOT, "voz-9.kicad_pcb"))
    write_schematic(os.path.join(ROOT, "voz-9.kicad_sch"), embedded, meta)
    write_project(os.path.join(ROOT, "voz-9.kicad_pro"))
    print(f"ok  peças={len(parts)}  placa={W:.0f}x{H:.0f}  circuito até y={bottom:.1f}")


if __name__ == "__main__":
    main()
