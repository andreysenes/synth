#!/usr/bin/env bash
# VOZ-9 SPICE runner — run from voz-9/sim/
# Usage: ./run.sh [block]
#   block = 00_fonte | 01_osc | 01_fm | 02_noise | 04_shape | 05_vcf |
#           06_vca | 07_lfo | 08b_nab | 08_pin6 | 08_echo | harness_check |
#           09_vco | all

set -euo pipefail
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

if ! command -v ngspice >/dev/null 2>&1; then
  echo "ngspice not found. Install with: brew install ngspice" >&2
  exit 1
fi

mkdir -p out

run_one() {
  local name="$1"
  local cir="${name}.cir"
  if [[ ! -f "$cir" ]]; then
    echo "missing $cir" >&2
    return 1
  fi
  echo "=== $cir ==="
  if ngspice -b -o "out/${name}.log" "$cir"; then
    :
  else
    echo "ngspice failed — see out/${name}.log" >&2
    return 1
  fi
  echo "log → out/${name}.log"
  if grep -E '_DONE|_OK|SOURCE_OK' "out/${name}.log" >/dev/null 2>&1; then
    echo "OK markers found"
  else
    echo "(no DONE marker — check log for errors)"
  fi
}

BLOCKS=(
  00_fonte
  01_osc
  01_fm
  02_noise
  04_shape
  05_vcf
  06_vca
  07_lfo
  08b_nab
  08_pin6
  08_echo
  harness_check
  09_vco
)

target="${1:-all}"

if [[ "$target" == "all" ]]; then
  fail=0
  for b in "${BLOCKS[@]}"; do
    run_one "$b" || fail=1
  done
  exit $fail
fi

target="${target%.cir}"
run_one "$target"
