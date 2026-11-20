#!/bin/zsh
# Cuadros sueltos para revisar (barato: corrige aquí, no después del render).
# Uso: ./still.sh 1.5 6.4 12   → ref/st-<segundo>.png  +  ref/mosaico.jpg con las líneas de las zonas de peligro
set -e
cd "${0:h}"
mkdir -p ref
[ -d build ] && [ "${REBUILD:-1}" = "0" ] || { rm -rf build && npx remotion bundle src/index.ts --out-dir build --log=error >/dev/null; }
L=()
for s in "$@"; do
  f=$(python3 -c "print(round(${s}*30))")
  npx remotion still build Reel "ref/st-${s}.png" --frame=${f} --log=error >/dev/null
  L+=("ref/st-${s}.png")
done
# mosaico con guías: rojo = zonas que tapa Instagram (arriba 270, abajo 1480, derecha 960)
ARGS=(); for f in $L; do ARGS+=(-i "$f"); done
G=""; for i in $(seq 0 $((${#L}-1))); do G+="[${i}:v]drawbox=y=270:w=iw:h=4:color=red@0.8:t=fill,drawbox=y=1480:w=iw:h=4:color=red@0.8:t=fill,drawbox=x=960:w=4:h=ih:color=red@0.8:t=fill,scale=360:-2[m${i}];"; done
S=""; for i in $(seq 0 $((${#L}-1))); do S+="[m${i}]"; done
if [ ${#L} -gt 1 ]; then ffmpeg -v error -y "${ARGS[@]}" -filter_complex "${G}${S}hstack=inputs=${#L}" ref/mosaico.jpg; else ffmpeg -v error -y "${ARGS[@]}" -filter_complex "${G%;}" -map "[m0]" ref/mosaico.jpg; fi
echo "✓ ${#L} cuadros · ref/mosaico.jpg"
