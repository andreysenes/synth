# VOZ-9 — esquema

Alimentação simples, 9 V centro-negativo. Referência de áudio em 4,5 V. O MAX1044 gera −9 V para o germânio, o NE5532, o TL072 do NAB (**U3**), o TL072 do EQ voz (**U9**) e o TL072 do VU de saída (**U12**). Se ele falhar, o clipper ainda funciona como diodo à terra; o EQ da fita, o EQ 424 e o pré de mic perdem headroom.

Quantidades e compra: `bom.md`. Tudo novo — um instrumento = uma lista.

Uma fenolite no piso da caixa (220 × 216 mm): `pcb.md`. O painel só fura; os cabos soldam direto nos pads **J1–J10** da BASE. CIs em soquete. **Um módulo** retangular de mesa. O VCO cromático é a faixa de baixo do mesmo painel (`vco.md`), no **J10**.

---

## 0. Fonte

```
9V ── 1N5817 ──● V9 ── 47µ/25V ── GND
               │
               ├── 4k7 ── LED ── GND          (piloto)
               │
               ├── 78M05 ──● V5 ── 10µ ── GND
               │              └── 100n ── GND
               │
               └── MAX1044
                    8 = V9
                    4 = GND
                    2 ── 10µ ── 4
                    5 = VEE (−9V) ── 47µ ── GND
                    3 ── 10µ ── 5     (cap de voo; se só tiver 2× 10µ,
                                       use 10µ entre 2–4 e 22µ em VEE)

V9 ── 10k ──● 4V5 ── 10k ── GND
            └── 47µ ── GND           (terra virtual dos op-amps)
```

P4 no painel no centro horizontal (**x=110**), à direita do LED; combo IN no canto superior esquerdo (**x=20**). Centro-negativo. Não inverta a fonte.

VEE (−9 V) alimenta o **NE5532**, o **TL072 NAB (U3)**, o **TL072 EQ voz (U9)** e o **TL072 do VU (U12)** (§9). Sem o inversor, pré e EQs saturam cedo. O pré é diferencial ativo — **sem transformador**.

Nível: **PRE** → **SEND** (pré-EQ). **OSC IN** = mix osc (CCW) ↔ XLR (CW) → mix → **EQ 424** → SHAPE…. Sem XLR, PRE = pré-amp dos oscs. Detalhe: `pre-vocal.md`. Não confundir com **VOLUME** (saída).

---

## 1. Osciladores (as duas metades do op-amp)

Oscilador de relaxação — quadrado. Uma metade = um osc. Gira em faixa larga com um pot só. É o som LMNC (40106), sem comprar o 40106.

```
                    V9
                     │
                  ┌──┴──┐
                  │     │   metade A = OSC A
                  │ +   │
           100k ──┤     ├── OUT_A ── 1µ ──●── 10k ── mix A
              │   │ −   │                │
              │   └─────┘                └── jack A
              │      │
              │     100n
              │      │
              └──●── 4V5
                 │
                10k + PITCH A (500kA) ── OUT_A
                 │
                100k ── 4V5          (histerese)
```

**OSC A** — grave / drone

- C = **100 nF**
- R = **10 k + 500 kA**
- Histerese = **2× 100 k** (um do out para +, um do + para 4V5)
- f ≈ 10 Hz – 500 Hz

**OSC B** — médio / agudo

- C = **10 nF**
- R = **10 k + 500 kA**
- Histerese = **2× 220 k** (timbre/duty um pouco diferente — ajuda o batimento)
- f ≈ 100 Hz – 5 kHz

Zona em que os dois se encontram e batem: ~100–500 Hz.

Saída de cada um: capacitor **1 µF** filme para o mix e para o jack.

**OSC A / OSC B — chaves ON–OFF** (MTS-101, painel, ao lado de cada pot). Cortam o áudio *depois* do 1 µF, antes do 10 k de mix e do jack. Off = aquele osc some. O chip continua alimentado (não estoura, não muda o pitch do outro).

```
OUT_A ── 1µ ── [OSC A] ──●── 10k ── mix / AMOUNT
                         └── jack A

OUT_B ── 1µ ── [OSC B] ──●── 10k ── mix / AMOUNT
                         └── jack B
```

As duas off: ficam noise + EXT IN + voz. Uma off: AMOUNT vira nível do que restou.

### Vibrato / FM (1 J201 por osc)

O J201 entra em paralelo com o capacitor de tempo. Gate em 0 V → pouco efeito. Gate sobe → o cap descarrega mais rápido → o tom sobe e “molha”.

```
OUT ── Rpitch ──● −in
                │
               Ctempo
                │
               4V5

               D do J201 ── no nó −in
               S ── 4V5
               G ── 100k ── barramento PITCH_CV
```

Barramento PITCH_CV vem da chave LFO (posição “pitch”) via DEPTH, e não tem jack próprio no Sistema 0 — o vibrato é interno. Os jacks A e B continuam sendo áudio.

J201 #1 = OSC A. J201 #2 = OSC B.

---

## 2. Noise (J201 #3)

```
V9 ── 10k ── D ── 100n ── 100k ── mix     (nível baixo, sempre no fundo)
             │
            J201
             │
             S ── 1k ── GND
             G ── 1M ── GND
```

Se estiver quieto demais, troque o 100 k de mix por 22 k. Se chiado demais, volte.

---

## 3. Mix + OSC IN + EQ

```
OSC A  ── 10k ──┐
OSC B  ── 10k ──┤
NOISE  ── 100k ─┼──● AMOUNT (100kA entre A e B) ──●── OSC IN CCW
EXT IN ── 10k ──┘                                 │
                                                  │
PRE W ──┬── SEND (pré-EQ, jack)                   │
        └── 100n ── OSC IN CW ────────────────────┤
                                                  │
                                                  ● mix
                                                  │
                                             EQ 424 (U9) ── 100n ── SHAPE
```

**OSC IN** (A100 k): crossfade. CCW = só oscs/noise/EXT; CW = só mic (após PRE). Meio = blend. **SEND** sai do PRE **antes** do OSC IN — o loop não some quando o mix vai para os drones.

EXT IN = P10 + P2 em paralelo, após 100n. Guitarra no P10 não passa pelo 5532.

Envelope da fala (GATE): tap fixo PRE → 100n → 10k → 1N4148 → ENV (§6). Não passa pelo OSC IN.

J201 #6 = buffer opcional após o EQ / antes do SHAPE se o VCF carregar. Senão o mix + U9 aguentam.

---

## 3b. EQ voz (Tascam 424 MKIII) — U9 TL072

**Depois do mix**, **antes** do SHAPE. ±9 V (V9 / VEE). Pots **100 kB**, meio ≈ flat.

| Knob | Tipo | Faixa | Curso |
| --- | --- | --- | --- |
| **LOW** | shelf | **100 Hz** | ±10 dB |
| **MID F** | peaking (freq) | **250 Hz – 5 kHz** | — |
| **MID G** | peaking (ganho) | centro = MID F | ±12 dB |
| **HIGH** | shelf | **10 kHz** | ±10 dB |

```
mix ── 100n ──●── U9A+ (seguidor)
              │
             10k
              │
         ┌────┴──── Baxandall (LOW + HIGH) ────┐
         │  LOW 100kB · C=33n (~100 Hz)         │
         │  HIGH 100kB · C=1n (~10 kHz)         │
         │  Rsérie 10k cada braço               │
         └──────────────────┬───────────────────┘
                            │
                       10k ──●── U9B− (mid peaking)
                            │         │
                     MID G 100kB      │
                     (ganho ±12)      │
                            │         │
              MID F 100kB ──●── 10n ──┘
              (série 3k3: ~250 Hz–5 kHz)
                            │
                         out ── 100n ── SHAPE
```

Chicote **J9** 2×6. Não é o NAB da fita (§8b) nem o CUTOFF do VCF.

Passivos extras na BASE (além da lista geral): **2× 10 k**, **1× 3k3**, **1× 33 n**, **1× 1 n**, **1× 10 n**, **2× 100 n** de acoplamento — ver `bom.md` § EQ voz.

---

## 4. Waveshaper (MP20)

Dois andares. O primeiro sempre funciona. O segundo usa −9 V e ganha corpo.

**4a — clip assimétrico (sempre)**

```
SHAPE wiper ── 10k ──●── 100n ── FILT (normal)
                     │
                    MP20-1  (E = GND, B e C juntos = ânodo)
                     │
                    GND
```

Um diodo de germânio à terra. Harmônicos pares. SHAPE define o quanto satura.

O segundo MP20 **não** fica aqui. Ele vai para o laço do echo (saturação de fita). Ver §8.

---

## 5. VCF (J201 #4)

Passa-baixa de um polo. O J201 é resistência à terra.

```
audio ── 10k ──●── 220n ── GND
               │
               D J201
               S ── 1V8
               G ──●── CUTOFF 100kA ── 1V8
                   │         (outra ponta do pot = GND)
                   ├── 100k ── jack FCV
                   └── 100k ── LFO (quando a chave não está em pitch/time;
                                   na verdade o DEPTH só chega aqui
                                   se você patchar LFO→FCV, ou se
                                   no futuro ligar um jumper)

1V8:  V9 ── 22k ──● 1V8 ── 5k6 ── GND
                  └── 47µ ── GND
```

Vgs ≈ 0 (gate = 1V8) → JFET conduz → cap à terra → som escuro / filtro fechado?  

Cuidado com a lógica do shunt:

- JFET **ligado** (Vgs = 0) → baixa R à terra → **mais grave, menos agudo** (filtro fecha)
- JFET **pinch-off** (gate em 0, source em 1V8, Vgs = −1,8 V) → alta R → **filtro abre**

Então o CUTOFF “para a direita” deve ir de 1V8 → 0 V no gate se você quiser o sentido clássico (horário = mais aberto). Inverta as pontas do pot até o ouvido concordar.

Saída do VCF: o nó do 220 n, via **220 n** ou **100 n**, para o normal do VCA.

Ressonância barata: 68 k do nó de saída de volta à entrada do 10 k, em série com um trimpot 100 k. No máximo o filtro assovia — isso é um oscilador extra, de graça.

---

## 6. VCA + GATE + DRONE (J201 #5)

Mesma polarização 1V8. Aqui o JFET está **em série**:

```
audio ── 100n ── D
                 J201
                 S ── 10k ── 1V8
                 │
                 └── 1µ ── echo (normal)
                 G ──● ENV
```

- Gate = 1V8 → Vgs = 0 → conduz → som passa
- Gate = 0 → Vgs = −1,8 V → fecha → silêncio

**Envelope**

```
1V8 ── GATE (botão NA) ── 1N4148 ──● ENV ── 47µ ── GND
                                   │
                                  220k ── GND     (decay ~1 s)
                                   │
                                  100k ── jack VCV
                                   │
PRE W ── 100n ── 10k ── 1N4148 ──┘  (envelope da fala → oscs; fixo)
                                              │
DRONE / GATE (SPDT ON–ON):
  drone ── 1V8 direto em ENV (VCA aberto)
  gate  ── envelope (botão + VCV + **fala**) como acima
```

Com a chave em **GATE** e mic no XLR: a fala carrega o ENV (abre a porção de oscs). **OSC IN** = mix áudio osc ↔ XLR (CCW = só drones, CW = só mic). **PRE** = nível da voz no SEND (**pré-EQ**); sem XLR, PRE escala os oscs. No silêncio o 220 k esvazia o 47 µ (~1 s). Botão GATE e VCV somam no mesmo nó.

**Botão GATE com a chave em DRONE:** mute momentâneo de **OSC A e OSC B** (corta o áudio depois do 1 µF, como as chaves A/B, mas só enquanto o botão está pressionado). Noise, EXT e a cauda da fita seguem.

Dois 1N4148 no envelope (botão + fala); o 1N5817 fica na fonte. Detalhe do pré: `pre-vocal.md`.

---

## 7. LFO (2N5457)

Mesma ideia de fase do Glam Chorus, em taxa baixa/média.

```
V9 ── 10k ── D ── 1µ ──● LFO_OUT ── jack LFO
             │         │
          2N5457        └── DEPTH 25kB ── LFO MODE (SPDT ON–OFF–ON)
             │
             S ── 1k ── GND
             G ── rede de 3× 220n + (4k7 + RATE 100kC)

Rede (deslocamento de fase):

D ── 220n ── n1 ── 220n ── n2 ── [Csel] ── G
      │             │
     10k           10k          G ── (4k7 + 100kC) ── GND
     GND           GND          G ── 1M ── GND
```

**TREM — SPDT ON–OFF–ON (MTS-103, 3 estágios)** — *quão rápido* (e se) o LFO age. Escolhe o último cap (`Csel`) ou deixa aberto.

| Posição | Csel | Faixa (RATE min→max) | Som |
| --- | --- | --- | --- |
| Cima **TREMOLO** | **220 n** | ~3–60 Hz | LFO de synth. Na ponta rápida entra em áudio (FM / ring) |
| **Centro (off)** | *(aberto)* | — | **sem efeito** — DEPTH não modula pitch/time/VCA |
| Baixo **FLUTTER** | **47 µ** | ~0,3–4 Hz | wow de fita, heads cambaleando |

`Csel` (220 n / 47 µ) e o detector CLK moram na BASE. A chave TREM e o pot RATE descem por cabo. Centro = nenhum Csel → LFO parado / sem modulação no painel.

**LFO MODE — SPDT ON–OFF–ON (3 estágios)** — *para onde* o DEPTH vai. Só age se TREM ≠ centro.

| Posição | Destino do wiper do DEPTH |
| --- | --- |
| Cima (pitch) | barramento PITCH_CV (J201 de FM nos dois oscs) |
| Centro (nada) | LFO só no jack. Tremolo de amplitude: LFO → VCV |
| Baixo (time) | pino 6 dos três PT2399, via 220 k em cada |

Combinações: FLUTTER + time = Echo Master; TREMOLO + pitch = vibrato; TREMOLO + MODE centro + LFO→VCV = tremolo de volume; **TREM no meio = LFO off**.

---

## 8. Echo — fita de três heads (3× PT2399)

Três PT2399 novos. Em paralelo, tempos em progressão: é o desenho do **RE-201 / Space Echo** (três cabeças, um capstan). O LFO mexe nos três iguais.

```
 VCA ── 10k ──●── GRAVA (½ TL072) ── pin 16 H1 / H2 / H3
 F-BACK ──────┘         │
                    pin 14 ×3
                        │
                  mix 10k+10k+10k
                        │
                   LÊ (½ TL072)
                        │
              MP20-2 + WET + F-BACK ──┘
```

O EQ NAB (§8b) está **no caminho**. Sem o TL072 no soquete o eco some — não há bypass passivo.

Três chips × ~25 mA = **~75 mA**. Use **78M05** (500 mA, TO-220 ou TO-252) — 78L05 ferve. 10 µ + 100 n em V5 ao lado de cada chip.

### Tempo — um knob, três heads

O **TIME 10 kB** é o master. Cada pino 6 vê o mesmo pot, com resistor extra diferente.

```
TIME 10kB (cursor) ── GND
                  ──●── 2k        ── pin 6 H1
                  ──●── 1k+1k ── 22k ── pin 6 H2
                  ──●── 1k+1k ── 68k ── pin 6 H3

LFO / ECV / CLK ── 220k ── pin 6 dos três
```

### CLK — tempo de fora (bem simples)

Um jack **CLK** no painel. Entra pulso analógico 0–9 V (clock de synth, Volca/PO sync, Eurorack, Beatstep *sync out*). O circuito é um detector de picos: cada pulso enche um cap; pulsos mais seguidos = tensão média mais alta = os três pinos 6 se mexem. O knob **TIME** continua sendo a base. CLK *soma*, não substitui.

**Não é MIDI.** MIDI clock é outro idioma (DIN/TRS, 31,25 kHz). O VOZ-9 não decodifica. MIDI → caixinha “MIDI clock to analog clock / sync” → cabo P2 no CLK.

Detector na BASE. A ponta do jack CLK chega por cabo e soma no **mesmo nó do ECV**. Sem pino extra.

```
CLK ponta ── 47k ──●── 1N4148 ──●── 4µ7 ── GND
                   │             │
                  10k           220k ── GND          (sangria: o cap desce se o clock para)
                   │             │
                  GND           100k ──●── nó ECV
                                       │
CLK ponta ── 1N4148 ── V9              └── ECV ponta
            (trava >9 V de Eurorack)
```

- Sem cabo em CLK: o detector fica no 0, TIME e ECV mandam.  
- Clock lento / rarefeito: pouco deslocamento.  
- Clock rápido (ou gate preso em 5 V): eco mais curto, como TIME um pouco à esquerda.  
- Quadrado de outro LFO no CLK: o tempo “anda” no ritmo — não é flutter (isso é o LFO interno).

Não trava na colcheia. É “o relógio de fora puxa o capstan”. Se o ouvido achar o sentido invertido (mais BPM = eco *mais longo*), troque o 100 k de soma por um PNP/J201 depois — no ouvido primeiro.

Anti-latch **≥ 2 k** em cada pino 6. H1 = 2 k. H2 = 1 k+1 k + 22 k. H3 = 1 k+1 k + 68 k.

| TIME | Head 1 ≈ | Head 2 ≈ | Head 3 ≈ |
| --- | --- | --- | --- |
| mínimo | 30–50 ms slapback | ~80–120 ms | ~200–280 ms |
| meio | ~100 ms | ~200–250 ms | ~400–450 ms |
| máximo | ~150–170 ms | ~350–400 ms | **~550–620 ms** |

Head 3 no máximo é a zona vermelha do Echo Master (chiado de propósito). Os três juntos = uma fita com slap + médio + longo.

**Chaves de cabeça** (3× SPDT ON–ON, 2 estágios) — cada uma liga o pin 14 daquela head no mix molhado. Chip continua alimentado; só some do áudio.

| H1 | H2 | H3 | Som |
| --- | --- | --- | --- |
| off | off | off | **delay off** — só o seco (VCA → VOLUME) |
| on | off | off | slapback |
| on | on | off | dois heads |
| on | on | on | três heads (RE-201) |
| off | on | on | eco sem o tap curto |
| off | off | on | só a cauda longa |

```
H1 pin 14 ── [H1] ── 10k ──┐
H2 pin 14 ── [H2] ── 10k ──┼── mix molhado
H3 pin 14 ── [H3] ── 10k ──┘
```

**STACK** (SPDT ON–ON): pin 14 H1 → pin 16 H2 → pin 14 H2 → pin 16 H3. Série, ~0,8–1 s. Só faz sentido com **H1 on**. Off = paralelo (fita). On = caverna.

### Laço: um feedback, três heads

O LPF passivo 10 k+10 n **sai**. Quem filtra é a metade LÊ do TL072. O laço volta **à entrada da GRAVA**, para cada repeat passar de novo pelo NAB.

```
H1 pin 14 ── 10k ──┐
H2 pin 14 ── 10k ──┼── LÊ ──●── WET (ponta molhada)
H3 pin 14 ── 10k ──┘        │
                            MP20-2 ── GND
                            F-BACK B100k ──●── GRAVA
                                           └── VCA (10k)

molhado ── 10k ── 2n2 ── GND     (pó fino, depois do LÊ)
```

22 n no lugar do 2n2 = fita mais gasta / dub. O NAB continua.  

### Flutter e tremolo

Chave **FLUTTER**, LFO MODE em **time**, LFO no mínimo, DEPTH pouco: os três heads desafinam juntos.

Chave **TREMOLO**, LFO MODE em **time**: a fita “treme” rápido (quase ring). Em **pitch**: vibrato. No centro, LFO → VCV: tremolo de volume.

### Saída — WET e F-BACK

**WET** (A100 k): quanto de eco entra no som. Não é o AMOUNT dos osciladores. A ponta molhada vem da **saída LÊ**, não do mix cru dos pin 14.

```
seco (VCA)              ── ponta CCW ──┐
molhado (H1+H2+H3)      ── ponta CW  ──┼── WET A100k
                                       │   cursor ── VOLUME 2kB ── OUT
```

- CCW / 0 = só seco
- meio ≈ 50/50
- CW = só fita

Teto Echo Master (≤50/50): 10 k entre a ponta molhada e o cursor.

**F-BACK** (B100 k): feedback do laço, da saída LÊ de volta à entrada GRAVA. 0 = um eco; meio = repeats escuros; fundo = a fita oscila. O trimpot 100 k limita o máximo (igual ao trim interno do Echo Master), por baixo do painel.

H1+H2+H3 off **ou** WET no mínimo = sem eco.

### O que isso é — e o que não é

| Tem | Não tem |
| --- | --- |
| Três heads, um motor (RE-201) | Tempos independentes no painel (um TIME só) |
| 30–620 ms na faixa do Echo Master | Capstan / óxido de verdade |
| Wow / flutter **e** tremolo no painel | EQ de gravador de estúdio (o NAB aqui é elétrico, §8b) |
| EQ NAB de pré de fita | |
| Repeats escuros e saturados | |

### Caps dos três heads

Lista completa em `bom.md`. Papel por chip:

| Head | Som | Filtros |
| --- | --- | --- |
| H1 | curto / limpo | 100 p, 2 n2, 4 µ7, 22 n |
| H2 / H3 | médio / longo (gastos) | 100 n / 10 n + 10 µ em V5 + 47 µ na saída |

### 8b. EQ de pré de fita (NAB)

Máquina de fita faz duas curvas **complementares** (NAB / IEC). As duas estão no VOZ-9, no TL072 da BASE (U3).

1. **GRAVA** (½ A, antes dos heads) — corta grave (~50 Hz) e realça agudo (~3 kHz). O “óxido” não satura no baixo e o chiado some no alto.
2. **LÊ** (½ B, depois dos heads) — o inverso: devolve o grave e tira o agudo. O que sobra é “fita”, não um rádio AM.

Duas inversões = o molhado volta na fase do seco. +in A e +in B no **GND** (alimentação ±9 V). Sem o chip no soquete o eco some — não há bypass passivo.

```
TL072 DIP-8
  1 = out A (GRAVA)
  2 = −in A
  3 = +in A → GND
  4 = VEE (−9 V)
  5 = +in B → GND
  6 = −in B
  7 = out B (LÊ)
  8 = V9
  100 n em V9 e em VEE, junto do chip
```

#### Gravação — ½ A

```
VCA ── 10k ──●── 220n ── 4k7 ──●── −in A
F-BACK ──────┘                 │
                         15k ──┤
                         3,3n ─┘

−in A ── 15k ── out A          (ganho 1 no médio)
+in A ── GND

out A ── 100n ──●── 10k ── pin 16 H1
                ├── 10k ── pin 16 H2
                └── 10k ── pin 16 H3
```

15 k × 3,3 n ≈ **50 µs** (~3,2 kHz). 220 n × ~20 k ≈ **40 Hz**. O 4k7 limita o shelf (~10 dB) para o PT2399 não estourar.

#### Leitura — ½ B

```
mix H1+H2+H3 (10k+10k+10k)
    │
   100n ── 15k ── −in B
+in B ── GND

−in B ── 15k ── out B
−in B ── 3,3n ── out B          (corta o agudo que a gravação empurrou)
−in B ── 10k ── 220n ── out B   (devolve o grave, ~2,2 ms)

out B ──●── ponta molhada do WET
        └── 10k ── 2n2 ── GND
        └── MP20-2 ── GND
        └── F-BACK B100k ──● da GRAVA
```

| Constante | NAB | Aqui |
| --- | --- | --- |
| Agudo | 50 µs (3,2 kHz) | 15 k + **3,3 n** ≈ 50 µs |
| Grave | 3180 µs (50 Hz) | 10 k + **220 n** ≈ 2,2 ms (um pouco acima de 50 Hz) |

2 n2 no lugar de um 3,3 n: um pouco mais brilhante na gravação. Os dois 3,3 n da BOM são o NAB fechado.

**STACK** continua entre pin 14 e pin 16 dos chips — não passa pelo EQ. Série de heads, um NAB só no começo e no fim.

J201 #6 **não** é o NAB. Fica buffer depois do SHAPE se o VCF carregar o clipper. Quiser só a cor de Echoplex (uma curva, sem devolver grave): tire o TL072 e use o #6 no lugar da GRAVA — o eco volta a só escurecer.

---

## 9. VU de saída (U12 TL072)

Um **VU analógico** (movimento de bobina móvel, tipo TN-73) no painel mostra o nível que sai — **depois do VOLUME**, o mesmo ponto que vai ao combo OUT. Não é medidor de pico: sobe rápido e desce devagar, como um VU de mesa.

O movimento sozinho não lê nível de pedal (precisa de ~1 V e alguns mA) e, ligado direto, ainda **carregaria** o áudio. Então um **TL072 (U12, ±9 V)** faz um **retificador de precisão de onda completa** (valor absoluto) e a média enche o ponteiro. Uma metade retifica meia onda; a outra soma o sinal cru + a meia onda retificada = onda completa.

Essa plaquinha **não** entra na BASE: o U10 de lá é o AS3340. Mora **atrás do próprio meter** (uma ilhada / dead-bug). Sinal e alimentação sobem pelos pads **J8** (combo OUT), que passa de 2×3 para **2×4**. Os refs começam em R115 / C90 / RV8 para não repetir o VCO.

```
TIP (J8 p4, pós-VOLUME) ── C90 100n ──●── R116 10k ──●───────────●── R118 10k ──● U12B(−) ──● out B
                                      │              │           │                           │
                                     R115 100k     U12A(−)     R119 4k7                   R120 10k
                                      │            R117 10k (fb) (≈ R/2, da meia onda)       │
                                     GND           D6 · D7 (1N4148) no laço da U12A      out B ──┘
    U12A(+) = GND        U12B(+) = GND

out B ──●── RV8 10k (calibra 0 VU) ──● VU (+)   ── meter (bobina móvel) ──● VU (−) = GND
        └── C91 47µ ── GND  (balística / média)
```

- **U12A** retifica meia onda com D6/D7 (silício; a queda some no laço de feedback — por isso “precisão”).
- **U12B** soma o cru (R118 10 k) com a meia onda em dobro de peso (R119 4k7 ≈ R/2) → **onda completa**, sempre positiva.
- **RV8 10 k** ajusta o fundo de escala: toca no nível mais alto que você usa e abre RV8 até o ponteiro parar em **0 VU** (início do vermelho). RV3–RV7 são os trims do VCO, na BASE.
- **C91 47 µ** em paralelo com o meter faz a média: o ponteiro não treme na frequência do áudio, sobe rápido e cai devagar.
- 100 n em V9 e em VEE ao lado do U12 (**C92**, **C93**), como nos outros op-amps.

A corrente do ponteiro sai do trilho **V9** (pelo U12B), não do VEE. O VEE só ganha o consumo de repouso do U12 (~3 mA) — cabe no MAX1044 junto do 5532/U3/U9. Sem o U12 no soquete, o instrumento toca igual: o VU só para de indicar.

**Contrato J8** (combo OUT, agora **2×4**): pinos 1–5 = X2 · X3 · X1 · TIP · GND (como antes); **6 = V9**, **7 = VEE**, **8 = NC**. A plaquinha do VU puxa **TIP (p4) + GND (p5) + V9 (p6) + VEE (p7)** daqui e liga o meter localmente. Uma folga de 9 V ao lado do áudio de saída é pouca — os fios são curtos e o nível é alto.

---

## Mapa dos 6× J201 + amigos

| Peça        | Função                         |
| ----------- | ------------------------------ |
| J201 #1     | FM / VCR do OSC A              |
| J201 #2     | FM / VCR do OSC B              |
| J201 #3     | Noise                          |
| J201 #4     | VCF                            |
| J201 #5     | VCA                            |
| J201 #6     | Buffer pós-SHAPE (se o VCF carregar) |
| 2N5457      | LFO                            |
| MP20 #1     | Diodo clipper (shape)          |
| MP20 #2     | Saturação no laço da fita      |
| Op-amp U2 | OSC A + OSC B (TL072/4558) |
| TL072 U3 | NAB: GRAVA + LÊ (§8b) |
| TL072 U9 | EQ voz 424 (§3b) |
| AS3340 U10 | VCO cromático (`vco.md`) |
| MC34063 U11 | 9 V → 15 V do VCO |
| TL072 U12 | VU de saída — retificador (§9) |
| NE5532 U1 | Pré de mic |
| PT2399 #1 | Head 1 curto |
| PT2399 #2 | Head 2 médio |
| PT2399 #3 | Head 3 longo |
| 78M05 | 5 V dos três chips |
| MAX1044 | −9 V |
| 1N5817 | Proteção da fonte |

---

## Caps por bloco

Quantidades de compra em `bom.md`. Uso principal:

| Uso                         | Valor        | Qtd |
| --------------------------- | ------------ | --- |
| OSC A tempo                 | 100 n        | 1   |
| OSC B tempo                 | 10 n         | 1   |
| OSC A/B saída               | 1 µ filme    | 2   |
| LFO fase                    | 220 n        | 3   |
| LFO saída                   | 1 µ eletro   | use 2µ2 |
| VCF                         | 220 n        | 1   |
| NAB grave (GRAVA + LÊ)      | 220 n        | 2   |
| NAB agudo                   | 3,3 n        | 2   |
| NAB acoplo (out A, in B)    | 100 n        | 2   |
| Acoplos (shape, vca, in)    | 100 n        | 4   |
| Envelope                    | 47 µ         | 1   |
| Fonte V9, VEE, 4V5, 1V8     | 47 µ         | 4   |
| 78M05 + MAX1044             | 10 µ         | 3   |
| PT2399 + resto              | 10 n, 22 n, 100 p, 2n2, 4µ7, 100 n, 47 µ | ver BOM |

---

## Jack FILT (o único que quebra cadeia)

Jack P2 estéreo **chaveado**:

- Ponta (tip) → entrada do VCF (o 10 k)
- Normal (shunt interno) → saída do SHAPE
- GND → terra

Plugou um cabo em FILT → o SHAPE some do filtro. É assim que um oscilador cru, ou a guitarra, entra direto no VCF.

Os outros P2 são só ponta + terra. Sem chave.

---

## O que não é 1 V/oitava

PITCH A/B são pots grandes, não CV expo. FCV e ECV são “molhar o parâmetro”, não afinar. VCV é gate / envelope, não velocity.

O teclado não entra nestes pots. O VCO cromático está na mesma placa e no mesmo `painel.svg` (`vco.md`): **SAW / TRI / PUL** escolhem a onda, o áudio cai no mix (passa pelo SHAPE) e o GATE do teclado entra no **VCV**.
