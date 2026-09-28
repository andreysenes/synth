# VOZ-9 — escola das peças

Este arquivo é o caderno de estudo do instrumento. Pressupõe eletrônica **básica** (lei de Ohm, saber o que é terra, já ter soldado um LED). O resto se aprende aqui, peça por peça, no circuito real — não num curso solto.

Esquema: `esquema.md`. Pré de mic: `pre-vocal.md`. Placas: `pcb.md`. Compra: `bom.md`.

Datasheets mudam de URL. Se um link morrer: código da peça + `datasheet PDF`.

---

## Como estudar sozinho

Não leia tudo de uma vez. O caminho que fecha com a montagem:

1. **§ Fundamentos** — uma sentada. É o vocabulário do resto.
2. **Fonte** (1N5817, 78M05, MAX1044, LED) — primeiro bloco que se testa.
3. **Osciladores** (TL072/4558, pots 500 k, J201 #1 e #2).
4. **Shape / filtro / VCA** (MP20, J201 #3–#5, 1N4148).
5. **LFO** (2N5457, TREM 3 pos).
6. **Fita** (PT2399, TL072).
7. **Voz** (NE5532, combo).

Em cada peça há quatro blocos:

| Bloco | Para quê |
| --- | --- |
| **Ideia** | O que a peça *é*, em português |
| **No VOZ-9** | Onde ela entra *neste* circuito |
| **Banco** | O que medir ou ouvir para saber se está viva |
| **Datasheet** | PDF. Não precisa ler inteiro: capa, pinagem, “absolute maximum” |

Se uma palavra do esquema não fizer sentido, volta aos fundamentos. Se o fundamento não bastar, a própria peça abaixo aprofunda.

---

## Fundamentos — o que o VOZ-9 assume que você entende

### Tensão, corrente, terra

A **fonte de 9 V** é uma diferença: um fio está 9 volts *acima* do outro. Chamamos o fio de baixo de **GND** (terra do circuito — não é o terra da parede). Corrente é o que *passa*; tensão é o que *empurra*.

O áudio no VOZ-9 é uma tensão que sobe e desce no tempo, uns poucos volts, em torno de um ponto médio. Sem esse sobe-e-desce, o alto-falante não se mexe.

### Por que existe o 4V5

Os osciladores e vários JFETs não veem +9 V e −9 V. Eles veem **9 V simples**. O “meio” do áudio precisa ser inventado: dois resistores iguais (10 k e 10 k) entre V9 e GND criam **4,5 V**. Esse nó é o **terra virtual** — o silêncio do sinal. O som oscila em volta dele, não em volta do GND.

O pré de microfone é o contrário: o NE5532 quer **+9 V e −9 V**. Aí o silêncio *é* o GND. Quem fabrica o −9 V é o MAX1044.

Três “terras” mentais, um só fio GND na placa:

| Nome | Volts vs GND | Quem usa |
| --- | --- | --- |
| GND | 0 | jacks, fonte, MAX1044 pino 4 |
| 4V5 | +4,5 | oscs, mix, vários JFETs |
| 1V8 | ~+1,8 | bias do VCF e do VCA (divisor 22 k + 5k6) |
| V9 | +9 | quase tudo |
| V5 | +5 | só os PT2399 |
| VEE | −9 | NE5532 e um pouco de germânio |

### Resistor

Atrasa a corrente. `V = R × I`. Dois em série formam um **divisor**: o nó do meio é uma fração da tensão. Pots *são* divisores com o ponto do meio móvel.

¼ W basta em tudo aqui (9 V em 1 k = 0,08 W). Os 2k2 e 22k do mic pedem **1 %** e **iguais em pares**: o pré diferenciais só rejeita ruído do cabo se os dois lados forem o mesmo número.

### Capacitor

Dois pratos e um isolante. Continua **não passa** (depois de carregado). Alternada **passa**, com mais facilidade quanto maior o C e quanto mais aguda a frequência.

Três papéis no VOZ-9:

1. **Acoplo** (100 n, 10 µ no XLR) — deixa o áudio e bloqueia o contínuo. Sem isso, um estágio empurra o bias do outro e o som some ou distorce.
2. **Tempo** (100 n no OSC A, 10 n no OSC B, 220 n / 47 µ no LFO) — o cap enche e esvazia pelo resistor. `τ ≈ R × C`. Maior C ou maior R = mais lento = tom mais grave / LFO mais lento.
3. **Reserva** (47 µ na fonte, 10 µ no 5 V) — segura o trilho quando o circuito puxa um pico. Sem eles o LED pisca e o delay “engasga”.

Eletrolítico tem lado: a **listra é o negativo**. Invertido, estufa. Cerâmico e filme não têm lado.

### Diodo

Válvula de um sentido. Só conduz quando o ânodo está uns **Vf** acima do cátodo.

| Tipo | Vf típico | Aqui |
| --- | --- | --- |
| Silício (1N4148) | ~0,7 V | envelope do GATE |
| Schottky (1N5817) | ~0,3 V | proteção da fonte |
| Germânio (MP20 como diodo) | ~0,2 V | clipper “macio” |
| LED | ~1,8–2,2 V | piloto (sempre com resistor) |

### Transistor bipolar vs JFET (o essencial)

O **bipolar** (NPN/PNP) é controlado por *corrente* na base. O MP20 *é* um PNP, mas no VOZ-9 a gente une base e coletor e usa só a junção — vira diodo.

O **JFET** (J201, 2N5457) é controlado por *tensão* no **gate**. O gate quase não puxa corrente. Pense numa torneira: o gate é o registro.

Canal N, depleção (os nossos):

- Gate no mesmo potencial do source (`Vgs = 0`) → canal **aberto**, conduz.
- Gate mais negativo que o source → canal **afina**, até fechar (**pinch-off**, `Vgs(off)`).

Essa tensão de fechamento **muda de um J201 para o outro** (0,3 V a 1,5 V). Por isso compramos 8 e escolhemos. Não é defeito: é o componente.

TO-92, lado chato virado para você, pernas para baixo, lote Fairchild/ON: **D | G | S** (esquerda, meio, direita). Clone barato às vezes inverte — **confirma no datasheet do saco**.

### Op-amp em uma frase

Dois pinos de entrada (`+` e `−`) e uma saída. A saída corre para o teto ou para o chão tentando fazer `+` e `−` ficarem iguais — *desde que* você feche um laço de **feedback** com resistores. A razão desses resistores *é* o ganho.

```
ganho inversor    ≈  Rf / Rin
ganho não-inversor ≈ 1 + Rf / Rg
ganho em dB       ≈ 20 × log10(razão)     ×10 ≈ +20 dB, ×100 ≈ +40 dB
```

DIP-8 dual: **duas** metades no mesmo plástico. Pino 8 = +alimentação, pino 4 = −alimentação (ou GND, se for 9 V simples). Sempre soquete neste projeto.

### O que é “nível” de áudio

| Nome | Ordem de grandeza | Onde |
| --- | --- | --- |
| Mic (SM58 falando) | ~1–10 mV | XLR IN |
| Pedal / linha instrument | ~100 mV–1 V | P10, SEND, VOLUME |
| Linha de mesa (+4 dBu) | ~1 V | não é o nosso XLR OUT |
| Nosso XLR OUT | ~20 mV (pad) | canal de *mic* da mesa |

O pad (10 k + 220 Ω) é um divisor: entrega uns 2 % do VOLUME para o XLR, para a mesa achar que é um microfone.

### Como ler um datasheet sem sofrer

1. Primeira página: o que o chip *promete*.
2. Desenho dos pinos. **Decora isso.**
3. Tabela *Absolute Maximum Ratings*: passar disso = peça morta (PT2399: 6,5 V no VCC; 9 V mata).
4. Circuito de aplicação: o PT2399 *é* aquele desenho de caps em volta.

O resto (gráficos, ruído em nV) você volta quando o circuito já toca.

---

## Semicondutores discretos

### J201 — a torneira de tensão do instrumento

**Ideia.** JFET N pequeno, fácil de “abrir e fechar” com poucos volts no gate. É o coringa analógico do VOZ-9: a mesma peça vira vibrato, ruído, filtro, volume e buffer. O que muda é *onde* o canal está no circuito (paralelo ao cap, à terra, em série no áudio…).

**No VOZ-9** — 6 no circuito, 2 extra para escolher:

| # | Papel | O que o gate faz |
| --- | --- | --- |
| 1 | FM do OSC A | Paralelo ao cap de tempo. Gate sobe → o cap esvazia mais rápido → o tom **sobe** e amolece |
| 2 | FM do OSC B | Igual |
| 3 | Noise | Quase sem sinal no gate: a junção chiada vira o “vento” no mix |
| 4 | VCF | Canal à terra depois de um 10 k. Conduzindo = agudo some (filtro fecha). Pinch-off = filtro abre |
| 5 | VCA | Canal **em série** no áudio. Gate no 1V8 = som passa (drone). Gate em 0 = silêncio |
| 6 | Buffer | Só se o VCF carregar o clipper. **Não** é o NAB — isso é o TL072 |

O mais **vivo** (fecha com pouco Vgs, conduz fácil) → **VCF**. Um par parecido → FM A e B. Os 2 extra da BOM são reserva / casamento.

**Banco.** Com o circuito ligado, GATE em drone, WET no mínimo: gira CUTOFF. Tem de ir de abafado a aberto. Se os dois extremos soarem iguais, aquele J201 #4 é um “morto” ou está invertido (D/S).

**Em geral.** Buffer de Tube Screamer, amp-in-a-box (Tweed/Wampler), compressores JFET. Primos: J202 (mais corrente), MMBFJ201 (SMD). O 2N5457 *não* substitui bem no VCA.

**Datasheet.** [ON Semi J201/J202](https://www.onsemi.com/pdf/datasheet/j201-d.pdf)

**Não faça.** Gate sem resistor “no ar” em bancada — estática. Não espere 1 V/oitava: o J201 no pitch é *molho*, não teclado.

---

### 2N5457 — o relógio lento

**Ideia.** Também é JFET N, mas fecha com mais tensão e conduz menos. Péssimo VCA de guitarra; ótimo para oscilar devagar. Três caps em cadeia atrasam a fase ~180° e o transistor devolve o sinal — nasce um **LFO** (low frequency oscillator): um pulso que você não ouve como nota, ouve como *movimento*.

**No VOZ-9.** Um só, comprado novo. Drain → jack LFO e → DEPTH → LFO MODE. A chave **TREM** (ON–OFF–ON) escolhe 220 n (tremolo), **meio = off**, ou 47 µ (flutter).

**Banco.** LED não mostra LFO. Ouça no jack LFO no amp, volume baixo: “fom-fom” lento (flutter) ou trêmolo rápido. Sem isso, a rede de 220 n ou o JFET está invertido.

**Em geral.** Chorus, phaser, Univibe. Família 2N5457 / 58 / 59.

**Datasheet.** [ON Semi 2N5457](https://www.onsemi.com/pdf/datasheet/2n5457-d.pdf)

**Não faça.** Trocar por J201 “porque é JFET” sem recalcular os caps — a taxa muda e pode parar de oscilar.

---

### MP20 — germânio, usado como diodo mole

**Ideia.** Transistor PNP de germânio (rádios soviéticos). A junção germânio “abre” uns 0,2 V, não 0,7 V. O clip fica *redondo*: harmônicos pares, corpo, não o “zzz” do silício.

No VOZ-9 **não amplifica**. Base e coletor juntos = um diodo de duas pernas.

**No VOZ-9.**

| # | Onde | O que você ouve |
| --- | --- | --- |
| 1 | Depois do SHAPE, à terra | O quadrado ganha “lado”, deixa de ser oco |
| 2 | No laço do echo | Repeats escuros, fita gastando |

**Banco.** SHAPE no mínimo = quase limpo. SHAPE no máximo = cresce médio e “sujeira” doce. Se só ficar mais baixo, o diodo está invertido ou morto (calor de solda).

**Em geral.** Fuzz Face, Tone Bender. Primos: AC128, OC75, 1N34A / 1N60 se for *só* o diodo.

**Datasheet.** Folha de época, não PDF de 2020: [MP20 / МП20](https://www.radiolocman.com/datasheet/data/?di=148299). Trate eletricamente como AC128.

**Não faça.** Ferro alto, sem pausa. É a última peça a soldar. 1N4148 no lugar *funciona* e mata o caráter.

---

### 1N5817 — o seguro da tomada

**Ideia.** Schottky: mesma válvula, menos queda. Se você plugar a fonte **ao contrário**, ele não deixa o +9 V entrar no circuito. A queda pequena (~0,3 V) faz o instrumento ainda ver ~8,7 V — um 1N4001 comeria 0,7 V e o som murcharia.

**No VOZ-9.** Logo depois do P4, antes de tudo. Fonte Boss: **centro negativo**.

**Banco.** Multímetro no V9: ~9 V (na verdade 8,6–9,2). 0 V com a fonte invertida = o diodo fez o trabalho. −9 V aqui = você mediu o VEE sem querer.

**Datasheet.** [ON Semi 1N5817](https://www.onsemi.com/pdf/datasheet/1n5817-d.pdf) · [Vishay](https://www.vishay.com/docs/88525/1n5817.pdf)

**Não faça.** Achar que “qualquer diodo serve”. 1N5818/19 (30/40 V) servem. 1N4007 serve de emergência, com 0,4 V a menos no V9.

---

### 1N4148 — a trava do envelope

**Ideia.** Diodo de sinal, silício, barato. Aqui é uma **válvula de carga**: o botão GATE enche o cap 47 µ através dele. Quando você solta, o diodo *não deixa* a carga voltar pelo botão. O cap só esvazia pelo 220 k — isso *é* o decay (~1 s).

**No VOZ-9.** 1V8 → GATE (botão) → 1N4148 → nó ENV (gate do J201 #5). Segundo 1N4148: PRE → 100n → 10k → diodo → ENV (**envelope da fala**, tap fixo). **OSC IN** é o mix de áudio osc ↔ XLR, não este envelope.

**Banco.** Chave em GATE (não drone). Aperta: som aparece. Solta: some em ~1 s. Com SM58 e PRE a meio, **falar** também abre; calar fecha com a mesma cauda. Se some na hora, o 47 µ está invertido ou o 220 k está em curto. Se nunca some, o 1N4148 está invertido ou o DRONE está vazando 1V8.

**Datasheet.** [Vishay 1N4148](https://www.vishay.com/docs/81857/1n4148.pdf)

**Não faça.** Usar no SHAPE. **Quatro** no BOM: envelope (botão + fala), CLK, folga.

---

### LED 3 mm — “tem 9 V”

**Ideia.** Diodo que emite luz. Sempre com resistor (aqui 4k7): senão puxa corrente até queimar. Vf ~2 V; o 4k7 em 9 V limita a uns 1,5 mA — visível, não ofusca.

**No VOZ-9.** O POWER sai no **J6** pinos 1–2. O baseline KiCad acrescenta
nove indicadores no J11: CLIP, GATE/ENV, LFO, OSC A/B, H1–H3 e STACK. Todos
são vermelhos difusos de 3 mm, alvo de 1,5 mA; os estados de chaves usam polo
isolado e os três estados dinâmicos usam drivers discretos.

**Banco.** Fonte boa + 1N5817 no sentido certo = acende. Apagado: fonte, jack P4 ou o 4k7.

**Datasheet.** Qualquer 3 mm, ex. [Kingbright L-7104](https://www.kingbrightusa.com/images/catalog/SPEC/L-7104ID.pdf)

---

### VU analógico — nível de saída

**Ideia.** Galvanômetro de painel que mostra o nível médio do áudio. O modelo
escolhido tem frente nominal de **35 × 35 mm**, movimento de **500 µA**,
corpo anunciado de **37 × 35 × 35 mm**, massa de **21 g**, resistência de
**630 Ω** e escala −20…+5 VU. Fundo de escala elétrico:
`0,0005 A × 630 Ω ≈ 0,315 V DC`.

**No VOZ-9.** Mede pós-VOLUME, antes dos pads de saída, por driver/retificador
de alta impedância na BASE. J10 leva `M+`, `M−`, `L+` e `L−`. A luz quente é
filamento de 6–12 V, sempre ligado com o equipamento em V9 protegido. Corrente,
inrush e temperatura devem ser medidos; deixar opção de limitador em série.

**Banco.** Nunca ligue o movimento diretamente à saída. Injete nível conhecido,
ajuste o trim, confira repetibilidade e impeça que sobrecarga mantenha o ponteiro
batendo no fim. Meça também corrente e temperatura da lâmpada.

**Mecânica.** É frágil. Comprar uma amostra antes do painel final, medir corpo,
profundidade, furos e recorte com paquímetro, usar alívio de tração e manter
seco. A tolerância de 1–2 cm anunciada por uma listagem é inutilizável para CAD;
não confiar nas dimensões até medir.

---

## Circuitos integrados

### PT2399 — a “fita” de 5 volts

**Ideia.** Um chip que **grava um pedaço de som e toca atrasado**. Por dentro: converte o áudio em números (ADC), guarda numa RAM pequenininha (44 kbit), lê de novo (DAC) e filtra. Não é fita magnética. O *som* de fita vem do filtro ruim, do clock baixo e da saturação que a gente põe em volta (MP20, NAB, três heads).

O **tempo** é um relógio interno (VCO). Você afina esse relógio com um **resistor no pino 6**: mais ohms = relógio mais lento = delay mais longo. Um pot (TIME) + um resistor fixo diferente em cada chip = três heads com o mesmo knob.

**No VOZ-9** — três chips, um motor:

| Head | Extra no pino 6 | O que é |
| --- | --- | --- |
| H1 | 2 k + TIME | slap ~30–170 ms |
| H2 | 2 k + 22 k + TIME | médio ~80–400 ms |
| H3 | 2 k + 68 k + TIME | cauda ~200–620 ms |

Pino 16 = entra o som (depois do NAB). Pino 14 = sai. As chaves H1–H3 ligam ou calam cada saída no mix. O LFO no pino 6 (via 220 k) = flutter: o relógio treme, os três heads desafinam juntos.

**Por que 5 V e 78M05.** O PT2399 aceita 4,5–5,5 V. 9 V no pino 1 = funeral. Cada um puxa ~25 mA; três = ~75 mA. 78L05 ferve. O **78M05** (500 mA) é o tamanho certo.

**Por que ≥ 2 k no pino 6.** Abaixo disso o VCO no power-up às vezes **trava** (silêncio digital, chip quente). Não tire esse piso.

**Banco.** Um chip de cada vez. TIME no mínimo, H1 on, o resto off: slapback. Se nada, meça 5 V no pino 1 e ≥ 2 k do pino 6 ao TIME. Chiado no H3 no máximo = normal (zona vermelha do Echo Master).

**Em geral.** Todo delay/chorus barato desde ~2000. Não é MN3005 (BBD analógico). O “digital ruim” *é* o timbre.

**Datasheet.** [Princeton PT2399](https://www.princeton.com.tw/Portals/0/activeforums_Attach/PT2399-s.pdf) — copie o circuito de caps; a tabela R vs ms está lá.

Pinos que você precisa decorar: **1 VCC, 2 REF, 3/4 GND, 6 VCO, 14 out, 16 in**.

---

### MAX1044 — a máquina de fazer menos nove

**Ideia.** **Charge pump**: um cap “de voo” carrega em +9 V e é virado, como um balde que você enche e despeja do outro lado. O resultado no pino 5 é cerca de **−9 V**. Pouca corrente (uns 10–20 mA). Chega para um NE5532; não chega para três PT2399.

Irmão: ICL7660, TC1044S — mesma pinagem.

**No VOZ-9.** V9 no pino 8, GND no 4, VEE no 5. Caps 10 µ entre 2–4 e 3–5 (veja o esquema). Esse −9 V é o trilho negativo do pré de mic.

**Banco.** Multímetro: pino 5 vs GND ≈ −8 a −9 V. 0 V = cap invertido, chip morto ou pino 8 sem 9 V. +9 V no 5 = montou ao contrário.

**Datasheet.** [Analog MAX1044 / ICL7660](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX1044-ICL7660.pdf)

**Não faça.** Alimentar a fita por aqui. Invertir o eletrolítico de voo.

---

### 78M05 — o 5 V honesto

**Ideia.** Regulador **linear**: entra ~9 V, sai 5 V firmes, a diferença vira calor. Precisa de uns 2 V de folga na entrada (por isso 9 V serve e 6 V não). TO-220, 500 mA.

**No VOZ-9.** Um para os três PT2399. 10 µ + 100 n *em cada* chip, perto dos pinos — não um cap só no regulador.

**Banco.** 5,0 V ±0,2 no pino do meio (TO-220: in / GND / out, tab = GND). Quente após um minuto com 3 chips = normal. Escaldante + 4 V de saída = sobrecarga ou curto no V5.

**Datasheet.** [ST L78M05](https://www.st.com/resource/en/datasheet/l78m.pdf)

**Não faça.** 78L05 (TO-92) no lugar. Tab do 78M05 na caixa de metal sem mica = curto de GND (às vezes ok) ou de outro trilho (ruim).

---

### NE5532 — o ouvido do microfone

**Ideia.** Dois op-amps feitos para áudio: pouco chiado, consegue empurrar cabo. Nasceu em mesa de mixagem. Quer alimentação **dupla** (±). Em 9 V simples o swing some e o SM58 some no ruído.

**Por que diferencial.** O cabo de mic traz o mesmo chiado nos dois fios (pinos 2 e 3). O 5532-A subtrai um do outro: o chiado some, a voz (oposta nos dois fios) sobe. Isso *substitui* o transformador 1:10. Os resistores têm de ser iguais (1 %), senão o chiado vaza.

Conta que importa:

```
SM58 ~ 3 mV
× 10  (5532-A, 22k/2k2)  = 30 mV
× 11  (5532-B, 10k/1k)   = 330 mV   → PRE CW = nível de pedal, PT2399 feliz
```

**No VOZ-9.** BASE (U1). A dirige o XLR; B → PRE → **SEND** (pré-EQ) e mix; mix → **EQ voz (U9 TL072)** estilo 424 → SHAPE. Sem XLR, PRE escala os oscs. Os pinos do combo IN chegam por cabo. Guitarra **não** passa aqui: vai no P10 → AMOUNT.

**Banco.** SM58, PRE a meio, WET no mínimo, fone/amp no P10 OUT. Falar deve ser alto e limpo. PRE no mínimo = silêncio na voz; VOLUME não muda isso. Chiado de rádio = 100 p no XLR faltando ou malha do cabo solta. Zero som + 5532 quente = phantom 48 V passou — chip novo.

**Em geral.** Canal de mesa, fone, DI ativa. **Não** use LM358 (distorce no cruzamento zero, chiado).

**Datasheet.** [TI NE5532](https://www.ti.com/lit/ds/symlink/ne5532.pdf)

**Não faça.** Phantom neste IN. Pino 8 = +9, pino 4 = −9 (VEE), nunca os dois no +9.

---

### TL072 ou 4558 — a curva da fita (NAB)

**Ideia.** Gravador de fita de verdade **não** grava “plano”. Na gravação corta um pouco de grave e empurra agudo; na leitura faz o inverso. O que sobra é “fita”, não um telefone. Isso se chama curva **NAB** (ou IEC). Constantes clássicas: 50 µs (~3 kHz) e 3180 µs (~50 Hz).

O chip está **no caminho** da fita (`esquema.md` §8b). Sem ele no soquete o eco some. Uma metade **grava** (HPF + shelf), a outra **lê**.

TL072 = entrada JFET, mais “hi-fi”. 4558 = o som de pedal dos anos 80. Os dois servem; compre TL072 se for um só.

**No VOZ-9.** BASE (U3), ±9 V. ½ A = GRAVA (antes dos pin 16). ½ B = LÊ (depois do mix dos pin 14). Caps 3,3 n = o 50 µs. Esquema fechado: `esquema.md` §8b.

**Banco.** Eco com e sem o chip (soquete): com NAB o repeat tem um pouco de ar e o grave não some para sempre. Sem = só lama. Os dois são válidos; a escolha é estética.

**Datasheet.** [TI TL072](https://www.ti.com/lit/ds/symlink/tl072.pdf) · [TI RC4558](https://www.ti.com/lit/ds/symlink/rc4558.pdf)

---

### Op-amp dos osciladores — os dois quadrados

**Ideia.** **Oscilador de relaxação**: a saída bate no teto, o cap enche pelo pot de pitch, a entrada “−” passa de um limiar, a saída bate no chão, o cap esvazia, repete. O resultado é um **quadrado**, não um seno. Duas metades, dois osciladores. Quando as frequências se aproximam você ouve o **batimento** — o som do instrumento.

Não é MiniMoog. Não há 1 V/oitava. Os pots 500 kA *são* a escala.

**No VOZ-9.** OSC A (~10 Hz–500 Hz, cap 100 n). OSC B (~100 Hz–5 kHz, cap 10 n). A zona em que se encontram (~100–500 Hz) é onde o batimento vive.

**Banco.** Um osc de cada vez no amp, volume baixo. Gira o pitch: deve ir de “motor” a “apito”. Os dois no AMOUNT no meio: uivo lento quando os tons se cruzam.

**Datasheet.** O código na tampa. Apagou: [RC4558](https://www.ti.com/lit/ds/symlink/rc4558.pdf).

---

## Potenciômetros — três pernas, uma ideia

Um pot é um resistor com uma tomada no meio (**cursor**). As pontas são fixas. Girar = escolher que fração da tensão (ou que valor de R) você quer.

**Taper** é *como* a resistência cresce na rotação. O ouvido humano é logarítmico: o meio de um pot **linear** em volume parece “quase no máximo”. Por isso mix e volume usam **A** (log / áudio). Controle de “quantos ohms no circuito” (TIME, SHAPE, F-BACK) prefere **B** (linear). **C** é o contrário do A: mais curso no começo — útil no LFO para sobrar faixa lenta.

No Brasil (Alpha): **A = log, B = lin**. Lote japonês antigo às vezes inverte. Leia o corpo do pot.

| Peça | Taper | Knob | Por que |
| --- | --- | --- | --- |
| 500 kA | log | OSC A / B | Uma volta cobre grave→agudo sem “tudo no fim” |
| 100 kA | log | AMOUNT, CUTOFF | Balanço e filtro no ouvido |
| 1 kB | lin | SHAPE | É um resistor de drive, não um volume |
| 100 kC | antilog | LFO | Tempo de mais na região lenta |
| 10 kB | lin | TIME | R do pino 6 ≈ tempo |
| 25 kB | lin | DEPTH | Quanto de LFO |
| **B100 k** | lin | **F-BACK** | Achar o ponto em que a fita oscila |
| **A100 k** | log | **WET** | 50/50 cai no meio do curso |
| **A100 k** | log | **PRE** | Mic → SEND/mix; sem XLR = pré-amp dos oscs |
| **A100 k** | log | **OSC IN** | Mix osc (CCW) ↔ XLR (CW) |
| 100 kB ×4 | lin | **LOW · MID F · MID G · HIGH** | EQ voz 424 (± dB, flat no meio) |
| 2 kB | lin | VOLUME | Nível de saída |
| trim 100 k ×2 | lin | teto F-BACK / res | Chave de fenda, não knob |

Todos os pots saem da `bom.md`. Nada de recuperar de outro pedal.

**Banco.** Cursor no meio, pontas: num A, as resistências *não* são iguais (ex. 20 k e 80 k num 100 k). Num B, são ~50/50.

**Catálogo.** [Alpha 16 mm](https://www.taiwanalpha.com) — família, não um PDF único.

---

## Chaves — o que cada alavanca *é*

> **Baseline KiCad com LEDs:** OSC A/B passam a **DPST ON–OFF** e
> H1/H2/H3/STACK a **DPDT ON–ON**. O segundo polo é exclusivo do LED vermelho
> e fica eletricamente isolado do áudio. Os tipos SPST/SPDT abaixo descrevem a
> referência legada sem indicadores.

Pólo = quantos circuitos. Direção = quantos lugares o contato pode ir.

- **SPST**: um circuito, liga/desliga. O botão GATE é SPST **NA** (fecha *só* enquanto aperta). As chaves **OSC A** e **OSC B** são SPST **ON–OFF** (MTS-101): ficam no que você deixou.
- **SPDT ON–ON** (MTS-102): um circuito, duas casas, **sem meio morto**. H1–H3, STACK, DRONE/GATE.
- **SPDT ON–OFF–ON** (MTS-103): três casas, centro **não liga ninguém**. **TREM**: tremolo / *off* / flutter. **LFO MODE**: pitch / *nada* / time.

**No VOZ-9 a diferença que importa:** LFO MODE escolhe *para onde* o DEPTH vai. TREM escolhe *quão rápido* (ou **off** no meio). Independentes.

DRONE/GATE, STACK e LFO MODE são chaves novas (`bom.md`).

**Datasheet.** [Dailywell MTS](https://www.dailywell.com.tw/upload/web/product/MTS-series.pdf)

**Banco.** Continuity no multímetro, chave no ar, *antes* de soldar. ON–ON nunca “abre” no meio. ON–OFF–ON abre.

---

## Conectores

### Combo XLR + P10 clone

**Ideia.** Um furo, **dois** circuitos. XLR = três pinos de microfone. P10 = guitarra. No Neutrik de verdade, um plug costuma desligar o outro. No **clone**, meça: não acredite no marketing.

Pinos XLR, do ponto de vista do cabo:

1. malha / massa da caixa  
2. quente (o som “para a frente”)  
3. frio (o som invertido — o 5532 subtrai 3 de 2)

Os dois combos são **fêmea**. Cabo de SM58 entra no IN. A mesa também é fêmea: no OUT use P10, ou um cabo macho–macho curto.

| | XLR | P10 |
| --- | --- | --- |
| IN | voz → 5532 | guitarra → AMOUNT |
| OUT | mesa, nível de mic (pad) | amp / interface, nível de pedal |

**Phantom 48 V** (luz na mesa, mics condensadores) **não** entra neste IN. Condensador = phantom *inline antes* da caixa, ou outro pré.

**Banco.** Ohmímetro: XLR 1 ↔ terra da placa. P10 sleeve ↔ terra. Tip do IN **não** pode achar os pinos 2/3 do XLR (são caminhos separados).

**Referência de pino (não é o clone).** [Neutrik NCJ6FA-H](https://www.neutrik.com/en/product/ncj6fa-h). Furo: **mede** o teu, ~24 mm.

---

### Jack P2 3,5 mm chaveado

**Ideia.** Ponta = sinal. Anel e sleeve = GND neste instrumento (CV 0–9 V, sem stereo de verdade). O **shunt** (chave interna) está fechado *sem* cabo e abre quando o plug entra.

Só dois jacks usam isso de propósito:

- **FILT** — sem cabo, o SHAPE vai ao filtro. Com cabo, o SHAPE some e entra o que você plugou.
- **RCV** — sem cabo, o pré vai à fita. Com cabo, entra o loop.

Os outros P2 são só “ponha ou tire um fio”.

**Banco.** Sem cabo: FILT tip deve achar a saída do SHAPE. Com um cabo (mesmo sem nada na outra ponta): essa ligação **abre**.

---

### CLK — relógio de fora, sem MIDI na caixa

**Ideia.** Dois mundos diferentes, um jack só para o mais simples.

Um **clock analógico** é um pulso de tensão: 0 V, depois 5 V (ou 9 V), de novo 0 V, no andamento da música. Volca, Pocket Operator, Eurorack e o *sync out* de um Beatstep falam isso. O VOZ-9 só precisa de um diodo e um cap: cada pulso enche o cap; pulsos mais seguidos = tensão média maior = os pinos 6 da fita se mexem. O **TIME** continua no painel. CLK empurra, não substitui.

**MIDI clock** é outro idioma: um fio de corrente, 31 250 bits por segundo, 24 avisos por semínima. Não é 0–5 V. Ligar um cabo MIDI no CLK **não funciona** e pode ser má ideia para o outro aparelho. O caminho simples: MIDI → caixinha “MIDI clock to analog sync” (Korg, Arturia, ou um conversor barato) → P2 no CLK.

Não há chip extra: o detector mora na BASE e entra no **mesmo nó do ECV**. A ponta do jack CLK chega por cabo.

**O que não é.** Não trava o eco numa colcheia. Não é tap-tempo. É “o relógio de fora puxa o capstan”. Mais BPM, em geral, eco um pouco mais curto.

**Banco.** TIME no meio, H1 on. Sem CLK: slap fixo. Plugue um LFO quadrado lento no CLK: o slap deve “respirar”. Sem movimento = diodo invertido ou cap invertido.

Esquema: `esquema.md` §8.

---

### P4 — 9 V centro-negativo

Padrão Boss: o pino do *meio* do plug é o negativo (GND da fonte). A manga é o +9 V. No jack da placa, o terminal do centro vai ao GND *depois* que você entende o desenho — **confira no P4**, não no chute.

No painel o P4 fica no **centro horizontal** (x=110), à direita do LED; combo IN no canto superior esquerdo. TIP e GND saem no **J6** (pinos 3–4). O 1N5817 solda **na placa**, no pino TIP.

Invertido: o 1N5817 segura. O LED não acende.

---

### Chicotes 2×N (fêmea na placa)

**Ideia.** Housing 2,54 mm, **dupla fila**, no tamanho do grupo. **J1 OSC 2×10, J2 LFO 2×6, J3 DELAY 2×10, J4 PATCH A 2×10, J5 PATCH B 2×8, J6 CTRL 2×3, J7 IN+PRE+OSC IN 2×6, J8 OUT 2×3, J9 EQ 424 2×6** — nove chicotes.

Na BASE solda a **fêmea**. Do painel sai o **macho**. Pino 1 = pad quadrado. Não cruze os grupos.

CIs (U1–U4, U6–U8, **U9**) entram em **soquete DIP**. Ferro no soquete, nunca no chip.

Pinagem: `pcb.md`.

**Banco.** Fonte **desligada**: J6 pino 4 (P4-GND) ↔ malha do combo. Contínuo. J6 pino 3 (P4-TIP) **não** pode achar GND.

---

## Passivos — o que não é “só um R”

### Resistores que merecem nome

- **2k2 + 22k 1 %** — ganho ×10 do mic. Trocar um só dos 22 k por 20 k “qualquer” piora o CMRR (o cabo vira antena).
- **220 Ω** (dois) — pad do XLR OUT e a mesma Z no pino 3 (quase-balanceado: o mixer vê os dois fios iguais e cancela um pouco de ruído).
- **4k7 do LED**, **10 k** de mix, **220 k** de decay: lista em `bom.md`.

Código de 4 faixas: vermelho-vermelho-preto-marrom = 2,2 kΩ (5 faixas: o “preto” extra é o multiplicador ×1).

### Capacitores por valor

| Valor | Tipo | Papel para lembrar |
| --- | --- | --- |
| 100 p | cerâmico C0G se houver | desvia RF de rádio no XLR, colado no combo |
| 3,3 n | filme | 50 µs do NAB (`R × C ≈ 50 µs` com ~15 k) |
| 10 n | filme | filtro do PT2399 e do laço (~1,6 kHz com 10 k) |
| 100 n | cerâmico/filme | acoplo, OSC A, VCC dos chips |
| 220 n | filme | dois no LFO + um no VCF |
| 10 µ / **25 V** | eletrolítico | XLR, voo do MAX1044, V5 |
| 47 µ / 16 V | eletrolítico | flutter, envelope, saídas H2/H3, fonte |

25 V no XLR: phantom ainda mata o 5532, mas 16 V estoura *antes*.

### Fenolite

Papel + resina + uma face de cobre. Barata, fura com furadeira de mão. Não é FR4: molha, racha se torcer, ruim em RF de rádio — por isso os 100 p ficam *no conector*, não no meio da placa.

Cobre = verso. Sem furo metalizado: quando uma trilha precisa “mudar de lado”, é um **jumper** de fio no lado dos componentes.

---

## Mapa — “quero este som, que peça é?”

| Quero… | Mexe em |
| --- | --- |
| Os dois tons se encontrarem | OSC A/B, AMOUNT, op-amp dos osciladores |
| Calar um oscilador | chave ON–OFF ao lado do pot A ou B |
| Quadrado mais “humano” | SHAPE + MP20 #1 |
| Abrir / fechar o brilho | CUTOFF + J201 #4 |
| Nota com cauda / drone | DRONE/GATE, GATE, J201 #5, 1N4148 |
| Mix osc ↔ mic | **OSC IN** |
| Oscs com a fala (sem DRONE) | PRE → follower → ENV, chave em GATE |
| Timbre voz+oscs (sem mesa) | EQ 424 pós-mix; SEND pré-EQ |
| Vento no fundo | J201 #3 (AMOUNT num extremo) |
| Vibrato | TREM em tremolo + MODE em pitch |
| LFO desligado | TREM no **meio** |
| Fita cambaleando | FLUTTER + LFO MODE em time |
| Tremolo de volume | TREM em tremolo + MODE no centro + LFO → VCV |
| Slap / Space Echo / caverna | H1–H3, STACK, TIME |
| Tempo de outro synth / MIDI* | jack **CLK** (+ conversor se for MIDI) |
| Repeats até oscilar | F-BACK + trim + MP20 #2 |
| Seco ↔ molhado | WET |
| Voz no SM58 | combo IN XLR, NE5532, PRE, sem phantom |
| Nível da voz | PRE (não o VOLUME) |
| Eco com “ar” de gravador | TL072 + 3,3 n |
| Só 5 V / só −9 V / não explodir | 78M05 / MAX1044 / 1N5817 |

---

## Peças sem datasheet de verdade

| Peça | O que fazer |
| --- | --- |
| Combo clone | Medir pinos; Neutrik só como mapa |
| MP20 pintado | Folha soviética; tratar como AC128 |
| Knob, caixa, cabo P2 | Mecânica |

---

## Exercícios (autodidata, sem montar o instrumento inteiro)

Faça no papel ou na proto, 20 minutos cada.

1. **Divisor.** 10 k + 10 k em 9 V. Quanto no meio? (4,5 V.) Troque um por 22 k. Recalcule. Esse é o 4V5 e o 1V8.
2. **τ = R C.** 100 k × 100 nF = 0,01 s. É a ordem do OSC A no grave. 100 k × 47 µF ≈ 4,7 s — por isso o flutter é lento e o envelope do GATE dura ~1 s com 220 k (não 100 k).
3. **Ganho.** 22 k / 2k2 = 10. 20 × log10(10) = 20 dB. Some os dois andares do 5532: ~41 dB. 3 mV × 110 ≈ 330 mV.
4. **Pad.** 220 / (10 k+220) ≈ 0,021. 1 V no VOLUME vira ~21 mV no XLR. É “nível de mic”.
5. **Pino 6.** Datasheet do PT2399, tabela R vs delay. Ache a linha ~2 k e a ~50 k. Compare com H1 e H3.
6. **Clock ≠ MIDI.** Um pulso 0–5 V, 2 vezes por segundo, enche um 4µ7 através de um diodo. Sem pulso, o 220 k esvazia o cap. Desenhe as duas etapas. MIDI clock (24 PPQN a 120 BPM) *não* é essa forma de onda — por isso existe a caixinha no meio.

---

## Ordem de leitura na bancada

1. Este arquivo, fundamentos + a peça do dia  
2. `esquema.md` do **mesmo** bloco  
3. Solda / proto  
4. **Banco** da peça (acima)  
5. Só então o próximo bloco  

Montar tudo e “ver no que dá” ensina menos do que um oscilador que você *entendeu* por que apita.
