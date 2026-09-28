# Konnect + VOZ-9

[Konnect](https://github.com/mixelpixx/Konnect) (v0.12.1) é o MCP server usado para
editar o esquema em tempo real.

## Neste ambiente (Cloud Agent)

Binário instalado em:

```text
/workspace/tools/konnect/konnect
```

Config:

```text
/workspace/konnect.toml
/workspace/.mcp.json
```

Cliente Python auxiliar: `/workspace/tools/konnect_client.py`

Skills instaladas via `konnect init` em `~/.claude/skills/`.

### Realtime

1. **Edição de esquema** — Konnect grava `.kicad_sch` direto (não precisa do GUI).
2. **Acompanhar ao vivo** — no desktop com **KiCad 10**:
   - abrir `voz-9/kicad/voz-9.kicad_pro`;
   - habilitar *Preferences → Plugins → Enable KiCad API*;
   - instalar o PCM `konnect-pcm-*-linux.zip` ou apontar o MCP para o binário;
   - opcional: `open_schematic_viewer` / `schematic-viewer` no root sheet.
3. Este VM tem **KiCad 7** via apt: `kicad-cli` local **não** abre folhas
   escritas pelo Konnect (falha de load). Use KiCad **10** no desktop para GUI/ERC
   oficial. A validação de conectividade do Konnect (`validate_component_connections`,
   `export_netlist_summary`) funciona aqui.

## Reinstalar binário

```bash
curl -sL -o /tmp/konnect.tgz \
  https://github.com/mixelpixx/Konnect/releases/download/v0.12.1/konnect-v0.12.1-x86_64-unknown-linux-gnu.tar.gz
mkdir -p /workspace/tools/konnect
tar xzf /tmp/konnect.tgz -C /workspace/tools/konnect
chmod +x /workspace/tools/konnect/konnect
```

## Folha atual

`01-fonte.kicad_sch` — alimentaçao alinhada a `esquema.md` §0 (D1, LED, 78M05,
MAX1044 via simbolo LMC7660, 4V5; 1V8 com valores TODO).
