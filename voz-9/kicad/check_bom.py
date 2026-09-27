#!/usr/bin/env python3
"""Confere a lista de compras e o CSV da JLCPCB contra as peças da BASE.

A placa é a fonte. `bom.md` é a compra de rua (THT + painel). `jlcpcb-bom.csv`
é o equivalente SMT: cada designator dali tem de existir na placa. Germânio,
trimpot e pinos não entram no CSV. Os dois J201 de folga e o LED ficam só
na lista de rua.
"""

import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
VOZ = os.path.dirname(ROOT)
sys.path.insert(0, ROOT)

import gen_kicad

BOM = os.path.join(VOZ, "bom.md")
CSV = os.path.join(VOZ, "jlcpcb-bom.csv")

# Na placa, mas sem código LCSC. Compram-se pela bom.md.
OFF_CSV = {"D6", "D7", "RV1", "RV2"}
# Compra a mais, de propósito, e não é referência da placa.
SPARES = {"J201": 2}


def fail(errors):
    for item in errors:
        print(item)
    raise SystemExit(f"{len(errors)} erro(s) na lista")


def norm(value):
    text = value.lower().replace("ω", "")
    text = text.replace("**", "")
    text = re.sub(r"\d+\s*%", "", text)
    text = re.split(r"\s*/\s*", text)[0]
    text = text.replace("µ", "u").replace("μ", "u")
    text = re.sub(r"\s+", "", text).replace(",", ".")
    # 4k7, 2n2, 2u2. Um dígito só, para não engolir 2N5457 nem 78M05.
    match = re.fullmatch(r"(\d+)([knu])(\d)", text)
    if match:
        text = f"{match.group(1)}.{match.group(3)}{match.group(2)}"
    return text


def board_parts():
    gen_kicad.build_parts()
    rc = {}
    others = {}
    all_parts = {}
    for part in gen_kicad.parts:
        if not part["bom"] or part["ref"].startswith("J"):
            continue
        value = norm(part["val"])
        all_parts[part["ref"]] = value
        bucket = rc if part["sym"] in ("Device:R", "Device:C", "Device:C_Polarized") else others
        bucket.setdefault(value, []).append(part["ref"])
    return rc, others, all_parts


def read_csv():
    rows = []
    with open(CSV, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            refs = row["Designator"].split()
            rows.append((row["Comment"], refs, row["LCSC Part #"].strip(), row["Footprint"].strip()))
    return rows


def md_tables(text):
    section = ""
    tables = []
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            current = None
            continue
        if not line.startswith("|"):
            current = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if set(cells[0]) <= {"-", ":"}:
            continue
        if current is None:
            current = []
            tables.append((section, current))
        current.append(cells)
    return tables


def qty_cell(section, cells):
    if section.startswith("Resistor"):
        return cells[0], cells[1]
    if section.startswith("Capacitor"):
        return cells[0], cells[2]
    return None, None


def check_csv(all_parts):
    errors = []
    seen = {}
    for comment, refs, lcsc, footprint in read_csv():
        if not re.fullmatch(r"C\d+", lcsc):
            errors.append(f"CSV {comment}: LCSC {lcsc!r} não é um C-number")
        if not footprint:
            errors.append(f"CSV {comment}: footprint vazio")
        for ref in refs:
            if ref in seen:
                errors.append(f"CSV {ref} repetido em {comment!r} e {seen[ref]!r}")
            seen[ref] = comment
    on_board = all_parts
    for ref in sorted(set(seen) - set(on_board)):
        errors.append(f"CSV {ref} não está na placa")
    missing = []
    for ref, value in sorted(on_board.items()):
        if ref in OFF_CSV or ref.startswith("J"):
            continue
        if ref not in seen:
            missing.append(f"{ref} {value}")
    if missing:
        errors.append("na placa e fora do CSV: " + ", ".join(missing))
    by_comment = {}
    for ref, comment in seen.items():
        by_comment.setdefault(comment, set()).add(on_board.get(ref))
    for comment, values in by_comment.items():
        values.discard(None)
        if len(values) > 1:
            errors.append(f"CSV {comment!r} mistura valores {sorted(values)}")
    # 47 µ da placa mora na linha de 22 µ / 25 V.
    forty = {ref for ref, value in all_parts.items() if value == "47u"}
    if forty:
        owners = {seen.get(ref) for ref in forty}
        if len(owners) != 1 or not owners.pop() or "22uf" not in norm(next(iter({seen[ref] for ref in forty}))):
            line = next(iter({seen.get(ref) for ref in forty}))
            if line is None or "22u" not in line.lower().replace("µ", "u"):
                errors.append(f"47 µ da placa fora da linha 22 µ / 25 V: {line!r}")
    return errors


def check_street(rc, others, text):
    errors = []
    summed = {}
    for section, rows in md_tables(text):
        if not (section.startswith("Resistor") or section.startswith("Capacitor")):
            continue
        for cells in rows[1:]:
            label, raw = qty_cell(section, cells)
            if label is None or not raw.isdigit():
                continue
            key = norm(label)
            summed[key] = summed.get(key, 0) + int(raw)
    for value, refs in rc.items():
        if value not in summed:
            errors.append(f"bom.md sem quantidade de {value} ({len(refs)} na placa)")
            continue
        if summed[value] != len(refs):
            errors.append(
                f"bom.md {value}: lista {summed[value]}, placa {len(refs)}"
            )
    for value, qty in summed.items():
        if value not in rc:
            errors.append(f"bom.md lista {qty}× {value} e a placa não tem")
    # Semicondutores: a quantidade da lista é a da placa, mais a folga declarada.
    wanted = {
        "J201": len(others.get("j201", [])) + SPARES["J201"],
        "MP20": len(others.get("mp20", [])),
        "2N5457": len(others.get("2n5457", [])),
        "PT2399": len(others.get("pt2399", [])),
        "78M05": len(others.get("78m05", [])),
        "MAX1044": len(others.get("max1044", [])),
        "NE5532": len(others.get("ne5532", [])),
        "1N5817": len(others.get("1n5817", [])),
        "1N4148": len(others.get("1n4148", [])),
        "TL072": len(others.get("tl072", [])),
    }
    found = {key: 0 for key in wanted}
    for section, rows in md_tables(text):
        if not section.startswith("Semicond"):
            continue
        for cells in rows[1:]:
            if not cells[0].isdigit():
                continue
            piece = cells[1]
            for key in wanted:
                if key in piece:
                    found[key] += int(cells[0])
    for key, qty in wanted.items():
        if found[key] != qty:
            errors.append(f"bom.md {key}: lista {found[key]}, esperado {qty}")
    return errors


def check_panel(text):
    errors = []
    expect = {
        "Potenciômetro": 17,
        "Chaves": 9,
        "Knobs": 17,
    }
    for section, rows in md_tables(text):
        for title, total in expect.items():
            if not section.startswith(title):
                continue
            qty = 0
            for cells in rows[1:]:
                if not cells[0].isdigit():
                    continue
                if "trimpot" in cells[1].lower() or "botão" in cells[1].lower():
                    continue
                qty += int(cells[0])
            if qty != total:
                errors.append(f"bom.md {title}: {qty}, o painel pede {total}")
    if "piso ≥ 300×140" not in text:
        errors.append("bom.md: a caixa não está em 300×140 mm")
    if "124 pinos" not in text:
        errors.append("bom.md: J1–J9 não somam 124 pinos")
    return errors


def main():
    rc, others, all_parts = board_parts()
    text = open(BOM, encoding="utf-8").read()
    errors = []
    errors += check_csv(all_parts)
    errors += check_street(rc, others, text)
    errors += check_panel(text)
    if errors:
        fail(errors)
    print(f"ok  placa={len(all_parts)}  csv bate  bom.md bate")


if __name__ == "__main__":
    main()
