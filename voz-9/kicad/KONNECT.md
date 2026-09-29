# Konnect + VOZ-9

[Konnect](https://github.com/mixelpixx/Konnect) (v0.12.1) é o MCP server usado para
editar o esquema em tempo real.

## Neste ambiente (Cloud Agent)

### KiCad

| Ferramenta | Caminho | Versão |
| --- | --- | --- |
| KiCad 10 (preferido) | `/workspace/tools/kicad10/squashfs-root/usr/bin/kicad` | **10.0.6** AppImage lite |
| `kicad-cli` 10 | `/workspace/tools/kicad10/squashfs-root/usr/bin/kicad-cli` | **10.0.6** |
| Wrappers PATH | `~/.local/bin/kicad` e `kicad-cli` | apontam para o 10 |
| KiCad 7 (apt) | `/usr/bin/kicad` | 7.0.11 — legado; não use para este projeto |

Abrir o projeto:

```bash
kicad /workspace/voz-9/kicad/voz-9.kicad_pro
```

### Konnect

Binário:

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

1. **Edição de esquema** — Konnect grava `.kicad_sch` direto.
2. **GUI ao vivo** — abra o projeto com **KiCad 10** (`kicad` no PATH / atalho “KiCad 10”).
3. Habilite *Preferences → Plugins → Enable KiCad API* e, se quiser IPC no
   Konnect, preencha `ipc_address` em `konnect.toml`.
4. O `kicad-cli` 10 abre as folhas do Konnect (verificado com `01-fonte`).

## Reinstalar KiCad 10

```bash
curl -sL -o /tmp/kicad10-lite.AppImage.tar \
  https://downloads.kicad.org/kicad/linux/explore/stable/download/kicad-10.0.6-x86_64-lite.AppImage.tar
mkdir -p /workspace/tools/kicad10
tar xf /tmp/kicad10-lite.AppImage.tar -C /workspace/tools/kicad10
chmod +x /workspace/tools/kicad10/*.AppImage
cd /workspace/tools/kicad10 && ./*.AppImage --appimage-extract
```

## Reinstalar binário Konnect

```bash
curl -sL -o /tmp/konnect.tgz \
  https://github.com/mixelpixx/Konnect/releases/download/v0.12.1/konnect-v0.12.1-x86_64-unknown-linux-gnu.tar.gz
mkdir -p /workspace/tools/konnect
tar xzf /tmp/konnect.tgz -C /workspace/tools/konnect
chmod +x /workspace/tools/konnect/konnect
```

## Folha atual

`01-fonte.kicad_sch` — alimentação alinhada a `esquema.md` §0 (D1, LED, 78M05,
MAX1044 via símbolo LMC7660, 4V5, 1V8).
