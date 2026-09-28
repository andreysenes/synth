# Instruções para agentes — VOZ-9

## Trabalho de PCB no KiCad

Antes de posicionar, mover, rotacionar ou rotear qualquer item:

1. leia `esquema.md`, `pcb.md` e `kicad-layout-agent.md`;
2. execute o gate G0 de `kicad-layout-agent.md`;
3. confirme o perfil de fabricação;
4. trate o projeto KiCad e sua netlist como fonte de verdade;
5. pare se houver conflito entre esquema, BOM, footprint e documentação.

Execute somente um bloco funcional por lote via MCP. Leia o estado antes e
depois de cada mutação, rode DRC, salve um checkpoint coerente e entregue o
relatório da seção 13.

Não altere circuito, valores, pinagem, footprints, contorno, furos ou conectores
para facilitar o layout sem aprovação humana explícita.
