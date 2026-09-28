# VOZ-9 — projeto KiCad (somente esquema)

**Sem PCB nesta revisão.** PCB só após validação humana do esquema/netlist
(DEC-001 / DEC-038).

## Abrir

1. Abrir `voz-9.kicad_pro` no KiCad 7+.
2. Editar o esquema a partir da folha raiz (`voz-9.kicad_sch`).
3. Cada retângulo abre uma folha de bloco.

## Folhas (arquivos picados)

| Arquivo | Bloco |
| --- | --- |
| `voz-9.kicad_sch` | Índice / raiz |
| `01-fonte.kicad_sch` | Fonte |
| `02-osc.kicad_sch` | Osciladores |
| `03-noise.kicad_sch` | Noise |
| `04-mix-eq.kicad_sch` | Mix + EQ |
| `05-shape.kicad_sch` | Shape |
| `06-vcf.kicad_sch` | VCF |
| `07-vca.kicad_sch` | VCA |
| `08-lfo.kicad_sch` | LFO |
| `09-echo.kicad_sch` | Echo |
| `10-saida.kicad_sch` | Saída + VU |
| `11-indicadores.kicad_sch` | Indicadores |
| `12-conectores.kicad_sch` | Conectores |

## Padronização visual

- Papel **A3**, título `VOZ-9 / <Bloco>`, revisão **R0.1**, empresa VOZ-9.
- Comentários do bloco apontam para `esquema.md`, requisitos e playbook.
- Fluxo de sinal **esquerda → direita**.
- Alimentação no topo; GND na base.
- Labels hierárquicos nas bordas esquerda/direita.
- **Um bloco funcional por folha** — não misturar etapas.
- Classes de net já definidas no `.kicad_pro` (PWR_MAIN, PWR_LOCAL, MIC_LOW,
  AUDIO, TIME_CLOCK, CONTROL_HIZ).

## Regenerar esqueleto

```bash
python3 _gen_project.py
```

Sobrescreve apenas a estrutura; não use depois que o circuito estiver
preenchido sem backup.
