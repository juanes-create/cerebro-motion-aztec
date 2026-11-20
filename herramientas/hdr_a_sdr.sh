#!/bin/zsh
# Brutos de iPhone en HDR (HLG / Dolby Vision): ffmpeg sin convertir los deja LAVADOS y parece que le cambiaste el color
# a la cámara. Se convierten con el conversor de Apple (mismos tiempos, ya girados) antes de cualquier otro paso.
# Uso: herramientas/hdr_a_sdr.sh VIDEO [preset=Preset1920x1080]   → VIDEO.sdr.mov   (solo Mac)
set -e
V="$1"; P="${2:-Preset1920x1080}"
[ -f "$V" ] || { echo "uso: hdr_a_sdr.sh VIDEO [preset]"; exit 1; }
TR=$(ffprobe -v error -select_streams v -show_entries stream=color_transfer -of csv=p=0 "$V")
case "$TR" in
  arib-std-b67|smpte2084) echo "HDR detectado (${TR}): convirtiendo a SDR…" ;;
  *) echo "✓ no es HDR (${TR:-sin dato}): no hace falta convertir"; exit 0 ;;
esac
command -v avconvert >/dev/null || { echo "✗ falta avconvert (viene con macOS)"; exit 2; }
OUT="${V%.*}.sdr.mov"
avconvert -s "$V" -o "$OUT" -p "$P" --replace
echo "✓ ${OUT}  ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") s; compara un cuadro contra el original)"
