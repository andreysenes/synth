#!/usr/bin/env python3
"""Gera o projeto KiCad da BASE VOZ-9 (placa 300×300 mm).

O miolo é o mesmo desenho de `_gen_pcb.py` (220×160 centrado).
Não há netlist no SVG: o esquema traz as peças, os valores e os
footprints, ainda sem fios.
"""

import json
import os
import re
import uuid

import pcbnew

ROOT = os.path.dirname(os.path.abspath(__file__))
SYM = "/usr/share/kicad/symbols"
FP = "/usr/share/kicad/footprints"
DEMO_PRO = "/usr/share/kicad/demos/pic_programmer/pic_programmer.kicad_pro"

W, H = 300.0, 300.0
OX, OY = (W - 220.0) / 2.0, (H - 160.0) / 2.0  # igual a _gen_pcb.py

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
block = ""


def uid(*bits):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "voz-9:" + ":".join(bits)))


def add(ref, val, sym, fp, x, y, bom=True):
    parts.append(
        {
            "ref": ref,
            "val": val,
            "sym": sym,
            "fp": fp,
            "x": x,
            "y": y,
            "block": block,
            "bom": bom,
        }
    )


def R(ref, val, x, y):
    add(ref, val, "Device:R", FP_R, x - 3.81 + OX, y + OY)


def C(ref, val, x, y):
    add(ref, val, "Device:C", FP_C, x - 2.5 + OX, y + OY)


def CE(ref, val, x, y):
    add(ref, val, "Device:C_Polarized", FP_CE, x - 1.25 + OX, y + OY)


def D(ref, val, x, y):
    add(ref, val, "Device:D", FP_D, x - 3.81 + OX, y + OY)


def Q(ref, val, x, y):
    add(ref, val, SYM_JFET, FP_TO92, x - 1.27 + OX, y + 0.42 + OY)


def DIP8(ref, val, sym, x, y):
    add(ref, val, sym, FP_DIP8, x - 3.81 + OX, y - 3.81 + OY)


def DIP16(ref, val, sym, x, y):
    add(ref, val, sym, FP_DIP16, x - 3.81 + OX, y - 8.89 + OY)


def HDR(ref, cols, x, y, name):
    add(
        ref,
        name,
        f"Connector_Generic:Conn_02x{cols:02d}_Top_Bottom",
        f"voz9:PinSocket_2x{cols:02d}_TopBottom",
        x + OX,
        y + OY,
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
    add("U5", "78M05", SYM_REG, FP_TO220, 100 - 2.54 + OX, 23.6 + OY)
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
    add("RV1", "100k", "Device:R_Potentiometer_Trim", FP_TRIM, 168 + 2.54 + OX, 108 + OY)

    block = "TRIM"
    add("RV2", "100k", "Device:R_Potentiometer_Trim", FP_TRIM, 186 + 2.54 + OX, 104 + OY)
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


def write_schematic(path, embedded, meta):
    cells = []
    order = []
    seen = set()
    for p in parts:
        if p["block"] not in seen:
            seen.add(p["block"])
            order.append(p["block"])
    by_block = {name: [p for p in parts if p["block"] == name] for name in order}

    page_w, page_h = 1180.0, 420.0
    x = 25.0
    row_top = page_h - 28.0
    texts = [
        (
            20,
            page_h - 12,
            "VOZ-9 BASE 300×300 mm — peças do pcb.svg, ainda sem ligações. "
            "D6/D7 = MP20. J1–J9 numerados em linha (pino 1 no canto). "
            "Q7 2N5457: conferir pinagem do lote.",
        )
    ]
    for name in order:
        items = by_block[name]
        expanded = []
        for p in items:
            info = meta[p["sym"]]
            for unit in info["units"]:
                expanded.append((p, unit, info["pins"].get(unit, [])))
        cols = (len(expanded) + 15) // 16
        width = cols * 30.0
        if x + width > page_w - 15:
            x = 25.0
            row_top -= 330.0
        texts.append((x, row_top + 8, name))
        y = row_top
        col = 0
        n = 0
        for p, unit, pins in expanded:
            if n == 16:
                col += 1
                n = 0
                y = row_top
            cells.append((p, unit, pins, x + col * 30.0, y))
            y -= 18.0
            n += 1
        x += width + 16.0

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
        '\t\t(comment 1 "Placa 300 x 300 mm. Esquema sem fios.")',
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


def make_header(cols):
    src = pcbnew.FootprintLoad(
        os.path.join(FP, "Connector_PinSocket_2.54mm.pretty"),
        f"PinSocket_2x{cols:02d}_P2.54mm_Vertical",
    )
    sample = list(src.Pads())[0]
    fp = pcbnew.FOOTPRINT(None)
    name = f"PinSocket_2x{cols:02d}_TopBottom"
    fp.SetFPID(pcbnew.LIB_ID("voz9", name))
    fp.SetReference("REF**")
    fp.SetValue(f"J 2x{cols}")
    fp.SetLibDescription(
        "Soquete fêmea 2,54 mm. Pino 1 no canto superior esquerdo; "
        "a fila de cima é 1..N e a de baixo N+1..2N."
    )
    fp.SetAttributes(pcbnew.FP_THROUGH_HOLE)
    for col in range(cols):
        for row in range(2):
            n = col + 1 + row * cols
            pad = pcbnew.PAD(fp)
            pad.SetNumber(str(n))
            pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
            pad.SetShape(pcbnew.PAD_SHAPE_RECT if n == 1 else pcbnew.PAD_SHAPE_CIRCLE)
            pad.SetSize(sample.GetSize())
            pad.SetDrillSize(sample.GetDrillSize())
            pad.SetLayerSet(sample.GetLayerSet())
            pad.SetPosition(xy(col * 2.54, row * 2.54))
            fp.Add(pad)
    x1, y1 = -1.4, -1.5
    x2, y2 = (cols - 1) * 2.54 + 1.4, 2.54 + 1.5
    for layer, width in ((pcbnew.F_SilkS, 0.12), (pcbnew.F_CrtYd, 0.05)):
        box = pcbnew.PCB_SHAPE(fp)
        box.SetShape(pcbnew.SHAPE_T_RECT)
        box.SetStart(xy(x1, y1))
        box.SetEnd(xy(x2, y2))
        box.SetLayer(layer)
        box.SetWidth(mm(width))
        if layer == pcbnew.F_CrtYd:
            box.SetStart(xy(x1 - 0.25, y1 - 0.25))
            box.SetEnd(xy(x2 + 0.25, y2 + 0.25))
        fp.Add(box)
    fp.Reference().SetPosition(xy((cols - 1) * 1.27, -2.6))
    fp.Value().SetPosition(xy((cols - 1) * 1.27, 2.54 + 3.2))
    return name, fp


def write_footprints():
    lib = os.path.join(ROOT, "voz9.pretty")
    os.makedirs(lib, exist_ok=True)
    io = pcbnew.PCB_IO_MGR.FindPlugin(pcbnew.PCB_IO_MGR.KICAD_SEXP)
    for cols in (3, 6, 8, 10):
        name, fp = make_header(cols)
        io.FootprintSave(lib, fp)
    table = """(fp_lib_table
  (version 7)
  (lib (name "voz9")(type "KiCad")(uri "${KIPRJMOD}/voz9.pretty")(options "")(descr "Conectores J1–J9, numeração em linha"))
)
"""
    with open(os.path.join(ROOT, "fp-lib-table"), "w", encoding="utf-8") as fh:
        fh.write(table)


def load_fp(fp_id):
    nick, name = fp_id.split(":", 1)
    if nick == "voz9":
        directory = os.path.join(ROOT, "voz9.pretty")
    else:
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
    tb.SetComment(0, "300 x 300 mm")
    tb.SetComment(1, "Cobre simples no verso. Esquema ainda sem nets.")

    add_seg(board, 0, 0, W, 0, pcbnew.Edge_Cuts)
    add_seg(board, W, 0, W, H, pcbnew.Edge_Cuts)
    add_seg(board, W, H, 0, H, pcbnew.Edge_Cuts)
    add_seg(board, 0, H, 0, 0, pcbnew.Edge_Cuts)

    add_text(board, "VOZ-9 BASE  300 x 300 mm", 150, 8, pcbnew.F_SilkS, 2.2)
    add_text(
        board,
        "miolo 220x160 centrado   cobre no verso   CIs em soquete   pino 1 quadrado nos J",
        150,
        12,
        pcbnew.F_SilkS,
        1.2,
    )
    # Trilhos desenhados no SVG (ainda não são nets).
    for x, label in ((54, "GND"), (56.6, "V9"), (214, "4V5")):
        add_seg(board, x + OX, 10 + OY, x + OX, 150 + OY, pcbnew.Dwgs_User, 0.4)
        add_text(board, label, x + OX, 8 + OY, pcbnew.Dwgs_User, 1.2)

    for p in parts:
        fp = load_fp(p["fp"])
        fp.SetPosition(xy(p["x"], p["y"]))
        fp.SetReference(p["ref"])
        fp.SetValue(p["val"])
        fp.Reference().SetVisible(True)
        if not p["bom"]:
            fp.SetExcludedFromBOM(True)
        board.Add(fp)

    pcbnew.SaveBoard(path, board)


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
    check_parts()
    used = {p["sym"] for p in parts}
    embedded, meta = load_symbols(used)
    write_footprints()
    write_board(os.path.join(ROOT, "voz-9.kicad_pcb"))
    write_schematic(os.path.join(ROOT, "voz-9.kicad_sch"), embedded, meta)
    write_project(os.path.join(ROOT, "voz-9.kicad_pro"))
    print(f"ok  peças={len(parts)}  placa={W:.0f}x{H:.0f}  offset=({OX:.0f},{OY:.0f})")


if __name__ == "__main__":
    main()
