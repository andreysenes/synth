# VOZ-9 — VCO cromático

Mesma caixa, mesmo `painel.svg`, mesma fenolite. OSC A e OSC B continuam pots de relaxação, sem 1 V/oitava. O teclado não entra neles.

O cromático é um **AS3340** (Alfa; o Coolaudio **V3340** tem os mesmos pinos) na BASE. O par casado e a compensação de temperatura estão no die. Dois 2N3904 colados não fazem esse serviço.

A face cresce para **220 × 216 mm**: a faixa de baixo do `painel.svg` é o VCO. Os fios soldam nos pads **J10**. Lista na `bom.md` (detalhe em `vco-bom.md`).

---

## No instrumento

```
teclado CV (0–5 V, 1 V/oitava) ──► jack CV
teclado GATE                    ──► jack VCV
SAW / TRI / PUL (chaves)        ──► mix  (EQ → SHAPE → VCF → fita)
```

Cada chave liga aquela onda no mix, no mesmo ponto dos osciladores. As três off: o VCO some do áudio e ficam os drones. Uma on: essa onda. Mais de uma: elas somam. O som passa pelo germânio, pelo filtro e pela fita. **OSC IN** no CCW, **DRONE/GATE** em **GATE** para o teclado abrir o VCA.

**FM** é o LFO interno (TREM fora do centro), não um jack. Vibrato no cromático sem cabo.

---

## Painel (`painel.svg`)

Faixa de baixo, y = 190:

```
 COARSE   FINE  PW  FM    SAW  TRI  PUL    CV
```

| Knob | Pot | O que faz |
| --- | --- | --- |
| **COARSE** | 100 kB | 0–5 V no pino 15, via 100 k 1 %. Curso = **5 oitavas**. CCW = 0 V (não transpõe o teclado) |
| **FINE** | 100 kB | Entre +5 V e −5 V, via 1M5. Meio ≈ 0. Uns **±4 semitons** |
| **PW** | 100 kB | Largura do pulso, 0–5 V no pino 5. Meio ≈ quadrado |
| **FM** | 100 kA | Quanto do LFO entra no pino 15 (expo). CCW = parado |
| **SAW / TRI / PUL** | 3× SPDT ON–ON | Cada uma liga essa onda no mix. As três off = VCO fora do áudio |

COARSE é linear de propósito: volt linear = oitava linear. Os 500 kA de OSC A/B são outra coisa.

Furos no `painel.svg`, mm, origem no canto superior esquerdo. A faixa nova fica abaixo dos jacks.

| Peça | X | Y | Furo |
| --- | ---: | ---: | --- |
| COARSE | 32 | 190 | 7,5 |
| FINE | 66 | 190 | 7,5 |
| PW | 90 | 190 | 7,5 |
| FM | 114 | 190 | 7,5 |
| SAW / TRI / PUL | 138 / 156 / 174 | 190 | 6,0 |
| CV | 198 | 190 | 6,0 |

Trimpots **na placa**, multiturn, chave de fenda — não são knob:

| Trim | Onde | Para quê |
| --- | --- | --- |
| **TEMP** | pinos 1–2 | correntes de tempco iguais |
| **REF** | pino 13 | nota de referência (C6 com o pino 14 em curto) |
| **RANGE** | pino 15 ← +12 V | achar de novo o C6 com CV = +5 V |
| **SCALE** | pino 14, em série com 1k5 | **1 V/oitava** |
| **HF** | pino 7 | oitava de cima, se ficar grave |

---

## Por que a fonte é maior que 9 V

O AS3340 quer **+10 V a +18 V** no pino 16 e **−5 V** no pino 3 (folha: −4,5 V a −6 V direto, sem resistor). Nove volts no pino 16 fica fora da folha. Ripple nesse pino vira desafinação: o pino 9 é o limiar do triângulo, um terço do VCC.

O **9 V** e o **−9 V** são os da fonte do instrumento (U4). Aqui entram o MC34063, o 78L12, o 78L05 e o 79L05. Não há segundo P4.

```
9 V ── 1N5817 ──● V9 ── 47µ ── GND
                │
                ├── 4k7 ── LED ── GND
                │
                ├── MC34063  ──► V15 ≈ 15 V
                │                 └── 78L12 ──► V12  (pino 16)
                │                       └── 78L05 ──► +5 V
                │                            (COARSE, PW, corrente do pino 13)
                │
                └── MAX1044 ──► VEE ≈ −9 V
                                 └── 79L05 ──► −5 V  (pino 3, direto)
```

Meça **antes** de pôr o AS3340 no soquete: V15 ≈ 15, V12 ≈ 12, +5 ≈ 5, −5 ≈ −5. O 79L05 não tem a ordem de pinos do 78L05 — confira o datasheet do saco.

### MC34063 — sobe 9 V para 15 V

Step-up da folha (TI, figura do conversor elevador). DIP-8, soquete. Corrente baixa: o indutor sai **depois** do resistor de pico, para o pino 7 enxergar a corrente.

```
V9 ─────────────── pin 6 (VCC)
 │
0,47 Ω
 │
 ├─────────────── pin 7 (Ipk)
 │
220 µH  (≥ 500 mA)
 │
 ├─ pin 1 (coletor) e pin 8 (driver) juntos
 │
1N5819  (ânodo neste nó, cátodo = V15)
 │
pin 2 (emissor) ── GND
pin 4 = GND
pin 3 ── 470 p ── GND

V15 ── 100µ/25V ── GND
V15 ── 12k + 1k2 ──●── pin 5
                   │
                  1k2 ── GND          V15 = 1,25 × (1 + 13,2k / 1,2k) = 15,0 V
```

100 n ao lado do pino 6. Se o 15 V não aparecer, o 0,47 Ω ou o 1N5819 está invertido — o AS3340 continua fora do soquete.

78L12: entrada no V15, saída = **V12**. 10 µ + 100 n dos dois lados. É esse 12 V quieto que alimenta o pino 16, não o nó do indutor.

### MAX1044 — o −9 V que a BASE já tem

Este é o **U4** do instrumento, não um segundo charge pump. O VCO só acrescenta o 79L05 em cima desse VEE.

```
8 = V9
3 = GND
2 ── 10µ ── 4          (cap de voo)
5 = VEE ── 47µ ── GND
6 = aberto             (LV só abaixo de 3,5 V)
7 = aberto
100 n no pino 8
```

O 10 µ entre 2 e 4 é o cap de voo (a nota da fonte do VOZ-9). 79L05 em seguida: entrada no VEE, saída **−5 V** no pino 3 do AS3340. Sem resistor em série — em −5 V a folha pede o pino direto.

---

## O chip

DIP-16. Soquete. Nada de soldar o CI.

```
                 AS3340
         pin 1  Scale 1     (TEMP)
         pin 2  Scale 2
         pin 3  −5 V
         pin 4  pulso
         pin 5  PWM
         pin 6  hard sync — 100 k ── GND   (sem jack)
         pin 7  HF track
         pin 8  serra
         pin 9  soft sync — 100 n ── GND
         pin 10 triângulo
         pin 11 cap ── 1 nF C0G ── GND
         pin 12 GND
         pin 13 referência (REF)
         pin 14 escala (SCALE) ── Rs ── GND
         pin 15 soma dos CV
         pin 16 +12 V
         100 n no pino 16 e no pino 3
```

### A conta que é a oitava

O pino 15 é terra virtual. Um resistor de **100 kΩ 1 %** transforma volt em corrente:

```
1 V / 100 kΩ = 10 µA
```

Essa corrente atravessa o **Rs** do pino 14. No silício, a frequência dobra a cada **VT·ln(2)** na base do par — **17,93 mV a 27 °C**.

```
10 µA × 1,793 kΩ = 17,93 mV  =  1 oitava
```

Rs de folha é 1k8 (18,0 mV, uns 5 centavos de oitava fora). O trim cobre:

```
pino 14 ── 1k5 1% ── SCALE (500 Ω multiturn) ── GND
```

1k5 + 500 Ω vai de 1,50 k a 2,00 k. **1,793 k está no meio.** JP1 (dois pinos) em paralelo com esse Rs, para o passo 2 da afinação: pino 14 em GND.

Simulação (`sim/09_vco.cir`): com Rs = 1,793 kΩ, cada volt anda 17,93 mV, +5 V = 1046,5 Hz (C6), 0 V = 32,70 Hz (C1), +1 V = 65,41 Hz. `./run.sh 09_vco` imprime `VCO_OK`.

O modelo é a lei a 27 °C. Quem segura essa lei quando a sala muda são os pinos 1 e 2 (tempco no die). Não compre resistor tempco.

### Tempco — pinos 1 e 2

Correntes iguais, ~100 µA. Com −5 V no pino 3:

```
pino 3 ── 5k6 1% ── pino 2
pino 3 ── 5k6 1% ──● TP ── TEMP 10k ── pino 1
```

Multímetro em mV entre **TP** e **pino 2**. Gira TEMP até **0,0 mV**. Uma vez. Não mexe mais.

### Referência — pino 13

A corrente de referência sai do **+5 V** (78L05), não do V15. Assim o ripple do indutor não vira vibrato.

```
+5 ── 330k 1% ── REF 200k ── pino 13 ── 10 n ── GND
```

### Soma — pino 15

```
CV (jack)     ── 100k 1% ──┐
COARSE (wiper)── 100k 1% ──┤
FINE (wiper)  ── 1M5 1%  ──┼── pino 15 ── 470 Ω ── 10 n ── GND
FM (wiper)    ── 100k 1% ──┤
V12 ── 180k ── RANGE 100k ─┘
pino 7 wiper  ── 2M2 ── pino 15     (HF; comece com o cursor no GND)
```

COARSE: pontas em **+5** e **GND**. FINE: pontas em **+5** e **−5** (meio = 0 V). FM: CCW = GND, CW = LFO (na BASE), cursor vai ao 100 k.

PW: pot de **+5** a GND, cursor ── 1 k ── pino 5.

### Ondas — SAW, TRI, PUL

Pino 4 é emissor aberto. Cada chave é SPDT ON–ON, no painel, e corta o áudio depois do 1 µ, como OSC A/B. Off = aquela onda sai do mix. O chip continua alimentado.

```
pino 8  ── 1k ── 1µ ── [SAW] ── 10k ── mix
pino 10 ── 1k ── 1µ ── [TRI] ── 10k ── mix
pino 4  ── 10k ── GND
         └── 1k ── 1µ ── [PUL] ── 10k ── mix
```

| SAW | TRI | PUL | O que se ouve |
| --- | --- | --- | --- |
| off | off | off | VCO fora. Ficam OSC A/B, noise, voz |
| on | off | off | serra |
| off | on | off | triângulo |
| off | off | on | pulso (largura = PW) |
| on | on | off | serra + triângulo |

Em +12 V a serra vai a ~0–8 V e o triângulo a ~0–4 V. O 1 µ tira o contínuo antes do mix.

---

## Afinação

Afinador ou outro instrumento estável. COARSE no CCW, FINE no meio, FM no CCW (LFO fora do pino 15). Os 100 k de CV e de COARSE têm de estar em 0 V nos passos 2 e 4 — COARSE no fim do curso, jack CV em curto com a luva (ou sem cabo).

1. **TEMP** — 0,0 mV entre TP e pino 2. (Já feito, não repetir.)
2. **JP1 fechado** (pino 14 em GND). **REF** até **C6 = 1046 Hz**. Abre o JP1 e guarda.
3. CV = **+5,00 V** (último Dó do teclado de cinco oitavas, ou o +5 do 78L05 medido). **RANGE** até C6 de novo.
4. CV = **0,00 V** (primeiro Dó, cinco oitavas abaixo). **SCALE** até **C1 = 32,7 Hz**.
5. Sobe o teclado. Se a última oitava ficar grave, tira o cursor do HF do chão aos poucos. Se não ficar, deixa no GND.

A escala gira em torno do C6: primeiro o C6, depois o C1. Invertido, os dois trims brigam.

O +5 do 78L05 tem folga de alguns por cento. Isso mexe no curso do COARSE, não no jack CV — o teclado traz o volt dele, pelo 100 k dele.

---

## Placa

A mesma BASE, agora **220 × 216 mm** (`pcb.svg`). O bloco VCO fica na faixa de baixo, ao lado do **J10**. Soquetes: **U10** AS3340, **U11** MC34063. 78L12, 78L05 e 79L05 sem soquete. O −9 V é o MAX1044 que o instrumento já tem; o 79L05 tira os −5 V do pino 3.

### J10 — 2×10

| Pino | Sinal |
| ---: | --- |
| 1–3 | COARSE GND · W · +5 |
| 4–6 | FINE −5 · W · +5 |
| 7–9 | PW GND · W · +5 |
| 10–12 | FM GND · W · LFO |
| 13–14 | SAW COM · ON |
| 15–16 | TRI COM · ON |
| 17–18 | PUL COM · ON |
| 19–20 | CV TIP · GND |

---

## Ordem na protoboard

1. Fonte, sem o AS3340: 15 V, 12 V, 5 V, −9 V, −5 V. LED aceso.
2. Chip no soquete. Serra no afinador, COARSE no meio, sem CV: tem nota.
3. TEMP, REF, RANGE, SCALE, como acima.
4. Liga **SAW** (TRI e PUL off). GATE do teclado no VCV. Uma oitava no teclado = uma oitava no filtro. TRI e PUL trocam o timbre; as três juntas somam.

Esquema do instrumento: `esquema.md`. Compra: `bom.md` (o recorte do que o VCO acrescenta está em `vco-bom.md`, já somado no total).
