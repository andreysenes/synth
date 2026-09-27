#!/usr/bin/env python3
"""Gera o zip que o JLCDFM (jlcdfm.com) e a JLCPCB aceitam.

Camadas no formato Protel, furação Excellon em milímetros, PTH e NPTH
separados. O arquivo sai em jlcdfm/voz-9-jlcdfm.zip.
"""

import os
import subprocess
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


def main():
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
        if name != os.path.basename(ZIP) and os.path.isfile(os.path.join(OUT, name))
    )
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(os.path.join(OUT, name), name)
    print(f"zip {ZIP}  {os.path.getsize(ZIP)} bytes  {len(names)} arquivos")
    for name in names:
        print(" ", name)


if __name__ == "__main__":
    main()
