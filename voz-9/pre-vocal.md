# Pré vocal — sem transformador

O Echo Master usa ferro Bourns. O VOZ-9 **não**: pré diferencial no NE5532 e saída XLR em pad. Mesmo papel (mic → pré → loop → eco → mesa), sem os ~R$ 190 dos trafos.

Pré e fita são peças novas da `bom.md`. Sem colher a placa roxa nem outro pedal.

```
SM58 ── COMBO IN (XLR) ── 5532 ── PRE ──┬── SEND (pré-EQ) ── pedais / RCV
                                        └── OSC IN (CW) ──┐
OSC A/B / noise ────────────────────────── OSC IN (CCW) ──┴── mix → EQ 424 → …
guitarra ─ COMBO IN (P10) ── AMOUNT ──────────────────────────┘
                                                              │
                                                         NAB + FITA 3× PT2399
                                                              │
                            WET ──┬── pad ── COMBO OUT (XLR) ── mesa
                                  └── VOLUME ── COMBO OUT (P10) ── amp
```

Mic → pré → **PRE** (nível / SEND) → **OSC IN** (mix com oscs) → EQ → … Sem T1/T2.

O que se perde sem ferro: isolamento galvânico e um pouco de CMRR/RF. Em mesa de casa, cabo curto, SM58, a diferença é pequena. O que se ganha: custo, peso, e o 5532 faz os ~40 dB sozinho.

---

## O que falta (é isto que compra o som)

| Bloco | Echo Master | VOZ-9 (sem trafo) |
| --- | --- | --- |
| Entrada balanceada | XLR + Bourns 1:10 | **combo XLR+P10** + diferencial no 5532 |
| Ganho limpo ~40 dB | trafo ~20 dB + pré ~20 dB | 5532-A ×10 + 5532-B ×11 ≈ **41 dB** |
| Nível do mic | trim / gain | **PRE A100k** no painel (depois do 5532) |
| Entrada ↔ oscs | — | **OSC IN A100k** (mix / balance) |
| EQ (voz + oscs) | — | **424**: LOW / MID F+G / HIGH **pós-mix** (SEND pré-EQ) |
| Headroom | interno | MAX1044 = **±9 V no 5532** |
| Loop de pedais | SEND/RECEIVE antes do delay | P2 SEND/RCV no painel; PRE dirige o SEND |
| Mix de voz | trava em 50/50 | resistor de teto no WET |
| Saída para a mesa | XLR + trafo 1:1, nível de mic | **combo** + pad ~30 dB, XLR quase-balanceado |
| Phantom 48 V | não tem | **não tem** |

J201 não entra no pré de mic — ruído alto demais.

---

## Esquema do pré (±9 V)

O MAX1044 da BOM é o inversor. V9 = +9 V, VEE = −9 V. O NE5532 **não** roda bem em 9 V simples.

Resistores do diferencial em **1 %**, pares iguais (os 2k2 juntos, os 22k juntos). CMRR depende disso.

```
COMBO IN (clone XLR+P10)
  XLR 1 ── massa da caixa (no conector)
  XLR 2 (quente) ── 10µ/25V ── 2k2 ── +in 5532-A
  XLR 3 (frio)   ── 10µ/25V ── 2k2 ── −in 5532-A
  Tip            ── AMOUNT (instrumento), via 100n
  Sleeve / Ring ── GND

5532-A (diferencial, ganho ×10 ≈ +20 dB)
  −in ── 22k ── out_A
  +in ── 22k ── GND
  out_A ── 100n ── +in 5532-B

5532-B (make-up + drive do SEND, ganho ×11 ≈ +21 dB)
  −in ── 1k ── GND
  −in ── 10k ── out_B
  out_B ── 100n ──● PRE CW (ponta quente)
                  │
             PRE A100k   cursor (W) ──● SEND (ponta)
                  │                   │
             PRE CCW ── GND  jack RECEIVE chaveado
                                      │
                                 para a fita
```

**PRE** (A100 k, Ø15 mm, sob o COMBO IN): divisor depois do ganho fixo. Com mic: CCW = mudo; meio ≈ nível de pedal; CW = cheio (~330 mV) → **SEND** (pré-EQ). Sem XLR: o mesmo pot escala os oscs. **VOLUME** continua sendo a saída do instrumento.

XLR e P10 do combo são contatos **separados**. Mic no XLR; guitarra no P10. Não os dois ao mesmo tempo no mesmo combo.

**Conta:** SM58 ~3 mV × 10 × 11 ≈ **330 mV** no CW do PRE — nível de pedal, loop e PT2399 felizes.

**LED IN** (3 mm vermelho, entre o combo e o PRE): tap nesse out_B, **antes** do pot. A fala acende o LED mesmo com PRE no zero. O P10 (guitarra → AMOUNT) não passa por aqui e não acende. Circuito: `esquema.md` §10.

RF no painel (vale a pena, é barato): **100 p** de XLR 2 → massa e XLR 3 → massa, colado no combo.

**Sem phantom.** Condensador precisa de 48 V inline *antes* do XLR IN. Se alguém mandar 48 V no cabo, os 10 µ / 25 V e o 5532 morrem — não ligue este IN em mesa com phantom ligado.

---

## Saída — combo OUT (sem T2)

Dois níveis, dois pinos. O pad joga o XLR para **nível de mic** (~20 mV a partir de ~1 V no VOLUME).

```
WET/VOLUME ── 10k ──●── combo OUT XLR 2     (quente, ~nível de mic)
                    │
                   220 ── GND
                    │
              XLR 3 ── 220 ── GND           (quase-balanceado: mesma Z)
              XLR 1 ── massa da caixa

VOLUME ────────── combo OUT Tip             (nível de pedal)
                  Sleeve ── GND
```

Quase-balanceado: o mixer vê a mesma impedância nos pinos 2 e 3, e cancela um pouco de ruído no cabo. **Não** isola terra (isso era o T2). Em casa, P10 direto na interface é o caminho mais limpo.

**Gênero do XLR:** o clone é **fêmea** dos dois lados. Cabo de microfone padrão serve no **IN**. No **OUT** a mesa também é fêmea: cabo **macho–macho** curto, adaptador, ou use só o **P10**.

Mix de voz: knob **WET** = seco/molhado. Teto Echo Master: 10 k entre a ponta wet e o cursor. **F-BACK** é o f-back do painel.

---

## Loop (SEND / RCV)

```
pré ── PRE ── SEND  ──►  fuzz / VOZ-9 / qualquer pedal de guitarra
RECEIVE ──►  fita

RECEIVE chaveado: sem cabo, o PRE vai direto à fita.
```

O loop é **antes** do delay, 100 % — não passa pelo MIX.

O VOZ-9 (oscs, filtro, germânio) pode viver *dentro* desse loop: voz no pré → PRE → SEND → IN do VOZ-9 → OUT do VOZ-9 → RECEIVE → fita. Ou a fita fica no VOZ-9 e o loop só leva pedais de fora.

---


## EQ voz — estilo Tascam 424 MKIII

**Pós-mix** (voz + oscs), antes do SHAPE. **SEND** no PRE (**pré-EQ**). **OSC IN** = balance osc ↔ XLR. Strip de canal Portastudio:

| Knob | Tipo | Frequência | Curso | Pot |
| --- | --- | --- | --- | --- |
| **LOW** | shelf | **100 Hz** | ±10 dB | 100 kB |
| **MID F** | peaking (freq) | **250 Hz – 5 kHz** | — | 100 kB |
| **MID G** | peaking (ganho) | (centro = MID F) | ±12 dB | 100 kB |
| **HIGH** | shelf | **10 kHz** | ±10 dB | 100 kB |

```
PRE W ──┬── SEND (pré-EQ)
        └── OSC IN CW ──┐
oscs ──── OSC IN CCW ───┴── mix → EQ (U9) → SHAPE…
```

Meio dos knobs EQ = flat (detent mental). U9 em ±9 V (mesmos trilhos do 5532). Chicote **J9** 2×6. Sem mic no XLR, PRE ainda escala os oscs e o EQ os molda.

## OSC IN — mix osc ↔ XLR

Pot **OSC IN** (A100 k) balanceia o áudio no mix (antes do EQ):

```
PRE W ──┬── SEND (sempre, pré-EQ)
        └── OSC IN CW  ──● mix
oscs / noise ─ OSC IN CCW ──┘
```

- **PRE** = nível da voz no SEND; **sem XLR** = pré-amp dos oscs.  
- **OSC IN** = CCW só osciladores · meio blend · CW só XLR.  
- Envelope da fala → ENV continua no tap fixo do PRE (GATE); não passa pelo OSC IN.

Só o áudio do mix muda com OSC IN. DRONE amarra ENV em 1V8 (oscs sempre on na proporção do mix).

---

## Time 30–620 ms (faixa do Echo Master)

Com **três** PT2399 em paralelo isso já é o TIME do painel:

- H1 ~30–170 ms  
- H2 ~80–400 ms  
- H3 ~200–**620 ms** (zona vermelha, chiado)

**STACK** (H1→H2→H3 em série) passa de 1 s — outro instrumento.

---

## Lista só do pré (já na `bom.md`)

| Qtd | Peça | Nota |
| --- | --- | --- |
| 1 | NE5532 DIP-8 | não use LM358 (ruído) |
| 2 | combo XLR+P10 clone | IN e OUT; ver `bom.md` |
| 1 | A100 k + knob Ø15 | **PRE** no painel |
| 1 | A100 k + knob Ø15 | **OSC IN** (mix osc ↔ XLR) |
| 4 | 100 kB + knob Ø15 | **LOW · MID F · MID G · HIGH** |
| 1 | TL072 DIP-8 | EQ voz (U9) |
| 2 | 10 µF / 25 V | acoplamento XLR 2 e 3 |
| 2 | 100 nF filme | entre as metades do 5532 e o PRE |
| 2 | 10 µF / 25 V | desacoplo ±9 V no 5532 |
| 2 | 2k2 1 % + 2× 22k 1 % | diferencial (pares iguais) |
| 2 | 220 Ω | pad + quase-balanceado da saída |
| 2 | 100 p | RF no combo IN (opcional, barato) |
| 1 | soquete DIP-8 | 5532 |
| 1 | 1N4148 + 10k + 100n | envelope da fala → ENV |

MAX1044 e 1N5817 vêm da `bom.md`. **Nenhum transformador.** O trimpot de bias do 5532 saiu: o PRE no painel cobre o nível.
