# VOZ-9 — uma placa no piso

Uma fenolite no **fundo da caixa**. O painel (`painel.svg`) é só chapa. **Nove** chicotes 2×N (2,54 mm): **fêmea na BASE**, **macho no painel**. CIs só em soquete. Sem FACE, sem flat, sem IDC.

| Placa | Arquivo | Tamanho | Cobre | O que leva |
| --- | --- | --- | --- | --- |
| **BASE** | `pcb.svg` | **220 × 160 mm** | simples, solda = verso | fonte, oscs, JFETs, NAB, 5532, EQ voz, fita, R/C, pads dos cabos |

Imprimir o SVG em **escala 100 %**. Para transferência térmica, espelhar o cobre.

```
          ┌──────── painel 220×160 ────────┐
          │  knobs / chaves / jacks / XLR  │
          │         (só furo + porca)      │
          └──────────────┬─────────────────┘
                         │ cabos 8–12 cm
          ┌──────────────┴─────────────────┐
          │  J1–J9 fêmea · fonte oscs fita │
          │     PCB 220×160  (R+C+CIs)     │
          └────────────────────────────────┘
            piso da caixa ~240×180×50
```

O painel parafusa na face 220 × 160. A placa parafusa no fundo (M3 nos quatro cantos). Cabos folgados, sem esticar.

---

## O que mora onde

### Painel (não é PCB)

Furos em `painel.svg`. Nada de cobre atrás da chapa.

- 17 pots, 9 alavancas, GATE, LED, P4, 11× P2, 2× combo
- 100 p de RF **também no combo IN** (pino 2 e 3 → massa). Na placa: C1 e C2, no bloco U1.

### BASE (`pcb.svg`)

Chicotes na coluna esquerda (**J1–J9**, fêmea 2×N). Circuito à direita. Gerador: `_gen_pcb.py`.

- soquetes DIP: U1 5532, U2 osc, U3 NAB, U4 7660, U6–U8 PT2399, **U9 EQ voz** — **não soldar o chip**
- 1N5817, 78M05 (sem soquete — TO-220)
- 6× J201, 2N5457, 2× MP20, 1N4148
- Csel (220 n / 47 µ) e detector CLK
- **2×** trimpot 100 k (RV1 F-BACK, RV2 res)
- **J1–J9** fêmea 2,54 mm 2×N — macho vem do painel

O **VU de saída** (U10 + R82–R87 + C72–C75 + D6/D7 + RV3) **não** entra na BASE — ela já está cheia. Mora numa ilhada atrás do meter e puxa TIP · GND · V9 · VEE do **J8** (agora 2×4). Esquema: `esquema.md` §9.

---

## Chicotes painel → BASE

Família: housing **dupla fila, passo 2,54 mm**. Fêmea na BASE, macho no painel.

| J | Tamanho | Vias | Grupo |
| --- | --- | ---: | --- |
| **J1** | 2×10 | 20 | OSC |
| **J2** | 2×6 | 12 | LFO |
| **J3** | 2×10 | 20 | DELAY |
| **J4** | 2×10 | 20 | PATCH A |
| **J5** | 2×8 | 16 | PATCH B |
| **J6** | 2×3 | 6 | CTRL (LED, P4, GATE) |
| **J7** | 2×6 | 12 | combo IN + PRE + OSC IN |
| **J8** | 2×4 | 8 | combo OUT + alimenta o VU |
| **J9** | 2×6 | 12 | EQ voz 424 |

Pino **1** = pad quadrado + lingueta. Não cruze os machos. Marque cada housing.

Três pernas de pot: **CCW · W · CW**. Reostato OSC A/B: **A · B**. Jack: **TIP · SW · GND**.

### J1 OSC — 2×10 (19 usados)

| Pino | Sinal |
| ---: | --- |
| 1–2 | OSC A A · B |
| 3–4 | OSC B A · B |
| 5–7 | AMOUNT CCW · W · CW |
| 8–10 | SHAPE CCW · W · CW |
| 11–13 | CUTOFF CCW · W · CW |
| 14–15 | chave A COM · ON |
| 16–17 | chave B COM · ON |
| 18–19 | DRONE COM · ON |
| 20 | NC |

### J2 LFO — 2×6 (12, cheio)

| Pino | Sinal |
| ---: | --- |
| 1–3 | RATE CCW · W · CW |
| 4–6 | DEPTH CCW · W · CW |
| 7–9 | TREM COM · A (220 n) · B (47 µ) — ON–OFF–ON; centro = off |
| 10–12 | MODE COM · PITCH · TIME |

Csel 220 n / 47 µ fica **na BASE**. RATE W = gate do LFO.

### J3 DELAY — 2×10 (20, cheio)

No painel, da esquerda: **TIME · WET · F-BACK · H1 · H2 · H3 · STACK** | VOLUME.  
Pinagem do chicote (estável com o SPICE / `jmap.inc`):

| Pino | Sinal |
| ---: | --- |
| 1–3 | TIME CCW · W · CW |
| 4–5 | H1 COM · ON |
| 6–7 | H2 COM · ON |
| 8–9 | H3 COM · ON |
| 10–12 | F-BACK CCW · W · CW |
| 13–15 | WET CCW · W · CW |
| 16–17 | STACK COM · ON |
| 18–20 | VOLUME CCW · W · CW |

Ao crimpar o macho do painel, siga a tabela — não a ordem física dos knobs.

### J4 PATCH A — 2×10 (18 usados)

A · B · IN · FILT · FCV · VCV — cada um **TIP · SW · GND**. FILT usa o SW.

| Pino | Jack |
| ---: | --- |
| 1–3 | A |
| 4–6 | B |
| 7–9 | IN |
| 10–12 | FILT |
| 13–15 | FCV |
| 16–18 | VCV |
| 19–20 | NC |

### J5 PATCH B — 2×8 (15 usados)

| Pino | Jack |
| ---: | --- |
| 1–3 | LFO |
| 4–6 | ECV |
| 7–9 | CLK |
| 10–12 | SEND |
| 13–15 | RCV |
| 16 | NC |

CLK ponta → detector na BASE → mesmo nó do ECV. SEND = PRE (pré-EQ / pré-OSC IN).

### J6 CTRL — 2×3

| Pino | Sinal |
| ---: | --- |
| 1–2 | LED A · K |
| 3–4 | P4 TIP · GND |
| 5–6 | GATE NA · GND |

P4: centro-negativo. **Confira no jack.** 1N5817 na BASE, no pino 3 (TIP).

### J7 combo IN + PRE + OSC IN — 2×6

| Pino | Sinal |
| ---: | --- |
| 1–5 | X2 · X3 · X1 · TIP · GND |
| 6–8 | PRE CCW · W · CW |
| 9–11 | OSC IN CCW · W · CW |
| 12 | NC |

100 p de RF no combo (e C1 C2 na placa). PRE = nível; OSC IN = mix osc ↔ XLR (`pre-vocal.md`).

### J8 combo OUT — 2×4

| Pino | Sinal |
| ---: | --- |
| 1–5 | X2 · X3 · X1 · TIP · GND |
| 6 | V9 (alimenta o VU) |
| 7 | VEE (alimenta o VU) |
| 8 | NC |

O TIP (pino 4, pós-VOLUME) é o sinal que o VU mede. A plaquinha do VU (U10) fica **atrás do meter** e puxa TIP · GND · V9 · VEE deste chicote (`esquema.md` §9).

### J9 EQ voz 424 — 2×6

| Pino | Sinal |
| ---: | --- |
| 1–3 | LOW CCW · W · CW |
| 4–6 | MID F CCW · W · CW |
| 7–9 | MID G CCW · W · CW |
| 10–12 | HIGH CCW · W · CW |

Shelf 100 Hz / peaking 250 Hz–5 kHz / shelf 10 kHz — `esquema.md` §3b.

---

## Furos do painel (`painel.svg`)

Coordenadas em mm, origem no canto superior esquerdo.

| Peça | X | Y | Furo |
| --- | ---: | ---: | --- |
| COMBO IN | 20 | 21 | 24 |
| PRE | 48 | 21 | 7,5 |
| OSC IN | 72 | 21 | 7,5 |
| LED | 96 | 21 | 3,2 |
| P4 9 V | 110 | 21 | 8,0 |
| COMBO OUT | 200 | 144 | 24 |
| LOW | 18 | 50 | 7,5 |
| MID F | 40 | 50 | 7,5 |
| MID G | 62 | 50 | 7,5 |
| HIGH | 84 | 50 | 7,5 |
| RATE | 18 | 74 | 7,5 |
| TREM (3 pos) | 40 | 74 | 6,0 |
| LFO MODE | 62 | 74 | 6,0 |
| DEPTH | 84 | 74 | 7,5 |
| OSC A | 128 | 36 | 7,5 |
| AMOUNT | 156 | 36 | 7,5 |
| OSC B | 184 | 36 | 7,5 |
| OSC A on | 116 | 76 | 6,0 |
| OSC B on | 130 | 76 | 6,0 |
| SHAPE | 148 | 76 | 7,5 |
| CUTOFF | 166 | 76 | 7,5 |
| DRONE/GATE | 184 | 76 | 6,0 |
| GATE | 198 | 76 | 7,0 |
| VU (saída) | 150 | 61 | recorte ~30×11 |
| TIME | 26 | 112 | 7,5 |
| WET | 52 | 112 | 7,5 |
| F-BACK | 84 | 112 | 7,5 |
| H1 / H2 / H3 | 114 / 132 / 150 | 112 | 6,0 |
| STACK | 168 | 112 | 6,0 |
| VOLUME | 198 | 112 | 7,5 |
| A … RCV (11 jacks) | 16 + n×15 | 144 | 6,0 |
| parafusos M3 (painel) | 6 / 214 | 6 / 154 | 3,2 |

Knobs: OSC A/B, TIME, F-BACK, VOLUME = Ø30 mm. AMOUNT, SHAPE, CUTOFF, RATE, PRE, OSC IN, DEPTH, WET, LOW, MID F, MID G, HIGH = Ø15 mm.

Parafusos da **BASE**: M3 em (4, 4), (216, 4), (4, 156), (216, 156).

---

## R e C na placa

Mesmos designators do `jlcpcb-bom.csv` + bloco EQ. Axial ¼ W, passo **7,62 mm**. Filme/cerâmico, passo **5,08 mm**. Eletrolítico: **+ à esquerda**.

| Bloco | Resistores | Capacitores |
| --- | --- | --- |
| FONTE | R14 R17 4k7 · R19 R20 10k · R18 5k6 · R55 22k | C22 100n · C64–C67 47µ · C56–C58 10µ |
| U1 5532 | R12 R13 2k2 · R57 R58 22k · R6 1k · R42 R44 10k · R1 R2 220 | C1 C2 100p · C23–C25 100n · C59–C63 10µ |
| U2 OSC | R21 R22 10k · R62 R63 100k · R72 220k | C21 C19 100n · C6 10n |
| MIX SHAPE FM | R23–R29 10k · R3 R4 1k · R64–R66 100k · R80 1M · R73 220k | C26 100n · C51 C52 1µ |
| VCF VCA LFO | R30–R34 10k · R67–R69 100k · R61 68k · R5 1k · R15 4k7 · R74 220k · R81 1M | C43–C47 220n |
| CLK TIME | R59 47k · R43 10k · R70 100k · R79 220k · R11 2k · R7–R10 1k · R56 22k · R60 68k | C55 4µ7 |
| U3 NAB | R51–R54 15k · R16 4k7 · R45 R46 10k | C4 C5 3n3 · C48–C50 220n · C20 C29 C30 100n |
| **U9 EQ** | 2× 10k Baxandall · 3k3 MID F · 10k mid | 33n LOW · 1n HIGH · 10n MID · 2× 100n acoplo |
| ENV | | C27 C28 100n · C68 C71 47µ · C53 C54 2µ2 |
| FITA | R35–R41 R47–R50 10k · R71 100k · R75–R78 220k | C3 2n2 · C7–C17 10n · C18 22n · C31–C42 100n · C69 C70 47µ |

Trimpots na BASE: RV1 teto F-BACK, RV2 ressonância. RV3 (10 k) = calibração do VU, na ilhada atrás do meter (`esquema.md` §9).

O **VU** não aparece na tabela: U10 + R82–R87 + C72–C75 + D6/D7 + RV3 ficam atrás do meter, alimentados pelo J8 2×4.

---

## Como gravar

1. Imprime `pcb.svg` em laser, **100 %**, sem “ajustar à página”.
2. Lado **COBRE**: espelha. Lado **SILK**: não espelha.
3. Fenolite simples. Furos: 0,8 mm nos J1–J9 e R/C, 1,0 mm nos soquetes DIP, 3,2 mm nos M3.
4. Jumpers no lado dos componentes (tracejado no SVG).
5. Solda **soquetes DIP** (incl. **U9**) e **fêmeas J1–J9**. Depois JFET/germânio. CIs e chicotes macho **por último**.

Antes de ligar 9 V: ohmímetro entre J6 pino 4 (P4-GND) e a malha do combo. Tem de ser contínuo. J6 pino 3 (P4-TIP) **não** pode achar GND.

---

## Ordem de teste

1. Só a BASE, sem cabos de áudio: P4 → 9 V, −9 V, 5 V, 4V5, 1V8. LED no pad.
2. Cabos dos pots. OSC A, OSC B, batimento. OSC IN no CCW.
3. SHAPE, CUTOFF, GATE/DRONE.
4. LFO. TREM (tremolo / off / flutter).
5. 5532 + combo IN + PRE + OSC IN (mix). SM58, PRE a meio → SEND ~150–300 mV.
6. U9 EQ 424: LOW/HIGH/MID — meio = flat.
7. TL072 NAB: VCA → GRAVA → H1 → LÊ. Sem o chip o eco some.
8. PT2399 os três. Combos e patch por último.

Esquema: `esquema.md`. Pré: `pre-vocal.md`.
