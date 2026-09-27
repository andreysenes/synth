# VOZ-9 — lista do VCO cromático

Módulo à parte (`vco.md`). Não soma nos ~R$ 610 do instrumento. Tudo novo. Preços estimados, varejo Brasil, set/2026, sem frete.

O CI é **AS3340** DIP-16 (Alfa) ou **V3340** (Coolaudio) — mesmos pinos. Sem tempco discreto e sem par de 2N3904.

---

## Semicondutores

| Qtd | Peça | Vai para | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 1 | AS3340 ou V3340 DIP-16 | oscilador | 55,00 | **55,00** |
| 1 | MC34063 DIP-8 | 9 V → 15 V | 3,00 | **3,00** |
| 1 | MAX1044 DIP-8 | −9 V | 6,00 | **6,00** |
| 1 | 78L12 TO-92 | +12 V do pino 16 | 2,00 | **2,00** |
| 1 | 78L05 TO-92 | +5 V (COARSE, PW, pino 13) | 2,00 | **2,00** |
| 1 | 79L05 TO-92 | −5 V do pino 3 | 2,00 | **2,00** |
| 1 | 1N5817 | proteção do P4 | 0,80 | **0,80** |
| 1 | 1N5819 | diodo do step-up | 1,00 | **1,00** |
| 1 | LED 3 mm | piloto | 0,40 | **0,40** |

**72,20.**

---

## Potenciômetros e trimpots

| Qtd | Peça | Knob / trim | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 3 | 100 kB 16 mm | COARSE, FINE, PW | 6,00 | **18,00** |
| 1 | 100 kA 16 mm | FM | 6,00 | **6,00** |
| 1 | multiturn 500 Ω | SCALE (1 V/oitava) | 3,50 | **3,50** |
| 1 | multiturn 10 k | TEMP | 3,50 | **3,50** |
| 2 | multiturn 100 k | RANGE, HF | 3,50 | **7,00** |
| 1 | multiturn 200 k | REF | 3,50 | **3,50** |

**41,50.** COARSE é B (linear): o curso é em oitavas. Trimpots na placa.

---

## Knobs, jacks, chicotes

| Qtd | Peça | Vai para | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 1 | knob Ø30 mm preto | COARSE | 4,00 | **4,00** |
| 3 | knob Ø15 mm preto | FINE, PW, FM | 2,50 | **7,50** |
| 5 | jack P2 3,5 mm | CV FM SAW TRI PULSE | 3,00 | **15,00** |
| 1 | P4 centro-negativo | 9 V | 3,00 | **3,00** |
| 1 | soquete fêmea 2×8 | J1 | 2,20 | **2,20** |
| 1 | soquete fêmea 2×6 | J2 | 2,00 | **2,00** |
| 1 | housing macho 2×8 | J1 | 1,80 | **1,80** |
| 1 | housing macho 2×6 | J2 | 1,60 | **1,60** |
| 40 | terminal crimp 2,54 mm | pinos (28 usados) | 0,10 | **4,00** |
| 1 | fio 24 AWG 2 m | chicotes | 4,00 | **4,00** |
| 1 | soquete DIP-16 | AS3340 | 1,50 | **1,50** |
| 2 | soquete DIP-8 | MC34063, MAX1044 | 1,50 | **3,00** |

**49,60.**

---

## Resistores — filme ¼ W, 1 % nos marcados

Pacote ~**8,00**.

| Valor | Qtd | Onde |
| --- | ---: | --- |
| 0,47 Ω | 1 | Rsc do MC34063 (pico ~0,6 A) |
| 1 k | 4 | série SAW, TRI, PULSE, PWM |
| 1k2 **1 %** | 2 | divisor do 15 V (um embaixo, um com o 12 k) |
| 1k5 **1 %** | 1 | Rs, em série com o SCALE |
| 4k7 | 1 | LED |
| 5k6 **1 %** | 2 | tempco, pinos 1 e 2 |
| 10 k | 1 | pulldown do pulso |
| 12 k **1 %** | 1 | divisor do 15 V, ramo de cima |
| 100 k **1 %** | 3 | CV, COARSE, FM → pino 15 |
| 100 k | 1 | hard sync → GND |
| 180 k **1 %** | 1 | RANGE, série com o trim |
| 330 k **1 %** | 1 | REF, série com o trim |
| 1M5 **1 %** | 1 | FINE → pino 15 |
| 2M2 | 1 | HF → pino 15 |
| 470 Ω | 1 | compensação do pino 15 |

O 100 k do CV é o resistor da oitava. Meça e fique com o que estiver mais perto de 100,0 k. O SCALE absorve o resto.

---

## Capacitores

| Valor | Tipo | Qtd | Onde | Unit. | Sub |
| --- | --- | ---: | --- | ---: | ---: |
| 470 p | cerâmico | 1 | Ct do MC34063 | 0,30 | **0,30** |
| 1 nF | C0G / filme 1 % | 1 | tempo, pino 11 | 1,50 | **1,50** |
| 10 nF | filme | 2 | pino 13, pino 15 | 0,40 | **0,80** |
| 100 nF | cerâmico | 6 | V9, V12, V15, −5, pino 9, pino 16 | 0,40 | **2,40** |
| 1 µF | filme | 4 | FM, SAW, TRI, PULSE | 1,50 | **6,00** |
| 10 µF / 25 V | eletrolítico | 6 | voo do 1044 (2), 78L12, 78L05, 79L05, folga | 0,60 | **3,60** |
| 47 µF / 25 V | eletrolítico | 2 | V9, VEE | 0,70 | **1,40** |
| 100 µF / 25 V | eletrolítico | 1 | V15 | 1,00 | **1,00** |
| 220 µH | indutor ≥ 500 mA | 1 | step-up | 4,00 | **4,00** |

**21,00.** O 1 nF do pino 11 é C0G ou poliestireno. X7R aí desafina com a temperatura.

---

## Caixa

| Qtd | Peça | Por quê | Unit. | Sub |
| --- | --- | --- | ---: | ---: |
| 1 | fenolite 160×110 mm | piso | 8,00 | **8,00** |
| 1 | caixa ~180×130×50 + face 160×110 | ao lado do VOZ-9 | 50,00 | **50,00** |

**58,00.**

---

## Total (sem frete)

| Pacote | Soma |
| --- | ---: |
| Semicondutores | 72 |
| Pots e trims | 42 |
| Knobs, jacks, chicotes | 50 |
| Resistores | 8 |
| Capacitores e indutor | 21 |
| Caixa | 58 |
| **Um VCO cromático** | ~ **251** |

Fonte 9 V: a do VOZ-9, em paralelo, se der corrente. Não entra de novo.
