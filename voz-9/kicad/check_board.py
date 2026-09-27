#!/usr/bin/env python3
"""Confere a BASE: cada pino na net certa, cobre ligado, DRC limpo.

A netlist de route.py é a ligação do circuito. A placa tem de repetir
essa lista, o cobre tem de fechar cada net, e o DRC não pode acusar erro.
"""

import os
import re
import subprocess
import tempfile

import pcbnew

import gen_kicad
import route
import silk

BOARD = route.BOARD

# Pino do símbolo KiCad -> nome. Se a biblioteca mudar o número, o teste para.
SYMBOL_PINS = {
    "Device:D": {"1": "K", "2": "A"},
    "Device:Q_NJFET_DGS": {"1": "D", "2": "G", "3": "S"},
    "Regulator_Linear:LM7805_TO220": {"1": "VI", "2": "GND", "3": "VO"},
    "Regulator_SwitchedCapacitor:MAX1044": {
        "1": "NC",
        "2": "CAP+",
        "3": "GND",
        "4": "CAP-",
        "5": "VOUT",
        "6": "LV",
        "7": "OSC",
        "8": "V+",
    },
    "Amplifier_Operational:LM2904": {
        "1": "",
        "2": "-",
        "3": "+",
        "4": "V-",
        "5": "+",
        "6": "-",
        "7": "",
        "8": "V+",
    },
    "Audio:PT2399": {
        "1": "VCC",
        "2": "REF",
        "3": "AGND",
        "4": "DGND",
        "5": "CLK_O",
        "6": "VCO",
        "7": "CC1",
        "8": "CC0",
        "16": "LPF1-IN",
        "15": "LPF1-OUT",
        "14": "LPF2-OUT",
    },
}

# Ligações que não podem mudar de net sem o circuito mudar junto.
REQUIRED = {
    ("D1", "1"): "V9",       # cátodo para o trilho
    ("D1", "2"): "P4_TIP",   # ânodo no jack
    ("U5", "1"): "V9",
    ("U5", "2"): "GND",
    ("U5", "3"): "V5",
    ("U4", "8"): "V9",
    ("U4", "3"): "GND",
    ("U4", "5"): "VEE",
    ("U4", "2"): "U4_CAP+",
    ("U4", "4"): "U4_CAP-",
    ("U1", "8"): "V9",
    ("U1", "4"): "VEE",
    ("U3", "8"): "V9",
    ("U3", "4"): "VEE",
    ("U9", "8"): "V9",
    ("U9", "4"): "VEE",
    ("U9", "5"): "GND",
    ("U9", "3"): "EQ_IN",
    ("U9", "1"): "EQ_BUF",
    ("U9", "2"): "EQ_BUF",
    ("U9", "6"): "EQ_SUM",
    ("U9", "7"): "EQ_B",
    ("J9", "1"): "EQ_BUF",
    ("J9", "3"): "EQ_B",
    ("J9", "4"): "MIDF_W",
    ("J9", "5"): "MIDF_W",
    ("J9", "6"): "MIDF_CW",
    ("R86", "2"): "EQ_SUM",
    ("C72", "2"): "EQ_OUT",
    ("J1", "5"): "GND",
    ("J1", "7"): "SUM",
    ("J1", "8"): "GND",
    ("J1", "10"): "EQ_OUT",
    ("J2", "4"): "GND",
    ("J2", "6"): "LFO_OUT",
    ("J6", "5"): "N1V8",
    ("J6", "6"): "GATE",
    ("D2", "2"): "GATE",
    ("D2", "1"): "ENV",
    ("D5", "1"): "V9",
    ("D5", "2"): "CLK_TIP",
    ("R71", "1"): "WET",
    ("R71", "2"): "WET_W",
    ("U2", "8"): "V9",
    ("U2", "4"): "GND",
    ("U6", "1"): "V5",
    ("U7", "1"): "V5",
    ("U8", "1"): "V5",
    ("U6", "3"): "GND",
    ("U6", "4"): "GND",
    ("D6", "1"): "GND",
    ("D6", "2"): "SHAPE",
    ("D7", "1"): "GND",
    ("D7", "2"): "WET",
    ("Q3", "1"): "NOISE_D",
    ("Q3", "2"): "Q3G",
    ("Q3", "3"): "NOISE_S",
}


def fail(errors):
    for item in errors:
        print(item)
    raise SystemExit(f"{len(errors)} erro(s)")


def symbol_pin_names(lib_id):
    lib, name = lib_id.split(":", 1)
    path = f"/usr/share/kicad/symbols/{lib}.kicad_sym"
    text = open(path, encoding="utf-8").read()
    found = {}
    for match in re.finditer(
        rf'\(symbol "{re.escape(name)}_(\d+)_1"',
        text,
    ):
        start = match.start()
        nxt = text.find("(symbol ", start + 10)
        body = text[start:nxt if nxt > 0 else start + 4000]
        for pin in re.finditer(
            r'\(name "([^"]*)"[\s\S]*?\(number "([^"]+)"',
            body,
        ):
            found[pin.group(2)] = pin.group(1)
    if not found:
        raise SystemExit(f"símbolo sem pinos: {lib_id}")
    return found


def expected_nets():
    raw = route.build_nets()
    errors = []
    seen = {}
    for name, pins in raw.items():
        if not pins:
            errors.append(f"net vazia: {name}")
        for pin in pins:
            if pin in route.OPEN:
                errors.append(f"{pin[0]}.{pin[1]} está aberto e na net {name}")
            if pin in seen:
                errors.append(
                    f"{pin[0]}.{pin[1]} em duas nets: {seen[pin]} e {name}"
                )
            else:
                seen[pin] = name
    merged = route.collapse_aliases(raw)
    for name, pins in merged.items():
        if len(pins) < 2:
            errors.append(f"net com menos de 2 pinos: {name} {pins}")
    if errors:
        fail(errors)
    expect = {}
    for name, pins in merged.items():
        for pin in pins:
            expect[pin] = name
    return expect


def check_symbols():
    errors = []
    for lib_id, pins in SYMBOL_PINS.items():
        found = symbol_pin_names(lib_id)
        for number, name in pins.items():
            if found.get(number) != name:
                errors.append(
                    f"{lib_id} pino {number}: biblioteca={found.get(number)!r} esperado={name!r}"
                )
    return errors


def check_required(expect):
    errors = []
    for pin, net in REQUIRED.items():
        got = expect.get(pin)
        if got != net:
            errors.append(f"netlist {pin[0]}.{pin[1]} = {got!r}, circuito pede {net}")
    return errors


def check_parts(board):
    if not gen_kicad.parts:
        gen_kicad.build_parts()
    errors = []
    wanted = {part["ref"]: part for part in gen_kicad.parts}
    present = {fp.GetReference(): fp for fp in board.GetFootprints()}
    for ref in sorted(set(wanted) - set(present)):
        errors.append(f"peça ausente na placa: {ref}")
    for ref in sorted(set(present) - set(wanted)):
        errors.append(f"peça a mais na placa: {ref}")
    for ref, part in wanted.items():
        fp = present.get(ref)
        if fp is None:
            continue
        if fp.GetValue() != part["val"]:
            errors.append(f"{ref} valor {fp.GetValue()!r} != {part['val']!r}")
    return errors


def check_pads(board, expect):
    errors = []
    board_net = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref.startswith("H"):
            for pad in fp.Pads():
                if pad.GetAttribute() != pcbnew.PAD_ATTRIB_NPTH:
                    errors.append(f"{ref} furo de fixação com cobre")
                if pad.GetNetname():
                    errors.append(f"{ref} furo de fixação na net {pad.GetNetname()}")
            continue
        for pad in fp.Pads():
            pin = pad.GetNumber()
            key = (ref, pin)
            got = pad.GetNetname() or ""
            board_net[key] = got
            if key in route.OPEN:
                if got:
                    errors.append(f"{ref}.{pin} devia ficar aberto e está em {got}")
                continue
            if key not in expect:
                errors.append(f"{ref}.{pin} sem regra na netlist (placa={got or 'aberto'})")
                continue
            if not got:
                errors.append(f"{ref}.{pin} sem net na placa; devia ser {expect[key]}")
    for key, net in expect.items():
        if key not in board_net:
            errors.append(f"{key[0]}.{key[1]} da net {net} não está na placa")
    by_board = {}
    for key, got in board_net.items():
        if not got or key in route.OPEN:
            continue
        by_board.setdefault(got, set()).add(expect.get(key))
    for got, roots in sorted(by_board.items()):
        roots.discard(None)
        if len(roots) > 1:
            errors.append(f"placa junta nets diferentes em {got}: {sorted(roots)}")
    by_root = {}
    for key, net in expect.items():
        got = board_net.get(key, "")
        by_root.setdefault(net, set()).add(got)
    for net, names in sorted(by_root.items()):
        names.discard("")
        if len(names) > 1:
            errors.append(f"net {net} partida na placa: {sorted(names)}")
    return errors


def check_two_pin(expect):
    """Resistor, capacitor e diodo não podem ter os dois pinos na mesma net."""
    errors = []
    if not gen_kicad.parts:
        gen_kicad.build_parts()
    for part in gen_kicad.parts:
        if part["sym"] not in ("Device:R", "Device:C", "Device:C_Polarized", "Device:D"):
            continue
        pins = [("1", expect.get((part["ref"], "1"))), ("2", expect.get((part["ref"], "2")))]
        if (part["ref"], "1") in route.OPEN and (part["ref"], "2") in route.OPEN:
            continue
        nets = {net for _, net in pins}
        if len(nets) < 2 or None in nets:
            errors.append(f"{part['ref']} não liga dois nós: {pins}")
    return errors


def check_copper(board):
    errors = []
    board.BuildConnectivity()
    missing = board.GetConnectivity().GetUnconnectedCount(False)
    if missing:
        errors.append(f"ratsnest: {missing} ligações sem cobre")
    gnd_filled = False
    for zone in board.Zones():
        if zone.GetNetname() != "GND":
            continue
        if zone.GetLayer() != pcbnew.B_Cu:
            continue
        if zone.GetFilledPolysList(pcbnew.B_Cu).TotalVertices() > 0:
            gnd_filled = True
    if not gnd_filled:
        errors.append("plano de GND no verso sem preenchimento")
    return errors


def check_drc(path):
    report = tempfile.NamedTemporaryFile(suffix=".rpt", delete=False)
    report.close()
    subprocess.run(
        ["kicad-cli", "pcb", "drc", "--severity-error", "-o", report.name, path],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    text = open(report.name, encoding="utf-8", errors="replace").read()
    os.unlink(report.name)
    errors = []
    for label in ("DRC violations", "unconnected pads", "Footprint errors"):
        match = re.search(rf"Found (\d+) {label}", text)
        count = int(match.group(1)) if match else -1
        if count != 0:
            errors.append(f"DRC {label}: {count}")
    if errors:
        # O resumo numérico não diz qual trilha. Guarda o miolo do relatório.
        body = "\n".join(
            line
            for line in text.splitlines()
            if line.startswith("[") or line.startswith("    @")
        )
        errors.append(body)
    return errors


def main():
    expect = expected_nets()
    board = pcbnew.LoadBoard(BOARD)
    errors = []
    errors += check_symbols()
    errors += check_required(expect)
    errors += check_parts(board)
    errors += check_pads(board, expect)
    errors += check_two_pin(expect)
    errors += check_copper(board)
    errors += silk.check(board)
    errors += check_drc(BOARD)
    if errors:
        fail(errors)
    parts = len({fp.GetReference() for fp in board.GetFootprints()})
    print(
        f"ok  peças={parts}  pinos={len(expect)}  "
        f"nets={len(set(expect.values()))}  ratsnest=0  drc=0"
    )


if __name__ == "__main__":
    main()
