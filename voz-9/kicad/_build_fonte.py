#!/usr/bin/env python3
"""Preenche voz-9/kicad/01-fonte.kicad_sch via Konnect MCP."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

SCH = Path("/workspace/voz-9/kicad/01-fonte.kicad_sch")
BACKUP = Path("/workspace/voz-9/kicad/01-fonte.kicad_sch.bak")

spec = importlib.util.spec_from_file_location("kc", "/workspace/tools/konnect_client.py")
kc = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(kc)


def main() -> None:
    shutil.copy2(SCH, BACKUP)
    k = kc.Konnect()
    for ts in ["sch_components", "sch_wiring", "sch_batch", "sch_export", "sch_analysis"]:
        k.tool("load_toolset", {"name": ts})

    sch = str(SCH)

    # Página A3 paisagem
    print("page", k.tool("set_schematic_page", {"schematic": sch, "size": "A3", "portrait": False}))

    # Remover texto/esqueleto anterior: recria arquivo limpo e restaura só o essencial
    # create_schematic sobrescreve — usamos create + set page
    print("create", k.tool("create_schematic", {"path": sch, "size": "A3", "portrait": False}))

    # Anotações de escopo
    notes = [
        (20.32, 12.70, "VOZ-9 / Fonte — esquema.md §0 · DEC-038"),
        (20.32, 15.24, "P4 centro-negativo no painel → D1 → V9. V5 so para PT2399. 4V5/1V8 NUNCA em GND."),
        (20.32, 17.78, "U4: simbolo LMC7660 (pinout ICL7660). BOM: MAX1044/ICL7660 — validar pinos na amostra."),
    ]
    for x, y, text in notes:
        print("text", k.tool("add_schematic_text", {"schematic": sch, "x": x, "y": y, "text": text}))

    # Componentes principais (posições em mm, grade 1.27)
    comps = [
        # Entrada / proteção
        {"lib_id": "Diode:1N5817", "reference": "D1", "value": "1N5817", "x": 50.80, "y": 50.80, "rotation": 0},
        # Bulk V9
        {"lib_id": "Device:C_Polarized", "reference": "C1", "value": "47u/25V", "x": 76.20, "y": 63.50, "rotation": 0},
        # LED piloto
        {"lib_id": "Device:R", "reference": "R1", "value": "4k7", "x": 88.90, "y": 40.64, "rotation": 0},
        {"lib_id": "Device:LED", "reference": "D2", "value": "LED red 3mm", "x": 101.60, "y": 40.64, "rotation": 0},
        # Regulador 5 V
        {"lib_id": "Regulator_Linear:LM78M05_TO220", "reference": "U5", "value": "78M05", "x": 127.00, "y": 50.80, "rotation": 0},
        {"lib_id": "Device:C_Polarized", "reference": "C2", "value": "10u", "x": 152.40, "y": 63.50, "rotation": 0},
        {"lib_id": "Device:C", "reference": "C3", "value": "100n", "x": 162.56, "y": 63.50, "rotation": 0},
        # Charge pump
        {"lib_id": "Regulator_SwitchedCapacitor:LMC7660", "reference": "U4", "value": "MAX1044", "x": 203.20, "y": 50.80, "rotation": 0},
        {"lib_id": "Device:C_Polarized", "reference": "C4", "value": "10u", "x": 228.60, "y": 40.64, "rotation": 90},  # CAP+ to CAP-
        {"lib_id": "Device:C_Polarized", "reference": "C5", "value": "10u", "x": 228.60, "y": 63.50, "rotation": 0},  # CAP- to VEE? fly for MAX style — use between CAP- and VOUT later
        {"lib_id": "Device:C_Polarized", "reference": "C6", "value": "47u", "x": 241.30, "y": 76.20, "rotation": 0},  # VEE bulk
        # Divisor 4V5
        {"lib_id": "Device:R", "reference": "R2", "value": "10k", "x": 279.40, "y": 40.64, "rotation": 0},
        {"lib_id": "Device:R", "reference": "R3", "value": "10k", "x": 279.40, "y": 63.50, "rotation": 0},
        {"lib_id": "Device:C_Polarized", "reference": "C7", "value": "47u", "x": 294.64, "y": 55.88, "rotation": 0},
        # Divisor 1V8 (aprox — valores finais no esquema/bias JFET)
        {"lib_id": "Device:R", "reference": "R4", "value": "TODO", "x": 330.20, "y": 40.64, "rotation": 0},
        {"lib_id": "Device:R", "reference": "R5", "value": "TODO", "x": 330.20, "y": 63.50, "rotation": 0},
        {"lib_id": "Device:C_Polarized", "reference": "C8", "value": "TODO", "x": 345.44, "y": 55.88, "rotation": 0},
    ]
    print("place", json.dumps(k.tool("batch_place_components", {"schematic": sch, "components": comps}), indent=2)[:2000])

    # Power symbols
    powers = [
        ("GND", 76.20, 88.90, 0),
        ("GND", 152.40, 88.90, 0),
        ("GND", 203.20, 88.90, 0),
        ("GND", 241.30, 88.90, 0),
        ("GND", 279.40, 88.90, 0),
        ("GND", 330.20, 88.90, 0),
        ("V9", 76.20, 27.94, 0),
        ("V5", 152.40, 27.94, 0),
        ("VEE", 241.30, 27.94, 0),
        ("4V5", 294.64, 27.94, 0),
        ("1V8", 345.44, 27.94, 0),
    ]
    for net, x, y, rot in powers:
        print("pwr", net, k.tool("add_power_symbol", {"schematic": sch, "power_net": net, "x": x, "y": y, "rotation": rot}))

    # Entrada tip (label)
    print("in", k.tool("add_schematic_net_label", {
        "schematic": sch, "net": "P4_TIP", "x": 33.02, "y": 50.80,
        "label_type": "global_label", "shape": "input", "rotation": 0,
    }))

    # Listar e conectar pins principais via pin locations
    pins = k.tool("batch_get_schematic_pin_locations", {
        "schematic": sch,
        "references": ["D1", "C1", "R1", "D2", "U5", "C2", "C3", "U4", "C4", "C5", "C6", "R2", "R3", "C7", "R4", "R5", "C8"],
    })
    print("pins keys", list(pins.keys()) if isinstance(pins, dict) else type(pins))
    Path("/tmp/fonte_pins.json").write_text(json.dumps(pins, indent=2))

    # Conexões principais por connect_pins / wires — usar connect_to_net com labels
    # D1 cathode side to V9 rail, anode to P4_TIP
    # We'll wire after inspecting pin file
    k.close()
    print("PINDUMP /tmp/fonte_pins.json")


if __name__ == "__main__":
    main()
