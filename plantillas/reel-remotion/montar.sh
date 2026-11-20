#!/bin/zsh
# Une el render con la voz ORIGINAL (intacta) + los clics del cursor + los efectos de efectos.json, sin recodificar el video.
# Uso: ./montar.sh "Mi reel EDITADO.mp4"      (nombre NUEVO: nunca sobrescribas tu base ni una entrega anterior)
set -e
cd "${0:h}"
H="${0:A:h}/../../herramientas"
SAL="${1:-out/Reel EDITADO.mp4}"
V=$(python3 -c "import json;print(json.load(open('src/datos/config.json')).get('fuente',''))")
[ -f "$V" ] || { echo "✗ no sé cuál es el video con la voz: corre antes ./preparar.sh VIDEO"; exit 1; }
FX=()
[ -f efectos.json ] && FX+=(--cues efectos.json)
python3 -I "$H/efectos.py" --voz "$V" --cursor src/datos/cursor.json "${FX[@]}" --salida out/mezcla.m4a
ffmpeg -v error -y -i out/reel-sin-audio.mp4 -i out/mezcla.m4a -map 0:v -map 1:a -c copy -shortest -movflags +faststart "$SAL"
python3 -I "$H/verificar.py" streams "$SAL"
echo "✓ ${SAL}"
