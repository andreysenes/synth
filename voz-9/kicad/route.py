#!/usr/bin/env python3
"""Liga a BASE conforme esquema.md / pre-vocal.md / bom.md e roteia.

Cobre no verso (B.Cu). O que cair na frente (F.Cu) é jumper.
R17 é a 4k7 de folga e fica sem net. Os passivos do EQ 424 (3k3, 33n, 1n)
não estão na placa: U9 entra como seguidor no lugar da rede.
"""

import os
import subprocess

import pcbnew

ROOT = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(ROOT, "voz-9.kicad_pcb")
DSN = "/tmp/voz9-route/voz-9.dsn"
SES = "/tmp/voz9-route/voz-9.ses"
JAR = "/tmp/freerouting/freerouting.jar"

# Pinos de propósito sem trilha.
OPEN = {
    ("J1", "20"),
    ("J4", "2"),
    ("J4", "5"),
    ("J4", "8"),
    ("J4", "14"),
    ("J4", "17"),
    ("J4", "19"),
    ("J4", "20"),
    ("J5", "2"),
    ("J5", "5"),
    ("J5", "8"),
    ("J5", "11"),
    ("J5", "16"),
    ("J7", "12"),
    ("J8", "6"),
    ("U4", "1"),
    ("U4", "6"),
    ("U4", "7"),
    ("U6", "5"),
    ("U7", "5"),
    ("U8", "5"),
    ("R17", "1"),
    ("R17", "2"),
    # EQ 424: os C/R da rede (33n, 1n, 10n, 3k3) não estão na placa.
    ("J9", "1"), ("J9", "2"), ("J9", "3"),
    ("J9", "4"), ("J9", "5"), ("J9", "6"),
    ("J9", "7"), ("J9", "8"), ("J9", "9"),
    ("J9", "10"), ("J9", "11"), ("J9", "12"),
}


def add(nets, name, *pins):
    bucket = nets.setdefault(name, [])
    for ref, pin in pins:
        bucket.append((ref, str(pin)))


def two(nets, ref, net_a, net_b):
    add(nets, net_a, (ref, "1"))
    add(nets, net_b, (ref, "2"))


def build_nets():
    n = {}
    # --- fonte ---
    two(n, "D1", "V9", "P4_TIP")  # K = pino 1, A = pino 2
    add(n, "P4_TIP", ("J6", "3"))
    add(n, "GND", ("J6", "4"))
    two(n, "R14", "V9", "LED_A")
    add(n, "LED_A", ("J6", "1"))
    add(n, "GND", ("J6", "2"))
    two(n, "R19", "V9", "N4V5")
    two(n, "R20", "N4V5", "GND")
    two(n, "R55", "V9", "N1V8")
    two(n, "R18", "N1V8", "GND")
    two(n, "C64", "V9", "GND")
    two(n, "C65", "VEE", "GND")
    two(n, "C66", "N4V5", "GND")
    two(n, "C67", "N1V8", "GND")
    two(n, "C22", "V5", "GND")
    two(n, "C58", "V5", "GND")
    add(n, "V9", ("U5", "1"))
    add(n, "GND", ("U5", "2"))
    add(n, "V5", ("U5", "3"))
    add(n, "V9", ("U4", "8"))
    add(n, "GND", ("U4", "3"))
    two(n, "C56", "U4_CAP+", "U4_CAP-")
    add(n, "U4_CAP+", ("U4", "2"))
    add(n, "U4_CAP-", ("U4", "4"))
    add(n, "VEE", ("U4", "5"))
    two(n, "C57", "VEE", "GND")

    # --- pré 5532, ±9 V ---
    add(n, "V9", ("U1", "8"), ("U3", "8"), ("U9", "8"))
    add(n, "VEE", ("U1", "4"), ("U3", "4"), ("U9", "4"))
    two(n, "C23", "V9", "GND")
    two(n, "C24", "VEE", "GND")
    two(n, "C61", "V9", "GND")
    two(n, "C62", "VEE", "GND")
    two(n, "C40", "V9", "GND")
    add(n, "GND", ("J7", "3"), ("J7", "5"))
    two(n, "C1", "XLR_HOT", "GND")
    two(n, "C2", "XLR_COLD", "GND")
    add(n, "XLR_HOT", ("J7", "1"))
    add(n, "XLR_COLD", ("J7", "2"))
    two(n, "C59", "XLR_HOT", "PRE_R12")
    two(n, "C60", "XLR_COLD", "PRE_R13")
    two(n, "R12", "PRE_R12", "U1_INP")
    two(n, "R13", "PRE_R13", "U1_INM")
    add(n, "U1_INP", ("U1", "3"))
    add(n, "U1_INM", ("U1", "2"))
    two(n, "R57", "U1_INM", "U1_OA")
    two(n, "R58", "U1_INP", "GND")
    add(n, "U1_OA", ("U1", "1"))
    two(n, "C25", "U1_OA", "U1_BP")
    add(n, "U1_BP", ("U1", "5"))
    add(n, "U1_BM", ("U1", "6"))
    add(n, "U1_OB", ("U1", "7"))
    two(n, "R6", "U1_BM", "GND")
    two(n, "R42", "U1_BM", "U1_OB")
    two(n, "C42", "U1_OB", "PRE_CW")
    add(n, "PRE_CW", ("J7", "8"))
    add(n, "GND", ("J7", "6"))
    add(n, "PRE_W", ("J7", "7"), ("J5", "10"))
    two(n, "C41", "PRE_W", "OSCIN_CW")
    add(n, "OSCIN_CW", ("J7", "11"))
    add(n, "SEND_SW", ("J5", "14"))
    add(n, "PRE_W", ("SEND_SW", "x")) if False else None
    # normal do RCV: o jack no painel liga SW em TIP
    add(n, "PRE_W", ("J5", "14"))

    # --- osciladores, alimentação simples ---
    add(n, "V9", ("U2", "8"))
    add(n, "GND", ("U2", "4"))
    two(n, "C19", "V9", "GND")
    add(n, "U2A_OUT", ("U2", "1"))
    add(n, "U2A_INM", ("U2", "2"), ("J1", "2"))
    add(n, "U2A_INP", ("U2", "3"))
    two(n, "R21", "U2A_OUT", "OSC_A_POT")
    add(n, "OSC_A_POT", ("J1", "1"))
    two(n, "C21", "U2A_INM", "N4V5")
    two(n, "R62", "U2A_OUT", "U2A_INP")
    two(n, "R63", "U2A_INP", "N4V5")
    two(n, "C51", "U2A_OUT", "SW_A")
    add(n, "SW_A", ("J1", "14"))
    add(n, "SW_A_ON", ("J1", "15"), ("J4", "1"))
    two(n, "R24", "SW_A_ON", "SUM")
    add(n, "U2B_OUT", ("U2", "7"))
    add(n, "U2B_INM", ("U2", "6"), ("J1", "4"))
    add(n, "U2B_INP", ("U2", "5"))
    two(n, "R22", "U2B_OUT", "OSC_B_POT")
    add(n, "OSC_B_POT", ("J1", "3"))
    two(n, "C6", "U2B_INM", "N4V5")
    two(n, "R72", "U2B_OUT", "U2B_INP")
    two(n, "R73", "U2B_INP", "N4V5")
    two(n, "C52", "U2B_OUT", "SW_B")
    add(n, "SW_B", ("J1", "16"))
    add(n, "SW_B_ON", ("J1", "17"), ("J4", "4"))
    two(n, "R25", "SW_B_ON", "SUM")
    add(n, "Q1D", ("Q1", "1"), ("U2A_INM", "x")) if False else None
    add(n, "U2A_INM", ("Q1", "1"))
    add(n, "N4V5", ("Q1", "3"), ("Q2", "3"))
    two(n, "R65", "PITCH_CV", "Q1G")
    add(n, "Q1G", ("Q1", "2"))
    add(n, "U2B_INM", ("Q2", "1"))
    two(n, "R66", "PITCH_CV", "Q2G")
    add(n, "Q2G", ("Q2", "2"))

    # --- noise + mix + amount ---
    two(n, "R23", "V9", "NOISE_D")
    add(n, "NOISE_D", ("Q3", "1"))
    add(n, "GND", ("Q3", "3"))
    two(n, "R3", "NOISE_S", "GND")
    add(n, "NOISE_S", ("Q3", "3"))
    # Q3 source já está em GND; R3 em série
    n["GND"] = [p for p in n["GND"] if p != ("Q3", "3")]
    add(n, "NOISE_S", ("Q3", "3"))
    two(n, "R80", "Q3G", "GND")
    add(n, "Q3G", ("Q3", "2"))
    two(n, "C26", "NOISE_D", "NOISE_MIX")
    two(n, "R64", "NOISE_MIX", "SUM")
    two(n, "R26", "EXT_IN", "SUM")
    add(n, "EXT_IN", ("J4", "7"))
    two(n, "C45", "INST_TIP", "EXT_IN")
    add(n, "INST_TIP", ("J7", "4"))
    add(n, "SUM", ("J1", "5"))
    add(n, "GND", ("J1", "7"))
    add(n, "AMT_W", ("J1", "6"), ("J7", "9"))
    add(n, "MIX", ("J7", "10"))
    two(n, "C30", "MIX", "EQ_IN")

    # U9 seguidor (a rede Baxandall ainda não tem peça na placa)
    add(n, "EQ_IN", ("U9", "3"))
    add(n, "EQ_A", ("U9", "1"), ("U9", "2"), ("U9", "5"))
    add(n, "EQ_OUT", ("U9", "6"), ("U9", "7"), ("J1", "8"))

    # buffer pós-EQ
    add(n, "V9", ("Q6", "1"))
    two(n, "R27", "EQ_OUT", "Q6G")
    add(n, "Q6G", ("Q6", "2"))
    two(n, "R4", "Q6S", "N4V5")
    add(n, "Q6S", ("Q6", "3"))
    two(n, "R28", "Q6S", "BUF_OUT")

    # --- shape ---
    add(n, "GND", ("J1", "10"))
    add(n, "SHAPE_W", ("J1", "9"))
    two(n, "R29", "SHAPE_W", "SHAPE")
    add(n, "BUF_OUT", ("SHAPE", "x")) if False else None
    # o buffer soma no nó do shape
    add(n, "SHAPE", ("R28", "2"))
    n["BUF_OUT"] = [p for p in n["BUF_OUT"] if p != ("R28", "2")]
    add(n, "SHAPE", ("D6", "2"))  # ânodo
    add(n, "GND", ("D6", "1"))
    two(n, "C28", "SHAPE", "FILT_SW")
    add(n, "FILT_SW", ("J4", "11"))
    add(n, "FILT_TIP", ("J4", "10"))

    # --- VCF ---
    two(n, "R30", "FILT_TIP", "VCF")
    two(n, "C47", "VCF", "GND")
    add(n, "VCF", ("Q4", "1"))
    add(n, "N1V8", ("Q4", "3"), ("J1", "11"))
    add(n, "GND", ("J1", "13"))
    add(n, "CUT_W", ("J1", "12"))
    two(n, "R68", "CUT_W", "Q4G")
    add(n, "Q4G", ("Q4", "2"))
    two(n, "R67", "Q4G", "FCV")
    add(n, "FCV", ("J4", "13"))
    two(n, "R61", "VCF", "RES_W")
    add(n, "RES_W", ("RV2", "2"))
    add(n, "VCF_IN", ("RV2", "1"), ("FILT_TIP", "x")) if False else None
    add(n, "FILT_TIP", ("RV2", "1"))
    add(n, "FILT_TIP", ("RV2", "3"))
    two(n, "C50", "VCF", "VCA_D")

    # --- VCA + envelope ---
    add(n, "VCA_D", ("Q5", "1"))
    add(n, "VCA_S", ("Q5", "3"))
    two(n, "R34", "VCA_S", "N1V8")
    two(n, "C54", "VCA_S", "DRY")
    add(n, "ENV", ("Q5", "2"))
    two(n, "C68", "ENV", "GND")
    two(n, "R74", "ENV", "GND")
    two(n, "R69", "ENV", "VCV")
    add(n, "VCV", ("J4", "16"))
    add(n, "GATE", ("J6", "5"), ("D2", "2"))
    add(n, "GND", ("J6", "6"))
    add(n, "ENV", ("D2", "1"))
    two(n, "C27", "PRE_W", "FALA")
    two(n, "R50", "FALA", "FALA_A")
    add(n, "FALA_A", ("D3", "2"))
    add(n, "ENV", ("D3", "1"))
    add(n, "N1V8", ("J1", "18"))
    add(n, "ENV", ("J1", "19"))

    # --- LFO ---
    two(n, "R31", "V9", "LFO_D")
    add(n, "LFO_D", ("Q7", "1"))
    two(n, "R5", "LFO_S", "GND")
    add(n, "LFO_S", ("Q7", "3"))
    add(n, "LFO_G", ("Q7", "2"))
    two(n, "C43", "LFO_D", "LFO_N1")
    two(n, "R32", "LFO_N1", "GND")
    two(n, "C44", "LFO_N1", "LFO_N2")
    two(n, "R33", "LFO_N2", "GND")
    add(n, "LFO_N2", ("J2", "7"))
    two(n, "C46", "TREM_A", "LFO_G")
    add(n, "TREM_A", ("J2", "8"))
    two(n, "C71", "TREM_B", "LFO_G")
    add(n, "TREM_B", ("J2", "9"))
    two(n, "R15", "LFO_G", "RATE_W")
    add(n, "RATE_W", ("J2", "1"), ("J2", "2"))
    add(n, "GND", ("J2", "3"))
    two(n, "R81", "LFO_G", "GND")
    two(n, "C53", "LFO_D", "LFO_AC")
    two(n, "R79", "LFO_AC", "LFO_OUT")
    add(n, "LFO_OUT", ("J5", "1"), ("J2", "4"))
    add(n, "GND", ("J2", "6"))
    add(n, "DEPTH_W", ("J2", "5"), ("J2", "10"))
    add(n, "PITCH_CV", ("J2", "11"))
    add(n, "TIME_CV", ("J2", "12"))

    # --- CLK ---
    add(n, "CLK_TIP", ("J5", "7"))
    two(n, "R59", "CLK_TIP", "CLK_A")
    two(n, "R43", "CLK_A", "GND")
    add(n, "CLK_A", ("D4", "2"))
    add(n, "CLK_B", ("D4", "1"))
    two(n, "C55", "CLK_B", "GND")
    two(n, "R78", "CLK_B", "GND")
    two(n, "R70", "CLK_B", "TIME_CV")
    add(n, "TIME_CV", ("J5", "4"))

    # --- NAB ---
    add(n, "GND", ("U3", "3"), ("U3", "5"))
    add(n, "STAR", ("J3", "11"), ("J5", "13"))
    two(n, "R46", "DRY", "STAR")
    two(n, "R51", "STAR", "GRAVA_IN")
    two(n, "C48", "GRAVA_IN", "NAB_MID")
    two(n, "R16", "NAB_MID", "U3A_IN")
    add(n, "U3A_IN", ("U3", "2"))
    add(n, "U3A_OUT", ("U3", "1"))
    two(n, "R52", "U3A_IN", "U3A_OUT")
    two(n, "C4", "U3A_IN", "U3A_OUT")
    two(n, "C20", "U3A_OUT", "HEADS")
    add(n, "WET_MIX", ("R53_IN", "x")) if False else None
    two(n, "C29", "WET_MIX", "LE_IN")
    two(n, "R53", "LE_IN", "U3B_IN")
    add(n, "U3B_IN", ("U3", "6"))
    add(n, "WET", ("U3", "7"))
    two(n, "R54", "U3B_IN", "WET")
    two(n, "C5", "U3B_IN", "WET")
    two(n, "R45", "U3B_IN", "NAB_BASS")
    two(n, "C49", "NAB_BASS", "WET")
    two(n, "R49", "WET", "WET_LP")
    two(n, "C3", "WET_LP", "GND")
    add(n, "WET", ("D7", "2"))
    add(n, "GND", ("D7", "1"))
    add(n, "WET", ("RV1", "1"))
    add(n, "FB_CW", ("RV1", "2"), ("RV1", "3"), ("J3", "12"))
    add(n, "GND", ("J3", "10"))

    # --- três heads ---
    for ref, series, mix_r, fb, vcc_c, ref_c, out_c, clk_c, lpf_c, pin6_r in (
        ("U6", "R35", "R38", "R41", "C31", "C37", "C34", "C7", "C10", "R75"),
        ("U7", "R36", "R39", "R47", "C32", "C38", "C35", "C8", "C11", "R76"),
        ("U8", "R37", "R40", "R48", "C33", "C39", "C36", "C9", "C12", "R77"),
    ):
        add(n, "V5", (ref, "1"))
        two(n, vcc_c, "V5", "GND")
        two(n, ref_c, "PT_REF_" + ref, "GND")
        add(n, "PT_REF_" + ref, (ref, "2"))
        add(n, "GND", (ref, "3"), (ref, "4"))
        add(n, "PT6_" + ref, (ref, "6"))
        two(n, pin6_r, "TIME_CV", "PT6_" + ref)
        two(n, clk_c, ref + "_CC1", ref + "_CC0")
        add(n, ref + "_CC1", (ref, "7"))
        add(n, ref + "_CC0", (ref, "8"))
        add(n, ref + "_OP", (ref, "9"), (ref, "10"), (ref, "11"), (ref, "12"), (ref, "13"))
        two(n, series, "HEADS", ref + "_IN")
        add(n, ref + "_IN", (ref, "16"))
        two(n, fb, ref + "_IN", ref + "_LP1")
        add(n, ref + "_LP1", (ref, "15"))
        two(n, lpf_c, ref + "_LP1", "GND")
        add(n, ref + "_OUT", (ref, "14"))
        two(n, out_c, ref + "_OUT", ref + "_SW")

    add(n, "U6_SW", ("J3", "4"), ("J3", "16"))
    add(n, "U7_IN", ("J3", "17"))
    two(n, "R38", "H1_ON", "WET_MIX")
    add(n, "H1_ON", ("J3", "5"))
    two(n, "R39", "H2_ON", "WET_MIX")
    add(n, "H2_ON", ("J3", "7"))
    two(n, "R40", "H3_ON", "WET_MIX")
    add(n, "H3_ON", ("J3", "9"))
    add(n, "U7_SW", ("J3", "6"))
    add(n, "U8_SW", ("J3", "8"))

    # tempo
    add(n, "V5", ("J3", "1"))
    add(n, "TIME_W", ("J3", "2"))
    add(n, "GND", ("J3", "3"))
    two(n, "R11", "TIME_W", "U6_PIN6")
    add(n, "U6_PIN6", ("U6", "6"))
    n["PT6_U6"] = [p for p in n["PT6_U6"] if p != ("U6", "6")]
    add(n, "U6_PIN6", ("R75", "2"))
    n["PT6_U6"].append(("R75", "2")) if False else None
    # R75 já liga TIME_CV a PT6_U6; o pino 6 tem de estar em PT6_U6
    add(n, "PT6_U6", ("U6", "6"))
    n["U6_PIN6"] = [p for p in n["U6_PIN6"] if p != ("U6", "6")]
    two(n, "R7", "TIME_W", "H2A")
    two(n, "R8", "H2A", "H2B")
    two(n, "R56", "H2B", "PT6_U7")
    two(n, "R9", "TIME_W", "H3A")
    two(n, "R10", "H3A", "H3B")
    two(n, "R60", "H3B", "PT6_U8")
    # H1: o 2k entra no mesmo nó do pino 6
    add(n, "PT6_U6", ("R11", "2"))
    n["U6_PIN6"] = [p for p in n.get("U6_PIN6", []) if p != ("R11", "2")]

    # WET / VOLUME / OUT
    add(n, "DRY", ("J3", "13"))
    add(n, "WET", ("J3", "15"))
    add(n, "WET_W", ("J3", "14"), ("J3", "20"))
    two(n, "R71", "WET", "WET_W")
    add(n, "GND", ("J3", "18"))
    add(n, "OUT", ("J3", "19"), ("J8", "4"))
    two(n, "R44", "OUT", "XLR_OUT")
    add(n, "XLR_OUT", ("J8", "1"))
    two(n, "R1", "XLR_OUT", "GND")
    two(n, "R2", "J8_COLD", "GND")
    add(n, "J8_COLD", ("J8", "2"))
    add(n, "GND", ("J8", "3"), ("J8", "5"))

    # terras dos jacks
    for ref, pins in (
        ("J4", ("3", "6", "9", "12", "15", "18")),
        ("J5", ("3", "6", "9", "12", "15")),
    ):
        for pin in pins:
            add(n, "GND", (ref, pin))

    # C63 sobra do 10µ: desacopla V5 junto da fita.
    # C69/C70 acoplam a saída dos heads longo e médio.
    two(n, "C63", "V5", "GND")
    two(n, "C69", "U7_OUT", "U7_SW")
    two(n, "C70", "U8_OUT", "U8_SW")
    # 220n de folga e 100n que fecham o filtro de saída dos heads já usados.
    # C13–C18: integrador grosseiro pin 9–14 de cada head.
    two(n, "C13", "U6_OP", "U6_OUT")
    two(n, "C14", "U7_OP", "U7_OUT")
    two(n, "C15", "U8_OP", "U8_OUT")
    two(n, "C16", "U6_LP1", "GND")
    two(n, "C17", "U7_LP1", "GND")
    two(n, "C18", "U8_LP1", "GND")
    return n


def collapse_aliases(nets):
    """Junta nets que nomeiam o mesmo pino (o pino foi parar em dois nomes)."""
    parent = {}

    def find(name):
        parent.setdefault(name, name)
        if parent[name] != name:
            parent[name] = find(parent[name])
        return parent[name]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    pin_owner = {}
    for name, pins in nets.items():
        for pin in pins:
            if pin in OPEN:
                raise SystemExit(f"{pin} está aberto e numa net {name}")
            if pin in pin_owner:
                union(pin_owner[pin], name)
            else:
                pin_owner[pin] = name
    merged = {}
    for name, pins in nets.items():
        root = find(name)
        bucket = merged.setdefault(root, [])
        for pin in pins:
            if pin not in bucket:
                bucket.append(pin)
    return merged


def apply_nets(board, nets):
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            pad.SetNetCode(0)
    code = 1
    for name in sorted(nets):
        item = pcbnew.NETINFO_ITEM(board, name, code)
        board.Add(item)
        code += 1
        for ref, pin in nets[name]:
            fp = board.FindFootprintByReference(ref)
            if fp is None:
                raise SystemExit(f"footprint ausente: {ref}")
            pads = [pad for pad in fp.Pads() if pad.GetNumber() == pin]
            if not pads:
                raise SystemExit(f"pino ausente: {ref}.{pin}")
            for pad in pads:
                pad.SetNet(item)
    board.BuildConnectivity()


def unconnected(board):
    missing = []
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref.startswith("H"):
            continue
        for pad in fp.Pads():
            pin = pad.GetNumber()
            if not pin or (ref, pin) in OPEN:
                continue
            if pad.GetNetname() in ("", None):
                missing.append(f"{ref}.{pin}")
    return missing


def export_dsn(board):
    os.makedirs(os.path.dirname(DSN), exist_ok=True)
    pcbnew.ExportSpecctraDSN(board, DSN)


def run_router():
    settings = "/tmp/freerouting/freerouting.json"
    os.makedirs("/tmp/freerouting", exist_ok=True)
    if os.path.exists(settings):
        import json
        cfg = json.load(open(settings, encoding="utf-8"))
    else:
        cfg = {}
    cfg.setdefault("gui", {})["enabled"] = False
    cfg.setdefault("usage_and_diagnostic_data", {})["disable_analytics"] = True
    router = cfg.setdefault("router", {})
    router["max_passes"] = 40
    router["max_threads"] = 4
    router["job_timeout"] = "01:00:00"
    opt = router.setdefault("optimizer", {})
    opt["max_passes"] = 15
    opt["max_threads"] = 4
    json_dump = __import__("json")
    with open(settings, "w", encoding="utf-8") as fh:
        json_dump.dump(cfg, fh, indent=2)
    proc = subprocess.run(
        ["java", "-Djava.awt.headless=true", "-jar", JAR, "-de", DSN, "-do", SES, "-mp", "40"],
        cwd="/tmp/freerouting",
        check=False,
    )
    if proc.returncode != 0 or not os.path.exists(SES):
        raise SystemExit(f"freerouting falhou ({proc.returncode})")


def import_ses(board):
    pcbnew.ImportSpecctraSES(board, SES)
    board.BuildConnectivity()


def stitch_open_nets(board):
    """Fecha o que o autorroteador deixou, nas duas faces."""
    import re
    import subprocess
    import tempfile

    import stitch

    tmp = tempfile.NamedTemporaryFile(suffix=".kicad_pcb", delete=False)
    tmp.close()
    rpt = tempfile.NamedTemporaryFile(suffix=".rpt", delete=False)
    rpt.close()
    pcbnew.SaveBoard(tmp.name, board)
    subprocess.run(
        ["kicad-cli", "pcb", "drc", "--severity-error", "-o", rpt.name, tmp.name],
        check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    report = open(rpt.name, encoding="utf-8", errors="replace").read()
    blocks = report.split("[unconnected_items]")[1:]
    done = 0
    for block in blocks:
        hits = re.findall(
            r"@\(([0-9.]+) mm, ([0-9.]+) mm\): (?:Track|PTH pad|Via)[^\[]*\[([^\]]+)\]",
            block,
        )
        if len(hits) < 2 or hits[0][2] != hits[1][2]:
            continue
        ax, ay = float(hits[0][0]), float(hits[0][1])
        bx, by = float(hits[1][0]), float(hits[1][1])
        if stitch.route_pair(board, hits[0][2], ax, ay, bx, by):
            done += 1
            print(f"ligou {hits[0][2]}")
        else:
            print(f"sem caminho {hits[0][2]}")
    print(f"fechadas {done}/{len(blocks)}")


def add_ground_zone(board):
    net = board.FindNet("GND")
    zone = pcbnew.ZONE(board)
    zone.SetLayer(pcbnew.B_Cu)
    zone.SetNet(net)
    zone.SetAssignedPriority(0)
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    zone.SetThermalReliefGap(pcbnew.FromMM(0.5))
    zone.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.6))
    zone.SetMinThickness(pcbnew.FromMM(0.5))
    zone.SetLocalClearance(pcbnew.FromMM(0.4))
    zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in ((1.5, 1.5), (298.5, 1.5), (298.5, 298.5), (1.5, 298.5)):
        outline.Append(int(pcbnew.FromMM(x)), int(pcbnew.FromMM(y)))
    board.Add(zone)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())


def main():
    raw = build_nets()
    nets = collapse_aliases(raw)
    print(f"nets {len(nets)}  pins {sum(len(v) for v in nets.values())}")
    board = pcbnew.LoadBoard(BOARD)
    apply_nets(board, nets)
    missing = unconnected(board)
    print(f"pinos sem net: {len(missing)}")
    for item in missing:
        print(" ", item)
    if missing:
        raise SystemExit("netlist incompleta")
    pcbnew.SaveBoard(BOARD, board)
    export_dsn(board)
    print("dsn", os.path.getsize(DSN))
    run_router()
    print("ses", os.path.getsize(SES))
    board = pcbnew.LoadBoard(BOARD)
    import_ses(board)
    stitch_open_nets(board)
    add_ground_zone(board)
    pcbnew.SaveBoard(BOARD, board)
    tracks = 0
    for item in board.GetTracks():
        tracks += 1
    print(f"trilhas/vias {tracks}")


if __name__ == "__main__":
    main()
