# VOZ-9 — simulação SPICE (placa + interface)

Painel e BASE só se encontram nos chicotes **J1–J10** (`pcb.md`).  
O PT2399 vira atraso fixo; JFET/op-amp/NAB/EQ são analógicos.

## Instalar

```bash
brew install ngspice
cd voz-9/sim
./run.sh 00_fonte
```

* Painel tocável (`painel.html`): Web Audio + osciloscópio. Clique **Tocar**.
  Knobs/chaves alteram o som ao vivo. Export SPICE continua no painel (details).

## Layout

| Arquivo | Função |
| --- | --- |
| `lib.inc` | modelos + pots A/B/C + chaves + jack SW |
| `models/` | J201, 5457, diodos, TL072/5532, trilhos |
| `painel.cir` | chapa flat (pots, chaves, jacks) nos nós `j1_*`…`j8_*` |
| `base.cir` | esqueleto fenolite (LED 9V, J10, Csel, P4) — subckt opcional |
| `painel_state.inc` | `.param` dos knobs (UI escreve isto) |
| `painel.html` | UI sobre o layout do `painel.svg` |
| `jmap.inc` | documentação dos pinos J |
| `00_…` / `08_…` | testes por bloco |
| `harness_check.cir` | CUTOFF / FILT / MODE / H1 |
| `run.sh` | batch ngspice → `out/*.log` |

## Tapers (Brasil / Alpha)

| Letra | Tipo | No sim | Onde |
| --- | --- | --- | --- |
| **A** | log | `pot_log` | OSC A/B, AMOUNT, CUTOFF, WET, **PRE**, **OSC IN** |
| **B** | lin | `pot_lin` | SHAPE, DEPTH, TIME, F-BACK, VOLUME, **EQ 424** |
| **C** | antilog | `pot_antilog` | RATE |

`u` ∈ [0, 1] = CCW → CW.

## Contrato J (resumo)

Ver `jmap.inc` e `pcb.md`. Exemplos:

- **J1** OSC: pitch A/B, AMOUNT, SHAPE, CUTOFF, chaves A/B/DRONE  
- **J2** LFO: RATE, DEPTH, TREM (−1 flutter / 0 off / +1 tremolo), MODE (−1 pitch / 0 / +1 time)  
- **J3** DELAY: TIME, H1–H3, F-BACK, WET, STACK, VOLUME  
- **J4** FILT usa **TIP·SW·GND** — cabo abre o normal do SHAPE→VCF  
- **J6** GATE NA·GND, P4, LED 9V
- **J10** LEDs A · B · RATE · REP · IN (A·K); 11–12 NC  
- **J7** combo IN + **PRE** + **OSC IN**  
- **J9** EQ voz 424: LOW · MID F · MID G · HIGH  

## O que cada teste prova

| Bloco | Análise | Sucesso |
| --- | --- | --- |
| `00_fonte` | OP + tran curto | V9≈9, V5≈5, VEE≈−9, 4V5≈4.5, 1V8≈1.8 |
| `01_osc` | tran + measure | OSC A/B oscilam; enables via J1 |
| `01_fm` | tran gate step | período cai quando gate→1V8 |
| `02_noise` | OP | bias do J201 #3 |
| `04_shape` | tran senóide | clip Ge (1N34A) |
| `05_vcf` | AC | 1 polo; CUTOFF no gate |
| `06_vca` | OP + tran | ENV / DRONE / GATE |
| `07_lfo` | tran longo | tremolo (220 n) vs flutter (47 µ) |
| `08b_nab` | AC Bode | GRAVA 50 µs + LÊ |
| `08_pin6` | OP | tensões pin6 H1/H2/H3 |
| `08_echo` | tran 1.5 s | 3 atrasos + laço + WET |
| `09_leds` | tran 0,4 s | OSC acende no alto do quadrado; IN/RATE/REP via BC547; 40 mV fica escuro |
| `harness_check` | OP | pinagem painel↔BASE |

## TIME → ms (PT2399 comportamental)

Usado em `08_echo.cir` (`.param time_set=0|1|2`):

| TIME | H1 | H2 | H3 |
| --- | ---: | ---: | ---: |
| mín (`time_set=0`) | 30 ms | 100 ms | 240 ms |
| meio (`1`) | 100 ms | 225 ms | 425 ms |
| máx (`2`) | 160 ms | 375 ms | 585 ms |

Faixas do `esquema.md` (30–170 / 80–400 / 200–620). O chiado da zona vermelha **não** entra no SPICE.

Rede analógica do pino 6: `08_pin6.cir` (2 k / 22 k / 68 k + TIME 10 k).

## Fluxo de mudança

1. Knob/chave no `painel.html` **ou** R/C no `.cir` da BASE.  
2. Pinagem: `pcb.md` + `painel.cir` + `base.cir` + `jmap.inc` juntos.  
3. Valor: `.cir` + `esquema.md` / `bom.md` / `jlcpcb-bom.csv`.  
4. `./run.sh <bloco>`  
5. Só então mexer no SVG da PCB.

## Limites

- MP20 ≈ 1N34A; Vgs(off) do J201 é “médio”.  
- Sem clock do ICL7660; trilhos ideais.  
- Chicote = 0,1 Ω; sem parasitics de cobre.
