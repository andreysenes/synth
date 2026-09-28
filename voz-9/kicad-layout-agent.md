# VOZ-9 — plano de layout e roteamento no KiCad

Este documento é a especificação operacional para um agente organizar e rotear a
placa **BASE** do VOZ-9 no KiCad por MCP. Ele complementa `esquema.md` e
`pcb.md`; não substitui esquema elétrico, netlist, datasheets nem regras do
fabricante.

Os requisitos e critérios de aceite ficam em `kicad-requisitos.md`. O gate R0
desse documento deve ser aprovado antes do G0 deste playbook.

O objetivo é obter uma placa fabricável, silenciosa, reparável e coerente com o
fluxo do áudio. “Caber” não é critério suficiente. Toda decisão deve preservar:

1. conectividade elétrica;
2. integridade de alimentação e terra;
3. separação entre pré de microfone, osciladores/LFO/clock e PT2399;
4. acesso mecânico, montagem e manutenção;
5. regras de fabricação verificadas por DRC.

Conectividade completa, DRC limpo e aparência plausível são condições
necessárias, mas **não provam** que o layout está bom. O agente produz proposta
e evidências; a aprovação de engenharia continua humana. Simulação, ERC, DRC e
inspeção 3D verificam aspectos diferentes e nenhum substitui teste da placa
física.

## 1. Condição de entrada

O agente **não pode iniciar o placement** enquanto não existirem:

- baseline de requisitos R0 aprovado;
- projeto `.kicad_pro`, esquema `.kicad_sch` anotado e PCB `.kicad_pcb`;
- ERC sem erro bloqueante;
- footprints associados e validados contra a peça real;
- netlist atualizada no PCB pelo próprio KiCad;
- contorno `Edge.Cuts` fechado de **220 × 160 mm**;
- furos M3 em `(4,4)`, `(216,4)`, `(4,156)` e `(216,156)`, coordenadas em mm;
- J1–J9 com tipo, número de vias e pino 1 conforme `pcb.md`, J10 para o VU
  analógico e J11 para LEDs após definição dos componentes;
- perfil de fabricação escolhido na seção 2;
- datasheets disponíveis para pinagem e recomendações de layout.

Hoje, os SVGs e `_gen_pcb.py` são referências mecânicas/visuais, não uma
netlist. O agente nunca deve inferir conectividade pelas linhas do SVG, pela
proximidade dos desenhos ou pela descrição textual. Em caso de divergência:

1. parar o bloco afetado;
2. registrar refs, nets e documentos conflitantes;
3. pedir decisão humana;
4. não “corrigir” esquema ou pinagem durante o layout.

### Gate G0 — auditoria obrigatória

Antes de mover qualquer footprint, produzir e salvar:

- versão do KiCad e revisão Git;
- perfil de fabricação;
- dimensões da placa;
- lista de footprints sem courtyard, modelo ou datasheet;
- lista de nets sem classe;
- contagem de pads, vias e ratsnest;
- resultado inicial de ERC/DRC;
- divergências entre esquema, BOM e `pcb.md`;
- matriz de `kicad-requisitos.md` atualizada;
- checklist extraído dos datasheets para os blocos críticos.

Se um item crítico estiver ausente, o estado é `BLOQUEADO`, não “aprovado com
ressalvas”.

### Rastreabilidade requisito → evidência

Antes do placement, converter requisitos em uma matriz versionada:

| ID | Requisito | Origem | Método de verificação | Critério de aprovação | Responsável | Estado/evidência |
| --- | --- | --- | --- | --- | --- | --- |
| MEC-01 | placa 220 × 160 mm | `pcb.md` | medida no KiCad | valor exato | agente + humano | pendente |
| PWR-01 | PT2399 somente em V5 | esquema/datasheet | ERC + inspeção de net | nenhum pad em V9 | agente + humano | pendente |
| LAY-01 | pré afastado de clock/PT2399 | este documento | inspeção/medição | regras das seções 4–7 | humano | pendente |

Cada requisito deve apontar para uma evidência reproduzível: leitura do KiCad,
relatório ERC/DRC, captura, cálculo, datasheet, inspeção 1:1 ou medição em
hardware. “Parece certo” e texto gerado pelo próprio agente não são evidência.

Se um critério falhar:

1. manter o estado `FALHOU`;
2. investigar causa e impacto;
3. corrigir e repetir o teste; ou
4. abrir uma exceção formal com evidência, risco, compensação, responsável e
   aprovação humana.

O agente nunca transforma falha em aprovação manual por conveniência.

## 2. Perfil de fabricação

Escolher **um** perfil e não misturar regras.

### Perfil A — BASE legada, fenolite de uma face

É apenas a referência legada de `pcb.md`; não é o baseline do projeto KiCad.

- placa THT, cobre somente em `B.Cu`;
- componentes e jumpers no lado superior;
- sem vias metalizadas como solução de troca de camada;
- toda troca necessária vira jumper THT explícito, com referência;
- trilha mínima recomendada: **0,40 mm**;
- trilha de alimentação: **0,80 mm**;
- tronco principal de GND e entrada V9: **1,00 mm**;
- clearance cobre–cobre: **0,30 mm**;
- cobre à borda: **1,00 mm**;
- furo acabado típico de R/C/header: **0,80 mm**;
- soquetes DIP e terminais robustos: validar entre **0,90 e 1,00 mm**;
- anel anular mínimo: **0,30 mm**;
- furos M3 NPTH: **3,20 mm**, sem cobre num raio de **3,0 mm** da borda do
  furo, salvo arruela aterrada deliberadamente;
- cobre de texto ou logotipo não pode estreitar trilha nem criar ilhas.

Este perfil exige confirmação da capacidade real de transferência/furação. Se o
fabricante ou processo exigir valores maiores, prevalece o valor mais
conservador.

### Perfil B — FR-4 de duas camadas

É o baseline aprovado em `kicad-requisitos.md`.

- JLCPCB, FR-4, 1,6 mm, cobre 1 oz, HASL sem chumbo, máscara verde e silk
  branca;
- `F.Cu` e `B.Cu`;
- trilha mínima recomendada: **0,25 mm**, ainda que a fábrica aceite menos;
- alimentação: **0,60 mm** ou maior;
- clearance: **0,25 mm**;
- via padrão: **0,80/0,40 mm** (diâmetro/furo), validada na fábrica;
- plano GND contínuo, preferencialmente em `B.Cu`;
- sinais no plano oposto devem evitar fendas no retorno;
- montagem híbrida: SMD/LCSC por PCBA JLCPCB e componentes indisponíveis
  soldados manualmente;
- todo item montado pela JLCPCB exige código LCSC, footprint, BOM e CPL
  conferidos na prévia do portal;
- peças manuais exigem modelo exato e impressão 1:1 antes da liberação.

### Regra de precedência

As regras finais são o máximo entre:

1. limites elétricos e mecânicos deste documento;
2. recomendações do datasheet;
3. capacidades da fábrica/processo escolhido.

Para cada CI crítico, o agente deve transcrever as recomendações aplicáveis do
datasheet para um checklist com página/figura e demonstrar onde cada uma foi
atendida. Apenas escrever “seguir o datasheet” não é suficiente. Se a
recomendação não couber ou conflitar com outra regra, encaminhar para decisão
humana.

IPC-2221/2222 e IPC-7351 são referências de engenharia, não números a copiar
sem contexto. Para esta placa de baixa tensão, as margens acima priorizam
fabricação artesanal e reparabilidade.

## 3. Restrições mecânicas e de montagem

Travar antes do placement:

- `Edge.Cuts`, furos M3 e keepouts;
- J1–J9 e os novos J10/J11 na faixa de conectores, acessíveis aos chicotes de
  8–12 cm;
- pino 1 visível e coerente com `pcb.md`;
- margem para inserir/remover conectores e eventuais CIs em soquete;
- área para alicate, ponta de prova e chave nos trimpots;
- polaridade legível em eletrolíticos, diodos, regulador e CIs;
- orientação dos eventuais DIPs preferencialmente única, com notch para o mesmo
  lado;
- altura livre sob o painel e sob knobs/chaves.

Não colocar componentes:

- sob arruela, parafuso ou espaçador;
- entre um header e a direção de saída do chicote;
- a menos de **2,0 mm** da borda, salvo componente mecânico previsto;
- onde o corpo invada courtyard ou impeça troca de CI;
- com texto sobre pad, furo ou corpo vizinho.

Reservar ao menos **10 mm** livres à frente dos headers na direção do cabo e
**5 mm** em torno de trimpots e eventuais soquetes, ajustando para a peça
física.

## 4. Arquitetura física da BASE

O fluxo preferido é da esquerda para a direita e de cima para baixo, mantendo
blocos funcionais reconhecíveis:

| Zona | Bloco | Prioridade |
| --- | --- | --- |
| faixa esquerda | J1–J11 | fixa; chicotes curtos e sem cruzamento |
| superior esquerda/centro | entrada 9 V, proteção, V9/V5/VEE/4V5/1V8 | longe do pré e do áudio de alta impedância |
| superior centro/direita | U1 pré de mic e U9 EQ | menor caminho XLR→U1; máxima distância de clock/PT2399 |
| superior direita | U2 osciladores | longe de U1 e dos cabos XLR |
| centro | mix, shape, VCF, VCA, ENV | segue a cadeia de áudio |
| centro distante de U1 | LFO e detector CLK/TIME | conter sinais periódicos |
| inferior/uma extremidade | U3 NAB e U6–U8 PT2399 | fluxo grava→heads→lê; V5 local |

As coordenadas do SVG atual são apenas ponto de partida. O agente pode
compactar blocos, mas não deve misturá-los para eliminar espaço vazio. Espaço
vazio útil melhora isolamento, acesso e roteamento.

### Ordem de posicionamento

1. elementos mecânicos e conectores;
2. reguladores e CIs;
3. capacitores de desacoplamento;
4. componentes críticos de cada CI;
5. cadeia principal de áudio;
6. controles, CV, envelope e sinais lentos;
7. resistores/capacitores restantes;
8. jumpers;
9. textos e pontos de teste.

Após cada etapa, alinhar em grade, verificar courtyard e executar DRC.

## 5. Regras de agrupamento por circuito

### 5.1 Fonte

- D1 deve ficar imediatamente após a entrada J6/P4.
- Capacitor bulk de V9 fica junto de D1 e do ponto de distribuição.
- U5/78M05 fica próximo de U6–U8, com entrada e saída desacopladas por caminhos
  curtos.
- U4/MAX1044 e capacitores de voo formam um grupo compacto. O laço entre pinos
  2, 4, 3 e 5 não deve atravessar áudio.
- Manter U4 e suas trilhas chaveadas longe de U1, J7, entradas do EQ e nós de
  alta impedância.
- Divisores 4V5 e 1V8, seus capacitores e consumidores devem formar árvores
  curtas. **4V5 e 1V8 não são GND** e nunca entram em zona/plano GND.

### 5.2 Pré de microfone e EQ

- J7→U1 é o caminho mais sensível da placa: curto, pareado e longe de clock,
  osciladores, LFO, V5 e trilhas de saída.
- Entradas diferencial quente/fria devem ter geometria semelhante, sem grandes
  diferenças de comprimento ou vizinhança.
- R12/R13 e R57/R58 ficam juntos e simétricos; seus pares devem permanecer
  equivalentes também no roteamento.
- C1/C2 de RF ficam no combo IN conforme `pcb.md`; se também existirem na BASE,
  não substituir os capacitores do conector sem decisão no esquema.
- PRE/SEND e entradas U9 ficam dentro da zona de baixo ruído.
- Não rotear saída de U1/U9 paralela às suas entradas. Se cruzar for inevitável
  em duas camadas, cruzar aproximadamente a 90°.

### 5.3 Osciladores, LFO e CLK

- Capacitores de tempo de U2 e resistores de feedback ficam colados aos pinos
  correspondentes.
- Separar OUT_A/OUT_B dos nós de temporização e da entrada de mic.
- Conter o LFO e o detector CLK numa zona; suas trilhas não percorrem a placa
  junto a áudio.
- Nets do pino 6 dos PT2399 são sensíveis a acoplamento: curtas, sem paralelo
  longo com saída de áudio e sem laços.

### 5.4 VCF, VCA e ENV

- Q4/Q5, bias 1V8 e seus R/C ficam compactos.
- O nó ENV e gates JFET são de alta impedância: trilhas curtas, limpas e longe
  de osciladores.
- FCV/VCV chegam pelo conector e encontram seus resistores de proteção/soma
  antes de entrar na zona sensível.
- RV2 deve ser acessível com a placa instalada.

### 5.5 NAB e três PT2399

- Posicionar em ordem física U3 GRAVA → U6/H1 → U7/H2 → U8/H3 → U3 LÊ.
- Cada PT2399 recebe **100 nF** a no máximo aproximadamente **5 mm** entre VCC e
  seu retorno, além do eletrolítico local previsto.
- Componentes de filtro dos pinos do PT2399 ficam junto do respectivo chip,
  sem compartilhar trajetos estreitos de retorno.
- Separar terra analógico local dos PT2399 do retorno pulsante de V5 até a
  conexão controlada com GND; não criar planos de terra isolados.
- Mix H1/H2/H3 e entrada de U3 LÊ devem ser curtos e afastados das trilhas de
  clock/time.
- RV1 e MP20-2 precisam de acesso e distância térmica para manutenção.

### 5.6 VU analógico

- Medir o nó mono pós-VOLUME e antes dos pads/saídas.
- Projetar para movimento de 500 µA/630 Ω (≈0,315 V DC no fundo de escala),
  validado na amostra física.
- Buffer/retificador e ajuste ficam na BASE, próximos da saída, mas afastados
  de U1/J7 e das entradas de baixo nível.
- A entrada do medidor deve ser ≥100 kΩ e sua falha não pode abrir o áudio.
- J10 é dedicado a `M+`/`M−` do movimento e `L+`/`L−` do filamento 6–12 V; não
  reutilizar pinos, GND sensível ou chicotes existentes.
- Retorno do movimento/iluminação deve chegar à distribuição de alimentação
  sem compartilhar garganta com `MIC_LOW`.
- Só definir footprint, recorte e posição após medir corpo, profundidade,
  fixação, tolerâncias e corrente da iluminação na amostra física.

### 5.7 LEDs indicadores

- POWER permanece em J6; CLIP, GATE/ENV, LFO, OSC A/B, H1–H3 e STACK usam J11.
- CLIP deriva do detector de saída/VU, com retenção visual, sem limiter no
  caminho de áudio.
- CLIP, GATE/ENV e LFO usam drivers discretos SMD de alta impedância; não
  estender diretamente os respectivos nós analógicos pelo chicote.
- OSC A/B, H1–H3 e STACK devem usar segundo polo isolado da chave ou driver
  equivalente. Nunca inserir LED/resistor no contato que conduz áudio.
- Usar LED vermelho difuso de 3 mm/baixo consumo; dimensionar inicialmente para
  1,5 mA por LED (4,7 kΩ inicial em V9) e recalcular com Vf, queda do driver,
  brilho, temperatura e peça exata.
- Alimentação e retorno de J11 seguem até a distribuição de potência sem usar
  o retorno do pré, das referências ou dos PT2399.
- Posicionar drivers junto da origem do sinal ou de J11, conforme produza o
  menor laço e menor acoplamento.

## 6. Alimentação, terra e desacoplamento

### Terra

- Usar **uma única net GND** e evitar “AGND/DGND” inventados.
- Não dividir plano de terra. Separação é obtida por placement e controle do
  caminho de retorno.
- O retorno de entrada de mic não deve compartilhar trecho estreito com
  PT2399, LED, regulador ou charge pump.
- No perfil de uma face, criar tronco GND robusto e conexões curtas em árvore;
  preencher zona somente depois do roteamento crítico.
- No perfil de duas camadas, preservar plano contínuo sob os sinais. Não passar
  sinal sobre corte, keepout ou garganta estreita do plano.
- Remover ilhas de cobre não conectadas.

### Desacoplamento

- Todo CI deve ter 100 nF local por trilho de alimentação, ligado primeiro ao
  pino e depois ao plano/tronco, sem “passear” por outro componente.
- Meta: corpo do capacitor a até **5 mm** do pino; caminho total do laço o menor
  possível.
- Bulk não substitui 100 nF local e 100 nF local não substitui bulk.
- U1/U3/U9 em ±9 V precisam desacoplamento em V9 e VEE conforme esquema.
- PT2399 nunca recebe 9 V. Marcar V5 claramente e validar ausência de curto
  V5–V9 antes da aprovação.

## 7. Classes de nets

Criar classes explícitas. Valores abaixo são do **Perfil B aprovado** e já
mantêm margem sobre os mínimos usuais da fábrica.

| Classe | Nets típicas | Largura | Clearance | Regras adicionais |
| --- | --- | ---: | ---: | --- |
| `PWR_MAIN` | entrada, V9, GND tronco | 1,00 mm | 0,25 mm | sem neck-down evitável |
| `PWR_LOCAL` | V5, VEE, 4V5, 1V8 | 0,60 mm | 0,25 mm | 4V5/1V8 não são terra |
| `MIC_LOW` | X2, X3, entradas U1 | 0,30 mm | 0,40 mm | curta, simétrica, keepout de clocks |
| `AUDIO` | cadeia principal, SEND/RCV | 0,30 mm | 0,25 mm | evitar paralelismo entrada/saída |
| `TIME_CLOCK` | OSC timing, LFO, CLK, PT p6 | 0,30 mm | 0,40 mm | manter ≥3 mm de `MIC_LOW` quando possível |
| `CONTROL_HIZ` | gates, ENV, CV somado | 0,30 mm | 0,40 mm | curta; sem ilhas e testpoints grandes |

Nomes reais devem vir do esquema. Não renomear net para “encaixar” nesta
tabela; atribuir a net existente à classe apropriada.

## 8. Regras de roteamento

Ordem obrigatória:

1. entrada de alimentação e retornos;
2. mic diferencial;
3. desacoplamentos e laços críticos;
4. V5/VEE/4V5/1V8;
5. cadeia de áudio;
6. timing/clock/LFO;
7. controles e demais sinais;
8. GND/zones;
9. jumpers e acabamento.

### Geometria

- usar segmentos a 45°; evitar ângulos agudos e zigue-zague gratuito;
- usar o menor caminho que preserve isolamento e retorno;
- evitar stubs; quando inevitáveis, mantê-los curtos;
- não reduzir trilha na saída de pad sem necessidade;
- entrar em pads de forma limpa, sem tangenciar furos;
- manter trilhas paralelas sensíveis separadas; aproximá-las somente pelo
  trecho mínimo;
- em componente manual, não passar entre pads se isso prejudicar solda ou
  retrabalho;
- não rotear sob cristal inexistente nem criar blindagem fictícia;
- vias/jumpers não são “falha”: no Perfil A, jumper explícito e testável é
  melhor que trilha impossível.

### Jumpers no Perfil A

- footprint THT próprio, referência `JPx`;
- caminho reto e curto, preferencialmente horizontal/vertical;
- não cruzar corpo alto, soquete ou área de ajuste;
- silk mostra referência e sentido;
- netlist e BOM devem refletir o jumper;
- não usar resistor de 0 Ω sem declarar essa escolha.

### Zonas

- adicionar por último;
- prioridade e net explícitas;
- thermal relief compatível com solda manual;
- remover ilhas;
- refazer fill e DRC após qualquer alteração;
- inspecionar gargalos de retorno visualmente, não apenas confiar no DRC.

## 9. Otimização de espaço

Otimizar significa reduzir área **sem piorar** ruído, montagem ou reparo.

Aplicar nesta ordem:

1. girar componentes para encurtar as conexões locais;
2. aproximar R/C do CI que servem;
3. alinhar passivos por bloco;
4. reduzir cruzamentos do ratsnest;
5. compactar apenas o bloco, mantendo separação entre blocos;
6. reavaliar acesso e roteamento;
7. só então deslocar o bloco inteiro.

Não usar:

- footprint menor que a peça comprada;
- montagem diagonal para “ganhar” milímetros sem benefício elétrico;
- passivo sob eventual CI em soquete;
- capacitor eletrolítico encostado em regulador quente;
- trilha fina como solução de congestionamento;
- courtyard sobreposto aceito por conveniência;
- autorouter como decisão final.

Um bloco é considerado bem colocado quando a maior parte de suas conexões é
local, o ratsnest cruza pouco e suas entradas/saídas apontam para os blocos
anterior/seguinte.

## 10. Pontos de teste e fabricação

Prever pads identificados, acessíveis e sem risco de curto para:

- `GND`, `V9`, `V5`, `VEE`, `4V5`, `1V8`;
- saída PRE/SEND;
- saída OSC A e OSC B;
- ENV;
- saída VCF/VCA;
- GRAVA e LÊ;
- saída H1/H2/H3 quando houver espaço.

Silkscreen mínimo:

- nome/revisão da placa;
- refs legíveis;
- pino 1 de todos os CIs e headers;
- `+` em eletrolíticos e LED;
- orientação de diodos e transistores;
- nomes de trilhos nos testpoints;
- aviso `PT2399 = 5 V`;
- indicação do lado dos componentes e, somente no Perfil A legado, do cobre.

Executar inspeção de impressão 1:1 para todo componente manual: DIP quando
usado, headers, TO-92, regulador, trimpots, eletrolíticos e furos. Footprint
“parecido” não é validado.

### Evidência não é aprovação automática

- Uma equação, tabela ou captura produzida pelo agente precisa ser recalculada
  ou conferida por fonte independente.
- Um relatório deve conter condições, unidades, revisão do circuito e limites;
  gráfico sem configuração reproduzível não vale como teste.
- Resultado “passou” deve ser calculado contra o critério original, não
  classificado pela narrativa do agente.
- Warnings e picos ocasionais não podem ser descartados sem análise.
- Mudança feita para resolver um teste exige regressão dos testes já aprovados.

## 11. Protocolo de execução via MCP

O agente deve tratar o KiCad como fonte de verdade e usar o MCP em ciclos
curtos, verificáveis e reversíveis.

### Descoberta

1. listar ferramentas e capacidades MCP disponíveis;
2. identificar operações de leitura, seleção, movimento, rotação, roteamento,
   zonas, DRC, screenshot e save;
3. não presumir nome de ferramenta, unidade, origem ou camada;
4. testar uma leitura sem mutação;
5. fazer uma alteração piloto reversível e ler de volta seu resultado.

Se o MCP não oferecer uma operação segura, o agente para e documenta a lacuna.
Não editar o arquivo S-expression do KiCad como atalho, salvo autorização
humana explícita e validação posterior pelo KiCad.

### Ciclo transacional

Para cada lote de no máximo um bloco funcional:

1. **OBSERVAR** — ler seleção, posições, orientação, nets, DRC e ratsnest;
2. **PLANEJAR** — declarar objetivo, refs afetadas e regras aplicadas;
3. **MUTAR** — mover/rotacionar poucas refs ou rotear poucas nets;
4. **LER DE VOLTA** — confirmar coordenadas, camada, orientação e conectividade;
5. **VALIDAR** — courtyard, ratsnest e DRC;
6. **SALVAR** — somente se o lote estiver íntegro;
7. **REGISTRAR** — resultado, exceções e próximo lote.

Nunca executar movimento global, autoplace, autoroute, delete-all, refill
destrutivo ou renumeração sem checkpoint e autorização específica.

### Divisão de responsabilidade

O agente pode executar autonomamente tarefas determinísticas:

- inventário, medições, aplicação de regras, alinhamento e organização;
- placement inicial de passivos locais após os componentes críticos estarem
  travados;
- roteamento de nets não críticas conforme plano aprovado;
- DRC, comparações, capturas e documentação.

Exigem aprovação humana:

- requisitos e perfil de fabricação;
- seleção ou troca de componente/footprint;
- placement de U1/U4/U5/U6–U9, conectores, retornos e componentes de timing;
- aceitação dos gates G2, G3 e G6;
- qualquer exceção, waiver ou liberação para fabricar.

Fluxo preferido: o agente propõe o placement crítico e sua evidência; o
engenheiro ajusta/aprova e bloqueia essas peças; o agente conclui passivos,
rotas não críticas, acabamento e relatórios. Se o humano posicionar uma peça,
isso não autoriza o agente a movê-la depois.

### Limite de tentativas

Não repetir placement completo “até parecer bom”. Para um mesmo bloco:

1. fazer uma proposta inicial;
2. fazer no máximo uma revisão automática baseada em feedback objetivo;
3. se ainda falhar, restaurar o último checkpoint íntegro, preservar evidências
   e solicitar placement humano dos elementos críticos;
4. retomar somente as tarefas delegadas após as peças serem bloqueadas.

Registrar número de ações, duração e motivo de cada repetição. Volume de
tokens, tempo de execução ou número de iterações não mede qualidade. Evitar
reanálise integral quando uma leitura incremental resolve.

### Concorrência em tempo real

Quando humano e agente operarem simultaneamente:

- antes de cada lote, reler revisão/timestamp e seleção atual;
- não mover item selecionado, bloqueado ou editado pelo humano;
- trabalhar apenas no bloco anunciado;
- se o estado mudar entre leitura e escrita, cancelar o lote e reler;
- salvar em checkpoints nomeados, nunca sobrescrever uma edição humana sem
  comparação;
- resolver conflito por estado atual do KiCad, não por memória da conversa.

### Checkpoints

Salvar/commit somente em estados coerentes:

- `R0-requisitos`;
- `G0-auditoria`;
- `G1-mecanica`;
- `G2-placement-blocos`;
- `G3-placement-final`;
- `G4-rotas-criticas`;
- `G5-roteamento-completo`;
- `G6-fabricacao`;
- `G7-hardware-validado`.

Não fazer commit de autosave, lock file, backup transitório ou cache.
Antes de mudança de footprint ou revisão estrutural autorizada, criar backup
legível e confirmar que ele abre no KiCad.

## 12. Gates de aprovação

### G1 — mecânica

- contorno fechado e 220×160 mm;
- quatro furos e keepouts corretos;
- J1–J9, J10 e J11 corretos, pino 1 e acesso de cabo validados;
- nenhum courtyard invade borda, furo ou conector.

### G2 — placement de blocos

- todos os footprints dentro da placa;
- blocos nas zonas previstas;
- caminho do áudio reconhecível;
- pré separado de clock/PT2399;
- power entry e reguladores corretamente localizados.
- placement crítico revisado e aprovado por humano antes de rotear.

### G3 — placement final

- zero courtyard overlap não justificado;
- distância pad–pad e fabricabilidade inspecionadas, não apenas courtyards;
- desacoplamentos e redes críticas junto aos pinos;
- polaridades/orientações conferidas com datasheet;
- trimpots, eventuais soquetes e testpoints acessíveis;
- ratsnest sem cruzamentos evitáveis dentro dos blocos.
- silkscreen sem invadir pads/furos e legível após montagem;
- aprovação humana registrada e peças críticas bloqueadas.

### G4 — rotas críticas

- mic diferencial e retornos revisados;
- charge pump contida;
- alimentação e desacoplamento completos;
- timing/clock isolados;
- DRC sem erro novo.

### G5 — roteamento completo

- zero net não roteada, salvo jumper/documentação deliberada;
- classes aplicadas;
- zonas preenchidas e sem ilhas;
- sem gargalo de retorno;
- DRC zero erros; warnings classificados individualmente.

### G6 — liberação

- ERC e DRC limpos;
- inspeção 3D e 1:1;
- Gerbers/drill ou arquivos de transferência conferidos em visualizador
  independente;
- BOM, refs e footprints consistentes;
- revisão humana de polaridade, pinagem, conectores e trilhos;
- matriz de requisitos sem falha ou exceção não aprovada;
- relatório final conforme seção 13.

### G7 — validação em hardware

G6 libera arquivos, não comprova desempenho físico. Depois da montagem:

- executar a ordem de teste de `pcb.md`, com limites e instrumentos registrados;
- medir todos os trilhos antes de inserir CIs;
- verificar ruído, crosstalk, estabilidade, aquecimento e comportamento nos
  extremos dos controles;
- testar variação de alimentação e componentes dentro dos limites seguros;
- testar temperatura quando aplicável ao uso real;
- comparar medições com simulação/requisitos e investigar discrepâncias;
- registrar retrabalho e alimentar as regras da próxima revisão.

Somente após revisão humana das medições o estado pode ser
`HARDWARE_VALIDADO`. Uma placa que liga ou produz áudio não necessariamente
atendeu aos requisitos.

## 13. Relatório obrigatório do agente

Ao terminar cada sessão, informar:

```text
Revisão/projeto:
Perfil de fabricação:
Gate alcançado:
Bloco alterado:
Refs movidas/rotacionadas:
Nets roteadas:
DRC antes/depois:
Ratsnest antes/depois:
Exceções e justificativas:
Decisões humanas pendentes:
Requisitos verificados/falhos:
Aprovação humana registrada:
Número de ações/tentativas:
Próxima ação segura:
```

O relatório final também deve listar:

- dimensões e stackup;
- regras efetivas;
- quantidade de vias ou jumpers;
- nets não roteadas;
- erros e warnings de DRC;
- footprints não validados fisicamente;
- arquivos de fabricação gerados;
- matriz requisito→evidência e exceções;
- checklist de datasheet com página/figura;
- checklist de revisão humana.

## 14. Proibições absolutas

O agente não pode:

- alterar esquema, valores, pinagem ou BOM para facilitar layout;
- ligar 4V5 ou 1V8 ao GND;
- ligar V5 ao V9;
- confiar no SVG como conectividade;
- trocar footprint sem conferir peça/datasheet;
- mover conectores/furos travados sem aprovação;
- aceitar DRC ignorado sem justificativa registrada;
- criar zona sem net;
- esconder unrouted com zona;
- remover desacoplamento;
- fabricar ou liberar arquivos com ERC/DRC bloqueante;
- declarar o layout pronto apenas porque o ratsnest chegou a zero;
- marcar teste falho como aprovado sem waiver humano rastreável;
- usar relatório, equação, simulação ou DRC gerado pelo agente como
  autovalidação;
- refazer placement completo repetidamente sem limite e sem novo diagnóstico;
- mover componente crítico já aprovado/bloqueado pelo engenheiro.

## 15. Checklist resumido para prompt do agente

```text
Leia esquema.md, pcb.md, kicad-requisitos.md e kicad-layout-agent.md.
Não inicie G0 sem aprovação humana do baseline R0.
Audite o projeto e execute somente o próximo gate.
Mantenha uma matriz requisito→evidência; não aprove a própria conclusão.
Use o KiCad/MCP como fonte de verdade; não infira nets do SVG.
Trabalhe em um bloco por lote, leia o estado antes/depois e salve checkpoint.
Preserve mecânica 220×160, furos, J1–J9, J10 do VU e J11 dos LEDs.
Priorize pré de mic, retornos, desacoplamento e isolamento de clock/PT2399.
Não altere o circuito para facilitar placement/routing.
Após uma revisão automática malsucedida, peça placement humano do bloco crítico.
Rode DRC após cada lote e pare em qualquer conflito de pinagem ou netlist.
Entregue o relatório padronizado da seção 13.
```
