"""Versão SMT da BASE: 200×100 mm, montável na JLCPCB.

A v1 (300×140, through-hole) não muda. Aqui só o que a pick-and-place
solda. J1–J9 são furos de fio, passo 3,96 mm, furo 1,6 mm: o cabo do
painel, inclusive o condutor do XLR, entra no furo e solda à mão.
D6 e D7 continuam MP20 axial: a LCSC não tem germânio.
"""

import csv
import os
import uuid

import pcbnew

# Axial que a v1 já usa. D6/D7 voltam para ele depois do tune.
FP_GE = "Diode_THT:D_DO-41_SOD81_P7.62mm_Horizontal"
FP_0603 = "Capacitor_SMD:C_0603_1608Metric"

# Valor normalizado -> LCSC. Resistores e capacitores da biblioteca Basic,
# os mesmos códigos já conferidos em jlcpcb-bom.csv.
PASSIVE = {
    "220": "C17557",
    "1k": "C17513",
    "2k": "C17604",
    "2k2": "C17520",
    "3k3": "C26010",
    "4k7": "C17673",
    "5k6": "C4382",
    "10k": "C17414",
    "15k": "C17475",
    "22k": "C17560",
    "47k": "C17713",
    "68k": "C17801",
    "100k": "C149504",
    "220k": "C17556",
    "1m": "C17514",
    "100p": "C1790",
    "1n": "C46653",
    "2n2": "C28260",
    "3n3": "C1613",
    "10n": "C1710",
    "22n": "C1729",
    "33n": "C1739",
    "100n": "C49678",
    "220n": "C5378",
    "1u": "C28323",
    "2u2": "C377773",
    "4u7": "C1779",
    "10u": "C15850",
    "22u": "C45783",
}

CHIP = {
    "U1": ("C7426", "SOIC-8", "NE5532DR"),
    "U2": ("C67473", "SOIC-8", "TL072CDR"),
    "U3": ("C67473", "SOIC-8", "TL072CDR"),
    "U4": ("C42421900", "SOIC-8", "ICL7660"),
    "U5": ("C58069", "TO-252-2", "78M05"),
    "U6": ("C126407", "SOP-16", "PT2399"),
    "U7": ("C126407", "SOP-16", "PT2399"),
    "U8": ("C126407", "SOP-16", "PT2399"),
    "U9": ("C67473", "SOIC-8", "TL072CDR"),
    "Q7": ("C2830807", "SOT-23", "MMBF5457"),
    "D1": ("C2480", "SMA", "SS14"),
    "D2": ("C2128", "SOD-323", "1N4148WS"),
    "D3": ("C2128", "SOD-323", "1N4148WS"),
    "D4": ("C2128", "SOD-323", "1N4148WS"),
    "D5": ("C2128", "SOD-323", "1N4148WS"),
    "RV1": ("C51284", "3314J", "100k"),
    "RV2": ("C51284", "3314J", "100k"),
}


_g = None

# Furo largo o bastante para o condutor de um cabo de XLR (até ~1 mm²)
# e para a malha torcida. Passo 3,96 mm: padrão de pino de fio.
PIN_PITCH = 3.96
PIN_DRILL = 1.6
PIN_PAD = 2.5
PIN_COUNTS = (6, 12, 16, 20)


def activate(mod):
    """`mod` é o gen_kicad que está rodando. Como script ele é __main__, não o import."""
    global _g
    _g = mod
    g = mod
    g.V2 = True
    g.OUT = os.path.join(os.path.dirname(g.ROOT), "kicad-v2")
    g.W, g.H = 200.0, 100.0
    g.PAGE_W, g.PAGE_H = 260.0, 140.0
    g.SHEET_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, "voz-9-v2-sheet"))
    g.TOP, g.LEFT = 6.0, 8.0
    # A altura é curta: o circuito tem de acabar antes da fileira de furos.
    g.GAP, g.ROW = 1.5, 1.15
    g.BAND, g.BAND_LAST = 2.6, 2.4
    g.COL, g.HEAD_GAP = 6.5, 4.5
    g.HOLE_INSET = 4.2
    ensure_footprints()

    g.FP_R = "Resistor_SMD:R_0805_2012Metric"
    g.FP_C = "Capacitor_SMD:C_0805_2012Metric"
    g.FP_CE = g.FP_C
    g.FP_D = "Diode_SMD:D_SOD-323"
    g.FP_DIP8 = "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
    g.FP_DIP16 = "Package_SO:SOP-16_4.4x10.4mm_P1.27mm"
    g.FP_TO92 = "Package_TO_SOT_SMD:SOT-23"
    g.FP_TO220 = "Package_TO_SOT_SMD:TO-252-3_TabPin2"
    g.FP_TRIM = "Potentiometer_SMD:Potentiometer_Bourns_3314J_Vertical"

    g.BOX[g.FP_R] = (-1.85, -1.15, 1.85, 1.15)
    g.BOX[g.FP_C] = (-1.90, -1.15, 1.90, 1.15)
    g.BOX[FP_0603] = (-1.65, -0.90, 1.65, 0.90)
    g.BOX["Diode_SMD:D_SMA"] = (-3.70, -1.90, 3.70, 1.90)
    g.BOX[g.FP_D] = (-1.80, -1.10, 1.80, 1.10)
    g.BOX[g.FP_DIP8] = (-3.90, -3.05, 3.90, 3.05)
    g.BOX[g.FP_DIP16] = (-4.50, -5.80, 4.50, 5.70)
    g.BOX[g.FP_TO92] = (-2.10, -1.90, 2.10, 1.90)
    g.BOX[g.FP_TO220] = (-6.60, -3.90, 4.90, 3.70)
    g.BOX[g.FP_TRIM] = (-2.70, -3.50, 2.70, 3.50)
    g.BOX[FP_GE] = (-1.50, -2.00, 9.40, 2.00)


def _key(value):
    return value.lower().replace("µ", "u").replace("μ", "u").replace("ω", "")


def ensure_footprints():
    """Furos redondos, pino 1 quadrado, para soldar o cabo direto."""
    pretty = os.path.join(os.path.dirname(__file__), "footprints", "VOZ9_Wire.pretty")
    os.makedirs(pretty, exist_ok=True)
    for count in PIN_COUNTS:
        name = f"WirePin_1x{count:02d}_P3.96mm_D1.6mm"
        path = os.path.join(pretty, name + ".kicad_mod")
        span = (count - 1) * PIN_PITCH
        pads = []
        for index in range(count):
            shape = "rect" if index == 0 else "circle"
            y = index * PIN_PITCH
            pads.append(
                "\t(pad \"{n}\" thru_hole {shape}\n"
                "\t\t(at 0 {y:.2f})\n"
                "\t\t(size {pad:.2f} {pad:.2f})\n"
                "\t\t(drill {drill:.2f})\n"
                "\t\t(layers \"*.Cu\" \"*.Mask\")\n"
                "\t\t(remove_unused_layers no)\n"
                "\t)".format(n=index + 1, shape=shape, y=y, pad=PIN_PAD, drill=PIN_DRILL)
            )
        silk = PIN_PAD / 2 + 0.35
        body = "\n".join(
            [
                f'(footprint "{name}"',
                "\t(version 20260206)",
                '\t(generator "voz9_v2")',
                '\t(layer "F.Cu")',
                f'\t(descr "Furo de fio 1x{count}, passo 3,96 mm, furo 1,6 mm. Cabo solda direto.")',
                "\t(attr through_hole)",
                "\t(duplicate_pad_numbers_are_jumpers no)",
                "\t(property \"Reference\" \"REF**\"",
                f"\t\t(at 0 {-silk - 1:.2f} 0)",
                '\t\t(layer "F.SilkS")',
                "\t\t(effects (font (size 1 1) (thickness 0.16)))",
                "\t)",
                f'\t(property "Value" "{name}"',
                f"\t\t(at 0 {span + silk + 1:.2f} 0)",
                '\t\t(layer "F.Fab")',
                "\t\t(effects (font (size 1 1) (thickness 0.16)))",
                "\t)",
                "\t(fp_line",
                f"\t\t(start {-silk:.2f} {-silk:.2f})",
                f"\t\t(end {silk:.2f} {-silk:.2f})",
                "\t\t(stroke (width 0.16) (type solid))",
                '\t\t(layer "F.SilkS")',
                "\t)",
                "\t(fp_line",
                f"\t\t(start {-silk:.2f} {span + silk:.2f})",
                f"\t\t(end {silk:.2f} {span + silk:.2f})",
                "\t\t(stroke (width 0.16) (type solid))",
                '\t\t(layer "F.SilkS")',
                "\t)",
                *pads,
                ")",
                "",
            ]
        )
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)


def tune():
    """Troca o que o encapsulamento SMT não carrega igual à lista through-hole."""
    g = _g
    for part in g.parts:
        ref = part["ref"]
        if ref.startswith("Q"):
            part["fp"] = g.FP_TO92
            part["swap_gs"] = True
            if ref == "Q7":
                part["val"] = "MMBF5457"
            else:
                part["val"] = "MMBFJ201"
        elif ref in ("D6", "D7"):
            part["fp"] = FP_GE
            part["val"] = "MP20"
        elif ref == "D1":
            part["fp"] = "Diode_SMD:D_SMA"
            part["val"] = "SS14"
        elif ref in ("D2", "D3", "D4", "D5"):
            part["val"] = "1N4148WS"
        elif ref == "U4":
            part["val"] = "ICL7660"
        elif ref in ("C4", "C5"):
            part["fp"] = FP_0603
        elif ref.startswith("C") and ref[1:].isdigit() and 64 <= int(ref[1:]) <= 71:
            # 47 µ / 16 V não existe em 0805 Basic que aguente 9 V.
            part["val"] = "22µ"
            part["sym"] = "Device:C"
            part["fp"] = g.FP_C
        elif part["sym"] == "Device:C_Polarized":
            part["sym"] = "Device:C"
            part["fp"] = g.FP_C

        if ref in CHIP:
            part["lcsc"], part["pkg"], part["val"] = CHIP[ref]
        elif part["sym"] in ("Device:R", "Device:C") and not ref.startswith("J"):
            code = PASSIVE.get(_key(part["val"]))
            if code is None:
                raise SystemExit(f"{ref} valor {part['val']!r} sem LCSC")
            part["lcsc"] = code
            part["pkg"] = "0603" if part["fp"] == FP_0603 else "0805"
        elif ref.startswith("Q") and ref != "Q7":
            part["lcsc"] = "C891687"
            part["pkg"] = "SOT-23"
        elif ref.startswith("J"):
            count = int(part["fp"].split("1x")[1][:2])
            part["fp"] = f"VOZ9_Wire:WirePin_1x{count:02d}_P3.96mm_D1.6mm"
            part["val"] = f"fio {count}"


def _pin_count(part):
    return int(part["fp"].split("1x")[1][:2])


def _place_row(refs, y, x_left, gap):
    """Fileira horizontal. Pino 1 à esquerda. `gap` é o vão entre o último pino de um grupo e o primeiro do próximo."""
    g = _g
    by_ref = {part["ref"]: part for part in g.parts}
    groups = [(by_ref[ref], _pin_count(by_ref[ref])) for ref in refs]
    if gap < PIN_PAD + 0.3:
        raise SystemExit(f"vão {gap:.1f} mm pequeno demais na fileira y={y:.0f}")
    x = x_left
    for part, count in groups:
        part["x"] = x
        part["y"] = y
        part["rot"] = 90
        g.notes.append((part["ref"], x + (count - 1) * PIN_PITCH / 2, y - 3.4))
        x += (count - 1) * PIN_PITCH + gap


def _place_column(refs, x, y_top, gap_between, label_dx):
    """Fileira vertical na lateral. Pino 1 em cima."""
    g = _g
    by_ref = {part["ref"]: part for part in g.parts}
    y = y_top
    for ref in refs:
        part = by_ref[ref]
        count = _pin_count(part)
        part["x"] = x
        part["y"] = y
        part["rot"] = 0
        g.notes.append((part["ref"], x + label_dx, y + (count - 1) * PIN_PITCH / 2))
        y += (count - 1) * PIN_PITCH + gap_between


def place_pins():
    """Duas fileiras na borda de baixo. A terceira vai na lateral direita, no vão livre."""
    g = _g
    # J1–J3 mais afastados. J4–J5 juntos, para a lateral direita ficar livre.
    _place_row(["J1", "J3"], g.H - 10.0, 9.0, 10.0)
    _place_row(["J4", "J5"], g.H - 18.0, 9.0, 6.0)
    _place_column(["J2", "J6"], 176.0, 9.0, 5.0, -4.0)
    _place_column(["J7", "J8"], 183.5, 9.0, 5.0, -3.4)
    _place_column(["J9"], 190.5, 9.0, 5.0, -3.4)


def apply_rules(board):
    """Trilha fina o bastante para sair do SOIC. Via 0,6 / furo 0,3, dentro da JLCPCB."""
    settings = board.GetDesignSettings()
    settings.m_TrackMinWidth = pcbnew.FromMM(0.15)
    settings.m_MinClearance = pcbnew.FromMM(0.16)
    settings.m_ViasMinSize = pcbnew.FromMM(0.55)
    settings.m_ViasMinDrill = pcbnew.FromMM(0.25)
    settings.m_MinThroughDrill = pcbnew.FromMM(0.25)
    net = settings.m_NetSettings.GetDefaultNetclass()
    net.SetTrackWidth(pcbnew.FromMM(0.2))
    net.SetClearance(pcbnew.FromMM(0.16))
    net.SetViaDiameter(pcbnew.FromMM(0.6))
    net.SetViaDrill(pcbnew.FromMM(0.3))


def write_bom(path):
    g = _g
    rows = {}
    missing = []
    for part in g.parts:
        if not part.get("lcsc"):
            if part["ref"].startswith(("J", "H")) or part["ref"] in ("D6", "D7"):
                continue
            if part["bom"]:
                missing.append(part["ref"])
            continue
        bucket = rows.setdefault(
            part["lcsc"],
            {"comment": part["val"], "pkg": part["pkg"], "refs": []},
        )
        bucket["refs"].append(part["ref"])
    if missing:
        raise SystemExit(f"SMT sem LCSC: {missing}")
    order = sorted(rows, key=lambda code: rows[code]["refs"][0])
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
        for code in order:
            item = rows[code]
            refs = " ".join(sorted(item["refs"], key=lambda ref: (ref[0], int(ref[1:]) if ref[1:].isdigit() else 0)))
            writer.writerow([item["comment"], refs, item["pkg"], code])
    stuffed = sum(len(item["refs"]) for item in rows.values())
    print(f"bom {path}  linhas={len(rows)}  peças montadas={stuffed}")
