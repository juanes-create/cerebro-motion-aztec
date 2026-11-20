#!/bin/zsh
# Hoja de contacto: un cuadro cada N segundos en una sola imagen, para ver el encuadre, los cortes y lo que ya viene quemado.
# Uso: herramientas/hoja.sh VIDEO [cada_segundos=3] [desde=0] [duracion=todo]
set -e
V="$1"; N="${2:-3}"; SS="${3:-0}"; T="${4:-}"
[ -f "$V" ] || { echo "uso: hoja.sh VIDEO [cada_s] [desde] [duracion]"; exit 1; }
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
[ -n "$T" ] || T=$(python3 -c "print(${D}-${SS})")
n=$(python3 -c "import math;print(max(1,math.ceil(${T}/${N})))")
W=$(ffprobe -v error -select_streams v -show_entries stream=width -of csv=p=0 "$V")
H=$(ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 "$V")
if [ "${W}" -lt "${H}" ]; then SC="216:384"; COLS=11; else SC="384:216"; COLS=6; fi
ROWS=$(python3 -c "import math;print(math.ceil(${n}/${COLS}))")
OUT="${V%.*}.hoja.jpg"
ffmpeg -v error -y -ss "${SS}" -t "${T}" -i "$V" -vf "fps=1/${N},scale=${SC},drawtext=text='%{pts\\:hms}':x=6:y=6:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6,tile=${COLS}x${ROWS}" -frames:v 1 "$OUT" 2>/dev/null \
  || ffmpeg -v error -y -ss "${SS}" -t "${T}" -i "$V" -vf "fps=1/${N},scale=${SC},tile=${COLS}x${ROWS}" -frames:v 1 "$OUT"
echo "✓ ${OUT}  (${n} cuadros, uno cada ${N} s desde ${SS} s)"
