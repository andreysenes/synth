# VOZ-9 — requisitos da placa BASE no KiCad

Baseline inicial: **R0.1 — decisões de produto registradas**

Escopo: placa BASE, interfaces com painel, fabricação, montagem e validação.

Processo de layout: `kicad-layout-agent.md`.

Este documento deve ser aprovado antes do gate G0. Ele define **o que** a placa
precisa cumprir; o playbook define **como** o agente organiza, roteia e verifica.
Texto gerado pelo agente não aprova requisito: a decisão final é humana.

## 1. Estados e prioridades

| Campo | Valores |
| --- | --- |
| Prioridade | `MUST` obrigatório · `SHOULD` desejável · `MAY` opcional |
| Estado | `PROPOSTO` · `APROVADO` · `BLOQUEADO` · `ADIADO` · `FALHOU` · `VERIFICADO` |
| Verificação | inspeção · ERC/DRC · cálculo · simulação · medição · teste funcional |

Regras:

- Todo `MUST` precisa de critério objetivo e evidência reproduzível.
- `VERIFICADO` significa que a evidência existe e foi revisada; não significa
  apenas que o agente declarou sucesso.
- Alteração de requisito aprovado muda a revisão do baseline e exige regressão
  dos itens afetados.
- Exceção exige requisito, risco, compensação, responsável e aprovação humana.
- Em conflito, prevalecem: segurança/datasheet → requisito aprovado → capacidade
  de fabricação → preferência de layout.

## 2. Premissas do baseline R0

Estas premissas foram escolhidas pelo responsável do produto:

1. faceplate quadrada de **300 × 300 mm** em alumínio de **1,5–2,0 mm**
   (espessura nominal provisória **2,00 mm**), montada numa caixa maior de
   paredes **15–18 mm** e envelope externo provisório **336,00 × 336,00 mm**
   (parede nominal 18 mm; faixa aceitável 330–336 mm conforme a madeira);
   PCB BASE de **200,00 × 150,00 mm** no fundo; altura interna provisória da
   caixa de **60,00 mm**;
2. FR-4 de duas camadas, 1,6 mm, cobre 1 oz, HASL sem chumbo, máscara verde e
   silk branca;
3. fabricação e PCBA pela JLCPCB;
4. montagem híbrida: SMD/LCSC montado pela JLCPCB e peças indisponíveis
   montadas manualmente;
5. painel separado, com knobs, botões, VU, jacks e demais interfaces ligados à
   BASE por chicotes;
6. alimentação externa regulada **9 V ±5 %, centro-negativo, mínimo 1 A**;
7. criar primeiro projeto e esquema KiCad; iniciar PCB somente após validação
   humana do esquema e da netlist;
8. selecionar modelos exatos para montagem manual, priorizando peças
   disponíveis no AliExpress com datasheet ou medidas verificáveis;
9. `esquema.md` define a intenção elétrica, mas ainda precisa virar um esquema
   KiCad validado;
10. `pcb.svg` é referência visual/mecânica legada, nunca fonte de conectividade.
11. funções do teste digital são classificadas em
    `sim/auditoria-requisitos.md`; instrumentos de depuração não viram hardware.

## 3. Requisitos funcionais e de conectividade

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| FUN-001 | MUST | Implementar a conectividade completa do esquema aprovado, sem nets omitidas ou adicionadas. | `esquema.md` | ERC, comparação de netlist e revisão humana | PROPOSTO |
| FUN-002 | MUST | Preservar a cadeia normalizada PRE/mix → EQ → SHAPE → VCF → VCA → NAB/delay → WET/VOLUME → OUT. | `README.md`, `esquema.md` | inspeção de esquema e teste funcional | PROPOSTO |
| FUN-003 | MUST | Preservar as funções dos três PT2399, H1–H3, STACK, TIME, ECV/CLK, WET e F-BACK. | `esquema.md` §8 | ERC e teste funcional por head | PROPOSTO |
| FUN-004 | MUST | Preservar OSC A/B, noise, FM, LFO, VCF, VCA, DRONE/GATE e envelope da fala. | `esquema.md` §§1–7 | ERC e testes por bloco | PROPOSTO |
| FUN-005 | MUST | FILT e RCV devem manter os contatos normalizados previstos; inserir plug deve abrir apenas o caminho especificado. | `componentes.md`, `esquema.md` | continuidade com/sem plug | PROPOSTO |
| FUN-006 | MUST | Nenhuma conectividade pode ser inferida do SVG, proximidade física ou texto quando divergir da netlist KiCad aprovada. | `pcb.md` | auditoria G0 | PROPOSTO |
| FUN-007 | MUST | Todas as funções DIG-001–DIG-019 classificadas como produto em `sim/auditoria-requisitos.md` devem ser rastreadas para esquema, teste e hardware. | auditoria digital | matriz de cobertura | APROVADO |
| FUN-008 | MUST | WAV/USB, solo de entrada, transporte, scope, telemetria, export SPICE, stereo Web Audio e limiter digital são instrumentos de teste, não funções da placa. | auditoria digital §3 | revisão de escopo | APROVADO |
| FUN-009 | MUST | Função documentada mas incompleta na simulação — incluindo IN→AMOUNT, SEND/RCV, CVs externos, CLK e saídas físicas — deve seguir o esquema aprovado, não a aproximação Web Audio. | auditoria digital §4 | esquema e testes dedicados | APROVADO |

## 4. Requisitos elétricos e de alimentação

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| PWR-001 | MUST | Entrada regulada de 9 V ±5 %, centro-negativo, por fonte com capacidade mínima de 1 A; polaridade conferida na peça física. | decisão DEC-009, `esquema.md` §0 | inspeção e medição | APROVADO |
| PWR-002 | MUST | D1/1N5817 deve bloquear alimentação invertida e alimentar toda a placa antes das derivações. | `esquema.md` §0 | ERC, inspeção e teste limitado | PROPOSTO |
| PWR-003 | MUST | V5 deve medir **5,0 V ±0,2 V** em operação; nenhum PT2399 pode receber V9. | `componentes.md` §78M05/PT2399 | ERC e medição sob carga | PROPOSTO |
| PWR-004 | MUST | VEE deve ficar aproximadamente entre **−8 e −9 V** com entrada nominal e carga normal. | `componentes.md` §MAX1044 | medição | PROPOSTO |
| PWR-005 | MUST | 4V5 deve acompanhar aproximadamente metade de V9; alvo inicial **4,2–4,8 V**. | `esquema.md` §0 | cálculo e medição | PROPOSTO |
| PWR-006 | MUST | 1V8 deve permanecer na faixa funcional inicial **1,6–2,0 V**. | `esquema.md` §5 | cálculo e medição | PROPOSTO |
| PWR-007 | MUST | 4V5 e 1V8 são referências/bias, não GND; é proibido uni-las ao plano GND. | `esquema.md`, playbook | ERC e inspeção | PROPOSTO |
| PWR-008 | MUST | Cada CI deve possuir desacoplamento local conforme esquema/datasheet; 100 nF deve ficar com caminho curto, meta de corpo a até 5 mm do pino. | playbook §6 | inspeção e medição no PCB | PROPOSTO |
| PWR-009 | MUST | Cada PT2399 deve possuir 100 nF e reserva local em V5; retorno pulsante não pode compartilhar garganta estreita com o pré. | datasheet/PT2399, playbook | inspeção de layout | PROPOSTO |
| PWR-010 | MUST | MAX1044 e capacitores de voo devem formar laço compacto, afastado do pré de mic e nós de alta impedância. | datasheet, playbook | inspeção de layout | PROPOSTO |
| PWR-011 | MUST | Corrente e potência térmica de D1, U4, U5, trilhas e vias devem suportar ao menos 2× a carga máxima calculada, em ambiente de 40 °C. | decisão DEC-006, datasheets | pior caso e teste térmico | APROVADO |
| PWR-012 | SHOULD | Incluir testpoints identificados para GND, V9, V5, VEE, 4V5 e 1V8. | playbook §10 | inspeção | PROPOSTO |

## 4.1 Requisitos de desempenho de áudio

Medir com osciladores e gerador de noise desligados, níveis nominais definidos
no plano de teste e largura de banda registrada.

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| AUD-001 | MUST | Caminho dry deve apresentar SNR ≥60 dB. | decisão DEC-007 | interface de áudio 24-bit/96 kHz ou melhor | APROVADO |
| AUD-002 | MUST | Caminho wet deve apresentar SNR ≥45 dB. | decisão DEC-007 | interface de áudio 24-bit/96 kHz ou melhor | APROVADO |
| AUD-003 | MUST | Hum de rede deve permanecer ≤−60 dBV na saída, nas condições nominais documentadas. | decisão DEC-007 | FFT/captura de áudio | APROVADO |
| AUD-004 | MUST | Crosstalk entre fontes/blocos isoláveis deve permanecer ≤−50 dB a 1 kHz. | decisão DEC-007 | injeção e medição por canal | APROVADO |
| AUD-005 | MUST | Limites de amplitude, frequência e tensão por testpoint devem vir de análise de tolerância dos componentes exatos, não de uma porcentagem arbitrária. | decisão DEC-008 | pior caso/Monte Carlo e correlação de protótipo | APROVADO |

## 4.2 Requisitos do VU físico

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| VU-001 | MUST | Incluir medidor físico de nível da saída mono. | decisão do produto, `sim/auditoria-requisitos.md` | esquema, PCB e teste | APROVADO |
| VU-002 | MUST | O tap deve medir o sinal pós-VOLUME e antes dos pads/saídas, equivalente ao ponto funcional do medidor digital sem copiar seu limiter. | auditoria digital §5 | inspeção de net e injeção de sinal | APROVADO |
| VU-003 | MUST | A entrada do VU deve ter impedância ≥100 kΩ e sua desconexão/falha não pode interromper ou degradar a saída. | boa prática de áudio | cálculo e teste A/B | APROVADO |
| VU-004 | MUST | Usar VU analógico de ponteiro, com escala VU e zona visual de sobrecarga; referência de 0 VU e balística ainda serão definidas. | decisão do produto, ACT-007 | calibração e teste dinâmico | APROVADO |
| VU-005 | MUST | Driver/retificador deve ficar na BASE, desacoplado e afastado do pré; retorno do mostrador não deve compartilhar garganta com MIC_LOW. | playbook, auditoria digital | revisão de placement/retorno | APROVADO |
| VU-006 | MUST | O mostrador analógico deve ficar no painel e usar um novo J10 dedicado; pinagem final deve contemplar movimento e eventual iluminação sem usar retorno sensível. | decisão do produto | esquema, pinout e continuidade | APROVADO |
| VU-007 | MUST | Prever ajuste de calibração acessível sem desmontar componentes críticos. | boa prática de medição | inspeção e calibração | APROVADO |
| VU-008 | MUST | Consumo, chaveamento de LEDs ou iluminação do VU devem entrar no orçamento de corrente e no pior caso térmico. | PWR-011 | cálculo e teste | APROVADO |
| VU-009 | MUST | Usar VU analógico genérico tipo AliExpress, dimensões nominais de 37 × 35 × 35 mm, frente preta e escala −20…+5 VU. | decisão do produto/listagem | amostra, medidas e impressão 1:1 | APROVADO |
| VU-010 | MUST | O movimento deve ser de 500 µA com resistência DC nominal de 630 Ω; fundo de escala elétrico calculado ≈0,315 V DC. | especificação da listagem | medição da amostra e calibração | APROVADO |
| VU-011 | MUST | A iluminação quente por filamento deve ficar sempre ligada com o equipamento, alimentada por V9 protegido através de `L+`/`L−` em J10, sem chave dedicada. | decisão DEC-022 | esquema e teste funcional | APROVADO |
| VU-012 | MUST | J10 deve fornecer quatro circuitos identificados: movimento `M+`/`M−` e iluminação `L+`/`L−`, sem usar retorno de áudio como condutor de potência. | arquitetura VU | esquema, pinout e continuidade | APROVADO |
| VU-013 | MUST | O driver deve limitar/proteger o movimento de 500 µA e oferecer trim de calibração; sobrecarga de entrada não pode bater o ponteiro continuamente no fim de escala. | boa prática de instrumento | cálculo, simulação e teste | APROVADO |
| VU-014 | MUST | Corpo, profundidade, furos, recorte e corrente real da lâmpada devem ser medidos numa amostra antes do painel final; a tolerância anunciada de 1–2 cm é inadequada e contradiz outra listagem. | listagens sem desenho técnico | paquímetro e mockup 1:1 | BLOQUEADO |
| VU-015 | MUST | O medidor pesa nominalmente 21 g e é frágil: painel, fixação e embalagem devem impedir esforço no corpo, terminais, ponteiro e lente; chicote precisa de alívio de tração. | manual/listagem do produto | inspeção mecânica e transporte | APROVADO |
| VU-016 | MUST | Manter seco; operação e armazenamento seguem DEC-010, sem umidade ou condensação. | manual do produto | revisão ambiental | APROVADO |
| VU-017 | MUST | Comissionamento deve verificar alimentação da luz entre 6–12 V, aplicar nível de áudio conhecido, ajustar calibração e observar estabilidade/repetibilidade. | manual do produto | procedimento de bancada | APROVADO |
| VU-018 | MUST | A instrução genérica “conectar ao equipamento de áudio” não autoriza ligação direta do movimento; o sinal deve passar pelo driver/retificador protegido da BASE. | análise de engenharia | esquema e teste de sobrecarga | APROVADO |
| VU-019 | MUST | Alegações comerciais de precisão, estabilidade e durabilidade não contam como evidência sem classe de exatidão, tolerâncias ou ensaio; cada lote deve ser calibrado/verificado. | análise das listagens | medição de amostra/lote | APROVADO |
| VU-020 | MUST | Corrente nominal, inrush e temperatura do filamento em 9 V devem ser medidos e incluídos em PWR-011; prever opção de resistor/limitador sem comprometer legibilidade. | especificação incompleta | medição e teste térmico | BLOQUEADO |
| VU-021 | MUST | Calibrar **0 VU = 0 dBV = 1,000 Vrms** no nó mono pós-VOLUME/pré-pads. | decisão DEC-023 | seno de 1 kHz, multímetro/interface e trim | APROVADO |
| VU-022 | MUST | A escala nominal implica aproximadamente −20 VU = 0,100 Vrms e +5 VU = 1,778 Vrms; confirmar linearidade real da amostra. | cálculo a partir de VU-021 | varredura de nível | APROVADO |
| VU-023 | MUST | Usar balística clássica de VU, alvo aproximado de 300 ms, sem peak-hold no ponteiro; o LED CLIP trata picos rápidos. | decisão DEC-024 | burst de 1 kHz e filmagem/medição | APROVADO |

## 4.3 Requisitos dos LEDs indicadores

O painel terá 10 LEDs no total: POWER existente e nove novos indicadores.

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| LED-001 | MUST | Incluir POWER, CLIP, GATE/ENV, LFO, OSC A, OSC B, H1, H2, H3 e STACK. | decisão DEC-015 | esquema, painel e teste | APROVADO |
| LED-002 | MUST | POWER continua indicando presença de V9 após proteção de polaridade. | esquema existente | medição e teste | APROVADO |
| LED-003 | MUST | CLIP deve usar o detector da saída, acender 1 dB antes do clipping real medido e reter por aproximadamente 150 ms, sem inserir limiter no áudio. | decisão DEC-025 | sweep de nível/carga e teste de pulso | APROVADO |
| LED-004 | MUST | O brilho de GATE/ENV deve acompanhar continuamente o envelope efetivo do VCA, incluindo ataque e decay, e não apenas a posição da chave. | decisão DEC-026 | injeção, gate, fala e captura óptica | APROVADO |
| LED-005 | MUST | LFO deve piscar de forma binária conforme os ciclos efetivos e permanecer apagado quando TREM estiver no centro/OFF. | decisão DEC-027 | teste nas duas faixas e OFF | APROVADO |
| LED-006 | MUST | OSC A/B, H1–H3 e STACK devem refletir a posição funcional de suas chaves. | decisão DEC-015 | teste de cada chave | APROVADO |
| LED-007 | MUST | Indicadores de chaves que comutam áudio devem usar segundo polo eletricamente isolado ou driver de alta impedância; LED/resistor não pode carregar o caminho de áudio. | boa prática de áudio | esquema e teste A/B | APROVADO |
| LED-008 | MUST | Corrente alvo deve ser baixa, inicialmente 1–2 mA por LED, recalculada para cor/peça escolhida e incluída no orçamento PWR-011. | margem térmica/ruído | cálculo e medição | APROVADO |
| LED-009 | MUST | Alimentação/retorno dos indicadores deve usar caminho dedicado até a distribuição de potência, sem compartilhar garganta com MIC_LOW, referências ou retornos do PT2399. | playbook | inspeção de retorno e ruído | APROVADO |
| LED-010 | MUST | Os nove indicadores novos devem usar chicote de status dedicado J11; POWER pode permanecer em J6. Pinagem final depende do circuito e dos polos das chaves. | arquitetura do painel | pinout e continuidade | APROVADO |
| LED-011 | MUST | Todos os 10 LEDs indicadores devem ser vermelhos; a iluminação integrada do VU, se existir, é tratada separadamente. | decisão DEC-016 | BOM e inspeção visual | APROVADO |
| LED-012 | MUST | Usar LEDs vermelhos difusos de 3 mm e baixo consumo, montados manualmente no painel. | decisão DEC-017 | amostras, datasheet e encaixe | APROVADO |
| LED-013 | MUST | Corrente nominal alvo deve ser 1,5 mA por LED; resistor inicial de 4,7 kΩ em V9 deve ser recalculado com Vf e queda do driver da peça exata. | decisão DEC-018 | cálculo e medição | APROVADO |
| LED-014 | MUST | OSC A/B devem usar DPST ON–OFF e H1–H3/STACK devem usar DPDT ON–ON; o segundo polo fica exclusivo para indicação, isolado do áudio. | decisão DEC-019 | esquema, continuidade e teste A/B | APROVADO |
| LED-015 | MUST | CLIP, GATE/ENV e LFO devem usar drivers com transistores discretos SMD, sem firmware e sem comparador integrado compartilhado. | decisão DEC-020 | esquema e teste | APROVADO |
| LED-016 | MUST | Transistor, polaridade, limiar, histerese/retenção e resistores exatos devem garantir alta impedância e ser aprovados antes do esquema final. | ACT-010 | cálculo, simulação e teste | BLOQUEADO |
| LED-017 | MUST | Definir clipping do estágio final pelo menor nível entre cargas/cantos aprovados que apresente compressão de ganho ≥1 dB ou THD+N ≥1 %; limiar CLIP fica 1 dB abaixo. | decisão DEC-025 | sweep a 1 kHz e análise de distorção | APROVADO |
| LED-018 | MUST | Driver GATE/ENV deve converter a faixa real de ENV em 0–1,5 mA de forma monotônica, apagar no repouso e apresentar impedância de entrada ≥1 MΩ. | decisão DEC-026 | sweep DC/transiente e medição de carga | APROVADO |
| LED-019 | MUST | Driver LFO deve usar limiar/histerese para comutação binária estável, carga de entrada ≥1 MΩ e corrente ON de 1,5 mA; em taxas altas pode parecer continuamente aceso. | decisão DEC-027 | sweep de frequência e osciloscópio | APROVADO |

## 5. Interfaces e conectores

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| IF-001 | MUST | J1 deve ser 2×10 OSC, J2 2×6 LFO, J3 2×10 DELAY, J4 2×10 PATCH A, J5 2×8 PATCH B, J6 2×3 CTRL, J7 2×6 IN/PRE, J8 2×3 OUT e J9 2×6 EQ424. | `pcb.md` | footprint/netlist/continuidade | PROPOSTO |
| IF-002 | MUST | A pinagem de J1–J9 deve corresponder integralmente às tabelas de `pcb.md`; NC deve permanecer sem conexão. | `pcb.md` §§J1–J9 | comparação pin a pin | PROPOSTO |
| IF-003 | MUST | Pino 1 deve ter pad quadrado, marca visível e orientação coerente em todos os headers. | `pcb.md` | inspeção 2D/1:1 | PROPOSTO |
| IF-004 | MUST | Fêmea fica na BASE, macho no painel, passo 2,54 mm, sem troca entre chicotes. | `pcb.md` | inspeção e encaixe físico | PROPOSTO |
| IF-005 | MUST | J6/P4-GND deve ter continuidade com a malha/sleeve dos jacks pelo chicote; P4-TIP não pode apresentar curto com GND. | `pcb.md` | ohmímetro antes de energizar | PROPOSTO |
| IF-006 | MUST | Entrada XLR não suporta phantom 48 V; aviso deve permanecer na documentação do produto. | `componentes.md` | revisão documental | PROPOSTO |
| IF-007 | MUST | Knobs, botões, jacks e demais interfaces de painel aprovadas devem ligar à BASE por chicotes; não fazem parte da PCBA SMD. | decisão do produto | esquema, pinout e inspeção | APROVADO |
| IF-008 | MUST | Cada peça de interface/manual deve ter fabricante/modelo ou desenho dimensional aprovado antes do footprint final. | decisões DEC-004/005 | datasheet, medidas e impressão 1:1 | APROVADO |
| IF-009 | MUST | O painel deve conter exatamente 17 pots: OSC A/B, AMOUNT, PRE, OSC IN, LOW, MID F, MID G, HIGH, RATE, DEPTH, SHAPE, CUTOFF, TIME, WET, F-BACK e VOLUME. | auditoria digital §2 | esquema, pinout e inspeção | APROVADO |
| IF-010 | MUST | O painel deve conter 9 alavancas: OSC A/B em DPST ON–OFF; H1/H2/H3/STACK em DPDT ON–ON; DRONE/GATE em SPDT ON–ON; TREM/MODE em SPDT ON–OFF–ON; além do botão GATE momentâneo. | auditoria digital §2, DEC-019 | esquema, pinout e inspeção | APROVADO |
| IF-011 | MUST | O painel deve conter os 11 jacks A, B, IN, FILT, FCV, VCV, LFO, ECV, CLK, SEND e RCV. | auditoria digital §2 | esquema, pinout e inspeção | APROVADO |
| IF-012 | MUST | COMBO IN/OUT, P4 e LED piloto continuam obrigatórios embora não estejam desenhados no SVG interno de `painel.html`. | auditoria digital §§2/6 | painel, esquema e inspeção | APROVADO |
| IF-013 | MUST | J1–J9 preservam as interfaces existentes; J10 será acrescentado exclusivamente para o VU analógico e sua iluminação opcional. | VU-006 | esquema, pinout e continuidade | APROVADO |
| IF-014 | MUST | J11 será dedicado aos nove LEDs novos e aos sinais/alimentação necessários; não misturar essas correntes em J7/J9 ou retornos de áudio. | LED-010 | esquema, pinout e continuidade | APROVADO |
| IF-015 | MUST | P4 (9 V) e os combos IN/OUT ficam no faceplate de alumínio, junto com pots, alavancas, patches, VU e LEDs; a caixa não recebe conectores de áudio/alimentação na traseira neste baseline. | decisão DEC-032 | desenho de painel e inspeção | APROVADO |
| IF-016 | MUST | O faceplate de alumínio fica ligado ao GND da BASE por **dois caminhos**: (1) contato condutivo das **porcas/bushings** dos jacks com a chapa; (2) **fio isolado dedicado** de bonding do alumínio a um ponto GND da BASE. Sleeves/malhas continuam pelos pinouts dos chicotes. | decisão DEC-033 | ohmímetro faceplate↔GND e continuidade sleeve→GND | APROVADO |

## 6. Requisitos mecânicos

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| MEC-001 | MUST | Contorno fechado da BASE de **200,00 × 150,00 mm** em `Edge.Cuts`. | decisão DEC-028 | medida no KiCad/DRC | APROVADO |
| MEC-002 | MUST | Quatro furos NPTH M3 de 3,20 mm nos centros `(4,4)`, `(196,4)`, `(4,146)`, `(196,146)` mm, origem no canto superior esquerdo da PCB. | decisão DEC-028 | medida no KiCad e impressão 1:1 | APROVADO |
| MEC-011 | MUST | Faceplate de **300,00 × 300,00 mm** em alumínio de **1,5–2,0 mm** (nominal provisório **2,00 mm**); a caixa de madeira é externa a ela e deve fixá-la e conter a BASE. | decisões DEC-028/031 | desenho mecânico e mockup | APROVADO |
| MEC-012 | MUST | Altura interna provisória da caixa de **60,00 mm**, dimensionada para ~35 mm de VU, peças altas da BASE e folga mínima de 5 mm; revisar após ACT-007 se a pilha medida ultrapassar o orçamento. | VU-014, DEC-029 | mockup 3D/físico e medição da amostra | APROVADO |
| MEC-013 | MUST | Paredes da caixa com **15–18 mm**; envelope externo provisório **336,00 × 336,00 mm** (parede nominal 18 mm), aceitando **330–336 mm** conforme a madeira escolhida; o faceplate de 300 × 300 mm encaixa no topo. | decisão DEC-030 | desenho mecânico e mockup | APROVADO |
| MEC-014 | MUST | O faceplate de alumínio deve ser rígido o bastante para porcas de pots/jacks sem flexão excessiva; bushings e comprimento de rosca devem ser escolhidos para a espessura final (1,5–2,0 mm). | decisão DEC-031 | inspeção mecânica e mockup | APROVADO |
| MEC-015 | MUST | Porcas/bushings dos jacks devem fazer contato elétrico confiável com o alumínio (arruela dentada/estrela ou equivalente limpo de óxido); prever olhal/parafuso para o fio isolado de bonding. | decisão DEC-033 | ohmímetro e inspeção 1:1 | APROVADO |
| MEC-016 | SHOULD | Acabamento superficial do faceplate (anodização, pintura ou cru) fica **adiado**; não bloqueia esquema nem PCB BASE; fecha antes do desenho final de painel/arte. | decisão DEC-034 | revisão de produto | ADIADO |
| MEC-003 | MUST | Manter cobre a 3,0 mm da borda dos furos M3, salvo aterramento deliberado aprovado. | playbook §2 | DRC/inspeção | PROPOSTO |
| MEC-004 | MUST | J1–J11 ficam na **borda inferior** da BASE (lado dos furos em y≈146 mm), com ao menos **10 mm** livres na direção de saída dos cabos. | decisão DEC-035 | medida/inspeção 3D | APROVADO |
| MEC-005 | MUST | Nenhum corpo/courtyard pode invadir borda, arruela, espaçador ou impedir remoção de CI em soquete. | playbook §3 | DRC, 3D e 1:1 | PROPOSTO |
| MEC-006 | MUST | Trimpots, testpoints e conectores devem ser acessíveis com a placa instalada. | `pcb.md`, playbook | inspeção mecânica | PROPOSTO |
| MEC-007 | MUST | Footprints devem ser validados com código LCSC, datasheet ou medidas da peça manual; “parecido” não aprova. | decisões DEC-004/005, playbook §10 | comparação dimensional e 1:1 | APROVADO |
| MEC-008 | SHOULD | CIs manuais devem compartilhar orientação de notch quando isso não prejudicar o layout elétrico. | playbook §3 | inspeção | PROPOSTO |
| MEC-009 | MUST | O painel deve receber recorte, fixação e área livre para o VU analógico exato, sem colisão com knobs, chicotes ou caixa. | VU-009 | CAD mecânico e impressão 1:1 | BLOQUEADO |
| MEC-010 | MUST | O painel deve acomodar os 10 LEDs, lentes e identificação legível sem conflito com VU, controles, porcas ou chicotes. | LED-001/011 | CAD mecânico e impressão 1:1 | BLOQUEADO |

## 7. Requisitos de placement

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| PLC-001 | MUST | Elementos mecânicos, headers e furos devem ser posicionados e bloqueados antes dos componentes elétricos. | playbook §4 | inspeção/histórico | PROPOSTO |
| PLC-002 | MUST | U1/J7 e pares diferenciais devem ficar no bloco de baixo ruído, afastados de U4, U2, LFO, CLK e PT2399. | playbook §§4–5 | inspeção e medidas | PROPOSTO |
| PLC-003 | MUST | R12/R13 e R57/R58 devem ficar agrupados e com geometria equivalente entre os dois caminhos do XLR. | playbook §5.2 | inspeção | PROPOSTO |
| PLC-004 | MUST | U4 e capacitores de voo devem ser compactos; U5 deve ficar próximo de U6–U8. | playbook §5.1 | inspeção | PROPOSTO |
| PLC-005 | MUST | U3/U6/U7/U8 devem seguir fisicamente GRAVA → H1 → H2 → H3 → LÊ, minimizando mix e retornos. | playbook §5.5 | inspeção/ratsnest | PROPOSTO |
| PLC-006 | MUST | Capacitores de tempo, feedback, filtros e desacoplamento devem ficar junto dos pinos que servem. | datasheets, playbook | checklist de datasheet | PROPOSTO |
| PLC-007 | MUST | ENV, gates JFET e outros nós de alta impedância devem permanecer curtos e afastados de sinais periódicos. | playbook §§5.3–5.4 | inspeção | PROPOSTO |
| PLC-008 | MUST | Placement crítico deve ser revisado por humano e bloqueado antes do roteamento. | playbook §11/G2 | registro de aprovação | PROPOSTO |
| PLC-009 | SHOULD | O fluxo físico deve ser reconhecível e manter blocos funcionais, sem compactação que piore isolamento ou manutenção. | playbook §§4 e 9 | revisão humana | PROPOSTO |
| PLC-010 | MUST | Driver e conector do VU devem ficar na zona de saída, afastados de U1/J7; retorno e alimentação não podem contaminar MIC_LOW. | VU-005 | revisão de layout | APROVADO |
| PLC-011 | MUST | Drivers de CLIP, GATE/ENV e LFO e J11 devem ficar junto de suas fontes/saída de painel, com retorno dedicado; não alongar nós analógicos de alta impedância. | LED-003–010 | revisão de layout | APROVADO |
| PLC-012 | MUST | Ao longo da borda inferior, J1–J11 devem ser ordenados pela **lógica do sinal** (blocos funcionais / cadeia de áudio), evitando cruzamento desnecessário de chicotes e mantendo pré/mic afastados de clock/PT2399/VU. | decisão DEC-035 | inspeção e revisão humana | APROVADO |

## 8. Requisitos de roteamento e terra

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| RTE-001 | MUST | Usar `F.Cu` e `B.Cu`; `B.Cu` deve preservar plano GND tão contínuo quanto possível e sinais não devem cruzar fendas de retorno. | decisão DEC-002, playbook §2 | DRC e inspeção de retorno | APROVADO |
| RTE-002 | MUST | Larguras mínimas: PWR_MAIN 1,00 mm; PWR_LOCAL 0,60 mm; sinais 0,25 mm. Usar valores maiores sempre que o espaço permitir. | perfil JLCPCB, playbook §7 | regras do KiCad/DRC | APROVADO |
| RTE-003 | MUST | Clearance mínimo geral 0,25 mm; MIC_LOW/TIME_CLOCK/CONTROL_HIZ 0,40 mm entre classes quando aplicável. | perfil JLCPCB, playbook §7 | regras do KiCad/DRC | APROVADO |
| RTE-004 | MUST | Cobre deve ficar a pelo menos 1,00 mm da borda da placa. | playbook §2 | DRC | PROPOSTO |
| RTE-005 | MUST | GND deve ser uma net única; não criar planos AGND/DGND isolados. | playbook §6 | ERC/inspeção de zonas | PROPOSTO |
| RTE-006 | MUST | Retorno do pré não pode compartilhar trecho estreito com PT2399, LED, regulador ou charge pump. | playbook §6 | inspeção de corrente de retorno | PROPOSTO |
| RTE-007 | MUST | X2/X3 devem ter geometria semelhante e ficar longe de sinais de clock; diferenças devem ser justificadas. | playbook §5.2 | inspeção/medição | PROPOSTO |
| RTE-008 | MUST | Entrada e saída de um mesmo estágio não devem correr paralelas; cruzamento inevitável deve ser curto. | playbook §5.2/§8 | inspeção | PROPOSTO |
| RTE-009 | MUST | Nets OSC timing, LFO, CLK e PT2399 pino 6 devem ser curtas e separadas de MIC_LOW; meta de 3 mm quando possível. | playbook §7 | inspeção/medição | PROPOSTO |
| RTE-010 | MUST | Zonas devem ter net explícita, thermal adequado a solda manual e zero ilha não conectada. | playbook §8 | DRC/inspeção | PROPOSTO |
| RTE-011 | MUST | Zero net não roteada no G5; qualquer jumper deliberado deve existir no esquema, BOM e PCB. | playbook G5 | DRC/ratsnest | PROPOSTO |
| RTE-012 | MUST | Incluir fio isolado dedicado de bonding do faceplate ao plano GND da BASE, além do contato pelas porcas; o retorno de áudio dos sleeves continua pelos pinouts J1–J11 e não deve depender só do chassi. | decisão DEC-033 | esquema, netlist, ohmímetro e inspeção | APROVADO |

## 9. Requisitos de fabricação, montagem e manutenção

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| DFM-001 | MUST | Fabricar na JLCPCB em FR-4, duas camadas, 1,6 mm, 1 oz, HASL sem chumbo, máscara verde e silk branca. | decisões DEC-002/003 | parâmetros do pedido e Gerbers | APROVADO |
| DFM-002 | MUST | Furos, anéis e slots devem seguir o datasheet da peça e as capacidades vigentes da JLCPCB, com impressão 1:1 para peças manuais. | decisão DEC-003, playbook | DRC, datasheet e 1:1 | APROVADO |
| DFM-003 | MUST | Silkscreen não pode invadir pads/furos e deve indicar refs, pin 1, polaridade, trilhos e lado de montagem. | playbook §10/G3 | DRC/inspeção | PROPOSTO |
| DFM-004 | MUST | Nenhum passivo deve ficar sob CI em soquete; eletrolítico não deve encostar no regulador quente. | playbook §9 | inspeção 3D | PROPOSTO |
| DFM-005 | MUST | Gerbers/drill ou arte de transferência devem ser verificados em visualizador independente e em impressão 1:1. | playbook G6 | revisão de arquivos | PROPOSTO |
| DFM-006 | MUST | BOM, designators, footprints e polaridades devem corresponder à revisão liberada. | `bom.md`, `jlcpcb.md` | comparação automatizada + humana | PROPOSTO |
| DFM-007 | SHOULD | Incluir testpoints de áudio para PRE/SEND, OSC A/B, ENV, VCF/VCA, GRAVA/LÊ e heads quando houver espaço seguro. | playbook §10 | inspeção | PROPOSTO |
| DFM-008 | MUST | Todo componente disponível e aprovado na biblioteca JLCPCB deve usar código LCSC e footprint compatível para PCBA SMD. | decisão DEC-004 | BOM/CPL e conferência no portal | APROVADO |
| DFM-009 | MUST | Componente sem opção LCSC aprovada deve usar footprint de montagem manual e aparecer separado na BOM. | decisão DEC-004 | BOM e inspeção | APROVADO |

## 10. Requisitos de verificação e qualidade

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| VER-001 | MUST | ERC deve ter zero erro bloqueante antes do placement. | playbook G0 | relatório ERC | PROPOSTO |
| VER-002 | MUST | DRC deve ter zero erro em G5/G6; todo warning deve ser resolvido ou possuir exceção aprovada. | playbook G5/G6 | relatório DRC | PROPOSTO |
| VER-003 | MUST | Cada requisito MUST deve apontar para evidência e responsável antes da liberação. | playbook §1 | matriz de rastreabilidade | PROPOSTO |
| VER-004 | MUST | Cálculo, simulação ou relatório produzido pelo agente deve ser revisado de forma independente. | playbook §10 | assinatura/evidência externa | PROPOSTO |
| VER-005 | MUST | Teste que falhar permanece FALHOU até correção/reteste ou waiver humano formal. | playbook §1 | histórico de teste | PROPOSTO |
| VER-006 | MUST | Mudança após teste aprovado exige regressão dos requisitos impactados. | playbook §10 | matriz de impacto/reteste | PROPOSTO |
| VER-007 | MUST | G2, G3 e G6 exigem aprovação humana registrada. | playbook §11 | registro de aprovação | PROPOSTO |
| VER-008 | MUST | G7 deve medir placa física; ligar ou produzir áudio não basta para `HARDWARE_VALIDADO`. | playbook G7 | relatório de bancada | PROPOSTO |
| VER-009 | MUST | A bancada mínima é multímetro, osciloscópio e interface de áudio; testes que precisarem de outro instrumento ficam bloqueados ou usam equipamento externo documentado. | decisão DEC-011 | inventário e plano de teste | APROVADO |
| VER-010 | MUST | O primeiro protótipo não exige ensaio EMC/ESD formal; ainda deve aplicar boas práticas de proteção/layout e testes funcionais. | decisão DEC-012 | revisão de projeto | APROVADO |
| VER-011 | MUST | Simulação só passa se não houver erro de solver, convergência, vetor ausente ou medida inválida; marcador `*_DONE` isolado não é evidência. | auditoria digital §4 | parser de log + revisão | APROVADO |

## 11. Requisitos para execução pelo agente/MCP

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| MCP-001 | MUST | MCP/KiCad deve ser a fonte de verdade; o agente deve ler estado antes e depois de cada mutação. | playbook §11 | log de sessão | PROPOSTO |
| MCP-002 | MUST | Cada lote pode alterar no máximo um bloco funcional e deve terminar com DRC e checkpoint coerente. | playbook §11 | log/checkpoint | PROPOSTO |
| MCP-003 | MUST | Item selecionado, bloqueado ou alterado pelo humano não pode ser movido pelo agente. | playbook §11 | log/diff | PROPOSTO |
| MCP-004 | MUST | Após proposta e uma revisão automática malsucedida, o placement crítico volta ao engenheiro. | playbook §11 | contagem de tentativas | PROPOSTO |
| MCP-005 | MUST | O agente não pode alterar circuito, valor, pinagem, footprint, contorno ou conector sem aprovação explícita. | `AGENTS.md` | diff/revisão | PROPOSTO |
| MCP-006 | MUST | Operação não suportada de forma segura pelo MCP deve bloquear o lote; edição textual do PCB exige autorização. | playbook §11 | log | PROPOSTO |
| MCP-007 | MUST | Cada sessão deve reportar refs, nets, DRC, ratsnest, requisitos, exceções, aprovações e próxima ação segura. | playbook §13 | relatório de sessão | PROPOSTO |

## 12. Requisitos de validação em hardware

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| HW-001 | MUST | Antes de inserir CIs, confirmar ausência de curto e medir V9, V5, VEE, 4V5 e 1V8. | `pcb.md`, playbook G7 | relatório de bancada | PROPOSTO |
| HW-002 | MUST | Testar blocos na ordem de `pcb.md`: fonte, osciladores, shape/VCF/VCA, LFO, pré/EQ, NAB e PT2399. | `pcb.md` | checklist de bancada | PROPOSTO |
| HW-003 | MUST | Verificar ruído, crosstalk, estabilidade, aquecimento e extremos dos controles. | playbook G7 | medições e teste auditivo documentado | PROPOSTO |
| HW-004 | MUST | Comparar hardware com requisitos/simulação e investigar toda discrepância relevante. | playbook G7 | relatório de correlação | PROPOSTO |
| HW-005 | SHOULD | Testar variação segura de alimentação e peças; operação deve ser validada entre 0–40 °C e armazenamento especificado entre −10–60 °C, em ambiente interno e seco. | decisão DEC-010, playbook G7 | plano de teste | APROVADO |

## 13. Decisões registradas e ações abertas

### Decisões do responsável do produto

| ID | Decisão | Estado |
| --- | --- | --- |
| DEC-001 | Criar projeto e esquema KiCad primeiro; PCB somente após validação. | RESOLVIDA |
| DEC-002 | FR-4 de duas camadas com PCBA JLCPCB. | RESOLVIDA |
| DEC-003 | Processo padrão: 1,6 mm, 1 oz, HASL sem chumbo, verde/branco. | RESOLVIDA |
| DEC-004 | SMD/LCSC via JLCPCB; restante com footprint manual validado. | RESOLVIDA |
| DEC-005 | Agente seleciona modelos manuais, priorizando AliExpress. | RESOLVIDA |
| DEC-006 | Margem de corrente 2× e ambiente máximo de projeto de 40 °C. | RESOLVIDA |
| DEC-007 | Dry 60 dB, wet 45 dB, hum −60 dBV, crosstalk −50 dB. | RESOLVIDA |
| DEC-008 | Limites derivados das tolerâncias dos componentes selecionados. | RESOLVIDA |
| DEC-009 | Fonte 9 V ±5 %, centro-negativo, mínimo 1 A. | RESOLVIDA |
| DEC-010 | Operação 0–40 °C; armazenamento −10–60 °C; interno/seco. | RESOLVIDA |
| DEC-011 | Bancada mínima: multímetro, osciloscópio e interface de áudio. | RESOLVIDA |
| DEC-012 | Protótipo sem ensaio EMC/ESD formal. | RESOLVIDA |
| DEC-013 | Incluir VU analógico de ponteiro no painel e circuito na BASE. | RESOLVIDA |
| DEC-014 | Usar VU compacto, com envelope inicial de até aproximadamente 45 × 35 mm. | RESOLVIDA |
| DEC-015 | Incluir opção C: POWER, CLIP, GATE/ENV, LFO, OSC A/B, H1–H3 e STACK. | RESOLVIDA |
| DEC-016 | Usar vermelho em todos os 10 LEDs indicadores. | RESOLVIDA |
| DEC-017 | Usar LED vermelho difuso de 3 mm e baixo consumo. | RESOLVIDA |
| DEC-018 | Usar corrente nominal alvo de 1,5 mA por LED. | RESOLVIDA |
| DEC-019 | Usar segundo polo isolado: DPST em OSC A/B e DPDT em H1–H3/STACK. | RESOLVIDA |
| DEC-020 | Usar transistores discretos para os indicadores CLIP, GATE/ENV e LFO. | RESOLVIDA |
| DEC-021 | Usar VU analógico nominal 37 × 35 × 35 mm, 500 µA/630 Ω, 21 g, com iluminação quente 6–12 V. | RESOLVIDA |
| DEC-022 | Manter a iluminação quente do VU sempre ligada enquanto o equipamento estiver ligado. | RESOLVIDA |
| DEC-023 | Calibrar 0 VU em 0 dBV, equivalente a 1,000 Vrms pós-VOLUME/pré-pads. | RESOLVIDA |
| DEC-024 | Usar balística clássica aproximada de 300 ms, sem peak-hold no ponteiro. | RESOLVIDA |
| DEC-025 | Acender CLIP 1 dB antes do clipping real medido, com retenção de 150 ms. | RESOLVIDA |
| DEC-026 | Fazer o brilho do LED GATE/ENV acompanhar continuamente ataque e decay do envelope. | RESOLVIDA |
| DEC-027 | Fazer o LED LFO piscar de forma binária e apagar com TREM no centro/OFF. | RESOLVIDA |
| DEC-028 | Faceplate 300 × 300 mm mais caixa; PCB BASE 200 × 150 mm. | RESOLVIDA |
| DEC-029 | Altura interna provisória da caixa de 60 mm. | RESOLVIDA |
| DEC-030 | Paredes 15–18 mm; envelope externo provisório 336 × 336 mm (faixa 330–336). | RESOLVIDA |
| DEC-031 | Faceplate de alumínio 1,5–2,0 mm (nominal provisório 2,00 mm). | RESOLVIDA |
| DEC-032 | P4 e combos IN/OUT no faceplate (sem conectores de áudio/alimentação na traseira). | RESOLVIDA |
| DEC-033 | Faceplate ligado ao GND pelas porcas/bushings e por fio isolado dedicado. | RESOLVIDA |
| DEC-034 | Acabamento do faceplate adiado para depois do baseline elétrico/mecânico. | ADIADA |
| DEC-035 | Headers J1–J11 na borda inferior da PCB, ordenados pela lógica do sinal. | RESOLVIDA |

### Ações técnicas bloqueantes

| ID | Ação/evidência necessária | Bloqueia | Responsável |
| --- | --- | --- | --- |
| ACT-001 | Criar `.kicad_pro` e `.kicad_sch`, anotar e validar ERC/netlist. Não criar PCB antes da aprovação. | G0 | engenharia |
| ACT-002 | Selecionar códigos LCSC e recalcular a BOM SMD conforme estoque/ciclo de vida. | esquema/PCBA | engenharia |
| ACT-003 | Selecionar modelos exatos das peças manuais e validar pinagem/dimensões. | footprint/G1 | engenharia + bancada |
| ACT-004 | Calcular consumo, dissipação e tolerâncias, verificando margem 2× a 40 °C. | esquema/G6 | engenharia |
| ACT-005 | Executar pior caso/Monte Carlo e gerar limites dos testpoints. | G6/G7 | engenharia |
| ACT-006 | Resolver conflitos da documentação legada THT/fenolite com o baseline híbrido. | R0 | documentação |
| ACT-007 | Comprar e medir uma amostra do VU selecionado: geometria, linearidade, balística real, corrente/inrush e temperatura da luz; confirmar se a pilha cabe na altura interna de 60 mm. | esquema/PCB/MEC-012 | engenharia |
| ACT-008 | Corrigir ou documentar as lacunas do teste digital listadas em `sim/auditoria-requisitos.md` antes de usá-lo como evidência. | esquema/G0 | engenharia |
| ACT-009 | Instalar versão registrada do ngspice, corrigir falsos positivos do runner e repetir toda a suíte sem erros. | evidência/G0 | engenharia |
| ACT-010 | Dimensionar transistores discretos, limiares/retenção e resistores sem carregar áudio; selecionar modelos exatos das chaves aprovadas. | esquema/painel/BOM | engenharia |

## 14. Gate R0 — aprovação de requisitos

Checklist de saída:

- [x] Escopo e perfil de fabricação aprovados.
- [x] Decisões DEC-001–DEC-035 registradas (DEC-034 adiada).
- [ ] Todos os requisitos `MUST` têm fonte, critério e método de verificação.
- [ ] Conflitos com `README.md`, `esquema.md`, `pcb.md`, BOM e datasheets foram
      resolvidos.
- [ ] Pendências classificadas por gate e responsável.
- [ ] Critérios de ruído, alimentação, temperatura e teste final definidos ou
      formalmente adiados para antes de G6.
- [ ] Revisão do baseline registrada no Git.
- [ ] Aprovação humana registrada abaixo.

```text
Baseline: R0.1
Revisão Git:
Perfil de fabricação: JLCPCB FR-4 2L, 1,6 mm, 1 oz, LF HASL, verde/branco
Aprovado por: decisões individuais registradas pelo responsável do produto
Data: 2026-09-28
Restrições/waivers:
Próximo gate autorizado: concluir R0; depois criar e validar somente o esquema
```

Sem essa aprovação, o próximo estado é `REQUISITOS_PENDENTES`, não G0.
