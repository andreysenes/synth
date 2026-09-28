# VOZ-9

Synth de mesa semi-modular em 9 V. Dois osciladores batendo, waveshaper de germânio, filtro, VCA com decay e fita de **três heads** (3× PT2399: flutter + saturação + repeats escuros). Família Look Mum No Computer / Noise Toaster / Ciat-Lonbarde.

A cadeia interna já toca sozinha. Os jacks só quebram ou desviam o fluxo.

```
 MIC ── XLR IN ── 5532 ── PRE ──┬── SEND (pré-EQ) ── RCV / fita
                                └── OSC IN (CW) ──┐
 OSC A/B/noise ──────────────────── OSC IN (CCW) ─┴── mix
                                                      │
                                                 EQ 424 → SHAPE → VCF → VCA
                                                      │
                                                 NAB → FITA → WET → VOLUME → OUT
```

Sem XLR, **PRE** escala os oscs. **OSC IN** = mix osc ↔ mic (CCW = só drones, CW = só voz).

O pré vocal está em `pre-vocal.md`. Mesmo papel do Echo Master, **sem transformador** (diferencial no NE5532 + pad no XLR).

Leia `esquema.md` para montar. Caderno de estudo: `componentes.md`. A referência
artesanal THT/fenolite está em `pcb.md`; o baseline KiCad atual é FR-4 de duas
camadas com PCBA SMD JLCPCB e montagem manual do restante. Para trabalhar no
KiCad via MCP, comece por `kicad-requisitos.md` e depois siga
`kicad-layout-agent.md`. Lista de compra: `bom.md`. Simulador:
`sim/painel.html`.

O baseline KiCad acrescenta um **VU analógico compacto de saída**: frontal
nominal 37 × 35 × 35 mm, 21 g, movimento 500 µA/630 Ω e iluminação quente por
filamento 6–12 V, sempre ligada com o equipamento. O chicote J10 separa
movimento e lâmpada. **0 VU = 0 dBV = 1,000 Vrms** pós-VOLUME/pré-pads.
Balística alvo de VU clássico: aproximadamente 300 ms, sem peak-hold. Recorte,
dimensões, consumo e resposta reais serão confirmados numa amostra antes de
atualizar `painel.svg`. O LED CLIP acende 1 dB antes do clipping real medido e
retém a indicação por aproximadamente 150 ms.

Também acrescenta nove indicadores em J11: **CLIP, GATE/ENV, LFO, OSC A/B,
H1–H3 e STACK**. Com o POWER existente, são **10 LEDs vermelhos difusos de
3 mm e baixo consumo**, com alvo de **1,5 mA por LED**. Lógica e polos das
chaves serão definidos antes do painel/BOM finais; CLIP, GATE/ENV e LFO usam
drivers discretos SMD, sem firmware. O brilho de GATE/ENV acompanha ataque e
decay do envelope; LFO pisca de forma binária e apaga com TREM no centro/OFF.

---

## Painel

**Um módulo só**, caixa de mesa. A referência legada usa faceplate **220 × 160 mm**; o baseline KiCad usa faceplate **300 × 300 mm** e caixa externa a ela. A BASE mede **200 × 150 mm** e fica no fundo. J1–J9 são a referência legada; o baseline acrescenta **J10 para o VU analógico e J11 para indicadores**.

```
 IN  PRE  OSC IN | LED 9V          OSC A  AMOUNT  OSC B
 LOW  MID F  MID G  HIGH           A  B  SHAPE  CUTOFF  DRONE  GATE
 RATE  TREM  MODE  DEPTH
 TIME  WET  F-BACK  H1  H2  H3  STACK     |  VOLUME
 A B IN FILT FCV VCV LFO ECV CLK SEND RCV |  OUT
```

- **Esquerda:** entrada + EQ + LFO. XLR no canto superior esquerdo.
- **Direita:** osciladores + A/B/SHAPE/CUTOFF/DRONE/GATE.
- **Delay:** TIME · WET · F-BACK · H1 · H2 · H3 · STACK.
- **VOLUME** e **OUT** na célula direita.

Knobs: OSC A/B, TIME, F-BACK, VOLUME = **Ø30 mm**; o resto **Ø15 mm**. VOLUME = chicken-head vermelho.

### Knobs

| Knob | Pot | Função |
| --- | --- | --- |
| **PRE** | A100 k | Nível do mic → SEND (pré-EQ); sem XLR = pré dos oscs |
| **OSC IN** | A100 k | Mix osc (CCW) ↔ XLR (CW) |
| **LOW / MID F / MID G / HIGH** | 4× 100 kB | EQ voz estilo 424 (pós-mix) |
| **OSC A / OSC B** | 500 kA | Pitch grave / agudo |
| **AMOUNT** | 100 kA | Balanço A ↔ B |
| **SHAPE** | 1 kB | Drive no germânio |
| **CUTOFF** | 100 kA | Corte do filtro |
| **RATE** | 100 kC | Velocidade do LFO |
| **DEPTH** | 25 kB | Quanto o LFO mexe no destino |
| **TIME** | 10 kB | Tempo das três heads |
| **WET** | A100 k | Seco ↔ molhado do eco |
| **F-BACK** | B100 k | Feedback / repeats |
| **VOLUME** | 2 kB | Nível de saída |

Trimpots na BASE: teto do F-BACK (RV1) e ressonância do VCF (RV2).

### Chaves

| Controle | Tipo | Posições | Função |
| --- | --- | --- | --- |
| **OSC A / OSC B** | 2× SPST ON–OFF (MTS-101) | off / on | Liga cada oscilador |
| **H1 / H2 / H3** | 3× SPDT ON–ON (MTS-102) | off / on | Liga cada head. As três off = delay off |
| **TREM** | SPDT ON–OFF–ON (MTS-103) | tremolo / **off** / flutter | Faixa do LFO (centro = sem efeito) |
| **MODE** | SPDT ON–OFF–ON (MTS-103) | pitch / nada / time | Destino do DEPTH |
| **DRONE / GATE** | SPDT ON–ON (MTS-102) | drone / gate | Drone = VCA aberto. Gate = envelope |
| **STACK** | SPDT ON–ON (MTS-102) | off / on | Heads em série (com H1 on) |

Botão momentâneo **GATE**: dispara o envelope com a chave em **gate**. Em DRONE, mute momentâneo dos oscs A/B.

---

## Conectores de palco — combo XLR+P10

Dois **combo XLR+P10 clone** (não Neutrik): XLR fêmea e P10 no mesmo furo.

| Combo | Lado XLR | Lado P10 |
| --- | --- | --- |
| **IN** | SM58 → pré diferencial (5532) → PRE | guitarra → AMOUNT (mix dos oscs) |
| **OUT** | mesa, **nível de mic** (pad) | amp / interface, **nível de pedal** |

SEND / RCV do loop são dois P2 da fileira de patch (`bom.md`). Detalhe do pré: `pre-vocal.md`.

## Jacks de patch

Cadeia normalizada: se nada está plugado, o sinal corre sozinho. Jack com * quebra a cadeia.

| Jack | Tipo | O que faz |
| --- | --- | --- |
| A | P2 out | Oscilador A cru |
| B | P2 out | Oscilador B cru |
| IN | P2 in | Áudio extra no AMOUNT. Paralelo ao P10 do combo IN |
| FILT* | P2 in chaveado | Entrada do filtro. Sem cabo = vem do SHAPE |
| FCV | P2 in CV | Soma no cutoff (0–9 V) |
| VCV | P2 in CV | Soma no VCA / gate |
| LFO | P2 out | Saída do LFO |
| ECV | P2 in CV | Flutter/CV nos três heads |
| **CLK** | P2 in clock | Pulso 0–9 V. Puxa o TIME. **Não é MIDI** |
| SEND / RCV | loop | Antes da fita, 100 % (SEND = PRE, pré-EQ) |

Pinos P2: ponta = sinal, anel/sleeve = GND. CV é 0–9 V, sem 1 V/oitava. CLK: `esquema.md` §8.

---

## Como toca

1. DRONE on, VOLUME no meio, WET no meio, F-BACK baixo, SHAPE e DEPTH no mínimo, TIME no mínimo, AMOUNT no meio, **OSC IN** no CCW (só oscs) ou meio (blend).
2. Aproxima OSC A e OSC B até aparecer o batimento.
3. Abre CUTOFF e SHAPE. EQ flat = knobs no meio.
4. **TREM** em tremolo + MODE em pitch = vibrato. Em time = fita tremendo.
5. **TREM no meio** = LFO off (DEPTH não modula).
6. DRONE off, aperta GATE: nota com cauda. Com XLR, a fala também abre o ENV.
7. H1/H2/H3: as três off = delay off. Só H1 = slapback. As três on = Space Echo. STACK = série.
8. Mic no XLR: PRE a meio, OSC IN a meio = voz + drones. CW = só voz; CCW = só oscs.

### Patches

- **Guitarra no filtro** — P10 IN ou P2 IN → FILT.
- **LFO no filtro** — LFO → FCV, MODE no centro, TREM ≠ off.
- **Fita 3 heads** — H1+H2+H3, TREM em flutter, MODE em time, F-BACK às 3h.
- **Tremolo de volume** — TREM em tremolo, MODE no centro, LFO → VCV.
- **Slapback** — só H1, TIME no mínimo, F-BACK baixo.
- **Clock externo** — sync → CLK. MIDI → conversor → CLK.
- **Voz + drones** — SM58, PRE meio, OSC IN meio, EQ a gosto, GATE ou DRONE.

---

## O que comprar

Tudo novo: `bom.md`. Um instrumento ~R$ **610** (varejo BR, set/2026, sem frete).

J201: marque Vgs(off) nos 8. O mais “vivo” vai no VCF; um par parecido nos FM. MP20 por último — ferro baixo.

---

## Ordem de teste na protoboard

1. Fonte: 9 V, −9 V (MAX1044), 5 V (78M05), 4V5, 1V8. LED acende.
2. OSC A / OSC B / batimento.
3. SHAPE, CUTOFF, GATE / DRONE.
4. LFO + TREM (tremolo / off / flutter) + MODE.
5. 5532 + PRE + OSC IN (mix) + EQ 424 (U9).
6. TL072 NAB: VCA → GRAVA → H1 → LÊ.
7. PT2399 H1, H2, H3. Jacks e normals por último.

Detalhe: `esquema.md`. Placa: `pcb.md`.
