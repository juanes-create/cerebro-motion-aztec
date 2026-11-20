#!/bin/zsh
# Prepara el proyecto con TU video: copia una versión liviana a public/video, fija la duración exacta,
# transcribe con tiempos por palabra y mide la cabeza del presentador.
# Uso: ./preparar.sh ../../videos/mi-reel.mp4        (el video ya cortado con herramientas/cortar.py, si aplica)
set -e
cd "${0:h}"
V="${1:A}"
[ -f "$V" ] || { echo "uso: ./preparar.sh VIDEO"; exit 1; }
H="${0:A:h}/../../herramientas"
W=$(ffprobe -v error -select_streams v -show_entries stream=width -of csv=p=0 "$V")
HH=$(ffprobe -v error -select_streams v -show_entries stream=height -of csv=p=0 "$V")
python3 -c "import sys; w,h=${W},${HH}; sys.exit(0 if abs(w/h-9/16)<0.01 else 1)" || echo "⚠ el video no es 9:16 (${W}×${HH}); se escalará a 1080×1920 con recorte al centro"
mkdir -p public/video ref out
# Archivo COPIADO (un enlace simbólico no carga en OffthreadVideo) y keyframe cada 15 cuadros: Remotion busca rápido.
ffmpeg -v error -y -i "$V" -an -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -crf 12 -preset veryfast -g 15 -pix_fmt yuv420p public/video/bruto.mp4
N=$(ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets -of csv=p=0 public/video/bruto.mp4)
python3 - "$N" "$V" <<'PY'
import json, sys
json.dump({"fps": 30, "cuadros": int(sys.argv[1]), "video": True, "fuente": sys.argv[2]}, open("src/datos/config.json", "w"), indent=1, ensure_ascii=False)
PY
echo "✓ public/video/bruto.mp4 · ${N} cuadros ($(python3 -c "print(round(${N}/30,2))") s)"
python3 -I "$H/transcribir.py" "$V" --carpeta src/datos
python3 -I "$H/cabeza.py" "$V" || echo "⚠ no se pudo medir la cabeza (¿compilaste las herramientas de Vision?)"
echo "\nListo. Abre el estudio con: npm run dev   ·   cuadros sueltos: ./still.sh 1.5 6 12"
