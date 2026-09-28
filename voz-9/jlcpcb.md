# VOZ-9 — BOM para a JLCPCB

> **Status:** JLCPCB/PCBA SMD foi escolhida para o baseline KiCad. Este arquivo e
> `jlcpcb-bom.csv` são ponto de partida, não BOM liberada. Estoque, códigos
> LCSC, footprints, encapsulamentos, substitutos, BOM e CPL devem ser
> revalidados após o esquema KiCad, conforme `kicad-requisitos.md`.

Arquivo para subir no [BOM Tool](https://jlcpcb.com/parts/bom-tool): **`jlcpcb-bom.csv`**.

Formato do [guia da JLCPCB](https://jlcpcb.com/help/article/bill-of-materials-for-pcb-assembly): `Comment`, `Designator`, `Footprint`, `LCSC Part #`.

Lista de rua (Brasil, THT, fenolite): `bom.md`. Esta aqui é a **equivalente SMT / LCSC**, para ver preço e estoque e, no futuro, montar FR4.

---

## Como subir

1. Abra [jlcpcb.com/parts/bom-tool](https://jlcpcb.com/parts/bom-tool).
2. **Upload Your BOM** → `jlcpcb-bom.csv`.
3. Confira o matching. C-number preenchido deve cair certo. Se um Extended estiver em falta, o próprio tool sugere substituto.
4. **Procure** trava o estoque na sua parts library. Só então faz sentido um pedido PCBA.

Mínimos da JLCPCB (reel / attrition) são maiores que a qtd do circuito. Um VOZ-9 não gasta um reel de 10 k — o tool avisa.

---

## O que este CSV *é*

Passivos **0805 1 %** da biblioteca **Basic** (sem taxa extra de peça). CIs em SOP/SOIC/DPAK. JFETs em SOT-23.

| Peça do `bom.md` | Aqui | LCSC |
| --- | --- | --- |
| NE5532 DIP-8 | NE5532DR | [C7426](https://www.lcsc.com/product-detail/C7426.html) |
| TL072 ×3 | TL072CDR | [C67473](https://www.lcsc.com/product-detail/C67473.html) |
| MAX1044 | **ICL7660CSA** (pino a pino) | [C42421900](https://jlcpcb.com/partdetail/TDSEMIC-ICL7660CSA/C42421900) |
| 78M05 | L78M05ABDT-TR | [C58069](https://jlcpcb.com/partdetail/C58069) |
| PT2399 DIP-16 | PT2399-SN SOP-16 | [C126407](https://www.lcsc.com/product-detail/C126407.html) |
| J201 TO-92 | MMBFJ201 | [C891687](https://www.lcsc.com/product-detail/C891687.html) |
| 2N5457 | MMBF5457 | [C2830807](https://www.lcsc.com/product-detail/C2830807.html) |
| 1N5817 | SS14 | [C2480](https://jlcpcb.com/partdetail/C2480) |
| 1N4148 | 1N4148WS | [C2128](https://jlcpcb.com/partdetail/C2128) |
| LED 3 mm | LED vermelho 0805 | [C84256](https://jlcpcb.com/partdetail/C84256) |
| 47 µ / 16 V | 22 µ / **25 V** 0805 | [C45783](https://jlcpcb.com/partdetail/C45783) |
| 2 n2 filme | 2,2 n C0G 0805 | [C28260](https://jlcpcb.com/partdetail/C28260) |
| 3,3 n filme | 3,3 n X7R 0603 | [C1613](https://jlcpcb.com/partdetail/C1613) |

47 µ 16 V em 0805 Basic é 6,3 V — morre em 9 V. O 22 µ / 25 V aguenta o trilho.

**Não compre o MAX1044CSA+ (C143327)** no tool: estoque 1, MOQ 2, ~US$ 32 na cotação de 5 placas. O ICL7660 é o mesmo inversor. Oscila mais baixo (pode assobiar no áudio); se ouvir, um 100 p no pino 7 empurra o clock.

**Não misture esta lista na fenolite atual.** SOP-16 / SOT-23 não cabem nos furos DIP / TO-92.

---

## O que o tool *não* tem (compra no `bom.md`)

| Qtd | Peça | Por quê |
| ---: | --- | --- |
| 2 | MP20 / AC128 | germânio — LCSC não tem. 1N60P da JLC é Schottky, não Ge |
| 17 | pots 16 mm incl. PRE + OSC IN + EQ 424 | painel, não SMT |
| 2 | trimpot 100 k | |
| 17 | knobs + capa GATE | |
| 9 | chaves MTS + GATE | |
| 11 | jack P2 3,5 mm | |
| 2 | combo XLR+P10 clone | |
| 1 | P4 9 V | |
| 4 | cabo P2 | |
| 1 | fio 24 AWG 10 m | chicotes painel → BASE |
| 9 | fêmea/macho 2×N (3 / 6 / 8 / 10) | J1–J9, passo 2,54 mm |
| 8 | soquete DIP | U1–U4, U6–U8, **U9** — some se for SOP |
| 1 | caixa + face 220×160 | legado; baseline KiCad: face 300×300 e PCB 200×150 |
| 1 | fenolite 220×160 | legado; baseline KiCad é FR-4 JLCPCB 200×150 |

Essas linhas **não** estão no CSV de propósito: o tool marcaria unmatched e sujaria o preço.

---

## Designators

Inventados para o matching. Ainda não há netlist KiCad. Quando existir PCB FR4, estes refs têm de bater com o CPL.

- **U1** 5532 · **U2** osc · **U3** NAB · **U4** ICL7660 · **U5** 78M05 · **U6–U8** PT2399 · **U9** EQ voz 424
- **Q1–Q6** J201 no circuito · **Q8 Q9** folga · **Q7** LFO
- **D1** proteção · **D2–D5** 4148 · **LED1** piloto
- **R1…R81** e **C1…C71** na ordem da `bom.md` (+ passivos EQ em §3b)

---

## Cotação BOM Tool — 13 set 2026

**PCB Assembled Qty = 5.** O tool não cobra “um instrumento”: multiplica por 5 e ainda arredonda para o mínimo do feeder. Por isso 32× 10 k vira **170** peças, 8× 22 µ vira **40**, 3× PT2399 vira **15**.

CSV atual: **ICL7660CSA C42421900** no lugar do MAX1044. Matching **36 / 37** — a linha *Not Matched* vazia é lixo do upload; ignore.

| | USD |
| --- | ---: |
| **Ext Total (36 linhas, qty 5)** | **54,67** |
| em estoque (35 linhas) | 40,29 |
| PT2399 C126407 (15 pç, pre-order, MOQ 8) | 14,38 |
| 22 µ / 25 V C45783 (40 pç) | 9,83 |
| 8× MMBFJ201 C891687 (40 pç) | 6,52 |
| 10 µ / 25 V (50 pç) | 4,22 |
| MMBF5457 (10 pç) | 3,31 |
| 100 n 0805 (130 pç) | 2,55 |
| ICL7660CSA (5 pç) | 1,09 |
| resto Basic + TL072 + 5532 + 78M05 | ~12,77 |
| **por placa SMT** (54,67 ÷ 5, com sobra) | **~10,93** |

### O que isso *não* é

- Não é o custo de **1** VOZ-9. É SMT para **5** placas + sobra de máquina.
- Não inclui PCB FR4, montagem SMT, stencil, frete, imposto, nem pots / jacks / caixa (`bom.md`).
- PT2399 está *Pre-order* (estoque 4, precisa 15). Os **US$ 14,38 são referência** — a JLC confirma em até 48 h depois do pagamento.

PT2399 fica C126407. Se o tool insistir em pre-order, espere estoque ou compre os 3 DIP no Brasil (~R$ 21) e deixe U6–U8 como *Customer Supply*.
