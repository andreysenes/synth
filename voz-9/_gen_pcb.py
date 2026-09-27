#!/usr/bin/env python3
"""Gera pcb.svg — BASE 220×160 com R1–R81 e C1–C71."""

from pathlib import Path

W, H = 220.0, 160.0
seen_r, seen_c = set(), set()
out = []


def emit(s):
    out.append(s)


def r(x, y, ref, val):
    assert ref not in seen_r, ref
    seen_r.add(ref)
    emit(
        f'  <g transform="translate({x:.1f},{y:.1f})">'
        f'<use href="#rth"/><text class="lab" y="2.55">{ref} {val}</text></g>'
    )


def cf(x, y, ref, val):
    assert ref not in seen_c, ref
    seen_c.add(ref)
    emit(
        f'  <g transform="translate({x:.1f},{y:.1f})">'
        f'<use href="#cth"/><text class="lab" y="2.65">{ref} {val}</text></g>'
    )


def ce(x, y, ref, val):
    assert ref not in seen_c, ref
    seen_c.add(ref)
    emit(
        f'  <g transform="translate({x:.1f},{y:.1f})">'
        f'<use href="#cel"/><text class="lab" y="4.0">{ref} {val}</text></g>'
    )


def blk(x, y, w, h, title):
    emit(f'  <rect class="blk" x="{x}" y="{y}" width="{w}" height="{h}"/>')
    emit(f'  <text class="silk-s" x="{x + 1.5}" y="{y + 2.5}" style="text-anchor:start">{title}</text>')


def dip8(x, y, name):
    emit(f'  <g transform="translate({x},{y})"><use href="#dip8"/><text class="lab" y="8.5">{name}</text></g>')


def dip16(x, y, name):
    emit(f'  <g transform="translate({x},{y})"><use href="#dip16"/><text class="lab" y="14">{name}</text></g>')


def to92(x, y, name):
    emit(f'  <g transform="translate({x},{y})"><use href="#to92"/><text class="lab" y="4.5">{name}</text></g>')


def trim(x, y, name):
    emit(f'  <g transform="translate({x},{y})">')
    emit('    <rect fill="#c4a05a" stroke="#6b3f12" stroke-width="0.2" x="-3.2" y="-3.4" width="6.4" height="6.4"/>')
    emit('    <circle class="pad" cx="-1.27" cy="1.3" r="0.5"/><circle class="hole" cx="-1.27" cy="1.3" r="0.26"/>')
    emit('    <circle class="pad" cx="0" cy="-1.3" r="0.5"/><circle class="hole" cx="0" cy="-1.3" r="0.26"/>')
    emit('    <circle class="pad" cx="1.27" cy="1.3" r="0.5"/><circle class="hole" cx="1.27" cy="1.3" r="0.26"/>')
    emit(f'    <text class="lab" y="5.8">{name}</text></g>')


def ge(x, y, name):
    emit(f'  <g transform="translate({x},{y})">')
    emit('    <circle class="pad" cx="-1.1" cy="0" r="0.5"/><circle class="hole" cx="-1.1" cy="0" r="0.26"/>')
    emit('    <circle class="pad" cx="1.1" cy="0" r="0.5"/><circle class="hole" cx="1.1" cy="0" r="0.26"/>')
    emit(f'    <text class="lab" y="3.4">{name}</text></g>')


def pads2x(x, y, cols, jref, title):
    """Pads 2×N para soldar o fio do painel. Passo 3,5 mm. Pino 1 = quadrado."""
    p = 3.5
    pr, hr = 1.2, 0.5
    assert x - pr > 7, (jref, x - pr)
    assert x + (cols - 1) * p + pr < 52.2, (jref, x + (cols - 1) * p + pr)
    assert y - pr > 12, (jref, y)
    assert y + p + pr < 151, (jref, y + p + pr)
    for col in range(cols):
        px = x + col * p
        for row in (0, 1):
            py = y + row * p
            n = col + 1 + row * cols
            if n == 1:
                emit(
                    f'  <rect class="pad" x="{px - pr:.2f}" y="{py - pr:.2f}" '
                    f'width="{2 * pr:.2f}" height="{2 * pr:.2f}"/>'
                )
            else:
                emit(f'  <circle class="pad" cx="{px:.2f}" cy="{py:.2f}" r="{pr}"/>')
            emit(f'  <circle class="hole" cx="{px:.2f}" cy="{py:.2f}" r="{hr}"/>')
    mid = x + (cols - 1) * p / 2
    emit(f'  <text class="lab" x="{x:.2f}" y="{y - pr - 0.55:.2f}">1</text>')
    emit(f'  <text class="lab" x="{x + (cols - 1) * p:.2f}" y="{y - pr - 0.55:.2f}">{cols}</text>')
    emit(f'  <text class="lab" x="{x:.2f}" y="{y + p + pr + 1.45:.2f}">{cols + 1}</text>')
    emit(f'  <text class="lab" x="{x + (cols - 1) * p:.2f}" y="{y + p + pr + 1.45:.2f}">{2 * cols}</text>')
    emit(
        f'  <text class="silk-s" x="{mid:.2f}" y="{y + p + pr + 3.15:.2f}">'
        f'{jref} {title}</text>'
    )


def rline(x0, y, items, dx=10.2):
    for i, (ref, val) in enumerate(items):
        r(x0 + i * dx, y, ref, val)


def cline(x0, y, items, dx=8.3):
    for i, (ref, val) in enumerate(items):
        cf(x0 + i * dx, y, ref, val)


def eline(x0, y, items, dx=9.4):
    for i, (ref, val) in enumerate(items):
        ce(x0 + i * dx, y, ref, val)


emit(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-4 -4 {W+8} {H+8}" width="{W+8}mm" height="{H+8}mm">
  <style>
    .brd {{ fill: #c4a05a; stroke: #5a3d14; stroke-width: 0.35; }}
    .gnd {{ fill: #8b5a2b; opacity: 0.18; }}
    .blk {{ fill: none; stroke: #6b3f12; stroke-width: 0.2; stroke-dasharray: 1 0.7; }}
    .cu {{ fill: none; stroke: #b87333; stroke-width: 0.7; stroke-linecap: round; }}
    .cu-w {{ fill: none; stroke: #b87333; stroke-width: 1.2; }}
    .pad {{ fill: #d4922a; stroke: #6b3f12; stroke-width: 0.12; }}
    .hole {{ fill: #1a1a1a; }}
    .silk {{ fill: #3a2410; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 2.1px; text-anchor: middle; }}
    .silk-s {{ fill: #3a2410; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 1.25px; text-anchor: middle; }}
    .lab {{ fill: #3a2410; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 1.02px; text-anchor: middle; }}
    .el {{ fill: none; stroke: #6b3f12; stroke-width: 0.18; }}
  </style>
  <defs>
    <g id="dip8">
      <rect fill="#c4a05a" stroke="#6b3f12" stroke-width="0.2" x="-5" y="-6" width="10" height="14"/>
      <circle class="pad" cx="-3.81" cy="-3.81" r="0.58"/><circle class="hole" cx="-3.81" cy="-3.81" r="0.3"/>
      <circle class="pad" cx="-3.81" cy="-1.27" r="0.58"/><circle class="hole" cx="-3.81" cy="-1.27" r="0.3"/>
      <circle class="pad" cx="-3.81" cy="1.27" r="0.58"/><circle class="hole" cx="-3.81" cy="1.27" r="0.3"/>
      <circle class="pad" cx="-3.81" cy="3.81" r="0.58"/><circle class="hole" cx="-3.81" cy="3.81" r="0.3"/>
      <circle class="pad" cx="3.81" cy="-3.81" r="0.58"/><circle class="hole" cx="3.81" cy="-3.81" r="0.3"/>
      <circle class="pad" cx="3.81" cy="-1.27" r="0.58"/><circle class="hole" cx="3.81" cy="-1.27" r="0.3"/>
      <circle class="pad" cx="3.81" cy="1.27" r="0.58"/><circle class="hole" cx="3.81" cy="1.27" r="0.3"/>
      <circle class="pad" cx="3.81" cy="3.81" r="0.58"/><circle class="hole" cx="3.81" cy="3.81" r="0.3"/>
    </g>
    <g id="dip16">
      <rect fill="#c4a05a" stroke="#6b3f12" stroke-width="0.2" x="-6" y="-11.4" width="12" height="24.8"/>
      <circle class="pad" cx="-3.81" cy="-8.89" r="0.52"/><circle class="hole" cx="-3.81" cy="-8.89" r="0.28"/>
      <circle class="pad" cx="-3.81" cy="-6.35" r="0.52"/><circle class="hole" cx="-3.81" cy="-6.35" r="0.28"/>
      <circle class="pad" cx="-3.81" cy="-3.81" r="0.52"/><circle class="hole" cx="-3.81" cy="-3.81" r="0.28"/>
      <circle class="pad" cx="-3.81" cy="-1.27" r="0.52"/><circle class="hole" cx="-3.81" cy="-1.27" r="0.28"/>
      <circle class="pad" cx="-3.81" cy="1.27" r="0.52"/><circle class="hole" cx="-3.81" cy="1.27" r="0.28"/>
      <circle class="pad" cx="-3.81" cy="3.81" r="0.52"/><circle class="hole" cx="-3.81" cy="3.81" r="0.28"/>
      <circle class="pad" cx="-3.81" cy="6.35" r="0.52"/><circle class="hole" cx="-3.81" cy="6.35" r="0.28"/>
      <circle class="pad" cx="-3.81" cy="8.89" r="0.52"/><circle class="hole" cx="-3.81" cy="8.89" r="0.28"/>
      <circle class="pad" cx="3.81" cy="-8.89" r="0.52"/><circle class="hole" cx="3.81" cy="-8.89" r="0.28"/>
      <circle class="pad" cx="3.81" cy="-6.35" r="0.52"/><circle class="hole" cx="3.81" cy="-6.35" r="0.28"/>
      <circle class="pad" cx="3.81" cy="-3.81" r="0.52"/><circle class="hole" cx="3.81" cy="-3.81" r="0.28"/>
      <circle class="pad" cx="3.81" cy="-1.27" r="0.52"/><circle class="hole" cx="3.81" cy="-1.27" r="0.28"/>
      <circle class="pad" cx="3.81" cy="1.27" r="0.52"/><circle class="hole" cx="3.81" cy="1.27" r="0.28"/>
      <circle class="pad" cx="3.81" cy="3.81" r="0.52"/><circle class="hole" cx="3.81" cy="3.81" r="0.28"/>
      <circle class="pad" cx="3.81" cy="6.35" r="0.52"/><circle class="hole" cx="3.81" cy="6.35" r="0.28"/>
      <circle class="pad" cx="3.81" cy="8.89" r="0.52"/><circle class="hole" cx="3.81" cy="8.89" r="0.28"/>
    </g>
    <g id="to92">
      <circle class="pad" cx="-1.3" cy="-1.9" r="0.52"/><circle class="hole" cx="-1.3" cy="-1.9" r="0.28"/>
      <circle class="pad" cx="0" cy="0" r="0.52"/><circle class="hole" cx="0" cy="0" r="0.28"/>
      <circle class="pad" cx="1.3" cy="-1.9" r="0.52"/><circle class="hole" cx="1.3" cy="-1.9" r="0.28"/>
    </g>
    <g id="wp">
      <circle class="pad" r="0.68"/><circle class="hole" r="0.38"/>
    </g>
    <g id="rth">
      <rect fill="#c4a05a" stroke="#6b3f12" stroke-width="0.14" x="-2.7" y="-1.0" width="5.4" height="2.0" rx="0.25"/>
      <circle class="pad" cx="-3.81" cy="0" r="0.52"/><circle class="hole" cx="-3.81" cy="0" r="0.26"/>
      <circle class="pad" cx="3.81" cy="0" r="0.52"/><circle class="hole" cx="3.81" cy="0" r="0.26"/>
    </g>
    <g id="cth">
      <rect fill="#c4a05a" stroke="#6b3f12" stroke-width="0.14" x="-1.5" y="-1.1" width="3.0" height="2.2"/>
      <circle class="pad" cx="-2.54" cy="0" r="0.48"/><circle class="hole" cx="-2.54" cy="0" r="0.25"/>
      <circle class="pad" cx="2.54" cy="0" r="0.48"/><circle class="hole" cx="2.54" cy="0" r="0.25"/>
    </g>
    <g id="cel">
      <circle class="el" r="2.25"/>
      <circle class="pad" cx="-1.27" cy="0" r="0.48"/><circle class="hole" cx="-1.27" cy="0" r="0.25"/>
      <circle class="pad" cx="1.27" cy="0" r="0.48"/><circle class="hole" cx="1.27" cy="0" r="0.25"/>
      <text x="-1.27" y="-2.7" class="lab">+</text>
    </g>
  </defs>
''')

emit(f'  <rect class="brd" x="0" y="0" width="{W}" height="{H}"/>')
emit(f'  <rect class="gnd" x="2" y="2" width="{W-4}" height="{H-4}" rx="1"/>')
emit('  <text class="silk" x="136" y="6.0">VOZ-9  BASE</text>')
emit('  <text class="silk-s" x="136" y="8.3">220×160 · CIs em soquete · cabos do painel soldados nos pads</text>')
for x, y in ((4, 4), (216, 4), (4, 156), (216, 156)):
    emit(f'  <circle class="pad" cx="{x}" cy="{y}" r="2.1"/><circle class="hole" cx="{x}" cy="{y}" r="1.55"/>')

# coluna de pads — fio do painel solda direto, sem conector
blk(6, 8, 46, 146, "PADS  CABO  J1–J9")
pads2x(9, 16, 10, "J1", "OSC")
pads2x(9, 38, 6, "J2", "LFO")
pads2x(9, 58, 10, "J3", "DELAY")
pads2x(9, 80, 10, "J4", "PATCH A")
pads2x(9, 102, 8, "J5", "PATCH B")
pads2x(9, 124, 3, "J6", "CTRL")
pads2x(20.5, 124, 6, "J7", "IN+PRE")
pads2x(42.5, 124, 3, "J8", "OUT")
pads2x(9, 140, 6, "J9", "EQ424")

emit('  <path class="cu-w" d="M54,10 V150"/>')
emit('  <path class="cu" d="M56.6,10 V148"/>')
emit('  <path class="cu" d="M214,10 V148"/>')
emit('  <text class="lab" x="54" y="11.8">GND</text>')
emit('  <text class="lab" x="56.6" y="11.8">V9</text>')
emit('  <text class="lab" x="214" y="11.8">4V5</text>')

# FONTE — ICs em cima, R no meio, 47µ embaixo, 10µ à direita do 78M05
blk(58, 10, 62, 46, "FONTE")
emit('  <g transform="translate(64,21)">')
emit('    <rect fill="#c4a05a" stroke="#6b3f12" stroke-width="0.2" x="-2" y="-2.8" width="4" height="7.6"/>')
emit('    <circle class="pad" cx="0" cy="-1.4" r="0.55"/><circle class="hole" cx="0" cy="-1.4" r="0.28"/>')
emit('    <circle class="pad" cx="0" cy="1.4" r="0.55"/><circle class="hole" cx="0" cy="1.4" r="0.28"/>')
emit('    <circle class="pad" cx="0" cy="3.8" r="0.55"/><circle class="hole" cx="0" cy="3.8" r="0.28"/>')
emit('    <text class="lab" y="6.3">D1</text></g>')
dip8(80, 22, "U4 SKT")
emit('  <g transform="translate(100,19)">')
emit('    <rect fill="#c4a05a" stroke="#6b3f12" stroke-width="0.2" x="-2.8" y="-3" width="5.6" height="9.2"/>')
emit('    <circle class="pad" cx="-1.5" cy="4.6" r="0.5"/><circle class="hole" cx="-1.5" cy="4.6" r="0.26"/>')
emit('    <circle class="pad" cx="0" cy="4.6" r="0.5"/><circle class="hole" cx="0" cy="4.6" r="0.26"/>')
emit('    <circle class="pad" cx="1.5" cy="4.6" r="0.5"/><circle class="hole" cx="1.5" cy="4.6" r="0.26"/>')
emit('    <text class="lab" y="-3.5">U5 78M05</text></g>')
ce(114, 20, "C56", "10µ")
ce(114, 29, "C57", "10µ")
ce(114, 38, "C58", "10µ")
rline(64, 35, [("R14", "4k7"), ("R17", "4k7"), ("R19", "10k"), ("R20", "10k")], dx=11.2)
r(64, 41.5, "R18", "5k6")
r(75.2, 41.5, "R55", "22k")
cf(90, 41.5, "C22", "100n")
eline(64, 51, [("C64", "47µ"), ("C65", "47µ"), ("C66", "47µ"), ("C67", "47µ")], dx=12)

# U1
blk(122, 10, 54, 40, "U1 NE5532")
dip8(130, 22, "U1 SKT")
rline(144, 16, [("R12", "2k2"), ("R13", "2k2"), ("R57", "22k")])
rline(144, 22.4, [("R58", "22k"), ("R6", "1k"), ("R42", "10k")])
rline(144, 28.8, [("R1", "220"), ("R2", "220"), ("R44", "10k")])
cline(128, 36, [("C1", "100p"), ("C2", "100p"), ("C23", "100n"), ("C24", "100n"), ("C25", "100n")])
eline(128, 45, [("C59", "10µ"), ("C60", "10µ"), ("C61", "10µ"), ("C62", "10µ"), ("C63", "10µ")])
dip8(156, 45, "U9 EQ")

# U2
blk(178, 10, 36, 40, "U2 OSC")
dip8(186, 21, "U2 SKT")
r(200, 16, "R21", "10k")
r(200, 22.4, "R22", "10k")
r(200, 28.8, "R62", "100k")
r(200, 35.2, "R63", "100k")
r(186, 35.2, "R72", "220k")
cf(186, 42, "C21", "100n")
cf(200, 42, "C6", "10n")
cf(186, 47.2, "C19", "100n")

# MIX
blk(58, 58, 62, 32, "MIX  SHAPE  FM")
to92(64, 65, "Q1")
to92(76, 65, "Q2")
to92(88, 65, "Q3")
to92(100, 65, "Q6")
ge(112, 65, "MP20-1")
rline(64, 73, [("R23", "10k"), ("R24", "10k"), ("R25", "10k"), ("R3", "1k"), ("R64", "100k"), ("R80", "1M")])
rline(64, 79, [("R26", "10k"), ("R29", "10k"), ("R27", "10k"), ("R28", "10k"), ("R4", "1k"), ("R65", "100k")])
rline(64, 85, [("R66", "100k"), ("R73", "220k")])
cline(90, 85, [("C26", "100n"), ("C51", "1µ"), ("C52", "1µ")])

# VCF VCA LFO
blk(122, 52, 54, 38, "VCF  VCA  LFO")
to92(128, 60, "Q4")
to92(140, 60, "Q5")
to92(152, 60, "Q7")
to92(164, 60, "D2")
rline(128, 68, [("R30", "10k"), ("R67", "100k"), ("R61", "68k"), ("R31", "10k"), ("R69", "100k")])
rline(128, 74.4, [("R74", "220k"), ("R68", "100k"), ("R5", "1k"), ("R32", "10k"), ("R33", "10k")])
rline(128, 80.8, [("R34", "10k"), ("R15", "4k7"), ("R81", "1M")])
cline(128, 86.8, [("C43", "220n"), ("C44", "220n"), ("C45", "220n"), ("C46", "220n"), ("C47", "220n")])

# CLK
blk(178, 52, 36, 38, "CLK  TIME")
to92(184, 60, "D3")
to92(196, 60, "D4")
r(208, 60, "R59", "47k")
rline(184, 68, [("R43", "10k"), ("R70", "100k"), ("R79", "220k")])
rline(184, 74.4, [("R11", "2k"), ("R7", "1k"), ("R8", "1k")])
rline(184, 80.8, [("R56", "22k"), ("R9", "1k"), ("R10", "1k")])
ce(186, 87, "C55", "4µ7")
r(202, 87, "R60", "68k")

# NAB
blk(58, 92, 62, 26, "U3 NAB")
dip8(66, 104, "U3 SKT")
rline(80, 98, [("R51", "15k"), ("R52", "15k"), ("R53", "15k"), ("R54", "15k"), ("R16", "4k7")])
rline(80, 104.4, [("R45", "10k"), ("R46", "10k")])
cline(80, 111, [("C4", "3n3"), ("C5", "3n3"), ("C48", "220n"), ("C49", "220n"), ("C20", "100n"), ("C29", "100n")])
cf(80, 116.5, "C30", "100n")
cf(90, 116.5, "C50", "220n")

# ENV
blk(122, 92, 54, 26, "ENV  SAÍDA")
cline(128, 98, [("C27", "100n"), ("C28", "100n")])
eline(128, 108, [("C68", "47µ"), ("C53", "2µ2"), ("C54", "2µ2"), ("C71", "47µ")])
trim(168, 108, "RV1")

# TRIM
blk(178, 92, 36, 26, "TRIM  Ge")
trim(186, 104, "RV2")
ge(202, 104, "MP20-2")

# FITA — chips + todos os R/C que faltam
blk(58, 120, 156, 34, "FITA   U6 H1    U7 H2    U8 H3")
dip16(68, 136, "U6 SKT")
dip16(88, 136, "U7 SKT")
dip16(108, 136, "U8 SKT")
rline(124, 126, [("R35", "10k"), ("R36", "10k"), ("R37", "10k"), ("R38", "10k"), ("R39", "10k"), ("R40", "10k"), ("R41", "10k"), ("R47", "10k")])
rline(124, 132.4, [("R48", "10k"), ("R49", "10k"), ("R50", "10k"), ("R71", "100k"), ("R75", "220k"), ("R76", "220k"), ("R77", "220k"), ("R78", "220k")])
cline(124, 139, [
    ("C3", "2n2"), ("C7", "10n"), ("C8", "10n"), ("C9", "10n"), ("C10", "10n"),
    ("C11", "10n"), ("C12", "10n"), ("C13", "10n"), ("C14", "10n"),
])
cline(124, 145.4, [
    ("C15", "10n"), ("C16", "10n"), ("C17", "10n"), ("C18", "22n"),
    ("C31", "100n"), ("C32", "100n"), ("C33", "100n"), ("C34", "100n"), ("C35", "100n"),
])
cline(124, 151.8, [
    ("C36", "100n"), ("C37", "100n"), ("C38", "100n"), ("C39", "100n"),
    ("C40", "100n"), ("C41", "100n"), ("C42", "100n"),
])
ce(190, 151.8, "C69", "47µ")
ce(202, 151.8, "C70", "47µ")

emit('  <text class="lab" x="136" y="157.6">CIs só no soquete · pads J1–J9 furo 1,0 · pino 1 = quadrado · sem conector</text>')
emit("</svg>\n")

missing_r = [f"R{i}" for i in range(1, 82) if f"R{i}" not in seen_r]
missing_c = [f"C{i}" for i in range(1, 72) if f"C{i}" not in seen_c]
extra_r = sorted(seen_r)
if missing_r or missing_c:
    raise SystemExit(f"FALTANDO R={missing_r} C={missing_c}")
if len(seen_r) != 81 or len(seen_c) != 71:
    raise SystemExit(f"contagem R={len(seen_r)} C={len(seen_c)}")

path = Path(__file__).with_name("pcb.svg")
path.write_text("\n".join(out))
print(f"ok {path}  R={len(seen_r)} C={len(seen_c)}")
