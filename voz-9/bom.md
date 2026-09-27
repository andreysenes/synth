# VOZ-9 — lista de materiais

Caderno de estudo (o que cada peça é, faz, e o datasheet): `componentes.md`.

BOM SMT / LCSC para o [BOM Tool da JLCPCB](https://jlcpcb.com/parts/bom-tool): `jlcpcb-bom.csv` — como subir: `jlcpcb.md`.

Projeto de **reprodução**: tudo **novo**, um instrumento = uma compra. Nada de recuperar pedais, kits DaPia ou a placa roxa. Dá para montar de novo com a mesma lista. O VCO cromático (faixa de baixo, chicote J10) entra nesta lista — não é outro módulo.

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
| 4 | 1N4148 | GATE env + **fala→ENV** + CLK + folga | 0,20 | **0,80** |
| 1 | LED 3 mm | piloto | 0,40 | **0,40** |
| 1 | AS3340 ou V3340 DIP-16 | VCO cromático (mesma BASE) | 55,00 | **55,00** |
| 1 | MC34063 DIP-8 | 9 V → 15 V do VCO | 3,00 | **3,00** |
| 1 | 78L12 TO-92 | +12 V, pino 16 | 2,00 | **2,00** |
| 1 | 78L05 TO-92 | +5 V (COARSE, PW, pino 13) | 2,00 | **2,00** |
| 1 | 79L05 TO-92 | −5 V, pino 3 | 2,00 | **2,00** |
| 1 | 1N5819 | diodo do step-up | 1,00 | **1,00** |

**166,00.** Sem segundo MAX1044 e sem segundo P4: o −9 V é o que o instrumento já gera. Sem 78L05 extra no lugar do 78M05 — o 78M05 continua sendo o regulador dos PT2399 (~75 mA). O 78L05 da tabela é só a referência quieta do AS3340. MP20 difícil: AC128, OC75, ou 1N34A / 1N60 se for *só* o diodo.

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
| 3 | 100 kB | **COARSE**, FINE, PW | 6,00 | **18,00** |
| 1 | 100 kA | **FM** (LFO interno → pino 15) | 6,00 | **6,00** |
| 1 | multiturn 500 Ω | SCALE (1 V/oitava) | 3,50 | **3,50** |
| 1 | multiturn 10 k | TEMP | 3,50 | **3,50** |
| 2 | multiturn 100 k | RANGE, HF | 3,50 | **7,00** |
| 1 | multiturn 200 k | REF | 3,50 | **3,50** |

**147,50.** No Brasil (Alpha): **A = log, B = lin, C = antilog**. PRE = nível (SEND pré-EQ); EQ voz = strip 424 **pós-mix**. MID F = freq, MID G = ganho. COARSE é B de propósito: volt linear = oitava linear. Os cinco multiturn ficam na placa, não no painel.

---

## Knobs

| Qtd | Peça | Vai em | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 4 | Ø30 mm preto | OSC A, OSC B, TIME, F-BACK | 4,00 | **16,00** |
| 1 | Ø30 mm **vermelho** (chicken-head) | VOLUME | 8,00 | **8,00** |
| 12 | Ø15 mm preto | AMOUNT…WET + **LOW · MID F · MID G · HIGH** | 2,50 | **30,00** |
| 1 | Ø30 mm preto | **COARSE** | 4,00 | **4,00** |
| 3 | Ø15 mm preto | FINE, PW, FM | 2,50 | **7,50** |

**65,50.** GATE é botão, não knob — capa vermelha na linha das chaves.

---

## Chaves

| Qtd | Peça | Vai para | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 8 | SPDT ON–ON MTS-102 | H1, H2, H3, STACK, DRONE/GATE, **SAW, TRI, PUL** | 3,50 | **28,00** |
| 2 | SPST ON–OFF MTS-101 | OSC A, OSC B | 3,50 | **7,00** |
| 2 | SPDT ON–OFF–ON MTS-103 | LFO MODE · **TREM** (tremolo / off / flutter) | 5,00 | **10,00** |
| 1 | botão momentâneo SPST + capa vermelha | GATE | 5,00 | **5,00** |

**50,00.** MTS-203 (ON–ON–ON) **não** serve no MODE nem no TREM — use MTS-103. SAW, TRI e PUL são ON–ON: cada uma liga aquela saída do AS3340 no mix. As três off = VCO fora do áudio. Mais de uma on = as ondas somam.

---

## Conectores e cabos

| Qtd | Peça | Vai para | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 12 | jack P2 3,5 mm estéreo chaveado | patch + CLK + **CV** (A B IN FILT FCV VCV LFO ECV CLK SEND RCV CV) | 3,00 | **36,00** |
| 4 | cabo P2 curto | patch | 4,50 | **18,00** |
| 2 | combo XLR+P10 **clone** | IN e OUT | 22,00 | **44,00** |
| 1 | P4 (jack 9 V DC) | fonte, centro-negativo | 3,00 | **3,00** |
| 4 | soquete fêmea **2×10** 2,54 mm | J1 OSC · J3 DELAY · J4 PATCH A · **J10 VCO** | 2,50 | **10,00** |
| 1 | soquete fêmea **2×8** 2,54 mm | J5 PATCH B | 2,20 | **2,20** |
| 3 | soquete fêmea **2×6** 2,54 mm | J2 LFO · J7 IN · **J9 EQ** | 2,00 | **6,00** |
| 2 | soquete fêmea **2×3** 2,54 mm | J6 CTRL · J8 OUT | 1,50 | **3,00** |
| 4 | housing macho **2×10** | chicotes J1 J3 J4 **J10** | 2,00 | **8,00** |
| 1 | housing macho **2×8** | J5 | 1,80 | **1,80** |
| 3 | housing macho **2×6** | J2 · J7 · **J9** | 1,60 | **4,80** |
| 2 | housing macho **2×3** | J6 J8 | 1,20 | **2,40** |
| 140 | terminal crimp macho 2,54 mm | pinos (144 usados) | 0,10 | **14,00** |
| 1 | fio 24 AWG 10 m (várias cores) | fios dos **10** chicotes J1–J10 | 8,00 | **8,00** |

**161.** Clone é fêmea nos dois furos. Confira o furo (~24 mm). Família 2×N: fêmea na placa, macho no painel. **J7** = 2×6 (combo + PRE + **OSC IN**; pino 12 NC). **J9** = EQ 424. **J10** = 2×10 (COARSE, FINE, PW, FM, SAW, TRI, PUL, CV).

---

## Resistores — filme ¼ W

Lista do circuito **inteiro**. ~R$ 0,10–0,25 a unidade.

| Valor | Qtd | Onde |
| --- | ---: | --- |
| 220 Ω | 2 | pad XLR OUT (quente e frio) |
| 1 k | 8 | noise S, LFO S, buffer S, 5532-B, H2 pin 6 (2×), H3 pin 6 (2×) |
| 2 k | 1 | H1 pin 6 (anti-latch) |
| 2k2 **1 %** | 2 | diferencial do 5532 |
| 4k7 | 4 | LED, série do RATE, teto do shelf NAB GRAVA, folga |
| 5k6 | 1 | divisor 1V8 |
| 10 k | 35 | 4V5 (2), pitch (2), mix A/B (2), noise D, EXT, buffer (2), SHAPE, VCF, VCA S, LFO D, LFO fase (2), pin 16 ×3, mix H1–H3 (3), laço / teto WET, 5532-B, CLK, pad, NAB LÊ grave, VCA→GRAVA, **série fala→ENV**, **EQ Baxandall (2)** |
| 15 k | 4 | NAB GRAVA (Zin + feedback) + NAB LÊ (Zin + feedback) |
| 22 k | 2 | 1V8, H2 pin 6 |
| 22 k **1 %** | 2 | diferencial do 5532 |
| 3k3 | 1 | **EQ MID F** (série no pot) |
| 47 k | 1 | CLK série |
| 68 k | 2 | H3 pin 6, ressonância VCF |
| 100 k | 10 | histerese A (2), noise mix, FM A/B (2), FCV, VCF, VCV, CLK |
| 220 k | 8 | histerese B (2), decay GATE, pin 6 LFO/ECV (3), sangria CLK |
| 1 M | 2 | gate noise, gate LFO |

Pacote do instrumento sem o VCO ~**16,00**. O VCO acrescenta o pacote abaixo (~**8,00**). Total de resistores ~**24**.

### VCO — filme ¼ W (mesma placa)

1 % onde marcado. O 100 k do CV é o resistor da oitava: fique com o que medir mais perto de 100,0 k.

| Valor | Qtd | Onde |
| --- | ---: | --- |
| 0,47 Ω | 1 | Rsc do MC34063 |
| 470 Ω | 1 | compensação do pino 15 |
| 1 k | 4 | série SAW, TRI, PUL, PWM |
| 1k2 **1 %** | 2 | divisor do 15 V |
| 1k5 **1 %** | 1 | Rs, em série com o SCALE |
| 5k6 **1 %** | 2 | tempco, pinos 1 e 2 |
| 10 k | 4 | pulldown do pulso + mix SAW/TRI/PUL |
| 12 k **1 %** | 1 | divisor do 15 V, ramo de cima |
| 100 k **1 %** | 3 | CV, COARSE, FM → pino 15 |
| 100 k | 1 | hard sync → GND |
| 180 k **1 %** | 1 | RANGE, série com o trim |
| 330 k **1 %** | 1 | REF, série com o trim |
| 1M5 **1 %** | 1 | FINE → pino 15 |
| 2M2 | 1 | HF → pino 15 |

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
| 470 p | cerâmico | 1 | Ct do MC34063 | 0,30 | **0,30** |
| 1 n | C0G / filme 1 % | 1 | tempo do AS3340, pino 11 | 1,50 | **1,50** |
| 10 n | filme | 2 | pino 13, pino 15 | 0,40 | **0,80** |
| 100 n | cerâmico | 6 | V12, V15, −5, pino 9, pino 16, pino 6 do 34063 | 0,40 | **2,40** |
| 1 µ | filme | 3 | SAW, TRI, PUL (antes da chave) | 1,50 | **4,50** |
| 10 µ / 25 V | eletrolítico | 6 | 78L12, 78L05, 79L05 (entrada e saída) | 0,60 | **3,60** |
| 100 µ / 25 V | eletrolítico | 1 | V15 | 1,00 | **1,00** |
| 220 µH ≥ 500 mA | indutor | 1 | step-up | 4,00 | **4,00** |

**55,85.** Polaridade: eletrolítico, listra = negativo. 25 V no XLR e no MAX1044. EQ voz: 33 n / 1 n / 10 n + 2× 100 n (`esquema.md` §3b). O 1 nF do pino 11 é C0G ou poliestireno — X7R aí desafina. O V15 e o −5 V são locais do VCO; o 47 µ de V9 e de VEE já está na linha de cima.

---

## Placas, soquetes, caixa

| Qtd | Peça | Por quê | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 1 | fenolite simples 250×250 mm | PCB BASE (cortar 220×216) | 16,00 | **16,00** |
| 6 | soquete DIP-8 | U1 5532 · U2 osc · U3 NAB · U4 7660 · **U9 EQ** · **U11 MC34063** | 1,50 | **9,00** |
| 4 | soquete DIP-16 | PT2399 H1, H2, H3 · **U10 AS3340** | 1,50 | **6,00** |
| 1 | caixa madeira ~240×236×50 mm + face 220×216 | mesa estilo Toaster | 90,00 | **90,00** |

**121,00.** Uma placa no piso, agora alta o bastante para a faixa do VCO. CIs nos soquetes. Sem FACE, sem IDC, sem flat, sem segunda caixa. O pré é o NE5532 em diferencial; a saída XLR é pad + quase-balanceado (`pre-vocal.md`). 78L12, 78L05 e 79L05 não usam soquete.

---

## Totais (sem frete)

| Pacote | Soma |
| --- | ---: |
| Semicondutores | 166 |
| Pots | 148 |
| Knobs | 66 |
| Chaves | 50 |
| Conectores | 161 |
| Resistores | 24 |
| Capacitores | 56 |
| Placas / caixa | 121 |
| **Um VOZ-9, tudo novo** | ~ **792** |

Fonte 9 V centro-negativo (~R$ 25–40) se ainda não tiver uma. Não entra na soma: a de pedal serve.

Para **N** instrumentos, multiplique a tabela. Não há peça “única do fundo da gaveta”.

Referências de rua: PT2399 ~R$ 5–10 (Supercomp / Achei); combo clone XLR+P10 ~R$ 20–25; MTS-102 ~R$ 3–8; MP20 / AC128 ~R$ 8–15.

---

## Se já tiver os kits (não é o caminho)

Tweed ’57, Fuzz Face e Glam Chorus cobrem parte dos pots, um PT2399, o MAX1044, o 2N5457, os MP20 e um tanto de R/C. Isso **não** é a receita do projeto: a lista de cima é a que se pede de novo. A placa roxa (*Advanced Vococal Echo*) também fica de fora — jacks, pots e soquetes vêm desta BOM.
