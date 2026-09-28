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
| Estado | `PROPOSTO` · `APROVADO` · `BLOQUEADO` · `FALHOU` · `VERIFICADO` |
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

1. uma única placa BASE de **220 × 160 mm**;
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

## 3. Requisitos funcionais e de conectividade

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| FUN-001 | MUST | Implementar a conectividade completa do esquema aprovado, sem nets omitidas ou adicionadas. | `esquema.md` | ERC, comparação de netlist e revisão humana | PROPOSTO |
| FUN-002 | MUST | Preservar a cadeia normalizada PRE/mix → EQ → SHAPE → VCF → VCA → NAB/delay → WET/VOLUME → OUT. | `README.md`, `esquema.md` | inspeção de esquema e teste funcional | PROPOSTO |
| FUN-003 | MUST | Preservar as funções dos três PT2399, H1–H3, STACK, TIME, ECV/CLK, WET e F-BACK. | `esquema.md` §8 | ERC e teste funcional por head | PROPOSTO |
| FUN-004 | MUST | Preservar OSC A/B, noise, FM, LFO, VCF, VCA, DRONE/GATE e envelope da fala. | `esquema.md` §§1–7 | ERC e testes por bloco | PROPOSTO |
| FUN-005 | MUST | FILT e RCV devem manter os contatos normalizados previstos; inserir plug deve abrir apenas o caminho especificado. | `componentes.md`, `esquema.md` | continuidade com/sem plug | PROPOSTO |
| FUN-006 | MUST | Nenhuma conectividade pode ser inferida do SVG, proximidade física ou texto quando divergir da netlist KiCad aprovada. | `pcb.md` | auditoria G0 | PROPOSTO |

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

## 5. Interfaces e conectores

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| IF-001 | MUST | J1 deve ser 2×10 OSC, J2 2×6 LFO, J3 2×10 DELAY, J4 2×10 PATCH A, J5 2×8 PATCH B, J6 2×3 CTRL, J7 2×6 IN/PRE, J8 2×3 OUT e J9 2×6 EQ424. | `pcb.md` | footprint/netlist/continuidade | PROPOSTO |
| IF-002 | MUST | A pinagem de J1–J9 deve corresponder integralmente às tabelas de `pcb.md`; NC deve permanecer sem conexão. | `pcb.md` §§J1–J9 | comparação pin a pin | PROPOSTO |
| IF-003 | MUST | Pino 1 deve ter pad quadrado, marca visível e orientação coerente em todos os headers. | `pcb.md` | inspeção 2D/1:1 | PROPOSTO |
| IF-004 | MUST | Fêmea fica na BASE, macho no painel, passo 2,54 mm, sem troca entre chicotes. | `pcb.md` | inspeção e encaixe físico | PROPOSTO |
| IF-005 | MUST | J6/P4-GND deve ter continuidade com malha; P4-TIP não pode apresentar curto com GND. | `pcb.md` | ohmímetro antes de energizar | PROPOSTO |
| IF-006 | MUST | Entrada XLR não suporta phantom 48 V; aviso deve permanecer na documentação do produto. | `componentes.md` | revisão documental | PROPOSTO |
| IF-007 | MUST | Knobs, botões, jacks e demais interfaces de painel aprovadas devem ligar à BASE por chicotes; não fazem parte da PCBA SMD. | decisão do produto | esquema, pinout e inspeção | APROVADO |
| IF-008 | MUST | Cada peça de interface/manual deve ter fabricante/modelo ou desenho dimensional aprovado antes do footprint final. | decisões DEC-004/005 | datasheet, medidas e impressão 1:1 | APROVADO |

## 6. Requisitos mecânicos

| ID | Pri. | Requisito e critério de aprovação | Fonte | Verificação | Estado |
| --- | --- | --- | --- | --- | --- |
| MEC-001 | MUST | Contorno fechado retangular de **220,00 × 160,00 mm** em `Edge.Cuts`. | `pcb.md` | medida no KiCad/DRC | PROPOSTO |
| MEC-002 | MUST | Quatro furos NPTH M3 de 3,20 mm nos centros `(4,4)`, `(216,4)`, `(4,156)`, `(216,156)` mm em relação ao canto superior esquerdo da placa. | `pcb.md` | medida no KiCad e impressão 1:1 | PROPOSTO |
| MEC-003 | MUST | Manter cobre a 3,0 mm da borda dos furos M3, salvo aterramento deliberado aprovado. | playbook §2 | DRC/inspeção | PROPOSTO |
| MEC-004 | MUST | J1–J9 devem permanecer acessíveis na faixa esquerda, com ao menos 10 mm livres na direção de saída dos cabos. | `pcb.md`, playbook §3 | medida/inspeção 3D | PROPOSTO |
| MEC-005 | MUST | Nenhum corpo/courtyard pode invadir borda, arruela, espaçador ou impedir remoção de CI em soquete. | playbook §3 | DRC, 3D e 1:1 | PROPOSTO |
| MEC-006 | MUST | Trimpots, testpoints e conectores devem ser acessíveis com a placa instalada. | `pcb.md`, playbook | inspeção mecânica | PROPOSTO |
| MEC-007 | MUST | Footprints devem ser validados com código LCSC, datasheet ou medidas da peça manual; “parecido” não aprova. | decisões DEC-004/005, playbook §10 | comparação dimensional e 1:1 | APROVADO |
| MEC-008 | SHOULD | CIs manuais devem compartilhar orientação de notch quando isso não prejudicar o layout elétrico. | playbook §3 | inspeção | PROPOSTO |

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

### Ações técnicas bloqueantes

| ID | Ação/evidência necessária | Bloqueia | Responsável |
| --- | --- | --- | --- |
| ACT-001 | Criar `.kicad_pro` e `.kicad_sch`, anotar e validar ERC/netlist. Não criar PCB antes da aprovação. | G0 | engenharia |
| ACT-002 | Selecionar códigos LCSC e recalcular a BOM SMD conforme estoque/ciclo de vida. | esquema/PCBA | engenharia |
| ACT-003 | Selecionar modelos exatos das peças manuais e validar pinagem/dimensões. | footprint/G1 | engenharia + bancada |
| ACT-004 | Calcular consumo, dissipação e tolerâncias, verificando margem 2× a 40 °C. | esquema/G6 | engenharia |
| ACT-005 | Executar pior caso/Monte Carlo e gerar limites dos testpoints. | G6/G7 | engenharia |
| ACT-006 | Resolver conflitos da documentação legada THT/fenolite com o baseline híbrido. | R0 | documentação |
| ACT-007 | Confirmar se “VU” significa adicionar um medidor ao painel ou foi apenas exemplo de interface. | escopo/esquema | responsável do produto |

## 14. Gate R0 — aprovação de requisitos

Checklist de saída:

- [x] Escopo e perfil de fabricação aprovados.
- [x] Decisões DEC-001–DEC-012 registradas.
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
