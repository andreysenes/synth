#!/usr/bin/env python3
"""Gera o esqueleto hierárquico do VOZ-9 (somente esquema, sem PCB).

Uso:
  python3 _gen_project.py

Sobrescreve a estrutura. Não rode depois que o circuito estiver preenchido
sem backup.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SHEETS = [
    ("01-fonte", "Fonte", "Alimentação 9 V, V5, VEE, 4V5, 1V8, proteção e LED piloto"),
    ("02-osc", "Osciladores", "OSC A / OSC B (metades do op-amp), enable e saídas A/B"),
    ("03-noise", "Noise", "Gerador de ruído J201"),
    ("04-mix-eq", "Mix + EQ", "PRE, OSC IN, mix, EQ voz U9 (Tascam 424)"),
    ("05-shape", "Shape", "Waveshaper assimétrico MP20"),
    ("06-vcf", "VCF", "Filtro JFET, CUTOFF e FCV"),
    ("07-vca", "VCA", "VCA, GATE, DRONE e envelope da fala"),
    ("08-lfo", "LFO", "LFO TREM/flutter, RATE, DEPTH e MODE"),
    ("09-echo", "Echo", "NAB U3 + três PT2399 (H1–H3), TIME, WET, F-BACK, STACK"),
    ("10-saida", "Saída + VU", "VOLUME, pads OUT, driver do VU analógico / J10"),
    ("11-indicadores", "Indicadores", "Drivers CLIP/GATE/LFO e LEDs OSC/H/STACK / J11"),
    ("12-conectores", "Conectores", "Headers J1–J11 na borda inferior, pinouts e bonding GND"),
]

COLS, ROWS = 4, 3
ORIGIN_X, ORIGIN_Y = 25.4, 30.48
DX, DY = 95.25, 55.88
SHEET_W, SHEET_H = 76.2, 38.1


def uid() -> str:
    return str(uuid.uuid4())


def title_block(title: str, comment: str) -> str:
    return f"""  (title_block
    (title "{title}")
    (date "2026-09-28")
    (rev "R0.1")
    (company "VOZ-9")
    (comment 1 "{comment}")
    (comment 2 "Baseline KiCad — sem PCB até validação humana do esquema")
    (comment 3 "Requisitos: ../kicad-requisitos.md · Playbook: ../kicad-layout-agent.md")
  )"""


def text_lines(x: float, y: float, lines: list[str]) -> str:
    parts: list[str] = []
    for i, line in enumerate(lines):
        escaped = line.replace("\\", "\\\\").replace('"', '\\"')
        ty = y + i * 2.54
        parts.append(
            f"""  (text "{escaped}" (at {x:.2f} {ty:.2f} 0)
    (effects (font (size 1.27 1.27)) (justify left top))
    (uuid "{uid()}")
  )"""
        )
    return "\n".join(parts)


POWER_LABELS = {
    "01-fonte": [
        ("V9", 40.64, 50.80),
        ("V5", 60.96, 50.80),
        ("VEE", 81.28, 50.80),
        ("4V5", 101.60, 50.80),
        ("1V8", 121.92, 50.80),
        ("GND", 40.64, 80.00),
    ],
}

SHEET_NOTES = {
    "01-fonte": [
        "Referencia: esquema.md §0",
        "Entrada P4 centro-negativo → 1N5817 → V9",
        "78M05 → V5 (somente PT2399); MAX1044 → VEE",
        "Divisores 4V5 e 1V8 — NUNCA amarrar a GND",
    ],
    "02-osc": [
        "Referencia: esquema.md §1",
        "Duas metades de op-amp: OSC A (grave) e OSC B (agudo)",
    ],
    "03-noise": ["Referencia: esquema.md §2", "J201 noise"],
    "04-mix-eq": [
        "Referencia: esquema.md §§3–3b",
        "PRE, OSC IN, mix e EQ voz U9",
    ],
    "05-shape": ["Referencia: esquema.md §4", "MP20 waveshaper"],
    "06-vcf": ["Referencia: esquema.md §5", "VCF JFET + CUTOFF/FCV"],
    "07-vca": ["Referencia: esquema.md §6", "VCA + GATE + DRONE + ENV"],
    "08-lfo": ["Referencia: esquema.md §7", "LFO TREM/flutter + MODE"],
    "09-echo": [
        "Referencia: esquema.md §8",
        "NAB + 3× PT2399; H1–H3; STACK; TIME/WET/F-BACK",
    ],
    "10-saida": [
        "Referencia: esquema.md saida + requisitos VU",
        "VOLUME, pads OUT, driver VU / J10",
    ],
    "11-indicadores": [
        "Referencia: requisitos LED-001..019",
        "Drivers discretos CLIP/GATE/LFO + LEDs de chave / J11",
    ],
    "12-conectores": [
        "Referencia: pcb.md pinouts J1–J9 + J10/J11",
        "Headers na borda inferior por logica do sinal; bonding GND",
    ],
}


def write_child(name: str, title: str, scope: str) -> None:
    lines = [
        f"FOLHA: {name}",
        f"ESCOPO: {scope}",
        "PADRAO VISUAL:",
        "- Fluxo de sinal da esquerda para a direita",
        "- Trilhos de alimentacao no topo; GND na base",
        "- Labels hierarquicos na borda esquerda/direita",
        "- Um bloco funcional por folha; sem misturar etapas",
        "- Referencias e valores sempre legiveis; pino 1 marcado",
        "",
        *SHEET_NOTES.get(name, []),
        "",
        "STATUS: esqueleto autorizado (DEC-038 / ACT-001).",
        "Circuito a preencher a partir de ../esquema.md.",
        "NAO criar PCB nesta revisao.",
    ]
    labels = POWER_LABELS.get(name, [("GND", 40.64, 80.00)])
    label_sexpr = "\n".join(
        f"""  (global_label "{lab}" (shape input) (at {x:.2f} {y:.2f} 0)
    (effects (font (size 1.27 1.27)) (justify left))
    (uuid "{uid()}")
  )"""
        for lab, x, y in labels
    )
    body = f"""(kicad_sch (version 20230121) (generator eeschema)

  (uuid "{uid()}")

  (paper "A3")

{title_block(f"VOZ-9 / {title}", scope)}

{text_lines(20.32, 20.32, lines)}

{label_sexpr}

)
"""
    (ROOT / f"{name}.kicad_sch").write_text(body, encoding="utf-8")


def write_root() -> None:
    sheet_blocks: list[str] = []
    for i, (name, title, _scope) in enumerate(SHEETS):
        col, row = i % COLS, i // COLS
        x = ORIGIN_X + col * DX
        y = ORIGIN_Y + row * DY
        sheet_blocks.append(
            f"""  (sheet (at {x:.2f} {y:.2f}) (size {SHEET_W:.2f} {SHEET_H:.2f})
    (stroke (width 0.1524) (type solid) (color 0 0 0 0))
    (fill (color 0 0 0 0.0000))
    (uuid "{uid()}")
    (property "Sheetname" "{title}" (id 0) (at {x:.2f} {y - 1.27:.2f} 0)
      (effects (font (size 1.524 1.524)) (justify left bottom))
    )
    (property "Sheetfile" "{name}.kicad_sch" (id 1) (at {x:.2f} {y + SHEET_H + 1.27:.2f} 0)
      (effects (font (size 1.27 1.27)) (justify left top))
    )
  )"""
        )

    intro = [
        "VOZ-9 — esquema hierarquico (sem PCB)",
        "Cada retangulo abre uma folha: fonte, osc, noise, mix-eq, shape, vcf, vca, lfo, echo, saida, indicadores, conectores.",
        "Padronizacao: A3, titulo VOZ-9 / Bloco, rev R0.1, fluxo E->D, um bloco por folha.",
        "Fonte de verdade eletrica: ../esquema.md · Requisitos: ../kicad-requisitos.md",
    ]

    root = f"""(kicad_sch (version 20230121) (generator eeschema)

  (uuid "{uid()}")

  (paper "A3")

{title_block("VOZ-9 / Indice", "Folha raiz — um bloco por arquivo hierarquico")}

{text_lines(20.32, 12.70, intro)}

{chr(10).join(sheet_blocks)}

  (sheet_instances
    (path "/" (page "1"))
  )

)
"""
    (ROOT / "voz-9.kicad_sch").write_text(root, encoding="utf-8")


def net_class(
    name: str,
    track_width: float,
    clearance: float,
    via_diameter: float = 0.6,
    via_drill: float = 0.3,
) -> dict:
    return {
        "bus_width": 12,
        "clearance": clearance,
        "diff_pair_gap": 0.25,
        "diff_pair_via_gap": 0.25,
        "diff_pair_width": 0.2,
        "line_style": 0,
        "microvia_diameter": 0.3,
        "microvia_drill": 0.1,
        "name": name,
        "pcb_color": "rgba(0, 0, 0, 0.000)",
        "schematic_color": "rgba(0, 0, 0, 0.000)",
        "track_width": track_width,
        "via_diameter": via_diameter,
        "via_drill": via_drill,
        "wire_width": 6,
    }


def write_pro() -> None:
    pro = {
        "board": {
            "design_settings": {
                "defaults": {},
                "diff_pair_dimensions": [],
                "drc_exclusions": [],
                "rules": {},
                "track_widths": [],
                "via_dimensions": [],
            }
        },
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": "voz-9.kicad_pro", "version": 1},
        "net_settings": {
            "classes": [
                net_class("Default", 0.25, 0.25),
                net_class("PWR_MAIN", 1.0, 0.25, 0.8, 0.4),
                net_class("PWR_LOCAL", 0.6, 0.25, 0.7, 0.35),
                net_class("MIC_LOW", 0.3, 0.4),
                net_class("AUDIO", 0.3, 0.25),
                net_class("TIME_CLOCK", 0.3, 0.4),
                net_class("CONTROL_HIZ", 0.3, 0.4),
            ],
            "meta": {"version": 2},
        },
        "pcbnew": {
            "last_paths": {
                "gencad": "",
                "idf": "",
                "netlist": "",
                "specctra_dsn": "",
                "spread_fritzing": "",
                "svg": "",
                "vrml": "",
            },
            "page_layout_descr_file": "",
        },
        "schematic": {
            "annotate_start_num": 0,
            "drawing": {
                "dashed_lines_dash_length_ratio": 12.0,
                "dashed_lines_gap_length_ratio": 3.0,
                "default_line_thickness": 6.0,
                "default_text_size": 50.0,
                "field_names": [],
                "intersheets_ref_own_page": False,
                "intersheets_ref_prefix": "",
                "intersheets_ref_short": False,
                "intersheets_ref_show": False,
                "intersheets_ref_suffix": "",
                "junction_size_choice": 3,
                "label_size_ratio": 0.375,
                "pin_symbol_size": 25.0,
                "text_offset_ratio": 0.15,
            },
            "legacy_lib_dir": "",
            "legacy_lib_list": [],
            "meta": {"version": 1},
            "net_format_name": "",
            "page_layout_descr_file": "",
            "plot_directory": "",
            "spice_current_sheet_as_root": False,
            "spice_external_command": 'spice "%I"',
            "spice_model_current_sheet_as_root": True,
            "spice_save_all_currents": False,
            "spice_save_all_voltages": False,
            "subsheet_field_names": [],
        },
        "sheets": [["Indice", "voz-9.kicad_sch"]]
        + [[title, f"{name}.kicad_sch"] for name, title, _ in SHEETS],
        "text_variables": {},
    }
    (ROOT / "voz-9.kicad_pro").write_text(
        json.dumps(pro, indent=2) + "\n", encoding="utf-8"
    )


def write_readme() -> None:
    rows = "\n".join(
        f"| `{name}.kicad_sch` | {title} |" for name, title, _ in SHEETS
    )
    text = f"""# VOZ-9 — projeto KiCad (somente esquema)

**Sem PCB nesta revisão.** PCB só após validação humana do esquema/netlist
(DEC-001 / DEC-038).

## Abrir

1. Abrir `voz-9.kicad_pro` no KiCad 7+.
2. Editar o esquema a partir da folha raiz (`voz-9.kicad_sch`).
3. Cada retângulo abre uma folha de bloco.

## Folhas (arquivos picados)

| Arquivo | Bloco |
| --- | --- |
| `voz-9.kicad_sch` | Índice / raiz |
{rows}

## Padronização visual

- Papel **A3**, título `VOZ-9 / <Bloco>`, revisão **R0.1**, empresa VOZ-9.
- Comentários do bloco apontam para `esquema.md`, requisitos e playbook.
- Fluxo de sinal **esquerda → direita**.
- Alimentação no topo; GND na base.
- Labels hierárquicos nas bordas esquerda/direita.
- **Um bloco funcional por folha** — não misturar etapas.
- Classes de net já definidas no `.kicad_pro` (PWR_MAIN, PWR_LOCAL, MIC_LOW,
  AUDIO, TIME_CLOCK, CONTROL_HIZ).

## Regenerar esqueleto

```bash
python3 _gen_project.py
```

Sobrescreve apenas a estrutura; não use depois que o circuito estiver
preenchido sem backup.
"""
    (ROOT / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for name, title, scope in SHEETS:
        write_child(name, title, scope)
    write_root()
    write_pro()
    write_readme()
    # Garantir ausência de PCB nesta revisão
    pcb = ROOT / "voz-9.kicad_pcb"
    if pcb.exists():
        raise SystemExit(f"PCB inesperada encontrada: {pcb}")
    print(f"Gerado em {ROOT}")
    for p in sorted(ROOT.glob("*")):
        print(f"  {p.name}")


if __name__ == "__main__":
    main()
