#!/usr/bin/env python3
"""Gera o zip que o JLCDFM (jlcdfm.com) e a JLCPCB aceitam.

Camadas no formato Protel, furação Excellon em milímetros, PTH e NPTH
separados. O arquivo sai em jlcdfm/voz-9-jlcdfm.zip.
"""

import csv
import os
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(ROOT, "voz-9.kicad_pcb")
OUT = os.path.join(ROOT, "jlcdfm")
ZIP = os.path.join(OUT, "voz-9-jlcdfm.zip")

LAYERS = ",".join(
    [
        "F.Cu",
        "B.Cu",
        "F.Paste",
        "B.Paste",
        "F.Silkscreen",
        "B.Silkscreen",
        "F.Mask",
        "B.Mask",
        "Edge.Cuts",
    ]
)


def run(args):
    proc = subprocess.run(args, check=False, text=True, capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout or f"falhou: {args[0]}")
    if proc.stdout.strip():
        print(proc.stdout.strip())


def use_v2():
    global BOARD, OUT, ZIP
    v2 = os.path.join(os.path.dirname(ROOT), "kicad-v2")
    BOARD = os.path.join(v2, "voz-9.kicad_pcb")
    OUT = os.path.join(v2, "jlcdfm")
    ZIP = os.path.join(OUT, "voz-9-v2-jlcdfm.zip")


def write_cpl(dest):
    """Centroid no mesmo eixo do gerber: Y já sai negativo do kicad-cli."""
    raw = dest + ".kicad.tmp"
    run(
        [
            "kicad-cli",
            "pcb",
            "export",
            "pos",
            "--format",
            "csv",
            "--units",
            "mm",
            "--side",
            "front",
            "--smd-only",
            "--exclude-dnp",
            "--output",
            raw,
            BOARD,
        ]
    )
    with open(raw, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    os.remove(raw)
    with open(dest, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
        for row in rows:
            writer.writerow(
                [
                    row["Ref"],
                    f"{float(row['PosX']):.4f}",
                    f"{float(row['PosY']):.4f}",
                    "Top",
                    f"{float(row['Rot']):.0f}",
                ]
            )
    print(f"cpl {dest}  peças={len(rows)}")


def readme_text():
    if "kicad-v2" in BOARD:
        return [
            "VOZ-9 v2 SMT",
            "Gerbers for the 200 x 100 mm board. Upload bom.csv and cpl.csv alongside this zip",
            "and turn PCB Assembly on. J1-J9 are 1.6 mm wire holes (solder the cable",
            "straight in, including an XLR conductor) and D6/D7 (MP20) are not in those",
            "files: solder them by hand.",
            "",
            "Layers: 2",
            "Size: 200 mm x 100 mm",
            "Thickness: 1.6 mm",
            "Material: FR-4",
            "Outer copper: 1 oz",
            "Solder mask: green, both sides",
            "Silkscreen: white, both sides",
            "Surface finish: lead-free HASL",
            "Via covering: tented",
            "Impedance control: no",
            "Gold fingers: no",
            "Castellated holes: no",
            "",
            "Outline: voz-9-Edge_Cuts.gm1",
            "Drills: Excellon, millimeters, absolute, decimal zeros",
            "PTH: voz-9-PTH.drl (1.6 mm wire holes and two axial diodes)",
            "NPTH: voz-9-NPTH.drl (four M3 mounting holes, 3.2 mm, no copper)",
            "",
            "Remove the JLCPCB order number, or place it on the bottom, away from the wire holes.",
            "",
        ]
    return [
            "VOZ-9 BASE",
            "Order this as a bare PCB. Parts are through-hole and are not assembled by JLCPCB.",
            "",
            "Layers: 2",
            "Size: 300 mm x 140 mm",
            "Thickness: 1.6 mm",
            "Material: FR-4",
            "Outer copper: 1 oz",
            "Solder mask: green, both sides",
            "Silkscreen: white, both sides",
            "Surface finish: lead-free HASL",
            "Via covering: tented",
            "Impedance control: no",
            "Gold fingers: no",
            "Castellated holes: no",
            "",
            "Outline: voz-9-Edge_Cuts.gm1",
            "Drills: Excellon, millimeters, absolute, decimal zeros",
            "PTH: voz-9-PTH.drl",
            "NPTH: voz-9-NPTH.drl (four M3 mounting holes, 3.2 mm, no copper)",
            "",
            "Remove the JLCPCB order number, or place it on the bottom, away from the pin headers.",
            "",
        ]


def main():
    if "--v2" in sys.argv:
        use_v2()
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(OUT):
        if name in (os.path.basename(ZIP), ".gitignore"):
            continue
        os.remove(os.path.join(OUT, name))
    run(
        [
            "kicad-cli",
            "pcb",
            "export",
            "gerbers",
            "--output",
            OUT,
            "--layers",
            LAYERS,
            "--subtract-soldermask",
            "--check-zones",
            BOARD,
        ]
    )
    run(
        [
            "kicad-cli",
            "pcb",
            "export",
            "drill",
            "--output",
            OUT,
            "--format",
            "excellon",
            "--drill-origin",
            "absolute",
            "--excellon-units",
            "mm",
            "--excellon-zeros-format",
            "decimal",
            "--excellon-oval-format",
            "alternate",
            "--excellon-separate-th",
            BOARD,
        ]
    )
    names = sorted(
        name
        for name in os.listdir(OUT)
        if name not in (os.path.basename(ZIP), ".gitignore")
        and os.path.isfile(os.path.join(OUT, name))
    )
    readme = os.path.join(OUT, "readme-jlcpcb.txt")
    with open(readme, "w", encoding="utf-8") as fh:
        fh.write("\n".join(readme_text()))
    if "kicad-v2" in BOARD:
        write_cpl(os.path.join(os.path.dirname(BOARD), "cpl.csv"))
    names.append("readme-jlcpcb.txt")
    names.sort()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(os.path.join(OUT, name), name)
    print(f"zip {ZIP}  {os.path.getsize(ZIP)} bytes  {len(names)} arquivos")
    for name in names:
        print(" ", name)


if __name__ == "__main__":
    main()
