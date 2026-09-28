# VOZ-9 — auditoria do teste digital para requisitos

Revisão: 2026-09-28

Escopo: `painel.html`, testes SPICE, painel físico e baseline KiCad.

## 1. Regra de interpretação

O teste digital mistura três categorias:

1. **função do produto** — deve existir no esquema e na PCB;
2. **modelo aproximado** — representa uma função, mas não define seu circuito;
3. **instrumentação do simulador** — serve para testar e não vai para a placa.

Nada deve virar hardware apenas por aparecer na interface do navegador. A coluna
“Destino” abaixo é a decisão de escopo.

## 2. Inventário do produto

### Controles e interfaces

| Grupo | Implementado no teste digital | Destino físico |
| --- | --- | --- |
| 17 pots | OSC A, OSC B, AMOUNT, PRE, OSC IN, LOW, MID F, MID G, HIGH, RATE, DEPTH, SHAPE, CUTOFF, TIME, WET, F-BACK, VOLUME | obrigatório, painel por chicotes |
| 9 alavancas | OSC A, OSC B, TREM, MODE, DRONE/GATE, H1, H2, H3, STACK | obrigatório, painel por chicotes |
| 1 botão | GATE momentâneo | obrigatório |
| 11 patches | A, B, IN, FILT, FCV, VCV, LFO, ECV, CLK, SEND, RCV | obrigatório |
| entrada/saída | XLR/COMBO modelado parcialmente na lateral da UI | dois combos físicos conforme esquema |
| alimentação | não desenhada na UI | P4 9 V centro-negativo + LED piloto |
| VU | pico/clip textual pós-saída | VU analógico de ponteiro obrigatório |
| indicadores | CLIP, GATE/ENV e TREM/FLUT aparecem apenas como texto/cor | adicionar LEDs CLIP, GATE/ENV e LFO, além de OSC A/B, H1–H3 e STACK |

### Funções sonoras

| ID | Função observada | Modelo digital | Requisito de hardware |
| --- | --- | --- | --- |
| DIG-001 | dois osciladores quadrados, enable e mix AMOUNT | Web Audio + SPICE parcial | implementar conforme esquema |
| DIG-002 | noise de fundo | Web Audio + SPICE isolado | implementar e validar nível |
| DIG-003 | PRE e crossfade OSC IN | Web Audio; pots no SPICE | implementar pré real e crossfade |
| DIG-004 | EQ LOW/MID F/MID G/HIGH pós-mix | Web Audio; apenas pots no SPICE | implementar U9 e testar curva |
| DIG-005 | clip/shape assimétrico | Web Audio + SPICE | implementar MP20 e validar |
| DIG-006 | VCF com cutoff e FCV | Web Audio + SPICE parcial | implementar JFET e entrada CV |
| DIG-007 | VCA, DRONE/GATE e envelope da fala | Web Audio + SPICE parcial | implementar circuito analógico |
| DIG-008 | LFO TREM/flutter, RATE e DEPTH | Web Audio + SPICE | implementar duas faixas e centro off |
| DIG-009 | MODE pitch/centro/time | Web Audio; harness SPICE parcial | implementar três destinos |
| DIG-010 | três heads, H1–H3, TIME, WET e F-BACK | Web Audio + atraso SPICE comportamental | implementar três PT2399 |
| DIG-011 | STACK em série | somente Web Audio | implementar e criar teste SPICE |
| DIG-012 | saturação e filtragem tipo fita/NAB | Web Audio aproximado + SPICE NAB | implementar U3/MP20 e correlacionar |
| DIG-013 | feedback chegando à auto-oscilação | Web Audio + SPICE aproximado | limitar por RV1 e validar estabilidade |
| DIG-014 | FILT quebra o normal SHAPE→VCF | Web Audio + harness SPICE | implementar jack normalizado |
| DIG-015 | SEND/RCV normalizado | Web Audio incompleto | implementar tap SEND e retorno real |
| DIG-016 | patches LFO→FCV/VCV/ECV | Web Audio parcial | preservar entradas e escalas elétricas |
| DIG-017 | CLK alterando tempo | UI sem fonte de clock real | implementar detector analógico do esquema |
| DIG-018 | saída mono para P10 e XLR atenuado | navegador duplica mono em estéreo | implementar somente saídas físicas documentadas |
| DIG-019 | VU de saída com indicação de pico/clip | texto no navegador | implementar VU analógico pós-VOLUME |

## 3. Instrumentação que não pertence à PCB

| Item da UI | Motivo |
| --- | --- |
| carregar WAV | fonte de teste |
| selecionar interface USB/microfone | fonte de teste |
| “Só entrada (muta OSC)” | atalho de teste, não controle do painel |
| Tocar/Parar | transporte do navegador |
| osciloscópio canvas | instrumento virtual |
| texto de frequência/modo/ENV | telemetria do simulador |
| exportar `.inc` | ferramenta de engenharia |
| saída stereo L/R do navegador | conveniência do Web Audio; produto é mono |
| limiter digital | proteção do áudio do navegador, não estágio do esquema |
| cabos demo pré-carregados | cenário de teste, não normalização física |

Não há elementos LED de status em `painel.html`. O único LED anteriormente
definido era o piloto de 9 V em `painel.svg`/J6. A decisão DEC-015 acrescenta
CLIP, GATE/ENV, LFO pulsante, OSC A/B, H1–H3 e STACK como indicadores físicos.
DEC-016/017 definem LED vermelho difuso de 3 mm e baixo consumo para todos os
10 indicadores. São requisitos novos derivados dos estados da interface e das
chaves, não circuitos já validados pela simulação.

## 4. Cobertura e lacunas

| Área | Web Audio | SPICE | Necessário antes do PCB |
| --- | --- | --- | --- |
| fonte/rails/LED | não | parcial/ideal | esquema real + carga/térmica |
| U1 pré e combos | comportamental | ausente | teste do pré, CMRR, ganho e pads |
| mix + U9 EQ | comportamental | ausente | teste AC/transiente completo |
| osciladores/FM/noise | sim | testes separados | integrar e analisar tolerâncias |
| shape/VCF/VCA/ENV | sim | testes separados | teste integrado e extremos |
| LFO/MODE/CV | parcial | parcial | validar todos os destinos e entradas externas |
| PT2399/TIME/CLK | atraso ideal | modelos separados | integrar pin6, CLK e três chips |
| STACK | sim | ausente | adicionar teste |
| SEND/RCV | incompleto | harness incompleto | validar tap, normal e retorno |
| J7/J8/J9 | parcial | harness incompleto | continuidade e função pin a pin |
| VU | debug somente | ausente | escolher circuito/display, simular e adicionar ao esquema |

O PCB não pode começar enquanto as lacunas elétricas acima não estiverem no
esquema KiCad e os blocos críticos não tiverem evidência suficiente.

### Validade dos resultados existentes

Os logs persistidos em `sim/out/` não comprovam aprovação da suíte:

- `01_osc` e `07_lfo` terminam com timestep insuficiente e vetores sem dados;
- `05_vcf` termina com matriz singular e vetor de saída indisponível;
- `01_fm` possui medidas fora do intervalo;
- `04_shape`, `06_vca`, `08_pin6`, `08_echo` e `harness_check` apresentam
  falhas de convergência/matriz singular;
- vários arquivos ainda imprimem `*_DONE`, pois esse marcador é emitido mesmo
  quando a análise falha;
- o ambiente atual não possui `ngspice`, portanto os testes não foram
  reproduzidos nesta auditoria.

Consequência: os resultados atuais têm estado `FALHOU` ou `NÃO REPRODUZIDO`,
nunca `VERIFICADO`. O runner deve falhar ao encontrar erro de análise, vetor
ausente, medida falha ou marcador com valor não numérico.

## 5. VU físico derivado do teste digital

O medidor do navegador lê o sinal final depois de `master/volume` e do limiter
virtual. O hardware não terá limiter digital; portanto, o ponto físico deve ser
o sinal mono **pós-VOLUME e antes dos pads/saídas**, sem carregar o áudio.

Requisitos mínimos:

- movimento analógico de ponteiro, com escala VU e zona de sobrecarga;
- tipo compacto nominal de 37 × 35 × 35 mm/21 g, movimento 500 µA/630 Ω e
  fundo de escala elétrico aproximado de 0,315 V DC;
- entrada do medidor com impedância mínima de 100 kΩ;
- driver/retificador de precisão e ajuste na BASE, desacoplados e afastados do
  pré de microfone;
- retorno de corrente do mostrador separado do retorno sensível do pré;
- mostrador no painel ligado por J10, com pares separados para movimento e
  iluminação quente por filamento 6–12 V;
- ajuste/calibração acessível;
- falha ou desconexão do VU não pode interromper nem degradar a saída;
- referência de 0 VU, balística, modo da iluminação, consumo, profundidade e
  recorte devem ser aprovados/medidos antes do esquema final.
- o manual classifica o medidor como frágil e exige ambiente seco; fixação,
  alívio de tração, embalagem e comissionamento devem refletir isso.
- a instrução genérica de conexão ao áudio não substitui o driver/retificador
  protegido requerido pelo projeto.
- alegações comerciais de precisão/estabilidade e tolerância dimensional de
  1–2 cm não são evidência; amostra e lote precisam de medição/calibração.

## 6. Inconsistências encontradas

- `painel.html` não desenha COMBO IN/OUT, LED ou P4, embora sejam físicos.
- a interface não contém LEDs de estado; DEC-015 converte estados úteis em nove
  LEDs físicos novos, ainda sem circuito simulado.
- Jack IN não percorre o caminho completo para AMOUNT na simulação.
- SEND não possui tap de áudio observável; RCV é apenas um gate aproximado.
- CLK, FCV, VCV e ECV não recebem fontes elétricas externas reais.
- STACK e TIME contínuo existem no Web Audio, mas não no teste SPICE integrado.
- U1 e U9 não possuem testes SPICE completos.
- `painel.cir` e `sim/README.md` ainda mencionam J1–J8 apesar de existir J9.
- `painel_state.inc` não deriva automaticamente as duas posições de TREM.
- o WAV padrão `sim/audio/twinkle.wav` não existe no repositório.
- alguns marcadores de sucesso não são reconhecidos pelo resumo do runner.
- inversamente, a presença de `*_DONE` não impede logs com erro de solver ou
  medida, gerando falso positivo.

Essas diferenças não autorizam mudar o produto para coincidir com o simulador.
O esquema aprovado é a fonte de verdade; a simulação deve ser corrigida ou
explicitamente limitada.
