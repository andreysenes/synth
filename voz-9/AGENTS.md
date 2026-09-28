# Instruções para agentes — VOZ-9

## Trabalho de PCB no KiCad

Antes de posicionar, mover, rotacionar ou rotear qualquer item:

1. leia `esquema.md`, `pcb.md`, `kicad-requisitos.md` e
   `kicad-layout-agent.md`;
2. feche e obtenha aprovação humana do gate R0 de requisitos;
3. execute o gate G0 de `kicad-layout-agent.md`;
4. confirme o perfil de fabricação;
5. trate o projeto KiCad e sua netlist como fonte de verdade;
6. mantenha a matriz requisito→evidência e o checklist dos datasheets;
7. pare se houver conflito entre esquema, BOM, footprint e documentação.

Execute somente um bloco funcional por lote via MCP. Leia o estado antes e
depois de cada mutação, rode DRC, salve um checkpoint coerente e entregue o
relatório da seção 13.

Placement conectado e DRC limpo não significam layout aprovado. Um humano deve
aprovar e bloquear os componentes críticos antes do roteamento. Após uma
proposta e uma revisão automática malsucedida, preserve o checkpoint e devolva
o placement crítico ao engenheiro; não repita o layout inteiro indefinidamente.

Não altere circuito, valores, pinagem, footprints, contorno, furos ou conectores
para facilitar o layout sem aprovação humana explícita.
