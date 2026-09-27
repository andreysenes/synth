# VOZ-9 — lista de materiais

Caderno de estudo (o que cada peça é, faz, e o datasheet): `componentes.md`.

BOM SMT / LCSC para o [BOM Tool da JLCPCB](https://jlcpcb.com/parts/bom-tool): `jlcpcb-bom.csv` — como subir: `jlcpcb.md`.

Projeto de **reprodução**: tudo **novo**, um instrumento = uma compra. Nada de recuperar pedais, kits DaPia ou a placa roxa. Dá para montar de novo com a mesma lista.

Preços **estimados**, varejo Brasil, set/2026, **sem frete**. Pré vocal **sem transformador**. Combos **clone** (não Neutrik).

---

## Semicondutores

| Qtd | Peça | Vai para | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 8 | J201 TO-92 | FM A/B, noise, VCF, VCA, buffer + 2 folga | 4,00 | **32,00** |
| 2 | MP20 (ou AC128) | clipper + saturação da fita | 10,00 | **20,00** |
| 1 | 2N5457 | LFO | 4,00 | **4,00** |
| 1 | TL072 ou 4558 DIP-8 | OSC A + OSC B | 3,00 | **3,00** |
| 1 | TL072 ou 4558 DIP-8 | EQ NAB de pré de fita | 3,00 | **3,00** |
| 1 | TL072 DIP-8 | EQ voz 424 (LOW/MID/HIGH) | 3,00 | **3,00** |
| 3 | PT2399 DIP-16 | heads 1, 2 e 3 | 7,00 | **21,00** |
| 1 | 78M05 | 5 V dos 3 chips | 3,00 | **3,00** |
| 1 | MAX1044 | −9 V | 6,00 | **6,00** |
| 1 | NE5532 DIP-8 | pré de mic | 4,00 | **4,00** |
| 1 | 1N5817 | proteção da fonte | 0,80 | **0,80** |
| 4 | 1N4148 | GATE env + **fala→ENV** + detector CLK + trava Eurorack (D5) | 0,20 | **0,80** |
| 1 | LED 3 mm | piloto | 0,40 | **0,40** |

**101,00.** Sem 78L05: o 78M05 já é o regulador certo (~75 mA nos três PT2399). MP20 difícil: AC128, OC75, ou 1N34A / 1N60 se for *só* o diodo.

J201: 6 no circuito; os 2 extra casam Vgs(off). O mais “vivo” (conduz com gate mais baixo) vai no VCF; um par parecido nos FM dos oscs.

---

## Potenciômetros (16 mm)

| Qtd | Peça | Knob | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 2 | 500 kA | OSC A, OSC B | 6,00 | **12,00** |
| 2 | 100 kA | AMOUNT, CUTOFF | 6,00 | **12,00** |
| 1 | 1 kB | SHAPE | 6,00 | **6,00** |
| 1 | 100 kC | RATE (LFO) | 6,00 | **6,00** |
| 1 | A100 k | **PRE** (mic → SEND pré-EQ; sem XLR = pré dos oscs) | 6,00 | **6,00** |
| 1 | A100 k | **OSC IN** (mix osc ↔ XLR) | 6,00 | **6,00** |
| 4 | 100 kB | **EQ** LOW · MID F · MID G · HIGH (voz 424) | 6,00 | **24,00** |
| 1 | 10 kB | TIME | 6,00 | **6,00** |
| 1 | 25 kB | DEPTH | 6,00 | **6,00** |
| 1 | 2 kB | VOLUME | 6,00 | **6,00** |
| 1 | A100 k | WET | 6,00 | **6,00** |
| 1 | B100 k | F-BACK | 6,00 | **6,00** |
| 2 | trimpot 100 k | teto F-BACK / res | 2,00 | **4,00** |

**106,00.** No Brasil (Alpha): **A = log, B = lin, C = antilog**. PRE = nível (SEND pré-EQ); EQ voz = strip 424 **pós-mix**. MID F = freq, MID G = ganho.

---

## Knobs

| Qtd | Peça | Vai em | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 4 | Ø30 mm preto | OSC A, OSC B, TIME, F-BACK | 4,00 | **16,00** |
| 1 | Ø30 mm **vermelho** (chicken-head) | VOLUME | 8,00 | **8,00** |
| 12 | Ø15 mm preto | AMOUNT…WET + **LOW · MID F · MID G · HIGH** | 2,50 | **30,00** |

**54,00.** GATE é botão, não knob — capa vermelha na linha das chaves.

---

## Chaves

| Qtd | Peça | Vai para | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 5 | SPDT ON–ON MTS-102 | H1, H2, H3, STACK, DRONE/GATE | 3,50 | **17,50** |
| 2 | SPST ON–OFF MTS-101 | OSC A, OSC B | 3,50 | **7,00** |
| 2 | SPDT ON–OFF–ON MTS-103 | LFO MODE · **TREM** (tremolo / off / flutter) | 5,00 | **10,00** |
| 1 | botão momentâneo SPST + capa vermelha | GATE | 5,00 | **5,00** |

**39,50.** MTS-203 (ON–ON–ON) **não** serve no MODE nem no TREM — use MTS-103.

---

## Conectores e cabos

| Qtd | Peça | Vai para | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 11 | jack P2 3,5 mm estéreo chaveado | patch + CLK (A B IN FILT FCV VCV LFO ECV CLK SEND RCV) | 3,00 | **33,00** |
| 4 | cabo P2 curto | patch | 4,50 | **18,00** |
| 2 | combo XLR+P10 **clone** | IN e OUT | 22,00 | **44,00** |
| 1 | P4 (jack 9 V DC) | fonte, centro-negativo | 3,00 | **3,00** |
| 4 | barra de pinos macho **1×40** 2,54 mm | cortar J1–J9 (124 pinos) na borda da BASE | 3,00 | **12,00** |
| 1 | fio 24 AWG 10 m (várias cores) | fios do painel até os pinos J1–J9 | 8,00 | **8,00** |

**~120** a menos que a lista antiga de housings: saíram soquete fêmea, macho e crimp. O fio solda no pino. Clone XLR continua fêmea nos dois furos — isso é o painel, não a placa. **J7** = 1×12 (combo + PRE + **OSC IN**; pino 12 NC). **J9** = EQ 424.

---

## Resistores — filme ¼ W

Lista do circuito **inteiro**. ~R$ 0,10–0,25 a unidade. Pacote fechado ~**16,00**.

| Valor | Qtd | Onde |
| --- | ---: | --- |
| 220 Ω | 2 | pad XLR OUT (quente e frio) |
| 1 k | 8 | noise S, LFO S, buffer S, 5532-B, H2 pin 6 (2×), H3 pin 6 (2×) |
| 2 k | 1 | H1 pin 6 (anti-latch) |
| 2k2 **1 %** | 2 | diferencial do 5532 |
| 4k7 | 4 | LED, série do RATE, teto do shelf NAB GRAVA, folga |
| 5k6 | 1 | divisor 1V8 |
| 10 k | 36 | 4V5 (2), pitch (2), mix A/B (2), noise D, EXT, buffer (2), SHAPE, VCF, VCA S, LFO D, LFO fase (2), pin 16 ×3, mix H1–H3 (3), laço, **teto WET (R71)**, 5532-B, CLK, pad, NAB LÊ grave, VCA→GRAVA, **série fala→ENV**, **EQ Baxandall (R82 R83)**, **EQ mid (R84)** |
| 15 k | 4 | NAB GRAVA (Zin + feedback) + NAB LÊ (Zin + feedback) |
| 22 k | 2 | 1V8, H2 pin 6 |
| 22 k **1 %** | 2 | diferencial do 5532 |
| 3k3 | 1 | **EQ MID F** (série no pot) |
| 47 k | 1 | CLK série |
| 68 k | 2 | H3 pin 6, ressonância VCF |
| 100 k | 10 | histerese A (2), noise mix, FM A/B (2), FCV, VCF, VCV, CLK, **bias U9 (R85)** |
| 220 k | 8 | histerese B (2), decay GATE, pin 6 LFO/ECV (3), sangria CLK |
| 1 M | 2 | gate noise, gate LFO |

---

## Capacitores

| Valor | Tipo | Qtd | Onde | Unit. | Sub |
| --- | --- | ---: | --- | ---: | ---: |
| 100 p | cerâmico C0G | 2 | RF no XLR IN | 0,30 | **0,60** |
| 1 n | filme / C0G | 1 | **EQ HIGH** shelf (~10 kHz) | 0,40 | **0,40** |
| 2 n2 | filme | 1 | LPF do mix molhado | 0,50 | **0,50** |
| 3,3 n | filme | 2 | NAB 50 µs (GRAVA + LÊ) | 0,50 | **1,00** |
| 10 n | filme / cerâmico | 13 | OSC B; LPF laço; filtros PT2399; **EQ MID** | 0,35 | **4,55** |
| 22 n | filme | 1 | laço “fita gasta” (opcional no lugar do 10 n) | 0,50 | **0,50** |
| 33 n | filme | 1 | **EQ LOW** shelf (~100 Hz) | 0,50 | **0,50** |
| 100 n | cerâmico / filme | 27 | OSC A; acoplos; VCC PT2399; 5532; fala→ENV; **EQ in/out (2)** | 0,40 | **10,80** |
| 220 n | filme | 8 | LFO fase (3); Csel tremolo; VCF; NAB grave GRAVA+LÊ (2); folga | 0,50 | **4,00** |
| 1 µ | filme | 2 | saída OSC A e B | 1,50 | **3,00** |
| 1 µ / 2µ2 | eletrolítico | 2 | saída LFO; saída VCA | 0,50 | **1,00** |
| 4 µ7 | eletrolítico | 1 | detector CLK | 0,50 | **0,50** |
| 10 µ / **25 V** | eletrolítico | 8 | MAX1044 (2); 78M05; V5 H2+H3 (2); XLR (2); 5532 ± | 0,60 | **4,80** |
| 47 µ / 16 V | eletrolítico | 8 | V9, VEE, 4V5, 1V8, envelope, H2, H3, Csel flutter | 0,70 | **5,60** |

**37,75.** Polaridade: eletrolítico, listra = negativo. 25 V no XLR e no MAX1044. EQ voz: 33 n / 1 n / 10 n + 2× 100 n (`esquema.md` §3b).

---

## Placas, soquetes, caixa

| Qtd | Peça | Por quê | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 1 | fenolite simples 300×300 mm | PCB BASE | 12,00 | **12,00** |
| 5 | soquete DIP-8 | U1 5532 · U2 osc · U3 NAB · U4 7660 · **U9 EQ voz** | 1,50 | **7,50** |
| 3 | soquete DIP-16 | PT2399 H1, H2 e H3 | 1,50 | **4,50** |
| 1 | caixa com piso ≥ 300×300 mm + face 220×160 | mesa estilo Toaster; a BASE é maior que a face | 80,00 | **80,00** |

**104,00.** Uma placa no piso. CIs nos soquetes. Sem FACE, sem IDC, sem flat. O pré é o NE5532 em diferencial; a saída XLR é pad + quase-balanceado (`pre-vocal.md`).

---

## Totais (sem frete)

| Pacote | Soma |
| --- | ---: |
| Semicondutores | 101 |
| Pots | 106 |
| Knobs | 54 |
| Chaves | 40 |
| Conectores | 117 |
| Resistores | 16 |
| Capacitores | 38 |
| Placas / caixa | 104 |
| **Um VOZ-9, tudo novo** | ~ **576** |

Fonte 9 V centro-negativo (~R$ 25–40) se ainda não tiver uma. Não entra na soma: a de pedal serve.

Para **N** instrumentos, multiplique a tabela. Não há peça “única do fundo da gaveta”.

Referências de rua: PT2399 ~R$ 5–10 (Supercomp / Achei); combo clone XLR+P10 ~R$ 20–25; MTS-102 ~R$ 3–8; MP20 / AC128 ~R$ 8–15.

---

## Se já tiver os kits (não é o caminho)

Tweed ’57, Fuzz Face e Glam Chorus cobrem parte dos pots, um PT2399, o MAX1044, o 2N5457, os MP20 e um tanto de R/C. Isso **não** é a receita do projeto: a lista de cima é a que se pede de novo. A placa roxa (*Advanced Vococal Echo*) também fica de fora — jacks, pots e soquetes vêm desta BOM.
